# Human Application Test Guidelines (인체적용시험 가이드라인)

## Overview

Human Application Tests (인체적용시험) are clinical studies conducted on human subjects to evaluate the safety and efficacy of cosmetic products. These tests are required for functional cosmetics approval in Korea and serve as the foundation for safety substantiation globally.

## Regulatory Framework

### Korea MFDS Requirements

**Legal Basis:**
- 화장품법 제4조 (기능성화장품 심사)
- 화장품법 시행규칙 제9조 (인체적용시험)
- 기능성화장품 심사에 관한 규정 (식약처 고시)

**Required Tests by Product Type:**

| 기능성 유형 | 피부자극시험 | 감작시험 | 광독성시험 | 효능시험 |
|------------|------------|---------|----------|---------|
| 미백 | ✓ | ✓ | △ | ✓ |
| 주름개선 | ✓ | ✓ | △ | ✓ |
| 자외선차단 | ✓ | ✓ | ✓ | ✓ |
| 탈모 | ✓ | ✓ | - | ✓ |

△ = 광흡수 성분 함유 시 필수

### Testing Institution Requirements

**MFDS 지정기관 요건:**
1. GLP (Good Laboratory Practice) 인증
2. ISO 17025 시험기관 인정
3. 피부과 전문의 참여
4. 적합한 시험시설 및 장비

**주요 지정기관:**
- 대학병원 임상시험센터
- 피부과학연구소
- 화장품 전문 CRO

---

## Test Categories

### 1. Primary Skin Irritation Test (1차 피부자극시험)

#### Single Application Patch Test

**Purpose:** Evaluate acute skin irritation potential

**Protocol:**
```
Day 0: Baseline assessment, patch application
Day 1: Patch removal (24h), reading at 30min post-removal
Day 2: Reading at 24h post-removal
Day 3: Reading at 48h post-removal (optional)
```

**Subject Selection:**
- Number: 30-50 subjects
- Age: 20-60 years
- Gender: Balanced (unless target-specific)
- Skin Type: Fitzpatrick I-IV (representative)
- Health: No skin diseases, no topical medications

**Exclusion Criteria:**
- Active skin diseases (eczema, psoriasis)
- Known allergies to test ingredients
- Pregnancy or lactation
- Immunosuppressive therapy
- Topical steroids within 2 weeks

**Application Details:**
- Test Site: Upper back (between scapulae) or inner forearm
- Patch Size: 2 x 2 cm (Finn Chamber or equivalent)
- Amount: 0.2 mL (liquid) or 0.2 g (semi-solid)
- Occlusion: Semi-occlusive (Finn Chamber) or occlusive (Patch Test Chamber)
- Duration: 24 hours standard, 48 hours optional

**Reading Schedule:**
| Time Point | Assessment |
|------------|------------|
| 30 min post-removal | Immediate reactions, irritant vs. allergic differentiation |
| 24 h post-removal | Delayed irritation |
| 48 h post-removal | Persistent reactions (optional) |
| 72 h post-removal | Late reactions (if 48h reading is positive) |

#### Cumulative Irritation Test

**Purpose:** Evaluate repeated exposure irritation

**Protocol:**
- 21 consecutive daily applications
- 24h semi-occlusive patches
- Same site throughout
- Daily readings using ICDRG scale

**Cumulative Irritation Index (CII):**
```
CII = Σ(Daily Scores) / (Number of Subjects × Number of Days)
```

**Classification:**
| CII | Classification |
|-----|----------------|
| 0 | Non-irritating |
| 0.1-0.4 | Minimally irritating |
| 0.5-1.9 | Mildly irritating |
| 2.0-4.9 | Moderately irritating |
| ≥5.0 | Severely irritating |

---

### 2. Skin Sensitization Test (피부감작시험)

#### Human Repeat Insult Patch Test (HRIPT)

**Purpose:** Evaluate allergic contact dermatitis (Type IV hypersensitivity) potential

**Protocol Overview:**
```
Week 1-3: Induction Phase (9 patches)
Week 4-5: Rest Period (10-14 days)
Week 6: Challenge Phase (1 patch)
```

**Detailed Induction Protocol:**

| Patch # | Day | Application | Occlusion | Reading |
|---------|-----|-------------|-----------|---------|
| 1 | 1 | Apply | 24-48h | Day 2 or 3 |
| 2 | 3 | Apply | 24-48h | Day 4 or 5 |
| 3 | 5 | Apply | 24-48h | Day 6 or 8 |
| 4 | 8 | Apply | 24-48h | Day 9 or 10 |
| 5 | 10 | Apply | 24-48h | Day 11 or 12 |
| 6 | 12 | Apply | 24-48h | Day 13 or 15 |
| 7 | 15 | Apply | 24-48h | Day 16 or 17 |
| 8 | 17 | Apply | 24-48h | Day 18 or 19 |
| 9 | 19 | Apply | 24-48h | Day 20 or 22 |

**Rest Period:** Days 22-36 (minimum 10 days, preferably 14 days)

**Challenge Protocol:**
- Day 36-38: Apply challenge patch to virgin site
- Day 37-40: Remove patch after 24-48h
- Reading: 24h and 48h post-removal

**Subject Requirements:**
- Minimum: 100 subjects (200 preferred for new ingredients)
- Completion: ≥80% completing all phases
- Demographics: Representative of target population

**Sensitization Interpretation:**
| Challenge Reaction | Interpretation |
|-------------------|----------------|
| Negative (-) | No sensitization |
| Doubtful (?) | Uncertain, may require re-challenge |
| Positive (+, ++, +++) | Sensitization confirmed |

**Sensitization Rate Reporting:**
- Report % of subjects with positive challenge reactions
- 95% confidence interval for proportion
- Compare to historical data for ingredient class

#### Human Maximization Test (HMT) - Kligman Method

**Purpose:** Enhanced sensitivity for detecting weak sensitizers

**Modifications from standard HRIPT:**
1. **Pre-treatment:** 24h SLS (sodium lauryl sulfate) patch before first induction
2. **Enhanced occlusion:** 48h patches with increased pressure
3. **Challenge enhancement:** SLS pre-treatment before challenge

**When to Use:**
- New chemical entities
- Ingredients with structural alerts for sensitization
- Products containing fragrances at high concentrations

---

### 3. Phototoxicity Test (광독성시험)

**Purpose:** Evaluate acute phototoxic potential (immediate, non-immunological reaction)

**Required For:**
- Products containing UV-absorbing chemicals
- Products with known phototoxic ingredients (psoralens, certain essential oils)
- Sunscreen products

**Protocol:**

**Day 0 - Application:**
1. Apply product to bilateral paired sites (4 sites minimum)
2. Amount: 2 μL/cm² or 2 mg/cm²
3. Allow 15-30 minutes for absorption

**UV Irradiation:**
- Source: Solar simulator or filtered xenon arc lamp
- Spectrum: UVA 320-400 nm (primarily)
- Dose: 10-20 J/cm² UVA
- Control site: Covered (no UV exposure)

**Reading Schedule:**
| Time | Assessment |
|------|------------|
| Immediately post-UV | Immediate erythema |
| 24h post-UV | Primary phototoxic reaction |
| 48h post-UV | Delayed reaction (if positive at 24h) |

**Phototoxicity Index (PI):**
```
PI = Score(UV + Product) - Score(UV only) - Score(Product only)
```

**Interpretation:**
| PI | Classification |
|----|----------------|
| <2 | Non-phototoxic |
| 2-5 | Weakly phototoxic |
| >5 | Phototoxic |

---

### 4. Photoallergy Test (광알레르기시험)

**Purpose:** Evaluate photoallergic potential (delayed, immunological reaction requiring UV + allergen)

**Protocol - Photopatch Test:**

**Induction Phase (3 weeks):**
1. Apply product to same site
2. UV irradiation (UVA 5-10 J/cm²) after each application
3. 3 times per week for 3 weeks

**Rest Period:** 2 weeks

**Challenge Phase:**
1. Apply to virgin site
2. UV irradiation after application
3. Read at 24h, 48h, 72h post-irradiation

**Controls:**
- Product only (no UV)
- UV only (no product)
- Vehicle + UV
- Known photoallergen (positive control)

---

## Scoring Systems

### ICDRG (International Contact Dermatitis Research Group) Scale

| Symbol | Score | Reaction | Description |
|--------|-------|----------|-------------|
| - | 0 | Negative | No reaction |
| ? | 0.5 | Doubtful | Faint erythema only |
| + | 1 | Weak positive | Erythema, slight infiltration |
| ++ | 2 | Strong positive | Erythema, infiltration, papules |
| +++ | 3 | Extreme positive | Vesicles, bullae |
| IR | - | Irritant | Sharply demarcated, glazed erythema |

### Draize Scale (Alternative)

| Score | Erythema | Edema |
|-------|----------|-------|
| 0 | None | None |
| 1 | Very slight (barely perceptible) | Very slight |
| 2 | Well defined | Slight (raised edges) |
| 3 | Moderate to severe | Moderate (raised ~1mm) |
| 4 | Severe (beet redness) | Severe (raised >1mm, spreading) |

### Primary Irritation Index (PII)

```
PII = Σ(Erythema + Edema Scores) / (Number of Subjects × Number of Sites)
```

| PII | Classification |
|-----|----------------|
| 0 | Non-irritating |
| 0.1-0.5 | Negligible irritation |
| 0.5-2.0 | Mild irritation |
| 2.0-5.0 | Moderate irritation |
| 5.0-8.0 | Severe irritation |

---

## Statistical Analysis

### Sample Size Calculation

**For Irritation Test (Continuous Outcome):**
```
n = 2 × [(Zα/2 + Zβ)² × σ²] / δ²

Where:
- Zα/2 = 1.96 (for α = 0.05)
- Zβ = 0.84 (for power = 80%)
- σ = expected standard deviation
- δ = minimum detectable difference
```

**For Sensitization Test (Proportion):**
```
n = [Zα/2 × √(2p̄q̄) + Zβ × √(p1q1 + p2q2)]² / (p1 - p2)²

Where:
- p1 = expected sensitization rate for test product
- p2 = expected sensitization rate for control (usually 0)
- p̄ = (p1 + p2) / 2
```

**Recommended Minimum Sample Sizes:**
| Test Type | Minimum n | Preferred n |
|-----------|-----------|-------------|
| Primary Irritation | 30 | 50 |
| Cumulative Irritation | 15 | 25 |
| HRIPT | 100 | 200 |
| Phototoxicity | 10 | 25 |
| Photoallergy | 25 | 50 |

### Statistical Tests

**For Paired Data (Pre-Post):**
- Wilcoxon signed-rank test (non-parametric)
- Paired t-test (if normally distributed)

**For Group Comparisons:**
- Mann-Whitney U test (non-parametric)
- Independent t-test (if normally distributed)

**For Proportions:**
- Fisher's exact test (small samples)
- Chi-square test (larger samples)
- Exact binomial confidence intervals

---

## Report Requirements

### Essential Report Sections

1. **Title Page**
   - Study title and protocol number
   - Sponsor and testing laboratory
   - Report date and version

2. **Study Summary**
   - Objective
   - Test article description
   - Subject population
   - Key findings

3. **Ethics Statement**
   - IRB approval number and date
   - Informed consent documentation
   - Declaration of Helsinki compliance

4. **Materials and Methods**
   - Test article specifications
   - Subject selection criteria
   - Study design and procedures
   - Assessment methods and scales

5. **Results**
   - Subject demographics
   - Individual subject data
   - Statistical analysis
   - Adverse events

6. **Discussion and Conclusion**
   - Interpretation of results
   - Comparison to acceptance criteria
   - Safety conclusion

7. **Appendices**
   - IRB approval letter
   - Informed consent form
   - Individual subject data tables
   - Statistical analysis details
   - Photographs (if applicable)

---

## Quality Assurance

### GLP Compliance Checklist

- [ ] Study protocol approved before initiation
- [ ] Test article properly identified and characterized
- [ ] Subject informed consent documented
- [ ] Study conducted per protocol
- [ ] Deviations documented and justified
- [ ] Raw data complete and accurate
- [ ] Statistical analysis appropriate
- [ ] Report reviewed and approved by Study Director
- [ ] Archive procedures followed

### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| High dropout rate | Over-recruit by 20%; incentivize completion |
| Inconsistent readings | Blind evaluators; training and calibration |
| Site reactions | Document and differentiate from test reactions |
| Missing data | Use appropriate imputation; sensitivity analysis |
| Protocol deviations | Document, assess impact, include in report |

---

*Reference: MFDS 기능성화장품 심사에 관한 규정, ISO 10993-10, OECD Guidelines*
