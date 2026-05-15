# Manuscript Draft v0｜Methods + Results

> Working title: From Anti-Freezing Claims to Functional Retention: A Critical Scoping Review of Cellulose-Based Wide-Temperature Gels

## 2. Scope, Corpus Construction, and Coding Framework

### 2.1 Review scope

This review focuses on cellulose-based and cellulose-relevant gels reported for wide-temperature, anti-freezing, conductive, sensing, biomedical, energy, or environmentally stable applications. The purpose is not to extract every full-text performance value from the literature, but to map how functional evidence is made visible at the record and abstract level.

The central question is whether claimed temperature tolerance is accompanied by visible evidence of retained function under the claimed temperature conditions. Therefore, the review treats anti-freezing as a functional-evidence problem rather than only a structural-survival problem.

### 2.2 Corpus layers

The literature pool was organized into four evidence layers.

| Layer | Name | Current size | Role in this manuscript |
|---|---|---:|---|
| D0 | Discovery pool | approximately 314 records | Search background and citation reservoir |
| D1 | Structured scoping set | 174 records | Record-level coding and sensitivity reference |
| D2 | Primary analysis set | 156 cellulose-relevant records | Main quantitative results |
| D3 | Full-text exemplar set | 12 core candidates in progress | Narrative examples for the evidence ladder |

Only D2 is used for the main quantitative claims in the Results section. D0 is not used for statistical conclusions. D3 is used to illustrate evidence levels and design trade-offs, not to represent the full field.

### 2.3 Eligibility and exclusion

Records were considered cellulose-relevant when cellulose, cellulose derivatives, nanocellulose, bacterial cellulose, regenerated cellulose, carboxymethyl cellulose, cellulose nanofibers, or cellulose nanocrystals were part of the reported gel system or functional architecture.

Records were excluded from the primary analysis set when the gel system was not cellulose-based or when cellulose relevance could not be established from the local record. Non-cellulose natural polymer systems, such as starch or pure synthetic polymer organohydrogels, were retained only as comparator records when they provided useful design references.

### 2.4 Coding fields

Each record was coded for bibliographic information, cellulose identity, architecture layer, solvent or cryoprotectant layer, network or functional engineering layer, application area, temperature reporting, and visible functional metrics.

The main binary fields were:

| Field group | Coded fields |
|---|---|
| Temperature evidence | `claims_wide_temperature`, `mentions_temp_value`, `has_negative_temp`, `lowest_neg_temp` |
| Functional metrics | `mentions_conductivity`, `reports_cond_value`, `mentions_GF`, `reports_GF_value`, `mentions_self_healing`, `reports_heal_value`, `mentions_adhesion`, `reports_adh_value` |
| Other performance dimensions | `mentions_anti_drying`, `mentions_sustainability`, `mentions_transparency`, `reports_mech_value` |
| Set membership | `reading_depth`, `has_cellulose` |

### 2.5 Interpretation boundary

Absence of a metric in the coded record was interpreted as “not visible at the abstract or record level,” not as “absent from the full text.” This distinction is essential because the purpose of the scoping analysis is to evaluate evidence visibility and reporting habits, rather than to make final claims about every full-text dataset.

### 2.6 Full-text exemplar workflow

Twelve cellulose core candidates were selected for follow-up verification based on five criteria: clear cellulose participation, visible temperature evidence, visible functional metrics, strategy coverage, and local note richness. For each exemplar, the next full-text pass will extract only five fields: tested temperature, in-situ low-temperature function, room-temperature baseline, cycle or duration evidence, and trade-off or cost.

## 3. Evidence Visibility Landscape

### 3.1 Dataset composition

The structured scoping set contained 174 records. Among them, 156 were classified as cellulose-relevant and used as the primary analysis set. This primary set forms the denominator for the main reported percentages.

The corpus was dominated by recent literature and by sensor-oriented applications, with additional records related to biomedical interfaces, energy devices, actuators, environmental materials, and coatings. Because some records use multi-functional materials and multi-label applications, application categories should be interpreted as visibility patterns rather than mutually exclusive classes.

### 3.2 Wide-temperature claims are common, but temperature conditions are less consistently visible

In the D2 primary analysis set, 130 of 156 records claimed wide-temperature or anti-freezing behavior, corresponding to 83.3%. However, only 55 records, or 35.3%, visibly reported a specific temperature value at the record level. Only 39 records, or 25.0%, visibly reported a subzero temperature condition.

This gap suggests that wide-temperature claims are much more visible than the specific conditions under which these claims are tested. For a functional material, this distinction matters because a broad claimed temperature window does not necessarily imply that conductivity, sensing, self-healing, adhesion, or device operation was retained under that temperature.

### 3.3 Functional metrics are less visible than function labels

Conductivity was mentioned in 75 of 156 cellulose-relevant records, but a numerical conductivity value was visible in only 22 records, or 14.1%. Gauge factor or strain sensitivity was mentioned in 53 records, but a numerical GF value was visible in only 10 records, or 6.4%. Self-healing was mentioned in 35 records, with a numerical value visible in 15 records, or 9.6%. Adhesion was mentioned in 30 records, but only 4 records, or 2.6%, visibly reported an adhesion value.

These results indicate a consistent drop from functional vocabulary to quantitative functional evidence. At the abstract or record level, the field often foregrounds desirable functions, but less consistently reports the numerical evidence needed to compare functional retention across temperature conditions.

### 3.4 Non-mechanical functional evidence is especially sparse

Only 39 of 156 cellulose-relevant records, or 25.0%, visibly reported at least one non-mechanical functional metric. When mechanical values were included, 69 records, or 44.2%, reported at least one quantitative performance metric.

This difference matters because many gels can retain shape or mechanical flexibility while still losing the function that makes them useful as sensors, electrodes, adhesives, actuators, or biomedical interfaces. Therefore, anti-freezing evaluation should not stop at structural survival.

### 3.5 Cellulose identity is often under-specified

The primary analysis set includes multiple cellulose forms, including regenerated cellulose, CMC, CNC, bacterial cellulose, CNF, and modified cellulose. However, a large fraction of records were coded as `Unspecified`, meaning that the abstract or local record did not make the cellulose identity sufficiently explicit for detailed mechanism-level comparison.

This ambiguity weakens attempts to infer whether cellulose acts as a water-state regulator, mechanical scaffold, conductive/ionic environment modifier, interface mediator, or sustainability label. A stronger reporting standard should therefore describe not only the presence of cellulose, but also its form, modification, network role, and relationship to the cryoprotective strategy.

### 3.6 Full-text exemplars support the need for an evidence ladder

The first core exemplar pass identified a wide spread of evidence levels. Some records visibly report low-temperature conductivity or mechanical performance, such as cellulose/PAA hydrogels with conductivity at `-45 °C` and zwitterionic CNF hydrogels with toughness, self-healing, and conductivity at `-40 °C`. Other records approach operational validation, including CNC@PANI hydrogel sensors tested across `-60 to 80 °C` with long-cycle motion monitoring, and CMC/PAA/Fe3+/LiCl hydrogels used in low-temperature supercapacitors.

At the same time, some promising eutectogel records show strong materials properties but require full-text confirmation before they can be classified as in-situ low-temperature functional evidence. This supports the use of an E0-E4 evidence ladder rather than a binary anti-freezing label.

## Result Takeaway

The main result is not that the field lacks functional data in every full text. The defensible claim is narrower and stronger: at the record and abstract level, wide-temperature claims are much more visible than verified functional-retention metrics. This is why the manuscript should propose a reporting framework rather than present itself as a comprehensive performance meta-analysis.
