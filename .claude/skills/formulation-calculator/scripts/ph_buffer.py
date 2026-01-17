#!/usr/bin/env python3
"""
pH Buffer Calculator for Cosmetic Formulation

화장품 제형의 pH 조정 및 버퍼 시스템 설계 도구
- Henderson-Hasselbalch 기반 버퍼 비율 계산
- pH 조정제 필요량 계산
- 완충액 제조 가이드

Author: EVAS Cosmetic
License: MIT
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import math


@dataclass
class BufferSystem:
    """버퍼 시스템 데이터 클래스"""
    name: str
    acid: str
    base: str
    pka_values: List[float]
    effective_ph_range: Tuple[float, float]
    acid_mw: float
    base_mw: float
    notes: Optional[str] = None


class BufferDatabase:
    """버퍼 시스템 데이터베이스"""

    BUFFERS = {
        "citric_citrate": BufferSystem(
            name="Citric Acid / Sodium Citrate",
            acid="Citric Acid",
            base="Trisodium Citrate",
            pka_values=[3.13, 4.76, 6.40],
            effective_ph_range=(2.5, 7.0),
            acid_mw=192.12,
            base_mw=294.10,
            notes="Most versatile buffer for cosmetics, chelating effect"
        ),
        "lactic_lactate": BufferSystem(
            name="Lactic Acid / Sodium Lactate",
            acid="Lactic Acid",
            base="Sodium Lactate",
            pka_values=[3.86],
            effective_ph_range=(3.0, 5.0),
            acid_mw=90.08,
            base_mw=112.06,
            notes="AHA function, skin-friendly, moisturizing"
        ),
        "acetic_acetate": BufferSystem(
            name="Acetic Acid / Sodium Acetate",
            acid="Acetic Acid",
            base="Sodium Acetate",
            pka_values=[4.76],
            effective_ph_range=(4.0, 6.0),
            acid_mw=60.05,
            base_mw=82.03,
            notes="Vinegar odor, limited cosmetic use"
        ),
        "phosphate": BufferSystem(
            name="Phosphate Buffer",
            acid="Monosodium Phosphate",
            base="Disodium Phosphate",
            pka_values=[2.15, 7.20, 12.35],
            effective_ph_range=(6.0, 8.0),
            acid_mw=119.98,
            base_mw=141.96,
            notes="Physiological buffer, good for cleansers"
        ),
        "glucono_gluconate": BufferSystem(
            name="Gluconolactone / Sodium Gluconate",
            acid="Gluconolactone",
            base="Sodium Gluconate",
            pka_values=[3.6],
            effective_ph_range=(3.0, 4.5),
            acid_mw=178.14,
            base_mw=218.14,
            notes="PHA, gentle exfoliation"
        )
    }

    @classmethod
    def get_buffer(cls, name: str) -> Optional[BufferSystem]:
        """버퍼 시스템 조회"""
        return cls.BUFFERS.get(name)

    @classmethod
    def suggest_buffer_for_ph(cls, target_ph: float) -> List[Dict]:
        """목표 pH에 적합한 버퍼 추천"""
        suggestions = []
        for key, buffer in cls.BUFFERS.items():
            if buffer.effective_ph_range[0] <= target_ph <= buffer.effective_ph_range[1]:
                # 가장 가까운 pKa 찾기
                closest_pka = min(buffer.pka_values, key=lambda x: abs(x - target_ph))
                distance = abs(closest_pka - target_ph)

                suggestions.append({
                    "buffer_key": key,
                    "name": buffer.name,
                    "closest_pka": closest_pka,
                    "distance_from_pka": round(distance, 2),
                    "effective_range": buffer.effective_ph_range,
                    "notes": buffer.notes
                })

        # pKa와 가까운 순으로 정렬 (버퍼 효율이 높음)
        suggestions.sort(key=lambda x: x["distance_from_pka"])
        return suggestions


@dataclass
class pHAdjuster:
    """pH 조정제 데이터 클래스"""
    name: str
    inci: str
    type: str  # "acid" or "base"
    strength: str  # "strong" or "weak"
    pka: Optional[float]
    mw: float
    typical_solution: str
    notes: Optional[str] = None


class AdjusterDatabase:
    """pH 조정제 데이터베이스"""

    ADJUSTERS = {
        # 산
        "citric_acid": pHAdjuster(
            name="Citric Acid",
            inci="Citric Acid",
            type="acid",
            strength="weak",
            pka=3.13,
            mw=192.12,
            typical_solution="10% w/w",
            notes="Most common, also chelating agent"
        ),
        "lactic_acid": pHAdjuster(
            name="Lactic Acid",
            inci="Lactic Acid",
            type="acid",
            strength="weak",
            pka=3.86,
            mw=90.08,
            typical_solution="10% w/w",
            notes="AHA, moisturizing effect"
        ),
        "glycolic_acid": pHAdjuster(
            name="Glycolic Acid",
            inci="Glycolic Acid",
            type="acid",
            strength="weak",
            pka=3.83,
            mw=76.05,
            typical_solution="10% w/w",
            notes="AHA, penetration enhancer"
        ),
        "phosphoric_acid": pHAdjuster(
            name="Phosphoric Acid",
            inci="Phosphoric Acid",
            type="acid",
            strength="weak",
            pka=2.15,
            mw=97.99,
            typical_solution="10% w/w",
            notes="For cleansers, triprotic"
        ),
        "hcl": pHAdjuster(
            name="Hydrochloric Acid",
            inci="Hydrochloric Acid",
            type="acid",
            strength="strong",
            pka=None,
            mw=36.46,
            typical_solution="1N (~3.6%)",
            notes="Strong, use with caution"
        ),

        # 알칼리
        "naoh": pHAdjuster(
            name="Sodium Hydroxide",
            inci="Sodium Hydroxide",
            type="base",
            strength="strong",
            pka=None,
            mw=40.00,
            typical_solution="10% w/w",
            notes="Most common base"
        ),
        "koh": pHAdjuster(
            name="Potassium Hydroxide",
            inci="Potassium Hydroxide",
            type="base",
            strength="strong",
            pka=None,
            mw=56.11,
            typical_solution="10% w/w",
            notes="Saponification, pH adjustment"
        ),
        "tea": pHAdjuster(
            name="Triethanolamine",
            inci="Triethanolamine",
            type="base",
            strength="weak",
            pka=7.76,
            mw=149.19,
            typical_solution="neat",
            notes="Gentle adjustment, carbomer neutralizer"
        ),
        "amp": pHAdjuster(
            name="Aminomethyl Propanol",
            inci="Aminomethyl Propanol",
            type="base",
            strength="weak",
            pka=9.96,
            mw=89.14,
            typical_solution="neat (95%)",
            notes="Carbomer neutralizer, less odor than TEA"
        ),
        "arginine": pHAdjuster(
            name="Arginine",
            inci="Arginine",
            type="base",
            strength="weak",
            pka=12.48,
            mw=174.20,
            typical_solution="powder",
            notes="Natural, amino acid"
        ),
        "sodium_citrate": pHAdjuster(
            name="Trisodium Citrate",
            inci="Trisodium Citrate",
            type="base",
            strength="weak",
            pka=None,
            mw=294.10,
            typical_solution="10% w/w",
            notes="Buffer component, mild"
        )
    }

    @classmethod
    def get_adjuster(cls, name: str) -> Optional[pHAdjuster]:
        """조정제 조회"""
        return cls.ADJUSTERS.get(name)

    @classmethod
    def get_acids(cls) -> List[pHAdjuster]:
        """산 목록"""
        return [adj for adj in cls.ADJUSTERS.values() if adj.type == "acid"]

    @classmethod
    def get_bases(cls) -> List[pHAdjuster]:
        """알칼리 목록"""
        return [adj for adj in cls.ADJUSTERS.values() if adj.type == "base"]


def calculate_buffer_ratio(target_ph: float, pka: float) -> Dict:
    """
    Henderson-Hasselbalch 방정식으로 버퍼 비율 계산

    Args:
        target_ph: 목표 pH
        pka: 산의 pKa

    Returns:
        {
            "target_ph": float,
            "pka": float,
            "acid_ratio": float,    # 산의 비율 (0-1)
            "base_ratio": float,    # 짝염기의 비율 (0-1)
            "acid_percent": float,  # 산의 백분율
            "base_percent": float,  # 짝염기의 백분율
            "buffer_efficiency": str
        }
    """
    # Henderson-Hasselbalch: pH = pKa + log([A-]/[HA])
    # [A-]/[HA] = 10^(pH - pKa)

    ratio = 10 ** (target_ph - pka)

    # 정규화 (합이 1)
    base_ratio = ratio / (1 + ratio)  # [A-] / ([A-] + [HA])
    acid_ratio = 1 / (1 + ratio)      # [HA] / ([A-] + [HA])

    # 버퍼 효율 평가
    distance = abs(target_ph - pka)
    if distance <= 0.5:
        efficiency = "Excellent (within pKa +/- 0.5)"
    elif distance <= 1.0:
        efficiency = "Good (within pKa +/- 1.0)"
    else:
        efficiency = "Poor (outside optimal buffer range)"

    return {
        "target_ph": target_ph,
        "pka": pka,
        "acid_ratio": round(acid_ratio, 4),
        "base_ratio": round(base_ratio, 4),
        "acid_percent": round(acid_ratio * 100, 1),
        "base_percent": round(base_ratio * 100, 1),
        "buffer_efficiency": efficiency
    }


def calculate_buffer_capacity(total_concentration: float, target_ph: float, pka: float) -> Dict:
    """
    버퍼 용량 계산

    Args:
        total_concentration: 총 버퍼 농도 (mol/L)
        target_ph: 목표 pH
        pka: 산의 pKa

    Returns:
        버퍼 용량 및 관련 정보
    """
    # Ka 계산
    ka = 10 ** (-pka)

    # H+ 농도
    h_conc = 10 ** (-target_ph)

    # 버퍼 용량: β = 2.303 × C × Ka × [H+] / (Ka + [H+])²
    numerator = 2.303 * total_concentration * ka * h_conc
    denominator = (ka + h_conc) ** 2
    buffer_capacity = numerator / denominator

    # 최대 버퍼 용량 (pH = pKa일 때)
    max_capacity = 0.576 * total_concentration

    return {
        "buffer_capacity": round(buffer_capacity, 6),
        "max_capacity": round(max_capacity, 6),
        "efficiency_percent": round((buffer_capacity / max_capacity) * 100, 1),
        "unit": "mol/L/pH",
        "note": f"Maximum capacity occurs at pH = pKa ({pka})"
    }


def calculate_acid_needed(current_ph: float, target_ph: float,
                          volume_ml: float, buffer_capacity: float = 0.01) -> Dict:
    """
    pH를 낮추기 위해 필요한 산의 양 계산

    Args:
        current_ph: 현재 pH
        target_ph: 목표 pH (current_ph보다 낮아야 함)
        volume_ml: 용액 부피 (mL)
        buffer_capacity: 버퍼 용량 (mol/L/pH), 기본 0.01

    Returns:
        필요한 산의 양 및 조정제 환산량
    """
    if target_ph >= current_ph:
        return {
            "error": "target_ph must be lower than current_ph for acid addition",
            "suggestion": "Use calculate_base_needed() for raising pH"
        }

    delta_ph = current_ph - target_ph
    volume_l = volume_ml / 1000

    # 필요한 산 (mol)
    acid_mol = buffer_capacity * volume_l * delta_ph
    acid_mmol = acid_mol * 1000

    # 조정제 환산
    citric_10pct = acid_mmol / (100 / 192.12 * 1000) * 1000  # 10% 시트르산 (mL)
    lactic_10pct = acid_mmol / (100 / 90.08 * 1000) * 1000   # 10% 젖산 (mL)
    hcl_1n = acid_mmol / 1000  # 1N HCl (mL)

    return {
        "current_ph": current_ph,
        "target_ph": target_ph,
        "delta_ph": round(delta_ph, 2),
        "volume_ml": volume_ml,
        "buffer_capacity": buffer_capacity,
        "acid_needed_mmol": round(acid_mmol, 3),
        "adjusters": {
            "citric_acid_10pct_ml": round(citric_10pct, 2),
            "lactic_acid_10pct_ml": round(lactic_10pct, 2),
            "hcl_1n_ml": round(hcl_1n, 3)
        },
        "note": "These are estimates. Titrate to exact pH."
    }


def calculate_base_needed(current_ph: float, target_ph: float,
                          volume_ml: float, buffer_capacity: float = 0.01) -> Dict:
    """
    pH를 높이기 위해 필요한 알칼리의 양 계산

    Args:
        current_ph: 현재 pH
        target_ph: 목표 pH (current_ph보다 높아야 함)
        volume_ml: 용액 부피 (mL)
        buffer_capacity: 버퍼 용량 (mol/L/pH), 기본 0.01

    Returns:
        필요한 알칼리의 양 및 조정제 환산량
    """
    if target_ph <= current_ph:
        return {
            "error": "target_ph must be higher than current_ph for base addition",
            "suggestion": "Use calculate_acid_needed() for lowering pH"
        }

    delta_ph = target_ph - current_ph
    volume_l = volume_ml / 1000

    # 필요한 알칼리 (mol)
    base_mol = buffer_capacity * volume_l * delta_ph
    base_mmol = base_mol * 1000

    # 조정제 환산
    naoh_10pct = base_mmol / (100 / 40.00 * 1000) * 1000   # 10% NaOH (mL)
    tea_neat = base_mmol / (1000 / 149.19) * 1000          # TEA neat (mL)
    amp_95pct = base_mmol / (950 / 89.14 * 1000) * 1000    # AMP 95% (mL)

    return {
        "current_ph": current_ph,
        "target_ph": target_ph,
        "delta_ph": round(delta_ph, 2),
        "volume_ml": volume_ml,
        "buffer_capacity": buffer_capacity,
        "base_needed_mmol": round(base_mmol, 3),
        "adjusters": {
            "naoh_10pct_ml": round(naoh_10pct, 2),
            "tea_neat_ml": round(tea_neat, 2),
            "amp_95pct_ml": round(amp_95pct, 2)
        },
        "note": "These are estimates. Titrate to exact pH."
    }


def design_citrate_buffer(target_ph: float, total_buffer_percent: float,
                          batch_size_g: float) -> Dict:
    """
    시트르산/소듐시트레이트 버퍼 설계

    Args:
        target_ph: 목표 pH
        total_buffer_percent: 총 버퍼 농도 (%)
        batch_size_g: 배치 크기 (g)

    Returns:
        버퍼 구성 및 중량
    """
    # 시트르산 pKa2 = 4.76 사용 (pH 3.5-5.5 범위 최적)
    pka = 4.76

    # pH가 3.5 미만이면 pKa1 = 3.13 사용
    if target_ph < 3.5:
        pka = 3.13

    ratio = calculate_buffer_ratio(target_ph, pka)

    # 중량 계산
    total_buffer_g = batch_size_g * (total_buffer_percent / 100)
    citric_acid_g = total_buffer_g * ratio["acid_ratio"]
    sodium_citrate_g = total_buffer_g * ratio["base_ratio"]

    return {
        "target_ph": target_ph,
        "pka_used": pka,
        "total_buffer_percent": total_buffer_percent,
        "batch_size_g": batch_size_g,
        "components": {
            "citric_acid": {
                "percent": round(total_buffer_percent * ratio["acid_ratio"], 3),
                "weight_g": round(citric_acid_g, 3),
                "inci": "Citric Acid"
            },
            "sodium_citrate": {
                "percent": round(total_buffer_percent * ratio["base_ratio"], 3),
                "weight_g": round(sodium_citrate_g, 3),
                "inci": "Trisodium Citrate"
            }
        },
        "buffer_efficiency": ratio["buffer_efficiency"]
    }


def design_lactate_buffer(target_ph: float, total_buffer_percent: float,
                          batch_size_g: float) -> Dict:
    """
    젖산/소듐락테이트 버퍼 설계

    Args:
        target_ph: 목표 pH
        total_buffer_percent: 총 버퍼 농도 (%)
        batch_size_g: 배치 크기 (g)

    Returns:
        버퍼 구성 및 중량
    """
    pka = 3.86  # 젖산 pKa

    if target_ph < 3.0 or target_ph > 5.0:
        return {
            "error": f"Target pH {target_ph} is outside effective range (3.0-5.0)",
            "suggestion": "Consider citrate buffer for wider pH range"
        }

    ratio = calculate_buffer_ratio(target_ph, pka)

    total_buffer_g = batch_size_g * (total_buffer_percent / 100)
    lactic_acid_g = total_buffer_g * ratio["acid_ratio"]
    sodium_lactate_g = total_buffer_g * ratio["base_ratio"]

    return {
        "target_ph": target_ph,
        "pka_used": pka,
        "total_buffer_percent": total_buffer_percent,
        "batch_size_g": batch_size_g,
        "components": {
            "lactic_acid": {
                "percent": round(total_buffer_percent * ratio["acid_ratio"], 3),
                "weight_g": round(lactic_acid_g, 3),
                "inci": "Lactic Acid"
            },
            "sodium_lactate": {
                "percent": round(total_buffer_percent * ratio["base_ratio"], 3),
                "weight_g": round(sodium_lactate_g, 3),
                "inci": "Sodium Lactate"
            }
        },
        "buffer_efficiency": ratio["buffer_efficiency"],
        "note": "Lactic acid provides AHA benefits"
    }


def ph_sensitive_ingredient_check(target_ph: float) -> Dict:
    """
    pH에 민감한 성분 호환성 체크

    Args:
        target_ph: 목표 pH

    Returns:
        성분별 호환성 정보
    """
    SENSITIVE_INGREDIENTS = {
        "l_ascorbic_acid": {
            "optimal_range": (2.5, 3.5),
            "concern": "Oxidation at pH > 4",
            "note": "Low pH essential for stability and penetration"
        },
        "niacinamide": {
            "optimal_range": (5.0, 7.0),
            "concern": "Converts to nicotinic acid at pH < 4",
            "note": "Avoid combining with low pH products"
        },
        "retinol": {
            "optimal_range": (5.5, 6.5),
            "concern": "Degradation at pH > 7",
            "note": "Neutral to slightly acidic preferred"
        },
        "salicylic_acid": {
            "optimal_range": (3.0, 4.0),
            "concern": "Reduced efficacy at pH > 4",
            "note": "pKa = 2.97, needs low pH"
        },
        "glycolic_acid": {
            "optimal_range": (3.0, 4.0),
            "concern": "Reduced efficacy at pH > 4",
            "note": "pKa = 3.83"
        },
        "hyaluronic_acid": {
            "optimal_range": (5.0, 8.0),
            "concern": "Degradation at pH < 4 or > 9",
            "note": "Neutral pH preferred"
        },
        "vitamin_e": {
            "optimal_range": (5.0, 8.0),
            "concern": "Saponification at pH > 8",
            "note": "Avoid alkaline"
        },
        "peptides": {
            "optimal_range": (5.0, 7.0),
            "concern": "Hydrolysis at extreme pH",
            "note": "Check specific peptide requirements"
        }
    }

    compatible = []
    incompatible = []
    caution = []

    for ingredient, info in SENSITIVE_INGREDIENTS.items():
        opt_min, opt_max = info["optimal_range"]

        if opt_min <= target_ph <= opt_max:
            compatible.append({
                "ingredient": ingredient,
                "status": "compatible",
                "optimal_range": info["optimal_range"]
            })
        elif abs(target_ph - opt_min) <= 0.5 or abs(target_ph - opt_max) <= 0.5:
            caution.append({
                "ingredient": ingredient,
                "status": "caution",
                "optimal_range": info["optimal_range"],
                "concern": info["concern"]
            })
        else:
            incompatible.append({
                "ingredient": ingredient,
                "status": "incompatible",
                "optimal_range": info["optimal_range"],
                "concern": info["concern"],
                "note": info["note"]
            })

    return {
        "target_ph": target_ph,
        "compatible": compatible,
        "caution": caution,
        "incompatible": incompatible
    }


# 사용 예시
if __name__ == "__main__":
    print("=" * 60)
    print("pH Buffer Calculator - Example Usage")
    print("=" * 60)

    # 1. 버퍼 비율 계산
    print("\n1. Buffer Ratio Calculation (pH 4.5)")
    print("-" * 40)
    ratio = calculate_buffer_ratio(target_ph=4.5, pka=4.76)
    print(f"Target pH: {ratio['target_ph']}")
    print(f"pKa: {ratio['pka']}")
    print(f"Acid ratio: {ratio['acid_percent']}%")
    print(f"Base ratio: {ratio['base_percent']}%")
    print(f"Efficiency: {ratio['buffer_efficiency']}")

    # 2. 시트레이트 버퍼 설계
    print("\n2. Citrate Buffer Design (pH 5.0, 0.2%)")
    print("-" * 40)
    buffer = design_citrate_buffer(target_ph=5.0, total_buffer_percent=0.2, batch_size_g=1000)
    print(f"Citric Acid: {buffer['components']['citric_acid']['percent']}% ({buffer['components']['citric_acid']['weight_g']}g)")
    print(f"Sodium Citrate: {buffer['components']['sodium_citrate']['percent']}% ({buffer['components']['sodium_citrate']['weight_g']}g)")

    # 3. pH 조정 계산
    print("\n3. Acid Addition Calculation")
    print("-" * 40)
    acid = calculate_acid_needed(current_ph=6.5, target_ph=5.5, volume_ml=500)
    print(f"From pH {acid['current_ph']} to {acid['target_ph']}")
    print(f"Citric Acid 10%: ~{acid['adjusters']['citric_acid_10pct_ml']} mL")

    # 4. 성분 호환성 체크
    print("\n4. Ingredient Compatibility at pH 3.5")
    print("-" * 40)
    compat = ph_sensitive_ingredient_check(target_ph=3.5)
    print("Compatible:", [i["ingredient"] for i in compat["compatible"]])
    print("Caution:", [i["ingredient"] for i in compat["caution"]])
    print("Incompatible:", [i["ingredient"] for i in compat["incompatible"]])

    # 5. 버퍼 추천
    print("\n5. Buffer Suggestion for pH 4.5")
    print("-" * 40)
    suggestions = BufferDatabase.suggest_buffer_for_ph(4.5)
    for s in suggestions[:2]:
        print(f"- {s['name']} (pKa: {s['closest_pka']}, distance: {s['distance_from_pka']})")
