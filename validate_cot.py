"""
Validate COT: compare retrieval quality of raw embed_text vs COT English.

1. Loads 500 sample chunks (with both embed_text and cot_english)
2. Builds two FAISS indices (raw vs COT)
3. Runs eval questions against both
4. Compares author hit rate and rank

Usage:
    python validate_cot.py --cot-chunks data/validation_cot_500.jsonl
"""

import argparse
import json
import os
import sys
from pathlib import Path

import faiss
import numpy as np
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "BAAI/bge-m3")

# Author alias map (eval question names → corpus author fragments)
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
    """Check if a chunk's author matches the eval question's expected author."""
    ca = chunk_author.lower()
    ea = eval_author.lower()
    if ea in ca:
        return True
    for alias in AUTHOR_ALIASES.get(ea, []):
        if alias in ca:
            return True
    return False


def embed_texts(texts: list[str], model_name: str) -> np.ndarray:
    """Embed a list of texts using sentence-transformers."""
    from sentence_transformers import SentenceTransformer

    print(f"  Loading embedding model: {model_name}")
    model = SentenceTransformer(model_name)
    print(f"  Embedding {len(texts)} texts...")
    vectors = model.encode(
        texts,
        batch_size=64,
        show_progress_bar=True,
        normalize_embeddings=True,
    )
    return np.array(vectors, dtype=np.float32)


def build_faiss_index(vectors: np.ndarray) -> faiss.IndexFlatIP:
    """Build a FAISS inner-product index (cosine sim on normalized vectors)."""
    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(vectors)
    return index


def run_eval(
    index: faiss.IndexFlatIP,
    query_vectors: np.ndarray,
    chunks: list[dict],
    questions: list[dict],
    k: int = 20,
) -> dict:
    """Run queries against index, compute author hit rate and MRR."""
    scores, indices = index.search(query_vectors, k)

    results = []
    for qi, q in enumerate(questions):
        expected_author = q["author"]
        retrieved_indices = indices[qi]

        # Find first rank where author matches
        first_hit_rank = None
        hits_in_k = 0
        for rank, ci in enumerate(retrieved_indices):
            if ci < 0 or ci >= len(chunks):
                continue
            if author_matches(chunks[ci]["author"], expected_author):
                if first_hit_rank is None:
                    first_hit_rank = rank + 1  # 1-indexed
                hits_in_k += 1

        results.append({
            "id": q["id"],
            "author": expected_author,
            "hit": first_hit_rank is not None,
            "first_rank": first_hit_rank,
            "hits_in_k": hits_in_k,
        })

    # Aggregate
    n = len(results)
    hit_rate = sum(1 for r in results if r["hit"]) / n
    mrr = sum(1.0 / r["first_rank"] for r in results if r["hit"]) / n

    # Recall at various k
    recall_at = {}
    for cutoff in [1, 5, 10, 20]:
        if cutoff > k:
            continue
        hits = sum(
            1 for r in results
            if r["first_rank"] is not None and r["first_rank"] <= cutoff
        )
        recall_at[cutoff] = hits / n

    return {
        "hit_rate": round(hit_rate, 3),
        "mrr": round(mrr, 3),
        "recall_at": {str(c): round(v, 3) for c, v in recall_at.items()},
        "per_question": results,
    }


def main():
    parser = argparse.ArgumentParser(description="Validate COT retrieval quality")
    parser.add_argument(
        "--cot-chunks",
        default="data/validation_cot_500.jsonl",
        help="COT-annotated chunks (output of cot.py on the 500 sample)",
    )
    parser.add_argument(
        "--questions",
        default="data/eval_questions.jsonl",
        help="Eval questions JSONL",
    )
    parser.add_argument(
        "--embedding-model",
        default=EMBEDDING_MODEL,
        help="HuggingFace embedding model",
    )
    parser.add_argument("--k", type=int, default=20, help="Top-k for retrieval")
    parser.add_argument(
        "--output",
        default="data/validation_results.json",
        help="Output file",
    )
    args = parser.parse_args()

    # Load COT chunks
    with open(args.cot_chunks, encoding="utf-8") as f:
        chunks = [json.loads(line) for line in f]
    print(f"Loaded {len(chunks)} COT chunks")

    # Check all have cot_english
    missing = [c for c in chunks if not c.get("cot_english")]
    if missing:
        print(f"WARNING: {len(missing)} chunks missing cot_english, skipping them")
        chunks = [c for c in chunks if c.get("cot_english")]

    # Load eval questions
    with open(args.questions, encoding="utf-8") as f:
        questions = [json.loads(line) for line in f]
    print(f"Loaded {len(questions)} eval questions")

    # Extract texts for both versions
    raw_texts = [c.get("embed_text", c.get("text", "")) for c in chunks]
    cot_texts = [c["cot_english"] for c in chunks]
    query_texts = [q["question"] for q in questions]

    # Embed everything
    print("\n--- Embedding raw texts ---")
    raw_vectors = embed_texts(raw_texts, args.embedding_model)

    print("\n--- Embedding COT texts ---")
    cot_vectors = embed_texts(cot_texts, args.embedding_model)

    print("\n--- Embedding queries ---")
    query_vectors = embed_texts(query_texts, args.embedding_model)

    # Build indices
    raw_index = build_faiss_index(raw_vectors)
    cot_index = build_faiss_index(cot_vectors)

    # Run eval on both
    print(f"\n--- Evaluating raw embed_text (top-{args.k}) ---")
    raw_results = run_eval(raw_index, query_vectors, chunks, questions, args.k)

    print(f"\n--- Evaluating COT English (top-{args.k}) ---")
    cot_results = run_eval(cot_index, query_vectors, chunks, questions, args.k)

    # Print comparison
    print("\n" + "=" * 60)
    print("RETRIEVAL COMPARISON (500 chunks, no metadata filtering)")
    print("=" * 60)
    print(f"Embedding model: {args.embedding_model}")
    print(f"Chunks: {len(chunks)}, Questions: {len(questions)}, k={args.k}")
    print()
    print(f"{'Metric':<20} {'Raw embed_text':>15} {'COT English':>15} {'Delta':>10}")
    print("-" * 60)

    print(f"{'Author hit rate':<20} {raw_results['hit_rate']:>15.3f} {cot_results['hit_rate']:>15.3f} {cot_results['hit_rate']-raw_results['hit_rate']:>+10.3f}")
    print(f"{'MRR':<20} {raw_results['mrr']:>15.3f} {cot_results['mrr']:>15.3f} {cot_results['mrr']-raw_results['mrr']:>+10.3f}")

    for cutoff in ["1", "5", "10", "20"]:
        if cutoff in raw_results["recall_at"]:
            rv = raw_results["recall_at"][cutoff]
            cv = cot_results["recall_at"][cutoff]
            print(f"{'Recall@' + cutoff:<20} {rv:>15.3f} {cv:>15.3f} {cv-rv:>+10.3f}")

    # Per-question comparison: where did COT help or hurt?
    improved = 0
    degraded = 0
    unchanged = 0
    for rr, cr in zip(raw_results["per_question"], cot_results["per_question"]):
        raw_rank = rr["first_rank"] or 999
        cot_rank = cr["first_rank"] or 999
        if cot_rank < raw_rank:
            improved += 1
        elif cot_rank > raw_rank:
            degraded += 1
        else:
            unchanged += 1

    print()
    print(f"Per-question: {improved} improved, {degraded} degraded, {unchanged} unchanged")

    # Save full results
    output = {
        "embedding_model": args.embedding_model,
        "num_chunks": len(chunks),
        "num_questions": len(questions),
        "k": args.k,
        "raw": {k: v for k, v in raw_results.items() if k != "per_question"},
        "cot": {k: v for k, v in cot_results.items() if k != "per_question"},
        "per_question": [
            {
                "id": rr["id"],
                "author": rr["author"],
                "raw_rank": rr["first_rank"],
                "cot_rank": cr["first_rank"],
                "raw_hits": rr["hits_in_k"],
                "cot_hits": cr["hits_in_k"],
            }
            for rr, cr in zip(raw_results["per_question"], cot_results["per_question"])
        ],
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"\nFull results saved to {args.output}")


if __name__ == "__main__":
    main()
