#!/usr/bin/env python3
"""
Batch Calculator for Cosmetic Manufacturing

화장품 배치 생산을 위한 계산 도구
- 스케일업 계산 (Lab → Pilot → Production)
- 배치 크기 결정 및 설비 용량 매칭
- 손실률 보정 및 여분량 계산
- 원료 소요량 및 발주량 산출
- 제조원가 계산
- 배치 기록서 생성

Author: EVAS Cosmetic
License: MIT
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import math


@dataclass
class Ingredient:
    """원료 데이터 클래스"""
    name: str
    inci: str = ""
    percent: float = 0.0
    price_per_kg: float = 0.0
    moq: Optional[float] = None  # 최소 발주 단위 (kg)
    phase: str = "A"  # 배합 페이즈 (A, B, C, D 등)
    notes: str = ""


@dataclass
class BatchResult:
    """배치 계산 결과"""
    batch_size_kg: float
    theoretical_output_kg: float
    expected_output_kg: float
    loss_kg: float
    loss_percent: float
    units_count: int
    raw_material_cost: float
    cost_per_unit: float


# 제형별 손실률 데이터베이스
LOSS_FACTORS = {
    "toner": {
        "average_loss": 0.04,
        "range": (0.03, 0.05),
        "components": {
            "weighing": 0.005,
            "mixing": 0.010,
            "filtration": 0.010,
            "filling": 0.015
        }
    },
    "essence": {
        "average_loss": 0.05,
        "range": (0.04, 0.06),
        "components": {
            "weighing": 0.005,
            "mixing": 0.015,
            "deaeration": 0.010,
            "filling": 0.020
        }
    },
    "lotion": {
        "average_loss": 0.07,
        "range": (0.05, 0.08),
        "components": {
            "weighing": 0.005,
            "mixing": 0.015,
            "emulsification": 0.020,
            "cooling": 0.010,
            "filling": 0.020
        }
    },
    "cream": {
        "average_loss": 0.08,
        "range": (0.06, 0.10),
        "components": {
            "weighing": 0.005,
            "mixing": 0.020,
            "emulsification": 0.025,
            "cooling": 0.010,
            "filling": 0.020
        }
    },
    "sunscreen": {
        "average_loss": 0.10,
        "range": (0.08, 0.12),
        "components": {
            "weighing": 0.010,
            "dispersion": 0.025,
            "emulsification": 0.025,
            "cooling": 0.010,
            "filling": 0.030
        }
    },
    "cleanser": {
        "average_loss": 0.05,
        "range": (0.04, 0.06),
        "components": {
            "weighing": 0.005,
            "mixing": 0.020,
            "deaeration": 0.010,
            "filling": 0.015
        }
    },
    "mask_essence": {
        "average_loss": 0.05,
        "range": (0.04, 0.06),
        "components": {
            "weighing": 0.005,
            "mixing": 0.020,
            "filtration": 0.010,
            "filling": 0.015
        }
    }
}


# 설비 용량 데이터베이스
EQUIPMENT_CAPACITIES = {
    "mixer": {
        "lab": [1, 2, 5, 10],  # L
        "bench": [20, 30, 50],
        "pilot": [100, 150, 200, 300],
        "production": [500, 1000, 2000, 3000, 5000]
    },
    "fill_ratio": {
        "default": 0.70,
        "emulsion": 0.70,
        "low_viscosity": 0.80,
        "high_viscosity": 0.65
    }
}


def calculate_batch_size(
    target_output_kg: float,
    loss_rate: float = 0.05,
    safety_margin: float = 0.02
) -> Dict:
    """
    목표 생산량에서 필요한 배치 크기 계산

    Args:
        target_output_kg: 목표 생산량 (kg)
        loss_rate: 예상 손실률 (기본 5%)
        safety_margin: 안전 여유분 (기본 2%)

    Returns:
        배치 크기 정보 dict
    """
    total_loss = loss_rate + safety_margin
    required_batch = target_output_kg / (1 - total_loss)

    return {
        "target_output_kg": target_output_kg,
        "loss_rate": loss_rate,
        "safety_margin": safety_margin,
        "total_adjustment": round(total_loss * 100, 1),
        "required_batch_kg": round(required_batch, 2),
        "overage_kg": round(required_batch - target_output_kg, 2)
    }


def calculate_yield(
    theoretical_batch_kg: float,
    actual_output_kg: float
) -> Dict:
    """
    수율 계산

    Args:
        theoretical_batch_kg: 이론 배치량 (kg)
        actual_output_kg: 실제 생산량 (kg)

    Returns:
        수율 정보 dict
    """
    yield_percent = (actual_output_kg / theoretical_batch_kg) * 100
    loss_kg = theoretical_batch_kg - actual_output_kg
    loss_percent = 100 - yield_percent

    return {
        "theoretical_batch_kg": theoretical_batch_kg,
        "actual_output_kg": actual_output_kg,
        "yield_percent": round(yield_percent, 2),
        "loss_kg": round(loss_kg, 2),
        "loss_percent": round(loss_percent, 2)
    }


def scale_formula(
    formula: List[Dict],
    source_batch_kg: float,
    target_batch_kg: float
) -> List[Dict]:
    """
    배합비 스케일 변환

    Args:
        formula: 원래 배합 리스트 [{"name": str, "percent": float}, ...]
        source_batch_kg: 원래 배치 크기 (kg)
        target_batch_kg: 목표 배치 크기 (kg)

    Returns:
        변환된 배합 리스트
    """
    scale_factor = target_batch_kg / source_batch_kg

    scaled_formula = []
    for item in formula:
        source_weight = (item.get("percent", 0) / 100) * source_batch_kg
        target_weight = source_weight * scale_factor

        scaled_formula.append({
            **item,
            "source_weight_kg": round(source_weight, 4),
            "target_weight_kg": round(target_weight, 4),
            "scale_factor": scale_factor
        })

    return scaled_formula


def percent_to_weight(
    formula: List[Dict],
    batch_size_kg: float
) -> List[Dict]:
    """
    배합비(%)를 중량(kg)으로 변환

    Args:
        formula: 배합 리스트 [{"name": str, "percent": float}, ...]
        batch_size_kg: 배치 크기 (kg)

    Returns:
        중량이 추가된 배합 리스트
    """
    result = []
    total_percent = 0

    for item in formula:
        percent = item.get("percent", 0)
        weight = (percent / 100) * batch_size_kg
        total_percent += percent

        result.append({
            **item,
            "weight_kg": round(weight, 4),
            "weight_g": round(weight * 1000, 2)
        })

    # 합계 검증
    if abs(total_percent - 100) > 0.01:
        print(f"Warning: Total percent is {total_percent}%, not 100%")

    return result


def calculate_material_requirements(
    formula: List[Dict],
    batch_size_kg: float,
    num_batches: int,
    safety_factor: float = 1.10
) -> List[Dict]:
    """
    원료 소요량 및 발주량 계산

    Args:
        formula: 배합 리스트 (moq 포함 가능)
        batch_size_kg: 배치 크기 (kg)
        num_batches: 배치 횟수
        safety_factor: 안전 재고 배율 (기본 10%)

    Returns:
        원료별 소요량/발주량 리스트
    """
    requirements = []

    for item in formula:
        name = item.get("name", "Unknown")
        percent = item.get("percent", 0)
        moq = item.get("moq")

        # 이론 소요량
        theoretical_kg = (percent / 100) * batch_size_kg * num_batches

        # 안전 재고 적용
        required_kg = theoretical_kg * safety_factor

        # MOQ 반올림
        if moq and moq > 0:
            order_qty = math.ceil(required_kg / moq) * moq
        else:
            order_qty = required_kg

        requirements.append({
            "name": name,
            "percent": percent,
            "theoretical_kg": round(theoretical_kg, 2),
            "required_kg": round(required_kg, 2),
            "moq": moq,
            "order_qty_kg": round(order_qty, 2)
        })

    return requirements


def calculate_raw_material_cost(
    formula: List[Dict],
    batch_size_kg: float
) -> Dict:
    """
    원료비 계산

    Args:
        formula: 배합 리스트 (price_per_kg 포함)
        batch_size_kg: 배치 크기 (kg)

    Returns:
        원료비 정보 dict
    """
    total_cost = 0
    cost_breakdown = []

    for item in formula:
        name = item.get("name", "Unknown")
        percent = item.get("percent", 0)
        price_kg = item.get("price_per_kg", 0)

        weight_kg = (percent / 100) * batch_size_kg
        cost = weight_kg * price_kg
        total_cost += cost

        cost_breakdown.append({
            "name": name,
            "percent": percent,
            "weight_kg": round(weight_kg, 4),
            "price_per_kg": price_kg,
            "cost": round(cost, 2)
        })

    return {
        "batch_size_kg": batch_size_kg,
        "total_raw_material_cost": round(total_cost, 2),
        "cost_per_kg": round(total_cost / batch_size_kg, 2) if batch_size_kg > 0 else 0,
        "breakdown": cost_breakdown
    }


def calculate_cost_per_unit(
    formula: List[Dict],
    batch_size_kg: float,
    fill_volume_ml: float,
    loss_rate: float = 0.05,
    packaging_cost: float = 0,
    labor_cost_per_batch: float = 0,
    overhead_rate: float = 0.15,
    density: float = 1.0
) -> Dict:
    """
    제품 단가 계산

    Args:
        formula: 배합 리스트 (price_per_kg 포함)
        batch_size_kg: 배치 크기 (kg)
        fill_volume_ml: 충전량 (ml)
        loss_rate: 손실률 (기본 5%)
        packaging_cost: 포장비 (개당)
        labor_cost_per_batch: 인건비 (배치당)
        overhead_rate: 간접비 비율 (기본 15%)
        density: 제품 밀도 (g/ml, 기본 1.0)

    Returns:
        단가 정보 dict
    """
    # 원료비 계산
    raw_cost_result = calculate_raw_material_cost(formula, batch_size_kg)
    total_raw_cost = raw_cost_result["total_raw_material_cost"]

    # 실제 생산량 (손실 고려)
    effective_output_kg = batch_size_kg * (1 - loss_rate)

    # 단위 수량 계산
    fill_weight_g = fill_volume_ml * density
    units_per_batch = (effective_output_kg * 1000) / fill_weight_g

    # 단위당 원료비
    raw_cost_per_unit = total_raw_cost / units_per_batch

    # 단위당 인건비
    labor_cost_per_unit = labor_cost_per_batch / units_per_batch if labor_cost_per_batch > 0 else 0

    # 소계 (원료 + 포장 + 인건비)
    subtotal = raw_cost_per_unit + packaging_cost + labor_cost_per_unit

    # 간접비
    overhead_cost = subtotal * overhead_rate

    # 총 원가
    total_cost = subtotal + overhead_cost

    return {
        "batch_size_kg": batch_size_kg,
        "fill_volume_ml": fill_volume_ml,
        "loss_rate": loss_rate,
        "effective_output_kg": round(effective_output_kg, 2),
        "units_per_batch": int(units_per_batch),
        "raw_cost_per_unit": round(raw_cost_per_unit, 2),
        "packaging_cost": packaging_cost,
        "labor_cost_per_unit": round(labor_cost_per_unit, 2),
        "subtotal": round(subtotal, 2),
        "overhead_rate": overhead_rate,
        "overhead_cost": round(overhead_cost, 2),
        "total_cost_per_unit": round(total_cost, 2),
        "total_batch_cost": round(total_cost * units_per_batch, 2)
    }


def match_equipment_capacity(
    target_batch_kg: float,
    density: float = 1.0,
    fill_ratio: float = 0.70
) -> Dict:
    """
    목표 배치에 맞는 설비 용량 추천

    Args:
        target_batch_kg: 목표 배치 크기 (kg)
        density: 제품 밀도 (kg/L)
        fill_ratio: 탱크 충전율 (기본 70%)

    Returns:
        추천 설비 용량 정보
    """
    # 필요 용량 계산
    target_volume_L = target_batch_kg / density
    required_capacity = target_volume_L / fill_ratio

    # 표준 용량 목록
    standard_capacities = [5, 10, 20, 50, 100, 150, 200, 300, 500, 1000, 2000, 3000, 5000]

    # 적합한 용량 찾기
    suitable = [c for c in standard_capacities if c >= required_capacity]
    recommended = suitable[0] if suitable else standard_capacities[-1]

    # 실제 유효 용량
    effective_volume = recommended * fill_ratio
    effective_batch = effective_volume * density

    # 스케일 결정
    if recommended <= 10:
        scale = "lab"
    elif recommended <= 50:
        scale = "bench"
    elif recommended <= 300:
        scale = "pilot"
    else:
        scale = "production"

    return {
        "target_batch_kg": target_batch_kg,
        "target_volume_L": round(target_volume_L, 1),
        "required_capacity_L": round(required_capacity, 1),
        "recommended_capacity_L": recommended,
        "effective_volume_L": round(effective_volume, 1),
        "effective_batch_kg": round(effective_batch, 1),
        "fill_ratio_percent": round(target_volume_L / recommended * 100, 1),
        "scale": scale
    }


def calculate_production_plan(
    target_units: int,
    fill_volume_ml: float,
    batch_size_kg: float,
    loss_rate: float = 0.05,
    density: float = 1.0
) -> Dict:
    """
    생산 계획 수립

    Args:
        target_units: 목표 생산 수량 (개)
        fill_volume_ml: 충전량 (ml)
        batch_size_kg: 배치 크기 (kg)
        loss_rate: 손실률
        density: 제품 밀도

    Returns:
        생산 계획 정보
    """
    # 배치당 생산량
    effective_output_kg = batch_size_kg * (1 - loss_rate)
    fill_weight_g = fill_volume_ml * density
    units_per_batch = int((effective_output_kg * 1000) / fill_weight_g)

    # 필요 배치 수
    batches_needed = math.ceil(target_units / units_per_batch)

    # 총 생산량
    total_units = batches_needed * units_per_batch
    total_batch_kg = batches_needed * batch_size_kg

    # 잉여 생산
    surplus_units = total_units - target_units

    return {
        "target_units": target_units,
        "fill_volume_ml": fill_volume_ml,
        "batch_size_kg": batch_size_kg,
        "units_per_batch": units_per_batch,
        "batches_needed": batches_needed,
        "total_units": total_units,
        "surplus_units": surplus_units,
        "total_batch_kg": round(total_batch_kg, 2),
        "total_raw_material_kg": round(total_batch_kg, 2)
    }


def get_loss_factor(formulation_type: str) -> Dict:
    """
    제형별 손실률 조회

    Args:
        formulation_type: 제형 타입

    Returns:
        손실률 정보
    """
    default = {
        "average_loss": 0.05,
        "range": (0.03, 0.08),
        "components": {
            "weighing": 0.005,
            "mixing": 0.015,
            "filling": 0.020
        }
    }

    return LOSS_FACTORS.get(formulation_type.lower(), default)


def generate_batch_record(
    product_name: str,
    product_code: str,
    batch_number: str,
    batch_size_kg: float,
    formula: List[Dict],
    manufacturing_date: Optional[str] = None
) -> str:
    """
    배치 기록서 생성

    Args:
        product_name: 제품명
        product_code: 제품코드
        batch_number: 배치번호
        batch_size_kg: 배치 크기 (kg)
        formula: 배합 리스트
        manufacturing_date: 제조일 (기본 오늘)

    Returns:
        배치 기록서 마크다운 문자열
    """
    if manufacturing_date is None:
        manufacturing_date = datetime.now().strftime("%Y-%m-%d")

    # 배합표 생성
    formula_with_weight = percent_to_weight(formula, batch_size_kg)

    formula_table = "| No. | 원료명 | INCI명 | 배합비(%) | 칭량(kg) | 실측(kg) | 비고 |\n"
    formula_table += "|-----|--------|--------|----------|---------|---------|------|\n"

    total_percent = 0
    for i, item in enumerate(formula_with_weight, 1):
        name = item.get("name", "")
        inci = item.get("inci", "")
        percent = item.get("percent", 0)
        weight = item.get("weight_kg", 0)
        total_percent += percent

        formula_table += f"| {i} | {name} | {inci} | {percent:.2f} | {weight:.4f} | ___.___ | |\n"

    record = f"""# 배치 기록서 (Batch Manufacturing Record)

## 제품 정보

| 항목 | 내용 |
|------|------|
| 제품명 | {product_name} |
| 제품코드 | {product_code} |
| 배치번호 | {batch_number} |
| 배치크기 | {batch_size_kg} kg |
| 제조일 | {manufacturing_date} |

## 배합표

{formula_table}
**배합 합계**: {total_percent:.2f}% / {batch_size_kg} kg

## 제조 공정

### Phase A: 수상 (Water Phase)
- 온도: ___°C (목표: 75-80°C)
- 교반속도: ___ rpm
- 시간: ___ min
- 담당자: _______ / 확인자: _______

### Phase B: 유상 (Oil Phase)
- 온도: ___°C (목표: 75-80°C)
- 교반속도: ___ rpm
- 시간: ___ min
- 담당자: _______ / 확인자: _______

### Phase C: 유화 (Emulsification)
- 유화온도: ___°C
- 균질기 속도: ___ rpm
- 균질시간: ___ min
- 냉각 종료온도: ___°C
- 담당자: _______ / 확인자: _______

### Phase D: 첨가 (Addition)
- 첨가온도: ___°C
- 교반속도: ___ rpm
- 시간: ___ min
- 담당자: _______ / 확인자: _______

## 품질 검사

| 항목 | 규격 | 측정값 | 판정 |
|------|------|-------|------|
| 외관 | 균일한 상태 | | P / F |
| 색상 | 규정 색상 | | P / F |
| 향취 | 이취 없음 | | P / F |
| pH | ___-___ | | P / F |
| 점도 | ___-___ cP | | P / F |
| 비중 | ___-___ | | P / F |

## 생산 실적

| 항목 | 수치 |
|------|------|
| 이론 생산량 | {batch_size_kg} kg |
| 실제 생산량 | _____ kg |
| 수율 | _____% |
| 충전량 | ___ ml x ___ ea = ___개 |
| 손실량 | _____ kg (_____%) |

## 비고
_________________________________________________________________
_________________________________________________________________

## 승인

| 역할 | 서명 | 일자 |
|------|------|------|
| 제조담당 | | |
| 품질담당 | | |
| 제조책임자 | | |

---
*Document generated by Batch Calculator v1.0.0*
"""

    return record


def calculate_scaleup_parameters(
    lab_batch_kg: float,
    lab_rpm: float,
    lab_impeller_diameter_m: float,
    production_batch_kg: float,
    production_impeller_diameter_m: float,
    scale_rule: str = "tip_speed"
) -> Dict:
    """
    스케일업 시 공정 파라미터 계산

    Args:
        lab_batch_kg: 실험실 배치 크기 (kg)
        lab_rpm: 실험실 교반 속도 (rpm)
        lab_impeller_diameter_m: 실험실 임펠러 직경 (m)
        production_batch_kg: 생산 배치 크기 (kg)
        production_impeller_diameter_m: 생산 임펠러 직경 (m)
        scale_rule: 스케일 규칙 (tip_speed, power_per_volume, reynolds)

    Returns:
        스케일업 파라미터 dict
    """
    scale_factor = production_batch_kg / lab_batch_kg

    # Lab Tip Speed
    lab_tip_speed = math.pi * lab_impeller_diameter_m * lab_rpm / 60

    # Production RPM 계산
    if scale_rule == "tip_speed":
        # Tip speed 일정 유지 (가장 일반적)
        prod_rpm = lab_rpm * (lab_impeller_diameter_m / production_impeller_diameter_m)
    elif scale_rule == "power_per_volume":
        # 단위 부피당 동력 일정
        ratio = lab_impeller_diameter_m / production_impeller_diameter_m
        prod_rpm = lab_rpm * (ratio ** (2/3))
    elif scale_rule == "reynolds":
        # Reynolds 수 일정
        ratio = lab_impeller_diameter_m / production_impeller_diameter_m
        prod_rpm = lab_rpm * (ratio ** 2)
    else:
        prod_rpm = lab_rpm * (lab_impeller_diameter_m / production_impeller_diameter_m)

    # Production Tip Speed
    prod_tip_speed = math.pi * production_impeller_diameter_m * prod_rpm / 60

    return {
        "scale_factor": round(scale_factor, 1),
        "scale_rule": scale_rule,
        "lab": {
            "batch_kg": lab_batch_kg,
            "rpm": lab_rpm,
            "impeller_diameter_m": lab_impeller_diameter_m,
            "tip_speed_m_s": round(lab_tip_speed, 2)
        },
        "production": {
            "batch_kg": production_batch_kg,
            "rpm": round(prod_rpm, 0),
            "impeller_diameter_m": production_impeller_diameter_m,
            "tip_speed_m_s": round(prod_tip_speed, 2)
        }
    }


# 사용 예시
if __name__ == "__main__":
    print("=" * 70)
    print("Batch Calculator - Example Usage")
    print("=" * 70)

    # 예시 배합
    sample_formula = [
        {"name": "Water", "inci": "Aqua", "percent": 70.0, "price_per_kg": 0.5, "moq": None},
        {"name": "Glycerin", "inci": "Glycerin", "percent": 5.0, "price_per_kg": 3.0, "moq": 20},
        {"name": "Butylene Glycol", "inci": "Butylene Glycol", "percent": 3.0, "price_per_kg": 5.0, "moq": 20},
        {"name": "Niacinamide", "inci": "Niacinamide", "percent": 2.0, "price_per_kg": 25.0, "moq": 1},
        {"name": "Cetearyl Alcohol", "inci": "Cetearyl Alcohol", "percent": 3.0, "price_per_kg": 8.0, "moq": 5},
        {"name": "Mineral Oil", "inci": "Paraffinum Liquidum", "percent": 10.0, "price_per_kg": 4.0, "moq": 20},
        {"name": "Emulsifier", "inci": "Ceteareth-20", "percent": 2.5, "price_per_kg": 15.0, "moq": 5},
        {"name": "Preservative", "inci": "Phenoxyethanol", "percent": 0.8, "price_per_kg": 20.0, "moq": 1},
        {"name": "Fragrance", "inci": "Parfum", "percent": 0.3, "price_per_kg": 80.0, "moq": 1},
    ]

    # 1. 배치 크기 계산
    print("\n1. Batch Size Calculation")
    print("-" * 50)
    batch_result = calculate_batch_size(target_output_kg=950, loss_rate=0.05)
    print(f"Target Output: {batch_result['target_output_kg']} kg")
    print(f"Required Batch: {batch_result['required_batch_kg']} kg")
    print(f"Overage: {batch_result['overage_kg']} kg")

    # 2. 설비 용량 매칭
    print("\n2. Equipment Capacity Matching")
    print("-" * 50)
    equipment = match_equipment_capacity(target_batch_kg=500, density=0.98)
    print(f"Recommended Mixer: {equipment['recommended_capacity_L']} L")
    print(f"Effective Batch: {equipment['effective_batch_kg']} kg")
    print(f"Scale: {equipment['scale']}")

    # 3. 원료비 계산
    print("\n3. Raw Material Cost")
    print("-" * 50)
    cost_result = calculate_raw_material_cost(sample_formula, batch_size_kg=500)
    print(f"Total Raw Material Cost: {cost_result['total_raw_material_cost']:,.0f} KRW")
    print(f"Cost per kg: {cost_result['cost_per_kg']:,.0f} KRW")

    # 4. 단가 계산
    print("\n4. Cost Per Unit")
    print("-" * 50)
    unit_cost = calculate_cost_per_unit(
        formula=sample_formula,
        batch_size_kg=500,
        fill_volume_ml=50,
        loss_rate=0.06,
        packaging_cost=500,
        labor_cost_per_batch=200000,
        overhead_rate=0.15
    )
    print(f"Units per Batch: {unit_cost['units_per_batch']}")
    print(f"Raw Cost per Unit: {unit_cost['raw_cost_per_unit']:,.0f} KRW")
    print(f"Total Cost per Unit: {unit_cost['total_cost_per_unit']:,.0f} KRW")

    # 5. 생산 계획
    print("\n5. Production Planning")
    print("-" * 50)
    plan = calculate_production_plan(
        target_units=100000,
        fill_volume_ml=50,
        batch_size_kg=500,
        loss_rate=0.06
    )
    print(f"Target Units: {plan['target_units']:,}")
    print(f"Batches Needed: {plan['batches_needed']}")
    print(f"Total Production: {plan['total_units']:,} units")
    print(f"Surplus: {plan['surplus_units']:,} units")

    # 6. 원료 발주량
    print("\n6. Material Requirements")
    print("-" * 50)
    requirements = calculate_material_requirements(
        formula=sample_formula,
        batch_size_kg=500,
        num_batches=plan['batches_needed'],
        safety_factor=1.10
    )
    print(f"{'Material':<20} {'Required':<12} {'Order Qty':<12}")
    print("-" * 44)
    for req in requirements:
        print(f"{req['name']:<20} {req['required_kg']:<12.1f} {req['order_qty_kg']:<12.1f}")

    # 7. 스케일업 파라미터
    print("\n7. Scale-Up Parameters")
    print("-" * 50)
    scaleup = calculate_scaleup_parameters(
        lab_batch_kg=0.5,
        lab_rpm=800,
        lab_impeller_diameter_m=0.05,
        production_batch_kg=500,
        production_impeller_diameter_m=0.40,
        scale_rule="tip_speed"
    )
    print(f"Scale Factor: {scaleup['scale_factor']}x")
    print(f"Lab RPM: {scaleup['lab']['rpm']} → Production RPM: {scaleup['production']['rpm']}")
    print(f"Lab Tip Speed: {scaleup['lab']['tip_speed_m_s']} m/s")
    print(f"Production Tip Speed: {scaleup['production']['tip_speed_m_s']} m/s")

    print("\n" + "=" * 70)
    print("Batch Record Generation (Preview)")
    print("=" * 70)
    # 배치 기록서 생성은 generate_batch_record() 함수 사용
    # print(generate_batch_record("Moisturizing Cream", "MC-001", "MC-001-20250115-01", 500, sample_formula))
