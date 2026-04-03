"""
Prompt templates for Context-Oriented Translation (COT).

Based on Iwata et al. (2024) "Context-Oriented Translation" approach,
adapted for ancient ecological/infrastructural texts.
"""

# System prompt for the COT + annotation pass.
# The LLM reads the original passage with surrounding context and produces:
#   1. A context-oriented English translation (for embedding)
#   2. Vocabulary labels from the Ancient Ecology Vocabulary (for graph)
#   3. Evidence layer classification (attestation / inference / framing)
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
E.g., translate ψυχή as "the rational soul" or "life force" depending on context, \
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

### Preceding context (for reference only — do NOT translate this):
{preceding_context}

### Passage:
{passage_text}

---

Produce your response as JSON with these fields:

```json
{{
  "cot_english": "<context-oriented English translation of the passage>",
  "vocab_terms": ["<term_id>", ...],
  "evidence_layer": "<attestation | inference | framing>",
  "confidence": <0.0-1.0>,
  "rationale": "<1-2 sentences explaining your classification choices>"
}}
```

For `vocab_terms`, use ONLY ids from this list (leave empty if none apply):
{vocab_term_ids}

Return ONLY the JSON object, no other text.\
"""
