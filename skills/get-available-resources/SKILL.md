---
name: get-available-resources
description: This skill should be used at the start of any cosmetic formulation or analysis task to detect and report all available cosmetic skills, scripts, and reference materials. It scans the cosmetic-skills directory structure and generates a JSON file with resource information and task-specific recommendations. Use this skill before starting formulation work, ingredient analysis, regulatory checks, or any cosmetic-related task where you need to know which tools are available.
license: MIT license
metadata:
    skill-author: EVAS Cosmetic
    based-on: K-Dense Inc. claude-scientific-skills
---

# Get Available Resources

## Overview

Detect all available cosmetic skills, scripts, and reference materials within the cosmetic-skills directory. This skill automatically scans the skill library and generates recommendations for which skills to use based on the user's task type.

## When to Use This Skill

Use this skill proactively at the start of any cosmetic-related task:

- **Before formulation work**: Identify available calculators (HLB, pH, viscosity) and compatibility checkers
- **Before ingredient analysis**: Find available database skills (CosIng, KFDA, INCIDecoder, CosDNA)
- **Before regulatory checks**: Locate compliance tools for different markets (EU, Korea, US, China)
- **Before trend research**: Discover available market analysis and consumer insight skills
- **At project initialization**: Understand the full capability of the cosmetic skill library

**Example scenarios:**
- "Help me formulate a brightening serum" -> Use this skill to find formulation-calculator, kfda-ingredient, stability-predictor
- "Check if this ingredient is safe" -> Use this skill to find cosdna-analysis, ewg-skindeep, cir-safety
- "Analyze the full ingredient list" -> Use this skill to find incidecoder-analysis, cosing-database
- "Can I use this ingredient in EU?" -> Use this skill to find regulatory-compliance, cosing-database

## How This Skill Works

### Resource Detection

The skill runs `scripts/detect_cosmetic_resources.py` to automatically detect:

1. **Available Skills**
   - All skill folders with SKILL.md files
   - Skill categories (databases, packages, integrations, thinking, helpers)
   - Skill descriptions and purposes

2. **Available Scripts**
   - Python scripts in each skill's `scripts/` folder
   - Script purposes (fetching, analysis, calculation, conversion)
   - Script dependencies if specified

3. **Reference Materials**
   - Markdown reference files in each skill's `references/` folder
   - Data files and assets
   - Knowledge bases and lookup tables

4. **Skill Status**
   - Fully implemented (SKILL.md + scripts + references)
   - Partially implemented (SKILL.md + scripts OR references)
   - Documentation only (SKILL.md only)

### Output Format

The skill generates a `.cosmetic_resources.json` file containing:

```json
{
  "timestamp": "2025-01-16T10:30:00",
  "cosmetic_skills_path": "/path/to/cosmetic-skills",
  "summary": {
    "total_skills": 31,
    "fully_implemented": 15,
    "partially_implemented": 10,
    "documentation_only": 6
  },
  "categories": {
    "databases": {
      "count": 10,
      "skills": ["cosing-database", "kfda-ingredient", "incidecoder-analysis", ...]
    },
    "packages": {
      "count": 6,
      "skills": ["formulation-calculator", "stability-predictor", ...]
    },
    "integrations": {...},
    "thinking": {...},
    "helpers": {...}
  },
  "skills": {
    "cosing-database": {
      "category": "databases",
      "description": "EU 화장품 성분 DB (INCI명, 규제, 기능)",
      "status": "fully_implemented",
      "has_skill_md": true,
      "scripts": ["cosing_query.py"],
      "references": ["cosing_api.md", "inci_nomenclature.md", "eu_regulations.md"]
    },
    ...
  },
  "recommendations": {
    "formulation": {
      "primary": ["formulation-calculator", "ingredient-compatibility", "stability-predictor"],
      "secondary": ["skin-penetration", "rdkit-cosmetic"]
    },
    "safety_analysis": {
      "primary": ["cosdna-analysis", "ewg-skindeep", "cir-safety"],
      "secondary": ["incidecoder-analysis", "irritation-predictor"]
    },
    "ingredient_lookup": {
      "primary": ["cosing-database", "kfda-ingredient", "incidecoder-analysis"],
      "secondary": ["icid-database", "ifra-standards"]
    },
    "regulatory": {
      "primary": ["regulatory-compliance", "regulatory-checker"],
      "secondary": ["cosing-database", "kfda-ingredient"]
    },
    "market_analysis": {
      "primary": ["trend-analysis", "consumer-insight", "mintel-gnpd"],
      "secondary": ["product-positioning", "formulation-strategy"]
    }
  }
}
```

### Task-Based Recommendations

The skill generates context-aware recommendations for common cosmetic tasks:

**Formulation Tasks:**
- **Primary**: formulation-calculator, ingredient-compatibility, stability-predictor
- **Secondary**: skin-penetration, rdkit-cosmetic, hlb-calculator

**Safety Analysis Tasks:**
- **Primary**: cosdna-analysis, ewg-skindeep, cir-safety
- **Secondary**: incidecoder-analysis, irritation-predictor

**Ingredient Lookup Tasks:**
- **Primary**: cosing-database, kfda-ingredient, incidecoder-analysis
- **Secondary**: icid-database, ifra-standards

**Regulatory Tasks:**
- **Primary**: regulatory-compliance, regulatory-checker
- **Secondary**: cosing-database, kfda-ingredient (for region-specific rules)

**Market Analysis Tasks:**
- **Primary**: trend-analysis, consumer-insight, mintel-gnpd
- **Secondary**: product-positioning, formulation-strategy

## Usage Instructions

### Step 1: Run Resource Detection

Execute the detection script at the start of any cosmetic task:

```bash
python scripts/detect_cosmetic_resources.py
```

Optional arguments:
- `-o, --output <path>`: Specify custom output path (default: `.cosmetic_resources.json`)
- `-v, --verbose`: Print full resource information to stdout
- `--category <name>`: Filter by category (databases, packages, integrations, thinking, helpers)
- `--task <type>`: Get recommendations for specific task (formulation, safety, regulatory, trend)

### Step 2: Read and Apply Recommendations

After running detection, read the generated `.cosmetic_resources.json` file:

```python
import json

with open('.cosmetic_resources.json', 'r') as f:
    resources = json.load(f)

# Check available skills for a task
if 'formulation' in task_type:
    recommended_skills = resources['recommendations']['formulation']['primary']
    print(f"Use these skills: {recommended_skills}")

# Check if a specific skill is available
if 'incidecoder-analysis' in resources['skills']:
    skill = resources['skills']['incidecoder-analysis']
    if skill['status'] == 'fully_implemented':
        # Use the skill's scripts
        scripts = skill['scripts']
```

### Step 3: Use Recommended Skills

Based on recommendations, invoke the appropriate skills:

**For formulation work:**
```python
# Use formulation-calculator for HLB calculation
from cosmetic_skills.formulation_calculator.scripts.hlb_calculator import calculate_hlb

# Use ingredient-compatibility for checking
from cosmetic_skills.ingredient_compatibility.scripts.compatibility_check import check_compatibility
```

**For safety analysis:**
```python
# Use cosdna-analysis for safety scores
from cosmetic_skills.cosdna_analysis.scripts.fetch_cosdna import fetch_ingredient_safety

# Use incidecoder-analysis for ingredient functions
from cosmetic_skills.incidecoder_analysis.scripts.fetch_incidecoder import fetch_ingredient_info
```

## Dependencies

The detection script uses only Python standard library:
- `json`, `os`, `pathlib`, `datetime`

No external packages required.

## Skill Categories

### 1. cosmetic-databases (10 skills)
Data retrieval from cosmetic ingredient databases:
- CosIng, KFDA, EWG, CIR, INCIDecoder, CosDNA, Mintel, ICID, IFRA

### 2. cosmetic-packages (6 skills)
Calculation and analysis tools:
- Formulation calculator, Compatibility checker, Stability predictor, Penetration model, RDKit, Irritation predictor

### 3. cosmetic-integrations (4 skills)
External platform connections:
- Cosmily, UL Prospector, Mintel GNPD, Supplier Gateway

### 4. cosmetic-thinking (6 skills)
Strategic methodologies:
- Claim substantiation, Regulatory compliance, Consumer insight, Trend analysis, Product positioning, Formulation strategy

### 5. cosmetic-helpers (5 skills)
Utility tools:
- Context initialization, INCI converter, Regulatory checker, Concentration converter, Batch calculator

## Best Practices

1. **Run at project start**: Execute resource detection when beginning a new formulation or analysis project
2. **Check before using a skill**: Verify the skill's status (fully_implemented vs documentation_only)
3. **Use recommendations**: Follow task-based recommendations for optimal skill combinations
4. **Re-run after updates**: Resource detection should be re-run after adding new skills or scripts
5. **Cache results**: The `.cosmetic_resources.json` file can be cached and reused within a project

## Troubleshooting

**No skills detected:**
- Verify the cosmetic-skills directory path is correct
- Check that SKILL.md files exist in skill folders

**Missing scripts:**
- Some skills may have SKILL.md but no scripts (documentation_only status)
- Check the skill's status field before attempting to use scripts

**Import errors:**
- Scripts may have external dependencies (requests, beautifulsoup4, rdkit)
- Check each skill's SKILL.md for dependency requirements
