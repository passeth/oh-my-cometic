#!/usr/bin/env python3
"""
Regulatory Batch Checker for Cosmetic Ingredients

A utility script for batch checking cosmetic ingredient regulatory compliance
across multiple countries (Korea, EU, USA, China, Japan, ASEAN).

Usage:
    python regulatory_batch_checker.py --input ingredients.csv --countries Korea,EU,USA --output report.xlsx
    python regulatory_batch_checker.py --input formulation.csv --all-countries --output compliance_report.xlsx
    python regulatory_batch_checker.py --ingredient "Niacinamide" --concentration 5 --countries Korea,EU

Author: claude-cosmetic-skills
Version: 1.0.0
"""

import argparse
import csv
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional


class ComplianceStatus(Enum):
    """Compliance status for ingredients."""
    ALLOWED = "allowed"
    RESTRICTED = "restricted"
    PROHIBITED = "prohibited"
    UNKNOWN = "unknown"
    REQUIRES_REVIEW = "requires_review"


class Country(Enum):
    """Supported countries/regions for regulatory checking."""
    KOREA = "Korea"
    EU = "EU"
    USA = "USA"
    CHINA = "China"
    JAPAN = "Japan"
    ASEAN = "ASEAN"


@dataclass
class IngredientCheck:
    """Result of checking a single ingredient."""
    inci_name: str
    concentration: Optional[float]
    country: Country
    status: ComplianceStatus
    max_allowed: Optional[float] = None
    notes: str = ""
    warnings: list = field(default_factory=list)
    alternatives: list = field(default_factory=list)


@dataclass
class ComplianceReport:
    """Complete compliance report for a formulation."""
    product_name: str
    check_date: str
    countries_checked: list
    total_ingredients: int
    results: list = field(default_factory=list)
    summary: dict = field(default_factory=dict)


# Regulatory database (simplified version - in production, use comprehensive database)
REGULATORY_DATABASE = {
    # Prohibited ingredients
    "prohibited": {
        "hydroquinone": {
            Country.KOREA: True,
            Country.EU: True,
            Country.USA: False,  # Allowed as OTC drug at 2%
            Country.CHINA: True,
            Country.JAPAN: True,
            Country.ASEAN: True,
        },
        "mercury": {
            Country.KOREA: True,
            Country.EU: True,
            Country.USA: True,
            Country.CHINA: True,
            Country.JAPAN: True,
            Country.ASEAN: True,
        },
        "methylisothiazolinone": {
            Country.KOREA: True,  # Completely banned
            Country.EU: False,  # Restricted in leave-on
            Country.USA: False,
            Country.CHINA: False,
            Country.JAPAN: True,
            Country.ASEAN: False,
        },
    },

    # Restricted ingredients with maximum concentrations
    "restricted": {
        "retinol": {
            Country.KOREA: {"max": 0.5, "category": "functional"},
            Country.EU: {"max": 0.3, "warning_threshold": 0.05, "warning": "Retinol warning required"},
            Country.USA: {"max": None, "notes": "No specific limit"},
            Country.CHINA: {"max": 0.5, "category": "special"},
            Country.JAPAN: {"max": None, "category": "quasi-drug for high concentrations"},
            Country.ASEAN: {"max": 0.5},
        },
        "salicylic acid": {
            Country.KOREA: {"max": 2.0, "use": "acne products"},
            Country.EU: {"max": 2.0},
            Country.USA: {"max": 2.0, "category": "OTC acne"},
            Country.CHINA: {"max": 2.0},
            Country.JAPAN: {"max": 0.2, "cosmetic_max": 0.2},
            Country.ASEAN: {"max": 2.0},
        },
        "phenoxyethanol": {
            Country.KOREA: {"max": 1.0},
            Country.EU: {"max": 1.0},
            Country.USA: {"max": None, "notes": "Safe for intended use"},
            Country.CHINA: {"max": 1.0},
            Country.JAPAN: {"max": 1.0},
            Country.ASEAN: {"max": 1.0},
        },
        "niacinamide": {
            Country.KOREA: {"max": None, "functional_threshold": 2.0},
            Country.EU: {"max": None},
            Country.USA: {"max": None},
            Country.CHINA: {"max": None},
            Country.JAPAN: {"max": None},
            Country.ASEAN: {"max": None},
        },
        "arbutin": {
            Country.KOREA: {"max": 7.0, "category": "functional"},
            Country.EU: {"max": 7.0},
            Country.USA: {"max": None},
            Country.CHINA: {"max": 7.0, "category": "special"},
            Country.JAPAN: {"max": None, "category": "quasi-drug"},
            Country.ASEAN: {"max": 7.0},
        },
        "titanium dioxide": {
            Country.KOREA: {"max": 25.0},
            Country.EU: {"max": 25.0, "nano_labeling": True},
            Country.USA: {"max": 25.0},
            Country.CHINA: {"max": 25.0},
            Country.JAPAN: {"max": None, "no_limit": True},
            Country.ASEAN: {"max": 25.0},
        },
        "avobenzone": {
            Country.KOREA: {"max": 5.0, "category": "UV filter"},
            Country.EU: {"max": 5.0},
            Country.USA: {"max": 3.0},
            Country.CHINA: {"max": 5.0},
            Country.JAPAN: {"max": 5.0},
            Country.ASEAN: {"max": 5.0},
        },
        "octocrylene": {
            Country.KOREA: {"max": 10.0, "category": "UV filter"},
            Country.EU: {"max": 10.0, "under_review": True, "warning": "Under SCCS review"},
            Country.USA: {"max": 10.0},
            Country.CHINA: {"max": 10.0},
            Country.JAPAN: {"max": 10.0},
            Country.ASEAN: {"max": 10.0},
        },
        "methylparaben": {
            Country.KOREA: {"max": 0.4},
            Country.EU: {"max": 0.4},
            Country.USA: {"max": None},
            Country.CHINA: {"max": 0.4},
            Country.JAPAN: {"max": 1.0},
            Country.ASEAN: {"max": 0.4},
        },
        "propylparaben": {
            Country.KOREA: {"max": 0.14},
            Country.EU: {"max": 0.14},
            Country.USA: {"max": None},
            Country.CHINA: {"max": 0.14},
            Country.JAPAN: {"max": 1.0},
            Country.ASEAN: {"max": 0.14},
        },
        "glycolic acid": {
            Country.KOREA: {"max": 10.0, "min_ph": 3.5},
            Country.EU: {"max": 10.0, "min_ph": 3.5},
            Country.USA: {"max": None, "professional_use": "higher allowed"},
            Country.CHINA: {"max": 6.0},
            Country.JAPAN: {"max": 10.0},
            Country.ASEAN: {"max": 10.0},
        },
        "tranexamic acid": {
            Country.KOREA: {"max": 2.0, "category": "functional"},
            Country.EU: {"max": None},
            Country.USA: {"max": None},
            Country.CHINA: {"max": None, "category": "special"},
            Country.JAPAN: {"max": None, "category": "quasi-drug"},
            Country.ASEAN: {"max": None},
        },
    },
}


def normalize_ingredient_name(name: str) -> str:
    """Normalize ingredient name for database lookup."""
    return name.lower().strip().replace("-", " ").replace("_", " ")


def check_single_ingredient(
    inci_name: str,
    concentration: Optional[float],
    country: Country
) -> IngredientCheck:
    """
    Check a single ingredient against regulatory requirements for a country.

    Args:
        inci_name: INCI name of the ingredient
        concentration: Concentration in percentage (optional)
        country: Target country/region

    Returns:
        IngredientCheck with compliance status and details
    """
    normalized_name = normalize_ingredient_name(inci_name)
    result = IngredientCheck(
        inci_name=inci_name,
        concentration=concentration,
        country=country,
        status=ComplianceStatus.UNKNOWN,
    )

    # Check prohibited list first
    if normalized_name in REGULATORY_DATABASE["prohibited"]:
        prohibited_data = REGULATORY_DATABASE["prohibited"][normalized_name]
        if country in prohibited_data and prohibited_data[country]:
            result.status = ComplianceStatus.PROHIBITED
            result.notes = f"Prohibited in {country.value}"
            result.warnings.append(f"CRITICAL: {inci_name} is prohibited in {country.value}")

            # Suggest alternatives
            if normalized_name == "hydroquinone":
                result.alternatives = ["Arbutin", "Alpha-Arbutin", "Niacinamide", "Kojic Acid"]
            elif normalized_name == "methylisothiazolinone":
                result.alternatives = ["Phenoxyethanol", "Benzyl Alcohol", "Ethylhexylglycerin"]

            return result

    # Check restricted list
    if normalized_name in REGULATORY_DATABASE["restricted"]:
        restricted_data = REGULATORY_DATABASE["restricted"][normalized_name]
        if country in restricted_data:
            country_data = restricted_data[country]
            max_limit = country_data.get("max")

            result.max_allowed = max_limit

            # Check concentration against limit
            if concentration is not None and max_limit is not None:
                if concentration > max_limit:
                    result.status = ComplianceStatus.PROHIBITED
                    result.notes = f"Exceeds maximum limit of {max_limit}%"
                    result.warnings.append(
                        f"Concentration {concentration}% exceeds max {max_limit}% for {country.value}"
                    )
                else:
                    result.status = ComplianceStatus.RESTRICTED
                    result.notes = f"Within limit (max: {max_limit}%)"
            elif max_limit is None:
                result.status = ComplianceStatus.ALLOWED
                result.notes = country_data.get("notes", "No specific limit")
            else:
                result.status = ComplianceStatus.RESTRICTED
                result.notes = f"Maximum allowed: {max_limit}%"

            # Add warnings and notes
            if "warning" in country_data:
                result.warnings.append(country_data["warning"])
            if "category" in country_data:
                result.notes += f" | Category: {country_data['category']}"
            if country_data.get("under_review"):
                result.warnings.append(f"Currently under regulatory review in {country.value}")
            if "warning_threshold" in country_data and concentration:
                if concentration > country_data["warning_threshold"]:
                    result.warnings.append(
                        f"Warning statement required above {country_data['warning_threshold']}%"
                    )

            return result

    # If not in database, mark as requires review
    result.status = ComplianceStatus.REQUIRES_REVIEW
    result.notes = "Not in database - manual verification recommended"

    return result


def batch_check_ingredients(
    ingredients: list,
    countries: list
) -> ComplianceReport:
    """
    Batch check multiple ingredients across multiple countries.

    Args:
        ingredients: List of dicts with 'name' and 'concentration' keys
        countries: List of Country enums to check against

    Returns:
        ComplianceReport with all results
    """
    report = ComplianceReport(
        product_name="Batch Check",
        check_date=datetime.now().isoformat(),
        countries_checked=[c.value for c in countries],
        total_ingredients=len(ingredients),
    )

    # Initialize summary counters
    for country in countries:
        report.summary[country.value] = {
            "allowed": 0,
            "restricted": 0,
            "prohibited": 0,
            "unknown": 0,
            "requires_review": 0,
        }

    # Check each ingredient against each country
    for ingredient in ingredients:
        name = ingredient.get("name", ingredient.get("inci_name", ""))
        concentration = ingredient.get("concentration")

        if concentration is not None:
            try:
                concentration = float(concentration)
            except (ValueError, TypeError):
                concentration = None

        for country in countries:
            result = check_single_ingredient(name, concentration, country)
            report.results.append(result)

            # Update summary
            status_key = result.status.value
            report.summary[country.value][status_key] += 1

    return report


def load_ingredients_from_csv(filepath: str) -> list:
    """Load ingredients from a CSV file."""
    ingredients = []

    with open(filepath, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Handle various column name formats
            name = (
                row.get("INCI Name") or
                row.get("inci_name") or
                row.get("Ingredient") or
                row.get("ingredient") or
                row.get("Name") or
                row.get("name", "")
            )

            concentration = (
                row.get("Concentration") or
                row.get("concentration") or
                row.get("%") or
                row.get("Percent") or
                row.get("percent")
            )

            if name:
                ingredients.append({
                    "name": name.strip(),
                    "concentration": concentration
                })

    return ingredients


def generate_text_report(report: ComplianceReport) -> str:
    """Generate a text-based compliance report."""
    lines = []
    lines.append("=" * 70)
    lines.append("REGULATORY COMPLIANCE REPORT")
    lines.append("=" * 70)
    lines.append(f"Generated: {report.check_date}")
    lines.append(f"Countries Checked: {', '.join(report.countries_checked)}")
    lines.append(f"Total Ingredients: {report.total_ingredients}")
    lines.append("")

    # Summary section
    lines.append("-" * 70)
    lines.append("SUMMARY BY COUNTRY")
    lines.append("-" * 70)

    for country, stats in report.summary.items():
        lines.append(f"\n{country}:")
        lines.append(f"  Allowed:        {stats['allowed']}")
        lines.append(f"  Restricted:     {stats['restricted']}")
        lines.append(f"  Prohibited:     {stats['prohibited']}")
        lines.append(f"  Unknown:        {stats['unknown']}")
        lines.append(f"  Requires Review: {stats['requires_review']}")

    # Detailed results - group by status
    lines.append("\n" + "-" * 70)
    lines.append("CRITICAL ISSUES (Prohibited Ingredients)")
    lines.append("-" * 70)

    prohibited = [r for r in report.results if r.status == ComplianceStatus.PROHIBITED]
    if prohibited:
        for result in prohibited:
            lines.append(f"\n[PROHIBITED] {result.inci_name}")
            lines.append(f"  Country: {result.country.value}")
            if result.concentration:
                lines.append(f"  Concentration: {result.concentration}%")
            lines.append(f"  Notes: {result.notes}")
            if result.warnings:
                for warning in result.warnings:
                    lines.append(f"  WARNING: {warning}")
            if result.alternatives:
                lines.append(f"  Alternatives: {', '.join(result.alternatives)}")
    else:
        lines.append("\nNo prohibited ingredients found.")

    # Restricted ingredients
    lines.append("\n" + "-" * 70)
    lines.append("RESTRICTED INGREDIENTS")
    lines.append("-" * 70)

    restricted = [r for r in report.results if r.status == ComplianceStatus.RESTRICTED]
    if restricted:
        for result in restricted:
            lines.append(f"\n[RESTRICTED] {result.inci_name}")
            lines.append(f"  Country: {result.country.value}")
            if result.concentration:
                lines.append(f"  Concentration: {result.concentration}%")
            if result.max_allowed:
                lines.append(f"  Max Allowed: {result.max_allowed}%")
            lines.append(f"  Notes: {result.notes}")
            if result.warnings:
                for warning in result.warnings:
                    lines.append(f"  Note: {warning}")
    else:
        lines.append("\nNo restricted ingredients found.")

    # Items requiring review
    lines.append("\n" + "-" * 70)
    lines.append("ITEMS REQUIRING MANUAL REVIEW")
    lines.append("-" * 70)

    review = [r for r in report.results if r.status == ComplianceStatus.REQUIRES_REVIEW]
    if review:
        # Get unique ingredients
        unique_ingredients = set(r.inci_name for r in review)
        for name in unique_ingredients:
            lines.append(f"  - {name}")
    else:
        lines.append("\nNo items requiring manual review.")

    lines.append("\n" + "=" * 70)
    lines.append("END OF REPORT")
    lines.append("=" * 70)

    return "\n".join(lines)


def generate_json_report(report: ComplianceReport) -> str:
    """Generate a JSON compliance report."""
    output = {
        "report_metadata": {
            "product_name": report.product_name,
            "check_date": report.check_date,
            "countries_checked": report.countries_checked,
            "total_ingredients": report.total_ingredients,
        },
        "summary": report.summary,
        "results": [],
    }

    for result in report.results:
        output["results"].append({
            "inci_name": result.inci_name,
            "concentration": result.concentration,
            "country": result.country.value,
            "status": result.status.value,
            "max_allowed": result.max_allowed,
            "notes": result.notes,
            "warnings": result.warnings,
            "alternatives": result.alternatives,
        })

    return json.dumps(output, indent=2, ensure_ascii=False)


def generate_csv_report(report: ComplianceReport) -> str:
    """Generate a CSV compliance report."""
    lines = []

    # Header
    headers = [
        "INCI Name",
        "Concentration (%)",
        "Country",
        "Status",
        "Max Allowed (%)",
        "Notes",
        "Warnings",
        "Alternatives"
    ]
    lines.append(",".join(headers))

    # Data rows
    for result in report.results:
        row = [
            f'"{result.inci_name}"',
            str(result.concentration) if result.concentration else "",
            result.country.value,
            result.status.value,
            str(result.max_allowed) if result.max_allowed else "",
            f'"{result.notes}"',
            f'"{"; ".join(result.warnings)}"',
            f'"{"; ".join(result.alternatives)}"',
        ]
        lines.append(",".join(row))

    return "\n".join(lines)


def main():
    """Main entry point for the regulatory batch checker."""
    parser = argparse.ArgumentParser(
        description="Batch check cosmetic ingredient regulatory compliance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input ingredients.csv --countries Korea,EU,USA --output report.txt
  %(prog)s --input formulation.csv --all-countries --format json --output report.json
  %(prog)s --ingredient "Niacinamide" --concentration 5 --countries Korea,EU
  %(prog)s --ingredient "Retinol" --concentration 0.5 --all-countries
        """
    )

    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--input", "-i",
        help="Input CSV file with ingredients (columns: name/INCI Name, concentration)"
    )
    input_group.add_argument(
        "--ingredient",
        help="Single ingredient INCI name to check"
    )

    parser.add_argument(
        "--concentration", "-c",
        type=float,
        help="Concentration in percent (for single ingredient check)"
    )

    # Country options
    country_group = parser.add_mutually_exclusive_group(required=True)
    country_group.add_argument(
        "--countries",
        help="Comma-separated list of countries (Korea,EU,USA,China,Japan,ASEAN)"
    )
    country_group.add_argument(
        "--all-countries",
        action="store_true",
        help="Check against all supported countries"
    )

    # Output options
    parser.add_argument(
        "--output", "-o",
        help="Output file path (optional, prints to stdout if not specified)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["text", "json", "csv"],
        default="text",
        help="Output format (default: text)"
    )

    args = parser.parse_args()

    # Parse countries
    if args.all_countries:
        countries = list(Country)
    else:
        country_map = {
            "korea": Country.KOREA,
            "eu": Country.EU,
            "usa": Country.USA,
            "us": Country.USA,
            "china": Country.CHINA,
            "japan": Country.JAPAN,
            "asean": Country.ASEAN,
        }
        countries = []
        for c in args.countries.split(","):
            c_lower = c.strip().lower()
            if c_lower in country_map:
                countries.append(country_map[c_lower])
            else:
                print(f"Warning: Unknown country '{c}', skipping", file=sys.stderr)

    if not countries:
        print("Error: No valid countries specified", file=sys.stderr)
        sys.exit(1)

    # Load ingredients
    if args.input:
        filepath = Path(args.input)
        if not filepath.exists():
            print(f"Error: Input file not found: {args.input}", file=sys.stderr)
            sys.exit(1)
        ingredients = load_ingredients_from_csv(args.input)
        if not ingredients:
            print("Error: No ingredients found in input file", file=sys.stderr)
            sys.exit(1)
    else:
        ingredients = [{
            "name": args.ingredient,
            "concentration": args.concentration
        }]

    # Run batch check
    report = batch_check_ingredients(ingredients, countries)

    # Generate output
    if args.format == "json":
        output = generate_json_report(report)
    elif args.format == "csv":
        output = generate_csv_report(report)
    else:
        output = generate_text_report(report)

    # Write output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Report saved to: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
