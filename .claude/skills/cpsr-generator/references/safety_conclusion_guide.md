# Safety Conclusion Decision Guide

## Overview

This guide provides the decision logic for reaching safety conclusions in CPSR Part B. Use this as a reference when assessing cosmetic product safety.

---

## 1. Overall Safety Decision Tree

```
START
  │
  ├─► Are all ingredients permitted under EU 1223/2009?
  │     NO → UNSAFE (Prohibited ingredient present)
  │     YES ↓
  │
  ├─► Do restricted ingredients comply with Annex III limits?
  │     NO → UNSAFE (Exceeds restriction limit)
  │     YES ↓
  │
  ├─► Do all assessed ingredients have MoS ≥ 100?
  │     │
  │     ├─ All MoS ≥ 100 → Continue assessment
  │     │
  │     ├─ Some MoS 50-100 → Requires justification
  │     │     └─► Can additional safety data justify lower MoS?
  │     │           NO → UNSAFE or reformulate
  │     │           YES → Continue with documentation
  │     │
  │     └─ Any MoS < 50 → UNSAFE (unacceptable risk)
  │
  ├─► Is microbiological quality acceptable?
  │     NO → UNSAFE (microbial risk)
  │     YES ↓
  │
  ├─► Is stability data adequate for claimed shelf life?
  │     NO → Request additional data or reduce shelf life
  │     YES ↓
  │
  ├─► Are there unacceptable sensitization risks?
  │     YES → UNSAFE or add appropriate warnings
  │     NO ↓
  │
  ├─► Are labelling requirements met?
  │     NO → SAFE with labelling modifications required
  │     YES ↓
  │
  └─► SAFE for intended use
```

---

## 2. MoS Interpretation Guide

### 2.1 Standard MoS Thresholds

| MoS Value | Interpretation | Action Required |
|-----------|----------------|-----------------|
| ≥ 100 | Safe | None - standard safety margin |
| 50 - 99 | May be acceptable | Justification required |
| 25 - 49 | Concerning | Strong justification or reformulate |
| < 25 | Unacceptable | Reformulate required |

### 2.2 Justifications for MoS < 100

When MoS is between 50-100, acceptable justifications include:

1. **Conservative NOAEL Used**
   - NOAEL from more sensitive species
   - NOAEL from more sensitive endpoint
   - Additional safety factors already applied

2. **Limited Dermal Absorption**
   - Measured data shows low absorption
   - High molecular weight (>500 Da)
   - Polymer with negligible penetration

3. **Local Effect Only**
   - Systemic toxicity not relevant
   - Effect is localized to application site
   - No systemic exposure expected

4. **Short Exposure Duration**
   - Rinse-off product
   - Infrequent use
   - Low retention factor

5. **Historical Safe Use**
   - Long history of safe use at this concentration
   - Post-market surveillance shows no issues
   - Wide use in similar products

### 2.3 Unacceptable Situations (Regardless of MoS)

- CMR category 1A or 1B substances (prohibited)
- Substances prohibited under Annex II
- Known strong sensitizers without warning
- Inadequate preservative efficacy
- Microbiologically contaminated

---

## 3. Ingredient-Specific Safety Considerations

### 3.1 Preservatives (Annex V)

| Check | Criteria | Action if Failed |
|-------|----------|------------------|
| Listed in Annex V | Must be listed | Remove or replace |
| Within concentration limit | ≤ maximum % | Reduce concentration |
| Appropriate for product type | Some restrictions by type | Verify applicability |
| Challenge test passes | Criterion A or B | Adjust system |

### 3.2 UV Filters (Annex VI)

| Check | Criteria | Action if Failed |
|-------|----------|------------------|
| Listed in Annex VI | Must be listed | Remove or replace |
| Within concentration limit | ≤ maximum % | Reduce concentration |
| Labelling requirements | Specific warnings | Add to label |
| Nanomaterial notification | If nano form | Notify 6 months prior |

### 3.3 Colorants (Annex IV)

| Check | Criteria | Action if Failed |
|-------|----------|------------------|
| Listed in Annex IV | Must be listed | Remove or replace |
| Appropriate field of application | Check column restrictions | Verify use type |
| Purity requirements | Meet specifications | Change supplier |
| Lake/salt form if specified | As per entry | Verify form |

### 3.4 Fragrances

| Check | Criteria | Action if Failed |
|-------|----------|------------------|
| IFRA compliance | Must comply | Reformulate fragrance |
| 26 allergens labelling | If > 0.001% (leave-on) | Declare on label |
| | If > 0.01% (rinse-off) | Declare on label |
| Prohibited substances | Annex II listed | Remove |
| Restricted substances | Annex III limits | Verify compliance |

---

## 4. Population-Specific Safety

### 4.1 Children Under 3 Years

**Products requiring special assessment:**
- Baby care products
- Products likely to be used on children

**Additional considerations:**
- Higher surface area to body weight ratio
- Skin barrier not fully developed
- Increased absorption potential
- Calculate exposure for 5 kg (3 months) or 8 kg (12 months)

**Decision factors:**
| Factor | Child-Safe Threshold |
|--------|---------------------|
| MoS | Consider ≥ 200 |
| Fragrance | Minimize or eliminate |
| Preservatives | Use gentlest effective system |
| pH | 5.5 - 7.0 preferred |
| Essential oils | Avoid or minimize |

### 4.2 Pregnant/Nursing Women

**Ingredients requiring assessment:**
- Retinoids (Vitamin A derivatives)
- Salicylic acid (>2%)
- Essential oils (certain types)
- Hydroquinone
- Formaldehyde releasers

**Decision:**
| Ingredient Present | Action |
|-------------------|--------|
| Retinol/Retinoids | Warning required or exclude |
| High-dose salicylic acid | Warning required |
| Certain essential oils | Warning or reformulate |

### 4.3 Sensitive Skin

**Sensitizer assessment:**
| Category | Examples | Risk Level |
|----------|----------|------------|
| Strong sensitizers | MI, MCI/MI, HICC | High - avoid or warn |
| Moderate sensitizers | Some fragrances | Medium - label required |
| Weak sensitizers | Most ingredients | Low - standard labelling |

**HRIPT requirement:**
- Recommended for leave-on products
- Essential if new ingredients used
- N ≥ 100 subjects preferred

---

## 5. Product Type-Specific Considerations

### 5.1 Leave-on vs Rinse-off

| Factor | Leave-on | Rinse-off |
|--------|----------|-----------|
| Retention Factor | 1.0 | 0.01 - 0.1 |
| Exposure duration | Continuous | Seconds to minutes |
| MoS requirement | Standard (≥100) | May accept lower |
| Preservative efficacy | Critical | Still required |
| Sensitizer concern | Higher | Lower |

### 5.2 Oral Exposure Products

**Products with oral exposure:**
- Lip products (lipstick, lip balm, lip gloss)
- Toothpaste, mouthwash
- Products near mouth area

**Additional requirements:**
- Oral toxicity data required
- Consider systemic effects
- Ingestion scenarios in exposure assessment
- Taste/flavor safety

### 5.3 Eye Area Products

**Special requirements:**
- Eye irritation data required
- Preservative selection critical
- pH range critical (6.5-7.5 preferred)
- Particle size considerations
- Antimicrobial efficacy essential

### 5.4 Spray Products (Inhalation)

**Additional assessment needed:**
- Particle size distribution
- Inhalation exposure calculation
- Respiratory irritation potential
- Not intended for inhalation statement

**Products requiring inhalation assessment:**
- Hair sprays
- Body sprays
- Powder products
- Aerosol products

---

## 6. Warning Requirements Decision Table

### 6.1 Mandatory Warnings by Ingredient

| Ingredient/Condition | Required Warning |
|---------------------|------------------|
| Fluoride compounds | "Children 6 years and under: Use pea-sized amount for supervised brushing" |
| Hydrogen peroxide >0.1% | "Contains hydrogen peroxide. Avoid contact with eyes" |
| Persulfates (hair bleach) | "Can cause allergic reaction. Wear gloves" |
| Strontium (depilatory) | "Keep away from eyes" |
| Sodium hydroxide (hair straightener) | "Causes severe burns. Keep away from children" |
| Aerosol products | "Pressurized container. Keep away from heat" |
| Products for children <3 | "Keep out of reach of children" |

### 6.2 Warning Decision Logic

```
Does product contain Annex III substance with mandatory warning?
  YES → Include exact warning text from Annex III
  NO ↓

Does product contain >0.001% fragrance allergen (leave-on)?
  YES → List allergen(s) in INCI list
  NO ↓

Is product for children under 3?
  YES → Add appropriate child-safety warnings
  NO ↓

Does clinical testing show any reactions?
  YES → Consider "Patch test recommended" or similar
  NO ↓

Are there foreseeable misuse scenarios?
  YES → Add preventive warnings
  NO → Standard labelling sufficient
```

---

## 7. Final Conclusion Wording Templates

### 7.1 Safe Product - Standard

> "Based on the evaluation of all available safety data, including the toxicological profile of all ingredients, the exposure assessment, stability and microbiological data, and clinical testing results, I conclude that the cosmetic product [PRODUCT NAME] is safe for human health when used under normal or reasonably foreseeable conditions of use, taking into account the presentation, labelling, and instructions for use provided."

### 7.2 Safe Product - With Conditions

> "The cosmetic product [PRODUCT NAME] is considered safe for human health subject to the following conditions:
> 1. [Condition 1]
> 2. [Condition 2]
> 
> These conditions must be communicated through appropriate labelling and instructions for use."

### 7.3 Safe Product - With Warnings

> "The cosmetic product [PRODUCT NAME] is considered safe for human health when the following mandatory warnings are included on the label:
> - [Warning 1]
> - [Warning 2]
> 
> Without these warnings, the product cannot be considered safe."

### 7.4 Conditionally Acceptable - Requires Action

> "The cosmetic product [PRODUCT NAME] cannot currently be assessed as safe due to:
> - [Issue 1]
> - [Issue 2]
> 
> The following actions are required before a positive safety conclusion can be reached:
> - [Required Action 1]
> - [Required Action 2]"

### 7.5 Unsafe Product

> "Based on the available data, the cosmetic product [PRODUCT NAME] cannot be considered safe for human health due to:
> - [Reason 1]
> - [Reason 2]
> 
> This product should not be placed on the market in its current formulation."

---

## 8. Documentation Requirements

### 8.1 Minimum Documentation for Safety Conclusion

| Document | Required | Notes |
|----------|----------|-------|
| Complete formula | Yes | With supplier specifications |
| MoS calculations | Yes | For all systemically relevant ingredients |
| Stability report | Yes | Minimum 3 months accelerated |
| Microbiological test | Yes | Plus challenge test |
| Safety data sheets | Yes | For all raw materials |
| NOAEL data sources | Yes | Referenced in assessment |
| Dermal absorption data | If available | Or justified default used |
| Clinical test report | Recommended | Required for novel products |

### 8.2 Record Keeping

- CPSR must be kept for 10 years after last batch
- Updates required when formulation changes
- Serious Undesirable Effects must be documented
- Annual review recommended

---

## 9. Red Flags - Immediate Safety Concerns

The following situations require immediate attention:

| Red Flag | Action |
|----------|--------|
| Annex II prohibited substance present | Stop - reformulate |
| Any MoS < 25 | Stop - reformulate |
| Failed challenge test | Stop - adjust preservation |
| Pathogen detected | Stop - investigate source |
| Stability failure before PAO | Stop - reformulate |
| Known allergen at high concentration | Reformulate or add strong warning |
| pH < 3 or > 10 (skin products) | Justify or reformulate |
| CMR substance without Article 15 exemption | Stop - remove |

---

## References

1. Regulation (EC) No 1223/2009 on cosmetic products
2. SCCS Notes of Guidance, 11th Revision (SCCS/1628/21)
3. SCCS opinions on specific ingredients
4. CIR safety assessments
5. ISO 11930 - Preservation efficacy testing
6. ISO 10993 - Biological evaluation (reference)

---

*This guide is for reference purposes. Safety assessors must exercise professional judgment for each specific assessment.*
