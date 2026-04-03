# Ancient Ecology Vocabulary — Construction Methodology

## Purpose

The Ancient Ecology Vocabulary is a controlled vocabulary for evidence-graded annotation of environmental and infrastructural claims in ancient Nile Valley texts (500 BCE–300 CE). It serves a dual function:

1. **ML label set** — used by an LLM during Context-Oriented Translation (COT) to classify passages against stable concept identifiers
2. **Semantic layer** — designed for linked-data interoperability, with mappings to Pleiades URIs and Trismegistos source terms

The vocabulary targets ecological and infrastructural knowledge at a granularity appropriate for historical interpretation, not engineering specification.

## Version History

| Version | Date | Terms | Changes |
|---------|------|-------|---------|
| v0.1 | 2026-04-03 | 29 | Initial skeleton: 4 domains, basic infrastructure/phenomena/practices/framings |
| v0.2 | 2026-04-03 | 60 | Added Pleiades URIs, Trismegistos Greek terms, new domains (water_bodies, personnel) |
| v0.3 | 2026-04-03 | 78 | Integrated Bonneau (1993) terminology; corrected source-term assignments; expanded all domains |

## Sources and How They Were Used

### 1. Bonneau, *Le régime administratif de l'eau du Nil* (Brill, 1993)

**Role:** Primary source for Greek water-management terminology attested in papyri.

**What we used:**
- **Table of Contents (p.7-11):** Bonneau organizes Part 1 ("La Terminologie") into three functional sections: A. Conveyance/Evacuation, B. Retention (dikes, basins), C. Distribution (canal mouths, gates, machines). Each Greek term that warrants its own TOC heading represents a distinct concept in the ancient administrative vocabulary. These headings became our term inventory.
- **Greek Index (p.351-358):** Cross-referenced against the TOC to verify term assignments and identify sub-terms. The index lists ~300+ Greek words with page references; we filtered to nouns naming infrastructure, roles, or practices (excluding verbs, adjectives, fiscal abstractions).
- **Part 2 "Le Fonctionnement" (p.139-255):** Source for personnel roles (chômatepeiktês, neïlomêtrês, limnastês, etc.) and maintenance operations (anapsêsmos, parylismos, limnasmos).

**What we corrected:**
- v0.2 listed `emblema` as a source term for "sluice gate" following Trismegistos. Bonneau (p.61-66) shows that emblema is actually a *transverse dike* (digue transversale). The sluice gate is `thyra` (p.97). v0.3 fixes this.
- v0.2 grouped all water-lifting devices under one term (`hf.shaduf`). Bonneau Part 1.C.3 (p.115-137) distinguishes six distinct technologies: kêlôneion (shaduf), kochlias (Archimedean screw), trochos (water wheel), tympanon (compartmented wheel), organon (taibout), mêchanê (saqia). v0.3 splits these into four vocabulary entries grouped by mechanism.

**What we deferred:**
- Bonneau's Part 3 ("Administration Générale," p.257-328) covers fiscal and administrative structures (taxes, bureaucratic hierarchies). These are relevant but require a separate "administration" domain, deferred to a future version.
- Fine-grained sub-types (e.g., pleurismos vs diapleurismos for lateral dike reinforcement) are recorded as source_terms within broader entries rather than given separate IDs, to keep the vocabulary at a usable granularity for ML classification.

### 2. Pleiades Place Types Vocabulary

**Role:** Linked-data authority for place and feature types in the ancient world.

**What we used:**
- Extracted 53 water-related terms from the full vocabulary of 229 place types (fetched from pleiades.stoa.org/vocabularies/place-types).
- Used Pleiades URIs as stable identifiers mapped to our terms via the `pleiades` field. This enables future interoperability with Pelagios and other Pleiades-consuming systems.
- Pleiades provided the framework for natural water features (river, lake, spring, marsh, delta, etc.) that Bonneau does not cover (her focus is infrastructure, not geography).

**Gaps in Pleiades:**
- No nilometer, shaduf, saqia, basin irrigation, or sluice gate terms — these are Egypt-specific features not represented in the general Mediterranean vocabulary.

### 3. Trismegistos GEO Status Categories

**Role:** Papyrologically grounded term list with original-language source terms.

**What we used:**
- Extracted all water-related status categories from trismegistos.org/geo/about_status.php, including:
  - "Canal/River/Lake" category (41 terms): dioryx, potamos, limne, choma, emblema, etc.
  - "Well/Water Supply" category (12 terms): krene, pege, phrear, hydreuma, etc.
  - "Harbour" category (5 terms): limen, hormos, portus, etc.
- Trismegistos provided the initial Greek/Latin/Egyptian source-term mappings for v0.2. These were then refined against Bonneau's more authoritative definitions in v0.3.

**Key contribution:** Trismegistos includes Egyptian-language terms (heni, mou, teni, shi, ir) from Demotic and Coptic sources that Bonneau's Greek-focused index omits.

### 4. Abdelwahed & Shehata, "Nile Water Management" (Rosetta 27, 2022)

**Role:** Systematic categorization of water-management personnel from Greek papyri.

**What we used:**
- Personnel role categories: water guards (hydrophylax), shore guards (aigialophylax), divers (nautokolymbêtês), inspectors, and administrative officers.
- Cross-referenced against Bonneau Part 2 for attestation details and hierarchical relationships.

### 5. Getty Art & Architecture Thesaurus (AAT)

**Role:** Upper ontology for cultural heritage interoperability (not directly cited in terms, but informed the category structure).

**What we used:**
- The AAT Hydraulic Structures hierarchy informed our distinction between conveyance, retention, and distribution infrastructure — though Bonneau's own organizational scheme (which predates AAT) turned out to be more appropriate for our domain.

## Design Principles

1. **IDs are stable and never reused.** Once assigned, an ID (e.g., `hf.canal`) persists across versions even if the label or description changes. This ensures annotations made with an earlier version remain valid.

2. **Source terms enable original-language matching.** Each term carries Greek (grc), Latin (lat), and/or Egyptian (egy) source terms so that NLP pipelines can match vocabulary concepts against original-language passages without requiring translation.

3. **Granularity targets historical interpretation, not engineering.** We distinguish a shaduf from a saqia (different labor requirements, different social implications) but do not distinguish sub-types of saqia. The vocabulary should be usable by a historian classifying passages, not by an engineer cataloguing machines.

4. **Evidence layers are orthogonal to domain terms.** A passage about a canal (hf.canal) might be an attestation ("this canal was dug"), an inference ("the canal probably served this basin"), or a framing ("the canal was a gift of the king"). The evidence layer is assigned separately from the domain term.

5. **Bonneau's functional organization is preserved.** Rather than imposing a modern engineering taxonomy, we follow Bonneau's tripartite structure (conveyance → retention → distribution) which reflects how ancient administrators actually categorized water infrastructure.

## What's Missing (Future Work)

- **Bonneau Part 3 terms:** Fiscal and administrative vocabulary (chômatikon tax, naubion, zeugmatikon, etc.) — requires a new "administration/fiscal" domain
- **Arabic-period continuations:** Bonneau covers through the Byzantine period; Arabic administrative vocabulary for the same infrastructure types
- **EpiDoc integration:** Formal mapping to EpiDoc element types for direct annotation of TEI-encoded papyri
- **Confidence calibration:** Empirical assessment of how reliably an LLM can assign these labels, based on inter-annotator agreement with human experts
- **Spatial mappings:** Linking infrastructure terms to specific Pleiades place instances (not just place *types*) for the Nile Valley case study
