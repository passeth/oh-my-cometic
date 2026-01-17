# Arrhenius Model Reference

## Overview

Arrhenius 모델은 온도와 화학 반응 속도 사이의 관계를 설명하는 수학적 모델로,
가속 안정성 시험 데이터로부터 실온에서의 유통기한을 예측하는 데 사용됩니다.

## Arrhenius Equation

### Basic Equation

```
k = A * exp(-Ea / RT)

Where:
- k: 반응 속도 상수 (rate constant, 1/time)
- A: 빈도 인자 또는 전-지수 인자 (pre-exponential factor, 1/time)
- Ea: 활성화 에너지 (activation energy, J/mol or kJ/mol)
- R: 기체 상수 (8.314 J/mol*K)
- T: 절대 온도 (Kelvin)
```

### Linearized Form

Arrhenius plot을 위한 선형화 형태:

```
ln(k) = ln(A) - (Ea/R) * (1/T)

형태: y = b + m*x
- y = ln(k)
- x = 1/T
- m = -Ea/R (기울기)
- b = ln(A) (y절편)
```

### Two-Temperature Form

두 온도에서의 반응 속도로 활성화 에너지 계산:

```
ln(k2/k1) = (Ea/R) * (1/T1 - 1/T2)

Ea = R * ln(k2/k1) / (1/T1 - 1/T2)
```

## Q10 Factor

### Definition

Q10은 온도가 10C 상승할 때 반응 속도가 증가하는 배수입니다.

```
Q10 = k(T+10) / k(T)

또는

Q10 = exp(Ea * 10 / (R * T * (T+10)))

근사식 (T ~ 298K 근처):
Q10 = exp(Ea * 10 / (R * 298^2))
Q10 = exp(0.001135 * Ea)  [Ea in kJ/mol]
```

### Q10 vs Activation Energy

| Q10 | Ea (kJ/mol) | 반응 특성 |
|-----|-------------|----------|
| 1.5 | 35 | 매우 안정, 물리적 변화 |
| 2.0 | 50 | 안정, 단순 산화 |
| 2.5 | 65 | 보통, 일반 분해 |
| 3.0 | 80 | 민감, 복합 분해 |
| 3.5 | 90 | 민감, 효소 유사 |
| 4.0 | 100 | 매우 민감 |
| 5.0 | 115 | 극도로 민감 |

### Q10 Typical Values

화장품 관련 일반적인 Q10 값:

| 분해 유형 | Q10 범위 | 예시 |
|----------|---------|------|
| 물리적 분리 | 1.5-2.0 | 에멀전 크리밍, 색상 변화 |
| 단순 산화 | 2.0-2.5 | Vitamin E 산화 |
| 가수분해 | 2.0-3.0 | 에스터 가수분해, Niacinamide |
| 복합 산화 | 2.5-3.5 | Vitamin C, Retinol |
| 이성질화 | 3.0-4.0 | Retinoid trans-cis 변환 |
| 효소 반응 | 3.0-5.0 | 생물학적 활성 성분 |

## Activation Energy Database

### Cosmetic Active Ingredients

```python
ACTIVATION_ENERGY_DATABASE = {
    # Vitamins
    "ASCORBIC_ACID": {
        "Ea_kJ_mol": 54.5,
        "Q10": 2.0,
        "degradation": "oxidation",
        "pH_dependency": "faster at pH > 4",
        "reference": "J Pharm Sci. 2011"
    },
    "SODIUM_ASCORBYL_PHOSPHATE": {
        "Ea_kJ_mol": 65.0,
        "Q10": 2.3,
        "degradation": "hydrolysis, oxidation",
        "stability": "more stable than L-AA"
    },
    "ASCORBYL_GLUCOSIDE": {
        "Ea_kJ_mol": 72.0,
        "Q10": 2.5,
        "degradation": "hydrolysis",
        "stability": "excellent"
    },
    "TOCOPHEROL": {
        "Ea_kJ_mol": 67.2,
        "Q10": 2.3,
        "degradation": "oxidation",
        "note": "protects other ingredients"
    },
    "RETINOL": {
        "Ea_kJ_mol": 83.7,
        "Q10": 2.8,
        "degradation": "oxidation, isomerization",
        "light_sensitive": True,
        "reference": "Int J Cosmet Sci. 2015"
    },
    "RETINALDEHYDE": {
        "Ea_kJ_mol": 78.5,
        "Q10": 2.7,
        "degradation": "oxidation",
        "stability": "more stable than retinol"
    },
    "NIACINAMIDE": {
        "Ea_kJ_mol": 91.4,
        "Q10": 3.1,
        "degradation": "hydrolysis to nicotinic acid",
        "pH_dependency": "faster at low pH"
    },

    # Peptides
    "ACETYL_HEXAPEPTIDE_8": {
        "Ea_kJ_mol": 85.0,
        "Q10": 2.9,
        "degradation": "hydrolysis",
        "pH_optimal": "5.0-6.5"
    },
    "PALMITOYL_TRIPEPTIDE_1": {
        "Ea_kJ_mol": 75.0,
        "Q10": 2.6,
        "degradation": "hydrolysis",
        "stability": "moderate"
    },

    # Acids
    "GLYCOLIC_ACID": {
        "Ea_kJ_mol": 60.0,
        "Q10": 2.2,
        "degradation": "esterification, polymerization",
        "stability": "generally stable"
    },
    "SALICYLIC_ACID": {
        "Ea_kJ_mol": 55.0,
        "Q10": 2.0,
        "degradation": "decarboxylation",
        "stability": "stable at pH 3-4"
    },
    "HYALURONIC_ACID": {
        "Ea_kJ_mol": 70.0,
        "Q10": 2.4,
        "degradation": "depolymerization",
        "pH_dependency": "faster at extreme pH"
    },

    # Antioxidants
    "FERULIC_ACID": {
        "Ea_kJ_mol": 58.0,
        "Q10": 2.1,
        "degradation": "oxidation",
        "synergy": "stabilizes Vitamin C"
    },
    "RESVERATROL": {
        "Ea_kJ_mol": 62.0,
        "Q10": 2.2,
        "degradation": "oxidation, isomerization",
        "light_sensitive": True
    },
    "UBIQUINONE": {
        "Ea_kJ_mol": 75.0,
        "Q10": 2.6,
        "degradation": "oxidation",
        "light_sensitive": True
    },

    # Physical Stability
    "EMULSION_CREAMING": {
        "Ea_kJ_mol": 35.0,
        "Q10": 1.5,
        "type": "physical",
        "note": "temperature effect on viscosity"
    },
    "EMULSION_COALESCENCE": {
        "Ea_kJ_mol": 45.0,
        "Q10": 1.8,
        "type": "physical"
    },
    "COLOR_FADING": {
        "Ea_kJ_mol": 40.0,
        "Q10": 1.7,
        "type": "physical/chemical"
    }
}
```

## Shelf Life Prediction

### First-Order Kinetics

대부분의 화장품 분해는 1차 반응 속도식을 따릅니다:

```
C(t) = C0 * exp(-k*t)

또는

ln(C/C0) = -k*t

Where:
- C(t): 시간 t에서의 농도
- C0: 초기 농도
- k: 반응 속도 상수
- t: 시간
```

### Shelf Life Calculation

특정 잔존율에서의 수명 계산:

```
# 90% 잔존 (t90)
t90 = -ln(0.90) / k = 0.105 / k

# 95% 잔존 (t95)
t95 = -ln(0.95) / k = 0.051 / k

# 80% 잔존 (t80)
t80 = -ln(0.80) / k = 0.223 / k
```

### Prediction from Accelerated Data

```python
def predict_shelf_life(temp1, rate1, temp2, rate2, target_temp=25, target_retention=0.90):
    """
    두 온도에서의 분해 속도로 수명 예측

    Parameters:
    -----------
    temp1, temp2: 시험 온도 (Celsius)
    rate1, rate2: 각 온도에서의 분해 속도 (1/day)
    target_temp: 예측 온도 (Celsius)
    target_retention: 목표 잔존율 (0-1)

    Returns:
    --------
    예측 수명 (days)
    """
    import math

    R = 8.314  # J/(mol*K)

    # Convert to Kelvin
    T1 = temp1 + 273.15
    T2 = temp2 + 273.15
    T_target = target_temp + 273.15

    # Calculate Ea
    Ea = R * math.log(rate2/rate1) / (1/T1 - 1/T2)

    # Calculate A (pre-exponential factor)
    A = rate1 / math.exp(-Ea / (R * T1))

    # Rate at target temperature
    k_target = A * math.exp(-Ea / (R * T_target))

    # Shelf life
    shelf_life = -math.log(target_retention) / k_target

    return {
        "Ea_kJ_mol": Ea / 1000,
        "Q10": math.exp(Ea * 10 / (R * T_target * (T_target + 10))),
        "k_target": k_target,
        "shelf_life_days": shelf_life,
        "shelf_life_months": shelf_life / 30
    }
```

## Practical Examples

### Example 1: Vitamin C Serum

```
Data:
- 45C: 10% degradation in 30 days -> k45 = 0.105/30 = 0.0035 /day
- 40C: 10% degradation in 60 days -> k40 = 0.105/60 = 0.00175 /day

Calculation:
T1 = 313.15 K (40C)
T2 = 318.15 K (45C)
k1 = 0.00175 /day
k2 = 0.0035 /day

Ea = 8.314 * ln(0.0035/0.00175) / (1/313.15 - 1/318.15)
Ea = 8.314 * 0.693 / (0.00319 - 0.00314)
Ea = 5.76 / 0.00005
Ea = 115,200 J/mol = 115.2 kJ/mol

Wait, this seems high. Let me recalculate...

Actually: 1/T1 - 1/T2 = 1/313.15 - 1/318.15 = 0.003194 - 0.003143 = 0.000051

Ea = 8.314 * ln(2) / 0.000051 = 8.314 * 0.693 / 0.000051 = 112,900 J/mol

Hmm, still high. This could indicate non-Arrhenius behavior or measurement error.

Typical Vitamin C Ea is ~55 kJ/mol, so:
- Expected k ratio for 5C difference: exp(55000 * 5 / (8.314 * 313 * 318)) = 1.34
- But observed ratio is 2.0

Conclusion: Re-verify experimental data or consider alternative degradation pathway.
```

### Example 2: Retinol Cream

```
Data:
- 50C: 20% degradation in 14 days -> k50 = 0.223/14 = 0.0159 /day
- 40C: 20% degradation in 56 days -> k40 = 0.223/56 = 0.00398 /day

Calculation:
T1 = 313.15 K, k1 = 0.00398
T2 = 323.15 K, k2 = 0.0159

Ea = 8.314 * ln(0.0159/0.00398) / (1/313.15 - 1/323.15)
Ea = 8.314 * ln(4) / (0.003194 - 0.003095)
Ea = 8.314 * 1.386 / 0.000099
Ea = 116,400 J/mol = 116.4 kJ/mol

This is within expected range for retinol (80-120 kJ/mol)

Q10 = exp(116400 * 10 / (8.314 * 298 * 308)) = exp(1.52) = 4.6

Prediction at 25C:
k25 = 0.00398 * exp(-116400/8.314 * (1/298 - 1/313))
k25 = 0.00398 * exp(-14000 * 0.000161)
k25 = 0.00398 * exp(-2.25)
k25 = 0.00398 * 0.105 = 0.00042 /day

t90 at 25C = 0.105 / 0.00042 = 250 days = 8.3 months

With 1.5x safety factor: 5.5 months recommended shelf life
```

## Model Limitations

### Non-Arrhenius Behavior

Arrhenius 모델이 적용되지 않는 경우:

1. **상전이 (Phase Transition)**
   - 왁스 융점 근처
   - 에멀전 전환 온도 (PIT)
   - 유리 전이 온도 근처

2. **복합 반응 메커니즘**
   - 온도에 따라 주요 경로 변경
   - 연쇄 반응
   - 자가 촉매 반응

3. **물리적 변화**
   - 점도 변화 (지수적이지 않음)
   - 입자 크기 성장 (Ostwald ripening)
   - 결정화

### Recommendations for Better Predictions

```
1. 최소 3개 온도에서 데이터 수집
   - 예: 30C, 40C, 50C
   - R^2 > 0.95 확인

2. 온도 범위 적절히 선택
   - 상한: 제품 물리적 안정성 유지
   - 하한: 충분한 분해 관찰 가능

3. 시험 기간 충분히 확보
   - 최소 10-20% 분해 관찰
   - 측정 오차 최소화

4. 분해 메커니즘 확인
   - HPLC로 분해물 확인
   - 단일 메커니즘인지 확인

5. 안전 계수 적용
   - 예측값의 70-80%를 유통기한으로 설정
   - 또는 90% 신뢰구간 하한 사용
```

## Alternative Models

### ASAP (Accelerated Stability Assessment Program)

```
Modified Arrhenius for humidity:

ln(k) = ln(A) - Ea/(R*T) + B*(%RH)

Parameters:
- A: Pre-exponential factor
- Ea: Activation energy
- B: Humidity sensitivity coefficient
```

### WLF Equation (for glassy systems)

```
log(aT) = -C1 * (T - Tg) / (C2 + T - Tg)

For products near glass transition temperature
- Lipsticks
- Solid cosmetics
```

## Statistical Analysis

### Confidence Intervals

```python
def calculate_confidence_interval(Ea, std_error, n_temps, confidence=0.95):
    """
    활성화 에너지의 신뢰구간 계산
    """
    from scipy import stats

    t_value = stats.t.ppf((1 + confidence) / 2, n_temps - 2)

    lower = Ea - t_value * std_error
    upper = Ea + t_value * std_error

    return lower, upper
```

### Model Validation

```
1. 잔차 분석
   - 무작위 분포 확인
   - 이상치 식별

2. 교차 검증
   - Leave-one-out validation
   - 예측값 vs 실측값 비교

3. 실시간 데이터와 비교
   - 가속 시험 후 실온 검증
   - 편차 분석 및 모델 보정
```

## References

1. Connors, K.A., et al. (1986) Chemical Stability of Pharmaceuticals
2. Waterman, K.C., Adami, R.C. (2005) J Pharm Sci 94(3):517-539
3. Kommanaboyina, B., Rhodes, C.T. (1999) Drug Dev Ind Pharm 25(12):1321-1338
4. Grimm, W. (1998) Drug Dev Ind Pharm 24(4):313-325
5. ICH Q1E: Evaluation of Stability Data
