#!/usr/bin/env python3
"""
Cosmetic Skills Resource Detection Script

Detects all available cosmetic skills, scripts, and reference materials
within the cosmetic-skills directory structure. Outputs a JSON file that
Claude Code can use to make informed decisions about which skills to use
for specific cosmetic formulation, analysis, or regulatory tasks.

Based on K-Dense Inc.'s get-available-resources skill from claude-scientific-skills.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


# Skill category mappings based on common cosmetic skill patterns
CATEGORY_PATTERNS = {
    "databases": [
        "cosing",
        "kfda",
        "ewg",
        "cir",
        "mintel",
        "icid",
        "ifra",
        "incidecoder",
        "cosdna",
        "pubchem",
    ],
    "packages": [
        "formulation",
        "calculator",
        "predictor",
        "compatibility",
        "penetration",
        "rdkit",
        "irritation",
    ],
    "integrations": ["integration", "cosmily", "ulprospector", "supplier", "gateway"],
    "thinking": [
        "claim",
        "regulatory-compliance",
        "consumer",
        "trend",
        "positioning",
        "strategy",
    ],
    "helpers": [
        "context",
        "initialization",
        "converter",
        "checker",
        "batch",
        "inci-converter",
    ],
}

# Task-based skill recommendations
TASK_RECOMMENDATIONS = {
    "formulation": {
        "description": "Formulation development and optimization",
        "primary": [
            "formulation-calculator",
            "ingredient-compatibility",
            "stability-predictor",
        ],
        "secondary": [
            "skin-penetration",
            "rdkit-cosmetic",
            "concentration-converter",
            "batch-calculator",
        ],
    },
    "safety_analysis": {
        "description": "Ingredient safety and toxicity assessment",
        "primary": ["cosdna-analysis", "ewg-skindeep", "cir-safety"],
        "secondary": [
            "incidecoder-analysis",
            "irritation-predictor",
            "cosing-database",
        ],
    },
    "ingredient_lookup": {
        "description": "Ingredient information and INCI lookup",
        "primary": ["cosing-database", "kfda-ingredient", "incidecoder-analysis"],
        "secondary": ["icid-database", "ifra-standards", "inci-converter"],
    },
    "regulatory": {
        "description": "Regulatory compliance and market access",
        "primary": ["regulatory-compliance", "regulatory-checker", "kfda-ingredient"],
        "secondary": ["cosing-database", "ifra-standards", "claim-substantiation"],
    },
    "market_analysis": {
        "description": "Market trends and consumer insights",
        "primary": ["trend-analysis", "consumer-insight", "mintel-gnpd"],
        "secondary": ["product-positioning", "formulation-strategy"],
    },
    "claim_development": {
        "description": "Marketing claims and substantiation",
        "primary": ["claim-substantiation", "kfda-ingredient", "incidecoder-analysis"],
        "secondary": ["consumer-insight", "regulatory-compliance"],
    },
}


def find_cosmetic_skills_root(start_path: Path = None) -> Optional[Path]:
    """
    Find the cosmetic-skills root directory.

    Searches for a directory containing characteristic skill folders.
    """
    if start_path is None:
        start_path = Path(__file__).parent.parent.parent

    # If we're in the scripts folder, go up to find cosmetic-skills
    if start_path.name == "scripts":
        start_path = start_path.parent.parent
    elif start_path.name == "get-available-resources":
        start_path = start_path.parent

    # Check if this is the cosmetic-skills root
    if (start_path / "cosing-database").exists() or (
        start_path / "formulation-calculator"
    ).exists():
        return start_path

    # Try parent directories
    for parent in start_path.parents:
        if parent.name == "cosmetic-skills":
            return parent
        if (parent / "cosmetic-skills").exists():
            return parent / "cosmetic-skills"

    return start_path


def parse_skill_md(skill_md_path: Path) -> Dict[str, Any]:
    """
    Parse SKILL.md file to extract metadata.
    """
    metadata = {"name": None, "description": None, "license": None, "author": None}

    try:
        content = skill_md_path.read_text(encoding="utf-8")

        # Parse YAML frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1]

                # Extract fields from frontmatter
                name_match = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
                if name_match:
                    metadata["name"] = name_match.group(1).strip()

                desc_match = re.search(
                    r"^description:\s*(.+)$", frontmatter, re.MULTILINE
                )
                if desc_match:
                    metadata["description"] = desc_match.group(1).strip()

                license_match = re.search(
                    r"^license:\s*(.+)$", frontmatter, re.MULTILINE
                )
                if license_match:
                    metadata["license"] = license_match.group(1).strip()

        # If no frontmatter, try to extract from content
        if not metadata["description"]:
            # Look for first paragraph after heading
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if line.startswith("# "):
                    # Found main heading, look for description
                    for j in range(i + 1, min(i + 10, len(lines))):
                        if lines[j].strip() and not lines[j].startswith("#"):
                            metadata["description"] = lines[j].strip()
                            break
                    break
    except Exception as e:
        metadata["parse_error"] = str(e)

    return metadata


def categorize_skill(skill_name: str) -> str:
    """
    Determine the category of a skill based on its name.
    """
    skill_lower = skill_name.lower()

    for category, patterns in CATEGORY_PATTERNS.items():
        for pattern in patterns:
            if pattern in skill_lower:
                return category

    # Default category
    return "other"


def scan_skill_directory(skill_path: Path) -> Dict[str, Any]:
    """
    Scan a single skill directory and extract information.
    """
    skill_info = {
        "name": skill_path.name,
        "path": str(skill_path),
        "has_skill_md": False,
        "scripts": [],
        "references": [],
        "assets": [],
        "status": "unknown",
        "category": categorize_skill(skill_path.name),
    }

    # Check for SKILL.md
    skill_md_path = skill_path / "SKILL.md"
    if skill_md_path.exists():
        skill_info["has_skill_md"] = True
        metadata = parse_skill_md(skill_md_path)
        skill_info["metadata"] = metadata
        if metadata.get("description"):
            skill_info["description"] = metadata["description"]

    # Scan scripts folder
    scripts_path = skill_path / "scripts"
    if scripts_path.exists() and scripts_path.is_dir():
        for script_file in scripts_path.glob("*.py"):
            if script_file.name != "__init__.py" and not script_file.name.startswith(
                "__"
            ):
                skill_info["scripts"].append(script_file.name)

    # Scan references folder
    references_path = skill_path / "references"
    if references_path.exists() and references_path.is_dir():
        for ref_file in references_path.glob("*.md"):
            skill_info["references"].append(ref_file.name)

    # Scan assets folder
    assets_path = skill_path / "assets"
    if assets_path.exists() and assets_path.is_dir():
        for asset_file in assets_path.iterdir():
            if asset_file.is_file():
                skill_info["assets"].append(asset_file.name)

    # Determine status
    has_scripts = len(skill_info["scripts"]) > 0
    has_references = len(skill_info["references"]) > 0
    has_skill_md = skill_info["has_skill_md"]

    if has_skill_md and has_scripts and has_references:
        skill_info["status"] = "fully_implemented"
    elif has_skill_md and (has_scripts or has_references):
        skill_info["status"] = "partially_implemented"
    elif has_skill_md:
        skill_info["status"] = "documentation_only"
    else:
        skill_info["status"] = "incomplete"

    return skill_info


def scan_all_skills(root_path: Path) -> Dict[str, Any]:
    """
    Scan all skill directories under the root path.
    """
    skills = {}
    categories = {}

    # Initialize category counters
    for category in CATEGORY_PATTERNS.keys():
        categories[category] = {"count": 0, "skills": []}
    categories["other"] = {"count": 0, "skills": []}

    # Scan each subdirectory
    for item in root_path.iterdir():
        if (
            item.is_dir()
            and not item.name.startswith(".")
            and not item.name.startswith("_")
        ):
            # Skip non-skill directories
            if item.name in ["docs", "examples", "tests", "__pycache__"]:
                continue

            skill_info = scan_skill_directory(item)
            skills[item.name] = skill_info

            # Update category counts
            category = skill_info["category"]
            if category not in categories:
                categories[category] = {"count": 0, "skills": []}
            categories[category]["count"] += 1
            categories[category]["skills"].append(item.name)

    return skills, categories


def generate_recommendations(skills: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate task-based recommendations based on available skills.
    """
    recommendations = {}

    for task_type, task_config in TASK_RECOMMENDATIONS.items():
        task_rec = {
            "description": task_config["description"],
            "primary": [],
            "secondary": [],
            "available_count": 0,
        }

        # Check which recommended skills are available and implemented
        for skill_name in task_config["primary"]:
            if skill_name in skills:
                skill = skills[skill_name]
                if skill["status"] in ["fully_implemented", "partially_implemented"]:
                    task_rec["primary"].append(
                        {
                            "name": skill_name,
                            "status": skill["status"],
                            "scripts": skill["scripts"],
                        }
                    )
                    task_rec["available_count"] += 1

        for skill_name in task_config["secondary"]:
            if skill_name in skills:
                skill = skills[skill_name]
                if skill["status"] in ["fully_implemented", "partially_implemented"]:
                    task_rec["secondary"].append(
                        {
                            "name": skill_name,
                            "status": skill["status"],
                            "scripts": skill["scripts"],
                        }
                    )
                    task_rec["available_count"] += 1

        recommendations[task_type] = task_rec

    return recommendations


def detect_all_resources(output_path: str = None) -> Dict[str, Any]:
    """
    Detect all cosmetic skill resources and save to JSON.

    Args:
        output_path: Optional path to save JSON. Defaults to .cosmetic_resources.json in cwd.

    Returns:
        Dictionary containing all resource information.
    """
    if output_path is None:
        output_path = os.path.join(os.getcwd(), ".cosmetic_resources.json")

    # Find the cosmetic-skills root
    root_path = find_cosmetic_skills_root()

    if root_path is None or not root_path.exists():
        return {
            "error": "Could not find cosmetic-skills directory",
            "searched_from": str(Path(__file__).parent),
        }

    # Scan all skills
    skills, categories = scan_all_skills(root_path)

    # Calculate summary statistics
    status_counts = {
        "fully_implemented": 0,
        "partially_implemented": 0,
        "documentation_only": 0,
        "incomplete": 0,
    }

    for skill in skills.values():
        status = skill.get("status", "unknown")
        if status in status_counts:
            status_counts[status] += 1

    # Generate recommendations
    recommendations = generate_recommendations(skills)

    # Build the final resource object
    resources = {
        "timestamp": datetime.now().isoformat(),
        "cosmetic_skills_path": str(root_path),
        "summary": {"total_skills": len(skills), **status_counts},
        "categories": categories,
        "skills": skills,
        "recommendations": recommendations,
    }

    # Save to JSON file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resources, f, indent=2, ensure_ascii=False)

    return resources


def print_summary(resources: Dict[str, Any]) -> None:
    """Print a human-readable summary of detected resources."""

    print("\n" + "=" * 60)
    print("COSMETIC SKILLS RESOURCE DETECTION")
    print("=" * 60)

    if "error" in resources:
        print(f"\nError: {resources['error']}")
        return

    summary = resources["summary"]
    print(f"\nPath: {resources['cosmetic_skills_path']}")
    print(f"Timestamp: {resources['timestamp']}")

    print(f"\n--- Summary ---")
    print(f"Total Skills: {summary['total_skills']}")
    print(f"  - Fully Implemented: {summary['fully_implemented']}")
    print(f"  - Partially Implemented: {summary['partially_implemented']}")
    print(f"  - Documentation Only: {summary['documentation_only']}")
    print(f"  - Incomplete: {summary['incomplete']}")

    print(f"\n--- Categories ---")
    for category, info in resources["categories"].items():
        if info["count"] > 0:
            print(f"  {category}: {info['count']} skills")
            for skill in info["skills"][:5]:  # Show first 5
                skill_status = resources["skills"][skill]["status"]
                print(f"    - {skill} ({skill_status})")
            if len(info["skills"]) > 5:
                print(f"    ... and {len(info['skills']) - 5} more")

    print(f"\n--- Task Recommendations ---")
    for task, rec in resources["recommendations"].items():
        if rec["available_count"] > 0:
            print(f"\n  {task.upper()}: {rec['description']}")
            print(f"    Primary: {[s['name'] for s in rec['primary']]}")
            if rec["secondary"]:
                print(f"    Secondary: {[s['name'] for s in rec['secondary']]}")

    print("\n" + "=" * 60)


def main():
    """Main entry point for CLI usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Detect available cosmetic skills and resources"
    )
    parser.add_argument(
        "-o",
        "--output",
        default=".cosmetic_resources.json",
        help="Output JSON file path (default: .cosmetic_resources.json)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print full resources to stdout as JSON",
    )
    parser.add_argument(
        "--category",
        choices=[
            "databases",
            "packages",
            "integrations",
            "thinking",
            "helpers",
            "other",
        ],
        help="Filter by skill category",
    )
    parser.add_argument(
        "--task",
        choices=list(TASK_RECOMMENDATIONS.keys()),
        help="Get recommendations for specific task type",
    )

    args = parser.parse_args()

    print("Detecting cosmetic skill resources...")
    resources = detect_all_resources(args.output)

    if "error" not in resources:
        print(f"Resources detected and saved to: {args.output}")

        if args.verbose:
            print("\n" + json.dumps(resources, indent=2, ensure_ascii=False))

        if args.category:
            print(f"\n--- Skills in category '{args.category}' ---")
            for skill_name in (
                resources["categories"].get(args.category, {}).get("skills", [])
            ):
                skill = resources["skills"][skill_name]
                print(f"  {skill_name}: {skill['status']}")
                if skill["scripts"]:
                    print(f"    Scripts: {skill['scripts']}")

        if args.task:
            print(f"\n--- Recommendations for '{args.task}' ---")
            rec = resources["recommendations"].get(args.task, {})
            print(f"  Description: {rec.get('description', 'N/A')}")
            print(f"  Primary skills: {[s['name'] for s in rec.get('primary', [])]}")
            print(
                f"  Secondary skills: {[s['name'] for s in rec.get('secondary', [])]}"
            )

        if not args.verbose and not args.category and not args.task:
            print_summary(resources)
    else:
        print(f"Error: {resources['error']}")


if __name__ == "__main__":
    main()
