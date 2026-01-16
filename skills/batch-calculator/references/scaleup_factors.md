# Scale-Up Factors Reference

## Overview

화장품 제조에서 스케일업(Scale-Up)은 실험실 규모의 배합을 파일럿 및 상업 생산 규모로 확대하는 과정입니다. 이 문서는 스케일업 시 고려해야 할 주요 요인과 조정 방법을 상세히 다룹니다.

## Scale-Up Stages

### 일반적인 스케일업 단계

```
Stage 1: Laboratory Scale (Lab)
├── 배치 크기: 100g - 1kg
├── 목적: 기본 배합 개발, 초기 안정성 확인
├── 장비: 비커, 교반기, 핫플레이트
└── 기간: 1-4주

Stage 2: Bench Scale
├── 배치 크기: 1kg - 10kg
├── 목적: 배합 최적화, 공정 파라미터 설정
├── 장비: 소형 믹서, 균질기
└── 기간: 2-4주

Stage 3: Pilot Scale
├── 배치 크기: 10kg - 100kg
├── 목적: 공정 검증, 스케일업 문제 식별
├── 장비: 파일럿 플랜트 설비
└── 기간: 4-8주

Stage 4: Production Scale
├── 배치 크기: 100kg - 2000kg+
├── 목적: 상업 생산
├── 장비: 생산 설비
└── 기간: 상시 운영
```

### Scale-Up 배율 기준

| From | To | Scale Factor | 주요 고려사항 |
|------|-----|-------------|--------------|
| Lab (500g) | Bench (5kg) | 10x | 기본 재현성 |
| Bench (5kg) | Pilot (50kg) | 10x | 혼합 효율, 열전달 |
| Pilot (50kg) | Production (500kg) | 10x | 설비 적합성, 수율 |
| Lab (500g) | Production (500kg) | 1000x | 전체 공정 검증 필수 |

## Physical Factors

### 1. 열전달 (Heat Transfer)

스케일업 시 가장 큰 변화가 일어나는 영역입니다.

#### Surface Area to Volume Ratio

```
부피 증가에 따른 표면적/부피 비율 변화:
─────────────────────────────────────────────────────
배치 크기    부피 (L)    표면적/부피 (m⁻¹)    상대 비율
─────────────────────────────────────────────────────
Lab           0.5         12.0                 1.00
Bench         5.0          5.6                 0.47
Pilot        50.0          2.6                 0.22
Production  500.0          1.2                 0.10
─────────────────────────────────────────────────────
```

표면적/부피 비율이 감소하면:
- 가열 시간 증가
- 냉각 시간 증가
- 온도 불균일 위험

#### 가열/냉각 시간 추정

```python
def estimate_heating_time(
    volume_liters: float,
    delta_temp: float,
    heat_transfer_coef: float = 500,  # W/m²·K
    jacket_area_ratio: float = 0.3     # 자켓 면적/부피
) -> float:
    """
    가열 시간 추정

    Args:
        volume_liters: 배치 부피 (L)
        delta_temp: 온도 변화량 (°C)
        heat_transfer_coef: 열전달 계수 (W/m²·K)
        jacket_area_ratio: 자켓 면적 비율

    Returns:
        예상 가열 시간 (분)
    """
    # 물성 가정: 밀도 1 kg/L, 비열 4000 J/kg·K
    mass = volume_liters  # kg
    specific_heat = 4000  # J/kg·K

    # 필요 열량
    heat_required = mass * specific_heat * delta_temp  # J

    # 열전달 면적 (근사)
    area = (volume_liters ** 0.67) * jacket_area_ratio  # m²

    # 평균 온도차 가정 (log mean)
    avg_delta_temp = delta_temp * 0.7  # 근사

    # 열전달 속도
    heat_rate = heat_transfer_coef * area * avg_delta_temp  # W

    # 가열 시간
    time_seconds = heat_required / heat_rate
    time_minutes = time_seconds / 60

    return round(time_minutes, 1)

# 예시: 500L 배치, 55°C 승온 (25→80°C)
# Lab (0.5L): ~5분
# Bench (5L): ~15분
# Pilot (50L): ~35분
# Production (500L): ~80분
```

#### 열전달 개선 방안

```
1. 설비 개선
   - 자켓 면적 증가
   - 내부 코일 설치
   - 외부 열교환기 순환

2. 공정 조정
   - 원료 예열 (물, 오일)
   - 분할 투입
   - 연속 가열/혼합

3. 배합 조정
   - 점도 낮은 단계에서 가열 완료
   - 열 민감 원료 후반부 투입
```

### 2. 혼합 효율 (Mixing Efficiency)

#### 혼합의 핵심 파라미터

```
Tip Speed (임펠러 끝 속도):
V = π × D × N / 60

V: Tip speed (m/s)
D: 임펠러 직경 (m)
N: 회전수 (rpm)

일반적인 권장 Tip Speed:
- 저점도 액상: 3-5 m/s
- 중점도 로션: 2-4 m/s
- 고점도 크림: 1-3 m/s
```

#### Reynolds Number (레이놀즈 수)

혼합 상태를 나타내는 무차원수:

```
Re = ρ × N × D² / μ

ρ: 밀도 (kg/m³)
N: 회전수 (1/s)
D: 임펠러 직경 (m)
μ: 점도 (Pa·s)

혼합 영역:
- Re < 10: 층류 (Laminar) - 불균일 혼합 위험
- 10 < Re < 10,000: 전이 영역
- Re > 10,000: 난류 (Turbulent) - 균일 혼합
```

#### 스케일업 시 혼합 조정

```python
def calculate_scaled_rpm(
    lab_rpm: float,
    lab_diameter: float,
    prod_diameter: float,
    scale_rule: str = "tip_speed"
) -> float:
    """
    스케일업 시 RPM 계산

    Args:
        lab_rpm: 실험실 스케일 RPM
        lab_diameter: 실험실 임펠러 직경 (m)
        prod_diameter: 생산 임펠러 직경 (m)
        scale_rule: 스케일 규칙
            - "tip_speed": Tip speed 일정 (가장 일반적)
            - "power_per_volume": 단위 부피당 동력 일정
            - "reynolds": Re 수 일정

    Returns:
        생산 스케일 RPM
    """
    if scale_rule == "tip_speed":
        # V = π × D × N / 60 → N ∝ 1/D
        prod_rpm = lab_rpm * (lab_diameter / prod_diameter)

    elif scale_rule == "power_per_volume":
        # P/V ∝ N³ × D² → N ∝ D^(-2/3)
        prod_rpm = lab_rpm * (lab_diameter / prod_diameter) ** (2/3)

    elif scale_rule == "reynolds":
        # Re ∝ N × D² → N ∝ D^(-2)
        prod_rpm = lab_rpm * (lab_diameter / prod_diameter) ** 2

    return round(prod_rpm, 0)

# 예시: Lab 800rpm, 50mm → Production 300mm
# Tip speed 기준: 800 × (0.05/0.30) = 133 rpm
# Power/Volume 기준: 800 × (0.05/0.30)^0.67 = 227 rpm
# Reynolds 기준: 800 × (0.05/0.30)² = 22 rpm
```

#### 임펠러 종류별 특성

| 임펠러 타입 | 용도 | 점도 범위 | 특징 |
|------------|------|----------|------|
| Propeller | 저점도 혼합 | <1,000 cP | 축방향 유동, 빠른 순환 |
| Paddle | 중점도 혼합 | 1,000-10,000 cP | 반경방향 유동 |
| Anchor | 고점도 혼합 | 10,000-50,000 cP | 벽면 긁기, 열전달 개선 |
| Helical Ribbon | 매우 고점도 | >50,000 cP | 전체 혼합, 느린 속도 |
| Disperser Blade | 분산 | 다양 | 높은 전단력, 분쇄 |

### 3. 전단력 (Shear Rate)

유화 및 분산에 중요한 요소입니다.

#### 전단속도 계산

```
균질기 전단속도:
γ = V / δ

γ: 전단속도 (1/s)
V: 로터 속도 (m/s)
δ: 로터-스테이터 갭 (m)

일반적인 전단속도:
- 교반기: 10-100 1/s
- 호모믹서: 1,000-10,000 1/s
- 고압균질기: 10,000-100,000 1/s
- 초음파: 100,000+ 1/s
```

#### 유화 안정성과 전단력

```
스케일업 시 유화 품질 유지:
1. 동일 전단속도 유지 (어려움)
2. 동일 에너지 투입 (더 실용적)
3. 결과 기반 조정 (입자 크기 확인)

에너지 밀도 (Energy Density):
E = P × t / V

E: 에너지 밀도 (J/L)
P: 동력 (W)
t: 시간 (s)
V: 부피 (L)
```

### 4. 체류시간 (Residence Time)

공정 시간 증가에 따른 고려사항:

```
Lab Scale: 30분-1시간 총 공정
Production: 2-4시간 총 공정

위험 요소:
1. 산화: 항산화제 추가, 질소 블랭킷
2. 미생물: 방부제 효능 확인, 온도 관리
3. 물리적 변화: 점도 변화, 상분리
4. 휘발 손실: 향료, 용매 농도 확인
```

## Process-Specific Scale-Up Factors

### 유화 (Emulsification)

```
O/W 에멀전 스케일업 체크리스트:
─────────────────────────────────────────────────────
항목                    Lab        Production    조정
─────────────────────────────────────────────────────
수상 가열 시간          10분       40분         시간 증가
유상 가열 시간          10분       30분         시간 증가
유상 투입 속도          즉시       10-15분      서서히 투입
호모믹서 RPM           8000       6000-8000    속도 유지
호모믹서 시간           5분        15-20분      시간 증가
냉각 시간              15분       60-90분      시간 증가
첨가제 투입 온도        40°C       40°C         동일 유지
─────────────────────────────────────────────────────
```

### 분산 (Dispersion)

```
안료/파우더 분산 스케일업:
─────────────────────────────────────────────────────
단계          Lab             Production
─────────────────────────────────────────────────────
프리믹스      비커 교반        디스퍼서 사용
메인 분산     비드밀 5분       비드밀 15-30분
입자 크기     <10μm           <10μm (동일 목표)
패스 횟수     1-2회           2-4회
─────────────────────────────────────────────────────
```

### 겔 형성 (Gelation)

```
카보머 등 점증제 분산:
─────────────────────────────────────────────────────
단계                 Lab          Production
─────────────────────────────────────────────────────
카보머 분산          5분          30-60분 (서서히)
수화 시간           30분          60-120분
중화제 투입         즉시          10-20분 (서서히)
최종 교반           5분           15-30분
탈포               10분          30-60분
─────────────────────────────────────────────────────
```

## Scale-Up Factor Database

### 제형별 스케일업 팩터

```python
SCALEUP_FACTORS = {
    "toner": {
        "mixing_time_factor": 1.5,      # 혼합 시간 배율
        "heating_time_factor": 4.0,      # 가열 시간 배율
        "cooling_time_factor": 4.0,      # 냉각 시간 배율
        "typical_loss": 0.04,            # 예상 손실률
        "notes": "저점도, 비교적 단순한 공정"
    },
    "essence": {
        "mixing_time_factor": 2.0,
        "heating_time_factor": 3.5,
        "cooling_time_factor": 3.5,
        "typical_loss": 0.05,
        "notes": "중점도, 활성 원료 안정성 주의"
    },
    "lotion": {
        "mixing_time_factor": 2.5,
        "heating_time_factor": 4.0,
        "cooling_time_factor": 5.0,
        "emulsification_time_factor": 3.0,
        "typical_loss": 0.07,
        "notes": "유화 공정, 온도 관리 중요"
    },
    "cream": {
        "mixing_time_factor": 3.0,
        "heating_time_factor": 4.5,
        "cooling_time_factor": 6.0,
        "emulsification_time_factor": 3.5,
        "typical_loss": 0.08,
        "notes": "고점도 유화, 냉각 시간 중요"
    },
    "sunscreen": {
        "mixing_time_factor": 3.0,
        "heating_time_factor": 4.0,
        "cooling_time_factor": 5.0,
        "dispersion_time_factor": 4.0,
        "typical_loss": 0.10,
        "notes": "UV 필터 분산, 입자 크기 확인"
    },
    "cleanser": {
        "mixing_time_factor": 2.0,
        "heating_time_factor": 3.0,
        "cooling_time_factor": 4.0,
        "typical_loss": 0.05,
        "notes": "계면활성제 용해, 기포 관리"
    },
    "mask_sheet": {
        "mixing_time_factor": 2.0,
        "heating_time_factor": 3.5,
        "cooling_time_factor": 4.0,
        "typical_loss": 0.05,
        "notes": "에센스 제조 + 함침 공정"
    }
}
```

### 공정별 시간 추정

```python
def estimate_process_time(
    formulation_type: str,
    batch_size_kg: float,
    base_batch_kg: float = 0.5
) -> dict:
    """
    생산 공정 시간 추정

    Args:
        formulation_type: 제형 타입 (lotion, cream, etc.)
        batch_size_kg: 목표 배치 크기 (kg)
        base_batch_kg: 기준 배치 크기 (kg)

    Returns:
        공정별 예상 시간 (분)
    """
    import math

    factors = SCALEUP_FACTORS.get(formulation_type, {})
    scale_ratio = batch_size_kg / base_batch_kg

    # 로그 스케일링 적용 (선형보다 현실적)
    scale_factor = math.log10(scale_ratio) + 1 if scale_ratio > 1 else 1

    # 기준 공정 시간 (Lab scale, 분)
    base_times = {
        "preparation": 15,
        "heating": 15,
        "emulsification": 10,
        "cooling": 20,
        "final_mixing": 10,
        "deaeration": 15
    }

    estimated_times = {}
    for process, base_time in base_times.items():
        factor_key = f"{process}_time_factor"
        if factor_key in factors:
            factor = factors[factor_key]
        else:
            factor = 2.5  # 기본 팩터

        estimated_times[process] = round(base_time * scale_factor * factor / 2, 0)

    estimated_times["total"] = sum(estimated_times.values())

    return estimated_times

# 예시: 크림 500kg
# estimate_process_time("cream", 500)
# => preparation: 45, heating: 60, emulsification: 35, cooling: 90, final_mixing: 30, deaeration: 45
# => total: 305분 (약 5시간)
```

## Troubleshooting Scale-Up Issues

### 유화 불안정

```
증상: 스케일업 후 상분리, 크리밍

원인 1: 불충분한 균질화
├── 확인: 입자 크기 측정
└── 해결: 균질 시간/압력 증가, 패스 횟수 증가

원인 2: 온도 불균일
├── 확인: 유화 시 온도 분포 측정
└── 해결: 교반 강화, 유상 투입 속도 조절

원인 3: 냉각 속도 차이
├── 확인: 냉각 프로파일 기록
└── 해결: 냉각 속도 제어, 특정 온도대 유지 시간 확보
```

### 점도 차이

```
증상: 스케일업 후 점도 낮음/높음

원인 1: 혼합 부족 (점도 낮음)
├── 확인: 육안 균일성, 현미경 관찰
└── 해결: 혼합 시간 증가, 임펠러 변경

원인 2: 과도한 전단 (점도 낮음)
├── 확인: 전단 이력 분석
└── 해결: 균질 시간 단축, 속도 감소

원인 3: 불완전 수화 (점도 낮음)
├── 확인: 점증제 분산 상태
└── 해결: 수화 시간 증가, 분산 방법 개선

원인 4: 과도한 수화 시간 (점도 높음)
├── 확인: 공정 시간 비교
└── 해결: 수화 시간 표준화
```

### 색상/외관 차이

```
증상: 스케일업 후 색상 변화, 기포

원인 1: 산화
├── 확인: 색상 변화 시점 확인
└── 해결: 질소 블랭킷, 항산화제 증량

원인 2: 온도 영향
├── 확인: 온도 프로파일 비교
└── 해결: 가열 온도 제한, 시간 단축

원인 3: 기포 혼입
├── 확인: 점도, 기포 상태
└── 해결: 탈포 시간 증가, 진공 탈포
```

## Scale-Up Documentation

### 스케일업 보고서 양식

```markdown
# Scale-Up Report

## Product Information
- Product Name: ________________
- Product Code: ________________
- Target Batch Size: _______ kg

## Scale-Up History

| Parameter | Lab (500g) | Pilot (50kg) | Production (500kg) |
|-----------|-----------|--------------|-------------------|
| Batch Size | 500g | 50kg | 500kg |
| Scale Factor | 1x | 100x | 1000x |
| Mixer Type | Beaker | Pilot Mixer | Production Mixer |
| Impeller Dia. | 50mm | 150mm | 400mm |
| Mixing Speed | 800 rpm | 400 rpm | 150 rpm |
| Tip Speed | 2.1 m/s | 3.1 m/s | 3.1 m/s |
| Heating Time | 10 min | 25 min | 50 min |
| Cooling Time | 15 min | 40 min | 90 min |
| Total Time | 45 min | 120 min | 280 min |
| Yield | 98% | 95% | 93% |

## Quality Comparison

| Parameter | Spec | Lab | Pilot | Production |
|-----------|------|-----|-------|------------|
| pH | 5.5-6.5 | 6.0 | 5.9 | 6.1 |
| Viscosity (cP) | 10,000-15,000 | 12,000 | 11,500 | 12,500 |
| Color | White | White | White | White |
| Odor | Fragrance | Conform | Conform | Conform |
| Particle Size (μm) | <10 | 5.2 | 5.8 | 6.5 |

## Issues & Solutions

### Issue 1: [Description]
- Cause: ________________
- Solution: ________________
- Result: ________________

## Recommendations
1. ________________
2. ________________
3. ________________

## Approval
- Prepared by: ________________ Date: ________
- Reviewed by: ________________ Date: ________
- Approved by: ________________ Date: ________
```

## Summary

스케일업 성공의 핵심 원칙:

1. **단계적 접근**: Lab → Bench → Pilot → Production
2. **핵심 파라미터 유지**: Tip speed, 에너지 밀도, 온도 프로파일
3. **품질 모니터링**: 각 단계에서 물성 확인, 비교
4. **문서화**: 모든 변경사항, 조정 내용 기록
5. **유연한 대응**: 문제 발생 시 원인 분석, 조정

스케일업은 단순한 배율 증가가 아니라 공정 최적화 과정입니다. 각 단계에서의 학습을 축적하고 활용하세요.
