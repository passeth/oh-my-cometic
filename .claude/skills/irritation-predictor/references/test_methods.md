---
title: In Vitro Skin Irritation Test Methods
type: reference
skill: irritation-predictor
version: 1.0.0
---

# In Vitro Skin Irritation Test Methods

## Regulatory Background

### Historical Context

Traditional skin irritation testing used animal models (Draize rabbit test). Due to ethical concerns and regulatory changes, validated in vitro alternatives are now required or preferred globally.

```
Timeline of Change

1944: Draize test introduced
         │
         ▼
2009: EU Cosmetics Regulation bans animal testing
         │
         ▼
2013: EU marketing ban on animal-tested cosmetics
         │
         ▼
2015: OECD TG 439 adopted
         │
         ▼
2019: OECD TG 439 updated (expanded protocols)
         │
         ▼
Present: Global adoption accelerating
```

### Regulatory Status

| Region | Status | Accepted Methods |
|--------|--------|------------------|
| EU | Mandatory in vitro | OECD TG 439 compliant |
| China | Transitioning | OECD methods accepted (2021+) |
| USA | Voluntary adoption | OECD methods preferred by FDA |
| Japan | Case-by-case | OECD methods accepted |
| Korea | Encouraged | OECD methods in MFDS guidance |
| Brazil | In progress | OECD adoption planned |

## OECD Test Guideline 439

### Overview

OECD TG 439 describes the Reconstructed human Epidermis (RhE) test method for skin irritation.

```
┌─────────────────────────────────────────────────────────────┐
│                    OECD TG 439 FRAMEWORK                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Principle: Measure cytotoxicity in 3D skin models          │
│                                                              │
│  Endpoint: Cell viability (MTT assay)                        │
│                                                              │
│  Classification:                                             │
│  • Viability ≤ 50% → Category 2 (Irritant)                  │
│  • Viability > 50% → No Category (Non-irritant)             │
│                                                              │
│  Exposure: 15-60 minutes depending on protocol               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Validated Test Methods (RhE Models)

#### 1. EpiDerm (MatTek Corporation)

```
┌─────────────────────────────────────────────────────────────┐
│                    EpiDerm SIT Protocol                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Model: EpiDerm EPI-200-SIT                                  │
│                                                              │
│  Structure:                                                  │
│  ┌──────────────────────────┐                               │
│  │ ═══════════════════════  │ Stratum Corneum               │
│  │ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ │ Stratum Granulosum           │
│  │ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ │ Stratum Spinosum             │
│  │ ● ● ● ● ● ● ● ● ● ● ● ● │ Stratum Basale               │
│  │ ═══════════════════════  │ Polycarbonate Membrane       │
│  │         Medium           │ Culture Medium               │
│  └──────────────────────────┘                               │
│                                                              │
│  Exposure Time: 60 minutes                                   │
│  Post-Incubation: 42 hours                                   │
│  Test Volume: 30 μL (liquids) or 25 mg (solids)             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**EpiDerm Protocol Steps:**

```
Day 0 (Pre-incubation)
    │
    ▼
Day 1 (Treatment)
┌────────────────────────────┐
│ Apply test substance       │ ← 60 min exposure
│ (30 μL or 25 mg)          │
└────────────────────────────┘
    │
    ▼
Rinse with PBS (25×)
    │
    ▼
Post-incubation (42 hours)
    │
    ▼
MTT Assay
┌────────────────────────────┐
│ 3 hours MTT incubation    │
│ Formazan extraction       │
│ OD measurement at 570 nm  │
└────────────────────────────┘
    │
    ▼
Calculate Viability (%)
```

#### 2. SkinEthic RhE (EPISKIN)

```
┌─────────────────────────────────────────────────────────────┐
│                   SkinEthic RhE Protocol                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Model: SkinEthic RhE/S/17                                   │
│                                                              │
│  Culture Surface: 0.5 cm²                                    │
│                                                              │
│  Exposure Conditions:                                        │
│  • Liquids/Semi-solids: 16 μL, 42 min exposure              │
│  • Solids: 16 mg, 42 min exposure                           │
│  • Surfactants: Additional dilution protocol available      │
│                                                              │
│  Post-Incubation: 42 hours at 37°C, 5% CO₂                  │
│                                                              │
│  Endpoint: MTT viability                                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### 3. LabCyte EPI-MODEL24 SIT

```
Japanese-developed model for TG 439

Specifications:
- Culture area: 0.3 cm²
- Exposure: 15 minutes
- Test volume: 25 μL (liquid) or 25 mg (solid)
- Post-incubation: 42 hours

Unique feature: Shorter exposure time (15 min vs 42-60 min)
```

#### 4. epiCS (CellSystems)

```
German-developed model

Specifications:
- Fully differentiated epidermis
- Exposure: 15 minutes
- Compatible with various endpoints
- Good reproducibility across laboratories
```

### Protocol Comparison

| Parameter | EpiDerm | SkinEthic | LabCyte | epiCS |
|-----------|---------|-----------|---------|-------|
| Exposure Time | 60 min | 42 min | 15 min | 15 min |
| Test Volume (liquid) | 30 μL | 16 μL | 25 μL | 50 μL |
| Test Amount (solid) | 25 mg | 16 mg | 25 mg | 25 mg |
| Post-Incubation | 42 hr | 42 hr | 42 hr | 42 hr |
| Culture Area | 0.6 cm² | 0.5 cm² | 0.3 cm² | 0.6 cm² |
| Replicates | 3 | 3 | 3 | 3 |

## MTT Assay Details

### Principle

MTT (3-(4,5-dimethylthiazol-2-yl)-2,5-diphenyltetrazolium bromide) measures mitochondrial activity:

```
            Living Cell                      Dead/Damaged Cell
       ┌─────────────────┐               ┌─────────────────┐
       │   Mitochondria  │               │   Mitochondria  │
       │   ┌─────────┐   │               │   ┌─────────┐   │
       │   │  Active │   │               │   │Inactive │   │
       │   │Reductase│   │               │   │Reductase│   │
       │   └────┬────┘   │               │   └─────────┘   │
       └────────┼────────┘               └─────────────────┘
                │
                ▼
        MTT (Yellow)                     MTT (Yellow)
        ┌──────────┐                     ┌──────────┐
        │ Soluble  │         →           │ No change│
        │ Tetrazole│                     │          │
        └────┬─────┘                     └──────────┘
             │
             ▼
        Formazan (Purple)
        ┌──────────┐
        │Insoluble │
        │ Crystal  │
        └──────────┘

Extract with isopropanol → Measure OD at 570 nm
```

### Calculation

```
                  OD₅₇₀ (Test Substance) - OD₅₇₀ (Blank)
% Viability = ───────────────────────────────────────────── × 100
              OD₅₇₀ (Negative Control) - OD₅₇₀ (Blank)

Classification:
• Viability ≤ 50%: Irritant (UN GHS Category 2)
• Viability > 50%: Non-irritant (No Category)
```

### Quality Control Criteria

| Control | Purpose | Acceptance Criteria |
|---------|---------|---------------------|
| Negative Control (NC) | Baseline viability | OD > 0.8 (typically 1.0-1.5) |
| Positive Control (PC) | Confirm sensitivity | Viability 0-40% |
| Blank | Background | Subtract from all readings |

**Standard Controls:**
- **Negative Control**: PBS, DPBS, or water
- **Positive Control**: 5% SDS (Sodium Dodecyl Sulfate)

## IL-1α Release Assay

### Complementary Endpoint

IL-1α release provides additional mechanistic information:

```
┌─────────────────────────────────────────────────────────────┐
│                IL-1α Release Mechanism                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Irritant Exposure                                           │
│        │                                                     │
│        ▼                                                     │
│  ┌──────────────────┐                                       │
│  │   Keratinocyte   │                                       │
│  │                  │                                       │
│  │  ┌────────────┐  │                                       │
│  │  │Pre-formed  │  │                                       │
│  │  │   IL-1α    │──┼──→ Released to medium                 │
│  │  └────────────┘  │         │                             │
│  │                  │         │                             │
│  │  Gene activation │         ▼                             │
│  │      │           │   Collect medium                      │
│  │      ▼           │         │                             │
│  │  ┌────────────┐  │         ▼                             │
│  │  │ New IL-1α  │  │   ELISA quantification               │
│  │  │ synthesis  │  │         │                             │
│  │  └────────────┘  │         ▼                             │
│  └──────────────────┘   pg/mL IL-1α                        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### IL-1α Protocol

```
Timeline:
0h        → Apply test substance
15-60min  → Remove test substance, rinse
+42h      → Collect medium
          → ELISA for IL-1α

Interpretation:
- Elevated IL-1α indicates inflammatory response
- Combined with MTT gives mechanism insight
- Not required by TG 439 but informative
```

## Extended Testing Protocols

### Surfactant-Specific Protocol

Surfactants may require modified testing:

```
Standard Protocol Issue:
Surfactants at high concentration → All models fail
                                    (100% cytotoxicity)

Solution: Dose-Response Protocol

┌──────────────────────────────────────────────────────────────┐
│             Surfactant Testing Protocol                       │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Test concentrations: 0.1%, 0.5%, 1%, 2%, 5%, 10%           │
│                                                               │
│  Generate dose-response curve:                                │
│                                                               │
│  Viability                                                    │
│  (%)                                                          │
│  100│●                                                        │
│     │  ●                                                      │
│   80│    ●                                                    │
│     │      ●                                                  │
│   60│        ●                                                │
│     │          ●                                              │
│   40│            ●                                            │
│     │              ●                                          │
│   20│                ●                                        │
│     │                  ●                                      │
│    0└───────────────────────────────                         │
│      0.1  0.5   1    2    5   10  Concentration (%)          │
│                                                               │
│  Calculate EC50 (concentration causing 50% viability loss)   │
│  Higher EC50 = less irritating surfactant                     │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### Time-Course Studies

For research purposes, kinetic assessment:

```
Sampling Points: 1h, 4h, 8h, 24h, 42h

Irritation kinetics reveal mechanism:
- Rapid onset (< 4h): Direct cytotoxicity
- Delayed onset (> 24h): Secondary inflammation
- Progressive: Cumulative damage
```

## Data Interpretation

### Classification Decision

```
                    TG 439 Classification Flow

                     MTT Viability Result
                            │
                            ▼
                    ┌───────────────┐
                    │ Viability ≤50%│
                    └───────┬───────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
        ┌──────────┐               ┌──────────┐
        │   YES    │               │    NO    │
        └────┬─────┘               └────┬─────┘
             │                          │
             ▼                          ▼
    ┌────────────────┐         ┌────────────────┐
    │  UN GHS Cat. 2 │         │  No Category   │
    │   (Irritant)   │         │(Non-Irritant)  │
    │                │         │                │
    │ H315: Causes   │         │ No hazard      │
    │skin irritation │         │classification  │
    └────────────────┘         └────────────────┘
```

### Prediction Model Performance

Based on validation studies:

| Model | Sensitivity | Specificity | Accuracy |
|-------|-------------|-------------|----------|
| EpiDerm | 100% | 74% | 86% |
| SkinEthic | 100% | 74% | 86% |
| LabCyte | 100% | 71% | 84% |
| epiCS | 100% | 80% | 89% |

**Note**: High sensitivity ensures irritants are identified; moderate specificity means some non-irritants may be false positives.

### False Positive Considerations

```
Potential False Positives:

1. Extreme pH
   pH < 2 or pH > 11.5 → Direct chemical damage
   May not reflect normal use conditions

2. Highly volatile substances
   May evaporate before full exposure
   Consider covered exposure

3. Colored/fluorescent substances
   May interfere with MTT reading
   Use alternative endpoints

4. Concentrated surfactants
   100% surfactant ≠ realistic exposure
   Use dose-response protocol
```

## Practical Considerations

### Sample Preparation

```
┌─────────────────────────────────────────────────────────────┐
│              Test Substance Preparation                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Physical State    Treatment                                 │
│  ─────────────────────────────────────────────────          │
│  Liquids          → Apply undiluted (unless specified)      │
│                                                              │
│  Viscous liquids  → Warm to room temperature                │
│                   → May need dilution for pipetting         │
│                                                              │
│  Solids           → Use as powder (25 mg)                   │
│                   → Moisten with water if specified         │
│                                                              │
│  Semi-solids      → Apply as-is                             │
│                   → Ensure complete coverage                │
│                                                              │
│  Formulations     → Test final product formulation          │
│                   → Note: pH adjustment may be needed       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Troubleshooting

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| Low NC viability | Poor tissue quality | Use fresh tissues |
| High PC viability | Dilution error | Verify SDS concentration |
| Variable results | Uneven application | Standardize application |
| Color interference | Pigmented substance | Use extraction control |
| Precipitate | Insoluble compound | Use appropriate vehicle |

## Cost and Timing

### Typical Testing Costs

| Component | Cost Range (USD) |
|-----------|-----------------|
| RhE tissues (6-pack) | $400-600 |
| MTT reagents | $50-100 |
| Controls and supplies | $50-100 |
| Labor (per test) | $200-400 |
| **Total per substance** | **$700-1,200** |

### Timeline

```
Standard Testing Timeline

Day -1: Receive tissues, pre-incubate
Day 0:  Treatment and exposure
Day 2:  MTT assay
Day 3:  Data analysis
Day 4:  Report generation

Total: 4-5 working days

Note: Shipping/logistics may add 2-3 days
```

## Integration with Other Tests

### Tiered Testing Strategy

```
┌─────────────────────────────────────────────────────────────┐
│              INTEGRATED TESTING STRATEGY                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Tier 1: In Silico Screening                                │
│          │                                                   │
│          ├─→ Clear non-irritant → Document, proceed         │
│          │                                                   │
│          └─→ Potential irritant or unclear                  │
│                    │                                         │
│                    ▼                                         │
│  Tier 2: In Vitro Testing (TG 439)                         │
│          │                                                   │
│          ├─→ Viability > 50% → Non-irritant                 │
│          │                                                   │
│          └─→ Viability ≤ 50% → Irritant classification      │
│                    │                                         │
│                    ▼                                         │
│  Tier 3: Additional Assessment                              │
│          │                                                   │
│          ├─→ Dose-response (quantitative)                   │
│          ├─→ IL-1α release (mechanism)                      │
│          └─→ Human volunteer patch test (if needed)         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Combined Endpoints

For comprehensive safety assessment:

| Endpoint | Test | Information Gained |
|----------|------|-------------------|
| Corrosion | TG 431 | Severe damage potential |
| Irritation | TG 439 | Reversible damage |
| Sensitization | TG 442 series | Allergic potential |
| Phototoxicity | TG 432 | Light-induced irritation |

## Report Requirements

### Minimum Documentation

```
Test Report Contents (TG 439 compliant):

1. Test Facility Information
   - Name, address, GLP status

2. Test Substance Information
   - Identity, purity, lot number
   - Physical state, pH, solubility

3. RhE Model Used
   - Name, lot number, supplier
   - Tissue quality check results

4. Protocol Details
   - Exposure time and conditions
   - Number of replicates
   - Deviations from protocol

5. Results
   - Individual tissue viabilities
   - Mean viability ± SD
   - Control results (NC, PC)

6. Conclusion
   - Classification outcome
   - Statement of GHS category
```

## References

1. OECD (2021). Test No. 439: In Vitro Skin Irritation: Reconstructed Human Epidermis Test Method
2. Kandarova H, et al. (2018). Toxicol In Vitro 50:299-310
3. Alépée N, et al. (2015). Toxicol In Vitro 29:1485-1491
4. MatTek Corporation. EpiDerm Skin Irritation Test Protocol
5. EPISKIN. SkinEthic RhE Skin Irritation Test Protocol
6. EURL ECVAM (2019). DB-ALM Protocol No. 135
