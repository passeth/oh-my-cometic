#!/usr/bin/env python3
"""
Cosmetic Efficacy Report Validation Script

Validates cosmetic efficacy clinical trial reports for completeness
and compliance with MFDS (Korea Food and Drug Safety) guidelines.

Checks for:
- Required sections presence
- Statistical analysis completeness
- Sample size adequacy
- Endpoint reporting
- Safety data inclusion
"""

import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime


# Required sections for efficacy reports
REQUIRED_SECTIONS = {
    "whitening": [
        "study summary",
        "study objective",
        "ethics",
        "irb approval",
        "informed consent",
        "test materials",
        "subject selection",
        "inclusion criteria",
        "exclusion criteria",
        "study design",
        "efficacy assessments",
        "melanin index",
        "colorimetry",
        "statistical analysis",
        "subject disposition",
        "demographics",
        "efficacy results",
        "safety results",
        "adverse events",
        "conclusion",
    ],
    "antiwrinkle": [
        "study summary",
        "study objective",
        "ethics",
        "irb approval",
        "informed consent",
        "test materials",
        "subject selection",
        "study design",
        "efficacy assessments",
        "skin roughness",
        "elasticity",
        "statistical analysis",
        "subject disposition",
        "demographics",
        "efficacy results",
        "safety results",
        "adverse events",
        "conclusion",
    ],
    "moisturizing": [
        "study summary",
        "study objective",
        "ethics",
        "test materials",
        "subject selection",
        "study design",
        "efficacy assessments",
        "hydration",
        "corneometer",
        "statistical analysis",
        "subject disposition",
        "efficacy results",
        "safety results",
        "conclusion",
    ],
}

# Minimum requirements by efficacy type
MIN_REQUIREMENTS = {
    "whitening": {
        "subjects": 20,
        "duration_weeks": 8,
        "primary_endpoints": ["melanin", "l*", "ita"],
    },
    "antiwrinkle": {
        "subjects": 20,
        "duration_weeks": 8,
        "primary_endpoints": ["roughness", "ra", "rz", "elasticity", "r2", "r5"],
    },
    "moisturizing": {
        "subjects": 20,
        "duration_weeks": 4,
        "primary_endpoints": ["hydration", "corneometer", "tewl"],
    },
}

# Statistical terms to check
STATISTICAL_TERMS = [
    "p-value",
    "p<",
    "p =",
    "statistical",
    "significant",
    "confidence interval",
    "mean",
    "standard deviation",
    "sd",
    "±",
    "wilcoxon",
    "t-test",
    "anova",
    "mann-whitney",
]


def detect_efficacy_type(content: str) -> str:
    """Detect the type of efficacy report based on content."""
    content_lower = content.lower()

    # Count keyword occurrences
    whitening_keywords = ["whitening", "미백", "melanin", "brightening", "pigment"]
    antiwrinkle_keywords = ["wrinkle", "주름", "elasticity", "탄력", "roughness"]
    moisturizing_keywords = ["moistur", "보습", "hydration", "tewl", "corneometer"]

    whitening_count = sum(content_lower.count(kw) for kw in whitening_keywords)
    antiwrinkle_count = sum(content_lower.count(kw) for kw in antiwrinkle_keywords)
    moisturizing_count = sum(content_lower.count(kw) for kw in moisturizing_keywords)

    max_count = max(whitening_count, antiwrinkle_count, moisturizing_count)

    if max_count == whitening_count:
        return "whitening"
    elif max_count == antiwrinkle_count:
        return "antiwrinkle"
    else:
        return "moisturizing"


def check_sections(content: str, efficacy_type: str) -> Tuple[List[str], List[str]]:
    """Check for presence of required sections."""
    content_lower = content.lower()
    required = REQUIRED_SECTIONS.get(efficacy_type, REQUIRED_SECTIONS["whitening"])

    present = []
    missing = []

    for section in required:
        if section in content_lower:
            present.append(section)
        else:
            missing.append(section)

    return present, missing


def extract_sample_size(content: str) -> int:
    """Extract sample size from report content."""
    patterns = [
        r"n\s*=\s*(\d+)",
        r"(\d+)\s*subjects",
        r"(\d+)\s*피험자",
        r"sample size[:\s]+(\d+)",
        r"enrolled[:\s]+(\d+)",
    ]

    for pattern in patterns:
        matches = re.findall(pattern, content.lower())
        if matches:
            # Return the largest number found (likely total enrolled)
            return max(int(m) for m in matches)

    return 0


def extract_duration(content: str) -> int:
    """Extract study duration in weeks."""
    patterns = [
        r"(\d+)\s*weeks?",
        r"(\d+)\s*주",
        r"duration[:\s]+(\d+)",
    ]

    for pattern in patterns:
        matches = re.findall(pattern, content.lower())
        if matches:
            return max(int(m) for m in matches)

    return 0


def check_statistical_analysis(content: str) -> Dict[str, bool]:
    """Check for statistical analysis components."""
    content_lower = content.lower()

    checks = {
        "has_pvalue": any(
            term in content_lower for term in ["p-value", "p<", "p =", "p="]
        ),
        "has_mean_sd": "±" in content
        or (
            "mean" in content_lower
            and ("sd" in content_lower or "standard deviation" in content_lower)
        ),
        "has_statistical_test": any(
            term in content_lower
            for term in ["t-test", "wilcoxon", "anova", "mann-whitney"]
        ),
        "has_significance": "significant" in content_lower
        or "p < 0.05" in content_lower,
        "has_baseline_comparison": "baseline" in content_lower
        and ("change" in content_lower or "difference" in content_lower),
    }

    return checks


def check_endpoints(content: str, efficacy_type: str) -> Dict[str, bool]:
    """Check for required endpoints based on efficacy type."""
    content_lower = content.lower()
    requirements = MIN_REQUIREMENTS.get(efficacy_type, MIN_REQUIREMENTS["whitening"])

    endpoint_presence = {}
    for endpoint in requirements["primary_endpoints"]:
        endpoint_presence[endpoint] = endpoint in content_lower

    return endpoint_presence


def check_safety_data(content: str) -> Dict[str, bool]:
    """Check for safety data completeness."""
    content_lower = content.lower()

    checks = {
        "has_adverse_events": "adverse event" in content_lower
        or "이상반응" in content_lower,
        "has_ae_summary": "subjects with" in content_lower
        and ("ae" in content_lower or "adverse" in content_lower),
        "has_tolerability": "tolerability" in content_lower
        or "tolerance" in content_lower,
        "has_safety_conclusion": "safety" in content_lower
        and "conclusion" in content_lower,
    }

    return checks


def check_ethics(content: str) -> Dict[str, bool]:
    """Check for ethics documentation."""
    content_lower = content.lower()

    checks = {
        "has_irb_approval": "irb" in content_lower
        or "institutional review" in content_lower
        or "윤리위원회" in content_lower,
        "has_informed_consent": "informed consent" in content_lower
        or "동의서" in content_lower,
        "has_ethics_statement": "declaration of helsinki" in content_lower
        or "good clinical practice" in content_lower
        or "kgcp" in content_lower,
    }

    return checks


def generate_report(validation_results: Dict[str, Any]) -> str:
    """Generate validation report."""
    report = []
    report.append("=" * 60)
    report.append("COSMETIC EFFICACY REPORT VALIDATION")
    report.append("=" * 60)
    report.append(f"\nFile: {validation_results['file_path']}")
    report.append(f"Efficacy Type: {validation_results['efficacy_type'].upper()}")
    report.append(f"Validation Date: {validation_results['timestamp']}")

    # Overall Score
    report.append(f"\n{'─' * 40}")
    report.append(f"OVERALL COMPLIANCE: {validation_results['overall_score']:.1f}%")
    report.append(f"{'─' * 40}")

    # Section Analysis
    report.append("\n📋 REQUIRED SECTIONS")
    present = validation_results["sections"]["present"]
    missing = validation_results["sections"]["missing"]
    report.append(f"   Present: {len(present)}/{len(present) + len(missing)}")
    if missing:
        report.append(f"   ⚠️  Missing sections:")
        for section in missing[:10]:  # Limit display
            report.append(f"      - {section}")
        if len(missing) > 10:
            report.append(f"      ... and {len(missing) - 10} more")

    # Sample Size
    report.append("\n📊 SAMPLE SIZE")
    sample_size = validation_results["sample_size"]
    min_required = MIN_REQUIREMENTS[validation_results["efficacy_type"]]["subjects"]
    status = "✓" if sample_size >= min_required else "✗"
    report.append(f"   {status} Detected: {sample_size} (minimum: {min_required})")

    # Duration
    report.append("\n⏱️  STUDY DURATION")
    duration = validation_results["duration_weeks"]
    min_duration = MIN_REQUIREMENTS[validation_results["efficacy_type"]][
        "duration_weeks"
    ]
    status = "✓" if duration >= min_duration else "✗"
    report.append(f"   {status} Detected: {duration} weeks (minimum: {min_duration})")

    # Statistical Analysis
    report.append("\n📈 STATISTICAL ANALYSIS")
    stats = validation_results["statistical_analysis"]
    for check, present in stats.items():
        status = "✓" if present else "✗"
        check_name = check.replace("has_", "").replace("_", " ").title()
        report.append(f"   {status} {check_name}")

    # Endpoints
    report.append("\n🎯 PRIMARY ENDPOINTS")
    endpoints = validation_results["endpoints"]
    for endpoint, present in endpoints.items():
        status = "✓" if present else "✗"
        report.append(f"   {status} {endpoint.upper()}")

    # Safety Data
    report.append("\n🛡️  SAFETY DATA")
    safety = validation_results["safety_data"]
    for check, present in safety.items():
        status = "✓" if present else "✗"
        check_name = check.replace("has_", "").replace("_", " ").title()
        report.append(f"   {status} {check_name}")

    # Ethics
    report.append("\n📜 ETHICS DOCUMENTATION")
    ethics = validation_results["ethics"]
    for check, present in ethics.items():
        status = "✓" if present else "✗"
        check_name = check.replace("has_", "").replace("_", " ").title()
        report.append(f"   {status} {check_name}")

    # Recommendations
    report.append(f"\n{'=' * 60}")
    report.append("RECOMMENDATIONS")
    report.append(f"{'=' * 60}")

    recommendations = []

    if missing:
        recommendations.append(f"• Add missing sections: {', '.join(missing[:5])}")

    if sample_size < min_required:
        recommendations.append(
            f"• Sample size ({sample_size}) is below minimum ({min_required})"
        )

    if duration < min_duration:
        recommendations.append(
            f"• Study duration ({duration} weeks) is below minimum ({min_duration})"
        )

    if not all(stats.values()):
        missing_stats = [k.replace("has_", "") for k, v in stats.items() if not v]
        recommendations.append(
            f"• Add statistical elements: {', '.join(missing_stats)}"
        )

    if not all(endpoints.values()):
        missing_endpoints = [k for k, v in endpoints.items() if not v]
        recommendations.append(
            f"• Include endpoint data for: {', '.join(missing_endpoints)}"
        )

    if not all(safety.values()):
        missing_safety = [k.replace("has_", "") for k, v in safety.items() if not v]
        recommendations.append(f"• Add safety information: {', '.join(missing_safety)}")

    if not all(ethics.values()):
        missing_ethics = [k.replace("has_", "") for k, v in ethics.items() if not v]
        recommendations.append(
            f"• Add ethics documentation: {', '.join(missing_ethics)}"
        )

    if recommendations:
        for rec in recommendations:
            report.append(rec)
    else:
        report.append(
            "✓ Report appears complete. Consider final review by regulatory specialist."
        )

    report.append("\n" + "=" * 60)

    return "\n".join(report)


def calculate_overall_score(validation_results: Dict[str, Any]) -> float:
    """Calculate overall compliance score (0-100)."""
    scores = []

    # Section completeness (30%)
    present = len(validation_results["sections"]["present"])
    total = present + len(validation_results["sections"]["missing"])
    section_score = (present / total) * 30 if total > 0 else 0
    scores.append(section_score)

    # Sample size (15%)
    efficacy_type = validation_results["efficacy_type"]
    min_subjects = MIN_REQUIREMENTS[efficacy_type]["subjects"]
    sample_score = 15 if validation_results["sample_size"] >= min_subjects else 0
    scores.append(sample_score)

    # Duration (15%)
    min_duration = MIN_REQUIREMENTS[efficacy_type]["duration_weeks"]
    duration_score = 15 if validation_results["duration_weeks"] >= min_duration else 0
    scores.append(duration_score)

    # Statistical analysis (15%)
    stats = validation_results["statistical_analysis"]
    stats_score = (sum(stats.values()) / len(stats)) * 15 if stats else 0
    scores.append(stats_score)

    # Endpoints (10%)
    endpoints = validation_results["endpoints"]
    endpoint_score = (sum(endpoints.values()) / len(endpoints)) * 10 if endpoints else 0
    scores.append(endpoint_score)

    # Safety (10%)
    safety = validation_results["safety_data"]
    safety_score = (sum(safety.values()) / len(safety)) * 10 if safety else 0
    scores.append(safety_score)

    # Ethics (5%)
    ethics = validation_results["ethics"]
    ethics_score = (sum(ethics.values()) / len(ethics)) * 5 if ethics else 0
    scores.append(ethics_score)

    return sum(scores)


def validate_report(file_path: str) -> Dict[str, Any]:
    """
    Validate a cosmetic efficacy report.

    Args:
        file_path: Path to the report file (Markdown or text)

    Returns:
        Dictionary containing validation results
    """
    path = Path(file_path)

    if not path.exists():
        return {"error": f"File not found: {file_path}"}

    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return {"error": f"Error reading file: {str(e)}"}

    # Detect efficacy type
    efficacy_type = detect_efficacy_type(content)

    # Run all checks
    present_sections, missing_sections = check_sections(content, efficacy_type)

    results = {
        "file_path": str(path),
        "timestamp": datetime.now().isoformat(),
        "efficacy_type": efficacy_type,
        "sections": {
            "present": present_sections,
            "missing": missing_sections,
        },
        "sample_size": extract_sample_size(content),
        "duration_weeks": extract_duration(content),
        "statistical_analysis": check_statistical_analysis(content),
        "endpoints": check_endpoints(content, efficacy_type),
        "safety_data": check_safety_data(content),
        "ethics": check_ethics(content),
    }

    # Calculate overall score
    results["overall_score"] = calculate_overall_score(results)

    return results


def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(
        description="Validate cosmetic efficacy clinical trial reports"
    )
    parser.add_argument("file", help="Path to the report file to validate")
    parser.add_argument("-o", "--output", help="Save validation results to JSON file")
    parser.add_argument(
        "-t",
        "--type",
        choices=["whitening", "antiwrinkle", "moisturizing"],
        help="Override auto-detected efficacy type",
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Only output JSON, suppress report"
    )

    args = parser.parse_args()

    # Validate report
    results = validate_report(args.file)

    if "error" in results:
        print(f"Error: {results['error']}")
        return 1

    # Override efficacy type if specified
    if args.type:
        results["efficacy_type"] = args.type
        present, missing = check_sections(
            Path(args.file).read_text(encoding="utf-8"), args.type
        )
        results["sections"] = {"present": present, "missing": missing}
        results["endpoints"] = check_endpoints(
            Path(args.file).read_text(encoding="utf-8"), args.type
        )
        results["overall_score"] = calculate_overall_score(results)

    # Generate and print report
    if not args.quiet:
        report = generate_report(results)
        print(report)

    # Save to JSON if requested
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to: {args.output}")

    # Return appropriate exit code
    return 0 if results["overall_score"] >= 70 else 1


if __name__ == "__main__":
    exit(main())
