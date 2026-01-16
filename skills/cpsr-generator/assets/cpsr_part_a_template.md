# COSMETIC PRODUCT SAFETY REPORT (CPSR)
## PART A - Safety Information

---

**Document Control**

| Field | Value |
|-------|-------|
| Document ID | CPSR-{{product_code}}-{{version}} |
| Version | {{version}} |
| Date | {{date}} |
| Product Name | {{product_name}} |
| Responsible Person | {{responsible_person}} |
| Prepared by | {{preparer}} |
| Reviewed by | {{reviewer}} |

---

## Table of Contents

1. [Quantitative and Qualitative Composition](#1-quantitative-and-qualitative-composition)
2. [Physical/Chemical Characteristics and Stability](#2-physicalchemical-characteristics-and-stability)
3. [Microbiological Quality](#3-microbiological-quality)
4. [Impurities, Traces, and Packaging Material Information](#4-impurities-traces-and-packaging-material-information)
5. [Normal and Reasonably Foreseeable Use](#5-normal-and-reasonably-foreseeable-use)
6. [Exposure to the Cosmetic Product](#6-exposure-to-the-cosmetic-product)
7. [Exposure to the Substances](#7-exposure-to-the-substances)
8. [Toxicological Profile of Substances](#8-toxicological-profile-of-substances)
9. [Undesirable Effects and Serious Undesirable Effects](#9-undesirable-effects-and-serious-undesirable-effects)
10. [Information on the Cosmetic Product](#10-information-on-the-cosmetic-product)

---

## 1. Quantitative and Qualitative Composition

### 1.1 Complete Formula

| No. | INCI Name | CAS No. | EC No. | Function | Concentration (%) |
|-----|-----------|---------|--------|----------|-------------------|
{{#each ingredients}}
| {{@index}} | {{inci_name}} | {{cas_number}} | {{ec_number}} | {{function}} | {{concentration}} |
{{/each}}

**Total**: 100.00%

### 1.2 Raw Material Specifications

{{#each ingredients}}
#### {{inci_name}}

| Parameter | Value |
|-----------|-------|
| INCI Name | {{inci_name}} |
| CAS Number | {{cas_number}} |
| EC Number | {{ec_number}} |
| Chemical/Common Name | {{common_name}} |
| Supplier | {{supplier}} |
| Lot/Batch Number | {{batch_number}} |
| Purity | {{purity}}% |
| Function in Formula | {{function}} |
| Concentration | {{concentration}}% |

{{/each}}

---

## 2. Physical/Chemical Characteristics and Stability

### 2.1 Physical/Chemical Properties of the Finished Product

| Parameter | Specification | Test Method |
|-----------|---------------|-------------|
| Appearance | {{appearance}} | Visual inspection |
| Color | {{color}} | Visual inspection |
| Odor | {{odor}} | Organoleptic |
| pH ({{ph_dilution}}) | {{ph_min}} - {{ph_max}} | Ph. Eur. 2.2.3 |
| Viscosity ({{viscosity_temp}}°C) | {{viscosity_min}} - {{viscosity_max}} {{viscosity_unit}} | {{viscosity_method}} |
| Specific Gravity | {{specific_gravity_min}} - {{specific_gravity_max}} | Ph. Eur. 2.2.5 |
| Relative Density (20°C) | {{relative_density}} | Pycnometer |

### 2.2 Stability Testing

#### 2.2.1 Study Design

| Parameter | Condition |
|-----------|-----------|
| Study Type | {{stability_type}} |
| Duration | {{stability_duration}} |
| Test Conditions | {{stability_conditions}} |
| Container/Closure | {{container_closure}} |

#### 2.2.2 Stability Conditions

| Condition | Temperature | Humidity | Duration | Light Exposure |
|-----------|-------------|----------|----------|----------------|
| Long-term | 25°C ± 2°C | 60% ± 5% RH | {{longterm_duration}} months | Protected |
| Accelerated | 40°C ± 2°C | 75% ± 5% RH | {{accelerated_duration}} months | Protected |
| Intermediate | 30°C ± 2°C | 65% ± 5% RH | {{intermediate_duration}} months | Protected |
| Light | 25°C ± 2°C | - | {{photostability_duration}} months | ICH Q1B |
| Freeze-Thaw | -10°C to 40°C | - | {{freezethaw_cycles}} cycles | Protected |

#### 2.2.3 Stability Results Summary

| Test Point | Appearance | Color | Odor | pH | Viscosity | Microbial | Status |
|------------|------------|-------|------|-----|-----------|-----------|--------|
| Initial | {{initial_appearance}} | {{initial_color}} | {{initial_odor}} | {{initial_ph}} | {{initial_viscosity}} | Pass | ✓ |
| 1 Month | {{m1_appearance}} | {{m1_color}} | {{m1_odor}} | {{m1_ph}} | {{m1_viscosity}} | Pass | ✓ |
| 3 Months | {{m3_appearance}} | {{m3_color}} | {{m3_odor}} | {{m3_ph}} | {{m3_viscosity}} | Pass | ✓ |
| 6 Months | {{m6_appearance}} | {{m6_color}} | {{m6_odor}} | {{m6_ph}} | {{m6_viscosity}} | Pass | ✓ |
| 12 Months | {{m12_appearance}} | {{m12_color}} | {{m12_odor}} | {{m12_ph}} | {{m12_viscosity}} | Pass | ✓ |

**Conclusion**: {{stability_conclusion}}

**Period After Opening (PAO)**: {{pao}} months

**Shelf Life**: {{shelf_life}} months from date of manufacture

---

## 3. Microbiological Quality

### 3.1 Microbiological Specifications

| Test | Specification | Method |
|------|---------------|--------|
| Total Aerobic Mesophilic Count | < {{tamc_limit}} CFU/g | ISO 21149 |
| Yeasts and Moulds | < {{ym_limit}} CFU/g | ISO 16212 |
| Escherichia coli | Absent in 1g | ISO 21150 |
| Pseudomonas aeruginosa | Absent in 1g | ISO 22717 |
| Staphylococcus aureus | Absent in 1g | ISO 22718 |
| Candida albicans | Absent in 1g | ISO 18416 |

### 3.2 Preservative Efficacy Test (Challenge Test)

**Test Method**: ISO 11930:2019 - Evaluation of the antimicrobial protection of a cosmetic product

| Organism | Inoculum (CFU/g) | Day 7 | Day 14 | Day 28 | Criterion A | Result |
|----------|------------------|-------|--------|--------|-------------|--------|
| Pseudomonas aeruginosa | {{ps_inoculum}} | {{ps_d7}} | {{ps_d14}} | {{ps_d28}} | ≥3 log ↓ (D7), NI (D28) | {{ps_result}} |
| Staphylococcus aureus | {{sa_inoculum}} | {{sa_d7}} | {{sa_d14}} | {{sa_d28}} | ≥3 log ↓ (D7), NI (D28) | {{sa_result}} |
| Escherichia coli | {{ec_inoculum}} | {{ec_d7}} | {{ec_d14}} | {{ec_d28}} | ≥3 log ↓ (D7), NI (D28) | {{ec_result}} |
| Candida albicans | {{ca_inoculum}} | {{ca_d7}} | {{ca_d14}} | {{ca_d28}} | ≥1 log ↓ (D14), NI (D28) | {{ca_result}} |
| Aspergillus brasiliensis | {{ab_inoculum}} | {{ab_d7}} | {{ab_d14}} | {{ab_d28}} | ≥1 log ↓ (D14), NI (D28) | {{ab_result}} |

**Conclusion**: {{pet_conclusion}}

NI = No increase; log ↓ = log reduction

---

## 4. Impurities, Traces, and Packaging Material Information

### 4.1 Potential Impurities

| Impurity | Source | Limit | Actual | Method | Compliant |
|----------|--------|-------|--------|--------|-----------|
| Heavy Metals (total) | Raw materials | {{hm_limit}} ppm | {{hm_actual}} ppm | ICP-MS | {{hm_compliant}} |
| Lead (Pb) | Raw materials | {{pb_limit}} ppm | {{pb_actual}} ppm | ICP-MS | {{pb_compliant}} |
| Arsenic (As) | Raw materials | {{as_limit}} ppm | {{as_actual}} ppm | ICP-MS | {{as_compliant}} |
| Mercury (Hg) | Raw materials | {{hg_limit}} ppm | {{hg_actual}} ppm | ICP-MS | {{hg_compliant}} |
| Cadmium (Cd) | Raw materials | {{cd_limit}} ppm | {{cd_actual}} ppm | ICP-MS | {{cd_compliant}} |
| Nickel (Ni) | Raw materials | {{ni_limit}} ppm | {{ni_actual}} ppm | ICP-MS | {{ni_compliant}} |

### 4.2 Traces from Manufacturing Process

| Substance | Source | Limit | Status |
|-----------|--------|-------|--------|
{{#each process_traces}}
| {{substance}} | {{source}} | {{limit}} | {{status}} |
{{/each}}

### 4.3 Packaging Material Information

#### 4.3.1 Primary Packaging

| Component | Material | Food Grade | Migration Testing | Compatibility |
|-----------|----------|------------|-------------------|---------------|
| {{primary_component}} | {{primary_material}} | {{primary_food_grade}} | {{primary_migration}} | {{primary_compatibility}} |

#### 4.3.2 Packaging Compatibility

| Test | Method | Result |
|------|--------|--------|
| Compatibility at 25°C | 12 months storage | {{compat_25c}} |
| Compatibility at 40°C | 6 months accelerated | {{compat_40c}} |
| Light protection | ICH Q1B photostability | {{light_protection}} |
| Migration testing | EU 10/2011 limits | {{migration_test}} |

---

## 5. Normal and Reasonably Foreseeable Use

### 5.1 Product Category

| Classification | Value |
|---------------|-------|
| Product Category | {{product_category}} |
| EU Cosmetics Regulation Article | {{eu_article}} |
| CosIng Category | {{cosing_category}} |
| Application Area | {{application_area}} |
| User Group | {{user_group}} |

### 5.2 Intended Use

{{intended_use_description}}

### 5.3 Application Instructions

1. {{instruction_1}}
2. {{instruction_2}}
3. {{instruction_3}}
{{#if instruction_4}}
4. {{instruction_4}}
{{/if}}
{{#if instruction_5}}
5. {{instruction_5}}
{{/if}}

### 5.4 Warnings and Precautions

{{#each warnings}}
- {{this}}
{{/each}}

### 5.5 Reasonably Foreseeable Misuse

| Misuse Scenario | Risk | Mitigation |
|-----------------|------|------------|
{{#each misuse_scenarios}}
| {{scenario}} | {{risk}} | {{mitigation}} |
{{/each}}

---

## 6. Exposure to the Cosmetic Product

### 6.1 Exposure Parameters (SCCS Notes of Guidance, 11th Revision)

| Parameter | Value | Reference |
|-----------|-------|-----------|
| Product Type | {{product_type}} |  SCCS/1628/21 |
| Amount Applied (A) | {{amount_applied}} mg/day | SCCS Table 1 |
| Application Frequency (F) | {{frequency}} per day | SCCS Table 1 |
| Retention Factor (RF) | {{retention_factor}} | SCCS Table 1 |
| Skin Surface Area (SSA) | {{skin_surface_area}} cm² | SCCS Table 2 |
| Body Weight (BW) | {{body_weight}} kg | Default |

### 6.2 Daily Exposure Calculation

**Daily Exposure = A × F × RF**

Daily Exposure = {{amount_applied}} mg × {{frequency}} × {{retention_factor}}

**Daily Exposure = {{daily_exposure}} mg/day**

### 6.3 Exposure Route

| Route | Applicable | Notes |
|-------|------------|-------|
| Dermal | {{dermal_exposure}} | Primary route |
| Oral | {{oral_exposure}} | {{oral_notes}} |
| Inhalation | {{inhalation_exposure}} | {{inhalation_notes}} |
| Ocular | {{ocular_exposure}} | {{ocular_notes}} |

---

## 7. Exposure to the Substances

### 7.1 Systemic Exposure Dose (SED) Calculations

**SED Formula**:
```
SED (mg/kg bw/day) = (A × C/100 × DA/100 × F × RF) / BW
```

Where:
- A = Amount of product applied (mg/day)
- C = Concentration of substance in product (%)
- DA = Dermal absorption (%)
- F = Frequency of application (per day)
- RF = Retention factor
- BW = Body weight (kg)

### 7.2 SED Results for Key Substances

| Ingredient | Conc. (%) | Dermal Abs. (%) | SED (mg/kg/day) | Source |
|------------|-----------|-----------------|-----------------|--------|
{{#each sed_results}}
| {{inci_name}} | {{concentration}} | {{dermal_absorption}} | {{sed}} | {{source}} |
{{/each}}

### 7.3 Dermal Absorption Data Sources

| Ingredient | Absorption (%) | Data Source | Study Type |
|------------|----------------|-------------|------------|
{{#each dermal_absorption_data}}
| {{inci_name}} | {{absorption}} | {{source}} | {{study_type}} |
{{/each}}

---

## 8. Toxicological Profile of Substances

### 8.1 Margin of Safety (MoS) Calculations

**MoS Formula**:
```
MoS = NOAEL / SED
```

**Acceptable MoS**: ≥ 100 (includes uncertainty factors for inter- and intra-species variability)

### 8.2 MoS Summary Table

| Ingredient | SED (mg/kg/day) | NOAEL (mg/kg/day) | MoS | Status |
|------------|-----------------|-------------------|-----|--------|
{{#each mos_results}}
| {{inci_name}} | {{sed}} | {{noael}} | {{mos}} | {{status}} |
{{/each}}

### 8.3 Detailed Toxicological Profiles

{{#each toxicological_profiles}}

#### {{inci_name}}

| Endpoint | Value | Study | Source |
|----------|-------|-------|--------|
| Acute Oral Toxicity | LD50 > {{oral_ld50}} mg/kg | {{oral_study}} | {{oral_source}} |
| Acute Dermal Toxicity | LD50 > {{dermal_ld50}} mg/kg | {{dermal_study}} | {{dermal_source}} |
| Skin Irritation | {{skin_irritation}} | {{irritation_study}} | {{irritation_source}} |
| Eye Irritation | {{eye_irritation}} | {{eye_study}} | {{eye_source}} |
| Skin Sensitization | {{sensitization}} | {{sensitization_study}} | {{sensitization_source}} |
| Repeated Dose Toxicity | NOAEL {{noael}} mg/kg/day | {{rdt_study}} | {{rdt_source}} |
| Mutagenicity/Genotoxicity | {{mutagenicity}} | {{mutagen_study}} | {{mutagen_source}} |
| Carcinogenicity | {{carcinogenicity}} | {{carcino_study}} | {{carcino_source}} |
| Reproductive Toxicity | {{repro_tox}} | {{repro_study}} | {{repro_source}} |
| Phototoxicity | {{phototoxicity}} | {{photo_study}} | {{photo_source}} |

**Conclusion for {{inci_name}}**: {{conclusion}}

{{/each}}

### 8.4 Substances with Special Considerations

{{#each special_considerations}}

#### {{inci_name}}

**Concern**: {{concern}}

**Regulatory Status**: {{regulatory_status}}

**Risk Assessment**: {{risk_assessment}}

**Conclusion**: {{conclusion}}

{{/each}}

---

## 9. Undesirable Effects and Serious Undesirable Effects

### 9.1 Potential Undesirable Effects

| Effect | Substance(s) | Likelihood | Severity | Mitigation |
|--------|--------------|------------|----------|------------|
{{#each potential_effects}}
| {{effect}} | {{substances}} | {{likelihood}} | {{severity}} | {{mitigation}} |
{{/each}}

### 9.2 Post-Market Surveillance Data

| Parameter | Status |
|-----------|--------|
| Complaints received | {{complaints_count}} |
| Serious undesirable effects reported | {{sue_count}} |
| Regulatory notifications filed | {{regulatory_notifications}} |
| Market recalls | {{recalls}} |

### 9.3 Clinical Testing Summary

| Test | Subjects | Result | Conclusion |
|------|----------|--------|------------|
| Patch Test (48h occlusive) | {{patch_subjects}} | {{patch_result}} | {{patch_conclusion}} |
| RIPT (HRIPT) | {{ript_subjects}} | {{ript_result}} | {{ript_conclusion}} |
| Use Test | {{use_subjects}} | {{use_result}} | {{use_conclusion}} |

---

## 10. Information on the Cosmetic Product

### 10.1 Product Identification

| Field | Value |
|-------|-------|
| Product Name | {{product_name}} |
| Trade Name(s) | {{trade_names}} |
| Product Code | {{product_code}} |
| Barcode/EAN | {{barcode}} |
| Net Content | {{net_content}} |
| Product Type | {{product_type}} |

### 10.2 Manufacturing Information

| Field | Value |
|-------|-------|
| Manufacturing Site | {{manufacturing_site}} |
| Site Address | {{site_address}} |
| GMP Certification | {{gmp_certification}} |
| ISO Certification | {{iso_certification}} |

### 10.3 Labelling Information

**Product Label Text**:

```
{{label_text}}
```

**Ingredients (INCI)**:
{{inci_list}}

### 10.4 Regulatory Compliance Summary

| Requirement | Status | Notes |
|-------------|--------|-------|
| EU Cosmetics Regulation 1223/2009 | {{eu_compliance}} | |
| Annex II (Prohibited) | {{annex_ii}} | |
| Annex III (Restricted) | {{annex_iii}} | {{annex_iii_notes}} |
| Annex IV (Colorants) | {{annex_iv}} | {{annex_iv_notes}} |
| Annex V (Preservatives) | {{annex_v}} | {{annex_v_notes}} |
| Annex VI (UV Filters) | {{annex_vi}} | {{annex_vi_notes}} |
| CMR substances (Art. 15) | {{cmr_compliance}} | |
| Nanomaterials (Art. 16) | {{nano_compliance}} | {{nano_notes}} |

---

## Appendices

### Appendix A: Raw Material Specifications (CoA)
{{#each ingredients}}
- {{inci_name}}: See attached CoA-{{@index}}
{{/each}}

### Appendix B: Stability Study Reports
- Long-term stability report: {{stability_report_longterm}}
- Accelerated stability report: {{stability_report_accelerated}}
- Photostability report: {{stability_report_photo}}

### Appendix C: Microbiological Test Reports
- Microbiological quality test: {{micro_report}}
- Challenge test report: {{challenge_report}}

### Appendix D: Toxicological Data Summaries
{{#each toxicological_profiles}}
- {{inci_name}}: {{tox_summary_ref}}
{{/each}}

### Appendix E: Clinical Test Reports
- Patch test report: {{patch_report}}
- RIPT report: {{ript_report}}
- Use test report: {{use_report}}

### Appendix F: Packaging Specifications
- Primary packaging specification: {{packaging_spec_primary}}
- Compatibility test report: {{compatibility_report}}

---

## Declaration

This Cosmetic Product Safety Report Part A has been prepared in accordance with Regulation (EC) No 1223/2009 on cosmetic products, Annex I, Part A.

All information provided is accurate and complete to the best of our knowledge. The data and conclusions presented are based on the most current information available at the time of assessment.

**Prepared by**: {{preparer}}

**Date**: {{preparation_date}}

**Signature**: ________________________

---

**Document Control**:
- Version {{version}}
- This document is controlled. Printed copies are uncontrolled.
- Review scheduled: {{next_review_date}}
