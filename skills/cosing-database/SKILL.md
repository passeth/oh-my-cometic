---
name: cosing-database
description: EU 화장품 성분 데이터베이스(CosIng) 검색 및 분석. INCI명 조회, 규제 상태 확인, 기능 분류, 제한/금지 물질 확인에 사용. 화장품 원료 규제 준수의 핵심 데이터 소스.
allowed-tools: [Read, Write, Edit, Bash, WebFetch]
license: MIT license
metadata:
    skill-author: EVAS Cosmetic
    original-source: K-Dense Inc. (claude-scientific-skills structure)
---

# CosIng Database Skill

## Overview

CosIng(Cosmetic Ingredient Database)은 **유럽연합 집행위원회**에서 운영하는 공식 화장품 성분 데이터베이스입니다. 30,000개 이상의 성분에 대한 INCI명, CAS 번호, 규제 상태, 기능 분류 정보를 제공합니다.

이 스킬은 CosIng 데이터베이스를 효율적으로 검색하고, 원료의 규제 적합성을 확인하며, 배합 시 필요한 규제 정보를 추출하는 방법을 제공합니다.

**데이터베이스 URL**: https://ec.europa.eu/growth/tools-databases/cosing/

## When to Use This Skill

- **INCI명 표준화**: 원료의 공식 INCI명 확인
- **규제 확인**: EU 화장품 규정(EC No 1223/2009) 준수 여부 확인
- **Annex 확인**: 금지물질(Annex II), 제한물질(Annex III), 허용 색소(Annex IV), 방부제(Annex V), 자외선차단제(Annex VI) 해당 여부
- **기능 분류**: 성분의 공식 기능(예: Emollient, Surfactant, Preservative) 확인
- **CAS 번호 조회**: 원료의 CAS 등록 번호 확인
- **배합 검토**: 신규 처방의 EU 규제 적합성 사전 검토

## Core Capabilities

### 1. 성분 검색 (Ingredient Search)

CosIng에서 성분을 검색하는 여러 방법:

#### INCI명으로 검색
```python
import requests
from bs4 import BeautifulSoup

def search_cosing_by_inci(inci_name: str) -> dict:
    """
    INCI명으로 CosIng 검색

    Args:
        inci_name: INCI 성분명 (예: "NIACINAMIDE", "HYALURONIC ACID")

    Returns:
        성분 정보 딕셔너리
    """
    base_url = "https://ec.europa.eu/growth/tools-databases/cosing/details"

    # CosIng API 또는 웹 스크래핑으로 검색
    # 실제 구현 시 적절한 API 엔드포인트 사용

    result = {
        "inci_name": inci_name,
        "cas_number": None,
        "ec_number": None,
        "functions": [],
        "restrictions": [],
        "annex_status": {}
    }

    return result
```

#### CAS 번호로 검색
```python
def search_cosing_by_cas(cas_number: str) -> dict:
    """
    CAS 번호로 CosIng 검색

    Args:
        cas_number: CAS 등록 번호 (예: "98-92-0" for Niacinamide)

    Returns:
        성분 정보 딕셔너리
    """
    # CAS 번호 형식 검증
    import re
    if not re.match(r'^\d{2,7}-\d{2}-\d$', cas_number):
        raise ValueError(f"Invalid CAS number format: {cas_number}")

    # 검색 수행
    return search_result
```

### 2. 규제 상태 확인 (Regulatory Status)

EU 화장품 규정의 Annex별 상태 확인:

| Annex | 내용 | 의미 |
|-------|------|------|
| **Annex II** | 금지 물질 | 화장품 사용 전면 금지 |
| **Annex III** | 제한 물질 | 조건부 사용 (농도, 용도 제한) |
| **Annex IV** | 허용 색소 | 색소로 사용 가능한 물질 |
| **Annex V** | 허용 방부제 | 방부제로 사용 가능한 물질 |
| **Annex VI** | 허용 UV 필터 | 자외선차단제로 사용 가능한 물질 |

```python
def check_annex_status(inci_name: str) -> dict:
    """
    성분의 Annex 해당 여부 확인

    Returns:
        {
            "annex_ii": False,      # 금지 여부
            "annex_iii": {          # 제한 사항
                "max_concentration": "0.3%",
                "product_types": ["rinse-off", "leave-on"],
                "conditions": "..."
            },
            "annex_iv": None,       # 색소 해당 여부
            "annex_v": None,        # 방부제 해당 여부
            "annex_vi": None        # UV필터 해당 여부
        }
    """
    pass
```

### 3. 기능 분류 조회 (Function Classification)

CosIng에서 정의하는 화장품 성분 기능:

```python
COSING_FUNCTIONS = {
    # 피부 관련
    "EMOLLIENT": "피부 연화, 유연 기능",
    "HUMECTANT": "수분 보유 기능",
    "MOISTURISING": "피부 보습 기능",
    "SKIN CONDITIONING": "피부 컨디셔닝",
    "SKIN PROTECTING": "피부 보호 기능",
    "SOOTHING": "피부 진정 기능",

    # 제형 관련
    "EMULSIFYING": "유화 기능",
    "SURFACTANT": "계면활성 기능",
    "VISCOSITY CONTROLLING": "점도 조절 기능",
    "SOLVENT": "용매 기능",
    "GEL FORMING": "겔 형성 기능",

    # 보존/안정화
    "PRESERVATIVE": "방부 기능",
    "ANTIOXIDANT": "산화방지 기능",
    "CHELATING": "금속이온봉쇄 기능",
    "UV ABSORBER": "자외선 흡수 기능",
    "UV FILTER": "자외선 차단 기능",

    # 미용 효과
    "SKIN BLEACHING": "피부 미백 기능",
    "ANTI-SEBUM": "피지 조절 기능",
    "KERATOLYTIC": "각질 제거 기능",

    # 기타
    "FRAGRANCE": "향료",
    "COLORANT": "착색제",
    "OPACIFYING": "불투명화제",
    "BULKING": "충전제"
}

def get_ingredient_functions(inci_name: str) -> list:
    """
    성분의 공식 기능 목록 조회

    Returns:
        ["HUMECTANT", "SKIN CONDITIONING", "MOISTURISING"]
    """
    pass
```

### 4. 제한 조건 상세 조회 (Restriction Details)

Annex III 제한물질의 상세 사용 조건:

```python
def get_restriction_details(inci_name: str) -> dict:
    """
    제한물질의 상세 사용 조건 조회

    Example for Salicylic Acid:
    {
        "inci_name": "SALICYLIC ACID",
        "cas_number": "69-72-7",
        "annex_iii_ref": "98",
        "restrictions": {
            "rinse_off_hair": {
                "max_concentration": "3.0%",
                "conditions": None
            },
            "leave_on": {
                "max_concentration": "2.0%",
                "conditions": "Not for children under 3 years"
            },
            "rinse_off": {
                "max_concentration": "2.0%",
                "conditions": None
            }
        },
        "labeling": [
            "Contains Salicylic Acid",
            "Not for use on children under 3 years (leave-on)"
        ]
    }
    """
    pass
```

### 5. 동의어 및 대체명 검색 (Synonym Search)

```python
def search_synonyms(query: str) -> list:
    """
    상품명, 화학명, INCI명 간 동의어 검색

    Args:
        query: 검색어 (예: "Vitamin B3", "Nicotinamide", "3-Pyridinecarboxamide")

    Returns:
        [
            {
                "inci_name": "NIACINAMIDE",
                "cas_number": "98-92-0",
                "other_names": [
                    "Nicotinamide",
                    "Vitamin B3",
                    "3-Pyridinecarboxamide",
                    "Nicotinic acid amide"
                ],
                "match_type": "synonym"
            }
        ]
    """
    pass
```

## Common Workflows

### Workflow 1: 신규 원료 규제 검토

새로운 원료를 배합에 도입하기 전 규제 적합성 검토:

```python
def review_new_ingredient(inci_name: str, intended_use: str, concentration: float) -> dict:
    """
    신규 원료의 EU 규제 적합성 검토

    Args:
        inci_name: INCI 성분명
        intended_use: 사용 목적 ("leave-on", "rinse-off", "eye", "oral")
        concentration: 배합 농도 (%)

    Returns:
        {
            "status": "APPROVED" | "RESTRICTED" | "PROHIBITED",
            "details": {...},
            "warnings": [...],
            "labeling_requirements": [...]
        }
    """

    # 1. CosIng에서 성분 검색
    ingredient = search_cosing_by_inci(inci_name)

    # 2. Annex II (금지물질) 확인
    if ingredient.get("annex_ii"):
        return {
            "status": "PROHIBITED",
            "reason": "Listed in Annex II (Prohibited Substances)",
            "alternative_suggestions": find_alternatives(inci_name)
        }

    # 3. Annex III (제한물질) 확인
    if ingredient.get("annex_iii"):
        restrictions = ingredient["annex_iii"]
        max_conc = restrictions.get(intended_use, {}).get("max_concentration")

        if max_conc and concentration > max_conc:
            return {
                "status": "RESTRICTED",
                "reason": f"Exceeds maximum concentration ({max_conc}%) for {intended_use}",
                "recommendation": f"Reduce concentration to ≤ {max_conc}%"
            }

    # 4. 기능별 Annex 확인 (방부제, UV필터, 색소)
    # ...

    return {
        "status": "APPROVED",
        "functions": ingredient.get("functions"),
        "notes": "No restrictions for intended use"
    }
```

### Workflow 2: 전체 처방 규제 스캐닝

```python
def scan_formulation(formula: list[dict]) -> dict:
    """
    전체 처방의 EU 규제 적합성 일괄 확인

    Args:
        formula: [{"inci": "AQUA", "percent": 70.0}, {"inci": "NIACINAMIDE", "percent": 5.0}, ...]

    Returns:
        {
            "overall_status": "PASS" | "REVIEW_REQUIRED" | "FAIL",
            "ingredients_checked": 15,
            "issues": [
                {"inci": "...", "issue": "...", "severity": "HIGH|MEDIUM|LOW"}
            ],
            "labeling_requirements": [...],
            "cmr_substances": [...]  # Carcinogenic, Mutagenic, Reprotoxic
        }
    """
    pass
```

### Workflow 3: Annex 업데이트 모니터링

```python
def check_recent_annex_updates(since_date: str = None) -> list:
    """
    최근 Annex 개정 사항 확인

    EU 화장품 규정은 정기적으로 Annex가 업데이트됨
    - 새로운 금지물질 추가
    - 제한 조건 변경
    - 새로운 UV필터/방부제 승인

    Returns:
        [
            {
                "regulation": "EU 2023/1545",
                "effective_date": "2024-07-15",
                "changes": [
                    {"annex": "II", "action": "ADD", "substance": "..."},
                    {"annex": "III", "action": "MODIFY", "substance": "..."}
                ]
            }
        ]
    """
    pass
```

## Best Practices

### 1. INCI명 표준화
- 항상 **대문자** INCI명 사용 (NIACINAMIDE, not Niacinamide)
- 공백 포함 가능 (HYALURONIC ACID)
- 숫자 포함 가능 (TOCOPHERYL ACETATE)

### 2. CAS 번호 검증
- 형식: `XXXXX-XX-X` (2-7자리-2자리-1자리)
- 체크섬 알고리즘으로 유효성 검증
- 여러 CAS가 하나의 INCI에 대응될 수 있음

### 3. 규제 해석 주의사항
- **Leave-on vs Rinse-off**: 제품 유형에 따라 제한 농도가 다름
- **Eye products**: 눈 주변 제품은 더 엄격한 제한
- **Children products**: 어린이용 제품 별도 규정
- **Nanomaterials**: 나노 형태는 별도 표기 필요 (예: `TITANIUM DIOXIDE (NANO)`)

### 4. Annex 업데이트 추적
- EU 공식 저널(Official Journal) 정기 확인
- 규정 발효일(effective date)과 적용일(application date) 구분
- 경과 조치(transitional measures) 확인

### 5. 데이터 캐싱
- CosIng 응답 캐싱으로 반복 쿼리 최적화
- 캐시 유효기간: 1일 권장 (규제 변경 가능성)
- 로컬 DB 동기화 고려

## Reference Files

상세 정보는 아래 참조 문서 확인:

| 파일 | 내용 |
|------|------|
| `references/cosing_api.md` | CosIng 웹 인터페이스 및 데이터 추출 방법 |
| `references/inci_nomenclature.md` | INCI 명명 규칙 및 표기법 |
| `references/eu_regulations.md` | EU 화장품 규정(EC 1223/2009) 상세 해설 |

## Troubleshooting

### 문제: 성분을 찾을 수 없음
```
원인 1: INCI명 철자 오류
해결: 정확한 INCI명 확인 (공백, 하이픈 포함)

원인 2: 새로 등록된 성분
해결: CAS 번호로 검색 시도, PCPC INCI Dictionary 확인

원인 3: 혼합물/추출물
해결: 개별 성분으로 분리하여 검색
```

### 문제: Annex 정보가 오래됨
```
원인: 최신 규정 미반영
해결:
1. EU 공식 저널에서 최신 개정 확인
2. EUR-Lex (https://eur-lex.europa.eu) 검색
3. CosIng 데이터베이스 업데이트 일자 확인
```

## Additional Resources

- **CosIng 공식**: https://ec.europa.eu/growth/tools-databases/cosing/
- **EU 화장품 규정**: [EC No 1223/2009](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32009R1223)
- **SCCS 의견**: https://health.ec.europa.eu/scientific-committees/scientific-committee-consumer-safety-sccs_en
- **PCPC INCI Dictionary**: https://www.personalcarecouncil.org/resources/inci/

## Quick Reference

```python
# 빠른 INCI 검색
result = search_cosing_by_inci("RETINOL")

# 규제 상태 확인
status = check_annex_status("HYDROQUINONE")  # Annex II - 금지

# 제한 조건 확인
restrictions = get_restriction_details("SALICYLIC ACID")

# 기능 분류
functions = get_ingredient_functions("GLYCERIN")
# ["HUMECTANT", "SKIN CONDITIONING", "SOLVENT"]
```

## Summary

**cosing-database** 스킬은 EU 화장품 규정 준수의 기본입니다:

1. **검색**: INCI명/CAS번호로 성분 정보 검색
2. **규제 확인**: Annex II-VI 해당 여부 확인
3. **제한 조건**: 농도, 용도별 제한 사항 파악
4. **기능 분류**: 공식 기능 카테고리 확인
5. **업데이트 추적**: 규정 개정 모니터링

EU 수출을 고려하는 모든 화장품 개발에 필수적인 도구입니다.
