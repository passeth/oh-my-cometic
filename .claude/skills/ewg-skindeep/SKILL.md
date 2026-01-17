---
name: ewg-skindeep
description: EWG Skin Deep 화장품 성분 안전성 등급 데이터베이스. 성분별 유해성 점수(1-10), 건강 우려 카테고리, 데이터 신뢰도 확인에 사용. 클린뷰티 제품 개발 및 소비자 커뮤니케이션의 핵심 참조 자료.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - WebFetch
license: MIT
metadata:
  version: "1.0.0"
  category: safety
  region: Global
  language: en
  last-updated: "2025-01-16"
  maintainer: cosmetic-skills
  tags:
    - EWG
    - Skin-Deep
    - safety-rating
    - clean-beauty
    - hazard-assessment
    - ingredient-safety
---

# EWG Skin Deep Skill

EWG(Environmental Working Group) Skin Deep 화장품 성분 안전성 등급 데이터베이스 스킬

## Overview

**EWG Skin Deep**은 미국의 비영리 환경단체 Environmental Working Group에서 운영하는 화장품 성분 안전성 데이터베이스입니다. 90,000개 이상의 화장품 제품과 성분에 대한 건강 위험도 평가를 제공합니다.

이 스킬은 EWG Skin Deep 데이터베이스를 활용하여 성분의 안전성 등급을 조회하고, 잠재적 건강 우려 사항을 확인하며, 클린뷰티 제품 개발에 필요한 정보를 제공합니다.

**데이터베이스 URL**: https://www.ewg.org/skindeep/

### EWG 안전성 등급 체계 (1-10 Scale)

| 등급 | 색상 | 의미 | 설명 |
|------|------|------|------|
| **1-2** | 녹색 (Green) | Low Hazard | 낮은 위험 - 안전한 성분 |
| **3-6** | 노란색 (Yellow) | Moderate Hazard | 중간 위험 - 주의 필요 |
| **7-10** | 빨간색 (Red) | High Hazard | 높은 위험 - 사용 회피 권장 |

## When to Use This Skill

이 스킬은 다음과 같은 상황에서 사용합니다:

- **성분 안전성 확인**: 개별 성분의 EWG 등급 및 우려 사항 조회
- **클린뷰티 제품 개발**: EWG 기준에 부합하는 처방 설계
- **소비자 커뮤니케이션**: 제품 안전성 마케팅 자료 준비
- **처방 검토**: 전체 처방의 안전성 프로파일 평가
- **대체 원료 탐색**: 고위험 성분의 저위험 대안 검색
- **규제 대응**: 클린뷰티 인증 요건 충족 여부 확인

## Core Capabilities

### 1. 안전성 등급 조회 (1-10 Scale)

EWG Skin Deep의 핵심 기능인 Hazard Score 조회:

```python
from ewg_query import EWGClient

client = EWGClient()

# 성분 등급 조회
rating = client.get_rating("NIACINAMIDE")
print(f"등급: {rating.score}")  # 1 (Low Hazard)
print(f"색상: {rating.hazard_level}")  # GREEN

# 다중 성분 일괄 조회
ratings = client.get_ratings(["RETINOL", "OXYBENZONE", "GLYCERIN"])
```

**등급 해석**:

| 등급 범위 | 의미 | 클린뷰티 적합성 |
|-----------|------|-----------------|
| 1-2 (GREEN) | 안전 | 적합 |
| 3-6 (YELLOW) | 중간 | 조건부 적합 (농도/용도 고려) |
| 7-10 (RED) | 위험 | 부적합 (회피 권장) |

### 2. 건강 우려 카테고리 확인

EWG가 평가하는 주요 건강 우려 카테고리:

```python
# 우려 카테고리 조회
concerns = client.get_concerns("OXYBENZONE")
```

**주요 우려 카테고리**:

| 카테고리 | 설명 |
|----------|------|
| **Cancer** | 발암성 (Carcinogenicity) |
| **Developmental & Reproductive Toxicity** | 발달/생식 독성 |
| **Allergies & Immunotoxicity** | 알레르기/면역독성 |
| **Use Restrictions** | 사용 제한 (규제 기관) |
| **Organ System Toxicity (Non-Reproductive)** | 장기 독성 |
| **Endocrine Disruption** | 내분비 교란 |
| **Persistence & Bioaccumulation** | 환경 잔류/생체 축적 |
| **Ecotoxicology** | 생태 독성 |
| **Occupational Hazards** | 직업적 위험 |
| **Irritation (Skin/Eyes/Lungs)** | 자극성 |
| **Contamination Concerns** | 오염 물질 우려 |
| **Biochemical/Cellular Level Changes** | 생화학적/세포 수준 변화 |

### 3. 데이터 신뢰도 확인 (Data Availability)

EWG 등급의 신뢰도를 결정하는 데이터 가용성:

```python
rating = client.get_rating("NIACINAMIDE")
print(f"데이터 가용성: {rating.data_availability}")  # ROBUST
```

**데이터 가용성 등급**:

| 등급 | 의미 | 신뢰도 |
|------|------|--------|
| **None** | 데이터 없음 | 매우 낮음 |
| **Limited** | 제한적 데이터 | 낮음 |
| **Fair** | 보통 수준 데이터 | 중간 |
| **Good** | 충분한 데이터 | 높음 |
| **Robust** | 풍부한 데이터 | 매우 높음 |

**중요**: 데이터 가용성이 낮은 경우, 등급의 신뢰도도 낮을 수 있습니다.

### 4. 성분별 상세 연구 링크

```python
# EWG 성분 상세 페이지 URL
url = client.get_ingredient_url("RETINOL")
# https://www.ewg.org/skindeep/ingredients/706428-RETINOL/

# 참고 연구 자료 링크
studies = client.get_study_references("RETINOL")
```

### 5. 제품 전체 등급 예측

전체 처방의 EWG 등급 예측:

```python
formula = [
    {"inci": "AQUA", "percent": 70.0},
    {"inci": "GLYCERIN", "percent": 5.0},
    {"inci": "NIACINAMIDE", "percent": 4.0},
    {"inci": "PHENOXYETHANOL", "percent": 1.0},
    # ...
]

# 제품 전체 등급 예측
product_rating = client.calculate_product_score(formula)
print(f"제품 예상 등급: {product_rating.score}")
print(f"우려 성분: {product_rating.flagged_ingredients}")
```

## Common Workflows

### Workflow 1: 클린뷰티 처방 검토

EWG 기준에 따른 클린뷰티 적합성 검토:

```
1. 처방 성분 목록 준비
2. 각 성분의 EWG 등급 조회
3. 고위험 성분(7-10) 식별 및 대체 검토
4. 중위험 성분(3-6) 농도 및 용도 검토
5. 제품 전체 등급 계산
6. 클린뷰티 기준 충족 여부 판정
```

```python
def review_clean_beauty_formula(formula):
    client = EWGClient()

    high_risk = []  # 7-10
    moderate_risk = []  # 3-6
    low_risk = []  # 1-2

    for ingredient in formula:
        rating = client.get_rating(ingredient["inci"])
        if rating.score >= 7:
            high_risk.append((ingredient, rating))
        elif rating.score >= 3:
            moderate_risk.append((ingredient, rating))
        else:
            low_risk.append((ingredient, rating))

    return {
        "high_risk": high_risk,
        "moderate_risk": moderate_risk,
        "low_risk": low_risk,
        "clean_beauty_compatible": len(high_risk) == 0
    }
```

### Workflow 2: 마케팅 클레임 준비

EWG 등급 기반 마케팅 문구 작성:

```
1. 제품 전체 EWG 등급 확인
2. EWG Verified 인증 자격 확인
3. 클린뷰티 클레임 작성 가능 여부 판단
4. 성분 안전성 커뮤니케이션 자료 준비
5. 소비자 FAQ 대응 준비
```

**주의사항**:
- EWG 등급을 직접 광고에 사용하려면 EWG 라이선스 필요
- "EWG Verified" 마크 사용 시 별도 인증 프로그램 참여 필요
- 국가별 광고 규제 확인 필수

### Workflow 3: 대체 원료 탐색

고위험 성분의 저위험 대안 검색:

```python
# 고위험 성분 대체 원료 탐색
alternatives = client.find_alternatives(
    ingredient="OXYBENZONE",  # 높은 등급 (8)
    function="UV_FILTER",
    max_score=3  # 등급 3 이하 대안만
)

# 결과:
# - ZINC OXIDE (등급 2)
# - TITANIUM DIOXIDE (등급 2)
```

### Workflow 4: 성분 비교 분석

```python
# 동일 기능 성분 간 안전성 비교
comparison = client.compare_ingredients([
    "OXYBENZONE",      # UV Filter, 등급 8
    "AVOBENZONE",      # UV Filter, 등급 2
    "ZINC OXIDE",      # UV Filter, 등급 2
    "TITANIUM DIOXIDE" # UV Filter, 등급 2
])

for ing in comparison:
    print(f"{ing.inci_name}: 등급 {ing.score}, 우려 {ing.concerns}")
```

## Best Practices

### 1. EWG 등급의 올바른 해석

```
중요 고려사항:
- EWG 등급은 "유해성(Hazard)"을 평가, "위험성(Risk)"은 별개
- 농도와 노출 빈도를 고려한 위험성 평가가 필요
- 규제 기관(FDA, EU SCCS) 평가와 다를 수 있음
- 데이터 가용성(Data Availability) 반드시 확인
```

**Hazard vs Risk**:
- **Hazard (유해성)**: 물질의 고유한 독성 잠재력
- **Risk (위험성)**: 실제 노출 조건에서의 피해 가능성

예: 물도 다량 섭취 시 유해하지만, 일반적 사용에서 위험하지 않음

### 2. 데이터 신뢰도 확인

```
항상 Data Availability 확인:
- NONE/LIMITED: 등급 신뢰도 낮음, 추가 조사 필요
- FAIR: 참고 수준, 다른 자료와 교차 확인 권장
- GOOD/ROBUST: 신뢰도 높음, 의사결정에 활용 가능
```

### 3. EWG 등급의 한계 이해

```
한계점:
1. 미국 중심 평가 (EU/아시아 규제와 차이 가능)
2. 보수적 평가 경향 (안전 마진 크게 설정)
3. 농도 미고려 (고농도 전제 평가)
4. 최신 연구 반영 지연 가능
5. 일부 천연 성분 과대평가 논란
```

### 4. 과학적 맥락에서의 활용

```
권장 접근법:
1. EWG 등급을 유일한 기준으로 사용하지 않음
2. EU SCCS, FDA, CIR 등 규제 기관 평가와 비교
3. 원료 공급업체의 안전성 자료 확인
4. 학술 문헌 교차 검증
5. 실제 배합 농도에서의 안전성 평가
```

### 5. 클린뷰티 마케팅 시 주의사항

```
주의사항:
- "EWG 인증"은 공식 표현 아님 (EWG Verified 별도)
- EWG 등급 수치 직접 표기 시 라이선스 확인
- 경쟁 제품 비방 목적 사용 금지
- 과학적 근거 없는 불안 조장 금지
- 국가별 화장품 광고 규제 준수
```

## Reference Files

| File | Description |
|------|-------------|
| [references/ewg_methodology.md](references/ewg_methodology.md) | EWG 평가 방법론 및 등급 산정 기준 |
| [scripts/ewg_query.py](scripts/ewg_query.py) | Python 쿼리 클라이언트 |

## Related Resources

- **EWG Skin Deep**: https://www.ewg.org/skindeep/
- **EWG Verified Program**: https://www.ewg.org/ewgverified/
- **EWG Methodology**: https://www.ewg.org/skindeep/contents/about-page/
- **CIR (Cosmetic Ingredient Review)**: https://www.cir-safety.org/
- **EU SCCS Opinions**: https://health.ec.europa.eu/scientific-committees/scientific-committee-consumer-safety-sccs_en

## Usage Examples

### 단일 성분 등급 조회
```
"Retinol EWG 등급 알려줘"
-> EWG Skin Deep 등급: 9 (High Hazard, RED)
-> 주요 우려: Developmental & Reproductive Toxicity, Use Restrictions
-> 데이터 가용성: GOOD
```

### 처방 안전성 검토
```
"이 처방의 EWG 등급 검토해줘"
-> 제품 예상 등급: 3 (Moderate Hazard, YELLOW)
-> 우려 성분: Phenoxyethanol (등급 4)
-> 클린뷰티 적합성: 조건부 적합
```

### 대체 원료 탐색
```
"Oxybenzone 대신 사용할 수 있는 저위험 자외선차단제?"
-> Zinc Oxide (등급 2) - 물리적 자외선차단
-> Titanium Dioxide (등급 2) - 물리적 자외선차단
-> Bis-Ethylhexyloxyphenol Methoxyphenyl Triazine (등급 1)
```

## EWG vs 규제 기관 비교

| 성분 | EWG 등급 | EU 규제 | FDA 규제 | 비고 |
|------|----------|---------|----------|------|
| Retinol | 9 (RED) | 제한 (0.3% face) | 허용 | EWG 더 보수적 |
| Oxybenzone | 8 (RED) | 허용 (6%) | 허용 (6%) | 내분비 교란 논란 |
| Phenoxyethanol | 4 (YELLOW) | 허용 (1%) | 허용 | 일반적으로 안전 |
| Parabens | 4-7 | 일부 제한 | 허용 | 논란 있음 |
| Hydroquinone | 9 (RED) | 금지 | OTC 2% | EU 더 엄격 |

## Troubleshooting

### 문제: 성분을 찾을 수 없음
```
원인 1: INCI명 불일치
해결: 정확한 INCI명 확인, 대문자 변환

원인 2: EWG 미등록 성분
해결: 동의어 검색, 유사 성분 참조

원인 3: 새로운 성분
해결: 다른 안전성 DB 참조 (CIR, SCCS)
```

### 문제: 등급 해석 불일치
```
원인: Hazard vs Risk 혼동
해결:
1. 배합 농도 고려
2. 노출 빈도 고려
3. 규제 기관 평가 참조
4. 원료사 안전성 자료 확인
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-01-16 | Initial release with 100+ common ingredients |
