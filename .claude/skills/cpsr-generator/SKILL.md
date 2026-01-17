---
name: cpsr-generator
description: Generate EU Cosmetic Product Safety Reports (CPSR) compliant with EC Regulation 1223/2009. Automatically calculates Margin of Safety (MoS), Systemic Exposure Dose (SED), and generates Part A (Product Safety Information) documentation from ingredient lists. Supports toxicological profile generation, exposure calculations, and regulatory compliance checks for EU market access.
allowed-tools: [Read, Write, Edit, Bash]
license: MIT License
metadata:
    skill-author: EVAS Cosmetic
    regulation: EC 1223/2009, UK Cosmetics Regulation
---

# CPSR Generator (Cosmetic Product Safety Report)

## Overview

The CPSR Generator automates the creation of Cosmetic Product Safety Reports required for EU market access under EC Regulation 1223/2009. This skill takes a product formula (ingredient list with concentrations) and generates Part A of the CPSR, including toxicological profiles, exposure calculations, and Margin of Safety (MoS) assessments.

**Key Capabilities:**
- Automatic CAS/EINECS number lookup for ingredients
- SED (Systemic Exposure Dose) calculation
- MoS (Margin of Safety) calculation from NOAEL data
- Toxicological profile generation
- Part A documentation draft generation
- Regulatory compliance checking

## When to Use This Skill

Use this skill when:
- Preparing a cosmetic product for EU market entry
- Creating Part A of the Product Information File (PIF)
- Calculating safety margins for ingredients
- Documenting toxicological profiles
- Preparing for Safety Assessor review
- Updating existing CPSR after formula changes

## Regulatory Background

### EU Cosmetics Regulation (EC) No. 1223/2009

**Article 10 - Safety Assessment:**
> "Prior to placing a cosmetic product on the market, the responsible person shall ensure that the cosmetic product has undergone a safety assessment... and that a cosmetic product safety report is set up."

**Annex I - Cosmetic Product Safety Report:**
- **Part A**: Cosmetic Product Safety Information
- **Part B**: Cosmetic Product Safety Assessment (requires qualified Safety Assessor)

### CPSR Structure

```
COSMETIC PRODUCT SAFETY REPORT
│
├── Part A: Cosmetic Product Safety Information
│   ├── 1. Quantitative and Qualitative Composition
│   ├── 2. Physical/Chemical Characteristics and Stability
│   ├── 3. Microbiological Quality
│   ├── 4. Impurities, Traces, Packaging Material
│   ├── 5. Normal and Reasonably Foreseeable Use
│   ├── 6. Exposure to the Cosmetic Product
│   ├── 7. Exposure to Substances
│   ├── 8. Toxicological Profile of Substances
│   ├── 9. Undesirable Effects and Serious Undesirable Effects
│   └── 10. Information on the Cosmetic Product
│
└── Part B: Cosmetic Product Safety Assessment
    ├── 1. Assessment Conclusion
    ├── 2. Labeled Warnings and Instructions
    ├── 3. Reasoning
    └── 4. Assessor's Credentials
```

---

## Core Calculations

### 1. Systemic Exposure Dose (SED)

SED represents the amount of a substance that enters the body systemically through dermal absorption.

**Formula:**
```
SED (mg/kg bw/day) = (A × C × DA × F) / (1000 × BW)

Where:
- A = Amount of product applied (mg/day)
- C = Concentration of ingredient (%)
- DA = Dermal Absorption (%, default assumptions below)
- F = Frequency of application (times/day)
- BW = Body Weight (default: 60 kg adult)
```

**SCCS Default Values for Amount Applied (A):**

| Product Type | Amount (mg/day) | Exposure Area |
|--------------|-----------------|---------------|
| Body lotion | 7,820 | Whole body |
| Face cream | 800 | Face |
| Hand cream | 2,160 | Hands |
| Lipstick | 57 | Lips |
| Eye shadow | 20 | Eye area |
| Mascara | 25 | Eyelashes |
| Foundation | 510 | Face |
| Hair styling | 3,920 | Hair |
| Shampoo | 10,460 | Hair |
| Shower gel | 16,200 | Whole body |
| Toothpaste | 138 | Oral cavity |
| Mouthwash | 32,000 | Oral cavity |

**Dermal Absorption (DA) Defaults:**
| Condition | DA Value |
|-----------|----------|
| No data available, MW < 500 | 100% |
| No data available, MW > 500 | 50% |
| SCCS/CIR published value | Use published value |
| In vitro study available | Use study value |

### 2. Margin of Safety (MoS)

MoS indicates the safety margin between the actual exposure and the level that causes no adverse effects.

**Formula:**
```
MoS = NOAEL / SED

Where:
- NOAEL = No Observed Adverse Effect Level (mg/kg bw/day)
- SED = Systemic Exposure Dose (mg/kg bw/day)
```

**Interpretation:**
| MoS Value | Interpretation |
|-----------|----------------|
| ≥ 100 | Generally considered safe |
| 50-100 | May require additional justification |
| < 50 | Typically not acceptable without strong justification |

**Why 100 as threshold?**
- 10× for interspecies variability (animal to human)
- 10× for intraspecies variability (human to human)
- Total safety factor = 10 × 10 = 100

### 3. Aggregate Exposure

When an ingredient appears in multiple products used simultaneously:

```
Total SED = SED_product1 + SED_product2 + ... + SED_productN
MoS_aggregate = NOAEL / Total_SED
```

---

## Toxicological Profile Requirements

### Required Data Points per Ingredient

| Endpoint | Test/Source | Requirement Level |
|----------|-------------|-------------------|
| Acute Oral Toxicity | LD50 | Essential |
| Acute Dermal Toxicity | LD50 | If dermal route relevant |
| Skin Irritation | OECD 439/431 | Essential |
| Eye Irritation | OECD 437/438 | Essential |
| Skin Sensitization | DPRA, KeratinoSens, h-CLAT | Essential |
| Dermal Absorption | In vitro/SCCS default | For SED calculation |
| Repeated Dose Toxicity | NOAEL | For MoS calculation |
| Mutagenicity/Genotoxicity | Ames, MN, Comet | Essential |
| Reproductive Toxicity | OECD 421/422 | If data available |
| Carcinogenicity | Literature review | If relevant |
| Phototoxicity | OECD 432 | If UV-absorbing |

### Data Sources Priority

1. **CIR (Cosmetic Ingredient Review)** - Most authoritative for cosmetics
2. **SCCS Opinions** - EU Scientific Committee opinions
3. **ECHA Registration Dossiers** - REACH data
4. **Supplier TDS/MSDS** - Manufacturer data
5. **Published Literature** - Peer-reviewed studies
6. **Read-across** - From structurally similar compounds

---

## Input/Output Specification

### Input Format

**JSON Formula Input:**
```json
{
  "product_name": "Brightening Essence",
  "product_type": "face_cream",
  "intended_use": "Leave-on face product for daily use",
  "target_population": "Adults",
  "formula": [
    {
      "inci_name": "AQUA",
      "concentration": 70.0,
      "function": "Solvent"
    },
    {
      "inci_name": "GLYCERIN",
      "concentration": 5.0,
      "function": "Humectant"
    },
    {
      "inci_name": "NIACINAMIDE",
      "concentration": 4.0,
      "function": "Skin Conditioning"
    },
    {
      "inci_name": "PHENOXYETHANOL",
      "concentration": 0.9,
      "function": "Preservative"
    }
  ]
}
```

**CSV Formula Input:**
```csv
inci_name,concentration,function,cas_number
AQUA,70.0,Solvent,7732-18-5
GLYCERIN,5.0,Humectant,56-81-5
NIACINAMIDE,4.0,Skin Conditioning,98-92-0
PHENOXYETHANOL,0.9,Preservative,122-99-6
```

### Output Format

**Part A Document (Markdown/Word):**
```markdown
# COSMETIC PRODUCT SAFETY REPORT - PART A
## Product: [Product Name]

### 1. Quantitative and Qualitative Composition

| INCI Name | CAS No. | EINECS | Conc. (%) | Function |
|-----------|---------|--------|-----------|----------|
| AQUA | 7732-18-5 | 231-791-2 | 70.0 | Solvent |
| ... | ... | ... | ... | ... |

### 6. Exposure to the Cosmetic Product

- Product Type: Face Cream
- Application Amount: 800 mg/day
- Frequency: 2x daily
- Retention Factor: 100% (leave-on)

### 7. Exposure to Substances

| Ingredient | Conc. (%) | SED (mg/kg/day) |
|------------|-----------|-----------------|
| NIACINAMIDE | 4.0 | 0.533 |
| ... | ... | ... |

### 8. Toxicological Profile

#### NIACINAMIDE
- CAS: 98-92-0
- NOAEL: 1000 mg/kg/day (oral, rat, 90-day)
- Dermal Absorption: 100% (default)
- SED: 0.533 mg/kg/day
- **MoS: 1876** ✓ (>100)
- Skin Irritation: Non-irritating
- Sensitization: Non-sensitizer
- Mutagenicity: Negative
```

---

## Workflow

### Step 1: Formula Input
```bash
python scripts/parse_formula.py input_formula.csv -o parsed_formula.json
```

### Step 2: CAS/EINECS Lookup
```bash
python scripts/lookup_identifiers.py parsed_formula.json -o formula_with_ids.json
```

### Step 3: Toxicological Data Collection
```bash
python scripts/collect_tox_data.py formula_with_ids.json -o tox_profiles.json
```

### Step 4: Exposure & MoS Calculation
```bash
python scripts/calculate_mos.py formula_with_ids.json \
  --product-type face_cream \
  --tox-data tox_profiles.json \
  -o mos_calculations.json
```

### Step 5: Generate Part A Document
```bash
python scripts/generate_cpsr_part_a.py \
  --formula formula_with_ids.json \
  --mos mos_calculations.json \
  --tox tox_profiles.json \
  --template templates/cpsr_part_a.md \
  -o CPSR_Part_A_ProductName.md
```

### Complete Pipeline
```bash
python scripts/cpsr_pipeline.py input_formula.csv \
  --product-type face_cream \
  --product-name "Brightening Essence" \
  -o output/
```

---

## Product Type Exposure Parameters

### SCCS Notes of Guidance (11th Revision) Values

```python
EXPOSURE_PARAMS = {
    "body_lotion": {
        "amount_mg": 7820,
        "frequency": 1,
        "retention": 1.0,
        "area_cm2": 15670
    },
    "face_cream": {
        "amount_mg": 800,
        "frequency": 2,
        "retention": 1.0,
        "area_cm2": 565
    },
    "hand_cream": {
        "amount_mg": 2160,
        "frequency": 2,
        "retention": 1.0,
        "area_cm2": 860
    },
    "lipstick": {
        "amount_mg": 57,
        "frequency": 2,
        "retention": 1.0,
        "area_cm2": 3.5,
        "oral_exposure": True
    },
    "eye_cream": {
        "amount_mg": 200,
        "frequency": 2,
        "retention": 1.0,
        "area_cm2": 32
    },
    "shampoo": {
        "amount_mg": 10460,
        "frequency": 1,
        "retention": 0.01,  # Rinse-off
        "area_cm2": 580
    },
    "shower_gel": {
        "amount_mg": 16200,
        "frequency": 1,
        "retention": 0.01,
        "area_cm2": 17500
    },
    "toothpaste": {
        "amount_mg": 138,
        "frequency": 2,
        "retention": 0.05,
        "area_cm2": 50,
        "oral_exposure": True
    },
    "sunscreen": {
        "amount_mg": 18000,
        "frequency": 1,
        "retention": 1.0,
        "area_cm2": 17500
    },
    "serum": {
        "amount_mg": 500,
        "frequency": 2,
        "retention": 1.0,
        "area_cm2": 565
    },
    "toner": {
        "amount_mg": 1400,
        "frequency": 2,
        "retention": 1.0,
        "area_cm2": 565
    },
    "essence": {
        "amount_mg": 600,
        "frequency": 2,
        "retention": 1.0,
        "area_cm2": 565
    },
    "ampoule": {
        "amount_mg": 300,
        "frequency": 1,
        "retention": 1.0,
        "area_cm2": 565
    },
    "sheet_mask": {
        "amount_mg": 20000,
        "frequency": 0.14,  # 1x/week
        "retention": 0.5,   # Partial absorption
        "area_cm2": 565
    }
}
```

---

## Regulatory Restrictions Check

### EU Annex II (Prohibited Substances)
Automatic check against 1,600+ prohibited substances

### EU Annex III (Restricted Substances)
Check concentration limits:
```python
ANNEX_III_LIMITS = {
    "PHENOXYETHANOL": {"max_conc": 1.0, "product_type": "all"},
    "SALICYLIC_ACID": {"max_conc": 0.5, "product_type": "leave_on", "note": "Not for children <3"},
    "RETINOL": {"max_conc": 0.3, "product_type": "face", "note": "0.05% for body"},
    "HYDROQUINONE": {"max_conc": 0, "product_type": "all", "note": "Prohibited except nail products"},
    # ... etc.
}
```

### EU Annex IV (Colorants)
Check CI numbers and allowed uses

### EU Annex V (Preservatives)
Check preservative limits and combinations

### EU Annex VI (UV Filters)
Check UV filter limits

---

## Resources

### Reference Files
- `references/sccs_exposure_parameters.md` - SCCS default exposure values
- `references/noael_database.md` - Common ingredient NOAEL values
- `references/dermal_absorption.md` - Dermal absorption defaults and studies
- `references/annex_restrictions.md` - EU Annex II-VI restrictions
- `references/mos_calculation_guide.md` - Detailed MoS calculation methodology

### Template Assets
- `assets/cpsr_part_a_template.md` - Part A document template
- `assets/tox_profile_template.md` - Individual ingredient tox profile
- `assets/mos_summary_template.md` - MoS calculation summary table

### Scripts
- `scripts/parse_formula.py` - Parse formula from CSV/JSON
- `scripts/lookup_identifiers.py` - CAS/EINECS number lookup
- `scripts/calculate_mos.py` - SED and MoS calculations
- `scripts/collect_tox_data.py` - Collect toxicological data
- `scripts/check_restrictions.py` - EU Annex compliance check
- `scripts/generate_cpsr_part_a.py` - Generate Part A document
- `scripts/cpsr_pipeline.py` - Complete generation pipeline

---

## Part B: Safety Assessment

### Overview

Part B is the Safety Assessor's conclusion and must be completed by a qualified professional meeting Article 10(2) requirements. This skill provides:

1. **Part B Template** - Structured template following Annex I requirements
2. **Safety Conclusion Guide** - Decision logic for reaching safety conclusions
3. **MoS Interpretation** - Guidelines for justifying safety margins

### Part B Structure

```
Part B: Cosmetic Product Safety Assessment
│
├── 1. Assessment Conclusion
│   ├── Safety statement
│   └── Summary of evaluation
│
├── 2. Review of Part A Information
│   ├── Composition assessment
│   ├── Stability & microbiological review
│   ├── Exposure assessment review
│   └── Toxicological profile evaluation
│
├── 3. Labelled Warnings and Instructions
│   ├── Mandatory warnings (Annex III)
│   ├── Recommended warnings
│   └── Instructions for use
│
├── 4. Reasoning
│   ├── Overall safety reasoning
│   ├── Vulnerable populations
│   ├── Cumulative exposure
│   └── Regulatory compliance
│
└── 5. Assessor's Credentials
    ├── Qualifications
    └── Declaration of independence
```

### Safety Conclusion Decision Tree

```
START
  │
  ├─► All ingredients permitted under EU 1223/2009?
  │     NO → UNSAFE
  │     YES ↓
  │
  ├─► Restricted ingredients within Annex III limits?
  │     NO → UNSAFE
  │     YES ↓
  │
  ├─► All MoS ≥ 100?
  │     │
  │     ├─ All ≥ 100 → Continue
  │     ├─ Some 50-100 → Requires justification
  │     └─ Any < 50 → UNSAFE
  │
  ├─► Microbiological quality acceptable?
  │     NO → UNSAFE
  │     YES ↓
  │
  ├─► Stability adequate for claimed shelf life?
  │     NO → Request data or reduce shelf life
  │     YES ↓
  │
  ├─► Labelling requirements met?
  │     NO → SAFE with modifications
  │     YES ↓
  │
  └─► SAFE for intended use
```

### MoS Justification Guidelines

When MoS is between 50-100, acceptable justifications include:

| Justification | Example |
|--------------|---------|
| Conservative NOAEL | Used lower species/endpoint value |
| Limited absorption | MW > 500 Da, measured low absorption |
| Local effect only | No systemic concern |
| Short exposure | Rinse-off, infrequent use |
| Historical safe use | Long market history |

### Vulnerable Population Considerations

| Population | Adjustment |
|------------|------------|
| Children < 3 years | Higher surface/BW ratio, consider MoS ≥ 200 |
| Pregnant women | Check retinoids, salicylates, essential oils |
| Sensitive skin | HRIPT required, sensitizer assessment |

### Part B Workflow

```bash
# 1. Review Part A data completeness
python scripts/validate_part_a.py cpsr_part_a.json

# 2. Generate Part B template with pre-filled data
python scripts/generate_cpsr_part_b.py \
  --part-a cpsr_part_a.json \
  --mos-data mos_calculations.json \
  -o CPSR_Part_B_Draft.md

# 3. Safety Assessor completes manual sections
# 4. Final review and sign-off
```

### Part B Template Sections

| Section | Automation Level |
|---------|-----------------|
| Assessment Conclusion | Template + Manual review |
| Part A Review | Auto-populated from Part A |
| MoS Summary Table | Auto-generated |
| Required Warnings | Auto-detected from ingredients |
| Reasoning | Manual - Safety Assessor |
| Credentials | Template + Manual |

### Part B Resources

- `assets/cpsr_part_b_template.md` - Complete Part B template
- `references/safety_conclusion_guide.md` - Decision logic for conclusions
- `references/warning_requirements.md` - Mandatory warnings by ingredient

---

## Limitations

1. **Part B Requires Safety Assessor**: Part B must be reviewed and signed by a qualified Safety Assessor with appropriate credentials under Article 10(2).

2. **NOAEL Data Availability**: MoS calculations depend on available NOAEL data. Novel ingredients may lack published values.

3. **Dermal Absorption Estimates**: Without specific studies, default assumptions (100% or 50%) are used, which may be conservative.

4. **Aggregate Exposure**: Tool calculates single-product exposure. Aggregate exposure from multiple products requires additional assessment.

5. **Special Populations**: Default calculations use adult (60 kg) parameters. Children, pregnant women, or other populations may need adjustments.

---

## Quality Checklist

### Part A Checklist

Before submitting Part A to Safety Assessor:

- [ ] All ingredients have CAS numbers
- [ ] All ingredients checked against Annex II (prohibited)
- [ ] All restricted ingredients within limits (Annex III-VI)
- [ ] All ingredients have toxicological profiles
- [ ] All MoS values ≥ 100 (or justified)
- [ ] Product type exposure parameters correct
- [ ] Stability data referenced
- [ ] Microbiological specifications defined
- [ ] Packaging compatibility confirmed
- [ ] IFRA compliance confirmed (for fragrance)

### Part B Checklist

Before finalizing Part B:

- [ ] All Part A sections reviewed and verified
- [ ] MoS calculations reviewed and interpreted
- [ ] Vulnerable populations assessed
- [ ] Cumulative exposure considered
- [ ] Required warnings identified
- [ ] Labelling requirements verified
- [ ] Safety reasoning documented
- [ ] Assessor credentials confirmed (Article 10(2))
- [ ] Declaration of independence signed
- [ ] Final safety conclusion stated
