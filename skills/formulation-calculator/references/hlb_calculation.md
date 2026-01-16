# HLB Calculation Reference

## HLB 시스템 개요

HLB(Hydrophilic-Lipophilic Balance)는 1949년 Griffin이 도입한 개념으로, 유화제의 친수성과 친유성의 균형을 0-20 스케일로 나타냅니다.

### HLB 스케일

```
HLB 값     용도                          예시
-----------------------------------------------
0-3        W/O 유화제 (강한 친유성)      Span 85
3-6        W/O 유화제                    Span 80
6-9        습윤제                        Tween 61
8-16       O/W 유화제                    Tween 80
10-13      세정제                        Sodium lauryl sulfate
12-15      세정제/가용화제               Tween 20
15-18      가용화제                      Sodium laureth sulfate
```

## 계산 방법

### 1. Griffin 방법 (비이온 계면활성제)

분자량 기반 HLB 계산:

```
HLB = 20 × (Mh / M)

Mh = 친수성 부분의 분자량 (예: 폴리에틸렌옥사이드 사슬)
M  = 전체 분자량
```

#### 예시: Tween 80 (Polysorbate 80)
```
- 전체 분자량 (M): 약 1310 g/mol
- 친수성 부분 (PEO 20 units): 약 880 g/mol
- HLB = 20 × (880 / 1310) = 13.4
```

#### 폴리에틸렌옥사이드 계열 간편식
```
HLB = E / 5

E = 에틸렌옥사이드 중량 %
```

#### 다가알코올 지방산 에스테르
```
HLB = 20 × (1 - S/A)

S = 에스테르의 비누화가
A = 지방산의 산가
```

### 2. Davies 방법 (기능기 기반)

화학 구조의 기능기를 기반으로 HLB 계산:

```
HLB = 7 + Σ(친수성 기값) - Σ(친유성 기값)
```

#### 친수성 기 값 (Hydrophilic Group Numbers)

| 기능기 | HLB 기여값 |
|--------|-----------|
| -SO4Na | +38.7 |
| -COOK | +21.1 |
| -COONa | +19.1 |
| -N (tertiary amine) | +9.4 |
| Ester (sorbitan ring) | +6.8 |
| Ester (free) | +2.4 |
| -COOH | +2.1 |
| -OH (free) | +1.9 |
| -O- | +1.3 |
| -OH (sorbitan ring) | +0.5 |

#### 친유성 기 값 (Lipophilic Group Numbers)

| 기능기 | HLB 기여값 |
|--------|-----------|
| -CH- | -0.475 |
| -CH2- | -0.475 |
| -CH3 | -0.475 |
| =CH- | -0.475 |
| -CF2- | -0.870 |
| -CF3 | -0.870 |

#### Davies 방법 예시: Sodium Lauryl Sulfate

```
구조: CH3-(CH2)11-O-SO3-Na+

계산:
- -SO4Na: +38.7
- -O-: +1.3
- -CH2- × 11: -0.475 × 11 = -5.225
- -CH3: -0.475

HLB = 7 + 38.7 + 1.3 - 5.225 - 0.475 = 41.3

(실제 HLB는 40, 계산값과 근사)
```

## 오일별 Required HLB 데이터베이스

### 탄화수소 오일

| 오일명 | Required HLB | 비고 |
|--------|-------------|------|
| Mineral Oil (Light) | 10-12 | 파라핀계 |
| Mineral Oil (Heavy) | 10.5 | 파라핀계 |
| Petrolatum | 7-8 | 바셀린 |
| Microcrystalline Wax | 9-10 | |
| Paraffin Wax | 10 | |
| Squalane | 10-11 | |
| Squalene | 11 | |

### 식물성 오일

| 오일명 | Required HLB | 비고 |
|--------|-------------|------|
| Jojoba Oil | 6-7 | 왁스 에스테르 |
| Argan Oil | 7 | |
| Sweet Almond Oil | 7 | |
| Avocado Oil | 7 | |
| Olive Oil | 7 | |
| Coconut Oil | 8 | |
| Sunflower Oil | 7 | |
| Grapeseed Oil | 7 | |
| Rosehip Oil | 7-8 | |
| Castor Oil | 14 | 친수성 높음 |
| Hemp Seed Oil | 7 | |
| Macadamia Oil | 6-7 | |

### 에스테르류

| 오일명 | Required HLB | 비고 |
|--------|-------------|------|
| Isopropyl Myristate | 11.5 | IPM |
| Isopropyl Palmitate | 11.5 | IPP |
| Cetyl Palmitate | 10 | |
| Cetyl Esters | 10 | 합성 왁스 |
| Decyl Oleate | 6 | |
| Diisopropyl Adipate | 8 | |
| Ethylhexyl Palmitate | 10-11 | |
| Caprylic/Capric Triglyceride | 5 | MCT 오일 |
| C12-15 Alkyl Benzoate | 13 | |

### 지방 알코올

| 오일명 | Required HLB | 비고 |
|--------|-------------|------|
| Cetyl Alcohol | 15-16 | Co-emulsifier |
| Stearyl Alcohol | 15-16 | Co-emulsifier |
| Cetearyl Alcohol | 15-16 | 혼합물 |
| Behenyl Alcohol | 15 | |

### 실리콘류

| 오일명 | Required HLB | 비고 |
|--------|-------------|------|
| Dimethicone (Low MW) | 5 | 100 cSt |
| Dimethicone (High MW) | 7-8 | 350 cSt |
| Cyclomethicone | 4-5 | 휘발성 |
| Cyclopentasiloxane | 4-5 | D5 |
| Dimethiconol | 8-10 | |
| Phenyl Trimethicone | 7 | |

## 유화제 HLB 데이터베이스

### Span 시리즈 (소르비탄 에스테르)

| 유화제 | INCI명 | HLB | 용도 |
|--------|--------|-----|------|
| Span 20 | Sorbitan Laurate | 8.6 | O/W (보조) |
| Span 40 | Sorbitan Palmitate | 6.7 | W/O |
| Span 60 | Sorbitan Stearate | 4.7 | W/O |
| Span 65 | Sorbitan Tristearate | 2.1 | W/O |
| Span 80 | Sorbitan Oleate | 4.3 | W/O |
| Span 85 | Sorbitan Trioleate | 1.8 | W/O |

### Tween 시리즈 (폴리소르베이트)

| 유화제 | INCI명 | HLB | 용도 |
|--------|--------|-----|------|
| Tween 20 | Polysorbate 20 | 16.7 | 가용화 |
| Tween 40 | Polysorbate 40 | 15.6 | O/W |
| Tween 60 | Polysorbate 60 | 14.9 | O/W |
| Tween 65 | Polysorbate 65 | 10.5 | O/W |
| Tween 80 | Polysorbate 80 | 15.0 | O/W, 가용화 |
| Tween 85 | Polysorbate 85 | 11.0 | O/W |

### Brij 시리즈 (폴리옥시에틸렌 알코올)

| 유화제 | INCI명 | HLB | 용도 |
|--------|--------|-----|------|
| Brij 30 | Laureth-4 | 9.7 | O/W |
| Brij 35 | Laureth-23 | 16.9 | 가용화 |
| Brij 52 | Ceteth-2 | 5.3 | W/O |
| Brij 56 | Ceteth-10 | 12.9 | O/W |
| Brij 58 | Ceteth-20 | 15.7 | O/W |
| Brij 72 | Steareth-2 | 4.9 | W/O |
| Brij 76 | Steareth-10 | 12.4 | O/W |
| Brij 78 | Steareth-20 | 15.3 | O/W |
| Brij 93 | Oleth-2 | 4.9 | W/O |
| Brij 98 | Oleth-20 | 15.3 | O/W |

### 기타 비이온 유화제

| 유화제 | INCI명 | HLB | 용도 |
|--------|--------|-----|------|
| Emulsifying Wax NF | Cetearyl Alcohol (and) Polysorbate 60 | 8-9 | O/W |
| Glyceryl Stearate | Glyceryl Stearate | 3.8 | Co-emulsifier |
| Glyceryl Stearate SE | Glyceryl Stearate (and) Sodium Stearate | 5.8 | O/W |
| PEG-100 Stearate | PEG-100 Stearate | 18.8 | 가용화 |
| Ceteareth-20 | Ceteareth-20 | 15.2 | O/W |
| Ceteareth-6 | Ceteareth-6 | 9.6 | O/W |
| Glyceryl Oleate | Glyceryl Oleate | 3.5 | W/O, Co-emulsifier |
| Sucrose Stearate | Sucrose Stearate | 15 | O/W, 천연 |
| Sucrose Palmitate | Sucrose Palmitate | 15 | O/W, 천연 |

### 이온성 유화제

| 유화제 | INCI명 | HLB | 용도 |
|--------|--------|-----|------|
| Sodium Lauryl Sulfate | Sodium Lauryl Sulfate | 40 | 세정 |
| Sodium Laureth Sulfate | Sodium Laureth Sulfate | 40 | 세정 |
| Sodium Cetearyl Sulfate | Sodium Cetearyl Sulfate | 20+ | O/W |
| Sodium Stearoyl Lactylate | Sodium Stearoyl Lactylate | 10-12 | O/W, 식품용 |
| Stearic Acid (neutralized) | Sodium Stearate | 17 | O/W (비누화) |

## 유화제 블렌딩

### 블렌딩 공식

두 유화제의 혼합 HLB:
```
HLB_mix = (W_A × HLB_A + W_B × HLB_B) / (W_A + W_B)

W_A, W_B = 각 유화제의 중량
HLB_A, HLB_B = 각 유화제의 HLB
```

### 목표 HLB를 위한 블렌딩 비율

```python
def calculate_blend_ratio(target_hlb, hlb_low, hlb_high):
    """
    목표 HLB를 위한 두 유화제 블렌딩 비율 계산

    Args:
        target_hlb: 목표 HLB
        hlb_low: 낮은 HLB 유화제의 HLB
        hlb_high: 높은 HLB 유화제의 HLB

    Returns:
        (high_ratio, low_ratio): 각 유화제의 비율 (합계 1.0)
    """
    if target_hlb < hlb_low or target_hlb > hlb_high:
        raise ValueError("목표 HLB가 블렌딩 가능 범위 밖입니다")

    high_ratio = (target_hlb - hlb_low) / (hlb_high - hlb_low)
    low_ratio = 1 - high_ratio

    return (high_ratio, low_ratio)
```

### 예시: HLB 10.5 달성

```
유화제: Span 60 (HLB 4.7) + Tween 60 (HLB 14.9)
목표: HLB 10.5

계산:
Tween 60 비율 = (10.5 - 4.7) / (14.9 - 4.7) = 0.569 (56.9%)
Span 60 비율 = 1 - 0.569 = 0.431 (43.1%)

검증:
HLB_mix = 0.569 × 14.9 + 0.431 × 4.7 = 8.48 + 2.03 = 10.5 ✓
```

## Required HLB 계산

### 오일 혼합물의 Required HLB

```python
def calculate_required_hlb(oils):
    """
    오일 혼합물의 Required HLB 계산

    Args:
        oils: [{"name": str, "percent": float, "required_hlb": float}, ...]

    Returns:
        float: 혼합물의 Required HLB
    """
    total_weight = sum(oil["percent"] for oil in oils)
    weighted_hlb = sum(oil["percent"] * oil["required_hlb"] for oil in oils)

    return weighted_hlb / total_weight
```

### 예시: 복합 오일상

```
오일상 구성:
- Mineral Oil: 8% (Required HLB: 10.5)
- Jojoba Oil: 3% (Required HLB: 6.5)
- Cetyl Alcohol: 2% (Required HLB: 15.5)

Required HLB = (8 × 10.5 + 3 × 6.5 + 2 × 15.5) / (8 + 3 + 2)
             = (84 + 19.5 + 31) / 13
             = 134.5 / 13
             = 10.35
```

## 유화제 사용량 가이드라인

### 일반적인 사용량

| 제품 유형 | 오일상 % | 유화제 사용량 |
|----------|---------|--------------|
| 로션 | 10-20% | 오일상의 15-20% |
| 크림 | 20-35% | 오일상의 15-20% |
| 콜드크림 | 35-50% | 오일상의 10-15% |
| W/O 크림 | 30-60% | 오일상의 8-15% |

### 최적화 접근법

1. **HLB 스캔**: 계산된 Required HLB ± 2 범위에서 0.5 간격으로 테스트
2. **농도 최적화**: 안정한 에멀전이 형성되는 최소 농도 탐색
3. **Co-emulsifier**: Cetyl/Stearyl Alcohol 추가로 안정성 향상

## 주의사항

### HLB 시스템의 한계

1. **온도 의존성**: POE 계열은 온도에 따라 HLB 변화
   - Cloud point 근처에서 유화 불안정
   - 일반적으로 온도↑ → HLB↓ (비이온)

2. **전해질 영향**: 염 첨가 시 HLB 변화
   - 양이온성 계면활성제: 영향 적음
   - 비이온 계면활성제: 영향 있음

3. **pH 영향**: 이온성 유화제는 pH에 민감
   - Stearic acid: pH > 9에서 비누화되어 유화

4. **유화 타입**: W/O와 O/W의 경계는 명확하지 않음
   - HLB 8-10 범위는 불안정한 전이 구간

### 실험적 검증 권장

- 계산값은 시작점, 실제 테스트로 최적화
- 안정성 테스트: 원심분리, 온도 사이클, 장기 보관
- 크림화 또는 상분리 관찰
