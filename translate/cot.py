"""
Context-Oriented Translation (COT) pipeline.

Reads RAG chunks (from TellusGraph or new ingestion), sends each to an LLM
with surrounding context, and produces:
  - cot_english: English paraphrase optimized for embedding
  - vocab_terms: Ancient Ecology Vocabulary labels
  - evidence_layer: attestation / inference / framing

Output: JSONL file with original chunk data + COT fields.
Supports --resume (skips already-translated chunks).
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests
import yaml
from dotenv import load_dotenv

from prompts import COT_SYSTEM, COT_USER

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
COT_MODEL = os.getenv("COT_MODEL", "gemma3:12b")

# ---------------------------------------------------------------------------
# Vocabulary loading
# ---------------------------------------------------------------------------

def load_vocab_term_ids(vocab_path: str) -> list[str]:
    """Load all term IDs from the ecology vocabulary YAML."""
    with open(vocab_path, encoding="utf-8") as f:
        vocab = yaml.safe_load(f)

    term_ids = []
    for domain in vocab.get("domains", {}).values():
        for term in domain.get("terms", []):
            term_ids.append(term["id"])
    return term_ids


# ---------------------------------------------------------------------------
# LLM call
# ---------------------------------------------------------------------------

def call_ollama(system: str, user: str, model: str = None) -> str:
    """Send a chat completion request to Ollama and return the response text."""
    model = model or COT_MODEL
    resp = requests.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "stream": False,
            "options": {"temperature": 0.3, "num_ctx": 8192},
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"]


def parse_llm_json(text: str) -> dict:
    """Extract JSON from LLM response, handling markdown fences."""
    text = text.strip()
    if text.startswith("```"):
        # Remove ```json ... ``` fences
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)
    return json.loads(text)


# ---------------------------------------------------------------------------
# COT pipeline
# ---------------------------------------------------------------------------

def build_preceding_context(chunks: list[dict], idx: int, n: int = 3) -> str:
    """Get the text of the N preceding chunks from the same work."""
    current = chunks[idx]
    work_id = current.get("work_id", "")

    preceding = []
    for i in range(max(0, idx - n), idx):
        if chunks[i].get("work_id", "") == work_id:
            preceding.append(chunks[i].get("text", ""))

    return "\n\n---\n\n".join(preceding) if preceding else "(No preceding context available)"


def translate_chunk(chunk: dict, preceding_context: str, vocab_ids: list[str]) -> dict:
    """Run COT on a single chunk. Returns the parsed JSON annotation."""
    user_prompt = COT_USER.format(
        author=chunk.get("author", "Unknown"),
        title=chunk.get("title", "Unknown"),
        language=chunk.get("language", "unknown"),
        reference=chunk.get("reference", ""),
        preceding_context=preceding_context,
        passage_text=chunk.get("text", ""),
        vocab_term_ids=", ".join(vocab_ids),
    )

    raw = call_ollama(COT_SYSTEM, user_prompt)

    try:
        result = parse_llm_json(raw)
    except json.JSONDecodeError:
        # If parsing fails, store the raw text and flag it
        result = {
            "cot_english": raw,
            "vocab_terms": [],
            "evidence_layer": "unknown",
            "confidence": 0.0,
            "rationale": "JSON parse failed — raw LLM output stored in cot_english",
        }

    return result


def run_pipeline(
    input_path: str,
    output_path: str,
    vocab_path: str,
    limit: int = None,
    resume: bool = True,
    batch_size: int = 50,
    shard: int = None,
    num_shards: int = None,
):
    """Run COT on all chunks, saving incrementally.

    If shard/num_shards are set, only process chunks where
    chunk_index % num_shards == shard. Each shard writes to its
    own output file (output_path with _shardN suffix).
    """

    # Load vocab
    vocab_ids = load_vocab_term_ids(vocab_path)
    print(f"Loaded {len(vocab_ids)} vocabulary terms")

    # Load input chunks
    with open(input_path, encoding="utf-8") as f:
        chunks = [json.loads(line) for line in f]
    print(f"Loaded {len(chunks)} chunks from {input_path}")

    # Sharding: select only this shard's chunks
    if shard is not None and num_shards is not None:
        base, ext = os.path.splitext(output_path)
        output_path = f"{base}_shard{shard:02d}{ext}"
        all_indices = list(range(len(chunks)))
        shard_indices = set(i for i in all_indices if i % num_shards == shard)
        print(f"Shard {shard}/{num_shards}: {len(shard_indices)} chunks → {output_path}")
    else:
        shard_indices = None  # process all

    # Resume: find already-processed chunk IDs
    done_ids = set()
    if resume and Path(output_path).exists():
        with open(output_path, encoding="utf-8") as f:
            for line in f:
                rec = json.loads(line)
                done_ids.add(rec.get("chunk_id", rec.get("id", "")))
        print(f"Resuming: {len(done_ids)} chunks already processed")

    # Filter to remaining
    to_process = []
    for i, c in enumerate(chunks):
        if shard_indices is not None and i not in shard_indices:
            continue
        cid = c.get("chunk_id", c.get("id", str(i)))
        if cid not in done_ids:
            to_process.append((i, c))

    if limit:
        to_process = to_process[:limit]

    print(f"Processing {len(to_process)} chunks (model: {COT_MODEL})")

    # Process with incremental saves
    results_buffer = []
    processed = 0
    t0 = time.time()

    for idx_in_list, (chunk_idx, chunk) in enumerate(to_process):
        cid = chunk.get("chunk_id", chunk.get("id", str(chunk_idx)))

        preceding = build_preceding_context(chunks, chunk_idx)

        try:
            annotation = translate_chunk(chunk, preceding, vocab_ids)
        except Exception as e:
            print(f"  ERROR on chunk {cid}: {e}")
            annotation = {
                "cot_english": "",
                "vocab_terms": [],
                "evidence_layer": "unknown",
                "confidence": 0.0,
                "rationale": f"Error: {e}",
            }

        # Merge original chunk data with COT annotation
        out_record = {**chunk, "chunk_id": cid, "cot_model": COT_MODEL, **annotation}
        results_buffer.append(out_record)
        processed += 1

        # Incremental save every batch_size chunks
        if len(results_buffer) >= batch_size:
            _flush(results_buffer, output_path)
            elapsed = time.time() - t0
            rate = processed / elapsed if elapsed > 0 else 0
            print(
                f"  [{processed}/{len(to_process)}] saved batch "
                f"({rate:.1f} chunks/min)"
            )
            results_buffer = []

    # Final flush
    if results_buffer:
        _flush(results_buffer, output_path)

    elapsed = time.time() - t0
    print(f"Done: {processed} chunks in {elapsed/60:.1f} min")


def _flush(records: list[dict], path: str):
    """Append records to output JSONL."""
    with open(path, "a", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Context-Oriented Translation pipeline"
    )
    parser.add_argument(
        "--input",
        default="../data/processed/rag/chunks.jsonl",
        help="Input chunks JSONL (from TellusGraph or new ingestion)",
    )
    parser.add_argument(
        "--output",
        default="../data/translated/cot_chunks.jsonl",
        help="Output JSONL with COT annotations",
    )
    parser.add_argument(
        "--vocab",
        default="../vocab/ecology_v01.yaml",
        help="Path to vocabulary YAML",
    )
    parser.add_argument(
        "--limit", type=int, default=None, help="Process only first N chunks"
    )
    parser.add_argument(
        "--no-resume",
        action="store_true",
        help="Start from scratch (don't skip already-processed chunks)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=50,
        help="Save checkpoint every N chunks",
    )
    parser.add_argument(
        "--shard",
        type=int,
        default=None,
        help="Shard index (0-based). Use with --num-shards for parallel jobs.",
    )
    parser.add_argument(
        "--num-shards",
        type=int,
        default=None,
        help="Total number of shards. Each shard writes to its own output file.",
    )
    args = parser.parse_args()

    # Ensure output directory exists
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    run_pipeline(
        input_path=args.input,
        output_path=args.output,
        vocab_path=args.vocab,
        limit=args.limit,
        resume=not args.no_resume,
        batch_size=args.batch_size,
        shard=args.shard,
        num_shards=args.num_shards,
    )
