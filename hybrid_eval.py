"""
Hybrid evaluation: LLM-as-judge + retrieval metrics on COT-indexed chunks.

Runs the full 171-question eval against a FAISS index built from COT English
translations, scoring with both an LLM judge (factual accuracy) and retrieval
metrics (Recall@k, MRR).

Usage:
    python hybrid_eval.py                                    # all 171 questions
    python hybrid_eval.py --limit 20 --verbose               # quick test
    python hybrid_eval.py --judge-model gemma3:12b           # local judge
    python hybrid_eval.py --skip-judge                       # retrieval metrics only
    python hybrid_eval.py --skip-retrieval                   # judge only
"""

import argparse
import json
import os
import sys
import time
from collections import Counter
from pathlib import Path

import faiss
import numpy as np
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gemma3:12b")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")

# ---------------------------------------------------------------------------
# Author matching
# ---------------------------------------------------------------------------

AUTHOR_ALIASES = {
    "virgil": ["vergilius"], "horace": ["horatius"], "caesar": ["caesar"],
    "cicero": ["cicero"], "ovid": ["ovidius"], "seneca": ["seneca"],
    "tacitus": ["tacitus"], "juvenal": ["juvenal"], "lucretius": ["lucretius"],
    "catullus": ["catullus"], "apuleius": ["apuleius"], "homer": ["homer"],
    "plato": ["plato"], "sophocles": ["sophocles"], "euripides": ["euripides"],
    "aristophanes": ["aristophanes"], "aeschylus": ["aeschylus"],
    "herodotus": ["herodotus"], "thucydides": ["thucydides"], "pindar": ["pindar"],
    "hesiod": ["hesiod"], "xenophon": ["xenophon"], "longus": ["longus"],
    "plutarch": ["plutarch"], "petronius": ["petronius"], "sallust": ["sallust"],
}


def author_matches(chunk_author: str, eval_author: str) -> bool:
    ca = chunk_author.lower()
    ea = eval_author.lower()
    if ea in ca:
        return True
    for alias in AUTHOR_ALIASES.get(ea, []):
        if alias in ca:
            return True
    return False


# ---------------------------------------------------------------------------
# Embedding + FAISS
# ---------------------------------------------------------------------------

_embed_model = None


def get_embed_model(model_name: str):
    global _embed_model
    if _embed_model is None:
        from sentence_transformers import SentenceTransformer
        print(f"Loading embedding model: {model_name}")
        _embed_model = SentenceTransformer(model_name)
    return _embed_model


def embed_texts(texts: list[str], model_name: str) -> np.ndarray:
    model = get_embed_model(model_name)
    vectors = model.encode(
        texts, batch_size=64, show_progress_bar=True, normalize_embeddings=True
    )
    return np.array(vectors, dtype=np.float32)


def build_index(chunks: list[dict], text_field: str, model_name: str):
    """Build FAISS index from chunks using the specified text field."""
    texts = [c.get(text_field, "") for c in chunks]
    vectors = embed_texts(texts, model_name)
    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(vectors)
    return index


# ---------------------------------------------------------------------------
# Retrieval
# ---------------------------------------------------------------------------

def retrieve(index, chunks, query_vector, k=12):
    """Retrieve top-k chunks for a query vector."""
    scores, indices = index.search(query_vector.reshape(1, -1), k)
    results = []
    for rank, (score, idx) in enumerate(zip(scores[0], indices[0])):
        if idx < 0 or idx >= len(chunks):
            continue
        chunk = chunks[idx]
        results.append({
            "rank": rank + 1,
            "score": float(score),
            "author": chunk.get("author", ""),
            "title": chunk.get("title", ""),
            "text": chunk.get("text", "")[:500],
            "cot_english": chunk.get("cot_english", "")[:500],
            "chunk_id": chunk.get("chunk_id", ""),
        })
    return results


# ---------------------------------------------------------------------------
# RAG answer generation
# ---------------------------------------------------------------------------

RAG_PROMPT = """\
You are a scholar of Classical Antiquity. Answer the question using ONLY the \
provided source passages. If the sources don't contain enough information, say so.

Sources:
{context}

Question: {question}

Answer:"""


def generate_answer(question: str, sources: list[dict], model: str) -> str:
    """Generate a RAG answer from retrieved sources."""
    context = "\n\n---\n\n".join(
        f"[{s['author']} — {s['title']}]\n{s['text']}" for s in sources
    )
    prompt = RAG_PROMPT.format(context=context, question=question)

    resp = requests.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"temperature": 0.3, "num_ctx": 8192},
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"]


# ---------------------------------------------------------------------------
# LLM-as-judge
# ---------------------------------------------------------------------------

JUDGE_PROMPT = """\
You are evaluating a RAG system that answers questions about classical literature.

Question: {question}
Expected answer (ground truth): {expected}
Retrieved sources: {sources}
RAG answer: {answer}

Score the RAG answer. Respond with a JSON object ONLY — no explanation outside the JSON.

{{
  "factual_score": <integer 0-3>,
  "source_hit": <true or false>,
  "reasoning": "<one sentence>"
}}

Scoring rubric for factual_score:
  3 = fully correct, matches the expected answer
  2 = mostly correct, minor omissions or inaccuracies
  1 = partially correct, some right elements but misses the key point
  0 = wrong, irrelevant, or clearly hallucinated

source_hit = true if at least one retrieved source is authored by {expected_author}.\
"""


def judge_answer(question, expected, expected_author, rag_answer, sources, model):
    """Score a RAG answer with LLM-as-judge."""
    sources_str = "; ".join(
        f"{s['author']} — {s['title']}" for s in sources
    ) or "none"

    prompt = JUDGE_PROMPT.format(
        question=question,
        expected=expected,
        sources=sources_str,
        answer=rag_answer[:2000],
        expected_author=expected_author,
    )

    try:
        resp = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "options": {"temperature": 0.0, "num_ctx": 4096},
                "format": "json",
            },
            timeout=120,
        )
        resp.raise_for_status()
        raw = resp.json()["message"]["content"]
        result = json.loads(raw)
        result["factual_score"] = int(result.get("factual_score", 0))
        result["source_hit"] = bool(result.get("source_hit", False))
        result["reasoning"] = str(result.get("reasoning", ""))
        return result
    except Exception as e:
        return {"factual_score": -1, "source_hit": False, "reasoning": f"ERROR: {e}"}


# ---------------------------------------------------------------------------
# Retrieval metrics
# ---------------------------------------------------------------------------

def compute_retrieval_metrics(results: list[dict], k_values=[1, 5, 10, 20]):
    """Compute Recall@k and MRR from per-question results."""
    n = len(results)
    if n == 0:
        return {}

    metrics = {}
    for k in k_values:
        hits = sum(
            1 for r in results
            if r.get("first_correct_rank") is not None
            and r["first_correct_rank"] <= k
        )
        metrics[f"recall_at_{k}"] = round(hits / n, 3)

    mrr = sum(
        1.0 / r["first_correct_rank"]
        for r in results
        if r.get("first_correct_rank") is not None
    ) / n
    metrics["mrr"] = round(mrr, 3)

    return metrics


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run_pipeline(args):
    # Load COT chunks
    with open(args.chunks, encoding="utf-8") as f:
        chunks = [json.loads(line) for line in f]
    print(f"Loaded {len(chunks)} COT chunks")

    # Load eval questions
    with open(args.questions, encoding="utf-8") as f:
        questions = [json.loads(line) for line in f]
    if args.limit:
        questions = questions[:args.limit]
    print(f"Evaluating {len(questions)} questions")

    # Build FAISS index from COT English
    print(f"\nBuilding FAISS index from cot_english ({args.embedding_model})...")
    index = build_index(chunks, "cot_english", args.embedding_model)

    # Embed all queries at once
    print("Embedding queries...")
    query_vectors = embed_texts(
        [q["question"] for q in questions], args.embedding_model
    )

    # Phase 1: Retrieve + generate answers
    print(f"\n--- Phase 1: Retrieval + Generation (k={args.k}) ---")
    results = []
    t0 = time.time()

    for i, q in enumerate(questions):
        qvec = query_vectors[i]
        sources = retrieve(index, chunks, qvec, k=args.k)

        # Find first correct author rank
        first_correct_rank = None
        for s in sources:
            if author_matches(s["author"], q["author"]):
                first_correct_rank = s["rank"]
                break

        # Generate RAG answer
        if not args.skip_judge:
            rag_answer = generate_answer(q["question"], sources, args.model)
        else:
            rag_answer = "(skipped)"

        record = {
            "id": q["id"],
            "author": q["author"],
            "work": q.get("work", ""),
            "question": q["question"],
            "expected_answer": q.get("answer", ""),
            "rag_answer": rag_answer,
            "sources": [
                {"author": s["author"], "title": s["title"], "chunk_id": s["chunk_id"]}
                for s in sources
            ],
            "first_correct_rank": first_correct_rank,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        results.append(record)

        if args.verbose:
            hit = "HIT" if first_correct_rank else "MISS"
            rank_str = f"rank={first_correct_rank}" if first_correct_rank else ""
            print(f"  [{i+1}/{len(questions)}] {q['author']}: {hit} {rank_str}")

        # Incremental save
        if (i + 1) % 25 == 0:
            elapsed = time.time() - t0
            rate = (i + 1) / elapsed * 60
            print(f"  [{i+1}/{len(questions)}] {rate:.0f} q/min")

    # Phase 2: Judge
    if not args.skip_judge:
        print(f"\n--- Phase 2: LLM-as-judge ({args.judge_model}) ---")
        for i, record in enumerate(results):
            judge = judge_answer(
                record["question"],
                record["expected_answer"],
                record["author"],
                record["rag_answer"],
                record["sources"],
                args.judge_model,
            )
            record["judge"] = judge

            if args.verbose:
                print(
                    f"  [{i+1}/{len(results)}] score={judge['factual_score']} "
                    f"hit={judge['source_hit']}"
                )

    # Compute retrieval metrics
    retrieval_metrics = compute_retrieval_metrics(results)

    # Save results
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # Build summary
    summary = {
        "num_questions": len(results),
        "num_chunks": len(chunks),
        "embedding_model": args.embedding_model,
        "rag_model": args.model,
        "k": args.k,
        "retrieval": retrieval_metrics,
    }

    if not args.skip_judge:
        valid = [r for r in results if r.get("judge", {}).get("factual_score", -1) >= 0]
        if valid:
            scores = [r["judge"]["factual_score"] for r in valid]
            hits = [r["judge"]["source_hit"] for r in valid]
            summary["judge"] = {
                "judge_model": args.judge_model,
                "avg_factual_score": round(sum(scores) / len(scores), 2),
                "source_hit_rate": round(sum(hits) / len(hits), 3),
                "score_distribution": dict(sorted(Counter(scores).items())),
            }

    summary_path = args.output.replace(".jsonl", "_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Print summary
    print("\n" + "=" * 60)
    print("HYBRID EVALUATION RESULTS")
    print("=" * 60)
    print(f"Chunks: {len(chunks)}, Questions: {len(results)}, k={args.k}")
    print(f"Embedding: {args.embedding_model}")
    print(f"RAG model: {args.model}")

    print(f"\n--- Retrieval ---")
    for key, val in retrieval_metrics.items():
        print(f"  {key}: {val}")

    if "judge" in summary:
        j = summary["judge"]
        print(f"\n--- LLM-as-judge ({j['judge_model']}) ---")
        print(f"  Avg factual score: {j['avg_factual_score']}/3")
        print(f"  Source hit rate:   {j['source_hit_rate']}")
        print(f"  Score distribution: {j['score_distribution']}")

    print(f"\nResults: {args.output}")
    print(f"Summary: {summary_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hybrid evaluation pipeline")
    parser.add_argument("--chunks", default="data/cot_full.jsonl",
                        help="COT-annotated chunks JSONL")
    parser.add_argument("--questions", default="data/eval_questions.jsonl")
    parser.add_argument("--model", default=CHAT_MODEL, help="RAG generation model")
    parser.add_argument("--judge-model", default=CHAT_MODEL, help="Judge model")
    parser.add_argument("--embedding-model", default=EMBEDDING_MODEL)
    parser.add_argument("--k", type=int, default=12, help="Chunks per query")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--output", default="data/hybrid_results.jsonl")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--skip-judge", action="store_true",
                        help="Only compute retrieval metrics")
    parser.add_argument("--skip-retrieval", action="store_true",
                        help="Only run LLM judge (requires pre-computed results)")
    args = parser.parse_args()

    run_pipeline(args)
