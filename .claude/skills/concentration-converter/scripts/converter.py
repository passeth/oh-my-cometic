#!/usr/bin/env python3
"""
Concentration Converter for Cosmetic Formulation

화장품 제형 개발용 농도 단위 변환 도구
- 퍼센트 변환 (w/w, w/v, v/v)
- ppm/ppb 변환
- 질량/부피 농도 변환
- 몰농도 변환
- 희석 계산
- 활성 농도 계산

Author: EVAS Cosmetic
License: MIT
"""

from dataclasses import dataclass
from typing import Dict, Optional, List, Union
from enum import Enum
import math


class ConcentrationUnit(Enum):
    """농도 단위 열거형"""
    PERCENT_WW = "% (w/w)"
    PERCENT_WV = "% (w/v)"
    PERCENT_VV = "% (v/v)"
    PPM = "ppm"
    PPB = "ppb"
    MG_G = "mg/g"
    MG_ML = "mg/mL"
    MG_KG = "mg/kg"
    MG_L = "mg/L"
    G_L = "g/L"
    UG_G = "μg/g"
    UG_ML = "μg/mL"
    MOLAR = "M"
    MILLIMOLAR = "mM"
    MICROMOLAR = "μM"


@dataclass
class Ingredient:
    """화장품 성분 데이터 클래스"""
    name: str
    molecular_weight: Optional[float] = None  # g/mol
    density: Optional[float] = None  # g/mL
    purity: float = 1.0  # 순도 (0-1)


# 주요 화장품 성분 분자량 데이터베이스
MOLECULAR_WEIGHTS: Dict[str, float] = {
    # 비타민
    "niacinamide": 122.12,
    "ascorbic_acid": 176.12,
    "retinol": 286.45,
    "tocopherol": 430.71,
    "panthenol": 205.25,
    "retinyl_palmitate": 524.86,
    "tocopheryl_acetate": 472.75,

    # AHA/BHA
    "glycolic_acid": 76.05,
    "lactic_acid": 90.08,
    "salicylic_acid": 138.12,
    "citric_acid": 192.12,
    "malic_acid": 134.09,
    "mandelic_acid": 152.15,
    "tartaric_acid": 150.09,

    # 보습제
    "hyaluronic_acid_unit": 401.30,  # 반복 단위
    "urea": 60.06,
    "allantoin": 158.12,

    # 기능성 성분
    "adenosine": 267.24,
    "arbutin": 272.25,
    "tranexamic_acid": 157.21,
    "kojic_acid": 142.11,

    # 아미노산
    "arginine": 174.20,
    "glycine": 75.07,
    "alanine": 89.09,

    # 방부제
    "phenoxyethanol": 138.16,
    "methylparaben": 152.15,
    "benzoic_acid": 122.12,
    "sorbic_acid": 112.13,

    # pH 조절제
    "triethanolamine": 149.19,
    "sodium_hydroxide": 40.00,
    "potassium_hydroxide": 56.11,
}


class ConcentrationConverter:
    """농도 변환 클래스"""

    @staticmethod
    def percent_to_ppm(percent: float) -> float:
        """
        % → ppm 변환

        Args:
            percent: 퍼센트 농도

        Returns:
            ppm 농도
        """
        return percent * 10000

    @staticmethod
    def ppm_to_percent(ppm: float) -> float:
        """
        ppm → % 변환

        Args:
            ppm: ppm 농도

        Returns:
            퍼센트 농도
        """
        return ppm / 10000

    @staticmethod
    def ppm_to_ppb(ppm: float) -> float:
        """ppm → ppb 변환"""
        return ppm * 1000

    @staticmethod
    def ppb_to_ppm(ppb: float) -> float:
        """ppb → ppm 변환"""
        return ppb / 1000

    @staticmethod
    def percent_to_mg_g(percent: float) -> float:
        """
        % (w/w) → mg/g 변환

        Args:
            percent: 퍼센트 농도 (w/w)

        Returns:
            mg/g 농도
        """
        return percent * 10

    @staticmethod
    def mg_g_to_percent(mg_g: float) -> float:
        """mg/g → % (w/w) 변환"""
        return mg_g / 10

    @staticmethod
    def percent_wv_to_mg_ml(percent_wv: float) -> float:
        """
        % (w/v) → mg/mL 변환

        Args:
            percent_wv: 퍼센트 농도 (w/v)

        Returns:
            mg/mL 농도
        """
        return percent_wv * 10

    @staticmethod
    def mg_ml_to_percent_wv(mg_ml: float) -> float:
        """mg/mL → % (w/v) 변환"""
        return mg_ml / 10

    @staticmethod
    def ppm_to_mg_g(ppm: float) -> float:
        """ppm → mg/g 변환"""
        return ppm / 1000

    @staticmethod
    def mg_g_to_ppm(mg_g: float) -> float:
        """mg/g → ppm 변환"""
        return mg_g * 1000

    @staticmethod
    def percent_ww_to_wv(
        percent_ww: float,
        solution_density: float
    ) -> float:
        """
        % (w/w) → % (w/v) 변환

        Args:
            percent_ww: 퍼센트 농도 (w/w)
            solution_density: 용액 밀도 (g/mL)

        Returns:
            % (w/v) 농도
        """
        return percent_ww * solution_density

    @staticmethod
    def percent_wv_to_ww(
        percent_wv: float,
        solution_density: float
    ) -> float:
        """
        % (w/v) → % (w/w) 변환

        Args:
            percent_wv: 퍼센트 농도 (w/v)
            solution_density: 용액 밀도 (g/mL)

        Returns:
            % (w/w) 농도
        """
        return percent_wv / solution_density

    @staticmethod
    def percent_vv_to_ww(
        percent_vv: float,
        solute_density: float,
        solution_density: float
    ) -> float:
        """
        % (v/v) → % (w/w) 변환

        Args:
            percent_vv: 퍼센트 농도 (v/v)
            solute_density: 용질 밀도 (g/mL)
            solution_density: 용액 밀도 (g/mL)

        Returns:
            % (w/w) 농도
        """
        return percent_vv * (solute_density / solution_density)

    @staticmethod
    def percent_ww_to_vv(
        percent_ww: float,
        solute_density: float,
        solution_density: float
    ) -> float:
        """
        % (w/w) → % (v/v) 변환

        Args:
            percent_ww: 퍼센트 농도 (w/w)
            solute_density: 용질 밀도 (g/mL)
            solution_density: 용액 밀도 (g/mL)

        Returns:
            % (v/v) 농도
        """
        return percent_ww * (solution_density / solute_density)

    @staticmethod
    def mg_ml_to_molar(
        mg_ml: float,
        molecular_weight: float
    ) -> float:
        """
        mg/mL → M (몰농도) 변환

        Args:
            mg_ml: mg/mL 농도
            molecular_weight: 분자량 (g/mol)

        Returns:
            몰농도 (M)
        """
        g_l = mg_ml  # mg/mL = g/L
        return g_l / molecular_weight

    @staticmethod
    def molar_to_mg_ml(
        molar: float,
        molecular_weight: float
    ) -> float:
        """
        M (몰농도) → mg/mL 변환

        Args:
            molar: 몰농도 (M)
            molecular_weight: 분자량 (g/mol)

        Returns:
            mg/mL 농도
        """
        return molar * molecular_weight

    @staticmethod
    def percent_wv_to_molar(
        percent_wv: float,
        molecular_weight: float
    ) -> float:
        """
        % (w/v) → M (몰농도) 변환

        Args:
            percent_wv: 퍼센트 농도 (w/v)
            molecular_weight: 분자량 (g/mol)

        Returns:
            몰농도 (M)
        """
        mg_ml = percent_wv * 10
        return mg_ml / molecular_weight

    @staticmethod
    def molar_to_percent_wv(
        molar: float,
        molecular_weight: float
    ) -> float:
        """
        M (몰농도) → % (w/v) 변환

        Args:
            molar: 몰농도 (M)
            molecular_weight: 분자량 (g/mol)

        Returns:
            % (w/v) 농도
        """
        mg_ml = molar * molecular_weight
        return mg_ml / 10

    @staticmethod
    def molar_to_millimolar(molar: float) -> float:
        """M → mM 변환"""
        return molar * 1000

    @staticmethod
    def millimolar_to_molar(millimolar: float) -> float:
        """mM → M 변환"""
        return millimolar / 1000

    @staticmethod
    def millimolar_to_micromolar(millimolar: float) -> float:
        """mM → μM 변환"""
        return millimolar * 1000

    @staticmethod
    def micromolar_to_millimolar(micromolar: float) -> float:
        """μM → mM 변환"""
        return micromolar / 1000


class DilutionCalculator:
    """희석 계산 클래스"""

    @staticmethod
    def calculate_stock_volume(
        c_final: float,
        v_final: float,
        c_stock: float
    ) -> float:
        """
        필요한 원액(stock) 부피 계산

        C1 × V1 = C2 × V2
        V1 = (C2 × V2) / C1

        Args:
            c_final: 최종 농도
            v_final: 최종 부피
            c_stock: 원액 농도

        Returns:
            필요한 원액 부피
        """
        if c_stock == 0:
            raise ValueError("Stock concentration cannot be zero")
        return (c_final * v_final) / c_stock

    @staticmethod
    def calculate_final_concentration(
        c_stock: float,
        v_stock: float,
        v_final: float
    ) -> float:
        """
        최종 농도 계산

        Args:
            c_stock: 원액 농도
            v_stock: 원액 부피
            v_final: 최종 부피

        Returns:
            최종 농도
        """
        if v_final == 0:
            raise ValueError("Final volume cannot be zero")
        return (c_stock * v_stock) / v_final

    @staticmethod
    def calculate_dilution_factor(
        c_stock: float,
        c_final: float
    ) -> float:
        """
        희석 배수 계산

        Args:
            c_stock: 원액 농도
            c_final: 최종 농도

        Returns:
            희석 배수 (예: 10배 희석 = 10)
        """
        if c_final == 0:
            raise ValueError("Final concentration cannot be zero")
        return c_stock / c_final

    @staticmethod
    def serial_dilution(
        c_initial: float,
        dilution_factor: float,
        n_dilutions: int
    ) -> List[float]:
        """
        연속 희석 농도 계산

        Args:
            c_initial: 초기 농도
            dilution_factor: 각 단계 희석 배수
            n_dilutions: 희석 횟수

        Returns:
            각 단계의 농도 리스트
        """
        concentrations = [c_initial]
        current = c_initial

        for _ in range(n_dilutions):
            current = current / dilution_factor
            concentrations.append(current)

        return concentrations


class ActiveConcentrationCalculator:
    """활성(유효) 성분 농도 계산 클래스"""

    @staticmethod
    def calculate_active_concentration(
        formula_percent: float,
        active_in_raw: float,
        purity: float = 1.0
    ) -> float:
        """
        실제 활성 성분 농도 계산

        Args:
            formula_percent: 배합률 (%)
            active_in_raw: 원료 내 활성 성분 비율 (0-1)
            purity: 순도 (0-1, 기본값 1.0)

        Returns:
            실제 활성 농도 (%)
        """
        return formula_percent * active_in_raw * purity

    @staticmethod
    def calculate_raw_material_amount(
        target_active: float,
        active_in_raw: float,
        purity: float = 1.0
    ) -> float:
        """
        목표 활성 농도를 위한 원료 배합량 계산

        Args:
            target_active: 목표 활성 농도 (%)
            active_in_raw: 원료 내 활성 성분 비율 (0-1)
            purity: 순도 (0-1, 기본값 1.0)

        Returns:
            필요한 원료 배합량 (%)
        """
        if active_in_raw == 0 or purity == 0:
            raise ValueError("Active ratio and purity cannot be zero")
        return target_active / (active_in_raw * purity)

    @staticmethod
    def compare_active_concentrations(
        materials: List[Dict]
    ) -> List[Dict]:
        """
        여러 원료의 활성 농도 비교

        Args:
            materials: 원료 정보 리스트
                [{"name": str, "formula_percent": float,
                  "active_ratio": float, "purity": float}, ...]

        Returns:
            활성 농도가 포함된 정렬된 리스트
        """
        results = []

        for mat in materials:
            active_conc = ActiveConcentrationCalculator.calculate_active_concentration(
                mat.get("formula_percent", 0),
                mat.get("active_ratio", 1.0),
                mat.get("purity", 1.0)
            )
            results.append({
                **mat,
                "active_concentration": round(active_conc, 4),
                "active_ppm": round(active_conc * 10000, 1)
            })

        # 활성 농도 내림차순 정렬
        results.sort(key=lambda x: x["active_concentration"], reverse=True)
        return results


def convert_concentration(
    value: float,
    from_unit: str,
    to_unit: str,
    molecular_weight: Optional[float] = None,
    solution_density: Optional[float] = None,
    solute_density: Optional[float] = None
) -> Dict:
    """
    범용 농도 단위 변환 함수

    Args:
        value: 변환할 값
        from_unit: 원래 단위 (예: "% (w/w)", "ppm", "mg/g", "M")
        to_unit: 목표 단위
        molecular_weight: 분자량 (몰농도 변환 시 필요)
        solution_density: 용액 밀도 (w/w ↔ w/v 변환 시 필요)
        solute_density: 용질 밀도 (v/v 변환 시 필요)

    Returns:
        {
            "original_value": float,
            "original_unit": str,
            "converted_value": float,
            "converted_unit": str,
            "formula": str
        }
    """
    conv = ConcentrationConverter()
    result = {
        "original_value": value,
        "original_unit": from_unit,
        "converted_unit": to_unit,
        "formula": ""
    }

    # 먼저 % (w/w)로 통일
    intermediate = value
    from_formula = ""

    # 1단계: 원래 단위 → % (w/w)
    if from_unit == "% (w/w)":
        intermediate = value
    elif from_unit == "% (w/v)":
        if solution_density is None:
            raise ValueError("Solution density required for % (w/v) conversion")
        intermediate = conv.percent_wv_to_ww(value, solution_density)
        from_formula = f"{value} / {solution_density}"
    elif from_unit == "% (v/v)":
        if solute_density is None or solution_density is None:
            raise ValueError("Both densities required for % (v/v) conversion")
        intermediate = conv.percent_vv_to_ww(value, solute_density, solution_density)
        from_formula = f"{value} × ({solute_density} / {solution_density})"
    elif from_unit == "ppm":
        intermediate = conv.ppm_to_percent(value)
        from_formula = f"{value} / 10000"
    elif from_unit == "ppb":
        intermediate = conv.ppm_to_percent(conv.ppb_to_ppm(value))
        from_formula = f"{value} / 10000000"
    elif from_unit == "mg/g":
        intermediate = conv.mg_g_to_percent(value)
        from_formula = f"{value} / 10"
    elif from_unit == "mg/kg":
        intermediate = value / 10000
        from_formula = f"{value} / 10000"
    elif from_unit == "mg/mL" or from_unit == "g/L":
        # mg/mL = g/L, w/v 기준
        intermediate = value / 10  # to % (w/v) first
        if solution_density:
            intermediate = intermediate / solution_density  # to % (w/w)
        from_formula = f"{value} / 10" + (f" / {solution_density}" if solution_density else " [w/v]")
    elif from_unit in ["M", "mM", "μM"]:
        if molecular_weight is None:
            raise ValueError("Molecular weight required for molar conversion")
        # 먼저 M으로 통일
        molar = value
        if from_unit == "mM":
            molar = value / 1000
        elif from_unit == "μM":
            molar = value / 1000000
        # M → g/L → % (w/v)
        g_l = molar * molecular_weight
        intermediate = g_l / 10  # to % (w/v)
        if solution_density:
            intermediate = intermediate / solution_density  # to % (w/w)
        from_formula = f"{molar} M × {molecular_weight} g/mol"
    else:
        raise ValueError(f"Unknown from_unit: {from_unit}")

    # 2단계: % (w/w) → 목표 단위
    converted = intermediate
    to_formula = ""

    if to_unit == "% (w/w)":
        converted = intermediate
    elif to_unit == "% (w/v)":
        if solution_density is None:
            raise ValueError("Solution density required for % (w/v) conversion")
        converted = conv.percent_ww_to_wv(intermediate, solution_density)
        to_formula = f"× {solution_density}"
    elif to_unit == "% (v/v)":
        if solute_density is None or solution_density is None:
            raise ValueError("Both densities required for % (v/v) conversion")
        converted = conv.percent_ww_to_vv(intermediate, solute_density, solution_density)
        to_formula = f"× ({solution_density} / {solute_density})"
    elif to_unit == "ppm":
        converted = conv.percent_to_ppm(intermediate)
        to_formula = "× 10000"
    elif to_unit == "ppb":
        converted = conv.ppm_to_ppb(conv.percent_to_ppm(intermediate))
        to_formula = "× 10000000"
    elif to_unit == "mg/g":
        converted = conv.percent_to_mg_g(intermediate)
        to_formula = "× 10"
    elif to_unit == "mg/kg":
        converted = intermediate * 10000
        to_formula = "× 10000"
    elif to_unit == "mg/mL" or to_unit == "g/L":
        # % (w/w) → % (w/v) → mg/mL
        wv = intermediate
        if solution_density:
            wv = intermediate * solution_density
        converted = wv * 10
        to_formula = f"× {solution_density if solution_density else 1} × 10"
    elif to_unit in ["M", "mM", "μM"]:
        if molecular_weight is None:
            raise ValueError("Molecular weight required for molar conversion")
        # % (w/w) → % (w/v) → g/L → M
        wv = intermediate
        if solution_density:
            wv = intermediate * solution_density
        g_l = wv * 10
        molar = g_l / molecular_weight
        if to_unit == "mM":
            converted = molar * 1000
        elif to_unit == "μM":
            converted = molar * 1000000
        else:
            converted = molar
        to_formula = f"→ {g_l:.4f} g/L ÷ {molecular_weight} g/mol"
    else:
        raise ValueError(f"Unknown to_unit: {to_unit}")

    result["converted_value"] = round(converted, 6)
    result["formula"] = f"{from_formula} → {to_formula}".strip(" →")

    return result


# 사용 예시
if __name__ == "__main__":
    print("=" * 60)
    print("Concentration Converter - Example Usage")
    print("=" * 60)

    conv = ConcentrationConverter()
    dilute = DilutionCalculator()
    active = ActiveConcentrationCalculator()

    # 1. 기본 퍼센트 ↔ ppm 변환
    print("\n1. 퍼센트 ↔ ppm 변환")
    print("-" * 40)

    percent = 5.0
    ppm = conv.percent_to_ppm(percent)
    print(f"{percent}% = {ppm} ppm")

    ppm_value = 100
    percent_from_ppm = conv.ppm_to_percent(ppm_value)
    print(f"{ppm_value} ppm = {percent_from_ppm}%")

    # 2. % (w/w) ↔ % (w/v) 변환
    print("\n2. % (w/w) ↔ % (w/v) 변환")
    print("-" * 40)

    percent_ww = 5.0
    density = 1.05  # g/mL
    percent_wv = conv.percent_ww_to_wv(percent_ww, density)
    print(f"{percent_ww}% (w/w), 밀도 {density} g/mL")
    print(f"→ {percent_wv}% (w/v)")

    # 3. 몰농도 변환
    print("\n3. 몰농도 변환")
    print("-" * 40)

    percent_wv = 5.0
    mw_niacinamide = MOLECULAR_WEIGHTS["niacinamide"]
    molar = conv.percent_wv_to_molar(percent_wv, mw_niacinamide)
    print(f"나이아신아마이드 (MW = {mw_niacinamide} g/mol)")
    print(f"{percent_wv}% (w/v) = {molar:.4f} M = {molar * 1000:.2f} mM")

    # 4. 희석 계산
    print("\n4. 희석 계산")
    print("-" * 40)

    c_stock = 10.0  # % 원액
    c_final = 2.0   # % 목표 농도
    v_final = 500   # mL 목표 부피

    v_stock = dilute.calculate_stock_volume(c_final, v_final, c_stock)
    df = dilute.calculate_dilution_factor(c_stock, c_final)

    print(f"원액: {c_stock}%")
    print(f"목표: {c_final}%, {v_final} mL")
    print(f"필요 원액: {v_stock} mL")
    print(f"희석 배수: {df}배")

    # 5. 연속 희석
    print("\n5. 연속 희석 (1:10, 3회)")
    print("-" * 40)

    serial = dilute.serial_dilution(c_initial=10.0, dilution_factor=10, n_dilutions=3)
    for i, conc in enumerate(serial):
        print(f"Step {i}: {conc}%")

    # 6. 활성 농도 계산
    print("\n6. 활성 농도 계산")
    print("-" * 40)

    # 센텔라 추출물: 아시아티코사이드 40% 함유
    formula_pct = 0.5  # 배합률 0.5%
    active_ratio = 0.40  # 40% 아시아티코사이드

    active_conc = active.calculate_active_concentration(formula_pct, active_ratio)
    print(f"센텔라 추출물 배합률: {formula_pct}%")
    print(f"아시아티코사이드 함량: {active_ratio * 100}%")
    print(f"실제 아시아티코사이드 농도: {active_conc}% = {active_conc * 10000} ppm")

    # 7. 범용 변환 함수
    print("\n7. 범용 변환 함수 사용 예")
    print("-" * 40)

    # ppm → % 변환
    result = convert_concentration(
        value=20000,
        from_unit="ppm",
        to_unit="% (w/w)"
    )
    print(f"20,000 ppm → {result['converted_value']}%")

    # % → mM 변환 (나이아신아마이드)
    result = convert_concentration(
        value=5.0,
        from_unit="% (w/v)",
        to_unit="mM",
        molecular_weight=122.12
    )
    print(f"나이아신아마이드 5% (w/v) → {result['converted_value']:.2f} mM")

    # mg/g → ppm 변환
    result = convert_concentration(
        value=2.5,
        from_unit="mg/g",
        to_unit="ppm"
    )
    print(f"2.5 mg/g → {result['converted_value']} ppm")

    print("\n" + "=" * 60)
    print("계산 완료")
    print("=" * 60)
