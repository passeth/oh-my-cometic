#!/usr/bin/env python3
"""
Formulation Strategy Generator
화장품 제형 전략 생성기

Usage:
    python strategy_generator.py --product serum --active vitamin_c --skin dry
"""

import argparse
from dataclasses import dataclass
from typing import List, Dict
from enum import Enum


class EmulsionType(Enum):
    OW = "O/W"
    WO = "W/O"
    WS = "W/S"
    ANHYDROUS = "Anhydrous"
    GEL = "Gel"


class DeliverySystem(Enum):
    LIPOSOME = "Liposome"
    CYCLODEXTRIN = "Cyclodextrin"
    SLN = "SLN/NLC"
    NANOEMULSION = "Nanoemulsion"
    NONE = "None"


ACTIVE_DB = {
    "vitamin_c": {
        "name": "Vitamin C",
        "inci": "ASCORBIC ACID",
        "solubility": "water",
        "issues": ["oxidation", "pH_sensitive"],
        "ph_range": (2.5, 3.5),
        "max_conc": 20.0,
        "delivery": [DeliverySystem.LIPOSOME]
    },
    "retinol": {
        "name": "Retinol",
        "inci": "RETINOL",
        "solubility": "oil",
        "issues": ["photodegradation", "oxidation"],
        "ph_range": (5.5, 6.5),
        "max_conc": 1.0,
        "delivery": [DeliverySystem.CYCLODEXTRIN, DeliverySystem.SLN]
    },
    "niacinamide": {
        "name": "Niacinamide",
        "inci": "NIACINAMIDE",
        "solubility": "water",
        "issues": [],
        "ph_range": (5.0, 7.0),
        "max_conc": 10.0,
        "delivery": [DeliverySystem.NONE]
    },
    "hyaluronic_acid": {
        "name": "Hyaluronic Acid",
        "inci": "SODIUM HYALURONATE",
        "solubility": "water",
        "issues": [],
        "ph_range": (5.0, 7.0),
        "max_conc": 2.0,
        "delivery": [DeliverySystem.NONE, DeliverySystem.LIPOSOME]
    },
    "peptide": {
        "name": "Peptides",
        "inci": "VARIOUS PEPTIDES",
        "solubility": "water",
        "issues": ["hydrolysis"],
        "ph_range": (5.0, 7.0),
        "max_conc": 5.0,
        "delivery": [DeliverySystem.LIPOSOME]
    }
}

PRODUCT_BASE = {
    "toner": {"emulsion": EmulsionType.GEL, "oil": (0, 5), "viscosity": (1, 50)},
    "essence": {"emulsion": EmulsionType.OW, "oil": (0, 10), "viscosity": (50, 500)},
    "serum": {"emulsion": EmulsionType.OW, "oil": (0, 15), "viscosity": (500, 5000)},
    "lotion": {"emulsion": EmulsionType.OW, "oil": (5, 20), "viscosity": (1000, 10000)},
    "cream": {"emulsion": EmulsionType.OW, "oil": (15, 40), "viscosity": (10000, 200000)},
    "oil_serum": {"emulsion": EmulsionType.ANHYDROUS, "oil": (95, 100), "viscosity": (10, 500)},
    "sunscreen": {"emulsion": EmulsionType.WS, "oil": (30, 50), "viscosity": (5000, 50000)}
}

SKIN_ADJUST = {
    "dry": {"oil_mult": 1.3, "preferred": [EmulsionType.WO, EmulsionType.OW]},
    "oily": {"oil_mult": 0.6, "preferred": [EmulsionType.OW, EmulsionType.GEL]},
    "combination": {"oil_mult": 0.9, "preferred": [EmulsionType.OW]},
    "sensitive": {"oil_mult": 1.0, "preferred": [EmulsionType.OW, EmulsionType.GEL]},
    "normal": {"oil_mult": 1.0, "preferred": [EmulsionType.OW]}
}

SEASON_ADJUST = {
    "summer": {"oil_mult": 0.7, "texture": "lightweight"},
    "winter": {"oil_mult": 1.4, "texture": "rich"},
    "spring": {"oil_mult": 0.9, "texture": "medium"},
    "fall": {"oil_mult": 1.1, "texture": "medium-rich"}
}


def generate_strategy(product: str, actives: List[str], skin: str, season: str) -> Dict:
    """Generate formulation strategy"""
    
    base = PRODUCT_BASE.get(product, PRODUCT_BASE["cream"])
    skin_adj = SKIN_ADJUST.get(skin, SKIN_ADJUST["normal"])
    season_adj = SEASON_ADJUST.get(season, SEASON_ADJUST["spring"])
    
    # Determine emulsion type
    emulsion = base["emulsion"]
    has_unstable = any(
        ACTIVE_DB.get(a, {}).get("issues", [])
        for a in actives
    )
    if has_unstable and any(ACTIVE_DB.get(a, {}).get("solubility") == "oil" for a in actives):
        emulsion = EmulsionType.ANHYDROUS
    
    # Determine delivery system
    delivery_scores = {}
    for active in actives:
        if active in ACTIVE_DB:
            for d in ACTIVE_DB[active].get("delivery", []):
                delivery_scores[d] = delivery_scores.get(d, 0) + 1
    delivery = max(delivery_scores, key=delivery_scores.get) if delivery_scores else DeliverySystem.NONE
    
    # Adjust oil content
    base_oil = (base["oil"][0] + base["oil"][1]) / 2
    adjusted_oil = base_oil * skin_adj["oil_mult"] * season_adj["oil_mult"]
    
    # Generate processing notes
    notes = []
    if emulsion == EmulsionType.OW:
        notes.append("Heat water phase and oil phase to 70-75°C")
        notes.append("Add oil phase to water phase while homogenizing")
        notes.append("Add heat-sensitive actives below 40°C")
    elif emulsion == EmulsionType.ANHYDROUS:
        notes.append("Mix all oils at 50-60°C")
        notes.append("Add heat-sensitive actives below 40°C")
        notes.append("Fill under nitrogen atmosphere")
    
    # Packaging recommendation
    packaging = "Airless pump" if has_unstable else "Standard pump or jar"
    if any(ACTIVE_DB.get(a, {}).get("issues", []).count("photodegradation") for a in actives):
        packaging += " + opaque container"
    
    return {
        "product_type": product,
        "actives": actives,
        "skin_type": skin,
        "season": season,
        "emulsion_type": emulsion.value,
        "delivery_system": delivery.value,
        "oil_content": f"{adjusted_oil:.1f}%",
        "processing_notes": notes,
        "packaging": packaging
    }


def print_strategy(strategy: Dict):
    """Print formatted strategy"""
    print("=" * 50)
    print("FORMULATION STRATEGY REPORT")
    print("=" * 50)
    print(f"Product: {strategy['product_type'].upper()}")
    print(f"Active Ingredients: {', '.join(strategy['actives'])}")
    print(f"Skin Type: {strategy['skin_type']}")
    print(f"Season: {strategy['season']}")
    print("-" * 50)
    print(f"Emulsion Type: {strategy['emulsion_type']}")
    print(f"Delivery System: {strategy['delivery_system']}")
    print(f"Adjusted Oil Content: {strategy['oil_content']}")
    print("-" * 50)
    print("Processing Notes:")
    for i, note in enumerate(strategy['processing_notes'], 1):
        print(f"  {i}. {note}")
    print("-" * 50)
    print(f"Packaging: {strategy['packaging']}")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="Formulation Strategy Generator")
    parser.add_argument("--product", type=str, default="serum",
                       choices=list(PRODUCT_BASE.keys()))
    parser.add_argument("--active", type=str, nargs="+", default=["niacinamide"])
    parser.add_argument("--skin", type=str, default="normal",
                       choices=list(SKIN_ADJUST.keys()))
    parser.add_argument("--season", type=str, default="spring",
                       choices=list(SEASON_ADJUST.keys()))
    
    args = parser.parse_args()
    
    strategy = generate_strategy(
        product=args.product,
        actives=args.active,
        skin=args.skin,
        season=args.season
    )
    
    print_strategy(strategy)


if __name__ == "__main__":
    main()
