# Cosmily Web Endpoints & Data Extraction

Cosmily 웹 엔드포인트 및 데이터 추출 패턴 문서

## Overview

Cosmily는 공식 API를 제공하지 않습니다. 이 문서는 웹 스크래핑을 통한 데이터 추출 방법을 설명합니다.

**주의**: 웹 스크래핑 시 반드시 이용약관을 확인하고, 서버 부하를 최소화하는 에티켓을 준수하세요.

## Base URL

```
https://cosmily.com
```

## Endpoint Patterns

### 1. 성분 검색 (Ingredient Search)

#### 검색 페이지
```
GET /ingredients?search={query}

Parameters:
  - search: 검색어 (INCI명, 일반명, CAS 번호)

Example:
  /ingredients?search=niacinamide
  /ingredients?search=vitamin+c
  /ingredients?search=98-92-0
```

#### 기능별 필터
```
GET /ingredients?function={function_name}

Parameters:
  - function: 기능 카테고리명

Examples:
  /ingredients?function=humectant
  /ingredients?function=preservative
  /ingredients?function=antioxidant
```

#### 안전성 등급 필터
```
GET /ingredients?rating={grade}

Parameters:
  - rating: A, B, C, D, F

Examples:
  /ingredients?rating=A
  /ingredients?rating=A,B  # 다중 선택
```

#### 복합 필터
```
GET /ingredients?function={func}&rating={grade}&search={query}

Example:
  /ingredients?function=preservative&rating=A,B&search=ethyl
```

### 2. 성분 상세 페이지 (Ingredient Detail)

```
GET /ingredients/{ingredient-slug}

URL Pattern:
  - slug는 INCI명의 소문자, 하이픈 구분 형식
  - 예: "NIACINAMIDE" -> "niacinamide"
  - 예: "HYALURONIC ACID" -> "hyaluronic-acid"

Examples:
  /ingredients/niacinamide
  /ingredients/hyaluronic-acid
  /ingredients/retinol
  /ingredients/ascorbic-acid
```

### 3. 제품 분석 (Product Analysis)

#### 제품 페이지
```
GET /products/{product-slug}

Examples:
  /products/brand-name-product-name
```

#### 성분 목록으로 분석 (JavaScript 기반)
```
POST /api/analyze (추정)

Request Body:
{
  "ingredients": ["AQUA", "GLYCERIN", "NIACINAMIDE", ...]
}

Note: 실제 API 엔드포인트가 아닐 수 있음.
      클라이언트 사이드 JavaScript로 처리될 수 있음.
```

### 4. 호환성 검사 (Compatibility Check)

```
GET /tools/compatibility-checker?ingredients={ing1},{ing2}

Parameters:
  - ingredients: 쉼표로 구분된 성분 목록

Example:
  /tools/compatibility-checker?ingredients=retinol,vitamin-c
```

## HTML Data Extraction

### 성분 상세 페이지 구조 (추정)

```html
<!-- 성분 이름 -->
<div class="ingredient-header">
  <h1 class="ingredient-name">NIACINAMIDE</h1>
  <div class="ingredient-aliases">
    <span>Also known as: Vitamin B3, Nicotinamide</span>
  </div>
</div>

<!-- 안전성 등급 -->
<div class="safety-section">
  <div class="safety-grade">A</div>
  <div class="safety-score">95</div>
  <div class="safety-description">Excellent - Very safe ingredient</div>
</div>

<!-- 코메도제닉/자극성 -->
<div class="ratings-section">
  <div class="comedogenic-rating">
    <span class="label">Comedogenic Rating:</span>
    <span class="value">0</span>
  </div>
  <div class="irritancy-rating">
    <span class="label">Irritancy Rating:</span>
    <span class="value">0</span>
  </div>
</div>

<!-- 기능 -->
<div class="functions-section">
  <h3>Functions</h3>
  <ul class="function-list">
    <li class="function-tag">Skin Conditioning</li>
    <li class="function-tag">Brightening</li>
    <li class="function-tag">Anti-Aging</li>
  </ul>
</div>

<!-- 효능 -->
<div class="benefits-section">
  <h3>Benefits</h3>
  <ul class="benefits-list">
    <li>Improves skin texture</li>
    <li>Reduces appearance of pores</li>
    <li>Brightens skin tone</li>
  </ul>
</div>

<!-- 우려사항 -->
<div class="concerns-section">
  <h3>Concerns</h3>
  <ul class="concerns-list">
    <!-- 비어있거나 우려사항 목록 -->
  </ul>
</div>

<!-- 권장 농도 -->
<div class="concentration-section">
  <h3>Recommended Concentration</h3>
  <span class="min">2%</span> - <span class="max">10%</span>
</div>

<!-- 추가 정보 -->
<div class="additional-info">
  <div class="cas-number">CAS: 98-92-0</div>
  <div class="description">
    <p>Niacinamide is a form of vitamin B3...</p>
  </div>
</div>
```

### CSS 선택자 맵핑 (추정)

```python
SELECTORS = {
    # 기본 정보
    "inci_name": "h1.ingredient-name",
    "common_names": ".ingredient-aliases span",
    "cas_number": ".cas-number",

    # 안전성
    "safety_grade": ".safety-grade",
    "safety_score": ".safety-score",
    "safety_description": ".safety-description",

    # 등급
    "comedogenic_rating": ".comedogenic-rating .value",
    "irritancy_rating": ".irritancy-rating .value",

    # 기능/효능
    "functions": ".function-list li",
    "benefits": ".benefits-list li",
    "concerns": ".concerns-list li",

    # 농도
    "concentration_min": ".concentration-section .min",
    "concentration_max": ".concentration-section .max",

    # 설명
    "description": ".description p",

    # 검색 결과 목록
    "search_results": ".ingredient-card",
    "search_result_name": ".ingredient-card .name",
    "search_result_rating": ".ingredient-card .rating",
    "search_result_link": ".ingredient-card a",
}
```

## Response Data Structures

### 성분 검색 결과

```python
SearchResult = {
    "total_count": 150,
    "page": 1,
    "per_page": 20,
    "results": [
        {
            "inci_name": "NIACINAMIDE",
            "slug": "niacinamide",
            "safety_grade": "A",
            "functions": ["Skin Conditioning", "Brightening"],
            "url": "/ingredients/niacinamide"
        },
        # ...
    ]
}
```

### 성분 상세 정보

```python
IngredientDetail = {
    "inci_name": "NIACINAMIDE",
    "slug": "niacinamide",
    "common_names": ["Vitamin B3", "Nicotinamide"],
    "cas_number": "98-92-0",
    "ec_number": "202-713-4",

    "safety": {
        "grade": "A",
        "score": 95,
        "description": "Excellent - Very safe ingredient"
    },

    "ratings": {
        "comedogenic": 0,
        "irritancy": 0
    },

    "functions": [
        "Skin Conditioning",
        "Brightening",
        "Anti-Aging",
        "Antioxidant"
    ],

    "benefits": [
        "Improves skin texture",
        "Reduces appearance of pores",
        "Brightens skin tone",
        "Helps with fine lines"
    ],

    "concerns": [],

    "concentration": {
        "min": 2.0,
        "max": 10.0,
        "unit": "%"
    },

    "description": "Niacinamide is a form of vitamin B3...",

    "compatibility": {
        "works_well_with": ["Hyaluronic Acid", "Vitamin C"],
        "use_with_caution": [],
        "avoid_with": []
    },

    "url": "https://cosmily.com/ingredients/niacinamide"
}
```

### 처방 분석 결과

```python
FormulaAnalysis = {
    "overall": {
        "grade": "B",
        "score": 78,
        "description": "Good formulation with minor concerns"
    },

    "ingredients": [
        {
            "inci": "AQUA",
            "grade": "A",
            "functions": ["Solvent"],
            "position": 1
        },
        {
            "inci": "GLYCERIN",
            "grade": "A",
            "functions": ["Humectant"],
            "position": 2
        },
        # ...
    ],

    "flagged": [
        {
            "inci": "FRAGRANCE",
            "grade": "C",
            "concern": "Potential sensitizer",
            "recommendation": "Consider fragrance-free alternative"
        }
    ],

    "function_coverage": {
        "present": ["Solvent", "Humectant", "Skin Conditioning", "Preservative"],
        "missing": ["UV Protection", "Antioxidant"]
    },

    "compatibility_issues": [],

    "suggestions": [
        "Consider adding antioxidant for stability",
        "Fragrance may cause sensitivity in some users"
    ]
}
```

### 호환성 검사 결과

```python
CompatibilityResult = {
    "ingredients": ["RETINOL", "ASCORBIC ACID"],
    "status": "CAUTION",
    "details": {
        "can_use_together": True,
        "recommendation": "Best used at different times of day",
        "reason": "Both are potent actives that may increase sensitivity",
        "tips": [
            "Use Vitamin C in AM",
            "Use Retinol in PM",
            "Start with lower concentrations"
        ]
    }
}
```

## Rate Limiting Implementation

### 요청 제한 설정

```python
RATE_LIMIT_CONFIG = {
    # 기본 설정
    "requests_per_minute": 20,
    "min_delay_seconds": 3.0,

    # 재시도 설정
    "max_retries": 3,
    "retry_delay_seconds": 10.0,
    "backoff_multiplier": 2.0,

    # 에러 처리
    "on_rate_limit": "wait_and_retry",  # or "fail_fast"
    "rate_limit_wait_seconds": 60.0,

    # User-Agent 로테이션
    "user_agents": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    ],
    "rotate_user_agent": True,
}
```

### 요청 헤더

```python
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; CosmeticSkills/1.0; Research)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
}
```

## Caching Strategy

### 캐시 설정

```python
CACHE_CONFIG = {
    # TTL (Time To Live) 설정
    "ingredient_detail_ttl": 86400,     # 24시간
    "search_results_ttl": 3600,         # 1시간
    "compatibility_ttl": 86400,         # 24시간
    "formula_analysis_ttl": 1800,       # 30분

    # 저장소 설정
    "backend": "sqlite",  # sqlite, redis, filesystem
    "db_path": "~/.cosmetic_skills/cosmily_cache.db",

    # 캐시 키 생성
    "key_format": "cosmily:{type}:{identifier}",

    # 정리 설정
    "cleanup_interval": 3600,  # 1시간마다
    "max_cache_size_mb": 100,
}
```

### 캐시 키 예시

```python
# 성분 상세
"cosmily:ingredient:niacinamide"

# 검색 결과
"cosmily:search:vitamin+c:page1"

# 호환성
"cosmily:compatibility:retinol_vitamin-c"

# 처방 분석
"cosmily:formula:md5hash_of_ingredients"
```

## Error Handling

### 예상 에러 유형

```python
ERROR_TYPES = {
    "NOT_FOUND": {
        "http_code": 404,
        "description": "성분을 찾을 수 없음",
        "action": "동의어 검색 시도 또는 다른 DB 참조"
    },
    "RATE_LIMITED": {
        "http_code": 429,
        "description": "요청 제한 초과",
        "action": "대기 후 재시도"
    },
    "ACCESS_DENIED": {
        "http_code": 403,
        "description": "접근 거부 (IP 차단 가능)",
        "action": "프록시 사용 또는 시간 경과 후 시도"
    },
    "SERVER_ERROR": {
        "http_code": 500,
        "description": "서버 오류",
        "action": "잠시 후 재시도"
    },
    "PARSE_ERROR": {
        "http_code": None,
        "description": "HTML 파싱 실패 (구조 변경)",
        "action": "선택자 업데이트 필요"
    },
    "TIMEOUT": {
        "http_code": None,
        "description": "요청 시간 초과",
        "action": "재시도 또는 타임아웃 증가"
    },
}
```

### 에러 응답 처리

```python
def handle_response_error(response, url):
    """응답 에러 처리"""
    if response.status_code == 404:
        raise IngredientNotFoundError(f"Ingredient not found: {url}")

    elif response.status_code == 429:
        retry_after = response.headers.get("Retry-After", 60)
        raise RateLimitError(f"Rate limited. Retry after {retry_after}s")

    elif response.status_code == 403:
        raise AccessDeniedError(f"Access denied: {url}")

    elif response.status_code >= 500:
        raise ServerError(f"Server error {response.status_code}: {url}")

    elif not response.ok:
        raise RequestError(f"Request failed: {response.status_code}")
```

## Data Validation

### 추출 데이터 검증

```python
VALIDATION_RULES = {
    "inci_name": {
        "required": True,
        "type": str,
        "pattern": r"^[A-Z0-9\s\-/()]+$",  # 대문자 INCI 형식
        "max_length": 200
    },
    "safety_grade": {
        "required": True,
        "type": str,
        "allowed_values": ["A", "B", "C", "D", "F"]
    },
    "safety_score": {
        "required": False,
        "type": int,
        "range": (0, 100)
    },
    "comedogenic_rating": {
        "required": False,
        "type": int,
        "range": (0, 5)
    },
    "irritancy_rating": {
        "required": False,
        "type": int,
        "range": (0, 5)
    },
    "cas_number": {
        "required": False,
        "type": str,
        "pattern": r"^\d{2,7}-\d{2}-\d$"  # CAS 번호 형식
    },
    "concentration_min": {
        "required": False,
        "type": float,
        "range": (0, 100)
    },
    "concentration_max": {
        "required": False,
        "type": float,
        "range": (0, 100)
    },
}
```

## JavaScript-Rendered Content

### 동적 콘텐츠 처리

일부 데이터는 JavaScript로 동적 렌더링될 수 있습니다.

```python
# Selenium 또는 Playwright 사용 시
JS_WAIT_SELECTORS = [
    ".safety-section",      # 안전성 정보 로드 대기
    ".functions-section",   # 기능 정보 로드 대기
    ".ingredient-loaded",   # 전체 로드 완료 표시
]

JS_RENDER_TIMEOUT = 10  # 초
```

### 대안: API 요청 감지

```python
# 브라우저 개발자 도구에서 XHR 요청 확인
POTENTIAL_API_ENDPOINTS = [
    "/api/ingredients/{id}",
    "/api/search",
    "/api/compatibility",
    # 실제 엔드포인트는 네트워크 탭에서 확인 필요
]
```

## Best Practices

### 스크래핑 에티켓

1. **robots.txt 확인**
   ```
   https://cosmily.com/robots.txt
   ```

2. **요청 간격 유지**
   - 최소 3초 간격
   - 피크 시간대 피하기

3. **캐싱 최대 활용**
   - 동일 요청 반복 방지
   - 적절한 TTL 설정

4. **에러 시 백오프**
   - 지수적 백오프 적용
   - 연속 실패 시 장시간 대기

5. **식별 가능한 User-Agent**
   - 목적을 명시한 User-Agent 사용
   - 연락처 포함 고려

### 데이터 품질 유지

1. **정기적 검증**
   - HTML 구조 변경 모니터링
   - 추출 데이터 샘플 검증

2. **다중 소스 교차 검증**
   - Cosmily + CosIng + EWG 비교
   - 불일치 시 플래그 처리

3. **업데이트 추적**
   - 마지막 스크래핑 일시 기록
   - 데이터 신선도 표시
