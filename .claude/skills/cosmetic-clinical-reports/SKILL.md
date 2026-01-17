---
name: cosmetic-clinical-reports
description: Write comprehensive cosmetic clinical reports including Human Application Tests (피부 자극/감작/광독성), Efficacy Clinical Trials (미백/주름개선/보습), Consumer Use Tests, Dermatologist Tests, Patch Tests, and SPF/PA measurements. Full support with templates, regulatory compliance (MFDS, EU CPR, FDA, NMPA), and validation tools for functional cosmetics (기능성화장품) approval.
allowed-tools: [Read, Write, Edit, Bash]
license: MIT License
metadata:
    skill-author: EVAS Cosmetic
    based-on: K-Dense Inc. clinical-reports skill
---

# Cosmetic Clinical Report Writing

## Overview

Cosmetic clinical report writing is the process of documenting safety and efficacy data for cosmetic products with precision, accuracy, and compliance with regulatory standards. This skill covers six major categories of cosmetic clinical reports: Human Application Tests (인체적용시험), Efficacy Clinical Trials (효능임상시험), Consumer Use Tests, Dermatologist Tests, Patch Tests, and Sunscreen Testing (SPF/PA). Apply this skill for functional cosmetics (기능성화장품) approval, marketing claim substantiation, and regulatory compliance.

**Critical Principle: Cosmetic clinical reports must be accurate, complete, objective, and compliant with applicable regulations (MFDS, EU CPR 1223/2009, FDA OTC Monograph, NMPA).** Subject privacy and data integrity are paramount. All clinical documentation must support evidence-based claims and meet professional standards.

## When to Use This Skill

This skill should be used when:
- Writing Human Application Test reports for safety assessment (피부 자극, 감작, 광독성)
- Documenting efficacy clinical trials for functional cosmetics (미백, 주름개선, 보습)
- Creating Consumer Use Test (CUT) reports for sensory and satisfaction claims
- Preparing Dermatologist Tested claims documentation
- Writing Patch Test reports for hypoallergenic claims
- Documenting SPF/PA measurements for sunscreen products
- Ensuring regulatory compliance for functional cosmetics approval
- Validating clinical documentation for completeness and accuracy
- Preparing regulatory submissions to MFDS, NMPA, or other authorities

---

## Core Capabilities

### 1. Human Application Tests (인체적용시험)

Human Application Tests assess the safety of cosmetic products on human subjects. These tests are required for functional cosmetics approval and safety substantiation.

#### 1.1 Skin Irritation Test (피부자극시험)

**Purpose:** Evaluate potential skin irritation from cosmetic products

**Test Methods:**
- **Single Patch Test**: 24-hour occlusive or semi-occlusive patch
- **Repeated Open Application Test (ROAT)**: Multiple applications over 2-3 weeks
- **Human Repeat Insult Patch Test (HRIPT)**: Induction and challenge phases

**Standard Protocol (Single Patch Test):**
1. **Subject Selection**: 30-50 healthy adults, balanced gender, Fitzpatrick skin types I-IV
2. **Test Site**: Upper back or inner forearm
3. **Application**: 0.2 mL or 0.2 g product on 2x2 cm patch
4. **Occlusion Time**: 24 or 48 hours
5. **Reading Times**: 30 min, 24h, 48h, 72h post-removal
6. **Scoring**: ICDRG (International Contact Dermatitis Research Group) scale

**ICDRG Scoring System:**
| Score | Reaction | Description |
|-------|----------|-------------|
| - | Negative | No reaction |
| ? | Doubtful | Faint erythema only |
| + | Weak positive | Erythema, infiltration, possibly papules |
| ++ | Strong positive | Erythema, infiltration, papules, vesicles |
| +++ | Extreme positive | Intense erythema, infiltration, coalescing vesicles |
| IR | Irritant reaction | Different morphology (sharply demarcated, glazed) |

**Report Components:**
- Study protocol and IRB approval
- Subject demographics and skin types
- Test article description (formulation, batch number)
- Positive and negative controls
- Individual subject data
- Statistical analysis (mean irritation index)
- Conclusion on skin compatibility

#### 1.2 Skin Sensitization Test (피부감작시험)

**Purpose:** Evaluate allergic contact dermatitis potential

**Test Methods:**
- **Human Repeat Insult Patch Test (HRIPT)**: Gold standard for sensitization
- **Human Maximization Test (HMT)**: Enhanced sensitivity with pretreatment
- **Repeated Open Application Test (ROAT)**: Confirmatory test

**HRIPT Protocol:**
1. **Induction Phase** (Weeks 1-3):
   - 9 consecutive 24-48 hour patches
   - Same site on back
   - 48-72 hour rest between patches

2. **Rest Period** (Weeks 4-5):
   - 10-14 days without exposure
   - Allows immune response development

3. **Challenge Phase** (Week 6):
   - Single 24-48 hour patch
   - Virgin (previously untreated) site
   - Read at 24h and 48h post-removal

**Subject Requirements:**
- Minimum 100-200 subjects for adequate sensitivity
- Healthy adults, no history of contact dermatitis
- No immunosuppressive medications
- Balanced demographics

**Sensitization Rate Calculation:**
```
Sensitization Rate (%) = (Number of subjects with positive challenge / Total subjects) x 100
```

**Classification:**
| Sensitization Rate | Classification |
|-------------------|----------------|
| 0% | No sensitization potential |
| 0.1-0.9% | Low sensitization potential |
| 1.0-3.9% | Moderate sensitization potential |
| ≥4.0% | High sensitization potential |

#### 1.3 Phototoxicity Test (광독성시험)

**Purpose:** Evaluate skin reactions when product is exposed to UV light

**Test Protocol:**
1. **Application Sites**: Bilateral paired sites (test vs. control)
2. **UV Exposure**: UVA (320-400nm) at 10-20 J/cm²
3. **Timing**: Immediate exposure after product application
4. **Reading**: 24h post-irradiation

**Scoring Criteria:**
- Compare irradiated vs. non-irradiated sites
- Calculate Phototoxicity Index (PI)
- PI ≥ 2.0 indicates phototoxic potential

#### 1.4 Photoallergy Test (광알레르기시험)

**Purpose:** Evaluate delayed allergic reaction induced by UV + product combination

**Test Protocol:**
1. **Induction Phase**: Multiple applications with UV exposure
2. **Rest Period**: 2-3 weeks
3. **Challenge Phase**: Single application + UV exposure on virgin site

---

### 2. Efficacy Clinical Trials (효능임상시험)

Efficacy trials demonstrate the functional benefits of cosmetic products. Required for functional cosmetics (기능성화장품) claims in Korea.

#### 2.1 Whitening Efficacy (미백 효능시험)

**Claims Supported:**
- "피부 미백에 도움을 줌" (Helps skin whitening)
- "기미, 주근깨 완화에 도움" (Helps reduce melasma, freckles)

**Standard Protocol (MFDS Guideline):**
1. **Subjects**: 20-30 per group, Fitzpatrick III-IV, with hyperpigmentation
2. **Duration**: Minimum 8 weeks, preferably 12 weeks
3. **Application**: Twice daily (morning and evening)
4. **Control**: Vehicle control or positive control (existing whitening product)

**Measurement Parameters:**
| Parameter | Instrument | Measurement |
|-----------|------------|-------------|
| Melanin Index | Mexameter MX18 | Direct melanin quantification |
| L* value | Chromameter CR-400 | Skin lightness (CIE L*a*b*) |
| ITA° | Colorimeter | Individual Typology Angle |
| Visual Assessment | Expert grader | Hyperpigmentation severity scale |

**ITA° Calculation:**
```
ITA° = [arctan((L* - 50) / b*)] × (180/π)
```

**ITA° Classification:**
| ITA° Range | Skin Type |
|------------|-----------|
| >55° | Very light |
| 41-55° | Light |
| 28-41° | Intermediate |
| 10-28° | Tan |
| <10° | Brown/Dark |

**Statistical Analysis:**
- Paired t-test or Wilcoxon signed-rank test
- ANOVA for multiple time points
- p < 0.05 for significance
- Report % improvement from baseline

#### 2.2 Anti-Wrinkle Efficacy (주름개선 효능시험)

**Claims Supported:**
- "피부 주름 개선에 도움을 줌" (Helps improve skin wrinkles)
- "탄력 개선에 도움" (Helps improve elasticity)

**Standard Protocol:**
1. **Subjects**: 20-30 per group, age 35-65, crow's feet or forehead wrinkles
2. **Duration**: Minimum 8 weeks, preferably 12 weeks
3. **Test Site**: Crow's feet (lateral canthal area) or forehead

**Measurement Parameters:**
| Parameter | Instrument | Description |
|-----------|------------|-------------|
| Skin Roughness (Ra, Rz) | PRIMOS, Visioscan | 3D surface analysis |
| Wrinkle Depth | Replica analysis | Silicone impression |
| Skin Elasticity (R2, R5, R7) | Cutometer MPA580 | Mechanical properties |
| Visual Wrinkle Grade | Expert grader | Fitzpatrick Wrinkle Scale |

**Cutometer Parameters:**
| Parameter | Meaning | Normal Range |
|-----------|---------|--------------|
| R2 (Ua/Uf) | Gross elasticity | 0.8-1.0 |
| R5 (Ur/Ue) | Net elasticity | 0.8-1.0 |
| R7 (Ur/Uf) | Biological elasticity | 0.5-0.7 |

**Fitzpatrick Wrinkle Scale:**
| Class | Wrinkle Score | Description |
|-------|---------------|-------------|
| I | 1-3 | Fine wrinkles |
| II | 4-6 | Fine to moderate depth wrinkles |
| III | 7-9 | Moderate depth wrinkles |

#### 2.3 Moisturizing Efficacy (보습 효능시험)

**Claims Supported:**
- "피부 보습에 도움을 줌" (Helps skin moisturization)
- "건조한 피부 개선에 도움" (Helps improve dry skin)

**Standard Protocol:**
1. **Subjects**: 20-30 per group, self-reported dry skin
2. **Duration**: Single application (acute) or 4+ weeks (chronic)
3. **Environmental Control**: 20-22°C, 40-50% RH

**Measurement Parameters:**
| Parameter | Instrument | Unit |
|-----------|------------|------|
| Skin Hydration | Corneometer CM825 | Arbitrary Units (AU) |
| TEWL | Tewameter TM300 | g/h/m² |
| Skin Barrier Function | Derived from TEWL | Recovery rate |

**Acute Hydration Protocol:**
- Baseline measurement
- Product application
- Measurements at 1h, 2h, 4h, 6h, 8h post-application
- Calculate AUC (Area Under Curve)

**Chronic Hydration Protocol:**
- Baseline measurement
- Daily application for 4 weeks
- Weekly measurements
- Final assessment at Week 4

---

### 3. Consumer Use Tests (소비자 사용 테스트)

Consumer Use Tests evaluate subjective product performance and user satisfaction.

**Purpose:**
- Support sensory claims (smooth texture, fast absorption)
- Generate satisfaction statistics (% agree)
- Identify potential issues before launch

**Standard Protocol:**
1. **Subjects**: 30-100 target consumers
2. **Duration**: 2-4 weeks typical home use
3. **Survey**: Pre-use, mid-use, post-use questionnaires

**Questionnaire Elements:**
- Product attributes (texture, scent, spreadability)
- Perceived efficacy (moisturization, brightness, smoothness)
- Overall satisfaction
- Purchase intent
- Comparison to current products

**Claim Examples:**
- "93% of users felt skin was more moisturized"
- "4 out of 5 users noticed improved skin texture"
- "89% would recommend to a friend"

**Statistical Requirements:**
- Minimum n=30 for percentage claims
- 95% confidence interval for proportions
- Use exact binomial or Wilson method

---

### 4. Dermatologist Tests (피부과 전문의 테스트)

**Purpose:** Support "Dermatologist Tested" or "Dermatologist Recommended" claims

**Test Types:**
1. **Dermatologist Supervised Study**: Clinical trial under dermatologist oversight
2. **Dermatologist Panel Review**: Product/formulation review by experts
3. **Dermatologist Evaluation**: Expert grading of efficacy/safety data

**Claim Examples:**
- "Dermatologist Tested" (tested under dermatologist supervision)
- "Dermatologist Approved" (reviewed and approved by dermatologists)
- "Recommended by Dermatologists" (survey of practicing dermatologists)

**Documentation Requirements:**
- Names and credentials of participating dermatologists
- Study protocol or evaluation criteria
- Individual assessments or survey results
- Statistical summary

---

### 5. Patch Tests (첩포시험)

Standard patch testing for hypoallergenic claims and product compatibility.

**T.R.U.E. TEST (Thin-layer Rapid Use Epicutaneous Test):**
- Standardized allergen panels
- 48-hour application
- Reading at 48h, 72h, 96h

**Cosmetic-Specific Panel:**
- Fragrances (fragrance mix I, II, balsam of Peru)
- Preservatives (MI, MCI/MI, parabens, formaldehyde releasers)
- Hair dyes (PPD, PTD)
- Lanolin and derivatives
- Propylene glycol
- Cocamidopropyl betaine

**Hypoallergenic Claim Requirements:**
- HRIPT with 0% sensitization rate
- Formulated without common allergens
- Dermatologist or allergist verification

---

### 6. Sunscreen Testing (자외선 차단 효능시험)

#### 6.1 SPF (Sun Protection Factor) Measurement

**In Vivo SPF Test (ISO 24444):**
1. **Subjects**: 10-20 subjects, Fitzpatrick I-III
2. **Application Rate**: 2 mg/cm² on back
3. **UV Source**: Solar simulator (UVB + UVA)
4. **MED Determination**: Minimal Erythema Dose
5. **Calculation**: SPF = MED(protected) / MED(unprotected)

**In Vitro SPF Prediction (ISO 24443):**
1. **Substrate**: PMMA plates (roughness Ra 2 or 6)
2. **Application Rate**: 1.3 mg/cm²
3. **Measurement**: UV transmittance spectrophotometry
4. **Calculation**: Mathematical integration of transmittance

#### 6.2 PA (Protection Grade of UVA)

**In Vivo UVA-PF (ISO 24442, PPD Method):**
1. **PPD Measurement**: Persistent Pigment Darkening
2. **UV Source**: UVA source (320-400nm)
3. **Reading**: 2-4 hours post-irradiation
4. **Calculation**: UVA-PF = MPPDD(protected) / MPPDD(unprotected)

**PA Rating (Japanese Standard):**
| UVA-PF Range | PA Rating |
|--------------|-----------|
| 2-4 | PA+ |
| 4-8 | PA++ |
| 8-16 | PA+++ |
| ≥16 | PA++++ |

#### 6.3 Water Resistance Testing

**Protocol (FDA/ISO):**
1. Baseline SPF measurement
2. Water immersion: 2 x 20 min (water resistant) or 4 x 20 min (very water resistant)
3. Post-immersion SPF measurement
4. Calculate % SPF retention

**Claim Requirements:**
| Claim | Requirement |
|-------|-------------|
| Water Resistant | ≥50% SPF retention after 2 x 20 min |
| Very Water Resistant | ≥50% SPF retention after 4 x 20 min |

---

## Regulatory Compliance

### Korea MFDS (식품의약품안전처)

**Functional Cosmetics Categories:**
1. 미백 (Whitening)
2. 주름개선 (Anti-wrinkle)
3. 자외선차단 (UV Protection)
4. 모발 염색/탈색/탈모
5. 여드름 완화
6. 아토피성 피부 보습

**Required Documentation:**
- Human Application Test reports (인체적용시험 자료)
- Efficacy test data (효능시험 자료)
- Stability data
- Safety data (피부자극, 감작, 광독성)

**Testing Laboratory Requirements:**
- MFDS-designated testing institution
- GLP (Good Laboratory Practice) compliance
- ISO 17025 accreditation

### EU Cosmetic Products Regulation (CPR 1223/2009)

**Product Safety Report (PSR) Components:**
- Part A: Product Safety Information
- Part B: Product Safety Assessment

**Human Patch Test Requirements:**
- HRIPT for sensitization assessment
- Documentation in Product Information File (PIF)

### FDA (United States)

**OTC Monograph for Sunscreens:**
- SPF testing per FDA Final Monograph
- Broad Spectrum test (Critical Wavelength ≥ 370nm)
- Water resistance labeling

### China NMPA (国家药品监督管理局)

**Special Use Cosmetics Categories:**
- 祛斑美白 (Whitening)
- 防晒 (Sunscreen)
- 染发 (Hair dye)
- 烫发/脱毛

**Required Tests:**
- Human safety test (30 subjects minimum)
- Efficacy substantiation data
- Acute oral toxicity (animal or alternative)

---

## Resources

### Reference Files

- `references/human_application_test_guidelines.md` - MFDS 인체적용시험 가이드라인
- `references/efficacy_test_standards.md` - 효능시험 방법 표준
- `references/spf_pa_measurement.md` - SPF/PA 측정 프로토콜 (ISO 24444, 24442)
- `references/regulatory_requirements.md` - 국가별 규제 요건 (한국, EU, 미국, 중국)
- `references/statistical_methods.md` - 임상시험 통계분석 방법
- `references/grading_scales.md` - 피부반응 평가척도 (ICDRG, Fitzpatrick)

### Template Assets

- `assets/irritation_test_template.md` - 피부자극시험 보고서 템플릿
- `assets/hript_template.md` - HRIPT 보고서 템플릿
- `assets/whitening_efficacy_template.md` - 미백 효능시험 보고서 템플릿
- `assets/antiwrinkle_efficacy_template.md` - 주름개선 효능시험 보고서 템플릿
- `assets/moisturizing_efficacy_template.md` - 보습 효능시험 보고서 템플릿
- `assets/spf_test_template.md` - SPF 측정 보고서 템플릿
- `assets/consumer_use_test_template.md` - 소비자 사용 테스트 보고서 템플릿
- `assets/clinical_protocol_template.md` - 임상시험 프로토콜 템플릿

### Automation Scripts

- `scripts/validate_efficacy_report.py` - 효능시험 보고서 검증
- `scripts/validate_safety_report.py` - 안전성 시험 보고서 검증
- `scripts/calculate_statistics.py` - 임상 데이터 통계 분석
- `scripts/generate_report_template.py` - 보고서 템플릿 생성
- `scripts/spf_calculator.py` - SPF/PA 계산기

---

## Workflow Examples

### Functional Cosmetics Approval (기능성화장품 심사)

**Phase 1: Safety Assessment (4-8 weeks)**
1. Primary Skin Irritation Test (24h patch)
2. HRIPT (6 weeks)
3. Phototoxicity Test (if UV-absorbing ingredients)
4. Documentation and report writing

**Phase 2: Efficacy Testing (8-12 weeks)**
1. Clinical trial protocol development
2. IRB approval
3. Subject recruitment and screening
4. Efficacy measurements (baseline, week 4, 8, 12)
5. Statistical analysis
6. Report preparation

**Phase 3: Regulatory Submission**
1. Compile all test reports
2. Prepare submission dossier
3. Submit to MFDS
4. Respond to queries

### Sunscreen Development

**SPF Development Cycle:**
1. In vitro SPF prediction (formulation optimization)
2. Preliminary in vivo SPF (10 subjects)
3. Final in vivo SPF (confirmatory)
4. UVA-PF measurement (PA rating)
5. Water resistance testing (if claimed)
6. Regulatory submission

---

## Best Practices

### Study Design
- Use appropriate sample sizes (power analysis)
- Include proper controls (vehicle, positive control)
- Randomize subject allocation when possible
- Blind evaluators to treatment assignment

### Data Quality
- Follow GCP/GLP principles
- Document all deviations
- Use validated instruments
- Maintain audit trails

### Statistical Rigor
- Pre-specify analysis methods
- Use appropriate tests for data type
- Report confidence intervals
- Address missing data appropriately

### Regulatory Awareness
- Know target market requirements
- Use accredited laboratories
- Keep current with guideline updates
- Document claim substantiation

---

## Final Checklist

Before finalizing any cosmetic clinical report, verify:

- [ ] Study protocol followed correctly
- [ ] IRB/ethics approval documented
- [ ] Subject informed consent obtained
- [ ] Appropriate sample size achieved
- [ ] Controls included and documented
- [ ] Measurements taken per protocol
- [ ] Statistical analysis appropriate
- [ ] Results clearly presented
- [ ] Conclusions supported by data
- [ ] Regulatory requirements met
- [ ] Report format follows template
- [ ] All signatures and dates present
- [ ] Quality review completed
