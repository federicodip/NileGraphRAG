# Evidence Layer Annotation Guidelines

## Purpose

These guidelines define how to classify passages into evidence layers for the NileGraphRAG annotation pipeline. They are used both for human gold-standard annotation and for instructing the LLM classifier.

The core principle: **keep what the text says, what scholars derive, and how the text frames its claims analytically distinct.** This prevents "evidentiary flattening" — the collapse of heterogeneous evidence types into undifferentiated "facts."

## The Three Evidence Layers

### ATTESTATION

**Definition:** What the passage directly states. The text explicitly says that something exists, happened, was ordered, or was observed.

**Test:** Can you point to specific words in the passage that state this claim? If you removed the passage, would the claim disappear?

**Typical signals:**
- Named agents performing actions ("the hydrophylax Petesouchos reports...")
- Dates, measurements, quantities ("in year 12...", "the Nile rose to 16 cubits...")
- Administrative language (orders, receipts, records, contracts)
- Direct description of objects, places, or events

**Genre correlation:**
- Documentary papyri → almost always attestation
- Inscriptions → usually attestation (dedications, decrees, building records)
- Technical/agronomic writing → attestation of practices and methods
- Historiography → attestation when narrating events (but often mixed with framing)

**Examples:**
- "In the 3rd year of Ptolemy, the dioryx of Dionysias was cleared of silt" → **ATTESTATION** (administrative record of a specific event)
- "The Nile reached 16 cubits at the nilometer of Elephantine" → **ATTESTATION** (recorded measurement)
- "Payment receipt for 5 days of corvée labor on the embankment" → **ATTESTATION** (fiscal document)
- Strabo describing the layout of canals in the Fayum → **ATTESTATION** (direct description of observed infrastructure)

### INFERENCE

**Definition:** A claim derived from one or more attestations but not directly stated in any single passage. The text provides evidence from which a conclusion can be drawn, but the conclusion requires interpretive reasoning.

**Test:** Does the claim require connecting dots across passages, or reading between the lines of a single passage? Would a different scholar plausibly draw a different conclusion from the same text?

**Typical signals:**
- Absence as evidence ("no records of tax collection in year X" → infer bad flood year)
- Patterns across documents (three repair orders in five years → infer structural problems)
- Technical implications (an order for dredging equipment → infer silted canal)
- Institutional signals (tax remission records → infer crop failure → infer inadequate flood)

**Important:** An inference is always *about* attestations. It says "given that the text says X, we can reasonably conclude Y." The inferential step should be explicit, not smuggled in as if the text directly states Y.

**Examples:**
- Tax remission records for the Fayum in 245 BCE → **INFERENCE** that there was a poor flood year (the documents don't describe the flood; we infer it from the fiscal response)
- Multiple embankment repair orders in quick succession → **INFERENCE** of structural problems or unusually destructive floods
- A contract for saqia parts → **INFERENCE** that mechanical irrigation was in use at that location (the contract doesn't describe irrigation practice)

### FRAMING

**Definition:** The rhetorical, explanatory, or narrative framework through which a passage presents an event or phenomenon. Framing is about *how the text explains or characterizes* something, not about what happened.

**Test:** Could the same underlying event be described with a completely different framing? Is the passage telling you about the world, or about how the author (or the author's culture) makes sense of the world?

**Typical signals:**
- Causal explanations involving divine will, fate, or supernatural agency
- Moral judgments (mismanagement, negligence, hubris, impiety)
- Conventional narrative patterns (prodigy catalogues, moral exempla, abundance topoi)
- Language of blame, praise, or legitimation
- "Crisis vocabulary" — moralized scarcity language, portent lists, apocalyptic imagery

**Genre correlation:**
- Historiography → frequent framing (events narrated through interpretive lenses)
- Royal/imperial decrees → framing through royal beneficence
- Religious texts → framing through divine agency
- Documentary papyri → rare framing (administrative language is typically neutral)

**Critical distinction:** A passage can *attest* an event AND *frame* it simultaneously. "The gods punished Egypt with drought, and the canals ran dry" contains both an attestation (canals ran dry) and a framing (divine punishment). In the current pipeline, assign the **dominant** layer. In future versions, multi-label annotation will be supported.

**Examples:**
- "Zeus sent a flood to punish the impious city" → **FRAMING** (divine agency)
- "The king in his wisdom and beneficence restored the canal that had fallen into ruin through the negligence of lesser officials" → **FRAMING** (royal beneficence + blame of subordinates; the canal repair may be attested, but the passage's purpose is legitimation)
- "As happens every year when the river rises, the fields were watered" → **FRAMING** (natural cycle topos — presenting the flood as predictable and benign)
- Herodotus: "Egypt is the gift of the Nile" → **FRAMING** (abundance topos)
- A prodigy catalogue listing floods alongside eclipses and monstrous births → **FRAMING** (the flood is presented as a sign, not as a hydrological event)

## Edge Cases and Decision Rules

### Mixed passages (attestation + framing)
Most common in historiography. A passage may attest that a canal was built AND frame it as royal beneficence. **Assign the dominant function.** If the passage's primary purpose is to record the event → attestation. If its primary purpose is to praise/blame/explain → framing.

### Genre as a prior, not a rule
Documentary papyri are *usually* attestation, but not always. A petition that accuses a neighbor of water theft frames the dispute (blame). A royal decree records a decision (attestation) but frames it as beneficence. Use genre as a starting point, then read the passage.

### The "so what" test for inference
If you find yourself writing "this passage *shows* that..." or "this *implies* that..." — you're making an inference. The passage itself doesn't show or imply; you (or a scholar) do. Mark it as inference and state the reasoning.

### Fragments and unclear passages
If a passage is too fragmentary to classify, mark it as attestation with low confidence. The default assumption is that a passage says what it says; framing and inference require positive evidence of rhetorical/interpretive intent.

## Practical Annotation Workflow

For gold-standard creation (50 passages):

1. Select passages stratified by:
   - Genre: 15 documentary (papyri), 15 literary (historiography), 10 technical/agronomic, 10 inscriptions
   - Content: at least 20 with water/infrastructure terms, 10 with crisis/famine terms, 10 with administrative/fiscal terms, 10 general
   - Language: mix of Greek and Latin

2. For each passage, annotate:
   - **Evidence layer** (attestation / inference / framing)
   - **Confidence** (high / medium / low)
   - **Reasoning** (1-2 sentences explaining why)
   - **Vocab terms** (which ecology vocabulary terms apply)

3. Second annotator repeats independently on the same 50 passages.

4. Compute inter-annotator agreement (Cohen's kappa) per layer.

5. Adjudicate disagreements through discussion → final gold standard.

## How This Maps to the LLM Prompt

The COT translation prompt asks the LLM to classify each chunk's evidence_layer. The prompt should be updated to include:
- The definitions above (condensed)
- The genre of the work as context (the LLM already receives author + title)
- Examples from each layer
- The "dominant function" rule for mixed passages
