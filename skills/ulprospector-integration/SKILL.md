---
name: ulprospector-integration
description: UL Prospector 화장품 원료 데이터베이스 연동. 공급사 검색, 기술 데이터 시트(TDS) 접근, 원료 스펙 조회, 대체 원료 탐색, 샘플 요청 워크플로우 지원. 원료 소싱의 핵심 플랫폼.
category: cosmetic-integrations
allowed-tools: [WebFetch, WebSearch, Read, Write, Edit]
license: MIT license
metadata:
    skill-author: EVAS Cosmetic
    original-source: K-Dense Inc. (claude-scientific-skills structure)
    platform-url: https://www.ulprospector.com
---

# UL Prospector Integration Skill

## Overview

**UL Prospector**는 화장품, 식품, 코팅 등 다양한 산업의 원료 정보를 제공하는 세계 최대 원료 데이터베이스 플랫폼입니다. 30,000개 이상의 글로벌 공급사와 500,000개 이상의 원료 제품 정보를 보유하고 있습니다.

이 스킬은 UL Prospector를 활용하여 화장품 원료 검색, 공급사 탐색, 기술 문서 접근, 샘플 요청을 효율적으로 수행하는 방법을 제공합니다.

**플랫폼 URL**: https://www.ulprospector.com/en/na/PersonalCare

## When to Use This Skill

- **원료 소싱**: 새로운 원료 공급사 및 제품 탐색
- **TDS/SDS 조회**: Technical Data Sheet, Safety Data Sheet 다운로드
- **스펙 비교**: 동일 기능 원료의 공급사별 스펙 비교
- **대체 원료 탐색**: 기존 원료의 대안 검색
- **샘플 요청**: 공급사에 샘플 의뢰
- **가격 정보**: 원료 가격대 및 MOQ 확인
- **공급사 연락처**: 담당자 정보 확인

## Platform Tiers

### Free Tier (무료 계정)
| 기능 | 제한 |
|------|------|
| 원료 검색 | 기본 검색 가능 |
| 제품 목록 조회 | 제한된 결과 수 |
| 공급사 정보 | 기본 정보만 |
| TDS 다운로드 | 로그인 필요, 일부 제한 |
| 샘플 요청 | 로그인 후 가능 |
| 월간 검색 | 제한 있음 |

### Premium Tier (유료 구독)
| 기능 | 포함 내용 |
|------|----------|
| 무제한 검색 | 모든 카테고리 |
| 전체 TDS/SDS | 제한 없이 다운로드 |
| 상세 스펙 비교 | Side-by-side 비교 도구 |
| 가격 정보 | 일부 공급사 가격대 |
| API 접근 | 기업용 API |
| 담당자 연락처 | 직접 연락 가능 |
| 알림 서비스 | 신제품/규제 변경 알림 |

## Core Capabilities

### 1. 원료 검색 (Ingredient Search)

#### 기본 검색 방법
```python
from typing import Optional, List, Dict
import requests
from dataclasses import dataclass

@dataclass
class ProspectorSearchParams:
    """UL Prospector 검색 파라미터"""
    keyword: str                          # 검색어
    category: str = "Personal Care"       # 카테고리
    function: Optional[str] = None        # 기능 분류
    supplier: Optional[str] = None        # 공급사명
    chemistry: Optional[str] = None       # 화학 분류
    trade_name: Optional[str] = None      # 상품명
    inci_name: Optional[str] = None       # INCI명
    certifications: Optional[List[str]] = None  # 인증 (Natural, Organic 등)

def search_prospector(params: ProspectorSearchParams) -> List[Dict]:
    """
    UL Prospector에서 원료 검색

    Args:
        params: 검색 파라미터

    Returns:
        검색 결과 리스트
    """
    base_url = "https://www.ulprospector.com/en/na/PersonalCare/search"

    # 검색 쿼리 구성
    query_params = {
        "q": params.keyword,
        "cat": params.category
    }

    if params.function:
        query_params["function"] = params.function
    if params.supplier:
        query_params["supplier"] = params.supplier

    # WebSearch를 통한 검색 실행
    # 실제 구현은 WebFetch 도구 활용

    results = []
    return results
```

#### 기능별 검색 카테고리
```python
PROSPECTOR_FUNCTIONS = {
    # 피부 케어
    "EMOLLIENT": "Emollients",
    "MOISTURIZER": "Moisturizers",
    "HUMECTANT": "Humectants",
    "SKIN_CONDITIONING": "Skin Conditioning Agents",
    "ANTI_AGING": "Anti-Aging Actives",
    "BRIGHTENING": "Skin Brightening",

    # 선케어
    "UV_FILTER": "UV Filters",
    "SUNSCREEN_ACTIVE": "Sunscreen Actives",
    "AFTER_SUN": "After Sun Care",

    # 헤어 케어
    "HAIR_CONDITIONING": "Hair Conditioning Agents",
    "SILICONE": "Silicones",
    "FILM_FORMER": "Film Formers",

    # 제형 기술
    "EMULSIFIER": "Emulsifiers",
    "THICKENER": "Thickeners & Rheology Modifiers",
    "SURFACTANT": "Surfactants",
    "SOLUBILIZER": "Solubilizers",

    # 보존
    "PRESERVATIVE": "Preservatives",
    "ANTIOXIDANT": "Antioxidants",
    "CHELATING": "Chelating Agents",

    # 감각
    "FRAGRANCE": "Fragrances",
    "COLORANT": "Colorants",
    "SENSORY": "Sensory Modifiers"
}
```

### 2. 공급사 검색 (Supplier Search)

```python
@dataclass
class SupplierInfo:
    """공급사 정보"""
    name: str
    headquarters: str
    regions: List[str]              # 공급 가능 지역
    product_count: int              # 등록 제품 수
    specialties: List[str]          # 전문 분야
    certifications: List[str]       # 보유 인증
    contact_info: Dict              # 연락처
    website: str

def search_suppliers(
    keyword: Optional[str] = None,
    region: str = "Asia Pacific",
    specialty: Optional[str] = None
) -> List[SupplierInfo]:
    """
    공급사 검색

    Args:
        keyword: 공급사명 또는 제품 키워드
        region: 지역 필터
        specialty: 전문 분야

    Returns:
        공급사 정보 리스트
    """
    pass
```

#### 주요 글로벌 공급사 (Personal Care)

| 공급사 | 본사 | 전문 분야 | 한국 유통 |
|--------|------|-----------|----------|
| BASF | 독일 | 계면활성제, 유화제, 활성성분 | O |
| Evonik | 독일 | 실리콘, 계면활성제 | O |
| Ashland | 미국 | 폴리머, 레올로지 | O |
| Croda | 영국 | 에멀리언트, 활성성분 | O |
| DSM | 네덜란드 | 비타민, 활성성분 | O |
| Symrise | 독일 | 향료, 활성성분 | O |
| Givaudan | 스위스 | 향료, 활성성분 | O |
| Seppic | 프랑스 | 유화제, 폴리머 | O |
| Lubrizol | 미국 | 폴리머, 레올로지 | O |
| Dow | 미국 | 실리콘, 폴리머 | O |

### 3. 기술 문서 접근 (Technical Documents)

#### TDS (Technical Data Sheet) 구조
```python
@dataclass
class TechnicalDataSheet:
    """기술 데이터 시트 정보"""
    product_name: str
    trade_name: str
    supplier: str
    inci_name: str
    cas_number: Optional[str]

    # 물리화학적 특성
    appearance: str
    color: str
    odor: str
    ph: Optional[str]
    viscosity: Optional[str]
    density: Optional[float]
    solubility: Dict[str, str]

    # 사용 권장
    recommended_use_level: str      # 권장 사용량 (%)
    applications: List[str]         # 적용 제품 유형
    processing_guidelines: str      # 처리 방법

    # 규제 정보
    regulatory_status: Dict[str, str]  # 국가별 규제 상태
    certifications: List[str]

    # 보관/취급
    storage_conditions: str
    shelf_life: str
    packaging: List[str]

def get_tds(product_id: str) -> TechnicalDataSheet:
    """
    제품의 TDS 정보 조회

    Args:
        product_id: UL Prospector 제품 ID

    Returns:
        TDS 정보 객체
    """
    pass
```

#### SDS (Safety Data Sheet) 접근
```python
@dataclass
class SafetyDataSheet:
    """안전 데이터 시트 정보"""
    product_name: str
    supplier: str
    revision_date: str

    # GHS 분류
    hazard_classification: List[str]
    signal_word: Optional[str]
    hazard_statements: List[str]
    precautionary_statements: List[str]

    # 구성 성분
    composition: List[Dict]

    # 응급 조치
    first_aid_measures: Dict[str, str]

    # 취급 및 저장
    handling_precautions: str
    storage_conditions: str

    # 노출 방지
    exposure_controls: Dict
    ppe_requirements: List[str]

def get_sds(product_id: str) -> SafetyDataSheet:
    """제품의 SDS 정보 조회"""
    pass
```

### 4. 제품 스펙 조회 (Product Specifications)

```python
@dataclass
class ProductSpecification:
    """제품 상세 스펙"""
    product_id: str
    trade_name: str
    supplier: str
    inci_name: str

    # 분류
    chemistry_type: str             # 화학적 분류
    function_categories: List[str]  # 기능 분류

    # 스펙
    specifications: Dict[str, str]  # 규격 항목

    # 사용 정보
    typical_use_level: str          # 일반 사용량
    suggested_applications: List[str]

    # 인증
    certifications: List[str]
    claims: List[str]               # 마케팅 클레임

    # 가격/MOQ (프리미엄 기능)
    price_range: Optional[str]
    moq: Optional[str]

def get_product_spec(product_id: str) -> ProductSpecification:
    """제품 상세 스펙 조회"""
    pass

def compare_products(product_ids: List[str]) -> Dict:
    """
    여러 제품 스펙 비교

    Args:
        product_ids: 비교할 제품 ID 리스트

    Returns:
        {
            "products": [...],
            "comparison_matrix": {...},
            "differences": [...],
            "recommendations": [...]
        }
    """
    pass
```

### 5. 대체 원료 탐색 (Alternative Ingredients)

```python
def find_alternatives(
    current_ingredient: str,
    criteria: Dict = None
) -> List[Dict]:
    """
    기존 원료의 대체 원료 탐색

    Args:
        current_ingredient: 현재 사용 중인 원료 (INCI명 또는 상품명)
        criteria: 대체 조건
            - same_function: 동일 기능 필수 (기본 True)
            - natural_preferred: 천연 원료 우선
            - cost_effective: 비용 효율 우선
            - region: 특정 지역 공급사
            - certifications: 필요 인증

    Returns:
        대체 원료 후보 리스트
        [
            {
                "product_name": "...",
                "supplier": "...",
                "inci_name": "...",
                "similarity_score": 0.85,
                "advantages": ["..."],
                "considerations": ["..."]
            }
        ]
    """
    default_criteria = {
        "same_function": True,
        "natural_preferred": False,
        "cost_effective": False,
        "region": None,
        "certifications": []
    }

    if criteria:
        default_criteria.update(criteria)

    # UL Prospector 검색 및 필터링
    alternatives = []

    return alternatives
```

#### 대체 원료 탐색 사례

```python
# 예시: Dimethicone 대체 원료 탐색
alternatives = find_alternatives(
    current_ingredient="DIMETHICONE",
    criteria={
        "same_function": True,
        "natural_preferred": True,
        "certifications": ["COSMOS", "ECOCERT"]
    }
)

# 결과 예시
"""
[
    {
        "product_name": "Squalane",
        "supplier": "Amyris",
        "inci_name": "SQUALANE",
        "similarity_score": 0.82,
        "advantages": [
            "천연/바이오 원료",
            "COSMOS 인증",
            "유사한 에멀리언트 효과"
        ],
        "considerations": [
            "실리콘 대비 높은 가격",
            "다른 감각 특성"
        ]
    },
    {
        "product_name": "Hemisqualane",
        "supplier": "Aprinnova",
        "inci_name": "C13-15 ALKANE",
        "similarity_score": 0.78,
        "advantages": [
            "가벼운 사용감",
            "지속가능 원료"
        ],
        "considerations": [
            "실리콘보다 휘발성"
        ]
    }
]
"""
```

### 6. 샘플 요청 워크플로우 (Sample Request)

```python
@dataclass
class SampleRequest:
    """샘플 요청 정보"""
    product_id: str
    product_name: str
    supplier: str
    quantity: str
    purpose: str
    company_info: Dict
    contact_info: Dict
    delivery_address: Dict
    additional_notes: Optional[str] = None

def create_sample_request(request: SampleRequest) -> Dict:
    """
    샘플 요청 생성

    Args:
        request: 샘플 요청 정보

    Returns:
        {
            "request_id": "...",
            "status": "submitted",
            "expected_response": "3-5 business days",
            "supplier_contact": {...}
        }
    """
    pass

def track_sample_request(request_id: str) -> Dict:
    """샘플 요청 상태 추적"""
    pass
```

#### 샘플 요청 템플릿

```python
sample_request_template = """
Subject: Sample Request - {product_name}

Dear {supplier_name} Team,

I am writing to request a sample of {product_name} for evaluation purposes.

Company Information:
- Company: {company_name}
- Industry: Personal Care / Cosmetics
- Location: {country}

Request Details:
- Product: {product_name} ({trade_name})
- Quantity: {quantity}
- Purpose: {purpose}

Intended Application:
{application_details}

Shipping Address:
{shipping_address}

Contact Person:
- Name: {contact_name}
- Email: {contact_email}
- Phone: {contact_phone}

We would appreciate receiving the sample along with:
- Technical Data Sheet (TDS)
- Safety Data Sheet (SDS)
- Certificate of Analysis (CoA)
- Pricing information (if available)

Thank you for your consideration.

Best regards,
{contact_name}
{company_name}
"""
```

## Common Workflows

### Workflow 1: 신규 원료 소싱

```python
def source_new_ingredient(
    function: str,
    requirements: Dict
) -> Dict:
    """
    신규 원료 소싱 워크플로우

    Args:
        function: 필요 기능 (예: "Emollient", "Thickener")
        requirements: 요구 사항
            - budget: 예산 범위
            - certifications: 필요 인증
            - region: 선호 공급 지역
            - natural: 천연 원료 여부

    Returns:
        소싱 결과 및 추천
    """
    workflow = {
        "step1_search": "기능별 원료 검색",
        "step2_filter": "요구사항 기반 필터링",
        "step3_compare": "상위 후보 스펙 비교",
        "step4_tds": "TDS/SDS 검토",
        "step5_sample": "샘플 요청",
        "step6_evaluate": "샘플 평가"
    }

    # Step 1: 검색
    search_results = search_prospector(ProspectorSearchParams(
        keyword=function,
        category="Personal Care",
        function=function
    ))

    # Step 2: 필터링
    filtered = filter_by_requirements(search_results, requirements)

    # Step 3: 비교
    top_candidates = filtered[:5]
    comparison = compare_products([p["id"] for p in top_candidates])

    return {
        "candidates": top_candidates,
        "comparison": comparison,
        "next_steps": ["Request TDS", "Request samples"]
    }
```

### Workflow 2: 원료 대체 검토

```python
def review_ingredient_replacement(
    current_ingredient: str,
    reason: str
) -> Dict:
    """
    원료 대체 검토 워크플로우

    Args:
        current_ingredient: 현재 원료
        reason: 대체 사유
            - "cost_reduction": 비용 절감
            - "supply_issue": 공급 문제
            - "natural_trend": 천연화 트렌드
            - "regulation": 규제 대응
            - "performance": 성능 개선

    Returns:
        대체 검토 결과
    """
    # 현재 원료 정보 조회
    current_spec = get_product_spec_by_inci(current_ingredient)

    # 대체 후보 탐색
    alternatives = find_alternatives(
        current_ingredient,
        criteria=get_criteria_by_reason(reason)
    )

    # 비교 분석
    comparison = {
        "current": current_spec,
        "alternatives": alternatives,
        "recommendation": analyze_best_alternative(
            current_spec, alternatives, reason
        )
    }

    return comparison
```

### Workflow 3: 공급사 평가

```python
def evaluate_supplier(supplier_name: str) -> Dict:
    """
    공급사 종합 평가

    Returns:
        {
            "basic_info": {...},
            "product_portfolio": [...],
            "certifications": [...],
            "strengths": [...],
            "considerations": [...],
            "similar_suppliers": [...]
        }
    """
    pass
```

## Best Practices

### 1. 검색 최적화
- **정확한 용어 사용**: INCI명, 화학명, 상품명 구분
- **기능 분류 활용**: 카테고리 필터로 검색 범위 축소
- **공급사 필터**: 알려진 공급사로 먼저 검색

### 2. TDS 검토 포인트
```
1. INCI명 및 CAS 번호 확인
2. 권장 사용량 확인
3. pH 호환성 체크
4. 가공 조건 (온도, 순서) 확인
5. 호환성/비호환성 정보
6. 보관 조건 및 유통기한
7. 규제 상태 (국가별)
```

### 3. 샘플 요청 시 주의사항
- **명확한 목적 기재**: 평가 목적 구체적 설명
- **적정 수량 요청**: 평가에 필요한 최소량
- **회사 정보 정확히**: 신뢰도 향상
- **후속 조치**: 평가 결과 피드백 제공

### 4. 가격 협상 참고
- UL Prospector 가격 정보는 참고용
- 실제 가격은 공급사 직접 협상
- MOQ, 납기, 결제 조건 확인 필수

## Free Tier 활용 팁

무료 계정으로도 다음 작업 가능:

1. **기본 검색**: 원료명, 기능별 검색
2. **공급사 확인**: 제품별 공급사 정보
3. **기본 TDS**: 로그인 후 일부 TDS 다운로드
4. **카테고리 브라우징**: 기능별 원료 탐색
5. **연락처 확인**: 공급사 기본 연락처

### 제한 우회 방법
- WebSearch로 공급사 직접 웹사이트 검색
- 공급사 뉴스레터/이벤트 구독
- 전시회/컨퍼런스 참가 시 명함 교환

## Premium 기능 가치 판단

### Premium 필요한 경우
- 월 50회 이상 검색 필요
- 다수 TDS/SDS 다운로드 필요
- 상세 스펙 비교 기능 필요
- API 연동 필요

### Free로 충분한 경우
- 간헐적 원료 검색
- 특정 공급사와 기존 거래 관계
- 소규모 R&D 팀

## Reference Files

상세 정보는 아래 참조 문서 확인:

| 파일 | 내용 |
|------|------|
| `references/prospector_features.md` | 플랫폼 기능 상세 |
| `references/supplier_database.md` | 공급사/제품 데이터베이스 구조 |
| `scripts/prospector_search.py` | 검색 유틸리티 스크립트 |

## Troubleshooting

### 문제: 검색 결과 없음
```
원인 1: 검색어 불일치
해결: INCI명/상품명/화학명 각각 검색 시도

원인 2: 카테고리 불일치
해결: "Personal Care" 외 다른 카테고리 확인

원인 3: 신규/마이너 제품
해결: 공급사 직접 웹사이트 검색
```

### 문제: TDS 다운로드 불가
```
원인 1: 로그인 필요
해결: 무료 계정 생성 후 로그인

원인 2: 프리미엄 전용 문서
해결: 공급사 직접 연락하여 요청

원인 3: 지역 제한
해결: VPN 사용 또는 다른 지역 포털 접속
```

### 문제: 공급사 연락처 없음
```
원인: 연락처 비공개 설정
해결:
1. 공급사 공식 웹사이트 검색
2. LinkedIn 담당자 검색
3. 전시회/컨퍼런스 참가
4. 한국 지사/대리점 검색
```

## Additional Resources

- **UL Prospector**: https://www.ulprospector.com/en/na/PersonalCare
- **Cosmetics & Toiletries**: https://www.cosmeticsandtoiletries.com/
- **in-cosmetics Global**: https://www.in-cosmetics.com/
- **공급사 협회**: PCPC, CEW, SCC

## Quick Reference

```python
# 원료 검색
results = search_prospector(ProspectorSearchParams(
    keyword="niacinamide",
    category="Personal Care",
    function="Skin Conditioning"
))

# 공급사 검색
suppliers = search_suppliers(
    keyword="vitamin c",
    region="Asia Pacific"
)

# 대체 원료 탐색
alternatives = find_alternatives(
    "DIMETHICONE",
    criteria={"natural_preferred": True}
)

# 샘플 요청
request = create_sample_request(SampleRequest(
    product_id="123456",
    product_name="Example Ingredient",
    supplier="Example Corp",
    quantity="500g",
    purpose="New product development"
))
```

## Summary

**ulprospector-integration** 스킬은 화장품 원료 소싱의 핵심 도구입니다:

1. **검색**: 기능/성분/공급사별 원료 탐색
2. **문서**: TDS/SDS 접근 및 분석
3. **비교**: 다중 제품 스펙 비교
4. **대체**: 대체 원료 탐색 및 평가
5. **소싱**: 샘플 요청 및 공급사 연락

효율적인 원료 소싱과 공급망 관리에 필수적인 플랫폼 연동 스킬입니다.
