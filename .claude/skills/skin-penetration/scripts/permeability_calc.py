#!/usr/bin/env python3
"""
Skin Permeability Calculation Tools

화장품 활성 성분의 피부 투과도 예측 및 분석을 위한 도구 모음.
Potts-Guy 모델, Lipinski 규칙 기반 평가, 플럭스 계산 등을 제공합니다.

Usage:
    from permeability_calc import (
        calculate_kp_potts_guy,
        check_lipinski_rules,
        estimate_flux,
        recommend_delivery_system,
        MolecularProperties,
        COMPOUND_DATABASE
    )
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum
import math


class PermeabilityClass(Enum):
    """피부 투과성 등급 분류"""
    VERY_HIGH = "매우 높음"      # log Kp > -4
    HIGH = "높음"               # -5 < log Kp <= -4
    MODERATE = "중간"           # -6 < log Kp <= -5
    LOW = "낮음"                # -7 < log Kp <= -6
    VERY_LOW = "매우 낮음"       # log Kp <= -7


class DeliverySystem(Enum):
    """전달 시스템 유형"""
    CONVENTIONAL = "일반 제형"
    PENETRATION_ENHANCER = "투과 촉진제"
    LIPOSOME = "리포좀"
    NANOEMULSION = "나노에멀전"
    SLN_NLC = "고체 지질 나노입자/NLC"
    MICRONEEDLE = "마이크로니들"
    IONTOPHORESIS = "이온토포레시스"
    PRODRUG = "프로드러그"


@dataclass
class MolecularProperties:
    """분자 특성 데이터 클래스

    Attributes:
        name: 성분명
        name_kr: 한국어 성분명
        cas_number: CAS 번호 (선택)
        mw: 분자량 (Da)
        log_p: 옥탄올/물 분배계수
        hbd: 수소결합 공여체 수
        hba: 수소결합 수용체 수
        psa: 극성 표면적 (Å²)
        melting_point: 융점 (°C, 선택)
        pka: pKa 값 (선택)
        solubility_water: 수용해도 (mg/mL, 선택)
    """
    name: str
    name_kr: str
    mw: float
    log_p: float
    hbd: int = 0
    hba: int = 0
    psa: float = 0.0
    cas_number: Optional[str] = None
    melting_point: Optional[float] = None
    pka: Optional[float] = None
    solubility_water: Optional[float] = None


# =============================================================================
# 화장품 활성 성분 데이터베이스
# =============================================================================

COMPOUND_DATABASE: Dict[str, MolecularProperties] = {
    # 미백 성분
    "niacinamide": MolecularProperties(
        name="Niacinamide",
        name_kr="나이아신아마이드",
        cas_number="98-92-0",
        mw=122.12,
        log_p=-0.37,
        hbd=1,
        hba=3,
        psa=56.0,
        melting_point=130,
        solubility_water=500000
    ),
    "arbutin": MolecularProperties(
        name="Alpha-Arbutin",
        name_kr="알파-아르부틴",
        cas_number="84380-01-8",
        mw=272.25,
        log_p=-1.49,
        hbd=4,
        hba=7,
        psa=119.0,
        melting_point=200,
        solubility_water=50000
    ),
    "kojic_acid": MolecularProperties(
        name="Kojic Acid",
        name_kr="코직산",
        cas_number="501-30-4",
        mw=142.11,
        log_p=-0.65,
        hbd=2,
        hba=4,
        psa=70.7,
        melting_point=152
    ),
    "tranexamic_acid": MolecularProperties(
        name="Tranexamic Acid",
        name_kr="트라넥삼산",
        cas_number="1197-18-8",
        mw=157.21,
        log_p=-2.35,
        hbd=3,
        hba=4,
        psa=89.0,
        melting_point=300
    ),
    "hydroquinone": MolecularProperties(
        name="Hydroquinone",
        name_kr="하이드로퀴논",
        cas_number="123-31-9",
        mw=110.11,
        log_p=0.59,
        hbd=2,
        hba=2,
        psa=40.5,
        melting_point=172
    ),

    # 항산화 성분
    "ascorbic_acid": MolecularProperties(
        name="Ascorbic Acid",
        name_kr="아스코르빈산",
        cas_number="50-81-7",
        mw=176.12,
        log_p=-1.85,
        hbd=4,
        hba=6,
        psa=107.0,
        melting_point=190,
        pka=4.2
    ),
    "ascorbyl_palmitate": MolecularProperties(
        name="Ascorbyl Palmitate",
        name_kr="아스코빌팔미테이트",
        cas_number="137-66-6",
        mw=414.53,
        log_p=8.9,
        hbd=3,
        hba=7,
        psa=107.0
    ),
    "tocopherol": MolecularProperties(
        name="Tocopherol (Vitamin E)",
        name_kr="토코페롤",
        cas_number="59-02-9",
        mw=430.71,
        log_p=12.2,
        hbd=1,
        hba=2,
        psa=29.5,
        melting_point=3
    ),
    "resveratrol": MolecularProperties(
        name="Resveratrol",
        name_kr="레스베라트롤",
        cas_number="501-36-0",
        mw=228.24,
        log_p=3.1,
        hbd=3,
        hba=3,
        psa=60.7,
        melting_point=254
    ),
    "ferulic_acid": MolecularProperties(
        name="Ferulic Acid",
        name_kr="페룰릭산",
        cas_number="1135-24-6",
        mw=194.18,
        log_p=1.51,
        hbd=2,
        hba=4,
        psa=66.8,
        melting_point=174
    ),

    # 레티노이드
    "retinol": MolecularProperties(
        name="Retinol",
        name_kr="레티놀",
        cas_number="68-26-8",
        mw=286.45,
        log_p=5.68,
        hbd=1,
        hba=1,
        psa=20.2,
        melting_point=63
    ),
    "tretinoin": MolecularProperties(
        name="Tretinoin (Retinoic Acid)",
        name_kr="트레티노인",
        cas_number="302-79-4",
        mw=300.44,
        log_p=6.3,
        hbd=1,
        hba=2,
        psa=37.3,
        melting_point=180
    ),
    "retinaldehyde": MolecularProperties(
        name="Retinaldehyde",
        name_kr="레티날데히드",
        cas_number="116-31-4",
        mw=284.44,
        log_p=5.48,
        hbd=0,
        hba=1,
        psa=17.1
    ),
    "retinyl_palmitate": MolecularProperties(
        name="Retinyl Palmitate",
        name_kr="레티닐팔미테이트",
        cas_number="79-81-2",
        mw=524.86,
        log_p=12.3,
        hbd=0,
        hba=2,
        psa=26.3,
        melting_point=28
    ),

    # 각질 관리
    "salicylic_acid": MolecularProperties(
        name="Salicylic Acid",
        name_kr="살리실산",
        cas_number="69-72-7",
        mw=138.12,
        log_p=2.26,
        hbd=2,
        hba=3,
        psa=57.5,
        melting_point=159,
        pka=2.97
    ),
    "glycolic_acid": MolecularProperties(
        name="Glycolic Acid",
        name_kr="글리콜산",
        cas_number="79-14-1",
        mw=76.05,
        log_p=-1.11,
        hbd=2,
        hba=3,
        psa=57.5,
        melting_point=80,
        pka=3.83
    ),
    "lactic_acid": MolecularProperties(
        name="Lactic Acid",
        name_kr="젖산",
        cas_number="50-21-5",
        mw=90.08,
        log_p=-0.72,
        hbd=2,
        hba=3,
        psa=57.5,
        melting_point=53,
        pka=3.86
    ),
    "azelaic_acid": MolecularProperties(
        name="Azelaic Acid",
        name_kr="아젤라산",
        cas_number="123-99-9",
        mw=188.22,
        log_p=1.57,
        hbd=2,
        hba=4,
        psa=74.6,
        melting_point=107
    ),

    # 보습 성분
    "hyaluronic_acid_low": MolecularProperties(
        name="Hyaluronic Acid (Low MW)",
        name_kr="저분자 히알루론산",
        mw=50000,  # 50 kDa
        log_p=-10.0,  # 추정값
        hbd=100,
        hba=200,
        psa=5000
    ),
    "urea": MolecularProperties(
        name="Urea",
        name_kr="요소",
        cas_number="57-13-6",
        mw=60.06,
        log_p=-2.11,
        hbd=2,
        hba=2,
        psa=69.1,
        melting_point=133
    ),
    "panthenol": MolecularProperties(
        name="Panthenol",
        name_kr="판테놀",
        cas_number="81-13-0",
        mw=205.25,
        log_p=-0.99,
        hbd=4,
        hba=5,
        psa=96.7,
        melting_point=68
    ),

    # 펩타이드
    "palmitoyl_tripeptide_1": MolecularProperties(
        name="Palmitoyl Tripeptide-1",
        name_kr="팔미토일트리펩타이드-1",
        mw=578.77,
        log_p=2.5,  # 추정값
        hbd=5,
        hba=8
    ),
    "acetyl_hexapeptide_8": MolecularProperties(
        name="Acetyl Hexapeptide-8",
        name_kr="아세틸헥사펩타이드-8",
        mw=888.97,
        log_p=-3.5,  # 추정값
        hbd=10,
        hba=15
    ),

    # 기타
    "caffeine": MolecularProperties(
        name="Caffeine",
        name_kr="카페인",
        cas_number="58-08-2",
        mw=194.19,
        log_p=-0.07,
        hbd=0,
        hba=6,
        psa=58.4,
        melting_point=238
    ),
    "centella_asiatica": MolecularProperties(
        name="Asiaticoside",
        name_kr="아시아티코사이드",
        cas_number="16830-15-2",
        mw=959.12,
        log_p=-2.1,
        hbd=12,
        hba=21,
        psa=309.5
    ),
    "bakuchiol": MolecularProperties(
        name="Bakuchiol",
        name_kr="바쿠치올",
        cas_number="10309-37-2",
        mw=256.38,
        log_p=4.76,
        hbd=1,
        hba=1,
        psa=29.5
    ),
}


# =============================================================================
# Core Functions
# =============================================================================

def calculate_kp_potts_guy(log_p: float, mw: float) -> float:
    """
    Potts-Guy 모델을 사용하여 피부 투과 계수(Kp)를 계산합니다.

    공식: log Kp = 0.71 × log P - 0.0061 × MW - 6.3

    Args:
        log_p: 옥탄올/물 분배계수 (log P)
        mw: 분자량 (Da)

    Returns:
        투과 계수 Kp (cm/h)

    Examples:
        >>> kp = calculate_kp_potts_guy(log_p=-0.37, mw=122)  # 나이아신아마이드
        >>> print(f"Kp = {kp:.2e} cm/h")  # Kp = 5.01e-08 cm/h
    """
    log_kp = 0.71 * log_p - 0.0061 * mw - 6.3
    kp = 10 ** log_kp
    return kp


def calculate_log_kp(log_p: float, mw: float) -> float:
    """
    Potts-Guy 모델을 사용하여 log Kp를 계산합니다.

    Args:
        log_p: 옥탄올/물 분배계수
        mw: 분자량 (Da)

    Returns:
        log Kp 값
    """
    return 0.71 * log_p - 0.0061 * mw - 6.3


def classify_permeability(log_kp: float) -> PermeabilityClass:
    """
    log Kp 값에 따른 투과성 등급을 분류합니다.

    Args:
        log_kp: log Kp 값

    Returns:
        PermeabilityClass 열거형 값
    """
    if log_kp > -4:
        return PermeabilityClass.VERY_HIGH
    elif log_kp > -5:
        return PermeabilityClass.HIGH
    elif log_kp > -6:
        return PermeabilityClass.MODERATE
    elif log_kp > -7:
        return PermeabilityClass.LOW
    else:
        return PermeabilityClass.VERY_LOW


def check_lipinski_rules(compound: MolecularProperties) -> Dict[str, any]:
    """
    Lipinski's Rule of 5를 피부 투과 관점에서 평가합니다.

    경피 최적 기준:
    - MW < 500 (이상적: < 300)
    - 1 < log P < 3 (이상적: 1.5-2.5)
    - HBD < 3
    - HBA < 5
    - PSA < 60 Å²

    Args:
        compound: 분자 특성 데이터

    Returns:
        평가 결과 딕셔너리:
        - 'passed': 통과 여부
        - 'score': 통과 점수 (0-5)
        - 'violations': 위반 항목 리스트
        - 'ideal': 이상적 조건 충족 여부
        - 'details': 상세 평가 결과
    """
    violations = []
    ideal_conditions = []
    details = {}

    # 1. 분자량 평가
    mw = compound.mw
    if mw <= 300:
        details['mw'] = {'value': mw, 'status': 'ideal', 'message': '이상적 (< 300 Da)'}
        ideal_conditions.append('mw')
    elif mw <= 500:
        details['mw'] = {'value': mw, 'status': 'pass', 'message': '통과 (< 500 Da)'}
    else:
        details['mw'] = {'value': mw, 'status': 'fail', 'message': '위반 (> 500 Da)'}
        violations.append('MW > 500')

    # 2. 친유성 평가
    log_p = compound.log_p
    if 1.5 <= log_p <= 2.5:
        details['log_p'] = {'value': log_p, 'status': 'ideal', 'message': '이상적 (1.5-2.5)'}
        ideal_conditions.append('log_p')
    elif 1 <= log_p <= 3:
        details['log_p'] = {'value': log_p, 'status': 'good', 'message': '양호 (1-3)'}
    elif 0 <= log_p <= 5:
        details['log_p'] = {'value': log_p, 'status': 'pass', 'message': '통과 (0-5)'}
    else:
        if log_p < 0:
            details['log_p'] = {'value': log_p, 'status': 'warning', 'message': '친수성 (< 0)'}
            violations.append('log P < 0 (친수성)')
        else:
            details['log_p'] = {'value': log_p, 'status': 'warning', 'message': '고친유성 (> 5)'}
            violations.append('log P > 5 (고친유성)')

    # 3. 수소결합 공여체 평가
    hbd = compound.hbd
    if hbd <= 3:
        details['hbd'] = {'value': hbd, 'status': 'pass', 'message': '통과 (≤ 3)'}
        if hbd <= 2:
            ideal_conditions.append('hbd')
    else:
        details['hbd'] = {'value': hbd, 'status': 'fail', 'message': '위반 (> 3)'}
        violations.append(f'HBD > 3 ({hbd})')

    # 4. 수소결합 수용체 평가
    hba = compound.hba
    if hba <= 5:
        details['hba'] = {'value': hba, 'status': 'pass', 'message': '통과 (≤ 5)'}
        if hba <= 4:
            ideal_conditions.append('hba')
    else:
        details['hba'] = {'value': hba, 'status': 'fail', 'message': '위반 (> 5)'}
        violations.append(f'HBA > 5 ({hba})')

    # 5. 극성 표면적 평가 (있는 경우)
    psa = compound.psa
    if psa > 0:
        if psa <= 60:
            details['psa'] = {'value': psa, 'status': 'ideal', 'message': '이상적 (< 60 Å²)'}
            ideal_conditions.append('psa')
        elif psa <= 120:
            details['psa'] = {'value': psa, 'status': 'pass', 'message': '통과 (< 120 Å²)'}
        else:
            details['psa'] = {'value': psa, 'status': 'fail', 'message': '위반 (> 120 Å²)'}
            violations.append(f'PSA > 120 ({psa:.1f})')

    # 점수 계산 (5점 만점)
    score = 5 - len(violations)
    if score < 0:
        score = 0

    # 투과 전망 평가
    if len(violations) == 0 and len(ideal_conditions) >= 3:
        outlook = "우수한 피부 투과 예상"
    elif len(violations) <= 1:
        outlook = "양호한 피부 투과 예상"
    elif len(violations) <= 2:
        outlook = "중간 정도의 피부 투과 예상"
    else:
        outlook = "낮은 피부 투과 예상, 전달 시스템 필요"

    return {
        'compound': compound.name,
        'compound_kr': compound.name_kr,
        'passed': len(violations) <= 1,  # 1개 이하 위반 시 통과
        'score': score,
        'violations': violations,
        'violation_count': len(violations),
        'ideal_count': len(ideal_conditions),
        'ideal_conditions': ideal_conditions,
        'details': details,
        'outlook': outlook
    }


def estimate_flux(
    kp: float,
    concentration: float,
    area: float = 1.0,
    time_hours: float = 24.0
) -> Dict[str, float]:
    """
    정상 상태에서의 피부 투과 플럭스를 추정합니다.

    공식: J = Kp × C × A

    Args:
        kp: 투과 계수 (cm/h)
        concentration: 적용 농도 (μg/mL = μg/cm³)
        area: 적용 면적 (cm², 기본값 1)
        time_hours: 적용 시간 (시간, 기본값 24)

    Returns:
        플럭스 정보 딕셔너리:
        - 'flux_per_area': 단위 면적당 플럭스 (μg/cm²/h)
        - 'total_flux': 총 플럭스 (μg/h)
        - 'cumulative_amount': 누적 투과량 (μg)
        - 'cumulative_amount_mg': 누적 투과량 (mg)

    Examples:
        >>> # 나이아신아마이드 5% 세럼
        >>> flux_info = estimate_flux(
        ...     kp=5e-8,
        ...     concentration=50000,  # 5% = 50,000 μg/mL
        ...     area=600,             # 얼굴 면적
        ...     time_hours=24
        ... )
    """
    # 단위 면적당 플럭스 (μg/cm²/h)
    flux_per_area = kp * concentration

    # 총 플럭스 (μg/h)
    total_flux = flux_per_area * area

    # 누적 투과량 (μg)
    cumulative = total_flux * time_hours

    return {
        'flux_per_area': flux_per_area,
        'flux_per_area_unit': 'μg/cm²/h',
        'total_flux': total_flux,
        'total_flux_unit': 'μg/h',
        'cumulative_amount': cumulative,
        'cumulative_amount_mg': cumulative / 1000,
        'cumulative_unit': 'μg',
        'application_area': area,
        'application_time': time_hours
    }


def recommend_delivery_system(compound: MolecularProperties) -> Dict[str, any]:
    """
    화합물 특성에 따른 최적 전달 시스템을 추천합니다.

    Args:
        compound: 분자 특성 데이터

    Returns:
        추천 정보 딕셔너리:
        - 'primary': 주요 추천 시스템
        - 'secondary': 보조 추천 시스템들
        - 'enhancers': 추천 투과 촉진제
        - 'rationale': 추천 근거
        - 'considerations': 고려사항
    """
    mw = compound.mw
    log_p = compound.log_p

    recommendations = {
        'compound': compound.name,
        'compound_kr': compound.name_kr,
        'primary': None,
        'secondary': [],
        'enhancers': [],
        'rationale': [],
        'considerations': []
    }

    # 분자량 기반 분류
    if mw > 1000:
        # 대형 분자 (> 1000 Da)
        recommendations['primary'] = DeliverySystem.MICRONEEDLE
        recommendations['secondary'] = [DeliverySystem.IONTOPHORESIS]
        recommendations['rationale'].append(f"고분자량 ({mw:.0f} Da)으로 일반 투과 불가")
        recommendations['considerations'].append("표면 작용으로 제한될 수 있음")

    elif mw > 500:
        # 중대형 분자 (500-1000 Da)
        recommendations['primary'] = DeliverySystem.LIPOSOME
        recommendations['secondary'] = [DeliverySystem.MICRONEEDLE, DeliverySystem.PRODRUG]
        recommendations['rationale'].append(f"분자량 ({mw:.0f} Da) 경계선, 전달 시스템 필요")
        recommendations['enhancers'] = ['프로필렌글라이콜', '에탄올']

    else:
        # 소형 분자 (< 500 Da)
        if log_p < 0:
            # 친수성
            recommendations['primary'] = DeliverySystem.LIPOSOME
            recommendations['secondary'] = [DeliverySystem.NANOEMULSION, DeliverySystem.IONTOPHORESIS]
            recommendations['rationale'].append(f"친수성 (log P = {log_p:.2f})으로 지질 장벽 통과 어려움")
            recommendations['enhancers'] = ['프로필렌글라이콜', '에탄올 20-30%', 'Tween 80']

        elif 0 <= log_p <= 3:
            # 이상적 친유성
            if log_p >= 1 and log_p <= 2.5:
                recommendations['primary'] = DeliverySystem.CONVENTIONAL
                recommendations['rationale'].append(f"이상적 친유성 (log P = {log_p:.2f})")
            else:
                recommendations['primary'] = DeliverySystem.PENETRATION_ENHANCER
                recommendations['rationale'].append(f"양호한 친유성 (log P = {log_p:.2f})")
            recommendations['secondary'] = [DeliverySystem.NANOEMULSION, DeliverySystem.LIPOSOME]
            recommendations['enhancers'] = ['저농도 에탄올', '올레산 (선택적)']

        elif 3 < log_p <= 5:
            # 친유성
            recommendations['primary'] = DeliverySystem.NANOEMULSION
            recommendations['secondary'] = [DeliverySystem.SLN_NLC, DeliverySystem.CONVENTIONAL]
            recommendations['rationale'].append(f"친유성 (log P = {log_p:.2f}), 각질층 흡수 양호")
            recommendations['enhancers'] = ['IPM', '테르펜 (리모넨)']
            recommendations['considerations'].append("깊은 층 도달은 제한적일 수 있음")

        else:
            # 고친유성 (log P > 5)
            recommendations['primary'] = DeliverySystem.SLN_NLC
            recommendations['secondary'] = [DeliverySystem.NANOEMULSION]
            recommendations['rationale'].append(f"고친유성 (log P = {log_p:.2f}), 각질층 축적 경향")
            recommendations['enhancers'] = ['사이클로덱스트린', '올레산']
            recommendations['considerations'].append("각질층 reservoir 효과 예상")
            recommendations['considerations'].append("서방 효과로 활용 가능")

    # 수소결합 특성 고려
    if compound.hbd > 3:
        recommendations['considerations'].append(f"높은 HBD ({compound.hbd})로 지질 투과 저해")
        if DeliverySystem.PRODRUG not in recommendations['secondary']:
            recommendations['secondary'].append(DeliverySystem.PRODRUG)

    # PSA 고려
    if compound.psa > 60:
        recommendations['considerations'].append(f"높은 PSA ({compound.psa:.1f} Å²)로 투과 저해")

    return recommendations


def analyze_compound(compound: MolecularProperties) -> Dict[str, any]:
    """
    화합물의 피부 투과 특성을 종합 분석합니다.

    Args:
        compound: 분자 특성 데이터

    Returns:
        종합 분석 결과 딕셔너리
    """
    # Potts-Guy 계산
    log_kp = calculate_log_kp(compound.log_p, compound.mw)
    kp = 10 ** log_kp
    permeability_class = classify_permeability(log_kp)

    # Lipinski 규칙 체크
    lipinski = check_lipinski_rules(compound)

    # 전달 시스템 추천
    delivery = recommend_delivery_system(compound)

    # 예시 플럭스 계산 (1% 농도, 얼굴 적용 가정)
    flux = estimate_flux(
        kp=kp,
        concentration=10000,  # 1% = 10,000 μg/mL
        area=600,  # 얼굴 면적 약 600 cm²
        time_hours=24
    )

    return {
        'compound': {
            'name': compound.name,
            'name_kr': compound.name_kr,
            'mw': compound.mw,
            'log_p': compound.log_p,
            'hbd': compound.hbd,
            'hba': compound.hba,
            'psa': compound.psa
        },
        'potts_guy': {
            'log_kp': round(log_kp, 2),
            'kp': kp,
            'kp_scientific': f"{kp:.2e}",
            'permeability_class': permeability_class.value
        },
        'lipinski': lipinski,
        'delivery': delivery,
        'flux_example': flux,
        'summary': _generate_summary(compound, log_kp, permeability_class, lipinski, delivery)
    }


def _generate_summary(
    compound: MolecularProperties,
    log_kp: float,
    perm_class: PermeabilityClass,
    lipinski: Dict,
    delivery: Dict
) -> str:
    """분석 결과 요약문 생성"""
    lines = [
        f"== {compound.name_kr} ({compound.name}) 피부 투과 분석 ==",
        "",
        f"분자량: {compound.mw:.2f} Da | log P: {compound.log_p:.2f}",
        f"예측 log Kp: {log_kp:.2f} → 투과성: {perm_class.value}",
        f"Lipinski 평가: {lipinski['score']}/5점 ({lipinski['outlook']})",
        "",
        f"권장 전달 시스템: {delivery['primary'].value if delivery['primary'] else 'N/A'}",
    ]

    if delivery['enhancers']:
        lines.append(f"권장 촉진제: {', '.join(delivery['enhancers'][:3])}")

    if delivery['considerations']:
        lines.append(f"고려사항: {delivery['considerations'][0]}")

    return "\n".join(lines)


def compare_compounds(compound_keys: List[str]) -> List[Dict]:
    """
    여러 화합물의 투과 특성을 비교합니다.

    Args:
        compound_keys: COMPOUND_DATABASE의 키 리스트

    Returns:
        비교 결과 리스트
    """
    results = []

    for key in compound_keys:
        if key in COMPOUND_DATABASE:
            compound = COMPOUND_DATABASE[key]
            log_kp = calculate_log_kp(compound.log_p, compound.mw)
            kp = 10 ** log_kp
            perm_class = classify_permeability(log_kp)

            results.append({
                'key': key,
                'name': compound.name,
                'name_kr': compound.name_kr,
                'mw': compound.mw,
                'log_p': compound.log_p,
                'log_kp': round(log_kp, 2),
                'kp': kp,
                'permeability': perm_class.value
            })

    # log Kp 기준 정렬 (높은 투과성 순)
    results.sort(key=lambda x: x['log_kp'], reverse=True)

    return results


def calculate_penetration_enhancement(
    base_kp: float,
    enhancement_factor: float
) -> Dict[str, float]:
    """
    투과 촉진 효과를 계산합니다.

    Args:
        base_kp: 기본 투과 계수 (cm/h)
        enhancement_factor: 촉진 배율

    Returns:
        촉진 효과 정보
    """
    enhanced_kp = base_kp * enhancement_factor

    return {
        'base_kp': base_kp,
        'enhanced_kp': enhanced_kp,
        'enhancement_factor': enhancement_factor,
        'base_log_kp': math.log10(base_kp),
        'enhanced_log_kp': math.log10(enhanced_kp),
        'log_kp_increase': math.log10(enhancement_factor)
    }


# =============================================================================
# Utility Functions
# =============================================================================

def list_compounds() -> List[str]:
    """데이터베이스의 모든 화합물 키 목록을 반환합니다."""
    return list(COMPOUND_DATABASE.keys())


def get_compound(key: str) -> Optional[MolecularProperties]:
    """키로 화합물을 조회합니다."""
    return COMPOUND_DATABASE.get(key)


def search_compounds(
    max_mw: Optional[float] = None,
    min_log_p: Optional[float] = None,
    max_log_p: Optional[float] = None,
    max_hbd: Optional[int] = None
) -> List[MolecularProperties]:
    """
    조건에 맞는 화합물을 검색합니다.

    Args:
        max_mw: 최대 분자량
        min_log_p: 최소 log P
        max_log_p: 최대 log P
        max_hbd: 최대 HBD 수

    Returns:
        조건에 맞는 화합물 리스트
    """
    results = []

    for compound in COMPOUND_DATABASE.values():
        if max_mw and compound.mw > max_mw:
            continue
        if min_log_p and compound.log_p < min_log_p:
            continue
        if max_log_p and compound.log_p > max_log_p:
            continue
        if max_hbd and compound.hbd > max_hbd:
            continue
        results.append(compound)

    return results


# =============================================================================
# Main Execution (Examples)
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("피부 투과도 계산 도구 - 사용 예시")
    print("=" * 60)

    # 예시 1: 나이아신아마이드 분석
    print("\n[예시 1] 나이아신아마이드 종합 분석")
    niacinamide = COMPOUND_DATABASE['niacinamide']
    analysis = analyze_compound(niacinamide)
    print(analysis['summary'])

    # 예시 2: 여러 화합물 비교
    print("\n[예시 2] 미백 성분 투과성 비교")
    whitening_agents = ['niacinamide', 'arbutin', 'kojic_acid', 'tranexamic_acid', 'hydroquinone']
    comparison = compare_compounds(whitening_agents)

    print(f"{'성분명':<25} {'MW':>8} {'log P':>8} {'log Kp':>8} {'투과성':<12}")
    print("-" * 70)
    for item in comparison:
        print(f"{item['name_kr']:<20} {item['mw']:>8.1f} {item['log_p']:>8.2f} "
              f"{item['log_kp']:>8.2f} {item['permeability']:<12}")

    # 예시 3: 플럭스 계산
    print("\n[예시 3] 나이아신아마이드 5% 세럼 플럭스 계산")
    kp = calculate_kp_potts_guy(log_p=-0.37, mw=122)
    flux = estimate_flux(
        kp=kp,
        concentration=50000,  # 5%
        area=600,  # 얼굴
        time_hours=24
    )
    print(f"  투과 계수 (Kp): {kp:.2e} cm/h")
    print(f"  단위 면적 플럭스: {flux['flux_per_area']:.4f} μg/cm²/h")
    print(f"  24시간 총 투과량: {flux['cumulative_amount_mg']:.2f} mg")

    # 예시 4: 이상적 투과 조건 화합물 검색
    print("\n[예시 4] 이상적 피부 투과 조건 화합물 검색")
    ideal_compounds = search_compounds(max_mw=300, min_log_p=1, max_log_p=3, max_hbd=3)
    print(f"조건: MW < 300, 1 < log P < 3, HBD ≤ 3")
    print(f"검색 결과: {len(ideal_compounds)}개")
    for c in ideal_compounds:
        print(f"  - {c.name_kr} (MW={c.mw:.1f}, log P={c.log_p:.2f})")

    print("\n" + "=" * 60)
    print("분석 완료")
