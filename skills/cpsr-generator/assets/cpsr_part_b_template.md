# COSMETIC PRODUCT SAFETY REPORT (CPSR)
## PART B - Safety Assessment

---

**Document Control**

| Field | Value |
|-------|-------|
| Document ID | CPSR-{{product_code}}-{{version}} |
| Version | {{version}} |
| Date | {{date}} |
| Product Name | {{product_name}} |
| Safety Assessor | {{safety_assessor_name}} |
| Qualification | {{safety_assessor_qualification}} |
| CPSR Part A Reference | {{part_a_reference}} |

---

## Table of Contents

1. [Assessment Conclusion](#1-assessment-conclusion)
2. [Review of Part A Information](#2-review-of-part-a-information)
3. [Labelled Warnings and Instructions](#3-labelled-warnings-and-instructions)
4. [Reasoning](#4-reasoning)
5. [Assessor's Credentials](#5-assessors-credentials)

---

## 1. Assessment Conclusion

### 1.1 Safety Statement

Based on the comprehensive review of the safety information provided in Part A of this Cosmetic Product Safety Report, I conclude that:

{{#if safe}}
**The cosmetic product "{{product_name}}" is SAFE for human health when used under normal or reasonably foreseeable conditions of use, taking into account:**
- The presentation of the product
- The labelling provided
- The instructions for use and disposal
- Any other indication or information provided

{{else}}
**The cosmetic product "{{product_name}}" cannot be considered SAFE for human health under the current formulation/conditions because:**
{{unsafe_reasons}}

**Recommendations for achieving safety:**
{{recommendations}}
{{/if}}

### 1.2 Summary of Safety Evaluation

| Parameter | Assessment | Status |
|-----------|------------|--------|
| Product Category | {{product_category}} | - |
| Intended Use | {{intended_use}} | ✓ Verified |
| Target Population | {{target_population}} | ✓ Appropriate |
| Exposure Assessment | {{exposure_assessment}} | ✓ Complete |
| Toxicological Evaluation | {{tox_evaluation}} | {{tox_status}} |
| Microbiological Quality | {{micro_quality}} | {{micro_status}} |
| Stability | {{stability_status}} | {{stability_result}} |
| Overall Safety | {{overall_safety}} | {{overall_status}} |

---

## 2. Review of Part A Information

### 2.1 Quantitative and Qualitative Composition

**Assessment**:
{{composition_assessment}}

**Key Observations**:
{{#each composition_observations}}
- {{this}}
{{/each}}

**Conclusion**: {{composition_conclusion}}

### 2.2 Physical/Chemical Characteristics and Stability

**Assessment**:
{{stability_assessment}}

| Parameter | Part A Data | Assessor's Evaluation |
|-----------|-------------|----------------------|
| Appearance | {{appearance}} | {{appearance_eval}} |
| pH | {{ph_value}} | {{ph_eval}} |
| Viscosity | {{viscosity}} | {{viscosity_eval}} |
| Stability Duration | {{stability_duration}} | {{stability_eval}} |
| PAO | {{pao}} months | {{pao_eval}} |

**Conclusion**: {{stability_conclusion}}

### 2.3 Microbiological Quality

**Assessment**:
{{micro_assessment}}

| Test | Result | Specification | Evaluation |
|------|--------|---------------|------------|
| Total Aerobic Count | {{tac_result}} | < {{tac_spec}} CFU/g | {{tac_eval}} |
| Yeast & Mould | {{ym_result}} | < {{ym_spec}} CFU/g | {{ym_eval}} |
| Pathogens | {{pathogen_result}} | Absent | {{pathogen_eval}} |
| Challenge Test | {{pet_result}} | Criterion A | {{pet_eval}} |

**Conclusion**: {{micro_conclusion}}

### 2.4 Impurities, Traces, and Packaging

**Assessment**:
{{impurities_assessment}}

**Heavy Metals Evaluation**:
| Metal | Result | Limit | Margin | Evaluation |
|-------|--------|-------|--------|------------|
| Lead (Pb) | {{pb_result}} ppm | {{pb_limit}} ppm | {{pb_margin}}x | {{pb_eval}} |
| Arsenic (As) | {{as_result}} ppm | {{as_limit}} ppm | {{as_margin}}x | {{as_eval}} |
| Mercury (Hg) | {{hg_result}} ppm | {{hg_limit}} ppm | {{hg_margin}}x | {{hg_eval}} |
| Cadmium (Cd) | {{cd_result}} ppm | {{cd_limit}} ppm | {{cd_margin}}x | {{cd_eval}} |

**Packaging Compatibility**: {{packaging_eval}}

**Conclusion**: {{impurities_conclusion}}

### 2.5 Normal and Reasonably Foreseeable Use

**Assessment**:
{{use_assessment}}

**Use Conditions Evaluated**:
- Normal use: {{normal_use_eval}}
- Reasonably foreseeable misuse: {{misuse_eval}}
- Vulnerable populations: {{vulnerable_eval}}

**Conclusion**: {{use_conclusion}}

### 2.6 Exposure Assessment

**Assessment**:
{{exposure_assessment_detail}}

**Exposure Parameters Used**:
| Parameter | Value | Source | Appropriateness |
|-----------|-------|--------|-----------------|
| Amount Applied | {{amount}} mg/day | {{amount_source}} | {{amount_eval}} |
| Frequency | {{frequency}}/day | {{freq_source}} | {{freq_eval}} |
| Retention Factor | {{retention}} | {{retention_source}} | {{retention_eval}} |
| Body Weight | {{body_weight}} kg | {{bw_source}} | {{bw_eval}} |

**Conclusion**: {{exposure_conclusion}}

### 2.7 Toxicological Profile Assessment

**Overall Toxicological Evaluation**:
{{tox_overall_assessment}}

#### 2.7.1 Margin of Safety Summary

| Ingredient | Concentration | SED | NOAEL | MoS | Assessor's Evaluation |
|------------|---------------|-----|-------|-----|----------------------|
{{#each mos_summary}}
| {{ingredient}} | {{concentration}}% | {{sed}} mg/kg/day | {{noael}} mg/kg/day | {{mos}} | {{evaluation}} |
{{/each}}

**MoS Interpretation**:
- All ingredients with MoS ≥ 100: {{mos_pass_comment}}
- Ingredients with MoS 50-100: {{mos_review_comment}}
- Ingredients with MoS < 50: {{mos_fail_comment}}

#### 2.7.2 Specific Toxicological Considerations

**Skin Irritation/Corrosion**:
{{skin_irritation_assessment}}

**Eye Irritation**:
{{eye_irritation_assessment}}

**Skin Sensitization**:
{{sensitization_assessment}}

**Phototoxicity/Photoallergenicity**:
{{phototoxicity_assessment}}

**Systemic Toxicity**:
{{systemic_toxicity_assessment}}

**Genotoxicity/Carcinogenicity**:
{{genotox_assessment}}

**Reproductive Toxicity**:
{{repro_tox_assessment}}

#### 2.7.3 Special Substance Considerations

{{#each special_substances}}
**{{name}}**:
- Concern: {{concern}}
- Concentration: {{concentration}}%
- Regulatory Status: {{regulatory_status}}
- Risk Assessment: {{risk_assessment}}
- Conclusion: {{conclusion}}

{{/each}}

### 2.8 Undesirable Effects

**Review of Available Data**:
{{undesirable_effects_review}}

**Clinical Test Results**:
| Test | N | Result | Interpretation |
|------|---|--------|----------------|
| Patch Test | {{patch_n}} | {{patch_result}} | {{patch_interp}} |
| HRIPT | {{hript_n}} | {{hript_result}} | {{hript_interp}} |
| Use Test | {{use_n}} | {{use_result}} | {{use_interp}} |

**Post-Market Data (if available)**:
{{post_market_data}}

**Conclusion**: {{undesirable_effects_conclusion}}

---

## 3. Labelled Warnings and Instructions

### 3.1 Mandatory Labelling Review

| Requirement | Present | Adequate | Notes |
|-------------|---------|----------|-------|
| Product Name | {{name_present}} | {{name_adequate}} | |
| INCI List | {{inci_present}} | {{inci_adequate}} | |
| Net Content | {{content_present}} | {{content_adequate}} | |
| PAO/Durability | {{pao_present}} | {{pao_adequate}} | |
| Batch Code | {{batch_present}} | {{batch_adequate}} | |
| Country of Origin | {{origin_present}} | {{origin_adequate}} | |
| Responsible Person | {{rp_present}} | {{rp_adequate}} | |
| Function | {{function_present}} | {{function_adequate}} | |
| Precautions | {{precautions_present}} | {{precautions_adequate}} | {{precautions_notes}} |

### 3.2 Required Warnings

Based on the formulation assessment, the following warnings are **REQUIRED**:

{{#each required_warnings}}
**{{category}}**:
- Warning: "{{warning_text}}"
- Basis: {{basis}}
- Regulatory Reference: {{reference}}

{{/each}}

### 3.3 Recommended Warnings

The following additional warnings are **RECOMMENDED** for consumer safety:

{{#each recommended_warnings}}
- "{{warning_text}}" - Reason: {{reason}}
{{/each}}

### 3.4 Instructions for Use

**Current Instructions**: {{current_instructions}}

**Assessment**: {{instructions_assessment}}

**Recommended Additions/Modifications**:
{{#each instruction_recommendations}}
- {{this}}
{{/each}}

---

## 4. Reasoning

### 4.1 Overall Safety Reasoning

{{overall_reasoning}}

### 4.2 Key Safety Factors

**Factors Supporting Safety**:
{{#each safety_factors_positive}}
1. {{this}}
{{/each}}

**Factors Requiring Attention**:
{{#each safety_factors_attention}}
1. {{this}}
{{/each}}

**Mitigating Measures Applied**:
{{#each mitigating_measures}}
1. {{this}}
{{/each}}

### 4.3 Vulnerable Populations

#### 4.3.1 Children (Under 3 Years)

**Applicability**: {{children_applicable}}

{{#if children_applicable}}
**Assessment**:
{{children_assessment}}

**Specific Considerations**:
{{#each children_considerations}}
- {{this}}
{{/each}}

**Conclusion**: {{children_conclusion}}
{{else}}
Product is not intended for use by children under 3 years of age.
{{/if}}

#### 4.3.2 Pregnant/Nursing Women

**Assessment**:
{{pregnancy_assessment}}

**Ingredients of Concern**:
{{#each pregnancy_concerns}}
- {{ingredient}}: {{concern}}
{{/each}}

**Conclusion**: {{pregnancy_conclusion}}

#### 4.3.3 Sensitive Skin/Allergy-Prone Individuals

**Assessment**:
{{sensitive_skin_assessment}}

**Potential Sensitizers Present**:
{{#each sensitizers}}
- {{ingredient}} ({{concentration}}%): {{risk_level}}
{{/each}}

**Conclusion**: {{sensitive_conclusion}}

### 4.4 Cumulative/Aggregate Exposure

**Assessment**:
{{cumulative_assessment}}

**Consideration of Combined Use**:
{{combined_use_consideration}}

**Conclusion**: {{cumulative_conclusion}}

### 4.5 Specific Exposure Routes

#### Dermal Exposure
{{dermal_reasoning}}

#### Oral Exposure (if applicable)
{{oral_reasoning}}

#### Inhalation Exposure (if applicable)
{{inhalation_reasoning}}

#### Ocular Exposure (if applicable)
{{ocular_reasoning}}

### 4.6 Regulatory Compliance

| Regulation | Compliance Status | Notes |
|------------|-------------------|-------|
| EU 1223/2009 | {{eu_compliance}} | {{eu_notes}} |
| Annex II (Prohibited) | {{annex_ii_status}} | {{annex_ii_notes}} |
| Annex III (Restricted) | {{annex_iii_status}} | {{annex_iii_notes}} |
| Annex IV (Colorants) | {{annex_iv_status}} | {{annex_iv_notes}} |
| Annex V (Preservatives) | {{annex_v_status}} | {{annex_v_notes}} |
| Annex VI (UV Filters) | {{annex_vi_status}} | {{annex_vi_notes}} |
| CMR Substances | {{cmr_status}} | {{cmr_notes}} |
| Nanomaterials | {{nano_status}} | {{nano_notes}} |

---

## 5. Assessor's Credentials

### 5.1 Safety Assessor Information

| Field | Information |
|-------|-------------|
| Name | {{assessor_name}} |
| Title/Position | {{assessor_title}} |
| Organization | {{assessor_organization}} |
| Address | {{assessor_address}} |
| Contact | {{assessor_contact}} |

### 5.2 Qualifications

**Educational Background**:
{{assessor_education}}

**Relevant Training**:
{{#each assessor_training}}
- {{this}}
{{/each}}

**Compliance with Article 10(2) of Regulation 1223/2009**:
The Safety Assessor holds a diploma or other evidence of formal qualifications awarded on completion of a university course of theoretical and practical study in:
- [ ] Pharmacy
- [ ] Toxicology
- [ ] Medicine
- [ ] Similar discipline
- [ ] Course recognized as equivalent by a Member State

### 5.3 Declaration of Independence

I, {{assessor_name}}, hereby declare that:

1. I have conducted this safety assessment independently and objectively.
2. I have no financial or other conflicts of interest that could affect the objectivity of this assessment.
3. All information provided in this report is accurate and complete to the best of my knowledge.
4. I am appropriately qualified under Article 10(2) of Regulation (EC) No 1223/2009 to perform this safety assessment.

---

## Final Safety Conclusion

### Summary Statement

{{final_summary}}

### Conditions for Safe Use

The product "{{product_name}}" is considered safe for human health under the following conditions:

1. **Application Method**: {{application_method}}
2. **Frequency of Use**: {{frequency_of_use}}
3. **Target Area**: {{target_area}}
4. **Target Population**: {{target_population}}
5. **Required Warnings**: As specified in Section 3.2

### Limitations

{{#each limitations}}
- {{this}}
{{/each}}

### Recommendations for Responsible Person

{{#each rp_recommendations}}
{{@index}}. {{this}}
{{/each}}

---

## Signatures

**Safety Assessor**:

Name: {{assessor_name}}

Signature: ________________________

Date: {{assessment_date}}

---

**Document Control**:
- Version {{version}}
- This document is controlled. Printed copies are uncontrolled.
- This assessment is valid for the specific formulation assessed.
- Any changes to the formulation require re-assessment.

---

## Appendix: Assessment Checklist

| Item | Verified | Notes |
|------|----------|-------|
| Part A complete and accurate | {{checklist_part_a}} | |
| All ingredients assessed | {{checklist_ingredients}} | |
| Exposure parameters appropriate | {{checklist_exposure}} | |
| MoS calculations correct | {{checklist_mos}} | |
| Stability data adequate | {{checklist_stability}} | |
| Microbiological data adequate | {{checklist_micro}} | |
| Clinical data reviewed | {{checklist_clinical}} | |
| Labelling requirements met | {{checklist_labelling}} | |
| Regulatory compliance verified | {{checklist_regulatory}} | |
| Vulnerable populations considered | {{checklist_vulnerable}} | |

---

*This Cosmetic Product Safety Report Part B has been prepared in accordance with Regulation (EC) No 1223/2009 on cosmetic products, Annex I, Part B.*
