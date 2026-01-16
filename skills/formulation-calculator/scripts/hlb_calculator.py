#!/usr/bin/env python3
"""
HLB Calculator for Cosmetic Formulation

화장품 유화 시스템 설계를 위한 HLB 계산 도구
- Required HLB 계산 (오일 혼합물)
- 유화제 블렌딩 최적화
- HLB 기반 유화제 선택

Author: EVAS Cosmetic
License: MIT
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import math


@dataclass
class Oil:
    """오일 성분 데이터 클래스"""
    name: str
    percent: float
    required_hlb: float
    category: Optional[str] = None


@dataclass
class Emulsifier:
    """유화제 데이터 클래스"""
    name: str
    inci: str
    hlb: float
    type: str  # "W/O", "O/W", "solubilizer"
    notes: Optional[str] = None


class OilDatabase:
    """화장품용 오일 Required HLB 데이터베이스"""

    # 오일별 Required HLB 값
    OILS = {
        # 탄화수소
        "mineral_oil_light": {"required_hlb": 11.0, "category": "hydrocarbon"},
        "mineral_oil_heavy": {"required_hlb": 10.5, "category": "hydrocarbon"},
        "petrolatum": {"required_hlb": 7.5, "category": "hydrocarbon"},
        "microcrystalline_wax": {"required_hlb": 9.5, "category": "hydrocarbon"},
        "paraffin_wax": {"required_hlb": 10.0, "category": "hydrocarbon"},
        "squalane": {"required_hlb": 10.5, "category": "hydrocarbon"},
        "squalene": {"required_hlb": 11.0, "category": "hydrocarbon"},

        # 식물성 오일
        "jojoba_oil": {"required_hlb": 6.5, "category": "vegetable"},
        "argan_oil": {"required_hlb": 7.0, "category": "vegetable"},
        "sweet_almond_oil": {"required_hlb": 7.0, "category": "vegetable"},
        "avocado_oil": {"required_hlb": 7.0, "category": "vegetable"},
        "olive_oil": {"required_hlb": 7.0, "category": "vegetable"},
        "coconut_oil": {"required_hlb": 8.0, "category": "vegetable"},
        "sunflower_oil": {"required_hlb": 7.0, "category": "vegetable"},
        "grapeseed_oil": {"required_hlb": 7.0, "category": "vegetable"},
        "rosehip_oil": {"required_hlb": 7.5, "category": "vegetable"},
        "castor_oil": {"required_hlb": 14.0, "category": "vegetable"},
        "hemp_seed_oil": {"required_hlb": 7.0, "category": "vegetable"},
        "macadamia_oil": {"required_hlb": 6.5, "category": "vegetable"},
        "shea_butter": {"required_hlb": 8.0, "category": "vegetable"},
        "cocoa_butter": {"required_hlb": 6.0, "category": "vegetable"},

        # 에스테르류
        "isopropyl_myristate": {"required_hlb": 11.5, "category": "ester"},
        "isopropyl_palmitate": {"required_hlb": 11.5, "category": "ester"},
        "cetyl_palmitate": {"required_hlb": 10.0, "category": "ester"},
        "cetyl_esters": {"required_hlb": 10.0, "category": "ester"},
        "decyl_oleate": {"required_hlb": 6.0, "category": "ester"},
        "diisopropyl_adipate": {"required_hlb": 8.0, "category": "ester"},
        "ethylhexyl_palmitate": {"required_hlb": 10.5, "category": "ester"},
        "cct_oil": {"required_hlb": 5.0, "category": "ester"},  # Caprylic/Capric Triglyceride
        "c12_15_alkyl_benzoate": {"required_hlb": 13.0, "category": "ester"},

        # 지방 알코올
        "cetyl_alcohol": {"required_hlb": 15.5, "category": "fatty_alcohol"},
        "stearyl_alcohol": {"required_hlb": 15.5, "category": "fatty_alcohol"},
        "cetearyl_alcohol": {"required_hlb": 15.5, "category": "fatty_alcohol"},
        "behenyl_alcohol": {"required_hlb": 15.0, "category": "fatty_alcohol"},

        # 실리콘
        "dimethicone_100": {"required_hlb": 5.0, "category": "silicone"},
        "dimethicone_350": {"required_hlb": 7.5, "category": "silicone"},
        "cyclomethicone": {"required_hlb": 4.5, "category": "silicone"},
        "cyclopentasiloxane": {"required_hlb": 4.5, "category": "silicone"},
        "dimethiconol": {"required_hlb": 9.0, "category": "silicone"},
        "phenyl_trimethicone": {"required_hlb": 7.0, "category": "silicone"},
    }

    @classmethod
    def get_required_hlb(cls, oil_name: str) -> Optional[float]:
        """오일의 Required HLB 조회"""
        oil_key = oil_name.lower().replace(" ", "_").replace("-", "_")
        oil_data = cls.OILS.get(oil_key)
        if oil_data:
            return oil_data["required_hlb"]
        return None

    @classmethod
    def list_oils_by_category(cls, category: str) -> List[Dict]:
        """카테고리별 오일 목록"""
        return [
            {"name": name, **data}
            for name, data in cls.OILS.items()
            if data["category"] == category
        ]

    @classmethod
    def search_oil(cls, query: str) -> List[Dict]:
        """오일 검색"""
        query = query.lower()
        results = []
        for name, data in cls.OILS.items():
            if query in name:
                results.append({"name": name, **data})
        return results


class EmulsifierDatabase:
    """유화제 HLB 데이터베이스"""

    EMULSIFIERS = {
        # Span 시리즈 (소르비탄 에스테르)
        "span_20": {"inci": "Sorbitan Laurate", "hlb": 8.6, "type": "O/W_aux"},
        "span_40": {"inci": "Sorbitan Palmitate", "hlb": 6.7, "type": "W/O"},
        "span_60": {"inci": "Sorbitan Stearate", "hlb": 4.7, "type": "W/O"},
        "span_65": {"inci": "Sorbitan Tristearate", "hlb": 2.1, "type": "W/O"},
        "span_80": {"inci": "Sorbitan Oleate", "hlb": 4.3, "type": "W/O"},
        "span_85": {"inci": "Sorbitan Trioleate", "hlb": 1.8, "type": "W/O"},

        # Tween 시리즈 (폴리소르베이트)
        "tween_20": {"inci": "Polysorbate 20", "hlb": 16.7, "type": "solubilizer"},
        "tween_40": {"inci": "Polysorbate 40", "hlb": 15.6, "type": "O/W"},
        "tween_60": {"inci": "Polysorbate 60", "hlb": 14.9, "type": "O/W"},
        "tween_65": {"inci": "Polysorbate 65", "hlb": 10.5, "type": "O/W"},
        "tween_80": {"inci": "Polysorbate 80", "hlb": 15.0, "type": "O/W"},
        "tween_85": {"inci": "Polysorbate 85", "hlb": 11.0, "type": "O/W"},

        # 기타 비이온 유화제
        "glyceryl_stearate": {"inci": "Glyceryl Stearate", "hlb": 3.8, "type": "W/O_aux"},
        "glyceryl_stearate_se": {"inci": "Glyceryl Stearate SE", "hlb": 5.8, "type": "O/W"},
        "ceteareth_20": {"inci": "Ceteareth-20", "hlb": 15.2, "type": "O/W"},
        "ceteareth_6": {"inci": "Ceteareth-6", "hlb": 9.6, "type": "O/W"},
        "steareth_2": {"inci": "Steareth-2", "hlb": 4.9, "type": "W/O"},
        "steareth_20": {"inci": "Steareth-20", "hlb": 15.3, "type": "O/W"},
        "peg_100_stearate": {"inci": "PEG-100 Stearate", "hlb": 18.8, "type": "solubilizer"},
        "emulsifying_wax_nf": {"inci": "Cetearyl Alcohol and Polysorbate 60", "hlb": 8.5, "type": "O/W"},
    }

    @classmethod
    def get_emulsifier(cls, name: str) -> Optional[Dict]:
        """유화제 정보 조회"""
        key = name.lower().replace(" ", "_").replace("-", "_")
        return cls.EMULSIFIERS.get(key)

    @classmethod
    def get_by_hlb_range(cls, min_hlb: float, max_hlb: float) -> List[Dict]:
        """HLB 범위로 유화제 검색"""
        return [
            {"name": name, **data}
            for name, data in cls.EMULSIFIERS.items()
            if min_hlb <= data["hlb"] <= max_hlb
        ]

    @classmethod
    def get_by_type(cls, emulsifier_type: str) -> List[Dict]:
        """타입별 유화제 검색"""
        return [
            {"name": name, **data}
            for name, data in cls.EMULSIFIERS.items()
            if data["type"] == emulsifier_type
        ]


def calculate_required_hlb(oils: List[Dict]) -> Dict:
    """
    오일 혼합물의 Required HLB 계산

    Args:
        oils: 오일 리스트
            [{"name": "mineral_oil", "percent": 10.0, "required_hlb": 10.5}, ...]
            required_hlb가 없으면 데이터베이스에서 조회

    Returns:
        {
            "required_hlb": float,
            "oil_phase_total": float,
            "breakdown": [{"name": str, "percent": float, "required_hlb": float, "contribution": float}]
        }
    """
    total_weight = 0
    weighted_hlb = 0
    breakdown = []

    for oil in oils:
        name = oil.get("name", "Unknown")
        percent = oil.get("percent", 0)

        # Required HLB 결정
        req_hlb = oil.get("required_hlb")
        if req_hlb is None:
            req_hlb = OilDatabase.get_required_hlb(name)
            if req_hlb is None:
                raise ValueError(f"Unknown oil or missing required_hlb: {name}")

        contribution = percent * req_hlb
        total_weight += percent
        weighted_hlb += contribution

        breakdown.append({
            "name": name,
            "percent": percent,
            "required_hlb": req_hlb,
            "contribution": round(contribution, 2)
        })

    if total_weight == 0:
        raise ValueError("Total oil weight cannot be zero")

    required_hlb = weighted_hlb / total_weight

    return {
        "required_hlb": round(required_hlb, 2),
        "oil_phase_total": round(total_weight, 2),
        "breakdown": breakdown
    }


def blend_emulsifiers(target_hlb: float, emulsifiers: List[Dict]) -> Dict:
    """
    목표 HLB를 달성하기 위한 유화제 블렌딩 비율 계산

    Args:
        target_hlb: 목표 HLB 값
        emulsifiers: 유화제 리스트 (2개 필요)
            [{"name": "Tween 60", "hlb": 14.9}, {"name": "Span 60", "hlb": 4.7}]

    Returns:
        {
            "target_hlb": float,
            "blend": [{"name": str, "hlb": float, "ratio": float, "percent": float}],
            "achievable": bool,
            "note": str
        }
    """
    if len(emulsifiers) != 2:
        raise ValueError("Exactly 2 emulsifiers required for blending calculation")

    e1 = emulsifiers[0]
    e2 = emulsifiers[1]

    hlb1 = e1.get("hlb")
    hlb2 = e2.get("hlb")

    if hlb1 is None or hlb2 is None:
        raise ValueError("Both emulsifiers must have HLB values")

    # 정렬 (hlb1 < hlb2)
    if hlb1 > hlb2:
        e1, e2 = e2, e1
        hlb1, hlb2 = hlb2, hlb1

    # 범위 확인
    if target_hlb < hlb1 or target_hlb > hlb2:
        return {
            "target_hlb": target_hlb,
            "blend": [],
            "achievable": False,
            "note": f"Target HLB ({target_hlb}) is outside achievable range ({hlb1}-{hlb2})"
        }

    # 블렌딩 비율 계산
    # target = r2 * hlb2 + (1-r2) * hlb1
    # target = r2 * hlb2 + hlb1 - r2 * hlb1
    # target - hlb1 = r2 * (hlb2 - hlb1)
    # r2 = (target - hlb1) / (hlb2 - hlb1)

    ratio_high = (target_hlb - hlb1) / (hlb2 - hlb1)
    ratio_low = 1 - ratio_high

    return {
        "target_hlb": target_hlb,
        "blend": [
            {
                "name": e1.get("name", "Low HLB"),
                "hlb": hlb1,
                "ratio": round(ratio_low, 4),
                "percent": round(ratio_low * 100, 1)
            },
            {
                "name": e2.get("name", "High HLB"),
                "hlb": hlb2,
                "ratio": round(ratio_high, 4),
                "percent": round(ratio_high * 100, 1)
            }
        ],
        "achievable": True,
        "verification_hlb": round(ratio_low * hlb1 + ratio_high * hlb2, 2),
        "note": "Blend ratios calculated. Verify HLB matches target."
    }


def calculate_hlb_griffin(hydrophilic_mw: float, total_mw: float) -> float:
    """
    Griffin 방법으로 HLB 계산 (비이온 계면활성제)

    Args:
        hydrophilic_mw: 친수성 부분의 분자량
        total_mw: 전체 분자량

    Returns:
        HLB 값
    """
    if total_mw <= 0:
        raise ValueError("Total molecular weight must be positive")

    hlb = 20 * (hydrophilic_mw / total_mw)
    return round(hlb, 1)


def calculate_hlb_davies(hydrophilic_groups: List[Tuple[str, int]],
                         lipophilic_carbons: int) -> float:
    """
    Davies 방법으로 HLB 계산 (기능기 기반)

    Args:
        hydrophilic_groups: 친수성 기능기 리스트 [(기능기명, 개수), ...]
        lipophilic_carbons: 탄소 원자 수 (CH3, CH2, CH 합계)

    Returns:
        HLB 값
    """
    # Davies 친수성 기 값
    HYDROPHILIC_VALUES = {
        "SO4Na": 38.7,
        "COOK": 21.1,
        "COONa": 19.1,
        "N_tertiary": 9.4,
        "ester_sorbitan": 6.8,
        "ester_free": 2.4,
        "COOH": 2.1,
        "OH_free": 1.9,
        "O_ether": 1.3,
        "OH_sorbitan": 0.5
    }

    # 친수성 합계
    hydrophilic_sum = 0
    for group, count in hydrophilic_groups:
        if group in HYDROPHILIC_VALUES:
            hydrophilic_sum += HYDROPHILIC_VALUES[group] * count
        else:
            print(f"Warning: Unknown group '{group}', skipping")

    # 친유성 합계 (탄소 1개당 -0.475)
    lipophilic_sum = lipophilic_carbons * 0.475

    # HLB 계산
    hlb = 7 + hydrophilic_sum - lipophilic_sum

    return round(hlb, 1)


def suggest_emulsifier_pair(target_hlb: float, emulsion_type: str = "O/W") -> Dict:
    """
    목표 HLB에 적합한 유화제 쌍 추천

    Args:
        target_hlb: 목표 HLB
        emulsion_type: "O/W" 또는 "W/O"

    Returns:
        추천 유화제 쌍과 블렌딩 비율
    """
    db = EmulsifierDatabase

    if emulsion_type == "O/W":
        # O/W: 높은 HLB 유화제 + 낮은 HLB 보조 유화제
        high_hlb_emulsifiers = db.get_by_hlb_range(12.0, 17.0)
        low_hlb_emulsifiers = db.get_by_hlb_range(3.0, 8.0)
    else:
        # W/O: 낮은 HLB 유화제
        high_hlb_emulsifiers = db.get_by_hlb_range(6.0, 10.0)
        low_hlb_emulsifiers = db.get_by_hlb_range(1.0, 5.0)

    recommendations = []

    for high_e in high_hlb_emulsifiers:
        for low_e in low_hlb_emulsifiers:
            if low_e["hlb"] < target_hlb < high_e["hlb"]:
                blend = blend_emulsifiers(
                    target_hlb,
                    [
                        {"name": low_e["name"], "hlb": low_e["hlb"]},
                        {"name": high_e["name"], "hlb": high_e["hlb"]}
                    ]
                )
                if blend["achievable"]:
                    recommendations.append({
                        "pair": [low_e["name"], high_e["name"]],
                        "blend": blend["blend"],
                        "hlb_range": f"{low_e['hlb']}-{high_e['hlb']}"
                    })

    # 상위 3개 추천
    return {
        "target_hlb": target_hlb,
        "emulsion_type": emulsion_type,
        "recommendations": recommendations[:3]
    }


def calculate_emulsifier_amount(oil_phase_percent: float,
                                emulsifier_ratio: float = 0.20) -> Dict:
    """
    유화제 사용량 계산

    Args:
        oil_phase_percent: 오일상 비율 (%)
        emulsifier_ratio: 유화제 비율 (기본 20%)

    Returns:
        유화제 사용량 권장
    """
    emulsifier_percent = oil_phase_percent * emulsifier_ratio

    return {
        "oil_phase_percent": oil_phase_percent,
        "emulsifier_ratio": emulsifier_ratio,
        "emulsifier_percent": round(emulsifier_percent, 2),
        "recommended_range": f"{round(oil_phase_percent * 0.15, 2)}-{round(oil_phase_percent * 0.25, 2)}%",
        "note": "Typical range: 15-25% of oil phase"
    }


# 사용 예시
if __name__ == "__main__":
    print("=" * 60)
    print("HLB Calculator - Example Usage")
    print("=" * 60)

    # 1. Required HLB 계산
    print("\n1. Required HLB Calculation")
    print("-" * 40)

    oils = [
        {"name": "mineral_oil_heavy", "percent": 8.0},
        {"name": "jojoba_oil", "percent": 3.0},
        {"name": "cetyl_alcohol", "percent": 2.0}
    ]

    result = calculate_required_hlb(oils)
    print(f"Oil Phase Total: {result['oil_phase_total']}%")
    print(f"Required HLB: {result['required_hlb']}")
    print("\nBreakdown:")
    for item in result["breakdown"]:
        print(f"  - {item['name']}: {item['percent']}% (Req HLB: {item['required_hlb']})")

    # 2. 유화제 블렌딩
    print("\n2. Emulsifier Blending")
    print("-" * 40)

    emulsifiers = [
        {"name": "Span 60", "hlb": 4.7},
        {"name": "Tween 60", "hlb": 14.9}
    ]

    blend = blend_emulsifiers(target_hlb=result["required_hlb"], emulsifiers=emulsifiers)
    print(f"Target HLB: {blend['target_hlb']}")
    print(f"Achievable: {blend['achievable']}")
    if blend["achievable"]:
        for e in blend["blend"]:
            print(f"  - {e['name']} (HLB {e['hlb']}): {e['percent']}%")
        print(f"Verification HLB: {blend['verification_hlb']}")

    # 3. Griffin 방법
    print("\n3. Griffin Method - Tween 80")
    print("-" * 40)
    hlb_griffin = calculate_hlb_griffin(hydrophilic_mw=880, total_mw=1310)
    print(f"Calculated HLB: {hlb_griffin} (Reference: 15.0)")

    # 4. 유화제 사용량
    print("\n4. Emulsifier Amount")
    print("-" * 40)
    amount = calculate_emulsifier_amount(oil_phase_percent=13.0)
    print(f"Oil Phase: {amount['oil_phase_percent']}%")
    print(f"Recommended Emulsifier: {amount['emulsifier_percent']}%")
    print(f"Range: {amount['recommended_range']}")
