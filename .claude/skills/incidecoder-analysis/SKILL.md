# INCIDecoder Analysis

INCIDecoder.com 데이터를 활용한 화장품 성분 분석 스킬

## Overview

INCIDecoder는 화장품 성분의 기능, 안전성 등급, 제품 사용 사례를 제공하는 영문 데이터베이스입니다. 이 스킬은 INCIDecoder의 성분 정보를 스크래핑하여 전성분 분석, 경쟁 제품 벤치마킹, 성분 트렌드 파악에 활용합니다.

### 검증 상태
- **SSR 확인**: React/Next.js SPA 아님, 서버 사이드 렌더링
- **스크래핑 가능**: requests + BeautifulSoup으로 접근 가능
- **JavaScript 불필요**: HTML 응답에 모든 콘텐츠 포함 (~81KB)

## When to Use This Skill

| 상황 | 사용 여부 |
|------|----------|
| 특정 성분의 기능과 효능 확인 | **사용** |
| 성분 등급(Superstar/Goodie/OK/Icky) 확인 | **사용** |
| 경쟁사 제품의 성분 농도 파악 | **사용** |
| 전성분 리스트 종합 분석 | **사용** |
| 한국 규제 정보 확인 | 미사용 (kfda-ingredient 사용) |
| EU 공식 규제 정보 확인 | 미사용 (cosing-database 사용) |

## Core Capabilities

### URL 패턴

```
성분 페이지: https://incidecoder.com/ingredients/{slug}
제품 페이지: https://incidecoder.com/products/{product-slug}
```

#### Slug 변환 규칙
```python
def to_slug(name: str) -> str:
    # 1. 소문자 변환
    # 2. 특수문자 제거 (알파벳, 숫자, 하이픈만 유지)
    # 3. 공백 → 하이픈(-)
    
# 예시:
"Ceramide NP"       → "ceramide-np"
"Hyaluronic Acid"   → "hyaluronic-acid"
"Sodium Hyaluronate" → "sodium-hyaluronate"
"Vitamin C"         → "vitamin-c"
```

### HTML 구조

```html
<!-- 성분명 -->
<h1>Niacinamide</h1>

<!-- 등급 (h1 인근) -->
Superstar | Goodie | OK | Icky

<!-- 별칭 -->
<section id="also-called-like-this">
  vitamin B3, nicotinamide, ...
</section>

<!-- 기능 -->
<section id="what-it-does">
  <a>cell-communicating</a>
  <a>skin brightening</a>
  ...
</section>

<!-- 핵심 효능 -->
<h2>Quick Facts</h2>
<ul>
  <li>anti-aging benefits...</li>
  <li>reduces brown spots...</li>
</ul>

<!-- 상세 설명 -->
<h2>Geeky Details</h2>
<p>Scientific explanation...</p>

<!-- 농도 명시 제품 -->
<section id="products-known-amount">
  <h2>Products with a known amount of Niacinamide</h2>
  ...
</section>

<!-- 기타 포함 제품 -->
<section id="other-products">
  <h2>Other products with Niacinamide</h2>
  ...
</section>
```

### 수집 데이터 구조

```python
{
    "url": str,                    # 원본 URL
    "name": str,                   # 성분명
    "rating": str,                 # Superstar, Goodie, OK, Icky
    "also_called": list[str],      # 동의어/별칭
    "functions": list[str],        # 기능 태그
    "quick_facts": list[str],      # 핵심 효능 요약
    "geeky_details": str,          # 상세 과학적 설명
    "products_known": list[dict],  # 농도 명시 제품
    "other_products": list[str]    # 기타 포함 제품
}
```

### 성분 분류 기준

```python
KEY_ACTIVES = {
    "brightening": [
        "niacinamide", "arbutin", "tranexamic-acid", 
        "ascorbic-acid", "vitamin-c", "alpha-arbutin"
    ],
    "anti_aging": [
        "retinol", "retinal", "retinaldehyde", "adenosine",
        "peptide", "palmitoyl-tripeptide", "matrixyl"
    ],
    "exfoliating": [
        "salicylic-acid", "glycolic-acid", "lactic-acid",
        "mandelic-acid", "pha", "gluconolactone"
    ],
    "soothing": [
        "centella-asiatica", "madecassoside", "panthenol",
        "allantoin", "bisabolol", "cica"
    ],
    "hydrating": [
        "hyaluronic-acid", "sodium-hyaluronate", "ceramide",
        "squalane", "glycerin", "beta-glucan"
    ]
}

# 분석 제외 베이스 성분
BASE_INGREDIENTS = [
    "water", "aqua", "butylene-glycol", "propanediol", 
    "1-2-hexanediol", "pentylene-glycol", "glycerin",
    "dimethicone", "carbomer", "xanthan-gum", "phenoxyethanol"
]
```

## Common Workflows

### 1. 단일 성분 분석

```python
from scripts.fetch_incidecoder import get_ingredient_info, to_slug

# 성분명으로 정보 조회
slug = to_slug("Niacinamide")
info = get_ingredient_info(slug)

print(f"등급: {info['rating']}")
print(f"기능: {', '.join(info['functions'])}")
print(f"핵심 효능: {info['quick_facts']}")
```

### 2. 전성분 분석

```python
from scripts.analyze_ingredients import analyze_full_ingredients

ingredients = """
Water, Glycerin, Niacinamide, Butylene Glycol, 
Ceramide NP, Sodium Hyaluronate, Adenosine
"""

result = analyze_full_ingredients(ingredients)

# 결과 구조
{
    "total_count": 7,
    "key_actives": {
        "brightening": [{"name": "Niacinamide", "rating": "Superstar"}],
        "anti_aging": [{"name": "Adenosine", "rating": "Goodie"}],
        "hydrating": [
            {"name": "Ceramide NP", "rating": "Superstar"},
            {"name": "Sodium Hyaluronate", "rating": "Superstar"}
        ]
    },
    "base_ingredients": ["Water", "Glycerin", "Butylene Glycol"],
    "insights": [
        "브라이트닝 + 안티에이징 + 보습 콤비네이션",
        "Niacinamide 10% 이상 제품들과 경쟁 포지셔닝 가능"
    ]
}
```

### 3. 경쟁 제품 농도 벤치마킹

```python
from scripts.fetch_incidecoder import get_ingredient_info

# Niacinamide 함유 제품 농도 분석
info = get_ingredient_info("niacinamide")

for product in info['products_known'][:10]:
    print(f"{product['brand']} - {product['name']}: {product['concentration']}")

# 출력 예시:
# The Ordinary - Niacinamide 10% + Zinc 1%: 10%
# Paula's Choice - 10% Niacinamide Booster: 10%
# Good Molecules - Niacinamide Serum: 10%
```

## Best Practices

### Rate Limiting
```python
import time

# 요청 간 최소 1초 간격 필수
for slug in ingredient_slugs:
    info = get_ingredient_info(slug)
    time.sleep(1.0)  # 서버 부하 방지
```

### User-Agent 설정
```python
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# 반드시 일반 브라우저 User-Agent 사용
response = requests.get(url, headers=HEADERS, timeout=10)
```

### 에러 처리
```python
def get_ingredient_info(slug: str) -> dict:
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return {"error": str(e), "url": url}
    
    # 404 시 대체 slug 시도
    if response.status_code == 404:
        # 하이픈 위치 변경, 단어 순서 변경 등 시도
        pass
```

## Limitations

| 제한사항 | 대안 |
|----------|------|
| 영문 데이터베이스 (한글 미지원) | INCI명 또는 영문명으로 검색 |
| 한국 제품 등록 제한적 | k-beauty 글로벌 브랜드는 등록됨 |
| 규제 정보 없음 | cosing-database, kfda-ingredient 병행 |
| 실시간 업데이트 지연 | 신규 성분은 수일~수주 후 등록 |
| 농도 정보 불완전 | 제조사 공개 제품만 농도 표시 |

## Integration with Other Skills

```python
# 1. 성분 기본 정보: INCIDecoder
incidecoder_info = get_ingredient_info("niacinamide")

# 2. EU 규제 정보: cosing-database
from cosing_database.scripts.cosing_query import query_ingredient
cosing_info = query_ingredient("niacinamide")

# 3. 한국 기능성 고시: kfda-ingredient
from kfda_ingredient.scripts.kfda_query import check_functional
kfda_info = check_functional("niacinamide")

# 4. 종합 분석
combined = {
    "name": "Niacinamide",
    "incidecoder": {
        "rating": incidecoder_info['rating'],
        "functions": incidecoder_info['functions']
    },
    "regulation": {
        "eu": cosing_info['restrictions'],
        "korea": kfda_info['functional_category']
    }
}
```

## References

- [INCIDecoder Official](https://incidecoder.com)
- [HTML Structure Guide](references/html_structure.md)
- [Ingredient Classification](references/ingredient_classification.md)
