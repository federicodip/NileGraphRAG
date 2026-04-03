# CLAUDE.md

## Project Overview

NileGraphRAG is a spatially-aware Graph-RAG system for studying water infrastructure in the ancient Nile Valley (500 BCE–300 CE). It ingests ancient Greek, Latin, and documentary texts, applies Context-Oriented Translation (COT) for embedding, annotates passages with an evidence-graded vocabulary, and supports graph-constrained retrieval over a Neo4j knowledge graph.

**Predecessor:** TellusGraph (../TellusGraph) — a flat FAISS-based RAG prototype for Perseus literary texts. NileGraphRAG builds on lessons learned there but uses a modular architecture.

## Pipeline (planned)

```bash
# 1. Ingest texts (Perseus TEI, later EpiDoc papyri/inscriptions)
python ingest/perseus.py                          # → data/processed/works/*.json

# 2. Build RAG chunks
python chunk.py                                   # → data/processed/chunks.jsonl

# 3. Context-Oriented Translation + vocabulary annotation
python translate/cot.py --input data/processed/chunks.jsonl
                                                   # → data/translated/cot_chunks.jsonl

# 4. Embed COT English into FAISS
python embed.py --ingest                           # → faiss_index/

# 5. (Later) Neo4j graph ingestion
python graph.py                                    # loads chunks + vocab + spatial data

# 6. Query (hybrid retrieval)
python retrieve.py --query "..."
```

## Architecture

- **ingest/** — text ingestion modules (Perseus TEI, later EpiDoc)
- **translate/** — Context-Oriented Translation pipeline + LLM prompts
- **vocab/** — Ancient Ecology Vocabulary (YAML). Versioned controlled vocabulary used as both ML label set and semantic layer.
- **eval/** — evaluation pipeline
- **jobs/** — Slurm job scripts for UZH ScienceCluster
- **chunk.py** — chunking logic (poetry vs prose detection)
- **embed.py** — FAISS embedding (uses COT English text)
- **retrieve.py** — hybrid retrieval (FAISS + graph constraints)
- **graph.py** — Neo4j operations

## Key Design Decisions

- **COT is for embedding only.** The context-oriented English translation is stored alongside the original text but used only for vector search. Citations always show the original passage.
- **Vocabulary annotation happens during COT.** One LLM call produces both the English paraphrase and the vocabulary/evidence-layer classification. This avoids double-processing.
- **Evidence grading is a first-class property.** Every annotation is classified as attestation, inference, or framing. This enables queries that distinguish discourse from events.
- **Incremental saves everywhere.** All long-running scripts checkpoint to disk periodically and support --resume.

## Environment

Python 3.10+ with venv. Ollama for local LLM inference.

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

Configuration in `.env` (see `.env.example`).

## Data Layout

```
data/
  processed/works/          # per-work JSON files from ingestion
  processed/chunks.jsonl    # RAG chunks (input to COT)
  translated/cot_chunks.jsonl  # COT-annotated chunks (input to embedding)
vocab/
  ecology_v01.yaml          # controlled vocabulary
faiss_index/                # FAISS vector index (gitignored)
```

## Maintenance

Keep this file up to date when the project changes.
