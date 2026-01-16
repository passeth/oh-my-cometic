---
name: cosmily-integration
description: Cosmily 화장품 처방 플랫폼 통합 스킬. 성분 검색, INCI명 조회, 안전성 등급, 처방 분석, 대체 원료 탐색 기능. 웹 스크래핑 기반 데이터 추출 및 처방 개발 지원.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - WebFetch
license: MIT
metadata:
  version: "1.0.0"
  category: cosmetic-integrations
  region: Global
  language: en
  last-updated: "2025-01-16"
  maintainer: cosmetic-skills
  tags:
    - cosmily
    - formulation
    - ingredient-search
    - INCI
    - safety-rating
    - web-scraping
    - cosmetic-database
---

# Cosmily Integration Skill

Cosmily 화장품 처방 플랫폼 통합 및 데이터 추출 스킬

## Overview

**Cosmily**는 화장품 처방 개발자와 소비자를 위한 종합 성분 데이터베이스 플랫폼입니다. 성분별 안전성 등급, INCI명, 기능 분류, 호환성 정보 등을 제공하며, 처방 분석 및 비교 기능을 제공합니다.

이 스킬은 Cosmily 플랫폼의 데이터를 활용하여 성분 검색, 안전성 확인, 처방 분석, 대체 원료 탐색 등의 기능을 제공합니다. 공식 API가 없어 웹 스크래핑 방식으로 데이터를 추출합니다.

**플랫폼 URL**: https://cosmily.com/

### 주요 기능

| 기능 | 설명 |
|------|------|
| **성분 검색** | INCI명, 일반명, CAS 번호로 성분 검색 |
| **안전성 등급** | Cosmily 자체 안전성 평가 점수 확인 |
| **기능 분류** | 성분의 화장품적 기능 분류 조회 |
| **처방 분석** | 전체 성분 목록 기반 처방 평가 |
| **대체 원료** | 유사 기능 성분 추천 |
| **호환성 확인** | 성분 간 호환성 정보 조회 |

## When to Use This Skill

이 스킬은 다음 상황에서 사용합니다:

- **성분 기초 조사**: 새로운 원료의 기본 정보 파악
- **INCI명 확인**: 상품명에서 공식 INCI명 조회
- **안전성 스크리닝**: 빠른 안전성 예비 평가
- **처방 비교 분석**: 경쟁 제품 처방 분석
- **대체 원료 탐색**: 기존 성분의 대안 검색
- **클린뷰티 검토**: 성분 안전성 프로파일 확인

## Core Capabilities

### 1. 성분 검색 (Ingredient Search)

Cosmily에서 성분 정보를 검색하는 방법:

```python
from cosmily_client import CosmilyClient

client = CosmilyClient()

# INCI명으로 검색
result = client.search_ingredient("NIACINAMIDE")
print(f"INCI: {result.inci_name}")
print(f"등급: {result.safety_rating}")
print(f"기능: {result.functions}")

# 일반명으로 검색
result = client.search_ingredient("Vitamin B3")

# CAS 번호로 검색
result = client.search_by_cas("98-92-0")
```

**검색 결과 구조**:

```python
{
    "inci_name": "NIACINAMIDE",
    "common_names": ["Vitamin B3", "Nicotinamide"],
    "cas_number": "98-92-0",
    "safety_rating": "A",  # A-F 등급
    "safety_score": 95,    # 0-100 점수
    "functions": ["Skin Conditioning", "Anti-Aging", "Brightening"],
    "concerns": [],
    "benefits": ["Improves skin texture", "Reduces pores", "Brightens skin"],
    "recommended_concentration": {"min": 2.0, "max": 10.0},
    "comedogenic_rating": 0,  # 0-5 스케일
    "irritancy_rating": 0,     # 0-5 스케일
    "url": "https://cosmily.com/ingredients/niacinamide"
}
```

### 2. 안전성 등급 시스템 (Safety Rating)

Cosmily의 안전성 평가 체계:

#### 문자 등급 (A-F)

| 등급 | 의미 | 설명 |
|------|------|------|
| **A** | Excellent | 매우 안전, 우려 사항 없음 |
| **B** | Good | 안전, 경미한 주의사항 가능 |
| **C** | Average | 보통, 일부 민감성 주의 필요 |
| **D** | Below Average | 낮음, 사용 주의 필요 |
| **F** | Poor | 우려됨, 사용 회피 권장 |

#### 수치 점수 (0-100)

- **90-100**: 매우 안전
- **70-89**: 안전
- **50-69**: 보통
- **30-49**: 주의 필요
- **0-29**: 우려됨

```python
# 안전성 등급 조회
rating = client.get_safety_rating("RETINOL")
print(f"문자 등급: {rating.grade}")  # C
print(f"점수: {rating.score}")        # 55
print(f"우려 사항: {rating.concerns}")
```

### 3. INCI명 조회 및 변환

상품명, 일반명에서 공식 INCI명 찾기:

```python
# 일반명 -> INCI 변환
inci = client.get_inci_name("Vitamin E")
# 결과: "TOCOPHEROL" 또는 "TOCOPHERYL ACETATE"

# 다양한 이름으로 검색
results = client.search_names("hyaluronic")
# 결과: ["HYALURONIC ACID", "SODIUM HYALURONATE", "HYDROLYZED HYALURONIC ACID", ...]

# INCI명 정규화
normalized = client.normalize_inci("niacinamide")
# 결과: "NIACINAMIDE" (대문자 표준 형식)
```

### 4. 기능별 성분 분류

Cosmily의 성분 기능 분류 체계:

```python
# 기능별 성분 조회
moisturizers = client.get_ingredients_by_function("Humectant")
# 결과: ["GLYCERIN", "HYALURONIC ACID", "PROPYLENE GLYCOL", ...]

# 성분의 기능 조회
functions = client.get_functions("SQUALANE")
# 결과: ["Emollient", "Moisturizer", "Skin Conditioning"]
```

**주요 기능 카테고리**:

| 카테고리 | 설명 | 예시 성분 |
|----------|------|-----------|
| **Humectant** | 수분 유지 | Glycerin, Hyaluronic Acid |
| **Emollient** | 피부 연화 | Squalane, Jojoba Oil |
| **Surfactant** | 계면활성 | Sodium Lauryl Sulfate |
| **Preservative** | 방부 | Phenoxyethanol, Parabens |
| **Antioxidant** | 산화방지 | Vitamin E, Vitamin C |
| **UV Filter** | 자외선차단 | Titanium Dioxide, Zinc Oxide |
| **Fragrance** | 향료 | Limonene, Linalool |
| **Colorant** | 착색 | CI 77891, CI 77492 |
| **pH Adjuster** | pH 조절 | Citric Acid, Sodium Hydroxide |
| **Thickener** | 증점 | Xanthan Gum, Carbomer |

### 5. 처방 분석 (Formula Analysis)

전체 성분 목록 기반 처방 평가:

```python
formula = [
    "AQUA", "GLYCERIN", "NIACINAMIDE", "HYALURONIC ACID",
    "PHENOXYETHANOL", "FRAGRANCE"
]

analysis = client.analyze_formula(formula)
print(f"전체 안전성: {analysis.overall_rating}")
print(f"우려 성분: {analysis.flagged_ingredients}")
print(f"누락 기능: {analysis.missing_functions}")
```

**분석 결과 구조**:

```python
{
    "overall_rating": "B",
    "overall_score": 78,
    "ingredient_count": 6,
    "ingredients": [
        {"inci": "AQUA", "rating": "A", "functions": ["Solvent"]},
        {"inci": "NIACINAMIDE", "rating": "A", "functions": ["Skin Conditioning"]},
        # ...
    ],
    "flagged_ingredients": [
        {"inci": "FRAGRANCE", "rating": "C", "concern": "Potential Sensitizer"}
    ],
    "function_coverage": {
        "present": ["Solvent", "Humectant", "Skin Conditioning", "Preservative"],
        "missing": ["UV Protection"]
    },
    "compatibility_issues": [],
    "suggestions": [
        "Consider replacing FRAGRANCE with fragrance-free alternative",
        "Add antioxidant for stability"
    ]
}
```

### 6. 대체 원료 탐색 (Alternative Finder)

특정 성분의 대안 검색:

```python
# 대체 원료 검색
alternatives = client.find_alternatives(
    ingredient="PHENOXYETHANOL",
    reason="cleaner_alternative",  # cleaner_alternative, cost_reduction, vegan, etc.
    max_results=5
)

# 결과
for alt in alternatives:
    print(f"{alt.inci_name}: 등급 {alt.safety_rating}, 유사도 {alt.similarity_score}")

# 기능 기반 대체
function_alts = client.find_by_function(
    function="Preservative",
    min_rating="B",
    exclude=["PARABENS"]
)
```

### 7. 성분 호환성 확인

성분 간 호환성 및 상호작용 확인:

```python
# 두 성분 호환성 확인
compatibility = client.check_compatibility("RETINOL", "VITAMIN C")
print(f"호환성: {compatibility.status}")  # "Compatible", "Caution", "Incompatible"
print(f"권장사항: {compatibility.recommendation}")

# 전체 처방 호환성 검사
formula_compatibility = client.check_formula_compatibility([
    "RETINOL", "NIACINAMIDE", "SALICYLIC ACID", "ASCORBIC ACID"
])
```

**호환성 상태**:

| 상태 | 의미 | 조치 |
|------|------|------|
| **Compatible** | 호환됨 | 안전하게 함께 사용 가능 |
| **Caution** | 주의 필요 | pH, 농도, 사용 시간 조절 필요 |
| **Incompatible** | 비호환 | 함께 사용 비권장 |

## Web Scraping Approach

### 데이터 추출 전략

Cosmily는 공식 API를 제공하지 않으므로, 웹 스크래핑을 통해 데이터를 추출합니다.

#### URL 패턴

```
# 성분 상세 페이지
https://cosmily.com/ingredients/{ingredient-slug}

# 성분 검색
https://cosmily.com/ingredients?search={query}

# 기능별 성분 목록
https://cosmily.com/ingredients?function={function}

# 제품 분석
https://cosmily.com/products/{product-slug}
```

#### 데이터 추출 포인트

```python
# HTML 구조 예시 (실제 구조와 다를 수 있음)
SELECTORS = {
    "inci_name": ".ingredient-name h1",
    "safety_rating": ".safety-badge .rating",
    "safety_score": ".safety-score .value",
    "functions": ".function-tags .tag",
    "concerns": ".concerns-list li",
    "benefits": ".benefits-list li",
    "comedogenic": ".comedogenic-rating .value",
    "irritancy": ".irritancy-rating .value",
    "description": ".ingredient-description p",
}
```

### Rate Limiting

서버 부하 방지 및 접근 차단 예방:

```python
# 권장 설정
RATE_LIMIT = {
    "requests_per_minute": 20,      # 분당 최대 요청
    "delay_between_requests": 3.0,  # 요청 간 최소 간격 (초)
    "retry_delay": 10.0,            # 실패 시 재시도 대기
    "max_retries": 3,               # 최대 재시도 횟수
    "backoff_multiplier": 2.0,      # 재시도 대기 배수
}
```

### 캐싱 전략

반복 요청 최소화 및 응답 속도 개선:

```python
CACHE_CONFIG = {
    "ingredient_cache_ttl": 86400,      # 24시간
    "search_cache_ttl": 3600,           # 1시간
    "formula_cache_ttl": 1800,          # 30분
    "cache_backend": "sqlite",          # sqlite, redis, file
    "cache_path": "~/.cosmetic_skills/cosmily_cache.db",
}
```

## Common Workflows

### Workflow 1: 신규 원료 조사

```
1. 상품명/일반명으로 Cosmily 검색
2. INCI명 확인 및 표준화
3. 안전성 등급 확인
4. 기능 분류 파악
5. 권장 농도 범위 확인
6. 호환성 정보 검토
7. 대체 원료 목록 준비
```

```python
def research_ingredient(name: str):
    client = CosmilyClient()

    # 1. 성분 검색
    result = client.search_ingredient(name)
    if not result:
        return {"status": "not_found"}

    # 2. 안전성 평가
    safety = {
        "rating": result.safety_rating,
        "score": result.safety_score,
        "concerns": result.concerns
    }

    # 3. 대체 원료 (등급이 낮은 경우)
    alternatives = []
    if result.safety_rating in ["D", "F"]:
        alternatives = client.find_alternatives(
            result.inci_name,
            min_rating="B"
        )

    return {
        "inci_name": result.inci_name,
        "safety": safety,
        "functions": result.functions,
        "recommended_concentration": result.recommended_concentration,
        "alternatives": alternatives
    }
```

### Workflow 2: 경쟁 제품 분석

```
1. 제품 성분 목록 입력
2. 각 성분 정보 조회
3. 전체 안전성 프로파일 생성
4. 우려 성분 식별
5. 기능별 분류 분석
6. 개선 포인트 도출
```

```python
def analyze_competitor_product(ingredients: list):
    client = CosmilyClient()

    analysis = client.analyze_formula(ingredients)

    # 강점/약점 분석
    strengths = [ing for ing in analysis.ingredients if ing["rating"] in ["A", "B"]]
    weaknesses = [ing for ing in analysis.ingredients if ing["rating"] in ["D", "F"]]

    # 차별화 포인트 제안
    suggestions = []
    if weaknesses:
        for weak in weaknesses:
            alts = client.find_alternatives(weak["inci"], min_rating="A")
            if alts:
                suggestions.append({
                    "replace": weak["inci"],
                    "with": alts[0].inci_name,
                    "benefit": f"Improves safety from {weak['rating']} to {alts[0].safety_rating}"
                })

    return {
        "overall_rating": analysis.overall_rating,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "improvement_suggestions": suggestions
    }
```

### Workflow 3: 클린뷰티 처방 설계

```
1. 목표 기능 정의
2. 각 기능별 클린 성분 검색 (A-B 등급만)
3. 호환성 검증
4. 처방 조합 최적화
5. 안전성 프로파일 확인
```

```python
def design_clean_formula(required_functions: list):
    client = CosmilyClient()

    formula = []

    for function in required_functions:
        # A-B 등급 성분만 검색
        candidates = client.get_ingredients_by_function(
            function,
            min_rating="B"
        )

        if candidates:
            # 첫 번째 후보 선택 (실제로는 추가 로직 필요)
            formula.append(candidates[0])

    # 호환성 검증
    compatibility = client.check_formula_compatibility(
        [ing.inci_name for ing in formula]
    )

    return {
        "formula": formula,
        "compatibility": compatibility,
        "clean_beauty_certified": all(ing.safety_rating in ["A", "B"] for ing in formula)
    }
```

## Best Practices

### 1. 웹 스크래핑 에티켓

```
- robots.txt 준수
- 적절한 User-Agent 설정
- Rate limiting 엄격 적용
- 캐싱으로 반복 요청 최소화
- 서버 부하 최소화 시간대 활용
```

### 2. 데이터 신뢰도

```
Cosmily 데이터 특성:
- 커뮤니티 기반 데이터 포함 가능
- 공식 규제 DB와 차이 가능
- 정기적 업데이트 확인 필요
- 교차 검증 권장 (CosIng, EWG, CIR)
```

### 3. 법적 고려사항

```
주의사항:
- 상업적 이용 시 이용약관 확인
- 데이터 저작권 존중
- 스크래핑 제한 준수
- 개인 학습/연구 목적 권장
```

### 4. 오류 처리

```python
# 권장 오류 처리 패턴
try:
    result = client.search_ingredient(name)
except RateLimitError:
    # 대기 후 재시도
    time.sleep(60)
    result = client.search_ingredient(name)
except NotFoundError:
    # 대체 검색 시도
    result = client.search_by_synonym(name)
except ConnectionError:
    # 캐시 데이터 사용
    result = client.get_from_cache(name)
```

## Reference Files

| File | Description |
|------|-------------|
| [references/cosmily_features.md](references/cosmily_features.md) | Cosmily 플랫폼 기능 상세 |
| [references/api_endpoints.md](references/api_endpoints.md) | 웹 엔드포인트 및 데이터 구조 |
| [scripts/cosmily_client.py](scripts/cosmily_client.py) | Python 웹 클라이언트 |

## Related Resources

- **Cosmily**: https://cosmily.com/
- **INCIDecoder**: https://incidecoder.com/ (유사 서비스)
- **CosDNA**: http://cosdna.com/ (유사 서비스)
- **Paula's Choice Ingredient Dictionary**: https://www.paulaschoice.com/ingredient-dictionary

## Data Comparison

Cosmily와 다른 성분 DB 비교:

| 항목 | Cosmily | EWG | CosIng | INCIDecoder |
|------|---------|-----|--------|-------------|
| 등급 체계 | A-F / 0-100 | 1-10 | 없음 | Good/Average/Poor |
| 규제 정보 | 일부 | 일부 | 상세 | 없음 |
| 기능 분류 | 상세 | 기본 | 공식 | 상세 |
| 호환성 | 제공 | 없음 | 없음 | 일부 |
| API | 없음 | 없음 | 없음 | 없음 |
| 업데이트 | 커뮤니티 | 정기 | 공식 | 정기 |

## Usage Examples

### 단일 성분 조회
```
"Niacinamide의 Cosmily 정보 알려줘"
-> INCI: NIACINAMIDE
-> 안전성: A등급 (95점)
-> 기능: Skin Conditioning, Brightening, Anti-Aging
-> 권장 농도: 2-10%
-> 코메도제닉: 0 (비면포성)
```

### 처방 분석
```
"이 성분들의 안전성 분석해줘: Water, Glycerin, Niacinamide, Fragrance"
-> 전체 등급: B (78점)
-> 우려 성분: FRAGRANCE (C등급 - 잠재적 민감성)
-> 권장: 무향 대안 고려
```

### 대체 원료 검색
```
"Parabens 대신 사용할 수 있는 안전한 방부제?"
-> PHENOXYETHANOL (B등급) - 가장 유사
-> ETHYLHEXYLGLYCERIN (A등급) - 부스터
-> POTASSIUM SORBATE (A등급) - 천연 대안
```

## Troubleshooting

### 문제: 성분을 찾을 수 없음
```
원인 1: 철자 오류
해결: 정확한 INCI명 확인, 대문자 변환

원인 2: 동의어 사용
해결: search_names() 메서드로 유사 이름 검색

원인 3: Cosmily 미등록
해결: 다른 DB 참조 (CosIng, INCIDecoder)
```

### 문제: 접근 차단
```
원인: Rate limit 초과 또는 IP 차단
해결:
1. 요청 간격 늘리기 (5초 이상)
2. User-Agent 다양화
3. 프록시 사용 고려
4. 캐싱 최대 활용
```

### 문제: 데이터 불일치
```
원인: 플랫폼 업데이트로 인한 구조 변경
해결:
1. HTML 선택자 업데이트
2. 최신 데이터 구조 확인
3. 백업 파서 구현
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-01-16 | Initial release with core functionality |
