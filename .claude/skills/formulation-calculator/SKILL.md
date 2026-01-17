---
name: formulation-calculator
description: 화장품 배합 계산 도구. HLB(Hydrophilic-Lipophilic Balance) 계산, pH 조정, 점도 예측, 배합비 변환 등 제형 개발에 필수적인 계산을 수행합니다. 유화 시스템 설계, 버퍼 용량 계산, 스케일업/다운에 사용됩니다.
allowed-tools: [Read, Write, Edit, Bash]
license: MIT license
metadata:
    skill-author: EVAS Cosmetic
    original-source: K-Dense Inc. (claude-scientific-skills structure)
    version: 1.0.0
---

# Formulation Calculator Skill

## Overview

**Formulation Calculator**는 화장품 제형 개발에 필요한 핵심 계산을 수행하는 도구입니다. 유화제 선택부터 pH 조정, 점도 예측, 배치 스케일링까지 R&D 실무에 필수적인 계산을 지원합니다.

이 스킬은 다음과 같은 계산을 수행합니다:
- **HLB 계산**: 유화 시스템 설계를 위한 Required HLB 및 유화제 블렌딩
- **pH 조정**: 버퍼 시스템 설계 및 pH 조정제 필요량 계산
- **점도 예측**: 점증제 농도에 따른 점도 예측 및 온도 보정
- **배합비 계산**: 백분율-중량 변환, 스케일업/다운, 수율 계산

## When to Use This Skill

- **유화 시스템 설계**: O/W 또는 W/O 에멀전 개발 시 HLB 계산
- **pH 버퍼 계산**: 안정적인 pH 유지를 위한 완충액 설계
- **점도 조절**: 목표 점도 달성을 위한 점증제 농도 결정
- **배치 변환**: 실험실 규모에서 생산 규모로 스케일업
- **원가 계산**: 배합비 기반 원료 소요량 산출

## Core Capabilities

### 1. HLB (Hydrophilic-Lipophilic Balance) 계산

HLB는 유화제의 친수성-친유성 균형을 나타내는 수치(0-20)로, 유화 시스템 설계의 핵심입니다.

#### HLB 스케일
```
0-3    : W/O 유화제 (매우 친유성)
3-6    : W/O 유화제
7-9    : 습윤제
8-18   : O/W 유화제
13-15  : 세정제
15-18  : 가용화제
```

#### Griffin 방법 (비이온 유화제)
분자량 기반 HLB 계산:
```
HLB = 20 × (Mh / M)

Mh: 친수성 부분의 분자량
M : 전체 분자량
```

#### Davies 방법 (기능기 기반)
기능기의 기여도 합산:
```
HLB = 7 + Σ(친수성 기값) - Σ(친유성 기값)

친수성 기값:
- -SO4Na: +38.7
- -COOK: +21.1
- -COONa: +19.1
- -OH (free): +1.9
- -O-: +1.3
- -OH (sorbitan ring): +0.5

친유성 기값:
- -CH-, -CH2-, -CH3: -0.475
- =CH-: -0.475
```

#### Required HLB 계산
오일 혼합물의 Required HLB:
```python
Required_HLB = Σ(오일 비율 × 오일의 Required HLB) / Σ(오일 비율)

# 예시: 미네랄오일 70% + 호호바오일 30%
# Required HLB = (0.7 × 10.5 + 0.3 × 6.5) / 1.0 = 9.3
```

#### 유화제 블렌딩
목표 HLB를 위한 유화제 혼합 비율:
```python
# 목표 HLB = 10.0
# Span 60 (HLB 4.7) + Tween 60 (HLB 14.9)

# Tween 60 비율 = (목표HLB - 저HLB) / (고HLB - 저HLB)
# = (10.0 - 4.7) / (14.9 - 4.7) = 0.52 (52%)

# Span 60 비율 = 1 - 0.52 = 0.48 (48%)
```

### 2. pH 조정 계산

화장품의 pH는 안정성, 효능, 안전성에 직접적인 영향을 미칩니다.

#### Henderson-Hasselbalch 방정식
```
pH = pKa + log([A-] / [HA])

[A-]: 짝염기 농도 (예: 소듐시트레이트)
[HA]: 산 농도 (예: 시트르산)
pKa: 산의 해리 상수
```

#### 버퍼 용량 계산
버퍼가 pH 변화에 저항하는 능력:
```
β = 2.303 × C × Ka × [H+] / (Ka + [H+])²

C: 총 버퍼 농도
Ka: 산 해리 상수
[H+]: 수소이온 농도
```

최대 버퍼 용량은 **pH = pKa**일 때 발생합니다.

#### pH 조정제 필요량
현재 pH에서 목표 pH로 조정:
```python
def calculate_acid_needed(current_ph, target_ph, volume_ml, buffer_capacity):
    """
    Args:
        current_ph: 현재 pH
        target_ph: 목표 pH
        volume_ml: 용액 부피 (mL)
        buffer_capacity: 버퍼 용량 (mol/L/pH)

    Returns:
        필요한 산의 양 (mmol)
    """
    delta_ph = current_ph - target_ph
    acid_mmol = buffer_capacity * volume_ml * delta_ph
    return acid_mmol
```

#### 주요 완충 시스템

| 버퍼 시스템 | pKa | 유효 pH 범위 | 용도 |
|------------|-----|-------------|------|
| 시트르산/소듐시트레이트 | 3.13, 4.76, 6.40 | 2.5-7.0 | 범용 |
| 젖산/소듐락테이트 | 3.86 | 3.0-5.0 | 스킨케어 |
| 아세트산/소듐아세테이트 | 4.76 | 4.0-6.0 | 토너 |
| 인산염 버퍼 | 2.15, 7.20, 12.35 | 6.0-8.0 | 세정제 |

### 3. 점도 예측

제형의 점도는 사용감, 안정성, 생산성에 영향을 미칩니다.

#### Power Law 모델 (비뉴턴 유체)
```
τ = K × γ^n

τ: 전단응력 (Pa)
γ: 전단속도 (1/s)
K: 유동 지수 (Pa·s^n)
n: 유동 거동 지수
   n < 1: 의가소성 (shear thinning) - 대부분의 화장품
   n = 1: 뉴턴 유체
   n > 1: 확장성 (shear thickening)
```

#### 점증제 농도-점도 관계
```python
# Carbomer (카보머)
# 농도 범위: 0.1-1.0%
viscosity = 10 ** (2.5 + 3.2 * concentration)  # cP

# Xanthan Gum (잔탄검)
# 농도 범위: 0.1-1.0%
viscosity = 10 ** (1.8 + 2.8 * concentration)  # cP

# HEC (하이드록시에틸셀룰로오스)
# 농도 범위: 0.5-2.0%
viscosity = 10 ** (1.2 + 1.5 * concentration)  # cP
```

#### 온도-점도 관계 (Arrhenius)
```
ln(η2/η1) = (Ea/R) × (1/T2 - 1/T1)

η: 점도 (cP)
Ea: 활성화 에너지 (J/mol)
R: 기체 상수 (8.314 J/mol·K)
T: 절대 온도 (K)
```

실용적 근사식:
```python
def temperature_correction(viscosity_at_t1, t1, t2, ea=15000):
    """
    온도 변화에 따른 점도 보정

    Args:
        viscosity_at_t1: T1에서의 점도 (cP)
        t1: 측정 온도 (°C)
        t2: 목표 온도 (°C)
        ea: 활성화 에너지 (기본값 15000 J/mol, 일반 로션)

    Returns:
        T2에서의 예측 점도 (cP)
    """
    import math
    R = 8.314
    T1_K = t1 + 273.15
    T2_K = t2 + 273.15

    ratio = math.exp((ea / R) * (1/T2_K - 1/T1_K))
    return viscosity_at_t1 * ratio
```

### 4. 배합비 계산

#### 백분율-중량 변환
```python
def percent_to_weight(formula: list, batch_size: float) -> list:
    """
    배합비(%)를 실제 중량(g)으로 변환

    Args:
        formula: [{"name": "AQUA", "percent": 70.0}, ...]
        batch_size: 배치 크기 (g)

    Returns:
        [{"name": "AQUA", "percent": 70.0, "weight": 700.0}, ...]
    """
    result = []
    for item in formula:
        weight = item["percent"] * batch_size / 100
        result.append({
            **item,
            "weight": round(weight, 2)
        })
    return result
```

#### 배치 스케일업/다운
```python
def scale_batch(original_batch: float, original_formula: list,
                target_batch: float) -> list:
    """
    배치 크기 변환

    Args:
        original_batch: 원래 배치 크기 (g)
        original_formula: 원래 배합 (중량 기준)
        target_batch: 목표 배치 크기 (g)

    Returns:
        변환된 배합 리스트
    """
    scale_factor = target_batch / original_batch

    result = []
    for item in original_formula:
        new_weight = item["weight"] * scale_factor
        result.append({
            **item,
            "weight": round(new_weight, 2),
            "scale_factor": scale_factor
        })
    return result
```

#### 수율 계산
```python
def calculate_yield(theoretical_batch: float, actual_output: float) -> dict:
    """
    수율 계산

    Args:
        theoretical_batch: 이론 배치량 (g)
        actual_output: 실제 생산량 (g)

    Returns:
        {"yield_percent": 95.0, "loss": 50.0, "loss_percent": 5.0}
    """
    yield_percent = (actual_output / theoretical_batch) * 100
    loss = theoretical_batch - actual_output
    loss_percent = 100 - yield_percent

    return {
        "yield_percent": round(yield_percent, 2),
        "loss": round(loss, 2),
        "loss_percent": round(loss_percent, 2)
    }
```

## Common Workflows

### Workflow 1: 에멀전 설계

O/W 에멀전 개발을 위한 HLB 기반 유화제 선택:

```python
# 1. 오일상 구성 및 Required HLB 계산
oils = [
    {"name": "Mineral Oil", "percent": 8.0, "required_hlb": 10.5},
    {"name": "Jojoba Oil", "percent": 3.0, "required_hlb": 6.5},
    {"name": "Cetyl Alcohol", "percent": 2.0, "required_hlb": 15.5}
]

required_hlb = calculate_required_hlb(oils)
# 결과: Required HLB ≈ 11.0

# 2. 유화제 블렌딩 최적화
emulsifiers = [
    {"name": "Tween 60", "hlb": 14.9},
    {"name": "Span 60", "hlb": 4.7}
]

blend = blend_emulsifiers(target_hlb=required_hlb, emulsifiers=emulsifiers)
# 결과: Tween 60: 62%, Span 60: 38%

# 3. 유화제 사용량 결정 (오일상의 15-25%)
oil_phase_total = sum([o["percent"] for o in oils])
emulsifier_total = oil_phase_total * 0.20  # 20%
```

### Workflow 2: pH 버퍼 설계

pH 4.5 토너를 위한 시트르산/소듐시트레이트 버퍼:

```python
# 1. 목표 pH에 맞는 산/염기 비율 계산
target_ph = 4.5
pka = 4.76  # 시트르산 두 번째 해리

buffer_ratio = calculate_buffer_ratio(target_ph, pka)
# 결과: acid_ratio: 0.65, base_ratio: 0.35

# 2. 버퍼 농도 결정 (0.1-0.5% 일반적)
total_buffer = 0.2  # %
citric_acid = total_buffer * 0.65  # 0.13%
sodium_citrate = total_buffer * 0.35  # 0.07%

# 3. pH 조정제로 미세 조정
# 시트르산 10% 용액 또는 NaOH 10% 용액 사용
```

### Workflow 3: 점도 최적화

목표 점도 달성을 위한 점증제 농도 결정:

```python
# 1. 목표 점도 설정
target_viscosity = 10000  # cP (크림 질감)

# 2. 점증제 선택 및 농도 예측
thickener = "Carbomer 940"
predicted_conc = predict_concentration(
    thickener=thickener,
    target_viscosity=target_viscosity
)
# 결과: 0.3-0.4%

# 3. 온도 보정 (25°C 기준 → 실온 20°C)
viscosity_20c = temperature_correction(
    viscosity_at_t1=target_viscosity,
    t1=25, t2=20
)
# 결과: ~12000 cP (온도 낮으면 점도 상승)
```

### Workflow 4: 스케일업

Lab scale (500g) → Pilot (50kg) → Production (500kg):

```python
# 실험실 배합
lab_formula = [
    {"name": "Water", "weight": 350.0},
    {"name": "Glycerin", "weight": 25.0},
    {"name": "Niacinamide", "weight": 25.0},
    # ... 총 500g
]

# Pilot 스케일업 (100배)
pilot = scale_batch(
    original_batch=500,
    original_formula=lab_formula,
    target_batch=50000
)

# 생산 스케일업 (10배)
production = scale_batch(
    original_batch=50000,
    original_formula=pilot,
    target_batch=500000
)

# 수율 고려 (95% 가정 시 추가 투입량)
adjusted_batch = 500000 / 0.95  # ≈ 526,316g
```

## Best Practices

### 1. 정확도 관리
- 소수점 처리: 중량은 소수점 2자리, 백분율은 소수점 3자리
- 반올림 시점: 최종 결과에서만 반올림, 중간 계산은 전체 정밀도 유지
- 검증: 백분율 합계 100% 확인, 중량 합계 배치량 확인

### 2. 단위 확인
- 점도: cP (centipoise) = mPa·s (밀리파스칼초)
- 온도: 계산 시 켈빈(K), 표시 시 섭씨(°C)
- 농도: w/w% (중량 기준) 기본, w/v% 명시 필요
- pH: 무단위, 로그 스케일 주의 (pH 1 차이 = 10배 H+ 농도 차이)

### 3. 온도 고려
- HLB: 온도에 따라 변할 수 있음 (특히 POE 계열)
- 점도: 온도 의존성 큼, 측정/목표 온도 명시
- pH: 온도 보정 필요 (일반적으로 온도↑ → pH↓)

### 4. 실험적 검증
- 계산값은 출발점, 실제 배합 테스트로 확인
- HLB: ±1 범위에서 최적점 탐색
- 점도: 전단속도 의존성 고려 (측정 조건 통일)
- pH: 전극 교정, 온도 보정 필수

### 5. 문서화
- 모든 계산의 입력값, 공식, 결과 기록
- 온도, 측정 조건 명시
- 스케일업 시 각 단계별 조정 사항 기록

## Reference Files

상세 정보는 아래 참조 문서 확인:

| 파일 | 내용 |
|------|------|
| `references/hlb_calculation.md` | HLB 시스템 상세, 오일/유화제 데이터베이스 |
| `references/ph_adjustment.md` | pH 조정 상세, 버퍼 시스템, 산/알칼리 목록 |
| `references/viscosity_models.md` | 점도 예측 모델, 점증제별 특성 |

## Scripts

| 스크립트 | 기능 |
|---------|------|
| `scripts/hlb_calculator.py` | HLB 계산, 유화제 블렌딩 |
| `scripts/ph_buffer.py` | pH 버퍼 설계, 조정제 계산 |
| `scripts/viscosity_predictor.py` | 점도 예측, 온도 보정 |

## Troubleshooting

### 문제: HLB 계산값으로 유화 안됨
```
원인 1: Required HLB 데이터 부정확
해결: 다른 출처의 Required HLB 확인, ±1-2 범위 테스트

원인 2: 유화제 농도 부족
해결: 오일상의 15-25%로 유화제 증량

원인 3: 제조 조건 문제
해결: 온도, 교반 속도, 첨가 순서 점검
```

### 문제: pH가 불안정
```
원인 1: 버퍼 용량 부족
해결: 버퍼 농도 증가 (0.1% → 0.3%)

원인 2: 성분 간 상호작용
해결: pH 민감 성분 확인, 첨가 순서 조정

원인 3: 미생물 오염
해결: 방부 시스템 점검, 위생 관리
```

### 문제: 점도가 예측과 다름
```
원인 1: 점증제 특성 차이
해결: 제조사별 사양 확인, 경험적 데이터 축적

원인 2: pH 영향
해결: 카보머는 pH 의존적, 중화 상태 확인

원인 3: 전해질 영향
해결: 염 농도 확인, 점증제 종류 변경 검토
```

## Quick Reference

```python
# HLB 계산
from scripts.hlb_calculator import calculate_required_hlb, blend_emulsifiers

oils = [{"name": "Mineral Oil", "percent": 10, "required_hlb": 10.5}]
required_hlb = calculate_required_hlb(oils)
blend = blend_emulsifiers(target_hlb=10.5, emulsifiers=[...])

# pH 버퍼
from scripts.ph_buffer import calculate_buffer_ratio, calculate_acid_needed

ratio = calculate_buffer_ratio(target_ph=4.5, pka=4.76)
acid = calculate_acid_needed(current_ph=6.0, target_ph=5.5, volume=1000)

# 점도 예측
from scripts.viscosity_predictor import predict_viscosity, temperature_correction

viscosity = predict_viscosity(thickener="Carbomer 940", concentration=0.3)
corrected = temperature_correction(viscosity, t1=25, t2=20)
```

## Summary

**formulation-calculator** 스킬은 화장품 제형 개발의 핵심 계산 도구입니다:

1. **HLB 계산**: Griffin/Davies 방법, Required HLB, 유화제 블렌딩
2. **pH 조정**: Henderson-Hasselbalch, 버퍼 설계, 조정제 필요량
3. **점도 예측**: Power Law, 점증제-점도 관계, 온도 보정
4. **배합비 계산**: 단위 변환, 스케일업/다운, 수율 관리

모든 계산은 실험적 검증의 출발점으로 활용하고, 실제 배합 테스트로 최적화하세요.
