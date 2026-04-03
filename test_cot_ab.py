"""
A/B test: Compare two LLMs on Context-Oriented Translation.

Runs both models on the same 10 sample chunks and saves results
side-by-side for manual comparison.

Usage:
    python test_cot_ab.py [--input data/test_sample_10.jsonl]
"""

import argparse
import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

# Try yaml, fall back to hardcoded vocab if not available
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# The two models to compare
MODELS = [
    os.getenv("COT_MODEL_A", "gemma3:27b"),
    os.getenv("COT_MODEL_B", "qwen3:32b"),
]

# ---------------------------------------------------------------------------
# Prompts (inline to keep this self-contained for the cluster)
# ---------------------------------------------------------------------------

COT_SYSTEM = """\
You are a specialist in ancient Greek and Latin texts, with expertise in \
environmental history, water infrastructure, and Nile Valley administration \
(500 BCE - 300 CE).

Your task is to produce a **Context-Oriented Translation** of the given passage. \
This is NOT a literal scholarly translation. It is an English rendering \
optimized for semantic search — designed so that a vector embedding of your \
output will match well against English-language research questions.

Guidelines:
1. **State the main point plainly.** What is this passage about? Lead with that.
2. **Disambiguate key terms.** Ancient terms often have multiple meanings. \
Choose the contextually correct one and state it explicitly. \
E.g., translate psyche as "the rational soul" or "life force" depending on context, \
not just "soul." For Egyptian/administrative terms, give the functional meaning.
3. **Resolve pronouns and references.** Replace "he," "it," "this" with the \
actual referent (person, place, object) so the passage is self-contained.
4. **Simplify argument structure.** Preserve all substantive content but \
streamline rhetorical complexity. Focus on claims, evidence, and conclusions.
5. **Add minimal context.** If the passage is unintelligible without knowing \
who is speaking, what work this is from, or what preceded it, state that briefly.
6. **Preserve all named entities.** People, places, institutions, dates, and \
measurements must appear in the output.
7. **Do NOT add information not in the passage or its immediate context.** \
Do not import external knowledge. If the passage is fragmentary, say so.

The translation will be used ONLY for vector embedding — users will never read it. \
Accuracy of meaning matters; literary quality does not.\
"""

COT_USER = """\
## Passage to translate

**Work:** {author}, *{title}*
**Language:** {language}
**Passage reference:** {reference}

### Passage:
{passage_text}

---

Produce your response as JSON with these fields:

```json
{{{{
  "cot_english": "<context-oriented English translation of the passage>",
  "vocab_terms": ["<term_id>", ...],
  "evidence_layer": "<attestation | inference | framing>",
  "confidence": <0.0-1.0>,
  "rationale": "<1-2 sentences explaining your classification choices>"
}}}}
```

For `vocab_terms`, use ONLY ids from this list (leave empty if none apply):
{vocab_term_ids}

Return ONLY the JSON object, no other text.\
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Hardcoded vocab IDs so the test runs without pyyaml
FALLBACK_VOCAB_IDS = [
    "hf.canal", "hf.dike", "hf.basin", "hf.nilometer", "hf.well",
    "hf.cistern", "hf.harbor", "hf.sluice", "hf.shaduf",
    "hp.inundation", "hp.low_water", "hp.high_flood", "hp.flood_anomaly",
    "hp.siltation", "hp.salinization", "hp.drought",
    "mp.irrigation", "mp.dredging", "mp.embankment_repair",
    "mp.canal_clearance", "mp.water_distribution", "mp.corvee_labor",
    "mp.tax_remission",
    "if.divine_agency", "if.mismanagement", "if.natural_cycle",
    "if.moral_exemplum", "if.prodigy", "if.royal_beneficence",
]


def load_vocab_term_ids(vocab_path: str) -> list[str]:
    if HAS_YAML:
        with open(vocab_path, encoding="utf-8") as f:
            vocab = yaml.safe_load(f)
        term_ids = []
        for domain in vocab.get("domains", {}).values():
            for term in domain.get("terms", []):
                term_ids.append(term["id"])
        return term_ids
    else:
        print("  (pyyaml not installed, using hardcoded vocab IDs)")
        return FALLBACK_VOCAB_IDS


def call_ollama(system: str, user: str, model: str) -> tuple[str, float]:
    """Call Ollama and return (response_text, elapsed_seconds)."""
    t0 = time.time()
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
        timeout=300,
    )
    elapsed = time.time() - t0
    resp.raise_for_status()
    return resp.json()["message"]["content"], elapsed


def parse_llm_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)
    # Try to find JSON object in the text
    start = text.find("{")
    end = text.rfind("}") + 1
    if start >= 0 and end > start:
        text = text[start:end]
    return json.loads(text)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_test(input_path: str, vocab_path: str, output_path: str):
    vocab_ids = load_vocab_term_ids(vocab_path)
    print(f"Loaded {len(vocab_ids)} vocabulary terms")
    print(f"Models: {MODELS[0]} vs {MODELS[1]}")
    print(f"Ollama: {OLLAMA_BASE_URL}")
    print()

    with open(input_path, encoding="utf-8") as f:
        chunks = [json.loads(line) for line in f]
    print(f"Testing on {len(chunks)} chunks\n")

    results = []

    for i, chunk in enumerate(chunks):
        chunk_id = chunk.get("chunk_id", str(i))
        print(f"--- Chunk {i+1}/{len(chunks)}: {chunk['author']} - {chunk['title']} "
              f"({chunk['language']}, {'poetry' if chunk['is_poetry_like'] else 'prose'}, "
              f"{chunk['token_count']} tok) ---")

        user_prompt = COT_USER.format(
            author=chunk.get("author", "Unknown"),
            title=chunk.get("title", "Unknown"),
            language=chunk.get("language", "unknown"),
            reference=chunk.get("cite_start", ""),
            passage_text=chunk.get("text", ""),
            vocab_term_ids=", ".join(vocab_ids),
        )

        record = {
            "chunk_id": chunk_id,
            "author": chunk["author"],
            "title": chunk["title"],
            "language": chunk["language"],
            "is_poetry": chunk["is_poetry_like"],
            "token_count": chunk["token_count"],
            "original_text": chunk["text"][:500],
        }

        for model in MODELS:
            print(f"  Running {model}...", end=" ", flush=True)
            try:
                raw, elapsed = call_ollama(COT_SYSTEM, user_prompt, model)
                try:
                    parsed = parse_llm_json(raw)
                    json_ok = True
                except json.JSONDecodeError:
                    parsed = {"cot_english": raw, "vocab_terms": [], "evidence_layer": "parse_error"}
                    json_ok = False

                record[model] = {
                    "cot_english": parsed.get("cot_english", ""),
                    "vocab_terms": parsed.get("vocab_terms", []),
                    "evidence_layer": parsed.get("evidence_layer", ""),
                    "confidence": parsed.get("confidence", 0),
                    "rationale": parsed.get("rationale", ""),
                    "elapsed_sec": round(elapsed, 1),
                    "json_valid": json_ok,
                    "raw_response": raw,
                }
                print(f"{elapsed:.1f}s, JSON={'OK' if json_ok else 'FAIL'}")

            except Exception as e:
                record[model] = {"error": str(e), "elapsed_sec": 0, "json_valid": False}
                print(f"ERROR: {e}")

        results.append(record)

        # Save after each chunk (incremental)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    for model in MODELS:
        times = [r[model]["elapsed_sec"] for r in results if "elapsed_sec" in r.get(model, {})]
        json_ok = sum(1 for r in results if r.get(model, {}).get("json_valid", False))
        vocab_counts = [len(r[model].get("vocab_terms", [])) for r in results if model in r]
        print(f"\n{model}:")
        print(f"  Avg time:    {sum(times)/len(times):.1f}s")
        print(f"  JSON valid:  {json_ok}/{len(results)}")
        print(f"  Avg vocab terms: {sum(vocab_counts)/len(vocab_counts):.1f}")

    print(f"\nFull results saved to {output_path}")
    print("Review the cot_english fields side by side to judge translation quality.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A/B test COT models")
    parser.add_argument("--input", default="data/test_sample_10.jsonl")
    parser.add_argument("--vocab", default="vocab/ecology_v01.yaml")
    parser.add_argument("--output", default="data/cot_ab_results.json")
    args = parser.parse_args()

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    run_test(args.input, args.vocab, args.output)
