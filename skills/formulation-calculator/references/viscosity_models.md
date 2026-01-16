# Viscosity Models Reference

## 점도 기초 개념

### 점도 정의

점도(Viscosity)는 유체의 흐름에 대한 저항을 나타내는 물리량입니다.

```
동점도 (Dynamic Viscosity): η
- 단위: Pa·s (파스칼초), cP (센티포아즈)
- 1 Pa·s = 1000 cP = 1000 mPa·s

운동점도 (Kinematic Viscosity): ν
- 정의: ν = η / ρ (밀도로 나눔)
- 단위: m²/s, cSt (센티스토크스)
- 1 cSt = 1 mm²/s
```

### 점도 단위 환산

| 단위 | 환산 |
|------|------|
| 1 Pa·s | = 1000 mPa·s = 1000 cP |
| 1 cP | = 1 mPa·s = 0.001 Pa·s |
| 1 P (Poise) | = 100 cP |
| 1 cSt | = 1 mm²/s |

### 화장품 점도 범위

| 제품 유형 | 점도 (cP) | 질감 |
|----------|----------|------|
| 물 | 1 | 액체 |
| 토너/미스트 | 1-50 | 워터리 |
| 에센스 | 50-500 | 부드러운 액체 |
| 세럼 | 500-3,000 | 점성 액체 |
| 로션 | 3,000-10,000 | 유동성 크림 |
| 크림 | 10,000-50,000 | 일반 크림 |
| 두꺼운 크림 | 50,000-200,000 | 리치 크림 |
| 밤/왁스 | 200,000+ | 고체에 가까움 |
| 꿀 | ~10,000 | 참고 |
| 케첩 | ~50,000 | 참고 |

## 유체 유동 특성

### 뉴턴 유체 (Newtonian Fluid)

점도가 전단속도에 무관하게 일정한 유체:

```
τ = η × γ

τ = 전단응력 (Pa)
η = 점도 (Pa·s) - 상수
γ = 전단속도 (1/s)

예시: 물, 글리세린, 실리콘 오일
```

### 비뉴턴 유체 (Non-Newtonian Fluid)

점도가 전단속도에 따라 변하는 유체:

#### 1. 의가소성 (Pseudoplastic / Shear Thinning)

전단속도 증가 시 점도 감소 - **대부분의 화장품**

```
특징:
- 정지 시: 높은 점도 (안정성)
- 도포 시: 낮은 점도 (펴짐성)
- 이상적인 화장품 특성

예시: 카보머 젤, 크림, 로션, 샴푸
```

#### 2. 확장성 (Dilatant / Shear Thickening)

전단속도 증가 시 점도 증가

```
특징:
- 빠른 교반/충격 시 점도 상승
- 드문 현상

예시: 고농도 전분 현탁액, 콘스타치 슬러리
```

#### 3. 소성 (Plastic / Bingham)

항복응력 이상에서만 흐름

```
τ = τ₀ + η_p × γ

τ₀ = 항복응력 (Pa)
η_p = 소성점도 (Pa·s)

예시: 치약, 일부 크림, 마스카라
```

#### 4. 틱소트로피 (Thixotropic)

시간에 따라 점도 변화 (전단 이력 의존)

```
특징:
- 교반 시 점도 감소
- 정치 시 점도 회복 (시간 소요)
- Hysteresis loop 형성

예시: 페인트, 일부 젤 제품
```

## 유동 모델

### 1. Power Law (Ostwald-de Waele) 모델

가장 널리 사용되는 비뉴턴 유체 모델:

```
τ = K × γⁿ

K = 유동 지수, Consistency index (Pa·sⁿ)
n = 유동 거동 지수, Flow behavior index (무단위)

겉보기 점도:
η_app = K × γ^(n-1)
```

#### 유동 거동 지수 (n) 해석

| n 값 | 유동 특성 | 의미 |
|------|----------|------|
| n < 1 | 의가소성 (Shear thinning) | 전단 시 점도 감소 |
| n = 1 | 뉴턴 유체 | 점도 일정 |
| n > 1 | 확장성 (Shear thickening) | 전단 시 점도 증가 |

#### 화장품 n 값 범위

| 제품 유형 | n 값 |
|----------|------|
| 카보머 젤 | 0.15-0.35 |
| 잔탄검 용액 | 0.10-0.25 |
| O/W 크림 | 0.40-0.60 |
| 로션 | 0.50-0.70 |
| 샴푸 | 0.60-0.80 |

### 2. Cross 모델

넓은 전단속도 범위에서 적용:

```
(η - η_∞) / (η_0 - η_∞) = 1 / (1 + (K × γ)^m)

η_0 = 제로 전단 점도 (zero-shear viscosity)
η_∞ = 무한 전단 점도 (infinite-shear viscosity)
K = 시간 상수
m = Cross rate constant
```

### 3. Carreau-Yasuda 모델

```
(η - η_∞) / (η_0 - η_∞) = [1 + (λ × γ)^a]^((n-1)/a)

λ = 완화 시간 (relaxation time)
a = Yasuda 상수 (전이 영역 폭)
n = Power law index
```

### 4. Herschel-Bulkley 모델

항복응력이 있는 유체:

```
τ = τ₀ + K × γⁿ

τ₀ = 항복응력
K, n = Power law 파라미터

n < 1: 항복응력 + 의가소성
n = 1: Bingham plastic
n > 1: 항복응력 + 확장성
```

## 점증제별 특성

### 1. 카보머 (Carbomer)

가장 널리 사용되는 합성 점증제

```
특성:
- 화학명: Carboxy vinyl polymer, Carbopol
- 구조: 아크릴산 가교 중합체
- HLB: 친수성 (수용성)
- pH 의존성: 중화 시 점증 (pH 4.5-8.0)
- 전해질 민감성: 높음 (점도 감소)
- 외관: 투명 젤

중화제: NaOH, KOH, TEA, AMP, Arginine
```

#### 카보머 농도-점도 관계

```python
def carbomer_viscosity(concentration_pct: float, grade: str = "940") -> float:
    """
    카보머 농도에 따른 점도 예측 (중화 후, 25°C)

    Args:
        concentration_pct: 카보머 농도 (%)
        grade: 카보머 등급 ("934", "940", "941", "Ultrez 10")

    Returns:
        예측 점도 (cP)
    """
    # 등급별 계수 (경험적)
    coefficients = {
        "934": {"a": 2.0, "b": 3.0},    # 저점도
        "940": {"a": 2.5, "b": 3.5},    # 범용
        "941": {"a": 2.0, "b": 3.2},    # 저점도
        "Ultrez 10": {"a": 2.8, "b": 3.8},  # 고점도
        "Ultrez 20": {"a": 2.3, "b": 3.3}   # 전해질 내성
    }

    coef = coefficients.get(grade, coefficients["940"])
    viscosity = 10 ** (coef["a"] + coef["b"] * concentration_pct)

    return round(viscosity, 0)

# 예시
# carbomer_viscosity(0.2, "940") → 약 4,000 cP
# carbomer_viscosity(0.3, "940") → 약 12,000 cP
# carbomer_viscosity(0.5, "940") → 약 70,000 cP
```

#### 카보머 사용 가이드

| 제품 | 농도 (%) | 예상 점도 (cP) |
|------|---------|---------------|
| 세럼 | 0.1-0.15 | 500-2,000 |
| 젤 로션 | 0.15-0.25 | 2,000-8,000 |
| 젤 크림 | 0.25-0.4 | 8,000-30,000 |
| 마스크 젤 | 0.4-0.8 | 30,000-100,000 |

### 2. 잔탄검 (Xanthan Gum)

천연 다당류 점증제

```
특성:
- 기원: Xanthomonas campestris 발효
- 구조: 음이온성 헤테로다당
- pH 범위: 2-12 (넓은 안정성)
- 전해질 내성: 우수
- 외관: 약간 탁함
- 특이점: 강한 의가소성, 낮은 n값
```

#### 잔탄검 농도-점도 관계

```python
def xanthan_viscosity(concentration_pct: float) -> float:
    """
    잔탄검 농도에 따른 점도 예측 (25°C, 낮은 전단속도)

    Args:
        concentration_pct: 잔탄검 농도 (%)

    Returns:
        예측 점도 (cP)
    """
    # 경험적 공식
    viscosity = 10 ** (1.8 + 2.8 * concentration_pct)
    return round(viscosity, 0)

# 예시
# xanthan_viscosity(0.2) → 약 250 cP
# xanthan_viscosity(0.5) → 약 1,600 cP
# xanthan_viscosity(1.0) → 약 16,000 cP
```

#### 잔탄검 사용 가이드

| 제품 | 농도 (%) | 특징 |
|------|---------|------|
| 현탁 안정화 | 0.1-0.2 | 입자 침전 방지 |
| 저점도 제형 | 0.2-0.4 | 로션, 에센스 |
| 중점도 제형 | 0.4-0.8 | 크림 베이스 |
| 고점도 제형 | 0.8-1.5 | 헤어젤, 마스크 |

### 3. HEC (Hydroxyethylcellulose)

셀룰로오스 유도체

```
특성:
- 화학명: 하이드록시에틸셀룰로오스
- 구조: 셀룰로오스 에테르
- 이온성: 비이온
- pH 범위: 2-12
- 전해질 내성: 우수 (비이온성)
- 외관: 투명-반투명
- 점도 등급: LR, MR, HR, VHR
```

#### HEC 농도-점도 관계

```python
def hec_viscosity(concentration_pct: float, grade: str = "250HHR") -> float:
    """
    HEC 농도에 따른 점도 예측 (25°C)

    Args:
        concentration_pct: HEC 농도 (%)
        grade: HEC 등급

    Returns:
        예측 점도 (cP)
    """
    # 등급별 2% 점도 기준
    grade_viscosity_2pct = {
        "250LR": 150,       # Low Range
        "250MR": 4500,      # Medium Range
        "250HR": 20000,     # High Range
        "250HHR": 6500,     # Very High Range
    }

    base_visc = grade_viscosity_2pct.get(grade, 6500)

    # 농도 비례 (비선형)
    viscosity = base_visc * (concentration_pct / 2.0) ** 1.8

    return round(viscosity, 0)
```

### 4. 기타 점증제

#### CMC (Carboxymethylcellulose)

```
특성:
- 음이온성 셀룰로오스 에테르
- pH 민감성: pH < 3에서 침전
- 전해질 민감성: 있음 (점도 감소)
- 농도: 0.5-2.0%
```

#### Guar Gum (구아검)

```
특성:
- 천연 갈락토만난
- 비이온성
- 저렴함
- 점도: 높음 (동일 농도에서 잔탄검보다 높음)
- 농도: 0.2-1.0%
```

#### HPMC (Hydroxypropyl Methylcellulose)

```
특성:
- 비이온성 셀룰로오스 에테르
- 열젤화 특성 (온도↑ → 젤화)
- 필름 형성성
- 농도: 0.5-2.0%
```

#### Sepigel 305 (Polyacrylamide/C13-14 Isoparaffin/Laureth-7)

```
특성:
- 프리메이드 겔 농축액
- 중화 불필요
- 사용 편의성
- 농도: 1-4%
```

## 온도-점도 관계

### Arrhenius 모델

온도에 따른 점도 변화:

```
η = A × exp(Ea / RT)

또는 두 온도 비교:

ln(η₂/η₁) = (Ea/R) × (1/T₂ - 1/T₁)

η = 점도 (Pa·s)
A = 빈도 인자
Ea = 활성화 에너지 (J/mol)
R = 기체 상수 (8.314 J/mol·K)
T = 절대 온도 (K)
```

#### 활성화 에너지 범위

| 제품 유형 | Ea (kJ/mol) |
|----------|-------------|
| 물 | 15-17 |
| 글리세린 | 45-50 |
| 로션 | 20-35 |
| 크림 | 30-50 |
| 실리콘 오일 | 10-15 |

### 온도 보정 계산

```python
import math

def temperature_correction(viscosity_t1: float, t1: float, t2: float,
                          ea: float = 25000) -> float:
    """
    온도 변화에 따른 점도 보정

    Args:
        viscosity_t1: T1에서의 점도 (cP)
        t1: 측정 온도 (°C)
        t2: 목표 온도 (°C)
        ea: 활성화 에너지 (J/mol), 기본 25000

    Returns:
        T2에서의 예측 점도 (cP)
    """
    R = 8.314  # J/mol·K

    T1_K = t1 + 273.15
    T2_K = t2 + 273.15

    # Arrhenius 비율
    ratio = math.exp((ea / R) * (1/T2_K - 1/T1_K))

    viscosity_t2 = viscosity_t1 * ratio

    return round(viscosity_t2, 0)

# 예시: 25°C에서 10,000 cP → 20°C에서?
# temperature_correction(10000, 25, 20) → 약 12,500 cP

# 예시: 25°C에서 10,000 cP → 40°C에서?
# temperature_correction(10000, 25, 40) → 약 5,800 cP
```

### 실무적 온도 보정 규칙

```
대략적 경험 법칙 (화장품 크림/로션):

온도 10°C 상승 → 점도 약 30-50% 감소
온도 10°C 하강 → 점도 약 40-60% 증가

예시 (25°C 기준):
- 15°C: +50-80%
- 20°C: +20-30%
- 30°C: -20-25%
- 40°C: -35-45%
```

## 점도 측정

### Brookfield 점도계

가장 널리 사용되는 회전 점도계:

```
구성:
- 스핀들: 다양한 형태/크기 (LV1-4, RV1-7 등)
- 회전 속도: 0.3-200 RPM
- 측정 범위: 1-8,000,000 cP (모델에 따라)

측정 원리:
- 스핀들 회전 시 토크 측정
- 토크 → 점도 환산 (스핀들 계수 적용)
```

#### 스핀들 선택 가이드

| 점도 범위 (cP) | 권장 스핀들 | RPM |
|---------------|------------|-----|
| 1-100 | LV1 | 60 |
| 100-1,000 | LV2 | 30-60 |
| 1,000-5,000 | LV3 | 12-30 |
| 5,000-20,000 | LV4 | 6-12 |
| 20,000-100,000 | RV5/6 | 2.5-10 |
| 100,000+ | RV7/T-Bar | 0.5-5 |

#### 측정 조건 표준화

```
온도: 25 ± 0.5°C (또는 명시된 온도)
평형 시간: 스핀들 삽입 후 1-5분
회전 시간: 최소 1분 안정화 후 읽기
스핀들 위치: 샘플 중앙, 일정 깊이
용기: 직경/깊이 일정 (600mL 비커 표준)

기록 사항:
- 점도계 모델
- 스핀들 번호
- RPM
- 온도
- % 토크 (20-80% 범위 권장)
```

### 콘-플레이트 점도계

정밀한 레올로지 측정:

```
특징:
- 낮은 전단속도 범위 측정 가능
- 유동 곡선 전체 측정
- 항복응력 측정
- 점탄성 측정 (진동 모드)

용도:
- R&D, 품질 관리
- 제형 개발 최적화
```

## 점도 예측 실무

### 점증제 선택 흐름도

```
목표 점도 결정
    │
    ▼
제형 특성 확인
    │
    ├── 투명 젤 필요? → 카보머, HEC
    │
    ├── 전해질 함유? → 잔탄검, HEC, Sepigel
    │
    ├── 넓은 pH 필요? → 잔탄검, HEC
    │
    ├── 천연 지향? → 잔탄검, 구아검, 셀룰로오스
    │
    └── 의가소성 강조? → 잔탄검, 카보머
```

### 점도 목표 달성

```python
def predict_thickener_concentration(thickener: str, target_viscosity: float,
                                   grade: str = None) -> dict:
    """
    목표 점도를 위한 점증제 농도 예측

    Args:
        thickener: 점증제 종류
        target_viscosity: 목표 점도 (cP)
        grade: 점증제 등급 (선택)

    Returns:
        예측 농도 범위 및 권장 사항
    """
    import math

    recommendations = {}

    if thickener.lower() == "carbomer":
        # 역계산: concentration = (log(viscosity) - 2.5) / 3.5
        conc = (math.log10(target_viscosity) - 2.5) / 3.5
        recommendations = {
            "concentration_pct": round(conc, 2),
            "range": f"{round(conc*0.85, 2)}-{round(conc*1.15, 2)}%",
            "notes": "중화 필수, pH 5.5-7.0"
        }

    elif thickener.lower() == "xanthan":
        # 역계산: concentration = (log(viscosity) - 1.8) / 2.8
        conc = (math.log10(target_viscosity) - 1.8) / 2.8
        recommendations = {
            "concentration_pct": round(conc, 2),
            "range": f"{round(conc*0.85, 2)}-{round(conc*1.15, 2)}%",
            "notes": "고속 분산 필요"
        }

    return recommendations
```

## 문제 해결

### 문제: 점도가 불안정

```
원인 1: 온도 변동
해결: 온도 조절, 측정 온도 통일

원인 2: 전단 이력
해결: 일정한 전처리 (shear history), 대기 시간

원인 3: 미생물 오염
해결: 방부 시스템 확인, 위생 관리
```

### 문제: 예측보다 점도 낮음

```
원인 1: 전해질 영향 (카보머)
해결: Ultrez 20 등 전해질 내성 등급 사용

원인 2: pH 부적절 (카보머)
해결: 충분한 중화 확인 (pH 5.5-7.0)

원인 3: 분산 불량
해결: 고속 분산, 분말 서서히 첨가

원인 4: 성분 상호작용
해결: 호환성 테스트, 점증제 변경
```

### 문제: 점도가 시간에 따라 감소

```
원인 1: 전단 박화 (Shear thinning)
해결: 정상 현상, 점탄성 회복 확인

원인 2: 고분자 분해
해결: 효소 활성 억제, 항균 확인

원인 3: 상분리
해결: 유화 안정성 확인, 재유화 고려
```
