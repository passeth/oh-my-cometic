---
name: concentration-converter
description: 화장품 원료 농도 단위 변환 도구. % (w/w, w/v, v/v), ppm, ppb, mg/g, mg/mL, mg/kg, 몰농도 (M, mM, μM) 간 변환 및 희석 계산을 수행합니다. 활성 성분 농도, 밀도 기반 변환, 희석 배수 계산에 사용됩니다.
allowed-tools: None
license: MIT
metadata:
  skill-author: EVAS Cosmetic
  original-source: K-Dense Inc. (claude-scientific-skills structure)
  version: 1.0.0
  category: cosmetic-helpers
  language: ko
  last-updated: "2025-01-16"
  tags:
    - concentration
    - unit-conversion
    - dilution
    - formulation
    - cosmetic-chemistry
---

# Concentration Converter Skill

## Overview

**Concentration Converter**는 화장품 제형 개발에서 사용되는 다양한 농도 단위 간 변환을 수행하는 도구입니다. 원료 공급사별로 다른 단위로 농도가 표기되는 경우, 규제 기준과 실제 배합량 비교, 희석 계산 등 실무에서 자주 발생하는 농도 변환 작업을 지원합니다.

이 스킬은 다음과 같은 변환을 수행합니다:
- **퍼센트 변환**: % (w/w), % (w/v), % (v/v) 상호 변환
- **ppm/ppb 변환**: ppm ↔ %, ppm ↔ mg/kg, ppb ↔ ppm
- **질량/부피 농도**: mg/g, mg/mL, mg/kg, g/L 변환
- **몰농도**: M, mM, μM 변환 및 질량 농도 ↔ 몰농도 변환
- **희석 계산**: 희석 배수, 최종 농도, 필요 원액량 계산
- **활성 농도**: 원료 내 활성 성분 실제 농도 계산

## When to Use This Skill

- **원료 농도 확인**: 원료 스펙의 농도 단위를 배합 단위로 변환
- **규제 농도 비교**: 식약처/FDA 기준(ppm, %)과 배합량 비교
- **희석액 제조**: 스톡 용액에서 희석액 제조 시 필요량 계산
- **활성 성분 계산**: 원료 내 유효 성분의 실제 배합 농도 산출
- **원가 계산**: 유효 성분 기준 원가 환산
- **안정성 데이터 해석**: 분석 결과와 초기 농도 비교

## Core Capabilities

### 1. 퍼센트 농도 (%, Percent)

퍼센트 농도는 가장 널리 사용되는 표기법이지만, 기준에 따라 의미가 다릅니다.

#### 퍼센트 농도 유형

```
% (w/w) - Weight per Weight (중량 백분율)
  = (용질의 질량 / 용액의 총 질량) × 100
  화장품 배합에서 가장 표준적인 표기

% (w/v) - Weight per Volume (질량/부피 백분율)
  = (용질의 질량 g / 용액의 부피 mL) × 100
  의약품, 주사제에서 주로 사용

% (v/v) - Volume per Volume (부피 백분율)
  = (용질의 부피 / 용액의 총 부피) × 100
  알코올, 향료 등 액체 원료에 사용
```

#### w/w와 w/v 변환

```python
# 밀도(d, g/mL)를 이용한 변환
% (w/v) = % (w/w) × d_solution
% (w/w) = % (w/v) / d_solution

# 예시: 5% 나이아신아마이드 (w/w), 용액 밀도 1.05 g/mL
% (w/v) = 5 × 1.05 = 5.25% (w/v)
```

#### v/v와 w/w 변환

```python
# 용질 밀도(d_solute)와 용액 밀도(d_solution) 필요
% (w/w) = % (v/v) × (d_solute / d_solution)
% (v/v) = % (w/w) × (d_solution / d_solute)

# 예시: 70% 에탄올 (v/v), 에탄올 밀도 0.789 g/mL, 혼합액 밀도 0.87 g/mL
% (w/w) = 70 × (0.789 / 0.87) = 63.5% (w/w)
```

### 2. ppm / ppb 변환

#### 정의

```
ppm (parts per million) = 백만분율
  1 ppm = 1 mg/kg = 1 μg/g = 0.0001%

ppb (parts per billion) = 십억분율
  1 ppb = 1 μg/kg = 1 ng/g = 0.0000001%
  1 ppm = 1000 ppb
```

#### ppm ↔ % 변환

```python
# ppm to %
% = ppm / 10,000

# % to ppm
ppm = % × 10,000

# 예시
# 나이아신아마이드 2% → 20,000 ppm
# 납 10 ppm → 0.001%
```

#### ppm 관련 단위 변환표

| From | To | 변환식 |
|------|-----|--------|
| ppm | % | ÷ 10,000 |
| ppm | mg/kg | × 1 (동일) |
| ppm | mg/g | ÷ 1,000 |
| ppm | mg/L | × d (밀도) |
| ppm | μg/g | × 1 (동일) |
| ppm | ppb | × 1,000 |

### 3. 질량/부피 농도

#### 단위 정의

```
mg/g (밀리그램/그램)
  = 그램당 밀리그램
  = 1000 ppm = 0.1%

mg/mL (밀리그램/밀리리터)
  = 밀리리터당 밀리그램
  = g/L

mg/kg (밀리그램/킬로그램)
  = 킬로그램당 밀리그램
  = ppm (고체/고체 또는 액체/액체)

g/L (그램/리터)
  = 리터당 그램
  = mg/mL
```

#### 변환 공식

```python
# mg/g ↔ %
mg/g = % × 10
% = mg/g / 10

# mg/g ↔ ppm
mg/g = ppm / 1000
ppm = mg/g × 1000

# mg/mL ↔ % (w/v)
mg/mL = % (w/v) × 10
% (w/v) = mg/mL / 10

# mg/mL ↔ mg/g (밀도 d g/mL 필요)
mg/g = mg/mL / d
mg/mL = mg/g × d
```

### 4. 몰농도 (Molar Concentration)

#### 정의

```
M (Molar) = mol/L
  1 M = 1 mol/L = 1000 mM

mM (millimolar) = mmol/L
  1 mM = 0.001 M = 1000 μM

μM (micromolar) = μmol/L
  1 μM = 0.001 mM = 0.000001 M
```

#### 질량 농도 ↔ 몰농도 변환

```python
# 몰농도 (M) = 질량농도 (g/L) / 분자량 (g/mol)
M = (mg/mL × 1000) / MW
M = (% w/v × 10) / MW

# 질량 농도 = 몰농도 × 분자량
mg/mL = M × MW / 1000
% (w/v) = M × MW / 10

# 예시: 나이아신아마이드 (MW = 122.12 g/mol)
# 5% (w/v) → 몰농도?
M = (5 × 10) / 122.12 = 0.409 M = 409 mM
```

#### 화장품 주요 성분 분자량

| 성분 | 분자량 (g/mol) |
|------|----------------|
| Niacinamide | 122.12 |
| Ascorbic Acid | 176.12 |
| Retinol | 286.45 |
| Adenosine | 267.24 |
| Hyaluronic Acid (repeating unit) | ~400 |
| Salicylic Acid | 138.12 |
| Glycolic Acid | 76.05 |
| Lactic Acid | 90.08 |
| Citric Acid | 192.12 |
| Tocopherol (Vitamin E) | 430.71 |

### 5. 희석 계산 (Dilution)

#### 희석 공식

```python
C1 × V1 = C2 × V2

C1: 원액 농도
V1: 원액 부피
C2: 희석 후 농도
V2: 희석 후 총 부피

# 필요 원액량 계산
V1 = (C2 × V2) / C1

# 희석 후 농도 계산
C2 = (C1 × V1) / V2
```

#### 희석 배수

```python
Dilution Factor (DF) = V_final / V_sample = C_original / C_final

# 예시: 10% 원액 → 1% 희석액
DF = 10 / 1 = 10배 희석
V_stock = V_final / DF = 100 mL / 10 = 10 mL 원액 필요
```

#### 연속 희석 (Serial Dilution)

```python
# n번 희석 후 최종 농도
C_final = C_initial / (DF)^n

# 예시: 1:10 희석을 3회 수행
C_final = C_initial / 10^3 = C_initial / 1000
```

### 6. 활성 농도 계산 (Active Concentration)

#### 원료 내 활성 성분 농도

```
실제 활성 농도 = 배합률(%) × 원료 내 활성 성분 비율

예시:
- 원료: 나이아신아마이드 99% (순도)
- 배합률: 5%
- 실제 활성 농도: 5% × 0.99 = 4.95%

예시2:
- 원료: 식물 추출물 (유효 성분 3% 함유)
- 배합률: 2%
- 실제 유효 성분 농도: 2% × 0.03 = 0.06% = 600 ppm
```

#### 희석 원료의 활성 농도

```python
# 원료가 이미 희석된 형태인 경우
# 예: 비타민 C 유도체가 50% 수용액으로 공급

원료 농도 = 50%  (w/w, 수용액 내)
배합률 = 10%
유효 성분 농도 = 10% × 0.50 = 5%
```

#### 복합 원료의 유효 성분 계산

```python
def calculate_active_concentration(
    formula_percent: float,
    active_in_raw_material: float,
    purity: float = 1.0
) -> float:
    """
    복합 원료에서 유효 성분의 실제 농도 계산

    Args:
        formula_percent: 배합률 (%)
        active_in_raw_material: 원료 내 유효 성분 비율 (0-1)
        purity: 순도 (기본값 1.0 = 100%)

    Returns:
        실제 활성 농도 (%)
    """
    return formula_percent * active_in_raw_material * purity
```

## Common Workflows

### Workflow 1: 규제 농도 확인

식약처/FDA 규제 기준과 배합 농도 비교:

```python
# 상황: 제품 내 납(Pb) 함량 규제 확인
# 규제 기준: 납 ≤ 10 ppm (화장품)

# 분석 결과: 0.0005%
납_ppm = 0.0005 × 10000 = 5 ppm
# 결과: 규제 기준(10 ppm) 이하 → 적합

# 상황: 살리실산 wash-off 제품 규제 (최대 2%)
배합률 = 1.5%  # w/w
# 결과: 2% 이하 → 적합
```

### Workflow 2: 원료 스펙 해석

원료 공급사별 다른 단위 표기 통일:

```python
# 원료 A 스펙: 유효 성분 25 mg/g
# 원료 B 스펙: 유효 성분 2.5%
# 원료 C 스펙: 유효 성분 25,000 ppm

# 모두 % 단위로 변환
A: 25 mg/g ÷ 10 = 2.5%
B: 2.5% (그대로)
C: 25,000 ppm ÷ 10,000 = 2.5%

# 결론: 세 원료의 유효 성분 농도는 동일 (2.5%)
```

### Workflow 3: 희석액 제조

스톡 용액에서 작업 용액 제조:

```python
# 상황: 10% 글리콜산 스톡 → 2% 작업 용액 500 mL 필요

C1 = 10%
C2 = 2%
V2 = 500 mL

V1 = (C2 × V2) / C1 = (2 × 500) / 10 = 100 mL

# 제조법:
# 1. 글리콜산 10% 스톡 용액 100 mL 취함
# 2. 정제수로 500 mL까지 메스업
```

### Workflow 4: 유효 성분 농도 계산

복합 원료의 실제 활성 농도 산출:

```python
# 상황: 센텔라 추출물 배합
# 원료 스펙: 아시아티코사이드 40% (지표 성분)
# 배합률: 0.5%

실제_아시아티코사이드 = 0.5% × 0.40 = 0.2%
실제_아시아티코사이드_ppm = 0.2 × 10000 = 2000 ppm

# 효능 발현 농도 확인
# 문헌: 아시아티코사이드 0.1% 이상에서 주름개선 효과
# 결론: 0.2% → 충분한 효능 발현 농도
```

### Workflow 5: 몰농도 기반 비교

다른 물질의 농도를 몰 기준으로 비교:

```python
# AHA 제품에서 글리콜산 vs 젖산 비교
# 목표: 동일한 분자 수(몰수)로 배합

# 글리콜산 5% (w/v), MW = 76.05
M_glycolic = (5 × 10) / 76.05 = 0.657 M

# 젖산도 0.657 M로 맞추려면?
# MW_lactic = 90.08
% w/v = 0.657 × 90.08 / 10 = 5.92%

# 결론: 글리콜산 5%와 동몰 농도 = 젖산 약 6%
```

## Best Practices

### 1. 단위 명확화

```
- 항상 농도 단위 명시 (%, ppm, mg/g 등)
- % 표기 시 w/w, w/v, v/v 구분
- 국제 표준 단위 사용 권장 (SI 단위)
- 문서화 시 변환 과정 기록
```

### 2. 밀도 고려

```
- w/w ↔ w/v 변환 시 밀도 확인 필수
- 농도가 높을수록 용액 밀도 변화 주의
- 온도에 따른 밀도 변화 고려 (특히 오일류)
- 밀도를 모르면 w/w 단위 그대로 사용
```

### 3. 유효 숫자

```
- 입력값의 유효 숫자에 맞춰 결과 표기
- 일반적으로 소수점 2-3자리
- ppm은 정수 또는 소수점 1자리
- 계산 중간에는 전체 정밀도 유지
```

### 4. 검증

```
- 변환 후 역변환으로 확인
- 상식적인 범위 체크 (ppm → % 시 매우 작은 값)
- 여러 경로로 같은 결과 도달하는지 확인
- 단위 차원 분석 (dimensional analysis)
```

### 5. 화장품 특수 고려사항

```
- 화장품 배합은 대부분 w/w 기준
- 활성 성분은 실제 유효 농도로 계산
- 고시 원료는 규제 기준 단위 확인
- 분석 결과와 배합량 비교 시 단위 통일
```

## Reference Files

상세 정보는 아래 참조 문서 확인:

| 파일 | 내용 |
|------|------|
| `references/concentration_units.md` | 농도 단위 상세 정의 및 변환 공식 |
| `references/density_table.md` | 화장품 원료 밀도 데이터베이스 |

## Scripts

| 스크립트 | 기능 |
|---------|------|
| `scripts/converter.py` | 농도 변환 유틸리티 (Python) |

## Troubleshooting

### 문제: % 변환 결과가 예상과 다름

```
원인 1: w/w와 w/v 혼동
해결: 용액 밀도 확인, 단위 유형 명확화

원인 2: 밀도 값 오류
해결: 실제 측정 밀도 사용 또는 문헌값 확인

원인 3: 농도 범위에 따른 밀도 변화
해결: 해당 농도에서의 밀도 데이터 사용
```

### 문제: ppm 계산 혼란

```
원인 1: mg/L와 mg/kg 혼동
해결:
- 고체/고체: ppm = mg/kg
- 액체: ppm ≈ mg/L (밀도 ≈ 1인 경우)
- 정확한 변환: mg/L = ppm × d

원인 2: ppb와 ppm 단위 오류
해결: 1000배 관계 확인 (1 ppm = 1000 ppb)
```

### 문제: 몰농도 변환 오류

```
원인 1: 분자량 오류
해결: 정확한 분자량 확인 (수화물 포함 여부)

원인 2: 단위 불일치
해결: g/L와 mg/mL 구분, MW 단위 확인

원인 3: 해리 고려 미흡
해결: 다양성자산/염기는 해리 상태 고려
```

### 문제: 희석 계산 오차

```
원인 1: 부피 변화 무시
해결: 희석 시 부피 변화 고려 (특히 고농도)

원인 2: 용질 추가 시 부피 계산
해결: "to" vs "with" 구분 (메스업 vs 혼합)

원인 3: 온도에 따른 부피 변화
해결: 동일 온도에서 측정, 또는 온도 보정
```

## Quick Reference

### 변환 빠른 참조표

| From | To | 변환식 |
|------|-----|--------|
| % (w/w) | ppm | × 10,000 |
| ppm | % | ÷ 10,000 |
| % (w/w) | mg/g | × 10 |
| mg/g | % | ÷ 10 |
| ppm | mg/kg | × 1 (동일) |
| ppm | mg/g | ÷ 1,000 |
| % (w/v) | mg/mL | × 10 |
| mg/mL | g/L | × 1 (동일) |
| mM | μM | × 1,000 |
| M | mg/mL | × MW ÷ 1,000 |

### 화장품 농도 범위 가이드

| 성분 유형 | 일반 농도 | 단위 |
|----------|----------|------|
| 유효 성분 (활성) | 0.1 - 10 | % |
| 방부제 | 0.1 - 1 | % |
| 향료 | 0.1 - 2 | % |
| 색소 | 0.001 - 1 | % |
| 중금속 (규제) | < 10 - 20 | ppm |
| 1,4-다이옥산 (불순물) | < 100 | ppm |
| 포름알데히드 (규제) | < 0.2 | % |

## Summary

**concentration-converter** 스킬은 화장품 개발의 농도 단위 변환 도구입니다:

1. **퍼센트 변환**: % (w/w, w/v, v/v) 상호 변환, 밀도 기반 계산
2. **ppm/ppb 변환**: 규제 기준 비교, 미량 성분 농도 환산
3. **질량/부피 농도**: mg/g, mg/mL, g/L 등 단위 간 변환
4. **몰농도**: M, mM, μM 변환, 분자량 기반 계산
5. **희석 계산**: 필요 원액량, 최종 농도, 희석 배수
6. **활성 농도**: 원료 내 유효 성분 실제 배합 농도 계산

단위 변환 시 항상 단위 유형을 명확히 하고, 필요한 경우 밀도 값을 확인하세요.
