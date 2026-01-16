#!/usr/bin/env python3
"""
Irritation Estimator - Skin Irritation Prediction Utility

A command-line tool for predicting skin irritation potential of cosmetic
ingredients and formulations based on molecular properties, QSAR models,
and empirical data.

Part of the irritation-predictor skill for claude-cosmetic-skills.

Usage:
    python irritation_estimator.py --ingredient "Sodium Lauryl Sulfate" --concentration 2.0
    python irritation_estimator.py --formula formula.json --output report.json
    python irritation_estimator.py --logp 2.5 --mw 288 --pka 4.75

Author: Claude Code
Version: 1.0.0
"""

import argparse
import json
import math
import sys
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional, List, Dict, Any, Tuple
from pathlib import Path


class IrritationCategory(Enum):
    """UN GHS skin irritation categories."""
    NON_IRRITANT = "Non-irritant"
    MILD = "Mild irritant"
    MODERATE = "Moderate irritant"
    SEVERE = "Severe irritant"
    CATEGORY_2 = "Category 2 (GHS)"  # Official GHS designation


@dataclass
class MolecularDescriptors:
    """Molecular descriptors for irritation prediction."""
    logp: Optional[float] = None
    molecular_weight: Optional[float] = None
    pka: Optional[float] = None
    psa: Optional[float] = None  # Polar Surface Area
    hbd: Optional[int] = None    # Hydrogen Bond Donors
    hba: Optional[int] = None    # Hydrogen Bond Acceptors
    charge: Optional[int] = None  # Formal charge at pH 7


@dataclass
class IngredientData:
    """Ingredient information for irritation assessment."""
    name: str
    inci_name: Optional[str] = None
    cas_number: Optional[str] = None
    concentration: float = 1.0  # Percentage
    descriptors: MolecularDescriptors = field(default_factory=MolecularDescriptors)
    known_irritation_score: Optional[float] = None  # If empirical data available
    cmc: Optional[float] = None  # Critical Micelle Concentration (for surfactants)
    zein_value: Optional[float] = None  # Protein denaturation index


@dataclass
class IrritationResult:
    """Result of irritation prediction."""
    ingredient_name: str
    concentration: float
    raw_score: float  # 0-100 scale
    adjusted_score: float  # After concentration/pH adjustments
    irritation_index: float
    category: IrritationCategory
    confidence: float  # 0-1 scale
    warnings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    method_used: str = "QSAR"


# Common cosmetic ingredients database with known irritation data
INGREDIENT_DATABASE: Dict[str, Dict[str, Any]] = {
    "sodium lauryl sulfate": {
        "inci": "Sodium Lauryl Sulfate",
        "cas": "151-21-3",
        "logp": 1.6,
        "mw": 288.38,
        "cmc": 8.2,  # mM
        "zein_value": 100,  # Reference standard
        "irritation_potential": 75,
        "category": "anionic surfactant",
        "max_recommended": 1.0,
    },
    "sodium laureth sulfate": {
        "inci": "Sodium Laureth Sulfate",
        "cas": "9004-82-4",
        "logp": 2.1,
        "mw": 422.0,  # Average for 2EO
        "cmc": 1.0,
        "zein_value": 65,
        "irritation_potential": 55,
        "category": "anionic surfactant",
        "max_recommended": 15.0,
    },
    "cocamidopropyl betaine": {
        "inci": "Cocamidopropyl Betaine",
        "cas": "61789-40-0",
        "logp": 0.8,
        "mw": 342.52,
        "cmc": 0.1,
        "zein_value": 30,
        "irritation_potential": 25,
        "category": "amphoteric surfactant",
        "max_recommended": 10.0,
    },
    "sodium cocoyl isethionate": {
        "inci": "Sodium Cocoyl Isethionate",
        "cas": "61789-32-0",
        "logp": 3.2,
        "mw": 314.0,
        "cmc": 6.0,
        "zein_value": 20,
        "irritation_potential": 20,
        "category": "anionic surfactant",
        "max_recommended": 50.0,
    },
    "decyl glucoside": {
        "inci": "Decyl Glucoside",
        "cas": "68515-73-1",
        "logp": 2.5,
        "mw": 320.42,
        "cmc": 2.2,
        "zein_value": 12,
        "irritation_potential": 15,
        "category": "nonionic surfactant",
        "max_recommended": 20.0,
    },
    "glycolic acid": {
        "inci": "Glycolic Acid",
        "cas": "79-14-1",
        "logp": -1.11,
        "mw": 76.05,
        "pka": 3.83,
        "irritation_potential": 50,  # pH dependent
        "category": "alpha hydroxy acid",
        "max_recommended": 10.0,  # Depends on pH
    },
    "salicylic acid": {
        "inci": "Salicylic Acid",
        "cas": "69-72-7",
        "logp": 2.26,
        "mw": 138.12,
        "pka": 2.97,
        "irritation_potential": 40,
        "category": "beta hydroxy acid",
        "max_recommended": 2.0,
    },
    "retinol": {
        "inci": "Retinol",
        "cas": "68-26-8",
        "logp": 6.2,
        "mw": 286.45,
        "irritation_potential": 60,
        "category": "vitamin a derivative",
        "max_recommended": 1.0,
    },
    "niacinamide": {
        "inci": "Niacinamide",
        "cas": "98-92-0",
        "logp": -0.37,
        "mw": 122.12,
        "irritation_potential": 5,
        "category": "vitamin b3",
        "max_recommended": 10.0,
    },
    "glycerin": {
        "inci": "Glycerin",
        "cas": "56-81-5",
        "logp": -1.76,
        "mw": 92.09,
        "irritation_potential": 0,
        "category": "humectant",
        "max_recommended": 30.0,
    },
    "propylene glycol": {
        "inci": "Propylene Glycol",
        "cas": "57-55-6",
        "logp": -0.92,
        "mw": 76.09,
        "irritation_potential": 10,
        "category": "humectant",
        "max_recommended": 20.0,
    },
    "phenoxyethanol": {
        "inci": "Phenoxyethanol",
        "cas": "122-99-6",
        "logp": 1.16,
        "mw": 138.16,
        "irritation_potential": 20,
        "category": "preservative",
        "max_recommended": 1.0,
    },
}


def get_ingredient_data(name: str) -> Optional[Dict[str, Any]]:
    """Look up ingredient in database (case-insensitive)."""
    normalized = name.lower().strip()
    return INGREDIENT_DATABASE.get(normalized)


def calculate_penetration_score(descriptors: MolecularDescriptors) -> float:
    """
    Calculate skin penetration potential based on molecular descriptors.
    Higher score = more likely to penetrate.
    """
    score = 50.0  # Base score

    # LogP contribution (optimal 2-4 for penetration)
    if descriptors.logp is not None:
        if descriptors.logp < 0:
            score -= 20
        elif 0 <= descriptors.logp < 2:
            score += 10
        elif 2 <= descriptors.logp <= 4:
            score += 25
        elif descriptors.logp > 4:
            score += 15  # Too lipophilic may be trapped in SC

    # Molecular weight contribution (500 Da rule)
    if descriptors.molecular_weight is not None:
        if descriptors.molecular_weight > 500:
            score -= 30
        elif 300 < descriptors.molecular_weight <= 500:
            score += 5
        elif descriptors.molecular_weight <= 300:
            score += 20

    # PSA contribution
    if descriptors.psa is not None:
        if descriptors.psa < 60:
            score += 15
        elif 60 <= descriptors.psa <= 90:
            score += 5
        else:
            score -= 10

    return max(0, min(100, score))


def calculate_base_irritation_score(descriptors: MolecularDescriptors) -> float:
    """
    Calculate base irritation score from molecular descriptors using QSAR model.
    Returns score on 0-100 scale.
    """
    score = 20.0  # Base irritation potential

    # Penetration-based component
    penetration = calculate_penetration_score(descriptors)
    score += penetration * 0.3

    # LogP direct contribution
    if descriptors.logp is not None:
        if 2 <= descriptors.logp <= 4:
            score += 15  # Optimal for membrane disruption
        elif descriptors.logp > 4:
            score += 10

    # Charge contribution (charged species interact with proteins)
    if descriptors.charge is not None and descriptors.charge != 0:
        score += 10

    return max(0, min(100, score))


def calculate_ph_adjustment(base_score: float, pka: Optional[float],
                           formulation_ph: float = 5.5) -> Tuple[float, float]:
    """
    Adjust irritation score based on pH and pKa.
    Returns (adjusted_score, percent_unionized).
    """
    if pka is None:
        return base_score, 100.0

    # Calculate percent unionized using Henderson-Hasselbalch
    # Assuming acid (adjust for bases if needed)
    percent_unionized = 100.0 / (1.0 + math.pow(10, formulation_ph - pka))

    # Unionized form is more penetrating/irritating
    adjustment_factor = percent_unionized / 50.0  # Normalized to 50% as baseline
    adjusted_score = base_score * adjustment_factor

    return max(0, min(100, adjusted_score)), percent_unionized


def calculate_concentration_factor(concentration: float,
                                   max_recommended: float = 100.0) -> float:
    """
    Calculate concentration adjustment factor.
    Non-linear relationship: low concentrations have proportionally lower effect.
    """
    if concentration <= 0:
        return 0.0

    # Sigmoid-like relationship
    normalized = concentration / max(max_recommended, 1.0)
    if normalized <= 0.1:
        factor = normalized * 2  # Very low concentrations
    elif normalized <= 0.5:
        factor = 0.2 + (normalized - 0.1) * 1.5
    else:
        factor = 0.8 + (normalized - 0.5) * 0.4

    return min(1.0, factor)


def calculate_irritation_index(ingredients: List[IngredientData],
                              formulation_ph: float = 5.5) -> Tuple[float, List[IrritationResult]]:
    """
    Calculate total Irritation Index for a formulation.

    II = Σ(Ci × IPi × AFi) / 100

    Where:
    - Ci = Concentration of ingredient i (%)
    - IPi = Irritation Potential score (0-100)
    - AFi = Adjustment Factor (pH, vehicle effects)
    """
    results = []
    total_ii = 0.0

    for ingredient in ingredients:
        # Get known data or use provided descriptors
        db_data = get_ingredient_data(ingredient.name)

        if ingredient.known_irritation_score is not None:
            base_score = ingredient.known_irritation_score
            method = "Empirical"
        elif db_data and "irritation_potential" in db_data:
            base_score = db_data["irritation_potential"]
            method = "Database"
            # Update descriptors from database if not provided
            if ingredient.descriptors.logp is None and "logp" in db_data:
                ingredient.descriptors.logp = db_data["logp"]
            if ingredient.descriptors.molecular_weight is None and "mw" in db_data:
                ingredient.descriptors.molecular_weight = db_data["mw"]
            if ingredient.descriptors.pka is None and "pka" in db_data:
                ingredient.descriptors.pka = db_data["pka"]
        else:
            base_score = calculate_base_irritation_score(ingredient.descriptors)
            method = "QSAR"

        # pH adjustment for ionizable compounds
        pka = ingredient.descriptors.pka
        if pka is None and db_data and "pka" in db_data:
            pka = db_data["pka"]

        adjusted_score, pct_unionized = calculate_ph_adjustment(
            base_score, pka, formulation_ph
        )

        # Concentration factor
        max_rec = 100.0
        if db_data and "max_recommended" in db_data:
            max_rec = db_data["max_recommended"]

        conc_factor = calculate_concentration_factor(ingredient.concentration, max_rec)

        # Calculate contribution to Irritation Index
        ii_contribution = (ingredient.concentration * adjusted_score * conc_factor) / 100
        total_ii += ii_contribution

        # Determine category
        if ii_contribution < 0.5:
            category = IrritationCategory.NON_IRRITANT
        elif ii_contribution < 2.0:
            category = IrritationCategory.MILD
        elif ii_contribution < 5.0:
            category = IrritationCategory.MODERATE
        else:
            category = IrritationCategory.SEVERE

        # Calculate confidence
        confidence = 0.9 if method == "Empirical" else (0.7 if method == "Database" else 0.5)

        # Generate warnings and recommendations
        warnings = []
        recommendations = []

        if db_data and ingredient.concentration > db_data.get("max_recommended", 100):
            warnings.append(f"Concentration exceeds maximum recommended ({db_data['max_recommended']}%)")

        if pka is not None and formulation_ph < pka - 1:
            warnings.append(f"Low pH increases free acid content ({pct_unionized:.1f}% unionized)")

        if base_score > 50 and ingredient.concentration > 5:
            recommendations.append("Consider reducing concentration or adding soothing agents")

        if db_data and db_data.get("category") == "anionic surfactant":
            recommendations.append("Consider amphoteric co-surfactant to reduce irritation")

        result = IrritationResult(
            ingredient_name=ingredient.name,
            concentration=ingredient.concentration,
            raw_score=base_score,
            adjusted_score=adjusted_score,
            irritation_index=ii_contribution,
            category=category,
            confidence=confidence,
            warnings=warnings,
            recommendations=recommendations,
            method_used=method
        )
        results.append(result)

    return total_ii, results


def classify_formulation(total_ii: float) -> Tuple[IrritationCategory, str]:
    """Classify formulation based on total Irritation Index."""
    if total_ii < 0.5:
        return IrritationCategory.NON_IRRITANT, "Formulation is expected to be non-irritating"
    elif total_ii < 2.0:
        return IrritationCategory.MILD, "Formulation may cause mild irritation in sensitive individuals"
    elif total_ii < 5.0:
        return IrritationCategory.MODERATE, "Formulation may cause moderate irritation; recommend patch testing"
    else:
        return IrritationCategory.SEVERE, "Formulation has high irritation potential; reformulation recommended"


def predict_mtv_viability(total_ii: float) -> Tuple[float, str]:
    """
    Predict approximate MTT viability (%) from Irritation Index.
    Based on correlation between II and in vitro results.
    """
    # Inverse sigmoid relationship
    if total_ii < 0.1:
        viability = 95.0
    else:
        viability = 100.0 / (1.0 + math.exp((total_ii - 3.0) * 0.8))

    viability = max(5.0, min(100.0, viability))

    if viability > 50:
        ghs_prediction = "No Category (Non-irritant per OECD TG 439)"
    else:
        ghs_prediction = "Category 2 (Irritant per OECD TG 439)"

    return viability, ghs_prediction


def format_report(total_ii: float, results: List[IrritationResult],
                 formulation_ph: float) -> Dict[str, Any]:
    """Generate comprehensive report dictionary."""
    category, description = classify_formulation(total_ii)
    predicted_viability, ghs_prediction = predict_mtv_viability(total_ii)

    report = {
        "summary": {
            "total_irritation_index": round(total_ii, 3),
            "classification": category.value,
            "description": description,
            "formulation_ph": formulation_ph,
        },
        "in_vitro_prediction": {
            "predicted_mtv_viability_percent": round(predicted_viability, 1),
            "ghs_classification": ghs_prediction,
            "note": "Prediction based on QSAR model; confirm with OECD TG 439 testing"
        },
        "ingredient_analysis": [
            {
                "name": r.ingredient_name,
                "concentration_percent": r.concentration,
                "raw_irritation_score": round(r.raw_score, 1),
                "adjusted_score": round(r.adjusted_score, 1),
                "irritation_index_contribution": round(r.irritation_index, 3),
                "category": r.category.value,
                "confidence": round(r.confidence, 2),
                "method": r.method_used,
                "warnings": r.warnings,
                "recommendations": r.recommendations,
            }
            for r in results
        ],
        "recommendations": [],
        "regulatory_notes": [
            "EU Cosmetics Regulation (EC) No 1223/2009 requires safety assessment",
            "OECD TG 439 is the accepted in vitro method for skin irritation",
            "In silico predictions should be validated with in vitro testing for regulatory submissions"
        ]
    }

    # Add overall recommendations
    if total_ii >= 2.0:
        report["recommendations"].append("Consider reformulation to reduce irritation potential")
    if any(r.warnings for r in results):
        report["recommendations"].append("Address ingredient-specific warnings before proceeding")
    if formulation_ph < 4.0:
        report["recommendations"].append("Low pH may increase irritation from acidic ingredients")
    if formulation_ph > 9.0:
        report["recommendations"].append("High pH may compromise skin barrier; consider pH adjustment")

    return report


def print_text_report(report: Dict[str, Any]) -> None:
    """Print human-readable report to console."""
    print("\n" + "=" * 70)
    print("              SKIN IRRITATION PREDICTION REPORT")
    print("=" * 70)

    summary = report["summary"]
    print(f"\nTotal Irritation Index: {summary['total_irritation_index']:.3f}")
    print(f"Classification: {summary['classification']}")
    print(f"Formulation pH: {summary['formulation_ph']}")
    print(f"\n{summary['description']}")

    print("\n" + "-" * 70)
    print("IN VITRO PREDICTION (OECD TG 439)")
    print("-" * 70)
    invitro = report["in_vitro_prediction"]
    print(f"Predicted MTT Viability: {invitro['predicted_mtv_viability_percent']:.1f}%")
    print(f"GHS Classification: {invitro['ghs_classification']}")

    print("\n" + "-" * 70)
    print("INGREDIENT ANALYSIS")
    print("-" * 70)

    for ing in report["ingredient_analysis"]:
        print(f"\n  {ing['name']} ({ing['concentration_percent']}%)")
        print(f"    Raw Score: {ing['raw_irritation_score']:.1f} | "
              f"Adjusted: {ing['adjusted_score']:.1f} | "
              f"II Contribution: {ing['irritation_index_contribution']:.3f}")
        print(f"    Category: {ing['category']} | "
              f"Confidence: {ing['confidence']:.0%} | "
              f"Method: {ing['method']}")

        if ing['warnings']:
            for w in ing['warnings']:
                print(f"    [WARNING] {w}")
        if ing['recommendations']:
            for r in ing['recommendations']:
                print(f"    [RECOMMEND] {r}")

    if report["recommendations"]:
        print("\n" + "-" * 70)
        print("OVERALL RECOMMENDATIONS")
        print("-" * 70)
        for rec in report["recommendations"]:
            print(f"  * {rec}")

    print("\n" + "-" * 70)
    print("REGULATORY NOTES")
    print("-" * 70)
    for note in report["regulatory_notes"]:
        print(f"  * {note}")

    print("\n" + "=" * 70)
    print("Note: This is a computational prediction. Validate with in vitro testing.")
    print("=" * 70 + "\n")


def parse_formula_file(filepath: str) -> Tuple[List[IngredientData], float]:
    """Parse formula from JSON file."""
    with open(filepath, 'r') as f:
        data = json.load(f)

    ph = data.get("ph", 5.5)
    ingredients = []

    for ing_data in data.get("ingredients", []):
        descriptors = MolecularDescriptors(
            logp=ing_data.get("logp"),
            molecular_weight=ing_data.get("mw"),
            pka=ing_data.get("pka"),
            psa=ing_data.get("psa"),
        )

        ingredient = IngredientData(
            name=ing_data["name"],
            inci_name=ing_data.get("inci"),
            concentration=ing_data.get("concentration", 1.0),
            descriptors=descriptors,
            known_irritation_score=ing_data.get("irritation_score"),
        )
        ingredients.append(ingredient)

    return ingredients, ph


def main():
    parser = argparse.ArgumentParser(
        description="Skin Irritation Prediction Utility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Predict irritation for a single ingredient
  python irritation_estimator.py --ingredient "Sodium Lauryl Sulfate" --concentration 2.0

  # Use molecular descriptors directly
  python irritation_estimator.py --logp 2.5 --mw 288 --concentration 5.0

  # Analyze a complete formula from JSON file
  python irritation_estimator.py --formula cleanser_formula.json --output report.json

  # Specify formulation pH
  python irritation_estimator.py --ingredient "Glycolic Acid" --concentration 10 --ph 3.5

Formula JSON format:
  {
    "name": "Gentle Cleanser",
    "ph": 5.5,
    "ingredients": [
      {"name": "Sodium Laureth Sulfate", "concentration": 12.0},
      {"name": "Cocamidopropyl Betaine", "concentration": 4.0}
    ]
  }
        """
    )

    parser.add_argument("--ingredient", "-i", type=str,
                       help="Single ingredient name to assess")
    parser.add_argument("--concentration", "-c", type=float, default=1.0,
                       help="Concentration in percent (default: 1.0)")
    parser.add_argument("--formula", "-f", type=str,
                       help="Path to formula JSON file")
    parser.add_argument("--ph", type=float, default=5.5,
                       help="Formulation pH (default: 5.5)")
    parser.add_argument("--logp", type=float,
                       help="LogP value for custom molecule")
    parser.add_argument("--mw", type=float,
                       help="Molecular weight in Da for custom molecule")
    parser.add_argument("--pka", type=float,
                       help="pKa value for custom molecule")
    parser.add_argument("--output", "-o", type=str,
                       help="Output JSON file path")
    parser.add_argument("--json", action="store_true",
                       help="Output as JSON to stdout")
    parser.add_argument("--list-ingredients", action="store_true",
                       help="List known ingredients in database")

    args = parser.parse_args()

    # List known ingredients
    if args.list_ingredients:
        print("\nKnown Ingredients in Database:")
        print("-" * 50)
        for name, data in sorted(INGREDIENT_DATABASE.items()):
            print(f"  {data.get('inci', name)}")
            print(f"    Category: {data.get('category', 'unknown')}")
            print(f"    Irritation Potential: {data.get('irritation_potential', 'N/A')}")
            print(f"    Max Recommended: {data.get('max_recommended', 'N/A')}%")
            print()
        return

    # Build ingredient list
    ingredients = []
    formulation_ph = args.ph

    if args.formula:
        # Load from file
        ingredients, formulation_ph = parse_formula_file(args.formula)
        if args.ph != 5.5:  # Override if specified
            formulation_ph = args.ph
    elif args.ingredient:
        # Single ingredient
        descriptors = MolecularDescriptors(
            logp=args.logp,
            molecular_weight=args.mw,
            pka=args.pka,
        )
        ingredient = IngredientData(
            name=args.ingredient,
            concentration=args.concentration,
            descriptors=descriptors,
        )
        ingredients.append(ingredient)
    elif args.logp is not None or args.mw is not None:
        # Custom molecule by descriptors
        descriptors = MolecularDescriptors(
            logp=args.logp,
            molecular_weight=args.mw,
            pka=args.pka,
        )
        ingredient = IngredientData(
            name="Custom Molecule",
            concentration=args.concentration,
            descriptors=descriptors,
        )
        ingredients.append(ingredient)
    else:
        parser.print_help()
        print("\nError: Please provide --ingredient, --formula, or molecular descriptors (--logp, --mw)")
        sys.exit(1)

    # Calculate irritation
    total_ii, results = calculate_irritation_index(ingredients, formulation_ph)

    # Generate report
    report = format_report(total_ii, results, formulation_ph)

    # Output
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Report saved to: {args.output}")

    if args.json:
        print(json.dumps(report, indent=2))
    elif not args.output:
        print_text_report(report)


if __name__ == "__main__":
    main()
