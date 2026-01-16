---
name: regulatory-checker
version: 1.0.0
category: cosmetic-helpers
description: Multi-country cosmetic regulatory compliance checking system
author: claude-cosmetic-skills
tools:
  - WebFetch
  - Read
  - Write
trigger_phrases:
  - "check regulatory compliance"
  - "regulatory check"
  - "export compliance"
  - "ingredient regulation"
  - "country regulation comparison"
  - "prohibited ingredients"
  - "labeling requirements"
  - "claim restrictions"
supported_countries:
  - Korea (MFDS)
  - EU (EC Regulation 1223/2009)
  - USA (FDA)
  - China (NMPA)
  - Japan (PMDA/MHLW)
  - ASEAN (ACD)
---

# Regulatory Checker Skill

Multi-country cosmetic regulatory compliance checking system for ingredient safety, labeling requirements, and claim restrictions.

## Purpose

This skill helps cosmetic formulators and regulatory affairs specialists:
- Check ingredient compliance across multiple countries
- Compare regulatory requirements between markets
- Generate compliance reports for export
- Track regulatory changes and updates
- Identify potential issues before product launch

## Skill Activation

Use this skill when:
- Planning to export cosmetics to new markets
- Checking ingredient compliance for formulations
- Comparing regulatory requirements between countries
- Preparing regulatory documentation
- Auditing existing products for compliance

## Core Capabilities

### 1. Multi-Country Ingredient Check

Check if ingredients are allowed, restricted, or prohibited in target markets.

**Example Request:**
```
Check regulatory compliance for these ingredients in Korea, EU, and China:
- Retinol 0.3%
- Salicylic Acid 2%
- Titanium Dioxide (nano) 25%
- Phenoxyethanol 1%
```

**Workflow:**
1. Parse ingredient list with concentrations
2. Check each ingredient against country databases
3. Identify restrictions and maximum limits
4. Generate compliance matrix
5. Flag potential issues

### 2. Export Compliance Assessment

Complete compliance assessment for exporting to a specific country.

**Example Request:**
```
Assess export compliance for my Korean sunscreen to EU market:
- SPF 50+ claim
- Contains: Octocrylene 10%, Avobenzone 3%, Titanium Dioxide (nano) 15%
- Claims: Waterproof, All-day protection
```

**Assessment Includes:**
- Ingredient compliance check
- UV filter limit verification
- Claim validity check
- Labeling requirement differences
- Required documentation list

### 3. Batch Ingredient Analysis

Process multiple ingredients or formulations at once.

**Example Request:**
```
Batch check these ingredients for Japan market:
[List of 50+ ingredients]
```

**Output:**
- Compliant ingredients list
- Restricted ingredients with limits
- Prohibited ingredients requiring reformulation
- Recommendations for alternatives

### 4. Regulatory Comparison Matrix

Compare regulations between countries for specific categories.

**Example Request:**
```
Compare UV filter regulations between Korea, EU, US, and Japan
```

**Matrix Output:**
| UV Filter | Korea | EU | US | Japan |
|-----------|-------|----|----|-------|
| Octocrylene | 10% | 10% | 10% | 10% |
| Avobenzone | 5% | 5% | 3% | 5% |
| ... | ... | ... | ... | ... |

## Reference Documents

This skill uses the following reference documents:

| Document | Description |
|----------|-------------|
| `references/multi_country_matrix.md` | Regulatory comparison matrix |
| `references/prohibited_lists.md` | Country-specific prohibited ingredients |
| `references/labeling_requirements.md` | Labeling requirements by country |

## Workflow Examples

### Workflow 1: New Product Export Check

```
User: I want to export my Korean whitening cream to China.
      Key ingredients: Niacinamide 5%, Arbutin 2%, Tranexamic Acid 3%

Claude:
1. [Check ingredient compliance for China]
   - Niacinamide 5%: ALLOWED (no limit for cosmetics)
   - Arbutin 2%: ALLOWED (max 7% as skin lightening agent)
   - Tranexamic Acid 3%: RESTRICTED (requires special registration)

2. [Check claim compliance]
   - "Whitening" claim: REQUIRES functional cosmetic registration in China
   - Processing time: 3-6 months for functional cosmetic

3. [Labeling requirements]
   - Chinese language labeling mandatory
   - NMPA registration number required
   - Responsible person in China required

4. [Recommendations]
   - Register as functional cosmetic for whitening claims
   - Prepare stability and efficacy data
   - Engage local regulatory agent
```

### Workflow 2: Multi-Country Launch Strategy

```
User: I'm launching a new anti-aging serum in Korea, EU, US, and Japan.
      Ingredients: Retinol 0.5%, Peptide Complex, Hyaluronic Acid

Claude:
1. [Generate compliance matrix]

| Country | Retinol 0.5% | Peptides | HA | Status |
|---------|--------------|----------|-----|--------|
| Korea | OK (cosmetic) | OK | OK | Ready |
| EU | OK (warning required) | OK | OK | Label update |
| US | OK | OK | OK | Ready |
| Japan | OK (quasi-drug?) | OK | OK | Review needed |

2. [Country-specific notes]
   - EU: Requires warning statement for retinol products
   - Japan: High retinol may require quasi-drug classification
   - US: No specific restrictions

3. [Action items]
   - Add EU warning statement to labels
   - Consult Japan regulatory expert for classification
   - Prepare country-specific claims
```

### Workflow 3: Prohibited Ingredient Alert

```
User: Check if my formulation is OK for EU export:
      - Hydroquinone 2%
      - Mercury compounds (preservative)
      - Formaldehyde 0.05%

Claude:
[CRITICAL COMPLIANCE ISSUES DETECTED]

| Ingredient | Status | Action Required |
|------------|--------|-----------------|
| Hydroquinone 2% | PROHIBITED | Remove from formulation |
| Mercury compounds | PROHIBITED | Remove immediately |
| Formaldehyde 0.05% | RESTRICTED | Below 0.05% limit but labeling required |

[Severity: HIGH - Do not export as-is]

Recommendations:
1. Replace Hydroquinone with: Arbutin, Niacinamide, or Alpha-Arbutin
2. Remove all mercury compounds (banned in cosmetics)
3. Add formaldehyde warning if concentration causes release
```

## Claim Restriction Checking

### Prohibited Claims by Region

**EU:**
- No medical claims (treats, cures, prevents disease)
- No misleading efficacy claims
- Must have substantiation for all claims

**US:**
- No drug claims without FDA approval
- Structure/function claims allowed
- Must not be misleading

**China:**
- Functional claims require registration
- No exaggerated efficacy claims
- Claims must match registered product type

**Korea:**
- Functional claims for registered categories only
- No medical claims
- Comparative claims restricted

### Example Claim Analysis

```
Claim: "Clinically proven to reduce wrinkles by 50%"

| Country | Status | Notes |
|---------|--------|-------|
| Korea | Conditional | Needs clinical data, functional cosmetic |
| EU | Allowed | With substantiation evidence |
| US | Allowed | With clinical evidence |
| China | Review needed | May require functional registration |
| Japan | Conditional | Quasi-drug if efficacy claim |
```

## Regulatory Change Tracking

The skill can help track recent regulatory changes:

```
User: What are recent regulatory changes for sunscreens in EU?

Claude:
Recent EU Sunscreen Regulation Updates (2024-2025):

1. [Nano material labeling] - Strengthened requirements
   - All nano ingredients must be clearly labeled
   - Safety assessment documentation required

2. [UV filter restrictions] - Under review
   - Several filters under endocrine disruptor evaluation
   - Potential restrictions on: Octocrylene, Homosalate

3. [SPF claim substantiation]
   - ISO methods required for testing
   - Updated water resistance testing protocols

[Recommendation: Monitor SCCS opinions for upcoming changes]
```

## Batch Processing Commands

For large-scale compliance checking:

```python
# Use the batch checker script
python regulatory_batch_checker.py \
    --input ingredients.csv \
    --countries Korea,EU,US,China,Japan \
    --output compliance_report.xlsx
```

## Output Formats

### Compliance Report Structure

```markdown
# Regulatory Compliance Report

## Product Information
- Product Name: [Name]
- Category: [Category]
- Target Markets: [Countries]

## Ingredient Compliance Summary
| Status | Count |
|--------|-------|
| Compliant | XX |
| Restricted | XX |
| Prohibited | XX |

## Detailed Findings
[Per-ingredient analysis]

## Action Items
[Required changes]

## Recommendations
[Expert guidance]
```

## Integration with Other Skills

This skill works well with:

- `formulation-assistant`: Get reformulation suggestions
- `ingredient-analyzer`: Deep ingredient safety analysis
- `labeling-generator`: Generate compliant labels
- `claim-validator`: Validate marketing claims

## Important Notes

1. **Regulatory Disclaimer**: This skill provides guidance based on known regulations. Always verify with official sources and regulatory experts before export.

2. **Update Frequency**: Regulations change frequently. Cross-check with official databases for critical decisions.

3. **Expert Consultation**: For complex cases or new markets, consult with registered regulatory affairs professionals.

4. **Documentation**: Keep records of all compliance checks for regulatory audits.

## Quick Reference Commands

| Command | Description |
|---------|-------------|
| `check [ingredient] for [country]` | Single ingredient check |
| `compare regulations [category] [countries]` | Regulation comparison |
| `export compliance [product] to [country]` | Full export assessment |
| `batch check [file] for [countries]` | Batch processing |
| `claim check [claim] for [countries]` | Claim validity check |
| `recent changes [country] [category]` | Regulatory updates |

## External Resources

- Korea MFDS: https://mfds.go.kr
- EU Cosmetics Regulation: https://ec.europa.eu/growth/sectors/cosmetics
- US FDA: https://www.fda.gov/cosmetics
- China NMPA: https://www.nmpa.gov.cn
- Japan PMDA: https://www.pmda.go.jp
- ASEAN Cosmetic Directive: https://asean.org
