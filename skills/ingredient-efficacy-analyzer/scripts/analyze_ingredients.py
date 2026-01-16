#!/usr/bin/env python3
"""
Cosmetic Ingredient Efficacy Analyzer

Analyzes ingredient lists to generate comprehensive efficacy reports.
- Categorizes ingredients by function and efficacy
- Explains mechanisms of action
- Identifies synergistic combinations
- Generates professional reports

Usage:
    python analyze_ingredients.py "Water, Glycerin, Niacinamide..." -o report.md
    python analyze_ingredients.py ingredients.txt --format json
"""

import json
import argparse
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, asdict, field
from datetime import datetime


# Comprehensive ingredient database
INGREDIENT_DATABASE = {
    # Brightening
    "NIACINAMIDE": {
        "common_names": ["Vitamin B3", "Nicotinamide", "니아신아마이드"],
        "categories": ["brightening", "sebum_control", "barrier_repair"],
        "mechanism": {
            "primary": "Inhibits melanosome transfer to keratinocytes",
            "secondary": [
                "Ceramide synthesis stimulation",
                "Sebum production regulation",
                "Anti-inflammatory",
            ],
        },
        "typical_concentration": {"min": 2.0, "max": 10.0, "optimal": 5.0},
        "evidence_level": "Strong clinical evidence",
        "claims_supported": [
            "미백",
            "Brightening",
            "Pore minimizing",
            "Barrier support",
        ],
        "synergies": ["HYALURONIC ACID", "ZINC", "PEPTIDES"],
        "precautions": "May cause flushing at high concentrations in sensitive individuals",
    },
    "ARBUTIN": {
        "common_names": ["Alpha-Arbutin", "Beta-Arbutin", "알부틴"],
        "categories": ["brightening"],
        "mechanism": {
            "primary": "Tyrosinase inhibition (competitive)",
            "secondary": ["Melanin synthesis reduction"],
        },
        "typical_concentration": {"min": 0.5, "max": 2.0, "optimal": 1.0},
        "evidence_level": "Strong clinical evidence",
        "claims_supported": ["미백", "Brightening", "Dark spot reduction"],
        "synergies": ["VITAMIN C", "NIACINAMIDE"],
        "precautions": "Alpha-arbutin is more stable and effective than beta form",
    },
    "TRANEXAMIC ACID": {
        "common_names": ["TXA", "트라넥삼산"],
        "categories": ["brightening"],
        "mechanism": {
            "primary": "Plasmin inhibition reducing keratinocyte-melanocyte interaction",
            "secondary": ["Anti-inflammatory", "Vascular permeability reduction"],
        },
        "typical_concentration": {"min": 2.0, "max": 5.0, "optimal": 3.0},
        "evidence_level": "Strong clinical evidence",
        "claims_supported": [
            "미백",
            "Melasma improvement",
            "Post-inflammatory hyperpigmentation",
        ],
        "synergies": ["NIACINAMIDE", "VITAMIN C"],
        "precautions": "Originally developed for medical use; excellent safety profile topically",
    },
    "ASCORBIC ACID": {
        "common_names": ["Vitamin C", "L-Ascorbic Acid", "비타민C"],
        "categories": ["brightening", "antioxidant", "anti_aging"],
        "mechanism": {
            "primary": "Tyrosinase inhibition and melanin reduction",
            "secondary": [
                "Collagen synthesis",
                "Antioxidant protection",
                "Photoprotection",
            ],
        },
        "typical_concentration": {"min": 5.0, "max": 20.0, "optimal": 15.0},
        "evidence_level": "Strong clinical evidence",
        "claims_supported": ["미백", "Brightening", "Anti-aging", "Antioxidant"],
        "synergies": ["VITAMIN E", "FERULIC ACID"],
        "precautions": "Unstable; requires low pH formulation; may irritate sensitive skin",
    },
    # Anti-aging
    "RETINOL": {
        "common_names": ["Vitamin A", "레티놀"],
        "categories": ["anti_aging", "exfoliating"],
        "mechanism": {
            "primary": "Retinoic acid receptor activation increasing cell turnover",
            "secondary": ["Collagen synthesis", "ECM remodeling", "Sebum regulation"],
        },
        "typical_concentration": {"min": 0.025, "max": 1.0, "optimal": 0.3},
        "evidence_level": "Gold standard clinical evidence",
        "claims_supported": ["주름개선", "Anti-wrinkle", "Skin renewal", "Acne"],
        "synergies": ["PEPTIDES", "HYALURONIC ACID"],
        "precautions": "Can cause irritation; sun sensitivity; avoid during pregnancy",
    },
    "ADENOSINE": {
        "common_names": ["아데노신"],
        "categories": ["anti_aging"],
        "mechanism": {
            "primary": "A2A receptor activation stimulating fibroblast activity",
            "secondary": ["Collagen/elastin synthesis", "Anti-inflammatory"],
        },
        "typical_concentration": {"min": 0.04, "max": 0.1, "optimal": 0.04},
        "evidence_level": "Regulatory approved (Korea MFDS)",
        "claims_supported": ["주름개선", "Anti-wrinkle", "Firming"],
        "synergies": ["PEPTIDES", "RETINOL"],
        "precautions": "MFDS approved functional ingredient at 0.04%+",
    },
    "PEPTIDES": {
        "common_names": ["Acetyl Hexapeptide", "Palmitoyl Tripeptide", "펩타이드"],
        "categories": ["anti_aging", "firming"],
        "mechanism": {
            "primary": "Signal peptides stimulating collagen synthesis",
            "secondary": ["Neurotransmitter modulation", "ECM support"],
        },
        "typical_concentration": {"min": 0.001, "max": 0.5, "optimal": 0.1},
        "evidence_level": "Moderate to strong evidence",
        "claims_supported": ["Anti-wrinkle", "Firming", "Lifting"],
        "synergies": ["ADENOSINE", "VITAMIN C"],
        "precautions": "Various types with different mechanisms; concentration matters",
    },
    # Hydrating
    "HYALURONIC ACID": {
        "common_names": ["Sodium Hyaluronate", "HA", "히알루론산"],
        "categories": ["hydrating"],
        "mechanism": {
            "primary": "Hygroscopic water binding (up to 1000x weight)",
            "secondary": ["Skin plumping", "Barrier support"],
        },
        "typical_concentration": {"min": 0.1, "max": 2.0, "optimal": 1.0},
        "evidence_level": "Strong clinical evidence",
        "claims_supported": ["보습", "Hydrating", "Plumping"],
        "synergies": ["GLYCERIN", "CERAMIDES", "NIACINAMIDE"],
        "precautions": "Multiple molecular weights provide different benefits",
    },
    "GLYCERIN": {
        "common_names": ["Glycerol", "글리세린"],
        "categories": ["hydrating"],
        "mechanism": {
            "primary": "Humectant drawing water from dermis and environment",
            "secondary": ["Barrier support", "Skin softening"],
        },
        "typical_concentration": {"min": 1.0, "max": 10.0, "optimal": 5.0},
        "evidence_level": "Strong clinical evidence",
        "claims_supported": ["보습", "Hydrating", "Moisturizing"],
        "synergies": ["HYALURONIC ACID", "CERAMIDES"],
        "precautions": "Very safe; can feel sticky at high concentrations",
    },
    "PANTHENOL": {
        "common_names": ["Pro-Vitamin B5", "Dexpanthenol", "판테놀"],
        "categories": ["hydrating", "soothing", "barrier_repair"],
        "mechanism": {
            "primary": "Converted to pantothenic acid; improves barrier function",
            "secondary": ["Anti-inflammatory", "Wound healing", "Moisturizing"],
        },
        "typical_concentration": {"min": 1.0, "max": 5.0, "optimal": 2.0},
        "evidence_level": "Strong clinical evidence",
        "claims_supported": ["보습", "Soothing", "Barrier repair"],
        "synergies": ["ALLANTOIN", "CENTELLA ASIATICA"],
        "precautions": "Excellent safety profile; suitable for sensitive skin",
    },
    # Barrier repair
    "CERAMIDE NP": {
        "common_names": ["Ceramide 3", "세라마이드"],
        "categories": ["barrier_repair", "hydrating"],
        "mechanism": {
            "primary": "Lipid replacement in stratum corneum",
            "secondary": ["Barrier restoration", "Water retention"],
        },
        "typical_concentration": {"min": 0.1, "max": 1.0, "optimal": 0.5},
        "evidence_level": "Strong clinical evidence",
        "claims_supported": ["장벽강화", "Barrier repair", "Moisturizing"],
        "synergies": ["CHOLESTEROL", "FATTY ACIDS", "PHYTOSPHINGOSINE"],
        "precautions": "Best combined with cholesterol and fatty acids (3:1:1 ratio)",
    },
    "CENTELLA ASIATICA EXTRACT": {
        "common_names": ["Cica", "Gotu Kola", "병풀추출물"],
        "categories": ["soothing", "barrier_repair", "regenerating"],
        "mechanism": {
            "primary": "Madecassoside/asiaticoside stimulate collagen synthesis",
            "secondary": ["Anti-inflammatory", "Wound healing", "Antioxidant"],
        },
        "typical_concentration": {"min": 0.1, "max": 5.0, "optimal": 1.0},
        "evidence_level": "Strong clinical evidence",
        "claims_supported": ["진정", "Soothing", "Barrier repair", "Anti-aging"],
        "synergies": ["PANTHENOL", "MADECASSOSIDE"],
        "precautions": "Active compounds include madecassoside, asiaticoside, asiatic acid",
    },
    # Soothing
    "ALLANTOIN": {
        "common_names": ["알란토인"],
        "categories": ["soothing", "hydrating"],
        "mechanism": {
            "primary": "Cell proliferation stimulation and keratolytic",
            "secondary": ["Anti-irritant", "Moisturizing"],
        },
        "typical_concentration": {"min": 0.1, "max": 2.0, "optimal": 0.5},
        "evidence_level": "Well-established",
        "claims_supported": ["진정", "Soothing", "Healing"],
        "synergies": ["PANTHENOL", "CENTELLA ASIATICA"],
        "precautions": "Very safe; suitable for sensitive skin",
    },
    "BISABOLOL": {
        "common_names": ["Alpha-Bisabolol", "비사보롤"],
        "categories": ["soothing", "antioxidant"],
        "mechanism": {
            "primary": "Anti-inflammatory via multiple pathways",
            "secondary": ["Antimicrobial", "Penetration enhancement"],
        },
        "typical_concentration": {"min": 0.1, "max": 1.0, "optimal": 0.5},
        "evidence_level": "Moderate clinical evidence",
        "claims_supported": ["진정", "Soothing", "Calming"],
        "synergies": ["CHAMOMILE", "ALLANTOIN"],
        "precautions": "Natural origin (chamomile); excellent tolerability",
    },
    # Antioxidant
    "TOCOPHEROL": {
        "common_names": ["Vitamin E", "토코페롤"],
        "categories": ["antioxidant", "barrier_repair"],
        "mechanism": {
            "primary": "Lipid peroxidation chain breaking",
            "secondary": ["UV protection", "Barrier support", "Anti-inflammatory"],
        },
        "typical_concentration": {"min": 0.1, "max": 2.0, "optimal": 1.0},
        "evidence_level": "Strong clinical evidence",
        "claims_supported": ["항산화", "Antioxidant", "Moisturizing"],
        "synergies": ["VITAMIN C", "FERULIC ACID"],
        "precautions": "Multiple forms available; alpha-tocopherol most bioactive",
    },
    "FERULIC ACID": {
        "common_names": ["페룰산"],
        "categories": ["antioxidant"],
        "mechanism": {
            "primary": "Free radical scavenging and UV absorption",
            "secondary": ["Stabilizes Vitamin C/E", "Anti-inflammatory"],
        },
        "typical_concentration": {"min": 0.5, "max": 1.0, "optimal": 1.0},
        "evidence_level": "Strong clinical evidence",
        "claims_supported": ["항산화", "Antioxidant", "Photoprotection"],
        "synergies": ["VITAMIN C", "VITAMIN E"],
        "precautions": "Part of famous C E Ferulic formulation",
    },
    # Exfoliating
    "GLYCOLIC ACID": {
        "common_names": ["AHA", "글리콜산"],
        "categories": ["exfoliating", "anti_aging"],
        "mechanism": {
            "primary": "Desmosome dissolution enabling cell shedding",
            "secondary": ["Collagen stimulation", "Hyperpigmentation reduction"],
        },
        "typical_concentration": {"min": 2.0, "max": 10.0, "optimal": 5.0},
        "evidence_level": "Strong clinical evidence",
        "claims_supported": ["각질제거", "Exfoliating", "Brightening", "Anti-aging"],
        "synergies": ["HYALURONIC ACID", "NIACINAMIDE"],
        "precautions": "pH dependent efficacy; sun sensitivity; can irritate",
    },
    "SALICYLIC ACID": {
        "common_names": ["BHA", "살리실산"],
        "categories": ["exfoliating", "sebum_control"],
        "mechanism": {
            "primary": "Lipophilic keratolytic penetrating pores",
            "secondary": ["Anti-inflammatory", "Antibacterial"],
        },
        "typical_concentration": {"min": 0.5, "max": 2.0, "optimal": 1.0},
        "evidence_level": "Strong clinical evidence",
        "claims_supported": ["각질제거", "Pore clearing", "Acne"],
        "synergies": ["NIACINAMIDE", "TEA TREE"],
        "precautions": "EU restricted to 2% leave-on; not for children under 3",
    },
    # Regenerating
    "EGF": {
        "common_names": ["Epidermal Growth Factor", "상피세포성장인자"],
        "categories": ["regenerating", "anti_aging"],
        "mechanism": {
            "primary": "EGFR activation stimulating cell proliferation",
            "secondary": ["Wound healing", "Collagen synthesis"],
        },
        "typical_concentration": {"min": 0.0001, "max": 0.001, "optimal": 0.0005},
        "evidence_level": "Moderate clinical evidence",
        "claims_supported": ["재생", "Regenerating", "Anti-aging"],
        "synergies": ["PEPTIDES", "HYALURONIC ACID"],
        "precautions": "Very potent at low concentrations; stability concerns",
    },
    "PDRN": {
        "common_names": ["Polydeoxyribonucleotide", "연어DNA", "PDRN"],
        "categories": ["regenerating", "anti_aging"],
        "mechanism": {
            "primary": "A2A purinergic receptor activation",
            "secondary": [
                "Salvage pathway activation",
                "Anti-inflammatory",
                "Angiogenesis",
            ],
        },
        "typical_concentration": {"min": 0.01, "max": 0.5, "optimal": 0.1},
        "evidence_level": "Emerging evidence",
        "claims_supported": ["재생", "Regenerating", "Wound healing"],
        "synergies": ["NAD+", "ADENOSINE"],
        "precautions": "Premium ingredient; salmon-derived",
    },
    # Microbiome
    "LACTOBACILLUS FERMENT": {
        "common_names": ["Probiotic", "유산균발효여과물"],
        "categories": ["microbiome", "soothing"],
        "mechanism": {
            "primary": "Postbiotic metabolites supporting skin microbiome",
            "secondary": ["Barrier support", "Anti-inflammatory"],
        },
        "typical_concentration": {"min": 0.1, "max": 5.0, "optimal": 1.0},
        "evidence_level": "Emerging evidence",
        "claims_supported": ["마이크로바이옴", "Microbiome balance", "Soothing"],
        "synergies": ["PREBIOTICS", "OTHER FERMENTS"],
        "precautions": "Postbiotic (not live bacteria); stable in formulation",
    },
    "GALACTOMYCES FERMENT FILTRATE": {
        "common_names": ["Pitera", "GFF", "갈락토미세스발효여과물"],
        "categories": ["microbiome", "brightening", "hydrating"],
        "mechanism": {
            "primary": "Rich in vitamins, amino acids, organic acids",
            "secondary": ["Brightening", "Hydrating", "Anti-aging"],
        },
        "typical_concentration": {"min": 1.0, "max": 95.0, "optimal": 50.0},
        "evidence_level": "Moderate clinical evidence",
        "claims_supported": ["미백", "Brightening", "Hydrating", "Anti-aging"],
        "synergies": ["NIACINAMIDE", "HYALURONIC ACID"],
        "precautions": "Famous SK-II ingredient; can be used at high concentrations",
    },
}

# Efficacy categories
EFFICACY_CATEGORIES = {
    "brightening": {
        "name_kr": "미백/브라이트닝",
        "name_en": "Brightening",
        "description": "Skin brightening and hyperpigmentation reduction",
        "mechanisms": [
            "Tyrosinase inhibition",
            "Melanin transfer inhibition",
            "Antioxidant",
            "Cell turnover",
        ],
    },
    "anti_aging": {
        "name_kr": "주름개선/안티에이징",
        "name_en": "Anti-aging",
        "description": "Wrinkle reduction and skin rejuvenation",
        "mechanisms": [
            "Collagen synthesis",
            "ECM remodeling",
            "Cell turnover",
            "Antioxidant",
        ],
    },
    "hydrating": {
        "name_kr": "보습",
        "name_en": "Hydrating",
        "description": "Skin hydration and moisture retention",
        "mechanisms": ["Humectant", "Occlusive", "Emollient", "NMF replenishment"],
    },
    "barrier_repair": {
        "name_kr": "장벽강화",
        "name_en": "Barrier Repair",
        "description": "Skin barrier strengthening and repair",
        "mechanisms": [
            "Lipid replenishment",
            "Ceramide synthesis",
            "Tight junction support",
        ],
    },
    "soothing": {
        "name_kr": "진정",
        "name_en": "Soothing",
        "description": "Anti-inflammatory and skin calming",
        "mechanisms": ["COX inhibition", "Cytokine modulation", "Histamine blocking"],
    },
    "antioxidant": {
        "name_kr": "항산화",
        "name_en": "Antioxidant",
        "description": "Free radical protection",
        "mechanisms": ["ROS scavenging", "Metal chelation", "Enzyme activation"],
    },
    "exfoliating": {
        "name_kr": "각질케어",
        "name_en": "Exfoliating",
        "description": "Cell turnover and surface renewal",
        "mechanisms": ["Keratolytic", "Desmosome dissolution", "pH modulation"],
    },
    "sebum_control": {
        "name_kr": "피지조절",
        "name_en": "Sebum Control",
        "description": "Oil control and pore minimization",
        "mechanisms": [
            "Sebocyte regulation",
            "Astringent",
            "5-alpha reductase inhibition",
        ],
    },
    "regenerating": {
        "name_kr": "재생",
        "name_en": "Regenerating",
        "description": "Wound healing and tissue repair",
        "mechanisms": [
            "Growth factor stimulation",
            "Cell proliferation",
            "Angiogenesis",
        ],
    },
    "microbiome": {
        "name_kr": "마이크로바이옴",
        "name_en": "Microbiome",
        "description": "Skin microbiome support",
        "mechanisms": ["Prebiotic", "Postbiotic", "pH balancing"],
    },
}

# Known synergistic combinations
SYNERGY_COMBINATIONS = [
    {
        "name": "C E Ferulic",
        "ingredients": ["ASCORBIC ACID", "TOCOPHEROL", "FERULIC ACID"],
        "benefit": "Synergistic antioxidant protection; vitamin C stabilization",
        "reference": "Pinnell et al., 2005",
    },
    {
        "name": "Barrier Repair Complex",
        "ingredients": ["CERAMIDE NP", "CHOLESTEROL", "FATTY ACIDS"],
        "benefit": "Optimal 3:1:1 ratio mimics natural stratum corneum lipids",
        "reference": "Elias et al., 1999",
    },
    {
        "name": "Cica Complex",
        "ingredients": ["CENTELLA ASIATICA EXTRACT", "PANTHENOL", "ALLANTOIN"],
        "benefit": "Multi-pathway soothing and barrier repair",
        "reference": "Multiple studies",
    },
    {
        "name": "Niacinamide + HA",
        "ingredients": ["NIACINAMIDE", "HYALURONIC ACID"],
        "benefit": "Enhanced hydration with barrier support and brightening",
        "reference": "Cosmetic formulation best practice",
    },
    {
        "name": "Retinol + Peptides",
        "ingredients": ["RETINOL", "PEPTIDES"],
        "benefit": "Complementary anti-aging via different pathways",
        "reference": "Clinical practice",
    },
    {
        "name": "PDRN + NAD+",
        "ingredients": ["PDRN", "NAD+"],
        "benefit": "Cellular energy and regeneration synergy",
        "reference": "Emerging research",
    },
]


def normalize_inci(name: str) -> str:
    """Normalize INCI name for database lookup"""
    normalized = name.upper().strip()
    # Remove common prefixes/suffixes
    normalized = re.sub(r"^\d+\s*", "", normalized)  # Remove leading numbers
    normalized = re.sub(
        r"\s*\([^)]*\)\s*$", "", normalized
    )  # Remove trailing parentheticals
    normalized = normalized.replace("/", " ").replace("-", " ")
    normalized = " ".join(normalized.split())  # Normalize whitespace
    return normalized


def parse_ingredient_list(text: str) -> List[str]:
    """Parse ingredient list from text"""
    # Split by common delimiters
    ingredients = re.split(r"[,;]\s*", text)
    # Clean up
    ingredients = [i.strip() for i in ingredients if i.strip()]
    return ingredients


def lookup_ingredient(inci_name: str) -> Optional[Dict[str, Any]]:
    """Look up ingredient in database"""
    normalized = normalize_inci(inci_name)

    # Direct match
    if normalized in INGREDIENT_DATABASE:
        return INGREDIENT_DATABASE[normalized]

    # Partial match
    for key, data in INGREDIENT_DATABASE.items():
        if key in normalized or normalized in key:
            return data
        # Check common names
        for common in data.get("common_names", []):
            if common.upper() in normalized or normalized in common.upper():
                return data

    return None


def estimate_concentration(position: int, total: int) -> Tuple[str, float]:
    """Estimate concentration based on INCI position"""
    # First ingredient typically 50-80%
    # Ingredients listed in descending order by concentration
    # Below 1% can be listed in any order

    if position == 0:
        return "High (50-80%)", 65.0
    elif position <= 3:
        return "High (5-20%)", 10.0
    elif position <= 7:
        return "Medium (1-5%)", 3.0
    elif position <= 15:
        return "Low (0.1-1%)", 0.5
    else:
        return "Trace (<0.1%)", 0.05


def find_synergies(ingredient_names: List[str]) -> List[Dict[str, Any]]:
    """Find synergistic combinations in ingredient list"""
    found_synergies = []
    normalized_names = set(normalize_inci(n) for n in ingredient_names)

    for synergy in SYNERGY_COMBINATIONS:
        synergy_ingredients = set(normalize_inci(i) for i in synergy["ingredients"])
        # Check if at least 2 ingredients from synergy are present
        matches = synergy_ingredients.intersection(normalized_names)
        if len(matches) >= 2:
            found_synergies.append(
                {
                    "name": synergy["name"],
                    "matched_ingredients": list(matches),
                    "all_ingredients": synergy["ingredients"],
                    "complete": len(matches) == len(synergy_ingredients),
                    "benefit": synergy["benefit"],
                    "reference": synergy["reference"],
                }
            )

    return found_synergies


def analyze_formula(
    ingredient_list: List[str], include_all: bool = False
) -> Dict[str, Any]:
    """
    Analyze complete ingredient list.

    Args:
        ingredient_list: List of INCI names
        include_all: Include base ingredients (not just actives)

    Returns:
        Complete analysis dictionary
    """
    analysis = {
        "timestamp": datetime.now().isoformat(),
        "total_ingredients": len(ingredient_list),
        "analyzed_ingredients": [],
        "unknown_ingredients": [],
        "efficacy_summary": {},
        "synergies": [],
        "category_scores": {},
    }

    # Initialize category scores
    for cat in EFFICACY_CATEGORIES:
        analysis["category_scores"][cat] = {"score": 0, "ingredients": []}

    # Analyze each ingredient
    for position, inci_name in enumerate(ingredient_list):
        normalized = normalize_inci(inci_name)
        data = lookup_ingredient(inci_name)

        conc_estimate, conc_value = estimate_concentration(
            position, len(ingredient_list)
        )

        if data:
            ingredient_info = {
                "name": inci_name,
                "normalized": normalized,
                "position": position + 1,
                "concentration_estimate": conc_estimate,
                "concentration_value": conc_value,
                "categories": data.get("categories", []),
                "mechanism": data.get("mechanism", {}),
                "evidence_level": data.get("evidence_level", "Unknown"),
                "claims_supported": data.get("claims_supported", []),
                "synergies": data.get("synergies", []),
                "precautions": data.get("precautions", ""),
            }
            analysis["analyzed_ingredients"].append(ingredient_info)

            # Update category scores
            for cat in data.get("categories", []):
                if cat in analysis["category_scores"]:
                    # Weight by position (higher position = higher concentration)
                    weight = max(1, 10 - position) / 10
                    analysis["category_scores"][cat]["score"] += weight
                    analysis["category_scores"][cat]["ingredients"].append(inci_name)
        else:
            analysis["unknown_ingredients"].append(
                {
                    "name": inci_name,
                    "position": position + 1,
                    "concentration_estimate": conc_estimate,
                }
            )

    # Calculate efficacy summary
    for cat, data in analysis["category_scores"].items():
        if data["score"] > 0:
            # Convert to 5-star scale
            stars = min(5, int(data["score"] * 2.5) + 1)
            analysis["efficacy_summary"][cat] = {
                "score": round(data["score"], 2),
                "stars": stars,
                "star_display": "★" * stars + "☆" * (5 - stars),
                "key_ingredients": data["ingredients"][:5],  # Top 5
            }

    # Find synergies
    analysis["synergies"] = find_synergies(ingredient_list)

    return analysis


def generate_report(analysis: Dict[str, Any], product_name: str = "Product") -> str:
    """Generate markdown report from analysis"""
    report = []

    report.append(f"# Ingredient Efficacy Analysis Report")
    report.append(f"\n**Product**: {product_name}")
    report.append(f"**Generated**: {analysis['timestamp']}")
    report.append(f"**Total Ingredients**: {analysis['total_ingredients']}")

    # Executive Summary
    report.append("\n## Executive Summary")

    # Top efficacy categories
    sorted_categories = sorted(
        analysis["efficacy_summary"].items(), key=lambda x: x[1]["score"], reverse=True
    )

    if sorted_categories:
        report.append("\n### Efficacy Score Card")
        report.append("\n| Category | Score | Key Ingredients |")
        report.append("|----------|-------|-----------------|")

        for cat, data in sorted_categories[:5]:
            cat_info = EFFICACY_CATEGORIES.get(cat, {})
            cat_name = cat_info.get("name_en", cat.title())
            ingredients = ", ".join(data["key_ingredients"][:3])
            report.append(f"| {cat_name} | {data['star_display']} | {ingredients} |")

    # Primary Benefits
    if sorted_categories:
        top_benefits = [
            EFFICACY_CATEGORIES.get(cat, {}).get("name_en", cat)
            for cat, _ in sorted_categories[:3]
        ]
        report.append(f"\n**Primary Benefits**: {', '.join(top_benefits)}")

    # Synergies Found
    if analysis["synergies"]:
        report.append(
            f"\n**Synergistic Combinations Found**: {len(analysis['synergies'])}"
        )

    # Active Ingredient Analysis
    report.append("\n## Active Ingredient Analysis")

    actives = [
        i
        for i in analysis["analyzed_ingredients"]
        if i["concentration_estimate"] in ["High (5-20%)", "Medium (1-5%)"]
    ]

    for ingredient in actives:
        report.append(f"\n### {ingredient['name']}")
        report.append(
            f"- **Position**: #{ingredient['position']} ({ingredient['concentration_estimate']})"
        )
        report.append(f"- **Categories**: {', '.join(ingredient['categories'])}")

        if ingredient["mechanism"]:
            report.append(
                f"- **Primary Mechanism**: {ingredient['mechanism'].get('primary', 'N/A')}"
            )
            secondary = ingredient["mechanism"].get("secondary", [])
            if secondary:
                report.append(f"- **Secondary Effects**: {', '.join(secondary[:3])}")

        report.append(f"- **Evidence Level**: {ingredient['evidence_level']}")

        if ingredient["claims_supported"]:
            report.append(
                f"- **Supported Claims**: {', '.join(ingredient['claims_supported'])}"
            )

        if ingredient["precautions"]:
            report.append(f"- **Notes**: {ingredient['precautions']}")

    # Synergy Analysis
    if analysis["synergies"]:
        report.append("\n## Synergy Analysis")

        for synergy in analysis["synergies"]:
            status = "✓ Complete" if synergy["complete"] else "○ Partial"
            report.append(f"\n### {synergy['name']} {status}")
            report.append(
                f"- **Matched Ingredients**: {', '.join(synergy['matched_ingredients'])}"
            )
            report.append(f"- **Benefit**: {synergy['benefit']}")
            report.append(f"- **Reference**: {synergy['reference']}")

    # Full Ingredient List
    report.append("\n## Full Ingredient Breakdown")
    report.append("\n| # | Ingredient | Concentration | Categories |")
    report.append("|---|------------|---------------|------------|")

    for i in analysis["analyzed_ingredients"]:
        cats = ", ".join(i["categories"][:2]) if i["categories"] else "-"
        report.append(
            f"| {i['position']} | {i['name']} | {i['concentration_estimate']} | {cats} |"
        )

    # Unknown ingredients
    if analysis["unknown_ingredients"]:
        report.append("\n### Ingredients Not in Database")
        for i in analysis["unknown_ingredients"]:
            report.append(
                f"- #{i['position']} {i['name']} ({i['concentration_estimate']})"
            )

    # Claim Support Summary
    report.append("\n## Claim Support Summary")

    all_claims = {}
    for i in analysis["analyzed_ingredients"]:
        for claim in i.get("claims_supported", []):
            if claim not in all_claims:
                all_claims[claim] = []
            all_claims[claim].append(i["name"])

    if all_claims:
        report.append("\n| Claim | Supporting Ingredients | Confidence |")
        report.append("|-------|----------------------|------------|")

        for claim, ingredients in sorted(
            all_claims.items(), key=lambda x: len(x[1]), reverse=True
        ):
            confidence = (
                "★★★★★"
                if len(ingredients) >= 3
                else "★★★☆☆"
                if len(ingredients) >= 2
                else "★★☆☆☆"
            )
            ing_list = ", ".join(ingredients[:3])
            report.append(f"| {claim} | {ing_list} | {confidence} |")

    report.append("\n---")
    report.append(
        "*This analysis is generated automatically based on known ingredient data. "
    )
    report.append(
        "Actual efficacy depends on concentrations, formulation, and individual factors.*"
    )

    return "\n".join(report)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="Analyze cosmetic ingredient efficacy")
    parser.add_argument("input", nargs="?", help="Ingredient list (text) or file path")
    parser.add_argument("--file", "-f", help="Input file containing ingredient list")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format",
    )
    parser.add_argument(
        "--product-name", "-n", default="Product", help="Product name for report"
    )

    args = parser.parse_args()

    # Get ingredient list
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    elif args.input:
        text = args.input
    else:
        print("Error: Provide ingredient list as argument or via --file")
        return 1

    # Parse ingredients
    ingredients = parse_ingredient_list(text)

    if not ingredients:
        print("Error: No ingredients found")
        return 1

    print(f"Analyzing {len(ingredients)} ingredients...")

    # Analyze
    analysis = analyze_formula(ingredients)

    # Generate output
    if args.format == "json":
        output = json.dumps(analysis, indent=2, ensure_ascii=False)
    else:
        output = generate_report(analysis, args.product_name)

    # Save or print
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Report saved to: {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    exit(main())
