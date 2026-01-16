"""
Stability Model Tools for Cosmetic Formulations

This module provides tools for:
- Arrhenius-based shelf life prediction
- Q10 factor calculations
- Emulsion stability scoring
- Stability protocol design

Author: EVAS Cosmetic
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Union
from enum import Enum
import math
from datetime import datetime


# =============================================================================
# Constants
# =============================================================================

GAS_CONSTANT = 8.314  # J/(mol*K)
CELSIUS_TO_KELVIN = 273.15


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class StabilityDataPoint:
    """Single stability data point at a specific temperature."""
    temperature_celsius: float  # Storage temperature in Celsius
    time_days: float  # Time at which measurement was taken
    remaining_percent: float  # Remaining percentage of active (0-100)

    @property
    def temperature_kelvin(self) -> float:
        """Convert temperature to Kelvin."""
        return self.temperature_celsius + CELSIUS_TO_KELVIN

    @property
    def degradation_percent(self) -> float:
        """Calculate degradation percentage."""
        return 100 - self.remaining_percent

    def calculate_rate_constant(self) -> float:
        """
        Calculate first-order rate constant.

        For first-order kinetics: C = C0 * exp(-k*t)
        Therefore: k = -ln(C/C0) / t
        """
        if self.remaining_percent <= 0 or self.time_days <= 0:
            raise ValueError("Invalid data: remaining_percent and time_days must be positive")

        fraction_remaining = self.remaining_percent / 100
        return -math.log(fraction_remaining) / self.time_days


@dataclass
class StabilityData:
    """Collection of stability data from accelerated testing."""
    product_name: str
    batch_number: str
    test_date: str
    data_points: List[StabilityDataPoint]
    notes: Optional[str] = None

    def get_rate_at_temperature(self, temp_celsius: float) -> Optional[float]:
        """Get rate constant at a specific temperature."""
        for point in self.data_points:
            if abs(point.temperature_celsius - temp_celsius) < 0.1:
                return point.calculate_rate_constant()
        return None

    def get_temperatures(self) -> List[float]:
        """Get list of unique temperatures in the data."""
        temps = set(p.temperature_celsius for p in self.data_points)
        return sorted(list(temps))


@dataclass
class ArrheniusResult:
    """Results from Arrhenius analysis."""
    activation_energy_kJ_mol: float
    frequency_factor: float
    q10_factor: float
    rate_at_25C: float
    estimated_shelf_life_days: float
    estimated_shelf_life_months: float
    r_squared: Optional[float] = None
    confidence_interval: Optional[Tuple[float, float]] = None

    def __str__(self) -> str:
        return f"""
Arrhenius Analysis Results:
--------------------------
Activation Energy (Ea): {self.activation_energy_kJ_mol:.1f} kJ/mol
Q10 Factor: {self.q10_factor:.2f}
Rate at 25C: {self.rate_at_25C:.6f} /day
Estimated Shelf Life: {self.estimated_shelf_life_days:.0f} days ({self.estimated_shelf_life_months:.1f} months)
"""


@dataclass
class TestCondition:
    """Single test condition for stability protocol."""
    name: str
    temperature_celsius: float
    humidity_percent: Optional[float] = None
    duration_months: int = 6
    sampling_points: List[str] = field(default_factory=list)
    description: str = ""


@dataclass
class Protocol:
    """Stability testing protocol."""
    product_type: str
    created_date: str
    conditions: List[TestCondition]
    evaluation_parameters: List[str]
    acceptance_criteria: Dict[str, str]
    notes: Optional[str] = None

    def __str__(self) -> str:
        lines = [
            f"\n{'='*60}",
            f"STABILITY PROTOCOL - {self.product_type}",
            f"{'='*60}",
            f"Created: {self.created_date}",
            "\nTEST CONDITIONS:",
            "-" * 40
        ]

        for cond in self.conditions:
            humidity = f"/{cond.humidity_percent}% RH" if cond.humidity_percent else ""
            lines.append(f"  - {cond.name}: {cond.temperature_celsius}C{humidity}")
            lines.append(f"    Duration: {cond.duration_months} months")
            lines.append(f"    Sampling: {', '.join(cond.sampling_points)}")

        lines.append("\nEVALUATION PARAMETERS:")
        lines.append("-" * 40)
        for param in self.evaluation_parameters:
            lines.append(f"  - {param}")

        lines.append("\nACCEPTANCE CRITERIA:")
        lines.append("-" * 40)
        for param, criteria in self.acceptance_criteria.items():
            lines.append(f"  - {param}: {criteria}")

        if self.notes:
            lines.append(f"\nNOTES: {self.notes}")

        return "\n".join(lines)


class ProductType(Enum):
    """Product types for protocol generation."""
    SERUM = "serum"
    CREAM = "cream"
    LOTION = "lotion"
    TONER = "toner"
    SUNSCREEN = "sunscreen"
    ESSENCE = "essence"
    EMULSION = "emulsion"
    GEL = "gel"
    OIL = "oil"
    POWDER = "powder"


@dataclass
class EmulsionStabilityScore:
    """Emulsion stability assessment results."""
    overall_score: float  # 0-10 scale
    creaming_risk: str  # LOW, MEDIUM, HIGH
    coalescence_risk: str
    ostwald_ripening_risk: str
    recommendations: List[str]
    parameters: Dict[str, any]

    def __str__(self) -> str:
        lines = [
            "\nEMULSION STABILITY ASSESSMENT",
            "=" * 40,
            f"Overall Score: {self.overall_score:.1f}/10",
            f"Creaming Risk: {self.creaming_risk}",
            f"Coalescence Risk: {self.coalescence_risk}",
            f"Ostwald Ripening Risk: {self.ostwald_ripening_risk}",
            "\nRecommendations:",
        ]
        for i, rec in enumerate(self.recommendations, 1):
            lines.append(f"  {i}. {rec}")

        return "\n".join(lines)


# =============================================================================
# Main Functions
# =============================================================================

def predict_shelf_life(
    data_points: List[Dict[str, float]],
    target_temp: float = 25,
    target_retention: float = 0.90
) -> ArrheniusResult:
    """
    Predict shelf life using Arrhenius model from accelerated stability data.

    Parameters
    ----------
    data_points : List[Dict[str, float]]
        List of dictionaries with 'temp' (Celsius) and 'rate' (1/day) keys.
        Example: [{"temp": 40, "rate": 0.005}, {"temp": 50, "rate": 0.015}]
    target_temp : float
        Temperature for shelf life prediction (default 25C)
    target_retention : float
        Target retention fraction (default 0.90 = 90%)

    Returns
    -------
    ArrheniusResult
        Contains Ea, Q10, predicted shelf life, etc.

    Example
    -------
    >>> data = [
    ...     {"temp": 40, "rate": 0.00175},
    ...     {"temp": 45, "rate": 0.0035},
    ...     {"temp": 50, "rate": 0.0065}
    ... ]
    >>> result = predict_shelf_life(data)
    >>> print(f"Shelf life: {result.estimated_shelf_life_months:.1f} months")
    """
    if len(data_points) < 2:
        raise ValueError("At least 2 temperature data points are required")

    # Extract temperatures (Kelvin) and ln(rates)
    temps_k = [d["temp"] + CELSIUS_TO_KELVIN for d in data_points]
    ln_rates = [math.log(d["rate"]) for d in data_points]
    inv_temps = [1/t for t in temps_k]

    # Linear regression: ln(k) = ln(A) - Ea/(R*T)
    n = len(data_points)
    sum_x = sum(inv_temps)
    sum_y = sum(ln_rates)
    sum_xy = sum(x*y for x, y in zip(inv_temps, ln_rates))
    sum_x2 = sum(x*x for x in inv_temps)

    # Calculate slope and intercept
    denominator = n * sum_x2 - sum_x ** 2
    if abs(denominator) < 1e-10:
        raise ValueError("Cannot calculate - temperatures too similar")

    slope = (n * sum_xy - sum_x * sum_y) / denominator
    intercept = (sum_y - slope * sum_x) / n

    # Calculate Ea and A
    Ea_J = -slope * GAS_CONSTANT
    Ea_kJ = Ea_J / 1000
    A = math.exp(intercept)

    # Calculate rate at target temperature
    target_temp_k = target_temp + CELSIUS_TO_KELVIN
    k_target = A * math.exp(-Ea_J / (GAS_CONSTANT * target_temp_k))

    # Calculate shelf life (time to reach target retention)
    shelf_life_days = -math.log(target_retention) / k_target

    # Calculate Q10 at 25C
    T1 = target_temp_k
    T2 = target_temp_k + 10
    q10 = math.exp(Ea_J * 10 / (GAS_CONSTANT * T1 * T2))

    # Calculate R-squared if more than 2 points
    r_squared = None
    if n > 2:
        y_mean = sum_y / n
        ss_tot = sum((y - y_mean)**2 for y in ln_rates)
        y_pred = [intercept + slope * x for x in inv_temps]
        ss_res = sum((y - yp)**2 for y, yp in zip(ln_rates, y_pred))
        if ss_tot > 0:
            r_squared = 1 - ss_res / ss_tot

    return ArrheniusResult(
        activation_energy_kJ_mol=round(Ea_kJ, 2),
        frequency_factor=A,
        q10_factor=round(q10, 2),
        rate_at_25C=k_target,
        estimated_shelf_life_days=round(shelf_life_days, 0),
        estimated_shelf_life_months=round(shelf_life_days / 30, 1),
        r_squared=round(r_squared, 4) if r_squared else None
    )


def calculate_q10(
    t1_rate: float,
    t2_rate: float,
    t1_celsius: float,
    t2_celsius: float
) -> float:
    """
    Calculate Q10 factor from two temperature-rate pairs.

    Q10 represents how much the reaction rate increases when
    temperature increases by 10C.

    Parameters
    ----------
    t1_rate : float
        Reaction rate at temperature t1 (same units as t2_rate)
    t2_rate : float
        Reaction rate at temperature t2
    t1_celsius : float
        First temperature in Celsius
    t2_celsius : float
        Second temperature in Celsius (must differ from t1)

    Returns
    -------
    float
        Q10 factor

    Example
    -------
    >>> q10 = calculate_q10(0.001, 0.003, 25, 35)
    >>> print(f"Q10 = {q10:.2f}")
    """
    if abs(t1_celsius - t2_celsius) < 0.1:
        raise ValueError("Temperatures must be different")

    if t1_rate <= 0 or t2_rate <= 0:
        raise ValueError("Rates must be positive")

    # Q10 = (k2/k1)^(10/(T2-T1))
    delta_t = t2_celsius - t1_celsius
    rate_ratio = t2_rate / t1_rate

    q10 = rate_ratio ** (10 / delta_t)

    return round(q10, 2)


def design_stability_protocol(
    product_type: Union[str, ProductType],
    include_photostability: bool = True,
    include_cycle_test: bool = True,
    tropical_climate: bool = False
) -> Protocol:
    """
    Design a stability testing protocol for a cosmetic product.

    Parameters
    ----------
    product_type : str or ProductType
        Type of cosmetic product
    include_photostability : bool
        Whether to include photostability testing
    include_cycle_test : bool
        Whether to include freeze-thaw cycle testing
    tropical_climate : bool
        If True, use tropical zone conditions (30C/75% RH)

    Returns
    -------
    Protocol
        Complete stability testing protocol

    Example
    -------
    >>> protocol = design_stability_protocol("serum")
    >>> print(protocol)
    """
    if isinstance(product_type, str):
        product_type = product_type.lower()
    else:
        product_type = product_type.value

    conditions = []

    # Long-term conditions
    if tropical_climate:
        conditions.append(TestCondition(
            name="Long-term (Tropical)",
            temperature_celsius=30,
            humidity_percent=75,
            duration_months=24,
            sampling_points=["0", "3", "6", "9", "12", "18", "24 months"],
            description="ICH Zone IVb - Hot/Very Humid"
        ))
    else:
        conditions.append(TestCondition(
            name="Long-term",
            temperature_celsius=25,
            humidity_percent=60,
            duration_months=24,
            sampling_points=["0", "3", "6", "9", "12", "18", "24 months"],
            description="ICH Zone II - Subtropical"
        ))

    # Accelerated conditions
    conditions.append(TestCondition(
        name="Accelerated",
        temperature_celsius=40,
        humidity_percent=75,
        duration_months=6,
        sampling_points=["0", "1", "2", "3", "6 months"],
        description="ICH standard accelerated condition"
    ))

    # Additional stress condition for certain products
    if product_type in ["serum", "essence", "toner"]:
        conditions.append(TestCondition(
            name="Stress (high temp)",
            temperature_celsius=45,
            humidity_percent=None,
            duration_months=3,
            sampling_points=["0", "1", "2", "3 months"],
            description="Rapid screening condition"
        ))

    # Refrigerated condition
    if product_type in ["serum", "essence"]:
        conditions.append(TestCondition(
            name="Refrigerated",
            temperature_celsius=4,
            humidity_percent=None,
            duration_months=12,
            sampling_points=["0", "3", "6", "12 months"],
            description="Cold storage stability"
        ))

    # Cycle test
    if include_cycle_test:
        conditions.append(TestCondition(
            name="Freeze-Thaw Cycle",
            temperature_celsius=-10,  # Alternating with 45C
            humidity_percent=None,
            duration_months=0,  # Measured in cycles
            sampling_points=["After each of 6 cycles"],
            description="-10C to 45C, 24h each, 6 cycles"
        ))

    # Photostability
    if include_photostability:
        conditions.append(TestCondition(
            name="Photostability (ICH Q1B)",
            temperature_celsius=25,
            humidity_percent=None,
            duration_months=0,
            sampling_points=["Before exposure", "After exposure"],
            description="UV: 200 Wh/m2, VIS: 1.2M lux*hr"
        ))

    # Define evaluation parameters based on product type
    base_params = ["Appearance", "Color", "Odor", "pH", "Viscosity"]

    product_specific_params = {
        "serum": ["Active ingredient assay", "Particle size (if applicable)"],
        "cream": ["Spreadability", "Emulsion stability"],
        "lotion": ["Emulsion stability", "Pour consistency"],
        "toner": ["Clarity", "Preservative assay"],
        "sunscreen": ["SPF (functional)", "UVA-PF", "Active assay"],
        "emulsion": ["Droplet size", "Zeta potential"],
        "gel": ["Gel strength", "Spreadability"],
        "oil": ["Peroxide value", "Acid value"],
        "powder": ["Moisture content", "Particle size", "Bulk density"]
    }

    eval_params = base_params + product_specific_params.get(product_type, [])
    eval_params.append("Microbial count")
    eval_params.append("Preservative efficacy (if applicable)")

    # Define acceptance criteria
    acceptance = {
        "Appearance": "No significant change",
        "Color": "Delta E < 3.0",
        "Odor": "No off-odor",
        "pH": "Initial +/- 0.5",
        "Viscosity": "Initial +/- 15%",
        "Active assay": "90-110% of label claim",
        "Microbial count": "< 100 CFU/mL (< 10 for eye products)"
    }

    return Protocol(
        product_type=product_type.capitalize(),
        created_date=datetime.now().strftime("%Y-%m-%d"),
        conditions=conditions,
        evaluation_parameters=eval_params,
        acceptance_criteria=acceptance,
        notes=f"Protocol designed for {product_type} product. Adjust based on specific formulation requirements."
    )


def emulsion_stability_score(
    formula: Dict[str, any]
) -> EmulsionStabilityScore:
    """
    Calculate emulsion stability score based on formulation parameters.

    Parameters
    ----------
    formula : Dict
        Dictionary containing formulation parameters:
        - oil_phase_percent: Oil phase percentage (0-100)
        - emulsifier_percent: Total emulsifier percentage
        - hlb_value: HLB of emulsifier system (optional)
        - required_hlb: Required HLB of oil phase (optional)
        - viscosity_cp: Continuous phase viscosity in cP
        - particle_size_um: Mean particle size in micrometers
        - zeta_potential_mv: Zeta potential in mV (optional)
        - emulsion_type: "o/w" or "w/o"

    Returns
    -------
    EmulsionStabilityScore
        Stability assessment with scores and recommendations

    Example
    -------
    >>> formula = {
    ...     "oil_phase_percent": 20,
    ...     "emulsifier_percent": 3,
    ...     "hlb_value": 12,
    ...     "required_hlb": 11,
    ...     "viscosity_cp": 5000,
    ...     "particle_size_um": 2,
    ...     "zeta_potential_mv": -35,
    ...     "emulsion_type": "o/w"
    ... }
    >>> result = emulsion_stability_score(formula)
    >>> print(result)
    """
    score = 10.0  # Start with perfect score
    recommendations = []

    # Extract parameters with defaults
    oil_percent = formula.get("oil_phase_percent", 15)
    emulsifier_percent = formula.get("emulsifier_percent", 2)
    hlb = formula.get("hlb_value")
    required_hlb = formula.get("required_hlb")
    viscosity = formula.get("viscosity_cp", 1000)
    particle_size = formula.get("particle_size_um", 5)
    zeta = formula.get("zeta_potential_mv")
    emulsion_type = formula.get("emulsion_type", "o/w").lower()

    # === Creaming/Sedimentation Risk ===
    # Based on Stokes' Law: v proportional to r^2 / viscosity

    creaming_risk = "LOW"

    # Particle size factor (most critical)
    if particle_size > 10:
        score -= 3
        creaming_risk = "HIGH"
        recommendations.append("Reduce particle size to < 5 um through better homogenization")
    elif particle_size > 5:
        score -= 1.5
        creaming_risk = "MEDIUM"
        recommendations.append("Consider reducing particle size to < 3 um")
    elif particle_size > 3:
        score -= 0.5
        creaming_risk = "MEDIUM"

    # Viscosity factor
    if viscosity < 500:
        score -= 2
        if creaming_risk == "LOW":
            creaming_risk = "MEDIUM"
        recommendations.append("Increase continuous phase viscosity (add thickener)")
    elif viscosity < 1000:
        score -= 1
        recommendations.append("Consider increasing viscosity for better stability")
    elif viscosity > 10000:
        score += 0.5  # Bonus for high viscosity

    # Oil phase amount
    if oil_percent > 40:
        score -= 1
        recommendations.append("High oil phase - consider w/o emulsion if stability issues persist")

    # === Coalescence Risk ===

    coalescence_risk = "LOW"

    # Emulsifier coverage
    emulsifier_oil_ratio = emulsifier_percent / max(oil_percent, 1) * 100

    if emulsifier_oil_ratio < 5:
        score -= 2
        coalescence_risk = "HIGH"
        recommendations.append("Increase emulsifier concentration (target 10-15% of oil phase)")
    elif emulsifier_oil_ratio < 10:
        score -= 1
        coalescence_risk = "MEDIUM"
        recommendations.append("Consider increasing emulsifier for better coverage")

    # HLB matching
    if hlb is not None and required_hlb is not None:
        hlb_diff = abs(hlb - required_hlb)
        if hlb_diff > 3:
            score -= 2
            coalescence_risk = "HIGH"
            recommendations.append(f"Adjust HLB: current {hlb}, required {required_hlb}")
        elif hlb_diff > 1.5:
            score -= 1
            if coalescence_risk == "LOW":
                coalescence_risk = "MEDIUM"

    # Zeta potential (electrostatic stabilization)
    if zeta is not None:
        abs_zeta = abs(zeta)
        if abs_zeta < 15:
            score -= 1.5
            coalescence_risk = "HIGH"
            recommendations.append("Low zeta potential - add ionic emulsifier or electrolyte")
        elif abs_zeta < 25:
            score -= 0.5
            if coalescence_risk == "LOW":
                coalescence_risk = "MEDIUM"
        elif abs_zeta > 40:
            score += 0.5  # Bonus for strong electrostatic stabilization

    # === Ostwald Ripening Risk ===
    # More relevant for small particles and volatile oils

    ostwald_risk = "LOW"

    if particle_size < 1:  # Nanoemulsion
        ostwald_risk = "MEDIUM"
        score -= 0.5
        recommendations.append("For nanoemulsions, add long-chain triglycerides to inhibit Ostwald ripening")

    # Ensure score is within bounds
    score = max(0, min(10, score))

    # Overall assessment
    if score >= 8:
        overall_comment = "Good stability expected"
    elif score >= 6:
        overall_comment = "Moderate stability - address recommendations"
    elif score >= 4:
        overall_comment = "Poor stability predicted - reformulation recommended"
    else:
        overall_comment = "Very poor stability - significant reformulation needed"

    if not recommendations:
        recommendations.append("Formulation parameters within acceptable ranges")

    recommendations.append(overall_comment)

    return EmulsionStabilityScore(
        overall_score=round(score, 1),
        creaming_risk=creaming_risk,
        coalescence_risk=coalescence_risk,
        ostwald_ripening_risk=ostwald_risk,
        recommendations=recommendations,
        parameters=formula
    )


def predict_from_q10(
    q10: float,
    accelerated_shelf_life_days: float,
    accelerated_temp: float,
    target_temp: float = 25
) -> Dict[str, float]:
    """
    Simple shelf life prediction using Q10 factor.

    Parameters
    ----------
    q10 : float
        Q10 factor (typically 2-4)
    accelerated_shelf_life_days : float
        Observed shelf life at accelerated temperature
    accelerated_temp : float
        Accelerated testing temperature in Celsius
    target_temp : float
        Target storage temperature (default 25C)

    Returns
    -------
    Dict[str, float]
        Predicted shelf life at target temperature

    Example
    -------
    >>> result = predict_from_q10(q10=2.5, accelerated_shelf_life_days=90, accelerated_temp=40)
    >>> print(f"Predicted shelf life: {result['shelf_life_months']:.1f} months")
    """
    delta_t = accelerated_temp - target_temp

    # Rate ratio: k_acc / k_target = Q10^(delta_T / 10)
    rate_ratio = q10 ** (delta_t / 10)

    # Shelf life inversely proportional to rate
    target_shelf_life_days = accelerated_shelf_life_days * rate_ratio

    return {
        "target_temperature": target_temp,
        "shelf_life_days": round(target_shelf_life_days, 0),
        "shelf_life_months": round(target_shelf_life_days / 30, 1),
        "rate_ratio": round(rate_ratio, 2),
        "note": f"Based on Q10={q10}, {accelerated_shelf_life_days} days at {accelerated_temp}C"
    }


# =============================================================================
# Utility Functions
# =============================================================================

def celsius_to_kelvin(celsius: float) -> float:
    """Convert Celsius to Kelvin."""
    return celsius + CELSIUS_TO_KELVIN


def kelvin_to_celsius(kelvin: float) -> float:
    """Convert Kelvin to Celsius."""
    return kelvin - CELSIUS_TO_KELVIN


def calculate_ea_from_q10(q10: float, reference_temp_celsius: float = 25) -> float:
    """
    Calculate activation energy from Q10 factor.

    Parameters
    ----------
    q10 : float
        Q10 factor
    reference_temp_celsius : float
        Reference temperature in Celsius (default 25C)

    Returns
    -------
    float
        Activation energy in kJ/mol
    """
    T = reference_temp_celsius + CELSIUS_TO_KELVIN
    T_plus_10 = T + 10

    # Q10 = exp(Ea * 10 / (R * T * (T+10)))
    # ln(Q10) = Ea * 10 / (R * T * (T+10))
    # Ea = ln(Q10) * R * T * (T+10) / 10

    Ea_J = math.log(q10) * GAS_CONSTANT * T * T_plus_10 / 10
    Ea_kJ = Ea_J / 1000

    return round(Ea_kJ, 1)


def validate_arrhenius_fit(
    data_points: List[Dict[str, float]],
    min_r_squared: float = 0.95
) -> Dict[str, any]:
    """
    Validate Arrhenius model fit quality.

    Parameters
    ----------
    data_points : List[Dict[str, float]]
        List of dictionaries with 'temp' and 'rate' keys
    min_r_squared : float
        Minimum acceptable R-squared value

    Returns
    -------
    Dict containing fit quality assessment
    """
    if len(data_points) < 3:
        return {
            "valid": False,
            "message": "Need at least 3 data points for validation",
            "recommendation": "Add more temperature points"
        }

    result = predict_shelf_life(data_points)

    if result.r_squared is None:
        return {
            "valid": False,
            "message": "Could not calculate R-squared"
        }

    valid = result.r_squared >= min_r_squared

    assessment = {
        "valid": valid,
        "r_squared": result.r_squared,
        "q10": result.q10_factor,
        "Ea_kJ_mol": result.activation_energy_kJ_mol
    }

    if not valid:
        assessment["message"] = f"R-squared ({result.r_squared:.3f}) below threshold ({min_r_squared})"
        assessment["recommendation"] = "Check for non-Arrhenius behavior or measurement errors"
    else:
        assessment["message"] = f"Good fit (R-squared = {result.r_squared:.3f})"

    # Check if Q10 is in reasonable range
    if result.q10_factor < 1.5 or result.q10_factor > 5:
        assessment["q10_warning"] = f"Q10 value ({result.q10_factor}) outside typical range (1.5-5)"

    return assessment


# =============================================================================
# Example Usage
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("STABILITY MODEL TOOLS - DEMO")
    print("=" * 60)

    # Example 1: Arrhenius prediction
    print("\n1. ARRHENIUS SHELF LIFE PREDICTION")
    print("-" * 40)

    stability_data = [
        {"temp": 40, "rate": 0.00175},  # k at 40C
        {"temp": 45, "rate": 0.0035},   # k at 45C
        {"temp": 50, "rate": 0.0068}    # k at 50C
    ]

    result = predict_shelf_life(stability_data)
    print(result)

    # Example 2: Q10 calculation
    print("\n2. Q10 CALCULATION")
    print("-" * 40)

    q10 = calculate_q10(0.00175, 0.0035, 40, 45)
    print(f"Q10 (40C to 45C): {q10}")

    ea = calculate_ea_from_q10(q10)
    print(f"Estimated Ea: {ea} kJ/mol")

    # Example 3: Protocol design
    print("\n3. STABILITY PROTOCOL DESIGN")
    print("-" * 40)

    protocol = design_stability_protocol("serum", include_photostability=True)
    print(protocol)

    # Example 4: Emulsion stability score
    print("\n4. EMULSION STABILITY ASSESSMENT")
    print("-" * 40)

    formula = {
        "oil_phase_percent": 20,
        "emulsifier_percent": 3,
        "hlb_value": 12,
        "required_hlb": 11,
        "viscosity_cp": 5000,
        "particle_size_um": 2,
        "zeta_potential_mv": -35,
        "emulsion_type": "o/w"
    }

    stability = emulsion_stability_score(formula)
    print(stability)

    # Example 5: Simple Q10 prediction
    print("\n5. SIMPLE Q10 PREDICTION")
    print("-" * 40)

    prediction = predict_from_q10(
        q10=2.5,
        accelerated_shelf_life_days=90,
        accelerated_temp=40
    )

    for key, value in prediction.items():
        print(f"  {key}: {value}")
