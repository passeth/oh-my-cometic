---
name: batch-calculator
description: 화장품 배치 생산 계산 도구. Lab Scale에서 Pilot, Production Scale로의 스케일업 계산, 배치 크기 결정, 손실률 보정, 원료 발주량 산출, 단가 계산, 배치 기록서 생성을 수행합니다. 생산 효율성 최적화와 비용 관리에 활용됩니다.
category: cosmetic-helpers
allowed-tools: None
license: MIT license
metadata:
    skill-author: EVAS Cosmetic
    original-source: K-Dense Inc. (claude-scientific-skills structure)
    version: 1.0.0
---

# Batch Calculator Skill

## Overview

**Batch Calculator**는 화장품 생산의 핵심 계산 도구입니다. 실험실 규모(Lab Scale)에서 파일럿(Pilot), 대량 생산(Production)으로의 스케일업 과정에서 필요한 모든 계산을 지원합니다.

이 스킬이 제공하는 주요 기능:
- **스케일업 계산**: Lab → Pilot → Production 단계별 배율 계산
- **배치 크기 결정**: 설비 용량에 맞는 최적 배치 크기 산출
- **손실률 보정**: 공정별 손실을 고려한 투입량 계산
- **원료 발주량 산출**: 안전 재고를 포함한 발주량 계산
- **단가 계산**: 배치당, 개당 제조원가 산출
- **배치 기록서 생성**: 생산 문서화를 위한 표준 양식

## When to Use This Skill

- **신제품 개발 완료 후**: Lab 배합을 생산 규모로 전환할 때
- **생산 계획 수립 시**: 월간/분기 생산량에 맞는 배치 횟수 계산
- **원가 분석 시**: 제품별 제조원가 산출 및 비교
- **원료 발주 시**: 생산 계획 기반 원료 소요량 계산
- **공정 최적화 시**: 손실률 분석 및 개선

## Core Concepts

### 1. Scale-Up Factors (스케일업 배율)

화장품 생산의 일반적인 스케일업 단계:

```
Lab Scale    →  Pilot Scale  →  Production Scale
(100-500g)      (5-50kg)        (100-1000kg)

배율:
- Lab → Pilot: 10x ~ 100x
- Pilot → Production: 10x ~ 20x
- Lab → Production: 100x ~ 1000x
```

#### 단계별 특성

| 단계 | 배치 크기 | 목적 | 주요 확인 사항 |
|------|----------|------|---------------|
| Lab Scale | 100-500g | 배합 개발, 안정성 테스트 | 기본 물성, 사용감 |
| Pilot Scale | 5-50kg | 공정 최적화, 스케일업 검증 | 재현성, 설비 적합성 |
| Production | 100kg+ | 상업 생산 | 생산성, 품질 일관성 |

### 2. Loss Factors (손실률)

화장품 제조 공정별 일반적인 손실률:

```
공정별 손실률 (일반적인 범위):
────────────────────────────────────────────
칭량 (Weighing)           : 0.5-1.0%
혼합 (Mixing)             : 1.0-3.0%
유화 (Emulsification)     : 1.5-3.0%
분산 (Dispersion)         : 1.0-2.0%
여과 (Filtration)         : 0.5-2.0%
탈포 (Deaeration)         : 0.5-1.0%
충전 (Filling)            : 1.0-3.0%
────────────────────────────────────────────
총 누적 손실              : 5-15%
```

#### 제형별 평균 손실률

| 제형 | 평균 손실률 | 주요 손실 원인 |
|------|------------|---------------|
| 토너/미스트 | 3-5% | 용기 잔류, 충전 손실 |
| 에센스/세럼 | 4-6% | 고점도 잔류, 배관 손실 |
| 로션 | 5-8% | 유화 손실, 배관 잔류 |
| 크림 | 6-10% | 용기 잔류, 이송 손실 |
| 선크림 | 8-12% | 분산 손실, 충전 손실 |
| 클렌저 | 4-6% | 배관 손실 |
| 마스크팩 | 3-5% | 함침 손실 |

### 3. Batch Size Calculation (배치 크기 계산)

#### 기본 공식

```python
# 목표 생산량에서 배치 크기 역산
batch_size = target_output / (1 - loss_rate)

# 예시: 950kg 목표 생산, 손실률 5%
batch_size = 950 / (1 - 0.05) = 950 / 0.95 = 1000kg
```

#### 설비 용량 고려

```python
# 탱크 용량의 70-80%를 실제 배치 크기로 설정
effective_batch = tank_capacity * 0.75

# 예시: 1000L 탱크
# 유화 시 팽창, 교반 공간 고려
effective_batch = 1000 * 0.75 = 750L ≈ 750kg (비중 1.0 가정)
```

### 4. Overage Calculation (여분량 계산)

손실을 보정하기 위한 추가 투입량:

```python
def calculate_overage(target_output, loss_rate, safety_margin=0.02):
    """
    여분량 계산

    Args:
        target_output: 목표 생산량 (kg)
        loss_rate: 예상 손실률 (예: 0.05 = 5%)
        safety_margin: 안전 여유분 (기본 2%)

    Returns:
        필요 배치량
    """
    total_loss = loss_rate + safety_margin
    required_batch = target_output / (1 - total_loss)
    return required_batch

# 예시
target = 900  # kg
loss = 0.05   # 5%
safety = 0.02 # 2%

batch = calculate_overage(900, 0.05, 0.02)
# batch = 900 / (1 - 0.07) = 900 / 0.93 ≈ 968 kg
```

### 5. Raw Material Ordering (원료 발주량 계산)

```python
def calculate_order_quantity(
    formula_percent,
    batch_size,
    num_batches,
    safety_stock_factor=1.1,
    min_order_qty=None
):
    """
    원료 발주량 계산

    Args:
        formula_percent: 배합비 (%)
        batch_size: 배치 크기 (kg)
        num_batches: 배치 횟수
        safety_stock_factor: 안전 재고 배율 (기본 10%)
        min_order_qty: 최소 발주 단위 (kg)

    Returns:
        발주량 (kg)
    """
    # 이론 소요량
    theoretical = (formula_percent / 100) * batch_size * num_batches

    # 안전 재고 적용
    required = theoretical * safety_stock_factor

    # 최소 발주 단위 올림
    if min_order_qty:
        import math
        required = math.ceil(required / min_order_qty) * min_order_qty

    return required
```

#### 원료별 최소 발주 단위 예시

| 원료 카테고리 | 일반적인 MOQ | 비고 |
|-------------|-------------|------|
| 정제수 | N/A | 현장 생산 |
| 글리세린 | 20-200kg | 드럼 단위 |
| 부틸렌글라이콜 | 20-200kg | 드럼 단위 |
| 유화제 | 5-25kg | 캔/백 단위 |
| 점증제 | 1-25kg | 캔/백 단위 |
| 방부제 | 1-5kg | 캔 단위 |
| 향료 | 1-5kg | 캔 단위 |
| 활성 원료 | 0.1-1kg | 소포장 |

### 6. Cost Per Unit Calculation (단가 계산)

```python
def calculate_cost_per_unit(
    formula: list,
    batch_size: float,
    filling_volume: float,
    packaging_cost: float = 0,
    labor_cost: float = 0,
    overhead_rate: float = 0.15
):
    """
    제품 단가 계산

    Args:
        formula: 배합 리스트 [{"name": str, "percent": float, "price_kg": float}, ...]
        batch_size: 배치 크기 (kg)
        filling_volume: 충전량 (ml 또는 g)
        packaging_cost: 용기/포장 비용 (개당)
        labor_cost: 인건비 (배치당)
        overhead_rate: 간접비 비율 (기본 15%)

    Returns:
        단가 정보 dict
    """
    # 원료비 계산
    raw_material_cost = 0
    for item in formula:
        weight = (item["percent"] / 100) * batch_size
        cost = weight * item["price_kg"]
        raw_material_cost += cost

    # 단위당 원료비
    units_per_batch = (batch_size * 1000) / filling_volume  # g 변환
    raw_cost_per_unit = raw_material_cost / units_per_batch

    # 단위당 인건비
    labor_cost_per_unit = labor_cost / units_per_batch

    # 소계 (원료 + 포장 + 인건비)
    subtotal = raw_cost_per_unit + packaging_cost + labor_cost_per_unit

    # 간접비 적용
    total = subtotal * (1 + overhead_rate)

    return {
        "raw_material_cost_per_unit": round(raw_cost_per_unit, 2),
        "packaging_cost": packaging_cost,
        "labor_cost_per_unit": round(labor_cost_per_unit, 2),
        "overhead": round(subtotal * overhead_rate, 2),
        "total_cost_per_unit": round(total, 2),
        "units_per_batch": int(units_per_batch)
    }
```

## Common Workflows

### Workflow 1: Lab to Production Scale-Up

실험실 배합(500g)을 생산 규모(500kg)로 스케일업:

```python
# Step 1: 스케일 배율 계산
lab_batch = 0.5      # kg
production_batch = 500  # kg
scale_factor = production_batch / lab_batch  # 1000x

# Step 2: 배합비를 중량으로 변환
lab_formula = [
    {"name": "Water", "percent": 70.0},
    {"name": "Glycerin", "percent": 5.0},
    {"name": "Emulsifier", "percent": 3.0},
    {"name": "Oil Phase", "percent": 15.0},
    {"name": "Active", "percent": 2.0},
    {"name": "Preservative", "percent": 1.0},
    {"name": "Fragrance", "percent": 0.5},
    # Total: 96.5%, 나머지는 pH 조정 등
]

# Step 3: 생산 배치용 중량 계산
production_formula = []
for item in lab_formula:
    weight = (item["percent"] / 100) * production_batch
    production_formula.append({
        "name": item["name"],
        "percent": item["percent"],
        "weight_kg": weight
    })

# 결과:
# Water: 350 kg
# Glycerin: 25 kg
# Emulsifier: 15 kg
# Oil Phase: 75 kg
# Active: 10 kg
# Preservative: 5 kg
# Fragrance: 2.5 kg
```

### Workflow 2: Equipment Capacity Matching

설비 용량에 맞는 배치 크기 결정:

```python
# 설비 사양
tank_capacity = 1000  # L
mixer_max = 800       # L (effective volume)
homogenizer_max = 500 # L/hr throughput

# 실제 배치 크기 결정
# 유화 탱크는 70-80% 충전
effective_batch = tank_capacity * 0.75  # 750 L

# 비중 고려 (크림류 평균 0.95-1.0)
density = 0.98
batch_weight = effective_batch * density  # 735 kg

# 충전량 기준 생산 수량
filling_volume = 50  # ml
units_per_batch = (batch_weight * 1000) / filling_volume  # 14,700 units
```

### Workflow 3: Production Planning

월간 생산 계획 수립:

```python
# 월간 목표
monthly_target_units = 100000
filling_volume = 50  # ml

# 배치당 생산량 (손실 고려)
batch_size = 750  # kg
loss_rate = 0.06  # 6%
effective_output = batch_size * (1 - loss_rate)  # 705 kg
units_per_batch = (effective_output * 1000) / filling_volume  # 14,100 units

# 필요 배치 수
import math
batches_needed = math.ceil(monthly_target_units / units_per_batch)
# batches_needed = ceil(100000 / 14100) = 8 batches

# 실제 생산량
actual_production = batches_needed * units_per_batch  # 112,800 units
```

### Workflow 4: Raw Material Requirements

원료 소요량 및 발주량 계산:

```python
formula = [
    {"name": "Water", "percent": 70.0, "moq": None},
    {"name": "Glycerin", "percent": 5.0, "moq": 20},
    {"name": "BG", "percent": 3.0, "moq": 20},
    {"name": "Niacinamide", "percent": 2.0, "moq": 1},
    {"name": "Emulsifier", "percent": 3.0, "moq": 5},
]

batch_size = 750  # kg
num_batches = 8
safety_factor = 1.10  # 10% 안전 재고

requirements = []
for item in formula:
    theoretical = (item["percent"] / 100) * batch_size * num_batches
    required = theoretical * safety_factor

    if item["moq"]:
        import math
        order_qty = math.ceil(required / item["moq"]) * item["moq"]
    else:
        order_qty = required

    requirements.append({
        "name": item["name"],
        "theoretical_kg": round(theoretical, 1),
        "required_kg": round(required, 1),
        "order_qty_kg": order_qty
    })

# 결과:
# Water: 4200 kg (현장 생산)
# Glycerin: 300 kg → 320 kg 발주 (20kg x 16)
# BG: 180 kg → 200 kg 발주 (20kg x 10)
# Niacinamide: 120 kg → 132 kg 발주 (1kg x 132)
# Emulsifier: 180 kg → 200 kg 발주 (5kg x 40)
```

### Workflow 5: Cost Analysis

제품 원가 분석:

```python
formula = [
    {"name": "Water", "percent": 70.0, "price_kg": 0.5},
    {"name": "Glycerin", "percent": 5.0, "price_kg": 3.0},
    {"name": "BG", "percent": 3.0, "price_kg": 5.0},
    {"name": "Niacinamide", "percent": 2.0, "price_kg": 25.0},
    {"name": "Emulsifier", "percent": 3.0, "price_kg": 15.0},
    {"name": "Oil Phase", "percent": 10.0, "price_kg": 8.0},
    {"name": "Preservative", "percent": 0.8, "price_kg": 20.0},
    {"name": "Fragrance", "percent": 0.3, "price_kg": 80.0},
]

batch_size = 500  # kg
filling_volume = 50  # ml

# 원료비 계산
raw_material_cost = sum(
    (item["percent"] / 100) * batch_size * item["price_kg"]
    for item in formula
)
# ≈ 3,430 원/kg

units_per_batch = (batch_size * 1000) / filling_volume  # 10,000 units
raw_cost_per_unit = raw_material_cost / units_per_batch  # 343 원/개

# 총 원가
packaging_cost = 500   # 원/개 (용기 + 박스)
labor_cost = 200000    # 원/배치
overhead_rate = 0.15   # 15%

labor_per_unit = labor_cost / units_per_batch  # 20 원/개
subtotal = raw_cost_per_unit + packaging_cost + labor_per_unit  # 863 원
total_cost = subtotal * (1 + overhead_rate)  # 993 원/개
```

## Batch Record Generation

### 표준 배치 기록서 양식

```markdown
# 배치 기록서 (Batch Manufacturing Record)

## 제품 정보
- 제품명: [Product Name]
- 제품코드: [Product Code]
- 배치번호: [Batch No.]
- 배치크기: [Batch Size] kg
- 제조일: [Manufacturing Date]

## 배합표

| No. | 원료명 | INCI명 | 배합비(%) | 칭량(kg) | 실측(kg) | 비고 |
|-----|-------|--------|----------|---------|---------|------|
| 1   | 정제수 | Water | 70.00 | 350.00 | ___.___ | |
| 2   | 글리세린 | Glycerin | 5.00 | 25.00 | ___.___ | |
| ... | | | | | | |

**배합 합계**: 100.00% / 500.00 kg

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

## 품질 검사

| 항목 | 규격 | 측정값 | 판정 |
|------|------|-------|------|
| 외관 | 균일한 크림상 | | P / F |
| 색상 | 흰색~미황색 | | P / F |
| 향취 | 이취 없음 | | P / F |
| pH | 5.5-6.5 | | P / F |
| 점도 | 10,000-15,000 cP | | P / F |
| 비중 | 0.95-1.05 | | P / F |

## 생산 실적

- 이론 생산량: _____ kg
- 실제 생산량: _____ kg
- 수율: _____ %
- 충전량: _____ ml × _____ ea = _____ 개
- 손실량: _____ kg (손실률: _____%)

## 승인

| 역할 | 서명 | 일자 |
|------|------|------|
| 제조담당 | | |
| 품질담당 | | |
| 제조책임자 | | |
```

## Scale-Up Considerations

### 물리적 요인

```
1. 열전달 (Heat Transfer)
   - Lab: 빠른 가열/냉각
   - Production: 열전달 면적/부피 비율 감소
   - 대응: 가열/냉각 시간 증가, 자켓 열교환기 활용

2. 혼합 효율 (Mixing Efficiency)
   - Lab: 균일한 혼합 용이
   - Production: 불균일 혼합 위험
   - 대응: 임펠러 종류/속도 조정, 배플 설치

3. 전단력 (Shear Rate)
   - Lab: 높은 전단력
   - Production: 상대적 전단력 감소
   - 대응: 균질기 압력/속도 조정

4. 체류시간 (Residence Time)
   - Lab: 짧은 공정 시간
   - Production: 공정 시간 증가
   - 대응: 안정성 확인, 산화/미생물 위험 관리
```

### 공정 변수 조정

```
스케일업 시 일반적인 조정 사항:
─────────────────────────────────────────────────────
변수              Lab Scale    Production Scale
─────────────────────────────────────────────────────
교반 속도         500-1000rpm  200-400rpm (Tip speed 유지)
가열 시간         10-20분      30-60분
균질 시간         5-10분       10-20분
냉각 시간         20-30분      60-120분
탈포 시간         15-30분      30-60분
─────────────────────────────────────────────────────
```

### Tip Speed 계산

```python
def calculate_tip_speed(rpm, diameter_m):
    """
    임펠러 끝 속도 계산

    Args:
        rpm: 회전 속도
        diameter_m: 임펠러 직경 (m)

    Returns:
        Tip speed (m/s)
    """
    import math
    circumference = math.pi * diameter_m
    tip_speed = (circumference * rpm) / 60
    return round(tip_speed, 2)

# Lab Scale
lab_tip_speed = calculate_tip_speed(rpm=800, diameter_m=0.05)  # 2.09 m/s

# Production Scale (동일 Tip Speed 유지)
prod_diameter = 0.3  # m
target_tip_speed = 2.09
prod_rpm = (target_tip_speed * 60) / (math.pi * prod_diameter)  # ≈ 133 rpm
```

## Best Practices

### 1. 스케일업 단계적 접근

```
Lab (500g) → Bench (5kg) → Pilot (50kg) → Production (500kg)

각 단계에서 확인:
✓ 물성 재현성 (pH, 점도, 색상)
✓ 안정성 (원심분리, 온도 사이클)
✓ 사용감 (관능평가)
✓ 공정 파라미터 기록
```

### 2. 손실률 관리

```
손실 최소화 전략:
1. 배관 최적화: 데드 볼륨 최소화
2. 용기 선택: 잔량 적은 재질/형태
3. 공정 순서: 고가 원료는 후반부 투입
4. 세척 프로토콜: 원료별 세척제 최적화
5. 기록 관리: 실제 손실률 데이터 축적
```

### 3. 원료 재고 관리

```
재고 관리 원칙:
- 안전 재고: 1-2개월 소요량
- 발주 시점: 안전 재고 도달 시
- 보관 조건: 원료별 권장 조건 준수
- 선입선출: FIFO 원칙 적용
- 유효기간: 개봉 후 사용기한 관리
```

### 4. 원가 관리

```
원가 절감 포인트:
1. 대량 구매: MOQ 협상, 연간 계약
2. 대체 원료: 동등 스펙 저가 원료 검토
3. 배합 최적화: 불필요한 원료 제거
4. 손실 감소: 공정 개선으로 수율 향상
5. 설비 효율: 배치 크기 최적화
```

## Reference Files

상세 정보는 아래 참조 문서 확인:

| 파일 | 내용 |
|------|------|
| `references/scaleup_factors.md` | 스케일업 고려사항, 공정 변수 조정 가이드 |
| `references/equipment_capacity.md` | 설비 용량 가이드, 장비별 사양 |

## Scripts

| 스크립트 | 기능 |
|---------|------|
| `scripts/batch_calculator.py` | 배치 계산, 원료 소요량, 원가 분석 |

## Quick Reference

```python
# 배치 크기 계산 (손실 고려)
def adjusted_batch_size(target_output, loss_rate=0.05):
    return target_output / (1 - loss_rate)

# 예시: 950kg 목표, 5% 손실
batch = adjusted_batch_size(950, 0.05)  # 1000kg

# 원료 소요량
def material_requirement(percent, batch_size, num_batches, safety=1.1):
    return (percent / 100) * batch_size * num_batches * safety

# 예시: 글리세린 5%, 500kg × 10배치
glycerin = material_requirement(5, 500, 10)  # 275kg

# 단위당 원가
def cost_per_unit(total_material_cost, batch_size, fill_volume, loss=0.05):
    effective = batch_size * (1 - loss) * 1000  # g 변환
    units = effective / fill_volume
    return total_material_cost / units

# 예시: 원료비 200만원, 500kg 배치, 50ml 충전
cost = cost_per_unit(2000000, 500, 50)  # ≈ 211원/개
```

## Troubleshooting

### 문제: 스케일업 후 물성 변화

```
원인 1: 혼합 불균일
해결: Tip speed 일정하게 유지, 교반 시간 증가

원인 2: 온도 프로파일 차이
해결: 가열/냉각 속도 조정, 승온/강온 단계 세분화

원인 3: 전단력 부족
해결: 균질기 압력/시간 증가, 패스 횟수 조정
```

### 문제: 수율이 예상보다 낮음

```
원인 1: 배관/용기 잔류
해결: 배관 구조 개선, 용기 재질 변경

원인 2: 칭량 오차
해결: 저울 교정, 칭량 절차 표준화

원인 3: 충전 손실
해결: 노즐 최적화, 충전 속도 조정
```

### 문제: 원가가 예산 초과

```
원인 1: 원료가 상승
해결: 대체 원료 검토, 복수 공급업체 확보

원인 2: 손실률 과다
해결: 공정 개선, 손실 원인 분석

원인 3: 간접비 증가
해결: 배치 크기 최적화, 생산 효율 개선
```

## Summary

**batch-calculator** 스킬은 화장품 생산의 핵심 계산을 지원합니다:

1. **스케일업 계산**: Lab → Pilot → Production 단계별 배율 및 파라미터 조정
2. **배치 크기 결정**: 설비 용량, 손실률을 고려한 최적 배치량
3. **원료 관리**: 소요량 계산, 발주량 산출, 재고 관리
4. **원가 분석**: 원료비, 포장비, 인건비, 간접비 포함 단가 계산
5. **생산 문서화**: 배치 기록서 생성, 품질 추적

모든 계산은 실제 생산 데이터로 검증하고, 제품/설비별 특성을 반영하여 조정하세요.
