#!/usr/bin/env python3
"""
IFRA Limit Checker Utility

A utility script for checking fragrance formulations against IFRA Standards.
Calculates final concentrations and verifies compliance with category-specific limits.

Author: claude-cosmetic-skills
Version: 1.0.0
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum
import json


class IFRACategory(Enum):
    """IFRA Product Categories 1-11"""
    CAT_1 = 1   # Lip products
    CAT_2 = 2   # Deodorants, intimate care
    CAT_3 = 3   # Fine fragrances (hydroalcoholic)
    CAT_4 = 4   # Body/face creams (non-hydroalcoholic)
    CAT_5 = 5   # Women's facial products
    CAT_6 = 6   # Oral care products
    CAT_7 = 7   # Rinse-off hair care
    CAT_8 = 8   # Leave-on hair care
    CAT_9 = 9   # Rinse-off body care
    CAT_10 = 10 # Household products
    CAT_11 = 11 # Candles, air fresheners


@dataclass
class IFRALimit:
    """IFRA limit data for a substance"""
    substance_name: str
    cas_number: str
    limits: dict[int, float]  # Category -> Max %
    prohibited: bool = False
    specification: Optional[str] = None


@dataclass
class ComplianceResult:
    """Result of an IFRA compliance check"""
    substance_name: str
    cas_number: str
    category: int
    final_concentration: float
    limit: float
    is_compliant: bool
    margin: float  # How much under/over limit (%)
    warning: Optional[str] = None


# Common IFRA restricted substances database
# Values based on 51st Amendment (simplified - verify with official sources)
IFRA_DATABASE: dict[str, IFRALimit] = {
    "coumarin": IFRALimit(
        substance_name="Coumarin",
        cas_number="91-64-5",
        limits={
            1: 0.02, 2: 0.17, 3: 2.5, 4: 0.83, 5: 0.08,
            6: 1.25, 7: 0.5, 8: 0.83, 9: 1.67, 10: 1.67, 11: 8.3
        }
    ),
    "citral": IFRALimit(
        substance_name="Citral",
        cas_number="5392-40-5",
        limits={
            1: 0.02, 2: 0.06, 3: 0.6, 4: 0.2, 5: 0.02,
            6: 0.3, 7: 0.12, 8: 0.2, 9: 0.4, 10: 0.4, 11: 2.0
        }
    ),
    "cinnamal": IFRALimit(
        substance_name="Cinnamal",
        cas_number="104-55-2",
        limits={
            1: 0.005, 2: 0.01, 3: 0.05, 4: 0.05, 5: 0.005,
            6: 0.05, 7: 0.02, 8: 0.05, 9: 0.05, 10: 0.05, 11: 0.2
        }
    ),
    "eugenol": IFRALimit(
        substance_name="Eugenol",
        cas_number="97-53-0",
        limits={
            1: 0.08, 2: 0.15, 3: 1.0, 4: 0.5, 5: 0.05,
            6: 0.75, 7: 0.3, 8: 0.5, 9: 1.0, 10: 1.0, 11: 5.0
        }
    ),
    "isoeugenol": IFRALimit(
        substance_name="Isoeugenol",
        cas_number="97-54-1",
        limits={
            1: 0.006, 2: 0.013, 3: 0.2, 4: 0.065, 5: 0.006,
            6: 0.1, 7: 0.04, 8: 0.065, 9: 0.13, 10: 0.13, 11: 0.65
        }
    ),
    "hydroxycitronellal": IFRALimit(
        substance_name="Hydroxycitronellal",
        cas_number="107-75-5",
        limits={
            1: 0.1, 2: 0.2, 3: 1.5, 4: 0.5, 5: 0.05,
            6: 0.75, 7: 0.3, 8: 0.5, 9: 1.0, 10: 1.0, 11: 5.0
        }
    ),
    "oakmoss": IFRALimit(
        substance_name="Oakmoss (Evernia prunastri)",
        cas_number="90028-68-5",
        limits={
            1: 0.01, 2: 0.02, 3: 0.1, 4: 0.1, 5: 0.1,
            6: 0.1, 7: 0.1, 8: 0.1, 9: 0.1, 10: 0.1, 11: 0.1
        },
        specification="Atranol < 100 ppm, Chloroatranol < 100 ppm"
    ),
    "treemoss": IFRALimit(
        substance_name="Treemoss (Evernia furfuracea)",
        cas_number="90028-67-4",
        limits={
            1: 0.01, 2: 0.02, 3: 0.1, 4: 0.1, 5: 0.1,
            6: 0.1, 7: 0.1, 8: 0.1, 9: 0.1, 10: 0.1, 11: 0.1
        },
        specification="Atranol < 100 ppm, Chloroatranol < 100 ppm"
    ),
    "hicc": IFRALimit(
        substance_name="HICC (Lyral)",
        cas_number="31906-04-4",
        limits={},
        prohibited=True
    ),
    "lilial": IFRALimit(
        substance_name="Lilial (Butylphenyl methylpropional)",
        cas_number="80-54-6",
        limits={},
        prohibited=True
    ),
    "linalool": IFRALimit(
        substance_name="Linalool",
        cas_number="78-70-6",
        limits={
            1: 0.6, 2: 1.7, 3: 15.0, 4: 5.7, 5: 0.6,
            6: 8.5, 7: 3.4, 8: 5.7, 9: 11.4, 10: 11.4, 11: 100.0
        },
        specification="Peroxide value < 20 mmol/L"
    ),
    "limonene": IFRALimit(
        substance_name="d-Limonene",
        cas_number="5989-27-5",
        limits={
            1: 0.7, 2: 2.0, 3: 16.6, 4: 6.6, 5: 0.7,
            6: 10.0, 7: 4.0, 8: 6.6, 9: 13.3, 10: 13.3, 11: 100.0
        },
        specification="Peroxide value < 20 mmol/L"
    ),
    "geraniol": IFRALimit(
        substance_name="Geraniol",
        cas_number="106-24-1",
        limits={
            1: 0.3, 2: 0.9, 3: 8.8, 4: 2.9, 5: 0.3,
            6: 4.4, 7: 1.8, 8: 2.9, 9: 5.9, 10: 5.9, 11: 29.4
        }
    ),
    "citronellol": IFRALimit(
        substance_name="Citronellol",
        cas_number="106-22-9",
        limits={
            1: 0.7, 2: 1.8, 3: 17.5, 4: 5.8, 5: 0.6,
            6: 8.8, 7: 3.5, 8: 5.8, 9: 11.7, 10: 11.7, 11: 58.3
        }
    ),
    "benzyl_benzoate": IFRALimit(
        substance_name="Benzyl benzoate",
        cas_number="120-51-4",
        limits={
            1: 0.4, 2: 1.0, 3: 9.7, 4: 3.2, 5: 0.3,
            6: 4.8, 7: 1.9, 8: 3.2, 9: 6.5, 10: 6.5, 11: 32.3
        }
    ),
    "benzyl_salicylate": IFRALimit(
        substance_name="Benzyl salicylate",
        cas_number="118-58-1",
        limits={
            1: 0.04, 2: 0.07, 3: 0.7, 4: 0.24, 5: 0.02,
            6: 0.35, 7: 0.14, 8: 0.24, 9: 0.48, 10: 0.48, 11: 2.4
        }
    ),
}


def calculate_final_concentration(
    ingredient_in_fragrance: float,
    fragrance_in_product: float
) -> float:
    """
    Calculate final ingredient concentration in finished product.

    Args:
        ingredient_in_fragrance: % of ingredient in fragrance compound
        fragrance_in_product: % of fragrance compound in finished product

    Returns:
        Final % of ingredient in finished product
    """
    return (ingredient_in_fragrance * fragrance_in_product) / 100


def check_ifra_compliance(
    substance_key: str,
    category: int,
    ingredient_in_fragrance: float,
    fragrance_in_product: float
) -> ComplianceResult:
    """
    Check if a substance is IFRA compliant for a given category.

    Args:
        substance_key: Key in IFRA_DATABASE (lowercase, underscore)
        category: IFRA category (1-11)
        ingredient_in_fragrance: % in fragrance compound
        fragrance_in_product: % fragrance in product

    Returns:
        ComplianceResult with compliance status
    """
    if substance_key not in IFRA_DATABASE:
        raise ValueError(f"Unknown substance: {substance_key}")

    if category < 1 or category > 11:
        raise ValueError(f"Invalid category: {category}. Must be 1-11.")

    substance = IFRA_DATABASE[substance_key]
    final_conc = calculate_final_concentration(ingredient_in_fragrance, fragrance_in_product)

    # Check if prohibited
    if substance.prohibited:
        return ComplianceResult(
            substance_name=substance.substance_name,
            cas_number=substance.cas_number,
            category=category,
            final_concentration=final_conc,
            limit=0.0,
            is_compliant=False,
            margin=-100.0,
            warning=f"PROHIBITED: {substance.substance_name} is not allowed in fragrances."
        )

    limit = substance.limits.get(category, 0.0)
    is_compliant = final_conc <= limit
    margin = ((limit - final_conc) / limit) * 100 if limit > 0 else 0.0

    warning = None
    if substance.specification:
        warning = f"Specification required: {substance.specification}"

    if not is_compliant:
        warning = f"EXCEEDS LIMIT: {final_conc:.4f}% > {limit:.4f}% maximum"
    elif margin < 10:
        warning = f"WARNING: Within 10% of limit ({margin:.1f}% margin)"

    return ComplianceResult(
        substance_name=substance.substance_name,
        cas_number=substance.cas_number,
        category=category,
        final_concentration=final_conc,
        limit=limit,
        is_compliant=is_compliant,
        margin=margin,
        warning=warning
    )


def check_formulation(
    category: int,
    fragrance_in_product: float,
    ingredients: dict[str, float]
) -> list[ComplianceResult]:
    """
    Check an entire fragrance formulation for IFRA compliance.

    Args:
        category: IFRA category (1-11)
        fragrance_in_product: % fragrance in finished product
        ingredients: Dict of {substance_key: % in fragrance compound}

    Returns:
        List of ComplianceResult for each ingredient
    """
    results = []
    for substance_key, pct_in_fragrance in ingredients.items():
        try:
            result = check_ifra_compliance(
                substance_key,
                category,
                pct_in_fragrance,
                fragrance_in_product
            )
            results.append(result)
        except ValueError as e:
            print(f"Skipping {substance_key}: {e}")

    return results


def print_compliance_report(results: list[ComplianceResult]) -> None:
    """Print a formatted compliance report."""
    print("\n" + "=" * 70)
    print("IFRA COMPLIANCE REPORT")
    print("=" * 70)

    compliant_count = sum(1 for r in results if r.is_compliant)
    total_count = len(results)

    print(f"\nCategory: {results[0].category if results else 'N/A'}")
    print(f"Total substances checked: {total_count}")
    print(f"Compliant: {compliant_count}")
    print(f"Non-compliant: {total_count - compliant_count}")

    print("\n" + "-" * 70)
    print(f"{'Substance':<25} {'Final %':<10} {'Limit %':<10} {'Status':<15}")
    print("-" * 70)

    for r in sorted(results, key=lambda x: x.is_compliant):
        status = "OK" if r.is_compliant else "FAIL"
        status_marker = "[OK]" if r.is_compliant else "[FAIL]"
        print(f"{r.substance_name:<25} {r.final_concentration:<10.4f} {r.limit:<10.4f} {status_marker:<15}")
        if r.warning:
            print(f"   >> {r.warning}")

    print("-" * 70)

    if compliant_count == total_count:
        print("\n[PASS] All substances are within IFRA limits.")
    else:
        print(f"\n[WARNING] {total_count - compliant_count} substance(s) exceed IFRA limits!")

    print("=" * 70 + "\n")


def get_category_description(category: int) -> str:
    """Get description for an IFRA category."""
    descriptions = {
        1: "Lip products, toys with oral contact",
        2: "Deodorants, antiperspirants, intimate care",
        3: "Fine fragrances (hydroalcoholic) - EdP, EdT, cologne",
        4: "Body/face creams, lotions (non-hydroalcoholic)",
        5: "Women's facial products, eye area",
        6: "Oral care - mouthwash, toothpaste",
        7: "Hair care (rinse-off) - shampoo, conditioner",
        8: "Hair care (leave-on) - styling products",
        9: "Body care (rinse-off) - shower gel, soap",
        10: "Household products - detergent, cleaners",
        11: "Air fresheners, candles, diffusers"
    }
    return descriptions.get(category, "Unknown category")


def list_available_substances() -> None:
    """Print all available substances in the database."""
    print("\nAvailable substances in database:")
    print("-" * 50)
    for key, substance in sorted(IFRA_DATABASE.items()):
        status = "[PROHIBITED]" if substance.prohibited else ""
        print(f"  {key:<25} - {substance.substance_name} {status}")
    print("-" * 50)


# Example usage and demonstration
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("IFRA LIMIT CHECKER UTILITY - Demo")
    print("=" * 70)

    # List available substances
    list_available_substances()

    # Example: Check a fine fragrance (Category 3) formulation
    print("\n--- Example: Fine Fragrance (Category 3) ---")
    print("Fragrance compound at 15% in product")

    example_formulation = {
        "linalool": 20.0,      # 20% linalool in fragrance
        "limonene": 15.0,      # 15% d-limonene in fragrance
        "citral": 2.0,         # 2% citral in fragrance
        "coumarin": 5.0,       # 5% coumarin in fragrance
        "eugenol": 3.0,        # 3% eugenol in fragrance
        "geraniol": 8.0,       # 8% geraniol in fragrance
    }

    results = check_formulation(
        category=3,
        fragrance_in_product=15.0,
        ingredients=example_formulation
    )

    print_compliance_report(results)

    # Example: Check a body lotion (Category 4)
    print("\n--- Example: Body Lotion (Category 4) ---")
    print("Fragrance compound at 1% in product")

    body_lotion_formulation = {
        "linalool": 25.0,
        "citronellol": 15.0,
        "hydroxycitronellal": 10.0,
        "benzyl_salicylate": 5.0,
    }

    results = check_formulation(
        category=4,
        fragrance_in_product=1.0,
        ingredients=body_lotion_formulation
    )

    print_compliance_report(results)

    # Example: Check a prohibited substance
    print("\n--- Example: Prohibited Substance Check ---")
    result = check_ifra_compliance("hicc", 3, 1.0, 10.0)
    print(f"Substance: {result.substance_name}")
    print(f"Compliant: {result.is_compliant}")
    print(f"Warning: {result.warning}")

    # Category descriptions
    print("\n--- IFRA Category Descriptions ---")
    for cat in range(1, 12):
        print(f"Category {cat}: {get_category_description(cat)}")
