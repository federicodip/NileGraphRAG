# NileGraphRAG

Spatially-aware Graph-RAG for water infrastructure in the ancient Nile Valley (500 BCE–300 CE).

Ingests ancient Greek, Latin, and documentary texts, applies **Context-Oriented Translation** (COT) for semantic embedding, annotates passages with an evidence-graded vocabulary, and supports graph-constrained retrieval over a Neo4j knowledge graph.

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (use source .venv/bin/activate on Linux)
pip install -r requirements.txt
cp .env.example .env            # edit with your settings
```

Requires [Ollama](https://ollama.com/) running locally for LLM inference.

## Pipeline

```
Perseus TEI / EpiDoc XML
    → ingest/perseus.py        → data/processed/works/*.json
    → chunk.py                 → data/processed/chunks.jsonl
    → translate/cot.py         → data/translated/cot_chunks.jsonl
    → embed.py                 → faiss_index/
    → retrieve.py --query "…"  → RAG answer with citations
```

## Key Idea: Context-Oriented Translation

Following [Iwata et al. (2024)](https://ipsj.ixsq.nii.ac.jp/ej/?action=pages_view_main&active_action=repository_view_main_item_detail&item_id=237025), we translate each text chunk into a **context-aware English paraphrase** optimized for semantic search — not a literal scholarly translation. This produces better embeddings because:

1. Embedding models are trained primarily on English
2. Ambiguous ancient terms are disambiguated in context
3. Pronouns and references are resolved for self-contained chunks
4. Argument structure is simplified for clearer semantic matching

The COT text is used **only for embedding**. The original passage is always displayed in citations.

## Evidence-Graded Annotation

Each chunk is classified into three layers:

- **Attestation** — what the passage directly says (anchored to text, with provenance)
- **Inference** — hypothesis derived from attestations (explicitly marked as non-direct)
- **Framing** — the rhetorical grammar of the passage (divine agency, moral exemplum, etc.)

This enables queries like: *"Show me attestations of canal maintenance in the Fayum, excluding passages that only frame irrigation as royal beneficence."*

## Ancient Ecology Vocabulary

A controlled vocabulary (`vocab/ecology_v01.yaml`) covering:

- **Hydraulic features**: canals, dikes, basins, nilometers, wells, cisterns, harbors
- **Hydrological phenomena**: inundation, low water, flood anomalies, siltation, drought
- **Management practices**: irrigation, dredging, embankment repair, corvée labor
- **Interpretive framings**: divine agency, mismanagement, natural cycle, prodigy

## Project Structure

```
ingest/          Text ingestion (Perseus TEI, later EpiDoc)
translate/       Context-Oriented Translation pipeline
vocab/           Ancient Ecology Vocabulary (versioned YAML)
eval/            Evaluation pipeline
jobs/            Slurm scripts for UZH ScienceCluster
```

## Predecessor

Built on lessons from [TellusGraph](https://github.com/federicodip/TellusGraph), a flat FAISS-based RAG system for Perseus literary texts.
