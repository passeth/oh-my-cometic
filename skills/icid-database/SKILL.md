---
name: icid-database
description: International Cosmetic Ingredient Dictionary (ICID/INCI Dictionary) - PCPC 공식 화장품 성분 데이터베이스. INCI명 등록, 모노그래프 조회, CAS 번호 연동, 성분 표준화의 권위있는 출처.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - WebFetch
license: MIT
metadata:
  version: "1.0.0"
  category: cosmetic-databases
  region: Global
  language: en
  last-updated: "2025-01-16"
  maintainer: cosmetic-skills
  tags:
    - ICID
    - INCI
    - PCPC
    - ingredient-nomenclature
    - CAS-number
    - monograph
    - cosmetic-database
---

# ICID Database Skill

International Cosmetic Ingredient Dictionary (ICID) - PCPC 공식 INCI 데이터베이스 스킬

## Overview

**ICID (International Cosmetic Ingredient Dictionary)**는 **PCPC (Personal Care Products Council)**에서 관리하는 화장품 성분 국제 표준 명명 체계의 공식 데이터베이스입니다. 전 세계 화장품 라벨에 사용되는 INCI(International Nomenclature of Cosmetic Ingredients) 명명 체계의 유일한 권위 있는 출처입니다.

### 핵심 정보

| 항목 | 내용 |
|------|------|
| **공식 명칭** | International Cosmetic Ingredient Dictionary and Handbook |
| **운영 기관** | PCPC (Personal Care Products Council) |
| **웹사이트** | https://www.personalcarecouncil.org/resources/inci/ |
| **등록 성분 수** | 30,000+ (2024년 기준) |
| **접근 방식** | 유료 구독 (연간 라이선스) |
| **업데이트 주기** | 분기별 (온라인) / 연간 (인쇄본) |

### ICID vs CosIng 비교

| 특성 | ICID (PCPC) | CosIng (EU) |
|------|-------------|-------------|
| **관리 기관** | PCPC (미국) | 유럽위원회 |
| **법적 지위** | 업계 표준 | EU 법적 데이터베이스 |
| **등록/신청** | INCI 신규 등록 가능 | 기존 명칭만 조회 |
| **접근 비용** | 유료 구독 | 무료 공개 |
| **규제 정보** | 명명만 (규제 정보 없음) | Annex 규제 포함 |
| **업데이트** | 분기별 | 수시 업데이트 |

## When to Use This Skill

이 스킬은 다음 상황에서 사용합니다:

### ICID 필수 사용 케이스

1. **INCI명 공식 확인**
   - 정확한 INCI 표기 확인 (대소문자, 공백, 하이픈)
   - CosIng에 없는 최신 등록 성분 조회

2. **신규 INCI명 등록**
   - 새로운 화장품 원료의 INCI명 신청
   - 기존에 없는 성분의 공식 명칭 요청

3. **모노그래프 조회**
   - 성분의 정의, 동의어, 상용명 확인
   - CAS 번호 연동 정보 확인

4. **INCI 명명 규칙 확인**
   - 식물 유래 성분 명명법
   - 합성 성분 명명 규칙
   - 복합 성분/혼합물 표기법

### ICID 권장 사용 케이스

- 처방전 작성 시 공식 INCI명 확인
- 라벨 표기 검수
- 수출용 제품의 성분 명칭 표준화
- 공급업체 원료 스펙 시트 검증

## Core Capabilities

### 1. INCI명 조회 (INCI Name Lookup)

ICID에서 성분을 검색하는 방법:

```python
# WebFetch를 통한 PCPC 웹사이트 조회
# 구독 회원만 전체 정보 접근 가능

# 기본 검색 URL 구조
search_url = "https://incidecoder.com/search/{ingredient_name}"
# 또는 무료 대안
cosing_url = "https://ec.europa.eu/growth/tools-databases/cosing/"
cosmily_url = "https://www.cosmily.com/ingredients/{ingredient_name}"
```

### 2. 모노그래프 구조 (Monograph Structure)

ICID 모노그래프에 포함된 정보:

```
┌─────────────────────────────────────────────────────────────┐
│  MONOGRAPH ENTRY                                            │
├─────────────────────────────────────────────────────────────┤
│  INCI Name: NIACINAMIDE                                     │
│                                                             │
│  CAS Numbers:                                               │
│    - 98-92-0                                                │
│                                                             │
│  EINECS/ELINCS:                                            │
│    - 202-713-4                                              │
│                                                             │
│  Definition:                                                │
│    Niacinamide is the amide of Nicotinic Acid.             │
│                                                             │
│  Chemical Name:                                             │
│    3-Pyridinecarboxamide                                    │
│                                                             │
│  Trade Names:                                               │
│    - Vitamin B3                                             │
│    - Nicotinamide                                           │
│                                                             │
│  References:                                                │
│    - Original registration date                             │
│    - Amendment history                                      │
│                                                             │
│  Functions (from other sources):                            │
│    - Skin conditioning                                      │
│    - Smoothing                                              │
└─────────────────────────────────────────────────────────────┘
```

### 3. CAS 번호 연동 (CAS Number Correlation)

ICID는 각 INCI명에 대해 관련 CAS 번호를 제공합니다:

| INCI Name | CAS Number(s) | Notes |
|-----------|---------------|-------|
| NIACINAMIDE | 98-92-0 | 단일 CAS |
| HYALURONIC ACID | 9004-61-9 | 단일 CAS |
| TOCOPHEROL | 59-02-9, 10191-41-0 | 복수 CAS (이성질체) |
| RETINOL | 68-26-8, 11103-57-4 | 복수 CAS (형태별) |

```python
# CAS 번호 검증 알고리즘
def validate_cas_number(cas: str) -> bool:
    """
    CAS 번호 형식 및 체크섬 검증

    형식: XXXXXXX-XX-X
    체크섬: 마지막 숫자
    """
    import re
    match = re.match(r'^(\d{2,7})-(\d{2})-(\d)$', cas)
    if not match:
        return False

    digits = match.group(1) + match.group(2)
    check_digit = int(match.group(3))

    total = sum(int(d) * (len(digits) - i) for i, d in enumerate(digits))
    return total % 10 == check_digit
```

### 4. INCI 등록 프로세스 (Registration Process)

새로운 INCI명 등록 절차:

```
┌────────────────────────────────────────────────────────────────┐
│  INCI NAME REGISTRATION PROCESS                                │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Step 1: Application Submission                                │
│  ─────────────────────────────────                            │
│  - PCPC 회원사를 통해 신청                                      │
│  - 필수 정보: 화학명, CAS 번호, 제조법, 용도                     │
│  - 신청비: 약 $2,000-5,000                                     │
│                                                                │
│  Step 2: Technical Review                                      │
│  ─────────────────────────                                     │
│  - PCPC 기술 위원회 검토                                        │
│  - 명명 규칙 적합성 확인                                        │
│  - 기존 등록명과 중복 여부 확인                                  │
│                                                                │
│  Step 3: Name Assignment                                       │
│  ─────────────────────────                                     │
│  - 검토 통과 시 INCI명 부여                                     │
│  - Dictionary에 추가                                           │
│  - 처리 기간: 4-8주                                            │
│                                                                │
│  Step 4: Publication                                           │
│  ────────────────────                                          │
│  - 분기별 온라인 업데이트                                       │
│  - 연간 인쇄본 발행                                             │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### 5. 구독 등급 및 접근 수준 (Subscription Levels)

| 구독 유형 | 연간 비용 (USD) | 접근 범위 |
|----------|----------------|----------|
| **Non-Member Online** | ~$500-1,000 | 온라인 검색만 |
| **Member Online** | 회원비 포함 | 전체 온라인 + PDF |
| **Print + Online** | ~$800-1,500 | 인쇄본 + 온라인 |
| **Corporate License** | 협의 | 다중 사용자, API |

### 6. 무료 대안 데이터베이스 (Free Alternatives)

ICID 구독이 없는 경우 활용 가능한 무료 소스:

#### CosIng (EU 공식)
```
URL: https://ec.europa.eu/growth/tools-databases/cosing/
특징:
  - 무료 공개
  - EU 규제 정보 포함 (Annex II-VI)
  - 30,000+ 성분
  - INCI명 표준화 정보

제한:
  - 최신 등록명은 ICID보다 늦게 반영
  - 일부 상용명 정보 부족
```

#### Cosmily
```
URL: https://www.cosmily.com/ingredients/
특징:
  - 무료 검색
  - 사용자 친화적 인터페이스
  - EWG 등급 정보
  - 제품 분석 기능

제한:
  - 비공식 데이터베이스
  - 정확도 검증 필요
```

#### INCIDecoder
```
URL: https://incidecoder.com/
특징:
  - 무료 검색
  - 성분 분석 정보
  - 제품 성분 리뷰

제한:
  - 비공식 소스
  - 일부 성분 정보 불완전
```

## Common Workflows

### Workflow 1: INCI명 공식 확인

```
1. 원료 상품명/화학명 확보
   └─ 예: "Nicotinamide", "Vitamin B3"

2. ICID/CosIng에서 검색
   └─ 정확한 INCI명 확인: "NIACINAMIDE"

3. CAS 번호 교차 검증
   └─ CAS: 98-92-0 확인

4. 라벨 표기용 최종 확정
   └─ 대문자, 공백, 하이픈 확인
```

### Workflow 2: 신규 원료 INCI 등록

```
1. 기존 INCI명 존재 여부 확인
   └─ ICID, CosIng 검색

2. 미등록 시 PCPC 신청
   └─ 회원사 통해 신청서 제출

3. 필요 정보 준비
   └─ 화학명, CAS, 제조법, 용도
   └─ 안전성 데이터 (필요시)

4. 임시 명칭 사용 (등록 전)
   └─ 화학명 또는 상품명 사용
   └─ "등록 중" 명시
```

### Workflow 3: 라벨 표기 검수

```
1. 처방전 INCI 목록 추출
2. 각 성분 ICID/CosIng 검증
3. 표기 오류 체크:
   - 대소문자
   - 공백/하이픈
   - 구 명칭 → 신 명칭 변경 여부
4. 수정 목록 작성
```

## Best Practices

### 1. INCI명 표기 원칙

```
DO:
  ✓ 항상 대문자 사용: NIACINAMIDE
  ✓ 공백 유지: HYALURONIC ACID
  ✓ 공식 명칭 사용: SODIUM HYALURONATE
  ✓ 정기적 업데이트 확인

DON'T:
  ✗ 소문자 사용: niacinamide
  ✗ 임의 축약: HA (Hyaluronic Acid)
  ✗ 상품명 사용: Vitamin B3
  ✗ 비공식 명칭: Niacin Amide
```

### 2. 다중 데이터베이스 활용

```python
# 권장 검증 순서
VERIFICATION_ORDER = [
    "ICID (PCPC)",      # 1순위: 공식 출처
    "CosIng (EU)",      # 2순위: 무료 공식 데이터
    "Cosmily",          # 3순위: 보조 참조
    "INCIDecoder",      # 4순위: 추가 정보
]
```

### 3. CAS 번호 교차 검증

```
한 성분 = 복수 CAS 가능
  └─ 이성질체, 수화물, 염 형태별로 다른 CAS

CAS 검증 시 주의사항:
  - INCI와 1:N 매핑 가능
  - 공급업체 CoA의 CAS 확인
  - CosIng에서 교차 검증
```

### 4. 등록 대기 성분 처리

```
신규 원료 (INCI 미등록) 임시 표기 옵션:

Option 1: 화학명 사용
  └─ "3-Pyridinecarboxamide" (INCI 등록 전)

Option 2: 상품명 + 설명
  └─ "Proprietary Ingredient ABC (pending INCI)"

Option 3: 일반 카테고리
  └─ "Plant Extract" (세부 명칭 대기 중)
```

## Reference Files

| File | Description |
|------|-------------|
| [references/inci_structure.md](references/inci_structure.md) | INCI Dictionary 구조 및 명명 규칙 |
| [references/pcpc_guidelines.md](references/pcpc_guidelines.md) | PCPC 명명 가이드라인 상세 |
| [scripts/inci_lookup.py](scripts/inci_lookup.py) | INCI명 조회 유틸리티 |

## Related Resources

### 공식 리소스

- **PCPC INCI Dictionary**: https://www.personalcarecouncil.org/resources/inci/
- **CosIng Database**: https://ec.europa.eu/growth/tools-databases/cosing/
- **CAS Registry**: https://www.cas.org/

### 무료 대안

- **Cosmily**: https://www.cosmily.com/
- **INCIDecoder**: https://incidecoder.com/
- **CosDNA**: https://cosdna.com/
- **화해 (한국)**: https://www.hwahae.co.kr/

### 관련 스킬

- `cosing-database`: EU CosIng 데이터베이스 스킬
- `inci-converter`: INCI명 변환 스킬
- `regulatory-compliance`: 규제 준수 확인 스킬

## Usage Examples

### INCI명 확인
```
"Vitamin C의 공식 INCI명이 뭐야?"
→ ASCORBIC ACID (순수 비타민C)
→ 유도체별: SODIUM ASCORBYL PHOSPHATE, ASCORBYL GLUCOSIDE 등
```

### CAS 번호 조회
```
"나이아신아마이드 CAS 번호 알려줘"
→ CAS: 98-92-0
→ EINECS: 202-713-4
```

### 무료 대안 검색
```
"ICID 구독 없이 INCI명 확인하는 방법?"
→ CosIng (EU 공식, 무료): ec.europa.eu/growth/tools-databases/cosing/
→ Cosmily (무료): cosmily.com
→ INCIDecoder: incidecoder.com
```

## Troubleshooting

### 문제: INCI명을 찾을 수 없음

```
원인 1: 신규 등록 성분
해결: ICID 최신 버전 확인, CosIng는 늦게 반영될 수 있음

원인 2: 명칭 변경
해결: 구 명칭 → 신 명칭 변경 이력 확인

원인 3: 비등록 성분
해결: PCPC 통해 신규 등록 신청
```

### 문제: CAS 번호 불일치

```
원인 1: 이성질체/수화물
해결: 동일 INCI에 복수 CAS 가능, 둘 다 유효

원인 2: 입력 오류
해결: 체크섬 검증으로 형식 확인
```

### 문제: 구독 비용 부담

```
해결 방안:
1. CosIng 활용 (무료, EU 공식)
2. 업계 협회 회원사 통해 접근
3. 필요 시 건별 조회 요청
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-01-16 | Initial release with ICID structure, PCPC guidelines |
