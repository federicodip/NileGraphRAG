# Ecologies of the Ancient Mediterranean: A Spatial AI Platform for Environmental Knowledge in Texts and Landscapes

## 1. Project Summary

This project proposes a spatially-aware AI research platform to study ancient Mediterranean ecologies by integrating textual, archaeological, and gazetteer data. Focusing on c. 500 BCE–300 CE, it will develop digital methods for identifying and analyzing ecological knowledge in ancient sources and linking that knowledge to specific places, times, and material contexts.

Technically, the project combines domain-adapted natural language processing, knowledge-graph construction, and retrieval-augmented generation (RAG) with geographic information to produce a research and retrieval tool for "Ecologies in Past Cultures", one of the core areas of the new Department of Archaeology, Classical Philology and Ancient Studies (IAKA) at the University of Zurich.

Substantively, the project will deliver case studies on water management, agricultural risk, and environmental crisis discourse in selected Mediterranean regions. These case studies are designed to treat "ecological knowledge" as (i) spatially anchored (place-linked discourse and regionally patterned practice), (ii) genre-shaped (historiography vs technical/agronomic writing vs documentary texts), and (iii) institutionally mediated (rights, obligations, maintenance regimes, fiscal systems, and governance capacity). (Horden and Purcell 2000; Butzer 2005; Post 2022; Cordovana 2023) In each cluster, the platform's distinctive contribution is to make it possible to move systematically between (a) attested textual claims, (b) inferred events and practices, (c) interpretive framings (divine agency, mismanagement, natural cycles), and (d) archaeological and landscape evidence—without collapsing these evidentiary layers into a single undifferentiated "fact." (Harris 2013; Haldon et al. 2018; Post 2022)

Methodologically, it will demonstrate how recent advances in AI—LLMs, graph-based retrieval, and multimodal linking—can be made transparent, auditable, and genuinely useful for ancient historians, philologists, and archaeologists. In particular, the platform is designed to support evidence-integration questions that are central to current ancient environmental history: where and why textual claims about infrastructure, shortage, or crisis align with material and spatial evidence, and where divergence is systematic (genre effects, elite bias, rhetorical tropes, or uneven preservation). (Butzer 2005; Harris 2013; Post 2022)

To make ecological extraction and querying stable and interoperable, the project will develop an explicit "Ancient Ecology Vocabulary": a controlled vocabulary and light ontology that provides a shared label set for NLP (e.g., "water infrastructure", "hazard event", "storage practice") and a durable semantic layer for data integration. This vocabulary will be published as a SKOS vocabulary with persistent URIs and versioned snapshots deposited on Zenodo with DOIs, following the FAIR vocabulary publication framework of Cox et al. (2021) and the model established by Heřmánková et al. (2025) for epigraphic vocabularies. Its terms will be grounded in published papyrological scholarship—particularly Bonneau's (1993) systematic inventory of Greek water-management terminology—and cross-referenced to Pleiades place types, Getty AAT, and Wikidata via `skos:closeMatch` mappings, allowing IAKA colleagues to reuse the same concepts, identifiers, and relations across projects rather than developing one-off taxonomies.

To bridge the language gap between ancient source languages and modern retrieval systems, the project employs Context-Oriented Translation (Iwata et al. 2024): LLM-generated English paraphrases optimized for semantic search, which have been shown to triple retrieval accuracy over raw ancient-language embeddings in preliminary evaluation.

Over 3.5 years, I will (1) build the spatial AI platform, (2) publish a series of peer-reviewed studies in historical ecology and ancient environmental history, and (3) use the platform as the core of a habilitation project at the IAKA.

## 2. Theoretical Framework

Research on ancient ecologies has grown significantly under labels such as historical ecology, landscape archaeology, and environmental history. These approaches emphasize long-term, regionally specific interactions between human communities and environments—water systems, agricultural regimes, landscapes of risk—rather than treating "nature" as a static backdrop. (Horden and Purcell 2000; Butzer 2005; Harris 2013; Post 2022) A further consequence of this turn is that "environmental" phenomena are increasingly treated as mixed-causation objects: climatic variability, land-use decisions, connectivity, and institutions interact, and historical explanation depends on keeping these interactions explicit rather than defaulting either to environmental determinism or purely rhetorical readings. (Butzer 2005; Haldon et al. 2018; Erdkamp, Manning and Verboven 2021)

Digital infrastructures for ancient world studies have likewise advanced. Gazetteers such as Pleiades, epigraphic databases, digital text corpora, and archaeological datasets have made spatial and textual data more accessible. Recent work on FAIR vocabularies for epigraphy (Heřmánková et al. 2025) and linked-data integration for classical authors and works (Berti 2025, LAGL) has established practical models for publishing controlled vocabularies as Linked Open Data with persistent identifiers. The ATR4CH methodology (Schimmenti et al. 2025) has demonstrated that LLM-based knowledge extraction can be systematically coordinated with ontological frameworks such as CIDOC-CRM and HiCo to produce auditable, provenance-tracked knowledge graphs from cultural heritage texts. At the same time, recent work in digital humanities and AI has shown that LLMs supplemented by domain-specific retrieval (RAG) can support scholarly search and exploration over large corpora, provided that they are grounded in transparent citation and rigorous evaluation.

However, there is still no integrated, spatial AI platform focused specifically on ancient ecologies that ties environmental vocabulary and events in texts to places and regions, connects texts to archaeological and landscape data, and supports interactive, map-based querying by scholars without requiring them to manage the underlying AI infrastructure. (Post 2022)

The proposed project addresses this gap. Conceptually, it is aligned with historical ecology's emphasis on multi-scalar, collaborative reconstruction of landscape histories; methodologically, it leverages recent, evaluated AI workflows from my existing work on RAG systems and graph-based retrieval for Ancient World corpora. Its case-study design also foregrounds a central methodological pressure point in the field: the need to move between event, practice, and discourse, and to make visible when "crisis language" is functioning as moral diagnosis, political critique, or conventional narrative form rather than straightforward reportage. (Post 2022; Cordovana 2023; Walter 2016)

A further gap—especially relevant for interdisciplinary collaboration at IAKA—is semantic: even when texts, places, and archaeological datasets are available, they often remain difficult to integrate because "ecological" categories are implicit, locally defined, or encoded differently across projects. The project therefore treats ontology and controlled vocabulary design not as an optional add-on but as an enabling layer for reproducible NLP and sustainable integration. The "Ancient Ecology Vocabulary" will provide explicit, versioned definitions for core ecological concepts and relations (infrastructure, environmental phenomena, practices, events, attestations, and interpretive frames), with mappings to widely used standards where possible so that ecological annotations remain portable and comprehensible across datasets and research teams.

## 3. Research Questions and Objectives

The central research question guiding this project is: **How did ancient Mediterranean societies describe, interpret, and manage their environments, and how can AI-assisted, spatially-aware analysis of texts and archaeological data reveal patterns in ecological knowledge and practice?**

Building on this, the project pursues four closely linked objectives. First, on the conceptual level, it aims to develop an operational working model of "ecological knowledge" in ancient Mediterranean sources, encompassing categories such as water management, agricultural regimes, climate and weather events, and environmental risk. This working model will be operationalized as a controlled vocabulary and light ontology (the "Ancient Ecology Vocabulary"), so that conceptual categories correspond to explicit, citable definitions and stable identifiers rather than ad hoc labels. (Post 2022; Cordovana 2023) The vocabulary's infrastructure domain draws on Bonneau's (1993) systematic inventory of Greek water-management terminology attested in papyri, with terms mapped to Pleiades place types and Trismegistos GEO categories. A pilot version (v0.3) covering 80 terms across six domains—hydraulic features, water bodies, hydrological phenomena, management practices, personnel, and interpretive framings—has been developed and will be iteratively expanded as case studies proceed. The model will explicitly encode distinctions that are crucial for historical interpretation: mentions/attestations versus inferred events, and events/practices versus interpretive framings (e.g., mismanagement, divine punishment, natural cycles). (Hunt and Marlow 2019; Scheer 2019; Walter 2016) This evidence-grading model will be formalized using the Historical Context Ontology (HiCo; Daquino and Tomasi 2015), which represents each annotation as an `InterpretationAct` with explicit provenance, and informed by the SEBI ontology's approach to attaching evidence with polarity using RDF-star (Pasqual 2025; Schimmenti et al. 2025). This ensures that evidence layers are not project-internal labels but interoperable, LOD-native constructs.

Second, in terms of data and infrastructure, it will integrate textual, gazetteer, and archaeological datasets into a coherent, georeferenced research infrastructure suitable for AI-assisted analysis within IAKA. In order to maximize reuse and interoperability across IAKA projects, the project's schema will be designed to align with existing, widely adopted semantic standards used in archaeology and cultural heritage data integration, and to support export or mapping into those standards as needed.

Third, on the methodological side, the project will design and implement AI workflows—natural language processing, knowledge graphs, and retrieval-augmented generation—tailored to ecological semantics in ancient texts, with particular emphasis on transparency, reproducibility, and scholarly auditability. The NLP pipelines will be explicitly grounded in the "Ancient Ecology Vocabulary" so that extraction outputs can be traced from terms to concepts to decisions, and so that evaluation can be performed at the level of clearly defined categories. Because the case studies require genre-aware interpretation, the platform will treat source type and genre as first-class metadata and support comparison of how ecological phenomena are narrated differently in historiography, technical/agronomic writing, and documentary records. (Post 2022; Cordovana 2023)

Finally, the project will develop historical case studies by applying the platform to three thematic clusters: water and irrigation in selected regions (for example, the Nile valley, the Aegean, and North Africa); agricultural risk, famine, and storage; and discourse around environmental crisis and resilience. Each case study will combine computational results with close reading and archaeological context to produce publishable research contributions to the "Ecologies in Past Cultures" area and related fields. Across all three clusters, the unifying analytical move is to treat ecological knowledge as simultaneously material (infrastructures and practices), institutional (rights, obligations, governance capacity), and discursive (crisis vocabularies, blame, divine agency), and to test textual claims against spatial and archaeological patterns rather than presuming either simple correspondence or simple distortion. (Horden and Purcell 2000; Butzer 2005; Harris 2013; Post 2022)

The project focuses on the Mediterranean basin, with particular attention to three case-study regions where both textual and archaeological evidence are relatively rich: the Nile valley, the Aegean, and Roman North Africa. Chronologically, it covers the period from roughly 500 BCE to 300 CE, encompassing the Classical, Hellenistic, and Roman imperial eras and enabling comparative analysis across different political and ecological regimes.

The textual component of the project will draw initially on three main types of sources. First, it will target literary, historiographical, and technical texts that contain ecological content, including discussions of agriculture, weather, hydrology, and natural resources. Second, it will incorporate epigraphic and papyrological corpora that record land use, water rights, harvests, and environmental events. Third, it will make use of open-access scholarly corpora—such as ISAW Papers and associated collections—which I have already employed as testbeds in my previous "AI Librarian" work, and extend these with further ancient source corpora wherever licensing permits. For bulk, machine-actionable ingestion, priority will be given to corpora with explicit open licences and downloadable structured formats (TEI/EpiDoc XML and/or RDF/linked-data exports), including papyrological and epigraphic hubs that provide stable identifiers and rich metadata suitable for place-linking and evidence modelling. (EDH - Universität Heidelberg)

The spatial and archaeological dimensions of the project will be grounded in established gazetteers, especially Pleiades, for places, regions, rivers, and coastal features. These will be enriched with archaeological datasets documenting sites, hydraulic infrastructure, and land use, drawn from existing projects and developed in collaboration with IAKA staff. Where feasible, paleoclimate and environmental reconstructions relevant to the case-study regions will be incorporated as contextual layers rather than primary data. In these cases, the project will treat environmental reconstructions explicitly as contextual "observations" with clear provenance (rather than as direct determinants), so that any link between proxy signals and historical interpretation remains transparent and contestable. (Haldon et al. 2018; Harris 2013) The platform is deliberately designed to be extensible, so that additional corpora and datasets can be onboarded without major structural changes.

## 4. Datasets and Data Sources

This project's data strategy prioritizes explicitly licensed, machine-actionable corpora that can be ingested, versioned, and redistributed as part of a reproducible research infrastructure, while treating important but restricted scholarly resources as link-out / lookup layers rather than bulk-ingested datasets.

### 4.1 Papyrology

Papyrological data will come from DDbDP, HGV, and DCLP, which provide stable identifiers, EpiDoc/TEI XML transcriptions, and rich descriptive metadata suitable for event/practice extraction and provenance-aware modelling. Records and editions in this ecosystem are explicitly distributed under CC BY 3.0, making them suitable for bulk ingestion into a KG with attribution. (Universität Heidelberg)

Where papyri.info surfaces collection-level metadata and images via APIS and holding-institution systems, the project will ingest (i) the text and metadata where licensing permits and (ii) treat images as rights-variable, item-level resources: image URLs may be stored as external references, but rights will be tracked per record/collection rather than assumed uniform.

For cross-database identifier alignment (especially across papyri and epigraphy), the project will make use of widely adopted crosswalk identifiers where permitted; resources that function primarily as subscription/discovery layers (not open-licensed bulk datasets) will be used conservatively as lookup/authority layers rather than rehosted.

### 4.2 Greek and Latin epigraphy

Open EpiDoc dumps where available; aggregators as discovery layers:

- **EDH** (Epigraphic Database Heidelberg) Open Data repository, which provides downloadable open data under CC BY-SA 4.0, suitable for KG ingestion with attribution and share-alike compliance.
- **EDR** (Epigraphic Database Roma) via its EpiDoc dataset releases on Zenodo (used for bulk ingestion where applicable), providing structured export suitable for NLP pipelines and graph modelling.
- **I.Sicily**, an EpiDoc-first corpus with explicit statements that its data are downloadable and reusable under CC BY 4.0, making it suitable as a high-quality epigraphic feedstock for place-linked ecological attestations.
- **U.S. Epigraphy Project** (USEP) for object-level linking (especially where museum/collection metadata aids spatial reasoning), noting its CC BY-NC-SA 4.0 constraints, which will be respected in any redistribution.

Large aggregators and portals (e.g., Europeana/EAGLE-style federation layers) are methodologically useful for discovery and reconciliation, but because licensing often varies at item level, they will be treated as routing layers rather than "bulk ingestion" sources.

### 4.3 Greek and Latin texts

For literary, historiographical, and technical/agronomic texts, the project will rely on open corpora that provide stable text structures and/or CTS/TEI conventions:

- **Perseus Digital Library** (PerseusDL) canonical corpora, distributed under CC BY-SA 4.0 and widely used for DH pipelines, enabling reproducible text chunking and citation.
- **Open Greek and Latin / First1KGreek** and related open repositories (where the relevant subcorpora and licences support ingestion), used to extend coverage for Greek and Latin texts in machine-actionable XML under open licensing.

Major subscription corpora (e.g., comprehensive Greek and Latin libraries) are crucial for research completeness, but their terms typically prohibit bulk copying and redistribution. Accordingly, they will be used only within the constraints of local licensed access (e.g., for scholar-side reading and citation), while the platform's ingestible KG layer will remain grounded in open corpora. For example, the TLG terms explicitly prohibit copying/downloading/redistribution beyond limited excerpts, so it is treated as non-ingestible.

### 4.4 Gazetteers and spatial authorities

Spatial reconciliation will be grounded in Pleiades place identifiers and types (and, where appropriate, compatible linked-places formats used in the linked-pasts ecosystem). Gazetteer entities will serve as the platform's shared spatial reference layer, supporting consistent place linking across papyrological, epigraphic, and literary corpora.

### 4.5 Bibliography and secondary scholarship (supporting layers)

Curated bibliographies and scholarly discovery tools (e.g., papyrological bibliographies) are essential for interpretive control, but they are not always published under open data licences. Where licensing is unclear or restrictive, these resources will be used for citation and manual verification and will not be bulk-ingested into the redistributable KG.

### 4.6 Practical rights and provenance handling (platform-level)

Because the project's core methodological commitment is auditability, the ingestion layer will store:

- dataset/source provenance (release, retrieval date, record identifiers),
- explicit licence metadata where available,
- and, for rights-variable media (especially images), an item-level "do not assume open" rule: store links and rights statements rather than rehosting media unless licensing is unambiguous.

## 5. Methods and Work Packages

The project is organized into four main work packages (WPs). Throughout, I will draw on my experience building the AI Librarian—a RAG system over ~2,000 multilingual Ancient World publications with evaluated performance—and GraphRAG-ISAW, a knowledge-graph extension that links text chunks to Pleiades place entities via Neo4j and exposes graph-based retrieval.

### WP1 – Data Integration and Spatial Infrastructure

The project will first harvest and normalize textual corpora, where licensing allows, with a focus on ecological content. It will build data pipelines for text extraction from varied formats (HTML, PDF, and both OCR'd and non-OCR'd texts), followed by chunking and metadata enrichment at the level of work, section, language, date, and source type.

A critical innovation is Context-Oriented Translation (COT), following Iwata et al. (2024): each text chunk is translated by an LLM into a context-aware English paraphrase optimized for semantic search rather than literary fidelity. Unlike expert translation, COT prioritizes disambiguation of polysemous terms, resolution of pronouns and anaphoric references, and explicit statement of argument structure—producing embeddings that capture meaning rather than surface form. Preliminary evaluation on 500 chunks from the Perseus corpus demonstrated that COT-based embeddings tripled Recall@1 (0.17 → 0.54) and doubled Mean Reciprocal Rank (0.27 → 0.63) compared to raw ancient-language embeddings, consistent with Iwata et al.'s findings on Plato's works.

These pipelines will also support the geo-referencing of toponyms using gazetteers such as Pleiades. Named entity recognition will leverage existing models for ancient Greek (Palladino and Yousef 2024, UGARIT/grc-ner-bert, F1=88.87%) and standard English NER on COT translations, with entity disambiguation following the candidate-based linking pattern demonstrated by the Pelagios Cultural Heritage AI Cookbook (2025). Author metadata will be enriched via LAGL's Wikidata property P12869 (Berti 2025), which provides geocoded biographical data for over 1,200 classical authors linked to CTS URNs already present in the Perseus corpus. In practice, bulk ingestion will prioritize openly licensed TEI/EpiDoc/RDF corpora with stable identifiers (notably papyrological and epigraphic datasets distributed under explicit Creative Commons terms), while access-bound corpora will be used as link-out/discovery layers rather than rehosted datasets.

On this basis, the project will implement a knowledge-graph schema (for example, in Neo4j) that connects text segments (chunks), works (articles or texts), places (Pleiades entities and local site identifiers), and, where relevant, people and institutions. The knowledge graph's internal schema will be mapped to CIDOC-CRM classes via the neosemantics (n10s) plugin, enabling on-demand RDF/Turtle export for interoperability with ARIADNE and the broader ancient-world LOD ecosystem. Spatial visualization will follow the Linked Places Format (Pelagios Network), rendering attestation maps via Peripleo. The result will be a stable, versioned data layer that can be reused by other IAKA projects. The main deliverable for this phase will be a working, documented graph and spatial database covering the selected corpora and regions.

### WP2 – NLP for Ecological Semantics in Ancient Texts

The project will develop an ecology-specific lexicon of terms referring to water sources and infrastructures (such as rivers, canals, cisterns, wells, and harbors), crops, pastoral practices and soils, climate and weather phenomena (including droughts, floods, storms, and winds), and forms of environmental risk such as famine, plagues, and disasters. Because the case studies require distinguishing practice, event, and discourse, the lexicon and label set will also include (i) institutional and governance terms tied to resource management (rights, obligations, labour regimes, civic/private investment, estate/temple administration), (ii) storage and provisioning terms (granaries, reserves, distributions, requisitions, price measures), and (iii) "crisis vocabulary" markers (portents/signs, prodigies, moralized scarcity language, blame attributions). (Cordovana 2023; Hunt and Marlow 2019; Scheer 2019; Walter 2016)

In parallel, the project will formalize these categories as the "Ancient Ecology Vocabulary," so that NLP labels correspond to explicit concepts with stable identifiers, definitions, and relationships (broader/narrower, related-to). This provides a disciplined bridge from text to annotation: extraction is not merely "tagging keywords," but linking passages to defined concepts, enabling transparent comparison across corpora, languages, and regions. Where possible, vocabulary entries will be mapped to established external vocabularies for environmental and cultural-heritage features, while retaining a domain-specific layer for concepts that are specifically ancient or historically contingent.

Using LLM-assisted annotation, the project will identify ecological entities and events in Greek, Latin, and other relevant languages and classify both the types of events and their rhetorical framing—for example, whether they are presented as divine punishment, mismanagement, or part of a natural cycle. Crucially, rhetorical framing will be encoded as an explicit interpretive annotation attached to an attestation (a text passage) rather than treated as a "fact" about the event itself. This separation between (a) attested mentions, (b) inferred events, and (c) interpretive framings is designed to keep outputs auditable and to preserve the scholar's ability to contest model choices. It also supports a core case-study goal: distinguishing "hunger talk" or moralized crisis rhetoric from signals that correlate with institutional actions (decrees, repairs, distributions, tax measures), preserving an auditable chain from passage → label → inference. (Cordovana 2023; Post 2022)

To keep extraction interpretable and robust, the project will implement weakly supervised and rule-based components rather than relying on opaque end-to-end models. Extraction quality will be evaluated against small, manually annotated gold-standard datasets created in collaboration with colleagues at IAKA. Gold-standard annotation will be conducted using INCEpTION (Klie et al. 2018), a web-based platform supporting custom tagsets aligned with the Ancient Ecology Vocabulary, Wikidata entity linking, and inter-annotator agreement measurement. Evaluation will follow the HIPE framework established for historical NER (Ehrmann et al. 2020) and the multi-level evaluation strategy of ATR4CH (Schimmenti et al. 2025), combining component-level F1 scores with G-EVAL for overall discourse representation fidelity. Evaluation will operate at the level of the vocabulary concepts (e.g., precision/recall for "canal" vs "aqueduct," "famine episode" vs "scarcity rhetoric," "low-Nile year" vs generic flood talk), ensuring that success criteria remain legible to non-technical collaborators. The main deliverable will be evaluated NLP pipelines that tag ecological vocabulary and events, link them to concepts in the "Ancient Ecology Vocabulary," and integrate these annotations into the knowledge graph.

### WP3 – Spatial Graph-RAG and Scholar Interface

The project will extend the knowledge graph with explicit relations linking text segments (chunks) to places and ecological events to places or regions, building on the deterministic linking approach I previously implemented for ISAW Papers and Pleiades. This enriched graph will be integrated with a vector-based retrieval backend (for example, FAISS or pgvector), creating a graph-augmented RAG architecture in which semantic search retrieves relevant chunks while graph relations constrain or re-rank results by place, time, or event type.

On top of this infrastructure, the project will design a scholar-facing interface that enables map-based exploration of ecological events and references, offers filters by region, period, source type, and ecological category, and supports natural-language querying via RAG with explicit citation and source highlighting. To ensure transparency and reliability, the system will implement observability and guardrails, including logging of queries and retrieval behavior, monitoring of accuracy and "hallucination" rates in generated answers, and clear surfacing of uncertainty and limitations to users. The main deliverable will be a prototype web application deployed within the IAKA environment and usable for both research and teaching.

### WP4 – Historical Case Studies and Synthesis

Using the platform, I will conduct three interconnected case studies. The case studies are deliberately structured around question-types that benefit from spatial linking, genre-aware extraction, and evidence integration (texts ↔ places ↔ material datasets). Each cluster will therefore generate both historical outputs (articles/chapters) and methodological outputs (refined vocabulary entries, evaluation sets, and graph relations) that feed back into WP1–WP3. (Butzer 2005; Harris 2013; Post 2022)

**Case Study 1: Water and infrastructure** (Nile valley + Aegean; extendable to North Africa). The first case study will analyze water-management discourse and practice in at least two regions (for example, the Nile valley and the Aegean), combining textual references to irrigation, wells, cisterns, qanats, harbours, flood basins, and floods with archaeological evidence for hydraulic infrastructure. It will treat water not only as supply but as a field where material systems, institutional regimes, and risk management become historically legible. (Horden and Purcell 2000; Butzer 2005; Harris 2013; Post 2022) The study will address:

- **Water as practice (material + institutional):** what hydraulic features are described (canals, dikes, wells, cisterns, qanats, harbours, flood basins), and what technical vocabularies cluster around them by genre (historiography vs agronomic/technical writing vs documentary texts). It will also ask how rights, obligations, and maintenance regimes are articulated (water-sharing rules; corvée labour; civic vs private investment; temple/estate management), and how these regimes differ across regions and political settings. (Cordovana 2023; Post 2022)
- **Water as risk:** how floods, low-Nile years, drought, and salinization are framed as causes of crisis (or as predictable cycles), and what counts as mismanagement versus "nature" or divine agency. The platform will allow these framings to be tracked explicitly as annotations on attestations and then mapped spatially. (Hunt and Marlow 2019; Scheer 2019; Walter 2016)
- **Water and political economy:** when hydraulic investment signals state capacity (imperial/royal interventions, city euergetism, estate intensification) versus local cooperation or household-level adaptation, and how water infrastructures map onto settlement patterns and connectivity (microecologies and interdependence across coast/river valley/hinterland). (Horden and Purcell 2000; Horden and Purcell 2019; Butzer 2005)
- **Evidence-integration (a platform-native question):** where textual claims about infrastructure match (or diverge from) archaeological and landscape evidence, and whether divergences are systematic (genre effects, rhetorical tropes, elite bias, uneven preservation). The case study will explicitly analyse spatial clustering of water-facility references (place-linked discourse) and temporal clustering (periods of investment, repair, or failure). (Butzer 2005; Harris 2013)

**Case Study 2: Agricultural risk, famine, and storage** (comparative focus on Italy + Egypt). The second case study will examine how harvest failures, storage practices, and food shortages are described across different Mediterranean polities, and how such events are spatially distributed and temporally clustered. It treats famine and scarcity as risk ecology: hazards interact with institutions, connectivity, and inequality, and the textual record captures both event signals and rhetorical constructions. (Garnsey 1988; Butzer 2005; Izdebski, Mordechai and White 2018; Van Bavel et al. 2020) Key questions include:

- **Risk ecology and coping strategies:** what hazards recur (drought, flood failure, plant disease, war disruption, price shocks), how they are ranked or narrated as "normal variability" vs "crisis," and what coping strategies are described or implied (crop diversification, storage and redistribution, market integration, fiscal relief, migration, rationing, price controls, religious responses). (Butzer 2005; Erdkamp, Manning and Verboven 2021)
- **Storage, logistics, and political economy:** how storage practices (granaries, estate storage, civic reserves, temple granaries) vary across regions and regimes, and how they relate to taxation, rents, and military supply. The study will compare cases where texts stress household/estate resilience versus cases foregrounding state capacity (annona-style provisioning, emergency imports, imperial benefaction). (Garnsey 1988; Cheung 2020; Temin 2001)
- **Discourse vs event (genre-aware extraction):** how authors encode scarcity (metaphors, moral critique, blame) and how this differs by genre (annalistic historiography vs agronomy vs documentary papyri/inscriptions). A central methodological aim is to distinguish "hunger talk" from signals that correlate with institutional actions (decrees, distributions, repairs, tax measures), preserving an auditable chain from passage → label → inference. (Cordovana 2023; Post 2022)
- **Spatial–temporal patterning (the platform's distinctive angle):** where famine/shortage references cluster geographically (ports vs inland; imperial cores vs margins; microregions), how clusters shift over 500 BCE–300 CE, and whether "bad years" synchronize across regions (shared climate signals / connectivity) or remain patchy (microecological variability; war, local governance, market access). This directly motivates map-based querying and time-sliced visualisation in WP3. (Horden and Purcell 2000; Horden and Purcell 2019; Haldon et al. 2018)

**Case Study 3: Environmental crisis and resilience** (drought, plague, earthquakes, and "signs"). The third case study will analyze language and imagery related to environmental crises—such as drought, plague, earthquakes, and "signs"—and investigate how communities frame resilience, divine intervention, or blame. It treats crisis as both event and interpretive grammar, examining how causal explanations distribute responsibility across divine punishment, elite failure, collective immorality, natural cycles, or imperial misrule. (Redman 2005; Folke 2006; Walter 2016; Post 2022) It will address:

- **Crisis vocabularies and causal grammars:** what linguistic repertoires mark "crisis" (drought, plague, earthquake, portents, prodigies, "signs") and how narrative forms differ (prodigy catalogues, historiographic moral exempla, technical rationalization, documentary "administrative crisis"). (Scheer 2019; Hunt and Marlow 2019; Post 2022)
- **Resilience as practice and as ideology:** what practical adaptations appear (rebuilding, mobility, institutional reforms, ritual innovations), what counts as resilience in different communities (persistence, recovery, transformation, strategic retreat), and how resilience costs are distributed (who bears the burden of coping—by status, legal category, and institutional position). (Izdebski, Mordechai and White 2018; Van Bavel et al. 2020)
- **Shock vs slow stress:** how slow variables (repeated flood failures, long dry phases, incremental degradation narratives) interact with shocks (epidemics, earthquakes, volcanic events) in the textual record, and whether "collapse" narratives are supported by discontinuity or countered by evidence of continuity through institutional flexibility and connectivity. (Butzer 2005; Erdkamp, Manning and Verboven 2021; Harper 2017)
- **Spatial analytics:** whether crisis references form corridors (seismic zones, river basins, disease networks, coastal nodes), how those corridors change across Classical → Hellenistic → Imperial contexts, and whether the platform can differentiate "discursive contagion" (shared tropes moving across regions) from localized crisis ecologies grounded in microregional conditions. (Mordechai and Pickett 2018; Horden and Purcell 2000; Horden and Purcell 2019)

Each case study will result in journal articles or book chapters and will feed into a larger habilitation manuscript on ecologies of the ancient Mediterranean.

In sum, the project will produce both a substantive contribution to ancient Mediterranean environmental history and a durable piece of digital infrastructure for IAKA. By combining historical ecology, close engagement with texts and material evidence, and rigorously evaluated AI workflows, it will demonstrate how large language models, knowledge graphs, and spatial retrieval can be integrated into day-to-day research without sacrificing scholarly control. (Haldon et al. 2018; Post 2022) The spatial AI platform, the NLP pipelines, and the case-study publications together form the core of a habilitation focused on "Ecologies in Past Cultures," while also laying the groundwork for future work on cultural heritage, agency, and reception within the department. Because the system is designed to be transparent, extensible, and reusable, it can support graduate training, collaborative projects, and teaching in archaeology, ancient history, and classical philology well beyond the project's initial 3.5-year span.

## References

Berti, M. (2025) 'Linked Ancient Greek and Latin (LAGL) and Wikidata: Structuring and Reusing Data of Classical Literature', *Journal of Open Humanities Data* 11. doi:10.5334/johd.423.

Bonneau, D. (1993) *Le régime administratif de l'eau du Nil dans l'Égypte grecque, romaine et byzantine*, Leiden: Brill.

Butzer, K.W. (2005) 'Environmental history in the Mediterranean world: cross-disciplinary investigation of cause-and-effect for degradation and soil erosion', *Journal of Archaeological Science* 32(12), pp. 1773–1800.

Cheung, C. (2020) 'Managing food storage in the Roman Empire', *Quaternary International* 597, pp. 63–75.

Cordovana, O. (2023).

Cox, S.J.D., Gonzalez-Beltran, A.N., Magagna, B., and Marinescu, M.-C. (2021) 'Ten simple rules for making a vocabulary FAIR', *PLOS Computational Biology* 17(6), e1009041.

Daquino, M. and Tomasi, F. (2015) 'Historical Context Ontology (HiCo): A Conceptual Model for Describing Context Information of Cultural Heritage Objects', *MTSR 2015*, Springer.

Erdkamp, P., Manning, J.G. and Verboven, K. (eds) (2021).

Folke, C. (2006).

Garnsey, P. (1988) *Famine and Food Supply in the Graeco-Roman World*, Cambridge: Cambridge University Press.

Haldon, J. et al. (2018) 'History meets palaeoscience', *Proceedings of the National Academy of Sciences* 115(13).

Harris, W.V. (ed.) (2013) *The Ancient Mediterranean Environment Between Science and History*, Leiden: Brill.

Harper, K. (2017).

Heřmánková, P. et al. (2025) 'From Fragmented Data to Linked History: Developing the FAIR Epigraphic Vocabularies', *Journal of Open Humanities Data* 11. doi:10.5334/johd.428.

Horden, P. and Purcell, N. (2000) *The Corrupting Sea*, Oxford: Blackwell.

Horden, P. and Purcell, N. (2019).

Hunt, D. and Marlow, L. (eds) (2019).

Iwata, N., Tanaka, I. and Ogawa, J. (2024) 'Improving Semantic Search Accuracy of Classical Texts through Context-Oriented Translation', *IPSJ Symposium on Humanities and Computer Science*.

Izdebski, A., Mordechai, L. and White, S. (2018).

Klie, J.-C. et al. (2018) 'The INCEpTION Platform: Machine-Assisted and Knowledge-Oriented Interactive Annotation', *COLING 2018*.

Mordechai, L. and Pickett, J. (2018).

Palladino, C. and Yousef, T. (2024) 'Development of robust NER Models and Named Entity Tagsets for Ancient Greek', *LT4HALA @ LREC-COLING 2024*.

Pasqual, V. (2025) *The Critical Inquiry in Humanities Knowledge Graphs*, PhD thesis, University of Bologna.

Pelagios Network (2025) 'The Cultural Heritage AI Cookbook', Lorentz Center workshop, Leiden.

Post, R. (2022) 'Environment, sustainability, and Hellenic studies', *The Journal of Hellenic Studies* 142, pp. 317–333.

Redman, C.L. (2005).

Scheer, T.S. (ed.) (2019).

Schimmenti, A., Pasqual, V., Vitali, F. and van Erp, M. (2025) 'Knowledge Graphs Generation from Cultural Heritage Texts: Combining LLMs and Ontological Engineering for Scholarly Debates', arXiv:2511.10354.

Temin, P. (2001) 'A market economy in the early Roman Empire', *Journal of Roman Studies* 91, pp. 169–181.

Van Bavel, B. et al. (2020).

Walter, F. (2016).
