#!/usr/bin/env python3
"""
Viscosity Predictor for Cosmetic Formulation

화장품 제형의 점도 예측 및 점증제 선택 도구
- 점증제 농도-점도 관계 예측
- 온도 보정
- 점증제 선택 가이드

Author: EVAS Cosmetic
License: MIT
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import math


@dataclass
class Thickener:
    """점증제 데이터 클래스"""
    name: str
    inci: str
    type: str  # "synthetic", "natural", "cellulose"
    ionic: str  # "anionic", "nonionic", "cationic"
    ph_range: Tuple[float, float]
    electrolyte_sensitivity: str  # "high", "medium", "low"
    appearance: str
    typical_concentration: Tuple[float, float]
    notes: Optional[str] = None


class ThickenerDatabase:
    """점증제 데이터베이스"""

    THICKENERS = {
        # 카보머 시리즈
        "carbomer_934": Thickener(
            name="Carbomer 934",
            inci="Carbomer",
            type="synthetic",
            ionic="anionic",
            ph_range=(4.5, 8.0),
            electrolyte_sensitivity="high",
            appearance="clear gel",
            typical_concentration=(0.1, 0.5),
            notes="Lower viscosity grade"
        ),
        "carbomer_940": Thickener(
            name="Carbomer 940",
            inci="Carbomer",
            type="synthetic",
            ionic="anionic",
            ph_range=(4.5, 8.0),
            electrolyte_sensitivity="high",
            appearance="clear gel",
            typical_concentration=(0.1, 0.5),
            notes="Most common, short flow"
        ),
        "carbomer_941": Thickener(
            name="Carbomer 941",
            inci="Carbomer",
            type="synthetic",
            ionic="anionic",
            ph_range=(4.5, 8.0),
            electrolyte_sensitivity="high",
            appearance="clear gel",
            typical_concentration=(0.2, 1.0),
            notes="Long flow, for lotions"
        ),
        "carbomer_ultrez_10": Thickener(
            name="Carbomer Ultrez 10",
            inci="Carbomer",
            type="synthetic",
            ionic="anionic",
            ph_range=(4.5, 8.0),
            electrolyte_sensitivity="high",
            appearance="clear gel",
            typical_concentration=(0.1, 0.4),
            notes="Highest efficiency"
        ),
        "carbomer_ultrez_20": Thickener(
            name="Carbomer Ultrez 20",
            inci="Acrylates/C10-30 Alkyl Acrylate Crosspolymer",
            type="synthetic",
            ionic="anionic",
            ph_range=(4.5, 8.0),
            electrolyte_sensitivity="medium",
            appearance="clear gel",
            typical_concentration=(0.2, 0.8),
            notes="Better electrolyte tolerance"
        ),

        # 천연 검류
        "xanthan_gum": Thickener(
            name="Xanthan Gum",
            inci="Xanthan Gum",
            type="natural",
            ionic="anionic",
            ph_range=(2.0, 12.0),
            electrolyte_sensitivity="low",
            appearance="slightly hazy",
            typical_concentration=(0.1, 1.5),
            notes="Strong pseudoplastic, wide pH"
        ),
        "guar_gum": Thickener(
            name="Guar Gum",
            inci="Guar Gum",
            type="natural",
            ionic="nonionic",
            ph_range=(4.0, 10.0),
            electrolyte_sensitivity="medium",
            appearance="hazy",
            typical_concentration=(0.2, 1.0),
            notes="Economical, high viscosity"
        ),
        "sclerotium_gum": Thickener(
            name="Sclerotium Gum",
            inci="Sclerotium Gum",
            type="natural",
            ionic="nonionic",
            ph_range=(3.0, 11.0),
            electrolyte_sensitivity="low",
            appearance="clear gel",
            typical_concentration=(0.5, 2.0),
            notes="Natural, good clarity"
        ),

        # 셀룰로오스 유도체
        "hec": Thickener(
            name="Hydroxyethylcellulose",
            inci="Hydroxyethylcellulose",
            type="cellulose",
            ionic="nonionic",
            ph_range=(2.0, 12.0),
            electrolyte_sensitivity="low",
            appearance="clear to hazy",
            typical_concentration=(0.5, 2.0),
            notes="Nonionic, electrolyte resistant"
        ),
        "hpmc": Thickener(
            name="Hydroxypropyl Methylcellulose",
            inci="Hydroxypropyl Methylcellulose",
            type="cellulose",
            ionic="nonionic",
            ph_range=(3.0, 11.0),
            electrolyte_sensitivity="low",
            appearance="clear to hazy",
            typical_concentration=(0.5, 2.0),
            notes="Film-forming, thermal gelation"
        ),
        "cmc": Thickener(
            name="Carboxymethylcellulose",
            inci="Cellulose Gum",
            type="cellulose",
            ionic="anionic",
            ph_range=(4.0, 10.0),
            electrolyte_sensitivity="medium",
            appearance="clear to hazy",
            typical_concentration=(0.5, 2.0),
            notes="Anionic, avoid low pH"
        ),

        # 프리메이드 시스템
        "sepigel_305": Thickener(
            name="Sepigel 305",
            inci="Polyacrylamide (and) C13-14 Isoparaffin (and) Laureth-7",
            type="synthetic",
            ionic="nonionic",
            ph_range=(3.0, 12.0),
            electrolyte_sensitivity="low",
            appearance="white cream",
            typical_concentration=(1.0, 4.0),
            notes="Pre-neutralized, easy to use"
        ),
        "sepimax_zen": Thickener(
            name="Sepimax Zen",
            inci="Polyacrylate Crosspolymer-6",
            type="synthetic",
            ionic="nonionic",
            ph_range=(3.0, 12.0),
            electrolyte_sensitivity="low",
            appearance="white cream",
            typical_concentration=(0.3, 2.0),
            notes="Excellent electrolyte tolerance"
        )
    }

    @classmethod
    def get_thickener(cls, name: str) -> Optional[Thickener]:
        """점증제 조회"""
        key = name.lower().replace(" ", "_").replace("-", "_")
        return cls.THICKENERS.get(key)

    @classmethod
    def get_by_type(cls, thickener_type: str) -> List[Thickener]:
        """타입별 점증제 검색"""
        return [t for t in cls.THICKENERS.values() if t.type == thickener_type]

    @classmethod
    def get_electrolyte_resistant(cls) -> List[Thickener]:
        """전해질 내성 점증제 검색"""
        return [t for t in cls.THICKENERS.values() if t.electrolyte_sensitivity == "low"]

    @classmethod
    def get_clear_gel_formers(cls) -> List[Thickener]:
        """투명 젤 형성 점증제"""
        return [t for t in cls.THICKENERS.values() if "clear" in t.appearance.lower()]


def predict_viscosity(thickener: str, concentration: float,
                      grade: Optional[str] = None) -> Dict:
    """
    점증제 농도에 따른 점도 예측

    Args:
        thickener: 점증제 종류 ("carbomer", "xanthan", "hec" 등)
        concentration: 점증제 농도 (%)
        grade: 점증제 등급 (선택)

    Returns:
        예측 점도 및 관련 정보
    """
    thickener_lower = thickener.lower()

    # 경험적 모델 계수 (log(viscosity) = a + b * concentration)
    MODELS = {
        "carbomer": {
            "934": {"a": 2.0, "b": 3.0, "unit": "cP", "temp": 25},
            "940": {"a": 2.5, "b": 3.5, "unit": "cP", "temp": 25},
            "941": {"a": 2.0, "b": 3.2, "unit": "cP", "temp": 25},
            "ultrez_10": {"a": 2.8, "b": 3.8, "unit": "cP", "temp": 25},
            "ultrez_20": {"a": 2.3, "b": 3.3, "unit": "cP", "temp": 25},
            "default": {"a": 2.5, "b": 3.5, "unit": "cP", "temp": 25}
        },
        "xanthan": {
            "default": {"a": 1.8, "b": 2.8, "unit": "cP", "temp": 25}
        },
        "hec": {
            "250lhr": {"a": 1.0, "b": 1.2, "unit": "cP", "temp": 25},
            "250mhr": {"a": 1.5, "b": 1.5, "unit": "cP", "temp": 25},
            "250hhr": {"a": 1.8, "b": 1.8, "unit": "cP", "temp": 25},
            "default": {"a": 1.5, "b": 1.5, "unit": "cP", "temp": 25}
        },
        "guar": {
            "default": {"a": 2.0, "b": 2.5, "unit": "cP", "temp": 25}
        },
        "cmc": {
            "default": {"a": 1.3, "b": 1.8, "unit": "cP", "temp": 25}
        },
        "sepigel_305": {
            "default": {"a": 2.0, "b": 1.5, "unit": "cP", "temp": 25}
        }
    }

    # 모델 선택
    if thickener_lower not in MODELS:
        return {
            "error": f"Unknown thickener: {thickener}",
            "available": list(MODELS.keys())
        }

    model_group = MODELS[thickener_lower]
    grade_key = grade.lower().replace(" ", "_") if grade else "default"

    if grade_key in model_group:
        model = model_group[grade_key]
    else:
        model = model_group["default"]

    # 점도 계산
    log_visc = model["a"] + model["b"] * concentration
    viscosity = 10 ** log_visc

    # 점도 범위 (±20%)
    visc_low = viscosity * 0.8
    visc_high = viscosity * 1.2

    return {
        "thickener": thickener,
        "grade": grade or "default",
        "concentration_pct": concentration,
        "predicted_viscosity_cP": round(viscosity, 0),
        "viscosity_range": f"{round(visc_low, 0)}-{round(visc_high, 0)} cP",
        "measurement_temp": model["temp"],
        "model_note": "Empirical model, verify experimentally"
    }


def predict_concentration(thickener: str, target_viscosity: float,
                          grade: Optional[str] = None) -> Dict:
    """
    목표 점도를 위한 점증제 농도 예측 (역계산)

    Args:
        thickener: 점증제 종류
        target_viscosity: 목표 점도 (cP)
        grade: 점증제 등급 (선택)

    Returns:
        예측 농도 및 권장 사항
    """
    # 동일한 모델 계수 사용
    MODELS = {
        "carbomer": {"a": 2.5, "b": 3.5},
        "xanthan": {"a": 1.8, "b": 2.8},
        "hec": {"a": 1.5, "b": 1.5},
        "guar": {"a": 2.0, "b": 2.5},
        "cmc": {"a": 1.3, "b": 1.8},
        "sepigel_305": {"a": 2.0, "b": 1.5}
    }

    thickener_lower = thickener.lower()

    if thickener_lower not in MODELS:
        return {
            "error": f"Unknown thickener: {thickener}",
            "available": list(MODELS.keys())
        }

    model = MODELS[thickener_lower]

    # 역계산: concentration = (log(viscosity) - a) / b
    log_visc = math.log10(target_viscosity)
    concentration = (log_visc - model["a"]) / model["b"]

    # 농도 범위 (±15%)
    conc_low = concentration * 0.85
    conc_high = concentration * 1.15

    # 실용 범위 확인
    thickener_data = ThickenerDatabase.get_thickener(thickener_lower)
    if thickener_data:
        typical_range = thickener_data.typical_concentration
        in_range = typical_range[0] <= concentration <= typical_range[1]
    else:
        typical_range = None
        in_range = True

    return {
        "thickener": thickener,
        "target_viscosity_cP": target_viscosity,
        "predicted_concentration_pct": round(concentration, 2),
        "concentration_range": f"{round(conc_low, 2)}-{round(conc_high, 2)}%",
        "typical_range": typical_range,
        "within_typical_range": in_range,
        "note": "Start with lower range and adjust experimentally"
    }


def temperature_correction(viscosity_at_t1: float, t1: float, t2: float,
                           ea: float = 25000) -> Dict:
    """
    Arrhenius 모델로 온도에 따른 점도 보정

    Args:
        viscosity_at_t1: T1에서의 점도 (cP)
        t1: 측정 온도 (°C)
        t2: 목표 온도 (°C)
        ea: 활성화 에너지 (J/mol), 기본 25000 (로션/크림)

    Returns:
        보정된 점도 및 관련 정보
    """
    R = 8.314  # 기체 상수 (J/mol·K)

    T1_K = t1 + 273.15
    T2_K = t2 + 273.15

    # Arrhenius 방정식
    # ln(η2/η1) = (Ea/R) × (1/T2 - 1/T1)
    exponent = (ea / R) * (1/T2_K - 1/T1_K)
    ratio = math.exp(exponent)

    viscosity_at_t2 = viscosity_at_t1 * ratio

    # 온도 변화에 따른 변화율
    if t2 > t1:
        change_type = "decrease"
        change_pct = (1 - ratio) * 100
    else:
        change_type = "increase"
        change_pct = (ratio - 1) * 100

    return {
        "input": {
            "viscosity_cP": viscosity_at_t1,
            "temperature_C": t1
        },
        "output": {
            "viscosity_cP": round(viscosity_at_t2, 0),
            "temperature_C": t2
        },
        "change": {
            "type": change_type,
            "percent": round(abs(change_pct), 1),
            "ratio": round(ratio, 3)
        },
        "activation_energy_J_mol": ea,
        "note": "Ea varies by formulation (15-50 kJ/mol typical)"
    }


def brookfield_spindle_selection(expected_viscosity: float,
                                 viscometer_type: str = "LV") -> Dict:
    """
    Brookfield 점도계 스핀들 및 속도 추천

    Args:
        expected_viscosity: 예상 점도 (cP)
        viscometer_type: 점도계 타입 ("LV", "RV", "HA", "HB")

    Returns:
        추천 스핀들 및 속도
    """
    # 스핀들별 측정 범위 (cP at 100% torque)
    SPINDLES = {
        "LV": {
            "1": {"range": (1, 60), "factor": 0.6},
            "2": {"range": (60, 300), "factor": 3.0},
            "3": {"range": (300, 1200), "factor": 12.0},
            "4": {"range": (1200, 6000), "factor": 60.0}
        },
        "RV": {
            "1": {"range": (100, 800), "factor": 8.0},
            "2": {"range": (400, 3200), "factor": 32.0},
            "3": {"range": (1000, 8000), "factor": 80.0},
            "4": {"range": (2000, 16000), "factor": 160.0},
            "5": {"range": (4000, 32000), "factor": 320.0},
            "6": {"range": (10000, 80000), "factor": 800.0},
            "7": {"range": (20000, 160000), "factor": 1600.0}
        }
    }

    if viscometer_type not in SPINDLES:
        return {"error": f"Unknown viscometer type: {viscometer_type}"}

    spindles = SPINDLES[viscometer_type]
    recommendations = []

    for spindle_num, data in spindles.items():
        min_visc, max_visc = data["range"]

        if min_visc <= expected_viscosity <= max_visc:
            # 추천 RPM 계산 (20-80% 토크 범위)
            # 점도 = factor × 100 / RPM × torque%
            # RPM = factor × 100 / 점도 × 50 (50% 토크 목표)

            target_torque = 50  # 목표 토크 %
            factor = data["factor"]

            # RPM = (factor / viscosity) × (100 / torque%) × 100
            calculated_rpm = (factor * 100 * 100) / (expected_viscosity * target_torque)

            # 표준 RPM으로 반올림
            STANDARD_RPMS = [0.3, 0.5, 0.6, 1, 1.5, 2, 2.5, 3, 4, 5, 6, 10, 12, 20, 30, 50, 60, 100]
            closest_rpm = min(STANDARD_RPMS, key=lambda x: abs(x - calculated_rpm))

            # 해당 RPM에서 예상 토크
            expected_torque = (factor * 100 * 100) / (expected_viscosity * closest_rpm)

            if 20 <= expected_torque <= 80:
                recommendations.append({
                    "spindle": f"{viscometer_type}{spindle_num}",
                    "rpm": closest_rpm,
                    "expected_torque_pct": round(expected_torque, 1),
                    "measurement_range": f"{min_visc}-{max_visc} cP"
                })

    if not recommendations:
        return {
            "expected_viscosity": expected_viscosity,
            "viscometer_type": viscometer_type,
            "error": "No suitable spindle/speed combination found",
            "suggestion": "Try different viscometer type or verify expected viscosity"
        }

    return {
        "expected_viscosity_cP": expected_viscosity,
        "viscometer_type": viscometer_type,
        "recommendations": recommendations,
        "note": "Aim for 20-80% torque for best accuracy"
    }


def thickener_selection_guide(requirements: Dict) -> Dict:
    """
    요구사항에 따른 점증제 추천

    Args:
        requirements: {
            "target_viscosity": float (cP),
            "ph": float,
            "has_electrolytes": bool,
            "clear_gel_needed": bool,
            "natural_preferred": bool
        }

    Returns:
        추천 점증제 목록
    """
    all_thickeners = list(ThickenerDatabase.THICKENERS.values())
    recommendations = []

    target_visc = requirements.get("target_viscosity", 5000)
    ph = requirements.get("ph", 6.0)
    has_electrolytes = requirements.get("has_electrolytes", False)
    clear_gel = requirements.get("clear_gel_needed", False)
    natural_pref = requirements.get("natural_preferred", False)

    for t in all_thickeners:
        score = 100  # 기본 점수
        notes = []

        # pH 호환성
        if not (t.ph_range[0] <= ph <= t.ph_range[1]):
            score -= 100
            notes.append(f"pH {ph} outside range {t.ph_range}")

        # 전해질 내성
        if has_electrolytes:
            if t.electrolyte_sensitivity == "high":
                score -= 40
                notes.append("High electrolyte sensitivity")
            elif t.electrolyte_sensitivity == "medium":
                score -= 20
                notes.append("Medium electrolyte sensitivity")

        # 투명성
        if clear_gel and "clear" not in t.appearance.lower():
            score -= 30
            notes.append("May not form clear gel")

        # 천연 선호
        if natural_pref:
            if t.type == "natural":
                score += 20
                notes.append("Natural origin (bonus)")
            elif t.type == "synthetic":
                score -= 20
                notes.append("Synthetic (penalty for natural preference)")

        # 점도 범위 적합성
        conc_result = predict_concentration(t.name.split()[0].lower(), target_visc)
        if "error" not in conc_result:
            predicted_conc = conc_result.get("predicted_concentration_pct", 0)
            if t.typical_concentration[0] <= predicted_conc <= t.typical_concentration[1]:
                notes.append(f"Predicted concentration: {predicted_conc:.2f}%")
            else:
                score -= 15
                notes.append(f"Concentration ({predicted_conc:.2f}%) outside typical range")

        if score > 0:
            recommendations.append({
                "name": t.name,
                "inci": t.inci,
                "score": score,
                "type": t.type,
                "typical_concentration": t.typical_concentration,
                "notes": notes
            })

    # 점수순 정렬
    recommendations.sort(key=lambda x: x["score"], reverse=True)

    return {
        "requirements": requirements,
        "recommendations": recommendations[:5],  # 상위 5개
        "total_evaluated": len(all_thickeners)
    }


# 사용 예시
if __name__ == "__main__":
    print("=" * 60)
    print("Viscosity Predictor - Example Usage")
    print("=" * 60)

    # 1. 점도 예측
    print("\n1. Viscosity Prediction - Carbomer 940 at 0.3%")
    print("-" * 40)
    result = predict_viscosity("carbomer", 0.3, "940")
    print(f"Predicted: {result['predicted_viscosity_cP']} cP")
    print(f"Range: {result['viscosity_range']}")

    # 2. 농도 예측
    print("\n2. Concentration Prediction - 10,000 cP with Xanthan")
    print("-" * 40)
    conc = predict_concentration("xanthan", 10000)
    print(f"Predicted concentration: {conc['predicted_concentration_pct']}%")
    print(f"Range: {conc['concentration_range']}")

    # 3. 온도 보정
    print("\n3. Temperature Correction - 10,000 cP at 25C to 20C")
    print("-" * 40)
    temp = temperature_correction(10000, 25, 20)
    print(f"At 25°C: {temp['input']['viscosity_cP']} cP")
    print(f"At 20°C: {temp['output']['viscosity_cP']} cP")
    print(f"Change: {temp['change']['type']} by {temp['change']['percent']}%")

    # 4. Brookfield 스핀들 선택
    print("\n4. Brookfield Spindle Selection - 5,000 cP")
    print("-" * 40)
    spindle = brookfield_spindle_selection(5000, "LV")
    if "recommendations" in spindle:
        for rec in spindle["recommendations"]:
            print(f"Spindle {rec['spindle']} at {rec['rpm']} RPM (torque ~{rec['expected_torque_pct']}%)")

    # 5. 점증제 선택 가이드
    print("\n5. Thickener Selection Guide")
    print("-" * 40)
    requirements = {
        "target_viscosity": 8000,
        "ph": 5.5,
        "has_electrolytes": True,
        "clear_gel_needed": True,
        "natural_preferred": False
    }
    guide = thickener_selection_guide(requirements)
    print(f"Requirements: {requirements}")
    print("Top recommendations:")
    for rec in guide["recommendations"][:3]:
        print(f"  - {rec['name']} (score: {rec['score']})")
