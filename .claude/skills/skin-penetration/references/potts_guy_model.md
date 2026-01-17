# Potts-Guy Model: Skin Permeability Prediction

## Overview

Potts-Guy 모델은 화합물의 피부 투과 계수(Kp)를 예측하는 가장 널리 사용되는 정량적 구조-투과성 관계(QSPR) 모델입니다. 1992년 Robert Potts와 Richard Guy가 발표한 이 모델은 단순하면서도 강력한 예측력을 제공합니다.

## The Equation

### 기본 공식

```
log Kp = 0.71 × log P - 0.0061 × MW - 6.3
```

**변수 설명:**
- **Kp**: 투과 계수 (Permeability Coefficient, cm/h)
- **log P**: 옥탄올/물 분배계수 (Partition Coefficient)
- **MW**: 분자량 (Molecular Weight, Dalton)

### 공식 유도 배경

Potts와 Guy는 97개 화합물의 실험적 투과 데이터를 분석하여 이 관계식을 도출했습니다:

1. **친유성 기여 (0.71 × log P)**
   - 각질층의 지질 구조와의 친화성
   - log P가 높을수록 투과 증가
   - 계수 0.71은 지질 장벽의 선택성 반영

2. **크기 기여 (-0.0061 × MW)**
   - 분자 크기에 따른 확산 제한
   - 큰 분자일수록 투과 감소
   - 음의 계수는 크기의 저해 효과 표현

3. **기본 상수 (-6.3)**
   - 모델의 절편값
   - 피부 장벽의 기본 저항성 반영

## Theoretical Basis

### Fick의 확산 법칙

피부 투과는 기본적으로 확산 현상입니다:

```
J = Kp × Cv

where:
  J = 플럭스 (Flux, μg/cm²/h)
  Kp = 투과 계수 (cm/h)
  Cv = 표면 농도 (μg/cm³)
```

### 투과 계수의 구성

```
Kp = (D × K) / h

where:
  D = 확산 계수 (Diffusion coefficient)
  K = 분배 계수 (각질층/용액)
  h = 확산 경로 길이 (각질층 두께)
```

### 모델의 물리적 의미

1. **log P 항**: 각질층-용액 간 분배 (K)에 해당
2. **MW 항**: 확산 계수 (D)에 해당
3. **상수 항**: 경로 길이와 기타 요인

## Application Examples

### 주요 화장품 활성 성분 Kp 값

| 성분 | MW (Da) | log P | 계산 log Kp | Kp (cm/h) | 투과성 |
|-----|---------|-------|-------------|-----------|--------|
| 카페인 | 194 | -0.07 | -7.53 | 2.95×10⁻⁸ | 중간 |
| 니코틴 | 162 | 1.17 | -5.46 | 3.47×10⁻⁶ | 높음 |
| 에스트라디올 | 272 | 4.01 | -4.81 | 1.55×10⁻⁵ | 높음 |
| 테스토스테론 | 288 | 3.32 | -5.40 | 3.98×10⁻⁶ | 높음 |
| 히드로코르티손 | 362 | 1.61 | -6.92 | 1.20×10⁻⁷ | 낮음 |
| 나이아신아마이드 | 122 | -0.37 | -7.30 | 5.01×10⁻⁸ | 중간 |
| 레티놀 | 286 | 5.68 | -4.80 | 1.58×10⁻⁵ | 높음 |
| 아스코르빈산 | 176 | -1.85 | -8.69 | 2.04×10⁻⁹ | 매우 낮음 |
| 살리실산 | 138 | 2.26 | -5.89 | 1.29×10⁻⁶ | 높음 |
| 알파-아르부틴 | 272 | -1.49 | -8.71 | 1.95×10⁻⁹ | 매우 낮음 |
| 트레티노인 | 300 | 6.30 | -4.66 | 2.19×10⁻⁵ | 매우 높음 |
| 하이드로퀴논 | 110 | 0.59 | -6.47 | 3.39×10⁻⁷ | 중간 |

### 계산 예시

**예시 1: 나이아신아마이드**
```python
MW = 122 Da
log_P = -0.37

log_Kp = 0.71 × (-0.37) - 0.0061 × 122 - 6.3
log_Kp = -0.26 - 0.74 - 6.3
log_Kp = -7.30

Kp = 10^(-7.30) = 5.01 × 10^-8 cm/h
```

**예시 2: 레티놀**
```python
MW = 286 Da
log_P = 5.68

log_Kp = 0.71 × 5.68 - 0.0061 × 286 - 6.3
log_Kp = 4.03 - 1.74 - 6.3
log_Kp = -4.01

Kp = 10^(-4.01) = 9.77 × 10^-5 cm/h
```

## Flux Calculation

### 기본 플럭스 계산

일정 농도에서 정상 상태 플럭스:

```
J = Kp × C_applied × A

where:
  J = 총 플럭스 (μg/h)
  Kp = 투과 계수 (cm/h)
  C_applied = 적용 농도 (μg/cm³ = μg/mL)
  A = 적용 면적 (cm²)
```

### 실제 적용 예시

**나이아신아마이드 5% 세럼, 얼굴 전체 적용:**
```
C_applied = 50,000 μg/mL = 50,000 μg/cm³
A = 600 cm² (얼굴 면적)
Kp = 5.01 × 10^-8 cm/h

J = 5.01 × 10^-8 × 50,000 × 600
J = 1.50 μg/h = 36 μg/day
```

### 시간에 따른 투과량

```
Q(t) = A × Kp × C × (t - lag_time)

where:
  Q(t) = 시간 t까지 누적 투과량
  lag_time = 지연 시간 (정상 상태 도달 시간)
```

## Model Limitations

### 1. 적용 범위 제한

**분자량 범위:**
- 유효 범위: 18 - 750 Da
- 최적 정확도: 100 - 500 Da
- 고분자(> 1000 Da): 정확도 급감

**친유성 범위:**
- 유효 범위: log P -3 ~ +6
- 매우 친수성(log P < -3): 과대 예측
- 매우 친유성(log P > 6): 과소 예측

### 2. 고려하지 않는 요인

| 요인 | 영향 | 한계점 |
|-----|------|--------|
| **이온화 상태** | pH에 따라 투과 변화 | 비이온화 형태만 고려 |
| **피부 상태** | 손상, 수화도 | 정상 피부 가정 |
| **대사** | 피부 내 효소 | 미변화체만 예측 |
| **제형 효과** | 용매, 점도 | 수용액 기준 |
| **부위 차이** | 해부학적 차이 | 평균 피부 가정 |
| **온도** | 확산 속도 | 32°C 기준 |

### 3. 실험값과의 편차

```
일반적 예측 정확도:
- 2배 이내: ~60%의 화합물
- 3배 이내: ~80%의 화합물
- 10배 이상 편차: ~10%의 화합물

특히 부정확한 경우:
- 매우 친수성 분자 (과대 예측)
- 이온화 분자 (과대 예측)
- 고분자량 분자 (예측 불가)
```

## Extended Models

### Flynn Database 확장

Flynn의 데이터베이스(90+ 화합물)를 기반으로 한 개선:

```
log Kp = 0.74 × log P - 0.0091 × MW - 2.39
```

### Abraham Model

용질 descriptor 기반 모델:

```
log Kp = -2.19 - 0.0087 × V + 0.42 × π - 1.58 × H_d - 3.57 × H_a + 1.89 × R

where:
  V = 분자 부피
  π = 분극률
  H_d = H-bond acidity
  H_a = H-bond basicity
  R = 과잉 굴절률
```

### 수정된 Potts-Guy (이온화 고려)

```
log Kp_apparent = log Kp_neutral + log(fraction_unionized)

fraction_unionized = 1 / (1 + 10^(pH - pKa))  # 산의 경우
fraction_unionized = 1 / (1 + 10^(pKa - pH))  # 염기의 경우
```

## Comparison with Experimental Data

### 검증 연구 결과

| 연구 | 화합물 수 | R² | RMSE (log) | 비고 |
|-----|----------|-----|------------|------|
| Potts & Guy (1992) | 97 | 0.67 | 0.72 | 원 논문 |
| Moss et al. (2002) | 210 | 0.59 | 0.83 | 확장 검증 |
| Mitragotri (2002) | 124 | 0.62 | 0.78 | 친유성 범위 확장 |
| Lian et al. (2008) | 89 | 0.64 | 0.71 | 화장품 성분 |

### 실측 vs 예측 비교

```
             예측 Kp (cm/h)    실측 Kp (cm/h)    비율
카페인        2.95×10⁻⁸        1.44×10⁻⁸        2.0x
에스트라디올   1.55×10⁻⁵        1.00×10⁻⁵        1.6x
테스토스테론   3.98×10⁻⁶        2.51×10⁻⁶        1.6x
니코틴        3.47×10⁻⁶        6.31×10⁻⁶        0.5x
물           1.26×10⁻⁴        2.00×10⁻³        0.06x*

* 물은 친수성 경로로 투과하여 모델 적용 부적합
```

## Practical Guidelines

### 투과 계수 해석

| log Kp | Kp (cm/h) | 투과성 등급 | 권장 전달 전략 |
|--------|-----------|-----------|---------------|
| > -4 | > 10⁻⁴ | 매우 높음 | 일반 제형 충분 |
| -4 ~ -5 | 10⁻⁵ ~ 10⁻⁴ | 높음 | 일반 제형 가능 |
| -5 ~ -6 | 10⁻⁶ ~ 10⁻⁵ | 중간 | 투과 촉진제 고려 |
| -6 ~ -7 | 10⁻⁷ ~ 10⁻⁶ | 낮음 | 전달 시스템 필요 |
| < -7 | < 10⁻⁷ | 매우 낮음 | 나노 캐리어/물리적 방법 |

### 화장품 개발 적용

1. **신규 활성 성분 스크리닝**
   - Potts-Guy로 1차 필터링
   - log Kp > -7 성분 우선 검토

2. **제형 최적화**
   - 예측 Kp 기반 농도 결정
   - 목표 플럭스 달성을 위한 조정

3. **효능 클레임 지원**
   - 피부 내 예상 농도 계산
   - 작용 농도와 비교

## Code Implementation

기본 계산 함수는 [permeability_calc.py](../scripts/permeability_calc.py)에서 제공합니다:

```python
def calculate_kp_potts_guy(log_p: float, mw: float) -> float:
    """
    Potts-Guy 모델로 투과 계수 계산

    Args:
        log_p: 옥탄올/물 분배계수
        mw: 분자량 (Da)

    Returns:
        Kp in cm/h
    """
    log_kp = 0.71 * log_p - 0.0061 * mw - 6.3
    return 10 ** log_kp
```

## References

1. Potts, R.O. & Guy, R.H. (1992). Predicting skin permeability. *Pharmaceutical Research*, 9(5), 663-669.
2. Flynn, G.L. (1990). Physicochemical determinants of skin absorption. *Principles of Route-to-Route Extrapolation for Risk Assessment*.
3. Moss, G.P. et al. (2002). Quantitative structure-permeability relationships for percutaneous absorption. *J Pharm Sci*, 91(7), 1619-1632.
4. Abraham, M.H. & Martins, F. (2004). Human skin permeation and partition: General linear free-energy relationship analyses. *J Pharm Sci*, 93(6), 1508-1523.
