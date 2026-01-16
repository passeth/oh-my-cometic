# Lipinski's Rule of 5 and Skin Penetration

## Overview

Lipinski's Rule of 5 (Ro5)는 원래 경구 약물의 흡수성을 예측하기 위해 개발되었지만, 피부 투과 예측에도 널리 적용됩니다. 이 문서는 경구 vs 경피 적용의 차이점과 화장품 활성 성분에 대한 분석을 다룹니다.

## Original Lipinski Rules

### 경구 생체이용률 예측 (1997)

Christopher Lipinski가 Pfizer에서 개발한 규칙:

```
좋은 경구 흡수 가능성 조건:
1. 분자량 (MW) ≤ 500 Da
2. 친유성 (log P) ≤ 5
3. 수소결합 공여체 (HBD) ≤ 5
4. 수소결합 수용체 (HBA) ≤ 10

※ 위 조건 중 2개 이상 위반 시 흡수 불량 가능성 높음
```

### Rule of 5의 명명 유래
- 모든 기준값이 5 또는 5의 배수 (5, 10, 500)
- 기억하기 쉬운 경험 법칙

## Application to Skin Penetration

### 경구 vs 경피 차이점

| 파라미터 | 경구 최적 | 경피 최적 | 차이 원인 |
|---------|----------|----------|----------|
| **MW** | < 500 | < 500 (이상: < 300) | 각질층 통과 더 제한적 |
| **log P** | < 5 | 1 ~ 3 | 친수/친유층 모두 통과 필요 |
| **HBD** | < 5 | < 3 | 지질 장벽 친화성 |
| **HBA** | < 10 | < 5 | 극성 감소 필요 |
| **PSA** | < 140 Å² | < 60 Å² | 각질층 지질 투과 |

### 경피 투과 최적화 규칙

Bos & Meinardi (2000)의 "500 Dalton Rule"을 포함한 경피 최적 조건:

```
이상적 경피 투과 조건:
1. 분자량 < 500 Da (이상적: 100-300 Da)
2. 친유성 1 < log P < 3 (이상적: 1.5-2.5)
3. 수소결합 공여체 < 3
4. 수소결합 수용체 < 5
5. 극성 표면적 < 60 Å²
6. 회전 가능 결합 < 5
7. 융점 < 200°C
```

## Parameter Analysis

### 1. 분자량 (Molecular Weight)

**피부 투과에서의 역할:**
- 확산 계수에 반비례
- 각질층의 "분자체(molecular sieve)" 효과

**분자량별 투과 특성:**
| MW 범위 | 투과 가능성 | 예시 성분 |
|---------|-----------|----------|
| < 150 Da | 매우 높음 | 카페인 (194), 요소 (60) |
| 150-300 Da | 높음 | 살리실산 (138), 레티놀 (286) |
| 300-500 Da | 중간 | 트레티노인 (300), 히드로코르티손 (362) |
| 500-1000 Da | 낮음 | 대부분 펩타이드 |
| > 1000 Da | 매우 낮음 | 히알루론산, 콜라겐 |

**500 Da Rule:**
```
MW > 500 Da인 물질은 정상 피부를 투과하기 매우 어려움
- 알레르겐 대부분 < 500 Da
- 치료용 단백질은 특수 전달 시스템 필요
```

### 2. 친유성 (log P)

**피부 투과의 양면성:**
각질층은 지질 장벽이지만, 더 깊은 층은 친수성 → 양쪽 모두와 호환 필요

**log P에 따른 투과 메커니즘:**
```
log P < 0 (친수성):
  - 세포간 수분 채널 통과 시도
  - 각질층에서 크게 저해
  - 예: 아스코르빈산 (log P = -1.85)

log P 0-1 (중간 친수성):
  - 경세포 경로 가능
  - 중간 정도 투과
  - 예: 나이아신아마이드 (log P = -0.37)

log P 1-3 (이상적):
  - 각질층 지질과 친화
  - 생체층에서도 용해
  - 예: 살리실산 (log P = 2.26)

log P 3-5 (친유성):
  - 각질층 빠른 흡수
  - 생체층 진입 지연
  - 예: 레티놀 (log P = 5.68)

log P > 5 (매우 친유성):
  - 각질층에 축적
  - 깊은 층 도달 어려움
  - "reservoir effect"
```

**Parabolic Relationship:**
```
투과 플럭스는 log P에 대해 포물선 관계
최적 log P ≈ 2-3에서 최대 투과
```

### 3. 수소결합 특성

**수소결합 공여체 (HBD):**
- -OH, -NH 그룹
- 물 분자와 강한 상호작용
- 많을수록 지질층 투과 어려움

**수소결합 수용체 (HBA):**
- =O, -O-, -N< 그룹
- 극성 증가 요인
- 적당히 있어야 수용성 확보

**화장품 성분 예시:**
| 성분 | HBD | HBA | 수소결합 영향 |
|-----|-----|-----|-------------|
| 나이아신아마이드 | 1 | 3 | 적당 - 투과 양호 |
| 아스코르빈산 | 4 | 6 | 과다 - 투과 불량 |
| 레티놀 | 1 | 1 | 최소 - 투과 양호 |
| 히알루론산 | 다수 | 다수 | 극단적 - 투과 불가 |

### 4. 극성 표면적 (PSA)

**정의:** 분자 표면 중 극성 원자(O, N)가 차지하는 면적

**피부 투과 기준:**
```
PSA < 60 Å²: 좋은 피부 투과
PSA 60-120 Å²: 중간
PSA > 120 Å²: 불량

비교: 경구 흡수는 PSA < 140 Å² 권장
```

**성분별 PSA:**
| 성분 | PSA (Å²) | 투과 예측 |
|-----|----------|----------|
| 카페인 | 58 | 양호 |
| 나이아신아마이드 | 56 | 양호 |
| 살리실산 | 58 | 양호 |
| 아스코르빈산 | 107 | 불량 |
| 히드로퀴논 | 40 | 양호 |

## Cosmetic Active Analysis

### 높은 투과성 활성 성분

**1. 레티놀 (Retinol)**
```
MW: 286 Da ✓
log P: 5.68 (높지만 작용)
HBD: 1 ✓
HBA: 1 ✓
PSA: 20 Å² ✓

평가: 4/5 규칙 만족
실제: 높은 투과성, 각질층 축적 가능
```

**2. 살리실산 (Salicylic Acid)**
```
MW: 138 Da ✓
log P: 2.26 ✓ (이상적)
HBD: 2 ✓
HBA: 3 ✓
PSA: 58 Å² ✓

평가: 5/5 규칙 만족
실제: 우수한 투과성
```

**3. 카페인 (Caffeine)**
```
MW: 194 Da ✓
log P: -0.07 (낮음)
HBD: 0 ✓
HBA: 6 (경계)
PSA: 58 Å² ✓

평가: 4/5 규칙 만족
실제: 중간 투과성 (log P 보상)
```

### 중간 투과성 활성 성분

**1. 나이아신아마이드 (Niacinamide)**
```
MW: 122 Da ✓
log P: -0.37 (낮음)
HBD: 1 ✓
HBA: 3 ✓
PSA: 56 Å² ✓

평가: 4/5 규칙 만족
실제: 중간 투과성, 친수성으로 제한
전략: 리포좀 봉입으로 개선 가능
```

**2. 하이드로퀴논 (Hydroquinone)**
```
MW: 110 Da ✓
log P: 0.59 ✓
HBD: 2 ✓
HBA: 2 ✓
PSA: 40 Å² ✓

평가: 5/5 규칙 만족
실제: 중간-양호 투과성
```

### 낮은 투과성 활성 성분

**1. 아스코르빈산 (Ascorbic Acid)**
```
MW: 176 Da ✓
log P: -1.85 ✗ (매우 친수성)
HBD: 4 ✗
HBA: 6 (경계)
PSA: 107 Å² ✗

평가: 2/5 규칙 만족
실제: 불량한 투과성
전략: 유도체 사용 (아스코빌팔미테이트 등)
```

**2. 알파-아르부틴 (Alpha-Arbutin)**
```
MW: 272 Da ✓
log P: -1.49 ✗
HBD: 4 (경계)
HBA: 7 ✗
PSA: 119 Å² ✗

평가: 1/5 규칙 만족
실제: 불량한 투과성
전략: 나노에멀전, 이온토포레시스
```

### 투과 불가 활성 성분

**1. 히알루론산 (Hyaluronic Acid)**
```
MW: > 1,000,000 Da ✗ (고분자)
log P: 매우 친수성 ✗
HBD: 다수 ✗
HBA: 다수 ✗
PSA: 매우 큼 ✗

평가: 0/5 규칙 만족
실제: 피부 투과 불가
작용: 표면 보습, 필름 형성
```

**2. 콜라겐 (Collagen)**
```
MW: > 100,000 Da ✗
친수성 아미노산 다수 ✗

평가: 투과 불가
실제: 표면 작용만
마케팅 vs 과학의 간극
```

## Exception Cases

### Lipinski 규칙 위반하지만 투과되는 경우

**1. 사이클로스포린 A (Cyclosporine A)**
```
MW: 1203 Da (규칙 위반)
log P: 2.92

실제: 중간 정도 투과
이유: 고리 구조로 분자 크기 감소 효과
      내부 수소결합으로 극성 감소
```

**2. 비타민 E (Tocopherol)**
```
MW: 431 Da ✓
log P: 12.2 (극단적 친유성, 규칙 위반)

실제: 양호한 피부 투과
이유: 각질층 지질과 높은 친화성
      피부 내 수송 단백질 존재
```

### Lipinski 규칙 만족하지만 투과 불량

**1. 글리신 (Glycine)**
```
MW: 75 Da ✓
log P: -3.21 ✗ (극단적 친수성)
HBD: 2 ✓
HBA: 3 ✓

실제: 불량한 투과
이유: 쯔비터이온 형태로 존재
      극단적 친수성
```

**2. 메트포르민 (Metformin)**
```
MW: 129 Da ✓
log P: -2.64 ✗
HBD: 4 (경계)
HBA: 5 ✓

실제: 불량한 투과
이유: 양이온 형태, 극성 분자
```

## Extended Rules for Cosmetics

### Beyond Rule of 5: 화장품 최적화 규칙

**"Rule of 3" for Optimal Skin Penetration:**
```
1. MW < 300 Da
2. 1 < log P < 3
3. HBD ≤ 3
4. HBA ≤ 5
5. PSA < 60 Å²
6. 융점 < 150°C
7. 수용해도 > 1 mg/mL
```

### 활성 성분 분류 매트릭스

```
                    MW < 300           MW 300-500        MW > 500

log P > 3      | 높은 투과           | 중간 투과         | 각질층 축적
(친유성)       | 레티놀, VitE        | 스테로이드        | 대형 테르펜
               |                     |                   |
1 < log P < 3  | 최적 투과           | 양호 투과         | 전달시스템 필요
(이상적)       | 살리실산, 카페인    | 일부 항산화제     | 펩타이드 유도체
               |                     |                   |
log P < 1      | 중간-낮음           | 낮은 투과         | 투과 불가
(친수성)       | 나이아신아마이드    | 아스코르빈산      | HA, 콜라겐
```

## Practical Guidelines

### 신규 활성 성분 평가 체크리스트

```
□ 분자량 확인: < 500 Da 필수, < 300 Da 권장
□ log P 계산: 1-3 이상적, 0-5 허용
□ 수소결합 특성: HBD < 3, HBA < 5
□ PSA 확인: < 60 Å² 권장
□ 이온화 상태: pH에 따른 변화 고려
□ 융점: 낮을수록 유리
```

### 투과 개선 전략

| 문제점 | 개선 전략 |
|-------|----------|
| MW > 500 | 활성 단편 사용, 프로드러그 |
| log P < 0 | 지질 친화성 유도체, 리포좀 |
| log P > 5 | 사이클로덱스트린 포접, 나노에멀전 |
| HBD > 3 | 에스터화, 내부 수소결합 유도 |
| PSA > 60 | 프로드러그 설계 |

### 유도체 설계 예시

**아스코르빈산 유도체:**
```
원본: 아스코르빈산
  - MW: 176, log P: -1.85
  - 투과: 불량

유도체: 아스코빌팔미테이트
  - MW: 414, log P: 8.9
  - 투과: 양호 (친유성 증가)

유도체: MAP (마그네슘아스코빌포스페이트)
  - MW: 289, log P: -5.0
  - 투과: 중간 (안정성 증가)
```

## Computational Tools

### log P 예측 방법

```python
# 다양한 방법으로 log P 추정
methods = {
    "XLogP3": "가장 정확한 방법 중 하나",
    "ALogP": "atom-based 방법",
    "MLOGP": "Moriguchi 방법",
    "WLogP": "Wildman-Crippen 방법"
}

# RDKit 사용 예시
from rdkit import Chem
from rdkit.Chem import Descriptors

mol = Chem.MolFromSmiles("SMILES_STRING")
log_p = Descriptors.MolLogP(mol)
```

### Lipinski 규칙 검사

[permeability_calc.py](../scripts/permeability_calc.py)의 `check_lipinski_rules()` 함수 참조

## References

1. Lipinski, C.A. et al. (1997). Experimental and computational approaches to estimate solubility and permeability in drug discovery and development settings. *Adv Drug Deliv Rev*, 23(1-3), 3-25.
2. Bos, J.D. & Meinardi, M.M. (2000). The 500 Dalton rule for the skin penetration of chemical compounds and drugs. *Exp Dermatol*, 9(3), 165-169.
3. Veber, D.F. et al. (2002). Molecular properties that influence the oral bioavailability of drug candidates. *J Med Chem*, 45(12), 2615-2623.
4. Ghose, A.K. et al. (1999). A knowledge-based approach in designing combinatorial or medicinal chemistry libraries for drug discovery. *J Comb Chem*, 1(1), 55-68.
