---
name: ingredient-efficacy-analyzer
description: Analyze cosmetic ingredient lists to generate comprehensive efficacy reports. Automatically categorizes active ingredients, explains mechanisms of action, provides clinical evidence summaries, analyzes formulation synergies, and generates professional technical reports suitable for marketing claims, R&D documentation, and consumer education. Integrates with INCIDecoder, CosDNA, and scientific literature databases.
allowed-tools: [Read, Write, Edit, Bash]
license: MIT License
metadata:
    skill-author: EVAS Cosmetic
---

# Ingredient Efficacy Analyzer

## Overview

The Ingredient Efficacy Analyzer transforms a product's full ingredient list into a comprehensive technical efficacy report. This skill automatically categorizes ingredients by function, explains scientific mechanisms, cites clinical evidence, and identifies formulation synergies to support marketing claims and R&D documentation.

**Key Capabilities:**
- Automatic ingredient categorization by efficacy function
- Mechanism of action explanation for active ingredients
- Clinical evidence summary and citation
- Formulation synergy analysis
- Competitive differentiation identification
- Multi-language report generation (KR/EN)

## When to Use This Skill

Use this skill when:
- Developing product claims and marketing materials
- Creating technical documentation for sales teams
- Preparing R&D formulation justification
- Generating consumer-facing ingredient explanations
- Analyzing competitor product formulations
- Supporting regulatory claim substantiation

---

## Ingredient Categorization System

### Primary Efficacy Categories

```python
EFFICACY_CATEGORIES = {
    "brightening": {
        "description": "Skin brightening and hyperpigmentation reduction",
        "mechanisms": ["Tyrosinase inhibition", "Melanin transfer inhibition", "Antioxidant"],
        "key_ingredients": [
            "NIACINAMIDE", "ARBUTIN", "ALPHA-ARBUTIN", "TRANEXAMIC ACID",
            "ASCORBIC ACID", "ASCORBYL GLUCOSIDE", "KOJIC ACID",
            "GLUTATHIONE", "LICORICE ROOT EXTRACT"
        ],
        "claims": ["미백", "Brightening", "Dark spot reduction", "Even skin tone"]
    },
    
    "anti_aging": {
        "description": "Wrinkle reduction and skin rejuvenation",
        "mechanisms": ["Collagen synthesis", "ECM remodeling", "Cell turnover", "Antioxidant"],
        "key_ingredients": [
            "RETINOL", "RETINYL PALMITATE", "ADENOSINE", "PEPTIDES",
            "BAKUCHIOL", "RESVERATROL", "COENZYME Q10", "NAD+"
        ],
        "claims": ["주름개선", "Anti-wrinkle", "Firming", "Elasticity improvement"]
    },
    
    "hydrating": {
        "description": "Skin hydration and moisture retention",
        "mechanisms": ["Humectant", "Occlusive", "Emollient", "NMF replenishment"],
        "key_ingredients": [
            "HYALURONIC ACID", "SODIUM HYALURONATE", "GLYCERIN",
            "PANTHENOL", "BETAINE", "TREHALOSE", "SQUALANE"
        ],
        "claims": ["보습", "Hydrating", "Moisturizing", "Plumping"]
    },
    
    "barrier_repair": {
        "description": "Skin barrier strengthening and repair",
        "mechanisms": ["Lipid replenishment", "Ceramide synthesis", "Tight junction support"],
        "key_ingredients": [
            "CERAMIDE NP", "CERAMIDE AP", "CERAMIDE EOP",
            "CHOLESTEROL", "PHYTOSPHINGOSINE", "FATTY ACIDS",
            "MADECASSOSIDE", "CENTELLA ASIATICA"
        ],
        "claims": ["장벽강화", "Barrier repair", "Soothing", "Sensitive skin care"]
    },
    
    "antioxidant": {
        "description": "Free radical protection and oxidative stress reduction",
        "mechanisms": ["ROS scavenging", "Metal chelation", "Enzyme activation"],
        "key_ingredients": [
            "TOCOPHEROL", "ASCORBIC ACID", "FERULIC ACID",
            "RESVERATROL", "GREEN TEA EXTRACT", "ASTAXANTHIN",
            "SUPEROXIDE DISMUTASE", "GLUTATHIONE"
        ],
        "claims": ["항산화", "Antioxidant", "Environmental protection", "Anti-pollution"]
    },
    
    "soothing": {
        "description": "Anti-inflammatory and skin calming",
        "mechanisms": ["COX inhibition", "Cytokine modulation", "Histamine blocking"],
        "key_ingredients": [
            "ALLANTOIN", "BISABOLOL", "PANTHENOL", "ALOE VERA",
            "CENTELLA ASIATICA", "CHAMOMILE EXTRACT", "BETA-GLUCAN",
            "MADECASSOSIDE", "ASIATICOSIDE"
        ],
        "claims": ["진정", "Soothing", "Calming", "Anti-redness"]
    },
    
    "exfoliating": {
        "description": "Cell turnover and surface renewal",
        "mechanisms": ["Keratolytic", "Desmosome dissolution", "pH modulation"],
        "key_ingredients": [
            "GLYCOLIC ACID", "LACTIC ACID", "SALICYLIC ACID",
            "MANDELIC ACID", "PHA", "PAPAIN", "BROMELAIN"
        ],
        "claims": ["각질제거", "Exfoliating", "Resurfacing", "Pore refining"]
    },
    
    "sebum_control": {
        "description": "Oil control and pore minimization",
        "mechanisms": ["5-alpha reductase inhibition", "Astringent", "Sebocyte regulation"],
        "key_ingredients": [
            "NIACINAMIDE", "ZINC PCA", "SALICYLIC ACID",
            "WITCH HAZEL", "KAOLIN", "BENTONITE"
        ],
        "claims": ["피지조절", "Oil control", "Mattifying", "Pore minimizing"]
    },
    
    "regenerating": {
        "description": "Wound healing and tissue repair",
        "mechanisms": ["Growth factor stimulation", "Angiogenesis", "Cell proliferation"],
        "key_ingredients": [
            "EGF", "PDRN", "SNAIL SECRETION FILTRATE",
            "CENTELLA ASIATICA", "ALLANTOIN", "PANTHENOL",
            "MADECASSOSIDE", "COPPER PEPTIDE"
        ],
        "claims": ["재생", "Regenerating", "Healing", "Recovery"]
    },
    
    "microbiome": {
        "description": "Skin microbiome support",
        "mechanisms": ["Prebiotic", "Probiotic", "Postbiotic", "pH balancing"],
        "key_ingredients": [
            "LACTOBACILLUS FERMENT", "BIFIDA FERMENT LYSATE",
            "GALACTOMYCES FERMENT FILTRATE", "SACCHAROMYCES FERMENT",
            "INULIN", "ALPHA-GLUCAN OLIGOSACCHARIDE"
        ],
        "claims": ["마이크로바이옴", "Microbiome balance", "Skin flora support"]
    }
}
```

### Functional Categories

```python
FUNCTIONAL_CATEGORIES = {
    "actives": {
        "description": "Primary active ingredients with proven efficacy",
        "typical_range": "0.1% - 10%"
    },
    "delivery_systems": {
        "description": "Ingredients that enhance active penetration",
        "examples": ["Liposomes", "Cyclodextrins", "Nanocarriers"]
    },
    "base_ingredients": {
        "description": "Formulation foundation (water, oils, emulsifiers)",
        "examples": ["AQUA", "Oils", "Emulsifiers", "Thickeners"]
    },
    "preservatives": {
        "description": "Microbial growth prevention",
        "examples": ["PHENOXYETHANOL", "ETHYLHEXYLGLYCERIN"]
    },
    "sensory_modifiers": {
        "description": "Texture, scent, and feel enhancement",
        "examples": ["Silicones", "Fragrance", "Film formers"]
    },
    "stabilizers": {
        "description": "Formula stability and ingredient protection",
        "examples": ["Antioxidants", "Chelators", "pH adjusters"]
    }
}
```

---

## Ingredient Analysis Process

### Step 1: Parse Ingredient List

**Input formats accepted:**
- INCI list (comma-separated)
- Full ingredient list from product label
- JSON/CSV with concentrations (if available)

```python
# Example input
ingredient_list = """
Water, Glycerin, Niacinamide, Butylene Glycol, 1,2-Hexanediol, 
Sodium Hyaluronate, Adenosine, Panthenol, Allantoin, 
Centella Asiatica Extract, Ceramide NP, Tocopherol, 
Carbomer, Arginine, Disodium EDTA, Phenoxyethanol
"""
```

### Step 2: Ingredient Identification

For each ingredient:
1. Normalize INCI name
2. Lookup in ingredient database
3. Retrieve: CAS number, function, efficacy category, typical concentration

### Step 3: Efficacy Categorization

Assign each active ingredient to efficacy categories:
```
NIACINAMIDE → [brightening, sebum_control, barrier_repair]
ADENOSINE → [anti_aging]
CENTELLA ASIATICA EXTRACT → [soothing, barrier_repair, regenerating]
CERAMIDE NP → [barrier_repair, hydrating]
```

### Step 4: Mechanism Analysis

For each key active:
- Primary mechanism of action
- Secondary mechanisms
- Target pathway/receptor
- Expected timeline for effects

### Step 5: Synergy Analysis

Identify beneficial combinations:
```
NIACINAMIDE + HYALURONIC ACID → Enhanced hydration
VITAMIN C + VITAMIN E + FERULIC ACID → Synergistic antioxidant (C E Ferulic formula)
CERAMIDES + CHOLESTEROL + FATTY ACIDS → Optimal 3:1:1 ratio for barrier
RETINOL + PEPTIDES → Complementary anti-aging
```

### Step 6: Report Generation

Generate comprehensive report with:
- Executive summary
- Ingredient categorization table
- Active ingredient deep dives
- Synergy analysis
- Competitive positioning
- Claim support summary

---

## Output Report Structure

### 1. Executive Summary

```markdown
## Executive Summary

**Product**: [Product Name]
**Primary Benefits**: [Top 3 efficacy categories]
**Key Differentiators**: [Unique ingredients or combinations]
**Target Consumer**: [Skin type, concerns, demographics]

### Efficacy Score Card
| Category | Score | Key Ingredients |
|----------|-------|-----------------|
| Brightening | ★★★★☆ | Niacinamide 4%, Tranexamic Acid |
| Hydrating | ★★★★★ | HA, Glycerin, Panthenol |
| Anti-aging | ★★★☆☆ | Adenosine, Peptides |
```

### 2. Full Ingredient Analysis

```markdown
## Full Ingredient Analysis

### Active Ingredients (High-Impact)

#### NIACINAMIDE (Vitamin B3)
- **Concentration**: Typically 2-5% (estimated 4% based on position)
- **Primary Function**: Brightening, Barrier Support
- **Mechanism**: 
  - Inhibits melanosome transfer to keratinocytes
  - Increases ceramide synthesis
  - Reduces sebum production
- **Clinical Evidence**:
  - 5% Niacinamide: 68% reduction in hyperpigmentation (12 weeks)
  - 2% Niacinamide: Significant improvement in skin texture
- **Synergies in Formula**: Works with Hyaluronic Acid for enhanced hydration

#### ADENOSINE
- **Concentration**: Typically 0.04% (regulatory minimum for anti-wrinkle claim in Korea)
- **Primary Function**: Anti-wrinkle
- **Mechanism**: 
  - Stimulates fibroblast activity
  - Increases collagen and elastin synthesis
  - Anti-inflammatory via A2A receptor
- **Regulatory Note**: MFDS-approved functional ingredient for 주름개선
```

### 3. Formulation Synergy Analysis

```markdown
## Formulation Synergy Analysis

### Identified Synergistic Combinations

#### 1. Barrier Repair Complex
**Ingredients**: Ceramide NP + Cholesterol (if present) + Fatty Acids
**Synergy Type**: Biomimetic lipid replacement
**Expected Benefit**: 
- Optimal skin barrier lipid ratio mimics natural stratum corneum
- Enhanced barrier repair vs. single ceramide

#### 2. Multi-functional Soothing
**Ingredients**: Centella Asiatica + Panthenol + Allantoin
**Synergy Type**: Multi-pathway calming
**Expected Benefit**:
- Centella: Anti-inflammatory (madecassoside)
- Panthenol: Wound healing, hydration
- Allantoin: Cell proliferation
- Combined effect: Comprehensive skin calming
```

### 4. Competitive Differentiation

```markdown
## Competitive Positioning

### Unique Formulation Aspects

1. **NAD+ Inclusion**: Emerging anti-aging ingredient with cellular energy focus
2. **PDRN (Salmon DNA)**: Premium regenerative ingredient popular in K-beauty
3. **Triple Ceramide System**: Complete barrier repair vs. single ceramide

### Comparison Matrix

| Feature | This Product | Competitor A | Competitor B |
|---------|--------------|--------------|--------------|
| Niacinamide | ✓ (High) | ✓ (Low) | ✗ |
| Multi-Ceramide | ✓ | ✗ | ✓ |
| Peptide Complex | ✓ (9 types) | ✓ (3 types) | ✗ |
| Fermented Ingredients | ✓ | ✗ | ✓ |
```

### 5. Claim Support Summary

```markdown
## Claim Support Summary

### Supported Claims

| Claim | Supporting Ingredients | Evidence Level |
|-------|----------------------|----------------|
| "Brightening" | Niacinamide, Tranexamic Acid | ★★★★★ Clinical |
| "Anti-wrinkle" | Adenosine, Peptides | ★★★★☆ Clinical |
| "Hydrating" | Hyaluronic Acid, Glycerin | ★★★★★ Clinical |
| "Soothing" | Centella, Allantoin | ★★★★☆ Clinical |
| "Barrier repair" | Ceramides, Panthenol | ★★★★☆ Clinical |

### Claims Requiring Caution

| Claim | Issue | Recommendation |
|-------|-------|----------------|
| "Anti-aging" | Generic term | Use specific claims (wrinkle, firmness) |
| "Regenerating" | Medical implication | Avoid or use carefully |
```

---

## Ingredient Database Structure

### Database Schema

```python
INGREDIENT_DATABASE = {
    "NIACINAMIDE": {
        "inci_name": "NIACINAMIDE",
        "common_names": ["Vitamin B3", "Nicotinamide", "니아신아마이드"],
        "cas_number": "98-92-0",
        "categories": ["brightening", "sebum_control", "barrier_repair"],
        "mechanism": {
            "primary": "Inhibits melanosome transfer",
            "secondary": ["Ceramide synthesis", "Sebum regulation", "Anti-inflammatory"]
        },
        "typical_concentration": {
            "min": 2.0,
            "max": 10.0,
            "optimal": 5.0
        },
        "clinical_evidence": [
            {
                "claim": "Hyperpigmentation reduction",
                "concentration": 5.0,
                "duration_weeks": 12,
                "result": "68% improvement",
                "reference": "Hakozaki et al., 2002"
            }
        ],
        "synergies": ["HYALURONIC ACID", "RETINOL", "VITAMIN C"],
        "incompatibilities": ["Low pH (<4) reduces stability"],
        "regulatory": {
            "EU": {"status": "Allowed", "limit": None},
            "Korea": {"status": "Functional", "claim": "미백"}
        }
    },
    # ... more ingredients
}
```

---

## Scripts

### Main Analysis Script

```bash
# Basic usage
python scripts/analyze_ingredients.py "Water, Glycerin, Niacinamide..."

# With output file
python scripts/analyze_ingredients.py input_inci.txt -o analysis_report.md

# Korean language output
python scripts/analyze_ingredients.py input_inci.txt --lang ko

# Include competitor comparison
python scripts/analyze_ingredients.py input_inci.txt \
  --compare competitor1.txt competitor2.txt

# Full pipeline
python scripts/efficacy_report_pipeline.py \
  --product-name "Brightening Serum" \
  --formula formula.csv \
  --output-format pdf \
  -o report/
```

### Available Scripts

- `scripts/analyze_ingredients.py` - Main ingredient analysis
- `scripts/categorize_efficacy.py` - Efficacy categorization
- `scripts/find_synergies.py` - Synergy detection
- `scripts/generate_report.py` - Report generation
- `scripts/compare_formulas.py` - Competitive comparison
- `scripts/efficacy_report_pipeline.py` - Complete pipeline

---

## Resources

### Reference Files
- `references/ingredient_database.json` - Comprehensive ingredient data
- `references/efficacy_mechanisms.md` - Mechanism explanations
- `references/clinical_evidence.md` - Clinical study summaries
- `references/synergy_combinations.md` - Known beneficial combinations
- `references/claim_guidelines.md` - Claim language guidance

### Template Assets
- `assets/efficacy_report_template.md` - Full report template
- `assets/ingredient_card_template.md` - Individual ingredient analysis
- `assets/synergy_analysis_template.md` - Synergy section template
- `assets/executive_summary_template.md` - Summary template

---

## Integration with Other Skills

This skill integrates with:
- **incidecoder-analysis**: Fetch ingredient data from INCIDecoder
- **cosdna-analysis**: Get safety/irritation scores
- **cosing-database**: EU regulatory status
- **kfda-ingredient**: Korean functional cosmetics status
- **claim-substantiation**: Align claims with evidence
- **cpsr-generator**: Provide ingredient data for safety reports

---

## Limitations

1. **Concentration Estimation**: Without actual formula %, concentrations are estimated from ingredient order (descending by amount as per labeling rules)

2. **Database Coverage**: Not all ingredients have complete mechanism/evidence data

3. **Clinical Evidence**: Cited studies may use different concentrations or formulations

4. **Synergy Prediction**: Theoretical synergies may not always manifest in specific formulations

5. **Regulatory Accuracy**: Regulations change; always verify current requirements
