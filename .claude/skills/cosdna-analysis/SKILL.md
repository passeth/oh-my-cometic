# CosDNA Analysis

CosDNA.com 데이터를 활용한 화장품 성분 안전성 분석 스킬

## Overview

CosDNA는 화장품 성분의 안전성(Safety), 여드름 유발(Acne), 자극성(Irritant) 점수를 제공하는 글로벌 화장품 성분 데이터베이스입니다. 이 스킬은 CosDNA의 성분 정보를 스크래핑하여 제품 안전성 분석, 민감성 피부 적합성 평가, 전성분 위험 요소 스크리닝에 활용합니다.

### 검증 상태
- **SSR 확인**: 서버 사이드 렌더링 (requests로 접근 가능)
- **다국어 지원**: 영어(/eng/), 한국어(/kor/), 일본어(/jpn/), 중국어 등
- **스크래핑 가능**: requests + BeautifulSoup으로 접근 가능

## When to Use This Skill

| 상황 | 사용 여부 |
|------|----------|
| 성분 안전성 점수 확인 (Safety 0-9) | **사용** |
| 여드름 유발 가능성 확인 (Acne 0-5) | **사용** |
| 피부 자극 가능성 확인 (Irritant 0-5) | **사용** |
| 전성분 위험 요소 스크리닝 | **사용** |
| 성분 기능/효능 확인 | 미사용 (incidecoder-analysis 사용) |
| EU 규제 정보 확인 | 미사용 (cosing-database 사용) |

## Core Capabilities

### URL 패턴

```
성분 검색: https://www.cosdna.com/eng/stuff.php?q={query}
성분 상세: https://www.cosdna.com/eng/{ingredient_id}.html
제품 검색: https://www.cosdna.com/eng/product.php?q={query}
전성분 분석: https://www.cosdna.com/eng/ingredients.php
```

### HTML 구조 (성분 상세 페이지)

```html
<!-- 성분명 -->
<h1 class="text-2xl text-[#6C0000] font-semibold">Nicotinamide</h1>

<!-- 동의어 -->
<div class="mt-2">
    Nicotinic acid amide,
    Niacinamide
</div>

<!-- 화학 정보 -->
<span class="px-2 py-1 rounded bg-stone-100">
    <span class="text-stone-600 mr-0.5">Formula: </span>
    C6H6N2O
</span>
<span class="px-2 py-1 rounded bg-stone-100">
    <span class="text-stone-600 mr-0.5">Molecular Weight: </span>
    122.12
</span>
<span class="px-2 py-1 rounded bg-stone-100">
    <span class="text-stone-600 mr-0.5">Cas No:</span>
    98-92-0
</span>

<!-- 안전성 점수 -->
<div class="border bg-amber-50 rounded text-center p-1">
    <div>Safety</div>
    <div><span class="safety safety-green">1</span></div>
</div>

<!-- 기능 -->
<div class="linkb1 tracking-wider leading-7">
    Skin conditioning - Smoothing
</div>
```

### 안전성 점수 체계

| 구분 | 점수 범위 | 의미 |
|------|----------|------|
| **Safety** | 0-9 | 전반적 안전성 (낮을수록 안전) |
| **Acne** | 0-5 | 여드름 유발 가능성 (낮을수록 안전) |
| **Irritant** | 0-5 | 자극 가능성 (낮을수록 안전) |

### 점수 색상 분류

```python
SAFETY_COLORS = {
    "green": [0, 1, 2],      # 안전
    "yellow": [3, 4, 5],     # 주의
    "red": [6, 7, 8, 9]      # 위험
}

ACNE_IRRITANT_COLORS = {
    "green": [0, 1],         # 안전
    "yellow": [2, 3],        # 주의
    "red": [4, 5]            # 위험
}
```

### 수집 데이터 구조

```python
{
    "url": str,
    "name": str,
    "aliases": list[str],
    "formula": str,
    "molecular_weight": float,
    "cas_no": str,
    "safety": int,           # 0-9
    "acne": int,             # 0-5 (없으면 None)
    "irritant": int,         # 0-5 (없으면 None)
    "function": str,
    "references": list[str]
}
```

## Common Workflows

### 1. 단일 성분 안전성 확인

```python
from scripts.fetch_cosdna import search_ingredient, get_ingredient_safety

# 성분 검색
results = search_ingredient("niacinamide")
# [{"name": "Niacinamide", "id": "af81356377", "url": "..."}]

# 안전성 정보 조회
safety_info = get_ingredient_safety(results[0]["id"])
print(f"Safety: {safety_info['safety']}")  # Safety: 1
print(f"Acne: {safety_info['acne']}")      # Acne: None
print(f"Irritant: {safety_info['irritant']}")  # Irritant: None
```

### 2. 전성분 안전성 스크리닝

```python
from scripts.analyze_safety import screen_ingredients

ingredients = """
Water, Glycerin, Niacinamide, Butylene Glycol,
Sodium Lauryl Sulfate, Fragrance, Phenoxyethanol
"""

result = screen_ingredients(ingredients)

# 결과 구조
{
    "total": 7,
    "screened": 5,
    "concerns": [
        {
            "name": "Sodium Lauryl Sulfate",
            "safety": 4,
            "irritant": 4,
            "concern": "높은 자극성"
        },
        {
            "name": "Fragrance",
            "safety": 5,
            "concern": "알레르기 가능성"
        }
    ],
    "safe_ingredients": [...],
    "summary": "2개 성분에 대한 주의 필요"
}
```

### 3. 민감성 피부 적합성 분석

```python
from scripts.analyze_safety import check_sensitive_skin_safe

ingredients = "Water, Glycerin, Niacinamide, Centella Asiatica Extract"

result = check_sensitive_skin_safe(ingredients)

# 결과
{
    "is_safe": True,
    "risk_level": "low",
    "flagged_ingredients": [],
    "recommendation": "민감성 피부에 적합한 처방입니다."
}
```

## Best Practices

### Rate Limiting
```python
import time

# 요청 간 최소 1초 간격 필수
for ingredient in ingredients:
    info = get_ingredient_safety(ingredient_id)
    time.sleep(1.0)
```

### User-Agent 설정
```python
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}
```

### 언어 선택
```python
# 영어 (기본)
url = "https://www.cosdna.com/eng/stuff.php?q=niacinamide"

# 한국어
url = "https://www.cosdna.com/kor/stuff.php?q=niacinamide"

# 일본어
url = "https://www.cosdna.com/jpn/stuff.php?q=niacinamide"
```

## Limitations

| 제한사항 | 대안 |
|----------|------|
| 모든 성분이 등록되어 있지 않음 | cosing-database 병행 |
| 안전성 점수가 주관적일 수 있음 | 여러 소스 교차 확인 |
| 농도 정보 미제공 | 전성분 순서로 농도 추정 |
| 신규 성분 업데이트 지연 | 공식 DB (CosIng, CIR) 확인 |

## Integration with Other Skills

```python
# 1. 안전성 점수: CosDNA
from cosdna_analysis.scripts.fetch_cosdna import get_ingredient_safety
cosdna_info = get_ingredient_safety("af81356377")

# 2. 기능/효능 정보: INCIDecoder
from incidecoder_analysis.scripts.fetch_incidecoder import get_ingredient_info
inci_info = get_ingredient_info("niacinamide")

# 3. EU 규제 정보: CosIng
from cosing_database.scripts.cosing_query import query_ingredient
cosing_info = query_ingredient("niacinamide")

# 4. 종합 분석
combined = {
    "name": "Niacinamide",
    "safety": {
        "cosdna_score": cosdna_info['safety'],
        "acne": cosdna_info['acne'],
        "irritant": cosdna_info['irritant']
    },
    "benefits": inci_info['functions'],
    "rating": inci_info['rating'],
    "regulation": cosing_info['restrictions']
}
```

## Safety Score Interpretation Guide

### Safety (0-9)

| 점수 | 해석 | 권장 조치 |
|------|------|----------|
| 0-2 | 안전 | 일반 사용 가능 |
| 3-5 | 주의 | 민감성 피부 패치 테스트 권장 |
| 6-9 | 위험 | 사용 제한 또는 대체 성분 검토 |

### Acne (0-5)

| 점수 | 해석 | 적합 피부 타입 |
|------|------|---------------|
| 0-1 | 비코메도제닉 | 모든 피부 |
| 2-3 | 약간 코메도제닉 | 정상~건성 피부 |
| 4-5 | 코메도제닉 | 지성/여드름 피부 주의 |

### Irritant (0-5)

| 점수 | 해석 | 적합 피부 타입 |
|------|------|---------------|
| 0-1 | 저자극 | 민감성 피부 가능 |
| 2-3 | 중간 자극 | 정상 피부 권장 |
| 4-5 | 고자극 | 민감성 피부 피할 것 |

## References

- [CosDNA Official](https://www.cosdna.com)
- [Safety Score Guide](references/safety_scores.md)
- [Common Flagged Ingredients](references/flagged_ingredients.md)
