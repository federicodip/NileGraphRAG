# Demo Queries for May 7 Presentation

Queries designed to showcase the platform's capabilities: COT retrieval, vocabulary annotation, evidence grading, and spatial linking. Each query demonstrates a different feature.

## 1. Basic COT Retrieval (show it works)

**Query:** "What irrigation technologies were used in Ptolemaic Egypt?"

**What it demonstrates:** COT English embeddings retrieve relevant passages that raw Greek/Latin embeddings would miss. Show side-by-side: same query, raw index vs COT index.

**Expected results:** Passages mentioning mechane (saqia), keloneion (shaduf), kochlias (Archimedean screw) — terms the user would never search in Greek.

---

## 2. Vocabulary-Filtered Retrieval (show the vocab matters)

**Query:** "Show me all passages tagged with `hf.saqia` or `hf.shaduf`"

**What it demonstrates:** Graph-constrained retrieval using vocabulary annotations. Instead of hoping the embedding finds the right passages, directly query by infrastructure type.

**Expected results:** Clustered results from Rathbone's Heroninos estate texts, Strabo on Egyptian agriculture, papyrological orders for saqia parts.

---

## 3. Evidence Layer Distinction (the core methodological claim)

**Query:** "How do sources describe Nile flood failures?"

**Then filter by evidence layer:**
- **Attestation only:** "In year X, the Nile reached only 12 cubits" — nilometer readings, administrative records
- **Framing only:** "The gods punished Egypt with drought" — Diodorus, Herodotus, prodigy narratives
- **Inference only:** Tax remission records from which low floods are inferred

**What it demonstrates:** The system can distinguish *what happened* from *how it was explained* — the anti-flattening claim in your abstract.

---

## 4. Spatial Query (the map demo)

**Query:** "Where is canal maintenance attested in the Fayum between 300-100 BCE?"

**What it demonstrates:** Passages tagged with `mp.canal_clearance` or `mp.dredging`, linked to Pleiades places, plotted on a map of the Fayum. Shows spatial clustering of infrastructure investment.

**Visualization:** Folium/Leaflet map with markers at Pleiades coordinates. Each marker shows the passage, author, date, and evidence layer.

---

## 5. Genre Comparison (genre as first-class metadata)

**Query:** "How is the Nile flood described differently across genres?"

**Filter 1:** Historiography (Herodotus, Diodorus, Strabo) → expect abundance topoi, divine agency, geographic marvels
**Filter 2:** Documentary papyri → expect measurements, administrative orders, flood levels
**Filter 3:** Technical/agronomic writing → expect practical descriptions of irrigation timing

**What it demonstrates:** The same phenomenon (Nile flood) narrated differently depending on genre. The platform makes this visible rather than requiring the scholar to already know where to look.

---

## 6. Cross-Regional Comparison (Case Study 1 preview)

**Query:** "Compare water infrastructure vocabulary between the Nile Valley and the Aegean"

**What it demonstrates:** Which vocab terms cluster in Egypt (saqia, nilometer, basin irrigation, corvée labor) vs Greece (cistern, aqueduct, fountain), showing regionally distinct water management regimes.

**Visualization:** Two-column table or split map showing term frequency by region.

---

## 7. Personnel Network (show the graph layer)

**Query:** "What water-management roles are attested in the Fayum, and who supervised whom?"

**Expected results:** Graph traversal showing hydrophylax → reports to → chomatepeiktes → reports to → strategos. Linked to specific papyrological attestations.

**What it demonstrates:** The knowledge graph captures institutional structure, not just text content.

---

## 8. "Hunger Talk" vs Institutional Response (Case Study 2 preview)

**Query:** "Find passages about grain shortage in Roman Egypt"

**Then split:**
- **Framing:** moralized scarcity language, blame, divine punishment
- **Attestation:** actual decrees, distributions, price controls, tax remissions

**What it demonstrates:** The platform can distinguish rhetorical "crisis" from documented institutional response — the "hunger talk" problem from your project description.

---

## Implementation Priority for May 7

| Query | Requires | Feasibility |
|---|---|---|
| 1. Basic COT retrieval | COT corpus + FAISS | Ready now (use 500-chunk validation) |
| 2. Vocab-filtered | Neo4j with vocab annotations | Needs graph layer |
| 3. Evidence layer | Evidence layer annotations | Available in COT output |
| 4. Spatial/map | Pleiades linking + Folium | Needs entity disambiguation |
| 5. Genre comparison | Genre metadata on chunks | Available (literary vs documentary) |
| 6. Cross-regional | Regional metadata | Available from Perseus metadata |
| 7. Personnel graph | Neo4j with personnel nodes | Needs graph layer |
| 8. Hunger talk | Framing annotations + attestation filter | Available in COT output |

**Minimum viable demo (queries 1, 3, 5):** Can be built with what exists today — COT output + FAISS + evidence layers. No Neo4j or Pleiades linking needed.

**Stretch goal (add query 4):** Needs Pleiades entity disambiguation — the Pelagios Cookbook pattern. Worth attempting if time allows.
