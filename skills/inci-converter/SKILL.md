---
name: inci-converter
description: 성분명 INCI 변환 유틸리티. 한글 성분명, 영문 상품명, INCI명 간 양방향 변환 및 CAS 번호 조회 기능. 전성분표 작성, 원료 검색, 라벨링 작업에 사용.
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
license: MIT license
metadata:
    skill-author: EVAS Cosmetic
    original-source: K-Dense Inc. (claude-scientific-skills structure)
    version: 1.0.0
    category: utility
---

# INCI Converter Skill

## Overview

**INCI(International Nomenclature of Cosmetic Ingredients)**는 화장품 성분의 국제 표준 명명법입니다. 이 스킬은 한글 성분명, 영문 상품명, INCI명 간의 양방향 변환을 지원하며, 전성분표 작성 및 원료 검색에 필수적인 도구입니다.

### 주요 특징

- **양방향 변환**: 한글 ↔ INCI, 상품명 → INCI
- **식물 성분 지원**: 학명 기반 식물 추출물 변환
- **배치 처리**: 다량의 성분을 일괄 변환
- **CAS 번호 조회**: 성분별 CAS 등록 번호 제공
- **200+ 성분 DB**: 화장품에 자주 사용되는 성분 데이터베이스 내장

## When to Use This Skill

| 상황 | 사용 방법 |
|------|----------|
| **전성분표 작성** | 한글 원료명 → INCI명 변환 |
| **원료 검색** | INCI명 → 한글명 변환으로 원료 찾기 |
| **라벨 번역** | 수입/수출 라벨 작성 시 명칭 변환 |
| **규제 문서 작성** | 정확한 INCI명으로 규제 문서 작성 |
| **원료 구매** | 상품명 → INCI명 변환으로 정확한 원료 확인 |
| **CAS 번호 필요** | 규제 검토, SDS 작성 시 CAS 조회 |

## Core Capabilities

### 1. 한글 → INCI 변환

한글 성분명을 국제 표준 INCI명으로 변환합니다.

```python
from inci_convert import InciConverter

converter = InciConverter()

# 단일 변환
converter.korean_to_inci("나이아신아마이드")
# Output: "NIACINAMIDE"

converter.korean_to_inci("히알루론산나트륨")
# Output: "SODIUM HYALURONATE"

converter.korean_to_inci("글리세린")
# Output: "GLYCERIN"

# 보습제
converter.korean_to_inci("부틸렌글라이콜")  # → "BUTYLENE GLYCOL"
converter.korean_to_inci("프로판다이올")    # → "PROPANEDIOL"

# 계면활성제
converter.korean_to_inci("세테아릴알코올")  # → "CETEARYL ALCOHOL"
converter.korean_to_inci("폴리소르베이트60")  # → "POLYSORBATE 60"

# 점증제
converter.korean_to_inci("카보머")         # → "CARBOMER"
converter.korean_to_inci("잔탄검")         # → "XANTHAN GUM"
```

### 2. INCI → 한글 변환

INCI명을 한글 성분명으로 변환합니다.

```python
# 단일 변환
converter.inci_to_korean("NIACINAMIDE")
# Output: "나이아신아마이드"

converter.inci_to_korean("TOCOPHEROL")
# Output: "토코페롤"

converter.inci_to_korean("ASCORBIC ACID")
# Output: "아스코르브산"

# 기능성 성분
converter.inci_to_korean("RETINOL")        # → "레티놀"
converter.inci_to_korean("ADENOSINE")      # → "아데노신"

# 유화제
converter.inci_to_korean("CETEARYL OLIVATE")  # → "세테아릴올리베이트"
converter.inci_to_korean("SORBITAN OLIVATE")  # → "소르비탄올리베이트"
```

### 3. 상품명 → INCI 변환

상업적 상품명/일반명을 INCI명으로 변환합니다.

```python
# 비타민류
converter.tradename_to_inci("Vitamin B3")   # → "NIACINAMIDE"
converter.tradename_to_inci("Vitamin E")    # → "TOCOPHEROL"
converter.tradename_to_inci("Vitamin C")    # → "ASCORBIC ACID"
converter.tradename_to_inci("Pro-Vitamin B5")  # → "PANTHENOL"

# 기타 상품명
converter.tradename_to_inci("AHA")          # → "GLYCOLIC ACID"
converter.tradename_to_inci("BHA")          # → "SALICYLIC ACID"
converter.tradename_to_inci("Squalane")     # → "SQUALANE"
converter.tradename_to_inci("Hyaluronic Acid")  # → "HYALURONIC ACID"
```

### 4. CAS 번호 조회

성분의 CAS(Chemical Abstracts Service) 등록 번호를 조회합니다.

```python
# INCI명으로 CAS 조회
converter.get_cas_number("NIACINAMIDE")
# Output: "98-92-0"

converter.get_cas_number("GLYCERIN")
# Output: "56-81-5"

converter.get_cas_number("HYALURONIC ACID")
# Output: "9004-61-9"

# 한글명으로 CAS 조회
converter.get_cas_number_korean("나이아신아마이드")
# Output: "98-92-0"
```

### 5. 식물 성분 학명 변환

식물 추출물의 한글명을 INCI 학명 표기로 변환합니다.

```python
# 식물 추출물
converter.korean_to_inci("녹차추출물")
# Output: "CAMELLIA SINENSIS LEAF EXTRACT"

converter.korean_to_inci("알로에베라잎추출물")
# Output: "ALOE BARBADENSIS LEAF EXTRACT"

converter.korean_to_inci("병풀추출물")
# Output: "CENTELLA ASIATICA EXTRACT"

# 오일
converter.korean_to_inci("호호바오일")
# Output: "SIMMONDSIA CHINENSIS (JOJOBA) SEED OIL"

converter.korean_to_inci("티트리오일")
# Output: "MELALEUCA ALTERNIFOLIA (TEA TREE) LEAF OIL"

# 워터
converter.korean_to_inci("라벤더워터")
# Output: "LAVANDULA ANGUSTIFOLIA (LAVENDER) FLOWER WATER"
```

### 6. 배치 변환

다수의 성분을 한 번에 변환합니다.

```python
# 한글 → INCI 배치 변환
ingredients = ["글리세린", "나이아신아마이드", "히알루론산나트륨", "판테놀"]
results = converter.batch_convert(ingredients, direction="korean_to_inci")
# Output: ["GLYCERIN", "NIACINAMIDE", "SODIUM HYALURONATE", "PANTHENOL"]

# INCI → 한글 배치 변환
inci_list = ["GLYCERIN", "NIACINAMIDE", "RETINOL"]
results = converter.batch_convert(inci_list, direction="inci_to_korean")
# Output: ["글리세린", "나이아신아마이드", "레티놀"]

# 결과를 딕셔너리로 반환
results = converter.batch_convert(ingredients, direction="korean_to_inci", as_dict=True)
# Output: {"글리세린": "GLYCERIN", "나이아신아마이드": "NIACINAMIDE", ...}
```

## Common Workflows

### Workflow 1: 전성분표 작성

제품 라벨에 사용할 전성분표를 작성합니다.

```python
def create_ingredient_list(korean_ingredients: list) -> str:
    """
    한글 원료 목록을 INCI 전성분표로 변환

    Args:
        korean_ingredients: 한글 성분명 리스트 (배합량 순서)

    Returns:
        INCI 전성분표 문자열
    """
    converter = InciConverter()

    inci_list = []
    failed = []

    for ingredient in korean_ingredients:
        result = converter.korean_to_inci(ingredient)
        if result:
            inci_list.append(result)
        else:
            failed.append(ingredient)

    # 전성분표 형식
    result = ", ".join(inci_list)

    if failed:
        print(f"변환 실패: {failed}")

    return result

# 사용 예시
ingredients = [
    "정제수", "글리세린", "나이아신아마이드", "부틸렌글라이콜",
    "히알루론산나트륨", "아데노신", "카보머", "트리에탄올아민",
    "페녹시에탄올", "향료"
]

inci_list = create_ingredient_list(ingredients)
# Output: "AQUA, GLYCERIN, NIACINAMIDE, BUTYLENE GLYCOL, SODIUM HYALURONATE,
#          ADENOSINE, CARBOMER, TRIETHANOLAMINE, PHENOXYETHANOL, FRAGRANCE"
```

### Workflow 2: 원료 데이터시트 작성

원료의 상세 정보를 포함한 데이터시트를 생성합니다.

```python
def create_ingredient_datasheet(inci_name: str) -> dict:
    """
    성분의 상세 정보 데이터시트 생성

    Args:
        inci_name: INCI 성분명

    Returns:
        성분 정보 딕셔너리
    """
    converter = InciConverter()

    return {
        "inci_name": inci_name,
        "korean_name": converter.inci_to_korean(inci_name),
        "cas_number": converter.get_cas_number(inci_name),
        "common_tradenames": converter.get_tradenames(inci_name),
        "category": converter.get_category(inci_name)
    }

# 사용 예시
datasheet = create_ingredient_datasheet("NIACINAMIDE")
# Output:
# {
#     "inci_name": "NIACINAMIDE",
#     "korean_name": "나이아신아마이드",
#     "cas_number": "98-92-0",
#     "common_tradenames": ["Vitamin B3", "Nicotinamide"],
#     "category": "Active Ingredient"
# }
```

### Workflow 3: 수입/수출 라벨 변환

해외 제품 라벨을 국내용으로 또는 국내 제품을 해외용으로 변환합니다.

```python
def convert_label(ingredient_list: str, direction: str) -> str:
    """
    라벨 전성분 변환

    Args:
        ingredient_list: 전성분 문자열 (쉼표 구분)
        direction: "to_korean" or "to_inci"

    Returns:
        변환된 전성분 문자열
    """
    converter = InciConverter()

    # 쉼표로 분리
    ingredients = [i.strip() for i in ingredient_list.split(",")]

    if direction == "to_korean":
        converted = converter.batch_convert(ingredients, "inci_to_korean")
    else:
        converted = converter.batch_convert(ingredients, "korean_to_inci")

    return ", ".join(converted)

# 수입 라벨 → 한글 변환
imported_label = "AQUA, GLYCERIN, NIACINAMIDE, PANTHENOL, TOCOPHEROL"
korean_label = convert_label(imported_label, "to_korean")
# Output: "정제수, 글리세린, 나이아신아마이드, 판테놀, 토코페롤"
```

## Supported Ingredient Categories

이 스킬에서 지원하는 성분 카테고리:

| 카테고리 | 예시 성분 | 지원 수 |
|---------|----------|--------|
| **보습제** | 글리세린, 부틸렌글라이콜, 프로판다이올 | 25+ |
| **유화제** | 세테아릴알코올, 폴리소르베이트류 | 20+ |
| **계면활성제** | 소듐라우릴설페이트, 코카미도프로필베타인 | 20+ |
| **점증제** | 카보머, 잔탄검, 하이드록시에틸셀룰로오스 | 15+ |
| **방부제** | 페녹시에탄올, 벤질알코올, 파라벤류 | 15+ |
| **활성 성분** | 나이아신아마이드, 레티놀, 펩타이드류 | 30+ |
| **비타민류** | 토코페롤, 아스코르브산, 판테놀 | 15+ |
| **식물 추출물** | 녹차, 알로에, 센텔라 추출물 | 40+ |
| **오일/버터** | 호호바오일, 시어버터, 아르간오일 | 20+ |
| **자외선차단제** | 옥시벤존, 티타늄디옥사이드, 징크옥사이드 | 10+ |

## Best Practices

### 1. 정확한 한글 표기 사용

```python
# 권장
converter.korean_to_inci("나이아신아마이드")  # 표준 표기

# 비권장 (변환 실패 가능)
converter.korean_to_inci("나이아신아미드")   # 비표준 표기
converter.korean_to_inci("니아신아마이드")   # 비표준 표기
```

### 2. INCI명 대문자 규칙

INCI명은 항상 **대문자**로 표기합니다:

```python
# 올바른 형식
"NIACINAMIDE"
"SODIUM HYALURONATE"
"CAMELLIA SINENSIS LEAF EXTRACT"

# 잘못된 형식
"Niacinamide"
"sodium hyaluronate"
```

### 3. 식물 추출물 표기

식물 추출물은 학명을 포함한 전체 INCI명을 사용합니다:

```python
# 올바른 형식
"CAMELLIA SINENSIS LEAF EXTRACT"
"ALOE BARBADENSIS LEAF EXTRACT"

# 불완전한 형식
"GREEN TEA EXTRACT"    # 비공식
"ALOE EXTRACT"         # 불완전
```

### 4. 배치 변환 시 오류 처리

```python
def safe_batch_convert(ingredients: list) -> dict:
    converter = InciConverter()
    results = {"success": [], "failed": []}

    for ing in ingredients:
        try:
            result = converter.korean_to_inci(ing)
            if result:
                results["success"].append((ing, result))
            else:
                results["failed"].append(ing)
        except Exception as e:
            results["failed"].append(ing)

    return results
```

## Reference Files

| 파일 | 내용 |
|------|------|
| `references/inci_rules.md` | INCI 명명 규칙 및 표기법 가이드 |
| `scripts/inci_convert.py` | Python 변환기 클래스 및 데이터베이스 |

## Troubleshooting

### 문제: 변환 결과가 None

```
원인 1: 지원되지 않는 성분
해결: 데이터베이스에 성분 추가 필요

원인 2: 철자 오류
해결: 정확한 한글 표기 확인

원인 3: 비표준 표기 사용
해결: 표준 한글 표기로 변환 후 시도
```

### 문제: 식물 추출물 변환 실패

```
원인: 추출물 종류(잎, 꽃, 뿌리 등) 미지정
해결: 추출 부위를 명시하여 검색
      예: "녹차잎추출물", "장미꽃추출물"
```

### 문제: CAS 번호 조회 실패

```
원인 1: 혼합물/복합 성분 (CAS 없음)
해결: 개별 성분으로 분리하여 조회

원인 2: 신규 등록 성분
해결: ChemSpider, PubChem 등 외부 DB 확인
```

## Additional Resources

- **PCPC INCI Dictionary**: https://www.personalcarecouncil.org/resources/inci/
- **CosIng Database**: https://ec.europa.eu/growth/tools-databases/cosing/
- **PubChem**: https://pubchem.ncbi.nlm.nih.gov/
- **대한화장품협회**: https://www.kcia.or.kr/

## Quick Reference

```python
from inci_convert import InciConverter

converter = InciConverter()

# 한글 → INCI
converter.korean_to_inci("나이아신아마이드")  # → "NIACINAMIDE"

# INCI → 한글
converter.inci_to_korean("NIACINAMIDE")       # → "나이아신아마이드"

# 상품명 → INCI
converter.tradename_to_inci("Vitamin B3")      # → "NIACINAMIDE"

# CAS 번호 조회
converter.get_cas_number("NIACINAMIDE")        # → "98-92-0"

# 배치 변환
converter.batch_convert(["글리세린", "판테놀"], "korean_to_inci")
# → ["GLYCERIN", "PANTHENOL"]
```

## Summary

**inci-converter** 스킬은 화장품 성분명 변환의 필수 도구입니다:

1. **한글 → INCI**: 전성분표 작성, 규제 문서 작성
2. **INCI → 한글**: 수입 라벨 번역, 원료 검색
3. **상품명 → INCI**: 원료 구매, 정확한 성분 확인
4. **CAS 번호 조회**: 규제 검토, SDS 작성
5. **배치 변환**: 대량 데이터 처리

전성분표 작성, 라벨 번역, 원료 관리 등 화장품 개발의 모든 단계에서 활용할 수 있습니다.
