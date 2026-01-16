---
name: kfda-ingredient
description: Korean FDA (MFDS) functional cosmetic ingredient database - 한국 식약처 기능성 화장품 고시원료 데이터베이스
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - WebFetch
license: MIT
metadata:
  version: "1.0.0"
  category: regulatory
  region: Korea
  language: ko
  last-updated: "2025-01-16"
  maintainer: cosmetic-skills
  tags:
    - KFDA
    - MFDS
    - functional-cosmetics
    - whitening
    - anti-wrinkle
    - sunscreen
    - Korean-regulation
---

# KFDA Ingredient Skill

한국 식품의약품안전처(MFDS) 기능성 화장품 고시원료 데이터베이스 스킬

## Overview

이 스킬은 한국 식약처에서 고시한 기능성 화장품 원료 정보를 제공합니다. 기능성 화장품은 「화장품법」 제2조에 따라 피부의 미백, 주름개선, 자외선차단 등의 기능을 가진 화장품을 의미하며, 고시된 원료를 사용할 경우 간소화된 심사(보고)로 제품 출시가 가능합니다.

### 기능성 화장품 3대 유형

1. **미백 기능성** (22종 고시원료)
   - 피부에 멜라닌 색소가 침착하는 것을 방지하여 기미, 주근깨 등의 생성을 억제

2. **주름개선 기능성** (6종 고시원료)
   - 피부에 탄력을 주어 피부의 주름을 완화 또는 개선

3. **자외선차단 기능성** (28종 고시원료)
   - 강한 햇볕을 방지하여 피부를 곱게 태워주거나 자외선으로부터 피부를 보호

## When to Use

이 스킬은 다음과 같은 상황에서 사용합니다:

- **기능성 원료 검색**: 특정 효능의 고시원료 목록 조회
- **고시 농도 확인**: 원료별 허용 배합 농도 범위 확인
- **기능성 심사 준비**: 보고/심사에 필요한 자료 요건 파악
- **처방 검토**: 기능성 원료 배합 적합성 검증
- **제품 기획**: 기능성 화장품 개발 시 원료 선정
- **규제 대응**: 식약처 규제 요건 충족 여부 확인

## Core Capabilities

### 1. 미백 기능성 원료 검색 (22종)

대표 원료:
- 나이아신아마이드 (Niacinamide) - 2~5%
- 알부틴 (Arbutin) - 2~5%
- 비타민C 유도체 (다양한 종류별 고시 농도)
- 닥나무추출물, 감초추출물 등 천연유래 원료

상세 정보: [references/whitening_ingredients.md](references/whitening_ingredients.md)

### 2. 주름개선 기능성 원료 검색 (6종)

대표 원료:
- 레티놀 (Retinol) - 2,500 IU/g
- 아데노신 (Adenosine) - 0.04%
- 폴리에톡실레이티드레틴아마이드 - 0.05~0.1%

상세 정보: [references/wrinkle_ingredients.md](references/wrinkle_ingredients.md)

### 3. 자외선차단 원료 검색 (28종)

유기 자외선차단제:
- 옥시벤존, 아보벤존, 옥토크릴렌 등

무기 자외선차단제:
- 징크옥사이드 (최대 25%)
- 티타늄디옥사이드 (최대 25%)

상세 정보: [references/sunscreen_ingredients.md](references/sunscreen_ingredients.md)

### 4. 고시 농도 범위 확인

각 원료별로 식약처에서 고시한 배합 농도 범위를 확인할 수 있습니다:
- 최소 유효 농도
- 최대 허용 농도
- 제형별 적용 기준

### 5. 배합 금지 성분 확인

기능성 원료와 함께 사용할 수 없는 성분 조합:
- 레티놀과 산성 성분 (AHA/BHA)
- 나이아신아마이드와 순수 비타민C (안정성 이슈)
- 자외선차단제 간 상호작용

### 6. 기능성 심사 자료 요건

**보고 대상** (고시원료 사용):
- 기능성화장품 심사 보고서
- 기준 및 시험방법 관련 자료
- 기능성 입증 자료 (생략 가능)

**심사 대상** (고시 외 원료 사용):
- 안전성 자료
- 유효성 자료
- 기준 및 시험방법
- 안정성 시험 자료

## Common Workflows

### Workflow 1: 기능성 제품 기획

```
1. 목표 기능성 유형 결정 (미백/주름개선/자외선차단)
2. 고시원료 목록 검색
3. 원료별 특성 비교 (효능, 안정성, 가격)
4. 배합 농도 결정 (고시 범위 내)
5. 배합 금지 성분 확인
6. 처방 초안 작성
```

### Workflow 2: 처방 규제 검토

```
1. 사용된 기능성 원료 확인
2. 배합 농도 고시 기준 충족 여부 확인
3. 복합 기능성 해당 여부 확인
4. 필요 심사 유형 결정 (보고/심사)
5. 준비 서류 목록 작성
```

### Workflow 3: 복합 기능성 제품 개발

```
1. 복합 기능성 유형 결정
   - 미백 + 주름개선
   - 미백 + 자외선차단
   - 자외선차단 + 주름개선
   - 3종 복합
2. 각 유형별 고시원료 선정
3. 원료 간 상호작용 검토
4. 통합 농도 기준 확인
5. 복합 기능성 심사 요건 파악
```

## Best Practices

### 1. 최신 고시 확인

```
- 식약처 고시는 수시로 개정됨
- 신규 원료 추가 및 농도 기준 변경 가능
- 최신 「기능성화장품 기준 및 시험방법」 확인 필수
- 식약처 의약품안전나라 (nedrug.mfds.go.kr) 참조
```

### 2. 복합 기능성 주의사항

```
- 각 기능성별 원료가 모두 고시 범위 내여야 함
- 원료 간 안정성 문제 검토 필요
- 복합 효능 표시 시 각각의 기능성 입증 필요
- 자외선차단 포함 시 SPF/PA 측정 필수
```

### 3. 안정성 고려사항

```
- 레티놀: 광안정성, 산소 민감성 고려
- 비타민C 유도체: pH 의존적 안정성
- 자외선차단제: 광안정화제 배합 검토
- 보존 조건 및 유효기간 설정
```

### 4. 표시 광고 주의

```
- 고시 농도 미만 시 기능성 표시 불가
- 과대 광고 금지 (의약품적 효능 표현 불가)
- 기능성 화장품 문구 표시 의무
- 자외선차단지수 정확한 표기
```

## Reference Files

| File | Description |
|------|-------------|
| [references/functional_ingredients.md](references/functional_ingredients.md) | 기능성 화장품 개요 및 법적 정의 |
| [references/whitening_ingredients.md](references/whitening_ingredients.md) | 미백 기능성 고시원료 22종 상세 |
| [references/wrinkle_ingredients.md](references/wrinkle_ingredients.md) | 주름개선 기능성 고시원료 6종 상세 |
| [references/sunscreen_ingredients.md](references/sunscreen_ingredients.md) | 자외선차단 기능성 원료 28종 상세 |
| [scripts/kfda_query.py](scripts/kfda_query.py) | Python 쿼리 클라이언트 |

## Related Resources

- **식약처 의약품안전나라**: https://nedrug.mfds.go.kr
- **기능성화장품 기준 및 시험방법**: 식약처 고시
- **화장품법**: 법률 제17250호
- **화장품법 시행규칙**: 총리령

## Usage Examples

### 미백 원료 검색
```
"나이아신아마이드 고시 농도 알려줘"
→ 미백 기능성: 2~5% (wash-off 포함 전 제형)
```

### 복합 기능성 확인
```
"레티놀과 나이아신아마이드 함께 사용 가능?"
→ 가능, 미백+주름개선 복합 기능성 제품
→ 각각 고시 농도 범위 내 배합 필요
```

### 자외선차단 원료 조회
```
"징크옥사이드 최대 배합 농도?"
→ 최대 25% (제품 전체 기준)
→ 나노 원료 사용 시 별도 표시 필요
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-01-16 | Initial release with 56 functional ingredients |
