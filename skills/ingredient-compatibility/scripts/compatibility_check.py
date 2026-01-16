#!/usr/bin/env python3
"""
Cosmetic Ingredient Compatibility Checker

This module provides tools for analyzing ingredient compatibility in cosmetic formulations.
It checks for pH conflicts, charge interactions, oxidation-reduction reactions, chelation
issues, and other incompatibilities.

Author: EVAS Cosmetic
Version: 1.0.0
License: MIT
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Severity(Enum):
    """Severity levels for compatibility issues."""
    CRITICAL = "critical"  # Immediate physical/chemical reaction, product unusable
    HIGH = "high"          # Significant efficacy loss or stability issue
    MEDIUM = "medium"      # Long-term stability concern or partial efficacy loss
    LOW = "low"            # Minor impact or theoretical concern
    OK = "ok"              # Compatible, no issues
    SYNERGY = "synergy"    # Positive interaction, use together recommended


class IncompatibilityType(Enum):
    """Types of incompatibility mechanisms."""
    PH_CONFLICT = "ph_conflict"
    CHARGE_INTERACTION = "charge_interaction"
    OXIDATION_REDUCTION = "oxidation_reduction"
    CHELATION = "chelation"
    PRECIPITATION = "precipitation"
    ENZYMATIC = "enzymatic"
    POLYMER_INCOMPATIBILITY = "polymer_incompatibility"
    SURFACTANT_CONFLICT = "surfactant_conflict"


class ChargeType(Enum):
    """Electrical charge types for surfactants and polymers."""
    ANIONIC = "anionic"
    CATIONIC = "cationic"
    AMPHOTERIC = "amphoteric"
    NONIONIC = "nonionic"
    UNKNOWN = "unknown"


@dataclass
class pHRange:
    """Represents an optimal pH range for an ingredient."""
    optimal_min: float
    optimal_max: float
    acceptable_min: float
    acceptable_max: float

    def overlaps_with(self, other: "pHRange") -> tuple[bool, Optional[tuple[float, float]]]:
        """Check if two pH ranges overlap and return the overlapping range."""
        overlap_min = max(self.optimal_min, other.optimal_min)
        overlap_max = min(self.optimal_max, other.optimal_max)

        if overlap_min <= overlap_max:
            return True, (overlap_min, overlap_max)

        # Check acceptable ranges
        acceptable_overlap_min = max(self.acceptable_min, other.acceptable_min)
        acceptable_overlap_max = min(self.acceptable_max, other.acceptable_max)

        if acceptable_overlap_min <= acceptable_overlap_max:
            return True, (acceptable_overlap_min, acceptable_overlap_max)

        return False, None


@dataclass
class Ingredient:
    """Represents a cosmetic ingredient with its properties."""
    inci_name: str
    common_names: list[str] = field(default_factory=list)
    ph_range: Optional[pHRange] = None
    charge_type: ChargeType = ChargeType.UNKNOWN
    oxidation_sensitive: bool = False
    is_oxidizer: bool = False
    is_reducer: bool = False
    is_chelator: bool = False
    is_metal_based: bool = False
    is_acid: bool = False
    is_retinoid: bool = False
    is_vitamin_c: bool = False
    solubility_limit: Optional[float] = None  # In percentage


@dataclass
class CompatibilityResult:
    """Result of a compatibility check between two ingredients."""
    ingredient_1: str
    ingredient_2: str
    compatible: bool
    severity: Severity
    incompatibility_type: Optional[IncompatibilityType] = None
    reason: str = ""
    solution: str = ""
    notes: str = ""


@dataclass
class Issue:
    """Represents an issue found in formula analysis."""
    ingredients_involved: list[str]
    issue_type: IncompatibilityType
    severity: Severity
    description: str
    recommendation: str


# ============================================================================
# INCOMPATIBILITY DATABASE
# ============================================================================

INCOMPATIBILITY_DATABASE: dict[tuple[str, str], dict] = {
    # Benzoyl Peroxide + Retinoids (Critical)
    ("BENZOYL PEROXIDE", "RETINOL"): {
        "severity": Severity.CRITICAL,
        "type": IncompatibilityType.OXIDATION_REDUCTION,
        "reason": "Benzoyl Peroxide oxidizes and degrades Retinol, causing complete efficacy loss",
        "solution": "Use in separate products: Benzoyl Peroxide in AM, Retinoid in PM",
    },
    ("BENZOYL PEROXIDE", "RETINALDEHYDE"): {
        "severity": Severity.CRITICAL,
        "type": IncompatibilityType.OXIDATION_REDUCTION,
        "reason": "Benzoyl Peroxide oxidizes Retinaldehyde",
        "solution": "Use in separate products",
    },
    ("BENZOYL PEROXIDE", "TRETINOIN"): {
        "severity": Severity.CRITICAL,
        "type": IncompatibilityType.OXIDATION_REDUCTION,
        "reason": "Benzoyl Peroxide degrades Tretinoin",
        "solution": "Never combine; use separately",
    },

    # Vitamin C + Copper Peptides
    ("ASCORBIC ACID", "COPPER TRIPEPTIDE-1"): {
        "severity": Severity.HIGH,
        "type": IncompatibilityType.OXIDATION_REDUCTION,
        "reason": "Cu2+ ions catalyze rapid oxidation of Vitamin C, causing browning and efficacy loss",
        "solution": "Use in separate routines with 10-15 minute gap, or use different products",
    },
    ("ASCORBIC ACID", "GHK-CU"): {
        "severity": Severity.HIGH,
        "type": IncompatibilityType.OXIDATION_REDUCTION,
        "reason": "Copper peptides catalyze Vitamin C oxidation",
        "solution": "Apply separately with time gap",
    },

    # Vitamin C + Niacinamide (Often misunderstood)
    ("ASCORBIC ACID", "NIACINAMIDE"): {
        "severity": Severity.LOW,
        "type": IncompatibilityType.PH_CONFLICT,
        "reason": "At very low pH (<3.5), Niacinamide can hydrolyze to Nicotinic Acid over time. "
                  "However, at room temperature and typical use conditions, this is minimal.",
        "solution": "Safe to use together at pH 5-6. The incompatibility is largely a myth for typical formulations.",
        "notes": "Synergistic benefits when combined properly",
    },

    # Retinol + AHA/BHA
    ("RETINOL", "GLYCOLIC ACID"): {
        "severity": Severity.HIGH,
        "type": IncompatibilityType.PH_CONFLICT,
        "reason": "Different optimal pH ranges (Retinol: 5.5-6.5, Glycolic Acid: 3-4). "
                  "Combination increases skin irritation and barrier disruption.",
        "solution": "Use in separate routines: AHA in AM or alternate days, Retinol in PM",
    },
    ("RETINOL", "LACTIC ACID"): {
        "severity": Severity.HIGH,
        "type": IncompatibilityType.PH_CONFLICT,
        "reason": "pH conflict and increased irritation potential",
        "solution": "Alternate usage or separate AM/PM application",
    },
    ("RETINOL", "SALICYLIC ACID"): {
        "severity": Severity.HIGH,
        "type": IncompatibilityType.PH_CONFLICT,
        "reason": "pH conflict and amplified irritation",
        "solution": "Use on alternate days or separate routines",
    },

    # Surfactant conflicts
    ("SODIUM LAURYL SULFATE", "CETRIMONIUM CHLORIDE"): {
        "severity": Severity.CRITICAL,
        "type": IncompatibilityType.SURFACTANT_CONFLICT,
        "reason": "Anionic + Cationic surfactant combination forms insoluble complex, "
                  "causing precipitation and clumping",
        "solution": "Use surfactants from the same charge family or nonionic alternatives",
    },
    ("SODIUM LAURETH SULFATE", "BEHENTRIMONIUM CHLORIDE"): {
        "severity": Severity.CRITICAL,
        "type": IncompatibilityType.SURFACTANT_CONFLICT,
        "reason": "Anionic-cationic charge conflict causes precipitation",
        "solution": "Unify surfactant charge type or use nonionic/amphoteric alternatives",
    },

    # Polymer incompatibilities
    ("CARBOMER", "CETRIMONIUM CHLORIDE"): {
        "severity": Severity.CRITICAL,
        "type": IncompatibilityType.POLYMER_INCOMPATIBILITY,
        "reason": "Cationic ingredients neutralize Carbomer's anionic charge, "
                  "causing viscosity collapse and gel breakdown",
        "solution": "Use cationic-compatible thickeners like Hydroxyethylcellulose",
    },
    ("CARBOMER", "BEHENTRIMONIUM CHLORIDE"): {
        "severity": Severity.CRITICAL,
        "type": IncompatibilityType.POLYMER_INCOMPATIBILITY,
        "reason": "Cationic quaternary compound destroys Carbomer gel structure",
        "solution": "Replace Carbomer with nonionic thickener (HEC, Sclerotium Gum)",
    },

    # EDTA + Metal-based actives
    ("DISODIUM EDTA", "ZINC OXIDE"): {
        "severity": Severity.HIGH,
        "type": IncompatibilityType.CHELATION,
        "reason": "EDTA chelates zinc ions, potentially reducing zinc oxide effectiveness",
        "solution": "Minimize EDTA concentration or use alternative chelators",
    },
    ("DISODIUM EDTA", "COPPER TRIPEPTIDE-1"): {
        "severity": Severity.CRITICAL,
        "type": IncompatibilityType.CHELATION,
        "reason": "EDTA strongly chelates copper ions, inactivating copper peptides",
        "solution": "Do not use EDTA with copper-based actives; use gentler chelators if needed",
    },

    # Vitamin C + Vitamin E (Synergy)
    ("ASCORBIC ACID", "TOCOPHEROL"): {
        "severity": Severity.SYNERGY,
        "type": None,
        "reason": "Vitamin E regenerates oxidized Vitamin C, and vice versa. "
                  "Creates a powerful antioxidant network.",
        "solution": "Combine for enhanced stability and photoprotection (recommended ratio: 15% C + 1% E)",
    },

    # Retinol + Vitamin E (Synergy)
    ("RETINOL", "TOCOPHEROL"): {
        "severity": Severity.SYNERGY,
        "type": None,
        "reason": "Vitamin E protects Retinol from oxidation and enhances its stability",
        "solution": "Combine for improved retinol stability (0.5-1% Tocopherol recommended)",
    },

    # Retinol + Ceramides (Synergy)
    ("RETINOL", "CERAMIDE NP"): {
        "severity": Severity.SYNERGY,
        "type": None,
        "reason": "Ceramides support barrier repair while Retinol increases cell turnover. "
                  "Helps minimize retinol irritation.",
        "solution": "Excellent combination for anti-aging with barrier support",
    },
}


# ============================================================================
# INGREDIENT PROPERTIES DATABASE
# ============================================================================

INGREDIENT_PROPERTIES: dict[str, Ingredient] = {
    # Vitamin C derivatives
    "ASCORBIC ACID": Ingredient(
        inci_name="ASCORBIC ACID",
        common_names=["L-Ascorbic Acid", "Vitamin C", "LAA"],
        ph_range=pHRange(2.5, 3.5, 2.0, 4.0),
        oxidation_sensitive=True,
        is_reducer=True,
        is_vitamin_c=True,
        is_acid=True,
    ),
    "ASCORBYL GLUCOSIDE": Ingredient(
        inci_name="ASCORBYL GLUCOSIDE",
        common_names=["AA2G", "Vitamin C Glucoside"],
        ph_range=pHRange(5.0, 7.0, 4.0, 7.5),
        oxidation_sensitive=False,
        is_vitamin_c=True,
    ),
    "SODIUM ASCORBYL PHOSPHATE": Ingredient(
        inci_name="SODIUM ASCORBYL PHOSPHATE",
        common_names=["SAP", "Vitamin C Phosphate"],
        ph_range=pHRange(6.0, 7.0, 5.0, 7.5),
        oxidation_sensitive=False,
        is_vitamin_c=True,
    ),

    # Retinoids
    "RETINOL": Ingredient(
        inci_name="RETINOL",
        common_names=["Vitamin A", "Retinol"],
        ph_range=pHRange(5.5, 6.5, 5.0, 7.0),
        oxidation_sensitive=True,
        is_retinoid=True,
    ),
    "RETINALDEHYDE": Ingredient(
        inci_name="RETINALDEHYDE",
        common_names=["Retinal"],
        ph_range=pHRange(5.0, 6.0, 4.5, 6.5),
        oxidation_sensitive=True,
        is_retinoid=True,
    ),
    "RETINYL PALMITATE": Ingredient(
        inci_name="RETINYL PALMITATE",
        common_names=["Vitamin A Palmitate"],
        ph_range=pHRange(5.0, 7.0, 4.0, 8.0),
        oxidation_sensitive=True,
        is_retinoid=True,
    ),

    # AHA/BHA
    "GLYCOLIC ACID": Ingredient(
        inci_name="GLYCOLIC ACID",
        common_names=["AHA", "Alpha Hydroxy Acid"],
        ph_range=pHRange(3.0, 4.0, 2.5, 4.5),
        is_acid=True,
    ),
    "LACTIC ACID": Ingredient(
        inci_name="LACTIC ACID",
        common_names=["AHA", "Milk Acid"],
        ph_range=pHRange(3.5, 4.0, 3.0, 5.0),
        is_acid=True,
    ),
    "SALICYLIC ACID": Ingredient(
        inci_name="SALICYLIC ACID",
        common_names=["BHA", "Beta Hydroxy Acid"],
        ph_range=pHRange(3.0, 4.0, 2.5, 4.5),
        is_acid=True,
        solubility_limit=0.2,  # At pH 3
    ),

    # Niacinamide
    "NIACINAMIDE": Ingredient(
        inci_name="NIACINAMIDE",
        common_names=["Nicotinamide", "Vitamin B3"],
        ph_range=pHRange(5.0, 7.0, 4.0, 7.5),
    ),

    # Peptides
    "COPPER TRIPEPTIDE-1": Ingredient(
        inci_name="COPPER TRIPEPTIDE-1",
        common_names=["GHK-Cu", "Copper Peptide"],
        ph_range=pHRange(5.0, 6.5, 4.5, 7.0),
        is_metal_based=True,
    ),

    # Surfactants - Anionic
    "SODIUM LAURYL SULFATE": Ingredient(
        inci_name="SODIUM LAURYL SULFATE",
        common_names=["SLS"],
        charge_type=ChargeType.ANIONIC,
    ),
    "SODIUM LAURETH SULFATE": Ingredient(
        inci_name="SODIUM LAURETH SULFATE",
        common_names=["SLES"],
        charge_type=ChargeType.ANIONIC,
    ),

    # Surfactants - Cationic
    "CETRIMONIUM CHLORIDE": Ingredient(
        inci_name="CETRIMONIUM CHLORIDE",
        common_names=["CTAC"],
        charge_type=ChargeType.CATIONIC,
    ),
    "BEHENTRIMONIUM CHLORIDE": Ingredient(
        inci_name="BEHENTRIMONIUM CHLORIDE",
        common_names=["BTAC"],
        charge_type=ChargeType.CATIONIC,
    ),

    # Polymers
    "CARBOMER": Ingredient(
        inci_name="CARBOMER",
        common_names=["Carbopol"],
        ph_range=pHRange(5.0, 7.0, 4.0, 8.0),
        charge_type=ChargeType.ANIONIC,
    ),
    "HYDROXYETHYLCELLULOSE": Ingredient(
        inci_name="HYDROXYETHYLCELLULOSE",
        common_names=["HEC", "Natrosol"],
        charge_type=ChargeType.NONIONIC,
    ),

    # Chelators
    "DISODIUM EDTA": Ingredient(
        inci_name="DISODIUM EDTA",
        common_names=["EDTA"],
        is_chelator=True,
    ),
    "PHYTIC ACID": Ingredient(
        inci_name="PHYTIC ACID",
        common_names=["Inositol Hexaphosphate"],
        is_chelator=True,
    ),

    # Oxidizers
    "BENZOYL PEROXIDE": Ingredient(
        inci_name="BENZOYL PEROXIDE",
        common_names=["BPO"],
        is_oxidizer=True,
    ),

    # Antioxidants
    "TOCOPHEROL": Ingredient(
        inci_name="TOCOPHEROL",
        common_names=["Vitamin E"],
        is_reducer=True,
    ),
    "FERULIC ACID": Ingredient(
        inci_name="FERULIC ACID",
        common_names=["Ferulic"],
        is_reducer=True,
        is_acid=True,
    ),

    # Other common ingredients
    "HYALURONIC ACID": Ingredient(
        inci_name="HYALURONIC ACID",
        common_names=["HA", "Sodium Hyaluronate"],
        ph_range=pHRange(5.0, 7.0, 4.0, 8.0),
    ),
    "ZINC OXIDE": Ingredient(
        inci_name="ZINC OXIDE",
        common_names=["ZnO"],
        is_metal_based=True,
    ),
    "CERAMIDE NP": Ingredient(
        inci_name="CERAMIDE NP",
        common_names=["Ceramide 3"],
        ph_range=pHRange(5.0, 6.0, 4.5, 7.0),
    ),
}


# ============================================================================
# COMPATIBILITY CHECK FUNCTIONS
# ============================================================================

def normalize_inci_name(name: str) -> str:
    """Normalize INCI name for consistent lookup."""
    return name.upper().strip()


def get_ingredient_properties(inci_name: str) -> Optional[Ingredient]:
    """Get properties for an ingredient from the database."""
    normalized = normalize_inci_name(inci_name)
    return INGREDIENT_PROPERTIES.get(normalized)


def check_compatibility(ingredient_1: str, ingredient_2: str) -> CompatibilityResult:
    """
    Check compatibility between two ingredients.

    Args:
        ingredient_1: INCI name of first ingredient
        ingredient_2: INCI name of second ingredient

    Returns:
        CompatibilityResult with details about compatibility
    """
    ing1 = normalize_inci_name(ingredient_1)
    ing2 = normalize_inci_name(ingredient_2)

    # Check direct database lookup (both directions)
    key1 = (ing1, ing2)
    key2 = (ing2, ing1)

    if key1 in INCOMPATIBILITY_DATABASE:
        data = INCOMPATIBILITY_DATABASE[key1]
        return CompatibilityResult(
            ingredient_1=ing1,
            ingredient_2=ing2,
            compatible=data["severity"] in [Severity.OK, Severity.SYNERGY, Severity.LOW],
            severity=data["severity"],
            incompatibility_type=data.get("type"),
            reason=data.get("reason", ""),
            solution=data.get("solution", ""),
            notes=data.get("notes", ""),
        )

    if key2 in INCOMPATIBILITY_DATABASE:
        data = INCOMPATIBILITY_DATABASE[key2]
        return CompatibilityResult(
            ingredient_1=ing1,
            ingredient_2=ing2,
            compatible=data["severity"] in [Severity.OK, Severity.SYNERGY, Severity.LOW],
            severity=data["severity"],
            incompatibility_type=data.get("type"),
            reason=data.get("reason", ""),
            solution=data.get("solution", ""),
            notes=data.get("notes", ""),
        )

    # Check based on ingredient properties
    props1 = get_ingredient_properties(ing1)
    props2 = get_ingredient_properties(ing2)

    if props1 and props2:
        # Check charge conflicts
        if (props1.charge_type == ChargeType.ANIONIC and props2.charge_type == ChargeType.CATIONIC) or \
           (props1.charge_type == ChargeType.CATIONIC and props2.charge_type == ChargeType.ANIONIC):
            return CompatibilityResult(
                ingredient_1=ing1,
                ingredient_2=ing2,
                compatible=False,
                severity=Severity.CRITICAL,
                incompatibility_type=IncompatibilityType.CHARGE_INTERACTION,
                reason="Anionic and cationic ingredients form insoluble complexes",
                solution="Use ingredients from the same charge family or nonionic alternatives",
            )

        # Check oxidizer + reducer
        if (props1.is_oxidizer and props2.is_reducer) or (props1.is_reducer and props2.is_oxidizer):
            return CompatibilityResult(
                ingredient_1=ing1,
                ingredient_2=ing2,
                compatible=False,
                severity=Severity.HIGH,
                incompatibility_type=IncompatibilityType.OXIDATION_REDUCTION,
                reason="Potential oxidation-reduction reaction between ingredients",
                solution="Use in separate products or apply with time gap",
            )

        # Check chelator + metal-based
        if (props1.is_chelator and props2.is_metal_based) or (props1.is_metal_based and props2.is_chelator):
            return CompatibilityResult(
                ingredient_1=ing1,
                ingredient_2=ing2,
                compatible=False,
                severity=Severity.MEDIUM,
                incompatibility_type=IncompatibilityType.CHELATION,
                reason="Chelating agent may bind metal ions, reducing active ingredient efficacy",
                solution="Minimize chelator concentration or use alternative metal-free actives",
            )

        # Check pH range overlap
        if props1.ph_range and props2.ph_range:
            overlaps, overlap_range = props1.ph_range.overlaps_with(props2.ph_range)
            if not overlaps:
                return CompatibilityResult(
                    ingredient_1=ing1,
                    ingredient_2=ing2,
                    compatible=False,
                    severity=Severity.MEDIUM,
                    incompatibility_type=IncompatibilityType.PH_CONFLICT,
                    reason=f"pH ranges do not overlap: {ing1} ({props1.ph_range.optimal_min}-{props1.ph_range.optimal_max}) "
                           f"vs {ing2} ({props2.ph_range.optimal_min}-{props2.ph_range.optimal_max})",
                    solution="Use in separate products or find a compromise pH in acceptable ranges",
                )

    # Default: compatible (no known issues)
    return CompatibilityResult(
        ingredient_1=ing1,
        ingredient_2=ing2,
        compatible=True,
        severity=Severity.OK,
        reason="No known incompatibilities",
    )


def analyze_formula(ingredients: list[dict]) -> list[Issue]:
    """
    Analyze a complete formula for compatibility issues.

    Args:
        ingredients: List of dicts with 'inci' and optionally 'percent' keys
            Example: [{"inci": "ASCORBIC ACID", "percent": 15}, {"inci": "NIACINAMIDE", "percent": 5}]

    Returns:
        List of Issue objects describing problems found
    """
    issues = []
    inci_list = [normalize_inci_name(ing.get("inci", "")) for ing in ingredients]

    # Check all pairs
    for i, ing1 in enumerate(inci_list):
        for ing2 in inci_list[i+1:]:
            result = check_compatibility(ing1, ing2)

            if result.severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM]:
                issues.append(Issue(
                    ingredients_involved=[ing1, ing2],
                    issue_type=result.incompatibility_type or IncompatibilityType.PH_CONFLICT,
                    severity=result.severity,
                    description=result.reason,
                    recommendation=result.solution,
                ))

    # Check for multiple acids
    acids = [ing for ing in inci_list if get_ingredient_properties(ing) and
             get_ingredient_properties(ing).is_acid]
    if len(acids) > 2:
        issues.append(Issue(
            ingredients_involved=acids,
            issue_type=IncompatibilityType.PH_CONFLICT,
            severity=Severity.MEDIUM,
            description=f"Multiple acids in formula ({len(acids)}): may cause pH management challenges and irritation",
            recommendation="Consider reducing the number of acid actives or using lower concentrations",
        ))

    # Check for multiple oxidation-sensitive ingredients without antioxidants
    oxidation_sensitive = [ing for ing in inci_list if get_ingredient_properties(ing) and
                          get_ingredient_properties(ing).oxidation_sensitive]
    antioxidants = [ing for ing in inci_list if get_ingredient_properties(ing) and
                   get_ingredient_properties(ing).is_reducer]

    if oxidation_sensitive and not antioxidants:
        issues.append(Issue(
            ingredients_involved=oxidation_sensitive,
            issue_type=IncompatibilityType.OXIDATION_REDUCTION,
            severity=Severity.HIGH,
            description=f"Oxidation-sensitive ingredients ({', '.join(oxidation_sensitive)}) without antioxidant protection",
            recommendation="Add antioxidants such as Tocopherol, Ferulic Acid, or BHT for stability",
        ))

    return issues


def find_optimal_ph_range(ingredients: list[str]) -> dict:
    """
    Find the optimal pH range for a list of ingredients.

    Args:
        ingredients: List of INCI names

    Returns:
        Dict with recommended pH, acceptable range, and any compromises needed
    """
    ph_ranges = []
    ingredients_with_ph = []

    for ing in ingredients:
        props = get_ingredient_properties(normalize_inci_name(ing))
        if props and props.ph_range:
            ph_ranges.append(props.ph_range)
            ingredients_with_ph.append((ing, props.ph_range))

    if not ph_ranges:
        return {
            "recommended": 5.5,
            "range": (5.0, 6.0),
            "compromises": [],
            "note": "No pH-sensitive ingredients found; using standard skin pH range",
        }

    # Find overlap of all optimal ranges
    optimal_min = max(r.optimal_min for r in ph_ranges)
    optimal_max = min(r.optimal_max for r in ph_ranges)

    if optimal_min <= optimal_max:
        return {
            "recommended": (optimal_min + optimal_max) / 2,
            "range": (optimal_min, optimal_max),
            "compromises": [],
            "note": "All ingredients have overlapping optimal pH ranges",
        }

    # No optimal overlap, try acceptable ranges
    acceptable_min = max(r.acceptable_min for r in ph_ranges)
    acceptable_max = min(r.acceptable_max for r in ph_ranges)

    if acceptable_min <= acceptable_max:
        compromises = []
        mid_ph = (acceptable_min + acceptable_max) / 2

        for ing, ph_range in ingredients_with_ph:
            if mid_ph < ph_range.optimal_min or mid_ph > ph_range.optimal_max:
                compromises.append({
                    "ingredient": ing,
                    "optimal_range": f"{ph_range.optimal_min}-{ph_range.optimal_max}",
                    "impact": "Slightly reduced stability or efficacy at compromise pH",
                })

        return {
            "recommended": mid_ph,
            "range": (acceptable_min, acceptable_max),
            "compromises": compromises,
            "note": "Compromise pH within acceptable ranges; some ingredients not at optimal",
        }

    # No overlap even in acceptable ranges
    return {
        "recommended": None,
        "range": None,
        "compromises": ingredients_with_ph,
        "note": "No common pH range found. Consider separating into different products.",
        "suggestion": "Separate products by pH-sensitive ingredient groups",
    }


def suggest_synergies(ingredients: list[str]) -> list[dict]:
    """
    Suggest beneficial ingredient combinations based on known synergies.

    Args:
        ingredients: List of INCI names currently in formula

    Returns:
        List of suggested additions with their benefits
    """
    normalized = [normalize_inci_name(ing) for ing in ingredients]
    suggestions = []

    # Vitamin C synergies
    if any(props := get_ingredient_properties(ing) for ing in normalized if props and props.is_vitamin_c):
        vit_c_ing = next(ing for ing in normalized if (p := get_ingredient_properties(ing)) and p.is_vitamin_c)

        if "TOCOPHEROL" not in normalized:
            suggestions.append({
                "add": "TOCOPHEROL",
                "reason": f"Vitamin E regenerates {vit_c_ing} and creates synergistic antioxidant network",
                "recommended_percent": "0.5-1%",
            })

        if "FERULIC ACID" not in normalized and "ASCORBIC ACID" in normalized:
            suggestions.append({
                "add": "FERULIC ACID",
                "reason": "Ferulic Acid stabilizes L-Ascorbic Acid and provides 4-8x photoprotection boost",
                "recommended_percent": "0.5%",
            })

    # Retinoid synergies
    if any((props := get_ingredient_properties(ing)) and props.is_retinoid for ing in normalized):
        if "TOCOPHEROL" not in normalized:
            suggestions.append({
                "add": "TOCOPHEROL",
                "reason": "Vitamin E protects retinoids from oxidation and improves stability",
                "recommended_percent": "0.5-2%",
            })

        if not any("CERAMIDE" in ing for ing in normalized):
            suggestions.append({
                "add": "CERAMIDE NP",
                "reason": "Ceramides support barrier repair and help minimize retinoid irritation",
                "recommended_percent": "0.1-0.5%",
            })

    # Niacinamide synergies
    if "NIACINAMIDE" in normalized:
        if "HYALURONIC ACID" not in normalized and "SODIUM HYALURONATE" not in normalized:
            suggestions.append({
                "add": "HYALURONIC ACID",
                "reason": "Excellent hydration synergy with Niacinamide for barrier support",
                "recommended_percent": "0.1-2%",
            })

    return suggestions


# ============================================================================
# MAIN / DEMO
# ============================================================================

if __name__ == "__main__":
    # Demo usage
    print("=" * 60)
    print("COSMETIC INGREDIENT COMPATIBILITY CHECKER")
    print("=" * 60)

    # Example 1: Check single pair
    print("\n[1] Single Pair Compatibility Check")
    print("-" * 40)

    pairs_to_check = [
        ("RETINOL", "GLYCOLIC ACID"),
        ("ASCORBIC ACID", "NIACINAMIDE"),
        ("ASCORBIC ACID", "TOCOPHEROL"),
        ("BENZOYL PEROXIDE", "RETINOL"),
    ]

    for ing1, ing2 in pairs_to_check:
        result = check_compatibility(ing1, ing2)
        status = "OK" if result.compatible else "INCOMPATIBLE"
        print(f"\n{ing1} + {ing2}: {status} ({result.severity.value})")
        if result.reason:
            print(f"  Reason: {result.reason}")
        if result.solution:
            print(f"  Solution: {result.solution}")

    # Example 2: Analyze full formula
    print("\n\n[2] Full Formula Analysis")
    print("-" * 40)

    test_formula = [
        {"inci": "AQUA", "percent": 65},
        {"inci": "ASCORBIC ACID", "percent": 15},
        {"inci": "NIACINAMIDE", "percent": 5},
        {"inci": "TOCOPHEROL", "percent": 1},
        {"inci": "FERULIC ACID", "percent": 0.5},
        {"inci": "HYALURONIC ACID", "percent": 0.5},
    ]

    print("Formula ingredients:")
    for ing in test_formula:
        print(f"  - {ing['inci']}: {ing['percent']}%")

    issues = analyze_formula(test_formula)

    if issues:
        print(f"\nIssues found ({len(issues)}):")
        for issue in issues:
            print(f"\n  [{issue.severity.value.upper()}] {issue.issue_type.value}")
            print(f"  Ingredients: {', '.join(issue.ingredients_involved)}")
            print(f"  Description: {issue.description}")
            print(f"  Recommendation: {issue.recommendation}")
    else:
        print("\nNo compatibility issues found!")

    # Example 3: Find optimal pH
    print("\n\n[3] Optimal pH Range")
    print("-" * 40)

    ingredients_for_ph = ["ASCORBIC ACID", "NIACINAMIDE", "HYALURONIC ACID"]
    ph_result = find_optimal_ph_range(ingredients_for_ph)

    print(f"Ingredients: {', '.join(ingredients_for_ph)}")
    print(f"Recommended pH: {ph_result.get('recommended')}")
    print(f"Acceptable range: {ph_result.get('range')}")
    if ph_result.get("compromises"):
        print("Compromises needed:")
        for c in ph_result["compromises"]:
            if isinstance(c, dict):
                print(f"  - {c.get('ingredient', c)}: {c.get('impact', 'pH outside optimal')}")
    print(f"Note: {ph_result.get('note')}")

    # Example 4: Synergy suggestions
    print("\n\n[4] Synergy Suggestions")
    print("-" * 40)

    current_formula = ["RETINOL", "GLYCERIN"]
    suggestions = suggest_synergies(current_formula)

    print(f"Current formula: {', '.join(current_formula)}")
    print("Suggested additions:")
    for sug in suggestions:
        print(f"\n  + {sug['add']} ({sug['recommended_percent']})")
        print(f"    Reason: {sug['reason']}")

    print("\n" + "=" * 60)
    print("Demo complete!")
