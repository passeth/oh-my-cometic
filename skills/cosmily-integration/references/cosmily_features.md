# Cosmily Platform Features

Cosmily 플랫폼의 주요 기능 및 데이터 구조 상세 문서

## Platform Overview

**Cosmily**는 화장품 성분 정보를 제공하는 종합 플랫폼으로, 소비자와 처방 개발자 모두를 위한 성분 데이터베이스를 제공합니다.

### 핵심 서비스

| 서비스 | 설명 | 대상 사용자 |
|--------|------|-------------|
| **Ingredient Database** | 성분별 상세 정보 | 소비자, 개발자 |
| **Product Analyzer** | 제품 성분 분석 | 소비자 |
| **Formula Builder** | 처방 설계 도구 | 개발자 |
| **Skincare Routine** | 스킨케어 루틴 추천 | 소비자 |
| **Compatibility Checker** | 성분 호환성 확인 | 소비자, 개발자 |

## Ingredient Database

### 데이터 항목

각 성분에 대해 제공되는 정보:

```yaml
Ingredient Profile:
  identification:
    - inci_name: 공식 INCI 명칭
    - common_names: 일반명/별명 목록
    - cas_number: CAS 등록 번호
    - ec_number: EC 번호 (EU)
    - chemical_formula: 분자식

  safety:
    - overall_rating: A-F 등급
    - safety_score: 0-100 점수
    - comedogenic_rating: 0-5 (면포 형성도)
    - irritancy_rating: 0-5 (자극성)
    - concerns: 우려 사항 목록
    - benefits: 효능 목록

  functionality:
    - primary_functions: 주요 기능
    - secondary_functions: 부가 기능
    - product_types: 적합 제품 유형

  usage:
    - recommended_concentration: 권장 농도 범위
    - optimal_ph: 최적 pH 범위
    - stability: 안정성 정보
    - compatibility_notes: 호환성 메모

  regulatory:
    - eu_status: EU 규제 상태
    - fda_status: FDA 규제 상태
    - restrictions: 사용 제한 사항

  sources:
    - natural_sources: 천연 원료원
    - synthetic_available: 합성 가능 여부
    - vegan_status: 비건 여부
    - sustainability: 지속가능성 정보
```

### 안전성 등급 체계

#### Letter Grade (A-F)

```python
SAFETY_GRADES = {
    "A": {
        "description": "Excellent",
        "score_range": (90, 100),
        "meaning": "매우 안전한 성분. 알려진 우려 사항 없음",
        "recommendation": "모든 피부 타입에 안전하게 사용 가능"
    },
    "B": {
        "description": "Good",
        "score_range": (70, 89),
        "meaning": "안전한 성분. 경미한 주의사항 있을 수 있음",
        "recommendation": "대부분의 경우 안전하게 사용 가능"
    },
    "C": {
        "description": "Average",
        "score_range": (50, 69),
        "meaning": "보통 수준. 일부 피부에 민감 반응 가능",
        "recommendation": "민감성 피부는 패치 테스트 권장"
    },
    "D": {
        "description": "Below Average",
        "score_range": (30, 49),
        "meaning": "주의 필요. 잠재적 자극/민감 우려",
        "recommendation": "대안 검토 권장, 필요시 낮은 농도로 사용"
    },
    "F": {
        "description": "Poor",
        "score_range": (0, 29),
        "meaning": "우려됨. 상당한 안전성 이슈",
        "recommendation": "사용 회피 권장, 필수 시 전문가 상담"
    }
}
```

#### 점수 산정 요소

```python
SCORING_FACTORS = {
    "toxicity_data": 25,        # 독성 연구 결과
    "sensitization": 20,        # 민감성/알레르기 위험
    "irritation": 15,           # 자극성
    "comedogenicity": 10,       # 면포 형성 가능성
    "environmental": 10,        # 환경적 우려
    "regulatory": 10,           # 규제 기관 평가
    "clinical_evidence": 10,    # 임상 근거
}
```

### 코메도제닉 등급 (0-5)

```python
COMEDOGENIC_RATINGS = {
    0: "Non-Comedogenic - 모공을 막지 않음",
    1: "Slightly Comedogenic - 매우 낮은 모공 폐쇄 가능성",
    2: "Moderately Low - 낮은 모공 폐쇄 가능성",
    3: "Moderate - 중간 수준 모공 폐쇄 가능성",
    4: "Fairly High - 높은 모공 폐쇄 가능성",
    5: "Highly Comedogenic - 모공 폐쇄 위험 높음",
}
```

### 자극성 등급 (0-5)

```python
IRRITANCY_RATINGS = {
    0: "Non-Irritating - 자극성 없음",
    1: "Very Low - 매우 낮은 자극성",
    2: "Low - 낮은 자극성",
    3: "Moderate - 중간 자극성",
    4: "High - 높은 자극성",
    5: "Very High - 매우 높은 자극성",
}
```

## Function Categories

### 주요 기능 분류

```python
FUNCTION_CATEGORIES = {
    # 피부 컨디셔닝
    "skin_conditioning": {
        "Humectant": "수분을 끌어당기고 유지",
        "Emollient": "피부를 부드럽고 유연하게",
        "Occlusive": "수분 증발 방지",
        "Moisturizer": "피부 수분 공급",
        "Skin Conditioning": "피부 상태 개선",
    },

    # 활성 성분
    "actives": {
        "Anti-Aging": "노화 방지/개선",
        "Brightening": "피부 톤 개선",
        "Acne-Fighting": "여드름 관리",
        "Exfoliant": "각질 제거",
        "Antioxidant": "산화 방지",
        "Anti-Inflammatory": "염증 진정",
        "Skin Repairing": "피부 장벽 회복",
    },

    # 제형 기능
    "formulation": {
        "Surfactant": "계면활성/세정",
        "Emulsifier": "유화제",
        "Thickener": "점도 증가",
        "Solvent": "용매",
        "pH Adjuster": "pH 조절",
        "Chelating Agent": "금속이온 봉쇄",
        "Viscosity Controller": "점도 조절",
    },

    # 보존/안정화
    "preservation": {
        "Preservative": "미생물 성장 방지",
        "Antioxidant": "산화 방지 (제형)",
        "Stabilizer": "제형 안정화",
        "UV Stabilizer": "자외선 안정제",
    },

    # 감각적 기능
    "sensory": {
        "Fragrance": "향료",
        "Colorant": "착색제",
        "Opacifier": "불투명화",
        "Pearlescent": "펄 효과",
    },

    # 특수 기능
    "special": {
        "UV Filter": "자외선 차단",
        "Film Former": "피막 형성",
        "Hair Conditioning": "모발 컨디셔닝",
        "Nail Care": "손톱 관리",
    },
}
```

## Product Analysis

### 분석 항목

제품 분석 시 확인하는 요소:

```yaml
Product Analysis:
  overall_assessment:
    - safety_score: 전체 안전성 점수
    - efficacy_potential: 예상 효능 수준
    - formulation_quality: 처방 품질 평가
    - clean_beauty_status: 클린뷰티 적합성

  ingredient_breakdown:
    - active_ingredients: 활성 성분 목록
    - beneficial_ingredients: 효능 성분 목록
    - filler_ingredients: 기본 성분 목록
    - concerning_ingredients: 우려 성분 목록

  skin_type_suitability:
    - oily: 지성 피부 적합도
    - dry: 건성 피부 적합도
    - combination: 복합성 피부 적합도
    - sensitive: 민감성 피부 적합도
    - acne_prone: 여드름성 피부 적합도

  concerns:
    - potential_irritants: 잠재적 자극 성분
    - allergens: 알레르겐
    - comedogenic_ingredients: 면포 유발 성분
    - controversial_ingredients: 논란 성분

  recommendations:
    - usage_tips: 사용 팁
    - compatible_products: 호환 제품 유형
    - avoid_with: 함께 사용 피해야 할 성분
```

### 처방 품질 평가 기준

```python
FORMULATION_QUALITY_CRITERIA = {
    "ingredient_order": {
        "description": "성분 배치 순서 적절성",
        "weight": 15,
        "criteria": "활성 성분이 목록 상위에 위치"
    },
    "function_balance": {
        "description": "기능적 균형",
        "weight": 20,
        "criteria": "필수 기능들이 적절히 포함"
    },
    "safety_profile": {
        "description": "안전성 프로파일",
        "weight": 30,
        "criteria": "우려 성분 최소화"
    },
    "ingredient_quality": {
        "description": "성분 품질",
        "weight": 20,
        "criteria": "효과적인 성분 사용"
    },
    "compatibility": {
        "description": "성분 호환성",
        "weight": 15,
        "criteria": "성분 간 상호작용 문제 없음"
    },
}
```

## Compatibility System

### 호환성 분류

```python
COMPATIBILITY_STATUS = {
    "COMPATIBLE": {
        "symbol": "✓",
        "color": "green",
        "description": "함께 사용 가능",
        "action": "안전하게 조합 가능"
    },
    "CAUTION": {
        "symbol": "⚠",
        "color": "yellow",
        "description": "주의 필요",
        "action": "조건부 사용 (농도/pH/타이밍 조절)"
    },
    "INCOMPATIBLE": {
        "symbol": "✗",
        "color": "red",
        "description": "비호환",
        "action": "함께 사용 비권장"
    },
    "UNKNOWN": {
        "symbol": "?",
        "color": "gray",
        "description": "정보 부족",
        "action": "추가 조사 필요"
    },
}
```

### 알려진 비호환 조합

```python
KNOWN_INCOMPATIBILITIES = [
    {
        "ingredients": ["RETINOL", "BENZOYL PEROXIDE"],
        "reason": "레티놀 비활성화",
        "severity": "HIGH",
        "solution": "아침/저녁 분리 사용"
    },
    {
        "ingredients": ["VITAMIN C (ASCORBIC ACID)", "NIACINAMIDE"],
        "reason": "과거 우려 (현재 논란됨)",
        "severity": "LOW",
        "solution": "일반적으로 함께 사용 가능, 민감 피부는 분리"
    },
    {
        "ingredients": ["AHA/BHA", "RETINOL"],
        "reason": "과다 자극 가능",
        "severity": "MEDIUM",
        "solution": "다른 날 교대 사용 또는 낮은 농도"
    },
    {
        "ingredients": ["VITAMIN C", "AHA/BHA"],
        "reason": "pH 충돌 가능",
        "severity": "MEDIUM",
        "solution": "사이에 대기 시간 두기"
    },
    {
        "ingredients": ["RETINOL", "AHA"],
        "reason": "피부 자극 증가",
        "severity": "MEDIUM",
        "solution": "교대 사용 또는 농도 조절"
    },
]
```

### pH 기반 호환성

```python
PH_COMPATIBILITY_NOTES = {
    "acidic_actives": {
        "ingredients": ["ASCORBIC ACID", "GLYCOLIC ACID", "SALICYLIC ACID"],
        "optimal_ph": (2.5, 4.0),
        "note": "낮은 pH에서 효과적, 알칼리 성분과 분리"
    },
    "neutral_actives": {
        "ingredients": ["NIACINAMIDE", "HYALURONIC ACID", "PEPTIDES"],
        "optimal_ph": (5.0, 7.0),
        "note": "중성 pH에서 안정적"
    },
    "ph_sensitive": {
        "ingredients": ["RETINOL", "BAKUCHIOL"],
        "optimal_ph": (5.5, 6.5),
        "note": "약산성에서 최적, 극단적 pH 회피"
    },
}
```

## User Features

### 스킨케어 루틴 빌더

```yaml
Routine Builder:
  inputs:
    - skin_type: 피부 타입
    - skin_concerns: 피부 고민 목록
    - current_products: 현재 사용 제품
    - sensitivity_level: 민감도 수준
    - budget: 예산 범위

  outputs:
    - morning_routine: AM 루틴 추천
    - evening_routine: PM 루틴 추천
    - product_recommendations: 제품 추천
    - ingredient_suggestions: 성분 추천
    - avoid_list: 피해야 할 성분

  routine_structure:
    morning:
      1. Cleanser
      2. Toner (optional)
      3. Essence (optional)
      4. Serum
      5. Moisturizer
      6. Sunscreen

    evening:
      1. Oil Cleanser (if wearing makeup)
      2. Water Cleanser
      3. Toner (optional)
      4. Treatment (actives)
      5. Serum
      6. Moisturizer
      7. Sleeping Mask (optional)
```

### 제품 비교 기능

```python
COMPARISON_METRICS = {
    "safety": {
        "weight": 30,
        "metrics": ["overall_rating", "concerning_ingredients_count"]
    },
    "efficacy": {
        "weight": 25,
        "metrics": ["active_concentration", "beneficial_ingredients"]
    },
    "value": {
        "weight": 20,
        "metrics": ["price_per_ml", "ingredient_quality_ratio"]
    },
    "suitability": {
        "weight": 25,
        "metrics": ["skin_type_match", "concern_targeting"]
    },
}
```

## Data Sources

### Cosmily 데이터 출처

```yaml
Data Sources:
  scientific:
    - PubMed research papers
    - CIR (Cosmetic Ingredient Review) reports
    - SCCS (Scientific Committee on Consumer Safety) opinions
    - Toxicology databases

  regulatory:
    - EU CosIng database
    - FDA ingredient lists
    - ASEAN Cosmetic Directive
    - Health Canada cosmetic regulations

  industry:
    - PCPC (Personal Care Products Council)
    - Supplier safety data sheets
    - Clinical study results
    - Patent literature

  community:
    - User reviews and feedback
    - Dermatologist recommendations
    - Beauty community insights
    - Brand information
```

## API-like Endpoints

Cosmily 웹사이트의 주요 접근 경로:

```
# 성분 관련
/ingredients                    # 성분 목록
/ingredients/{slug}             # 성분 상세
/ingredients?search={query}     # 성분 검색
/ingredients?function={func}    # 기능별 필터

# 제품 관련
/products                       # 제품 목록
/products/{slug}                # 제품 상세
/products/analyze               # 제품 분석 (POST)

# 도구
/tools/compatibility-checker    # 호환성 검사
/tools/routine-builder          # 루틴 빌더
/tools/formula-analyzer         # 처방 분석

# 사용자
/account/favorites              # 즐겨찾기
/account/routine                # 내 루틴
/account/skin-profile           # 피부 프로필
```

## Limitations

### 플랫폼 제한사항

```yaml
Limitations:
  data_coverage:
    - 모든 성분이 등록되어 있지 않음
    - 새로운 성분 추가에 지연 있음
    - 일부 성분 데이터 불완전

  accuracy:
    - 커뮤니티 기반 데이터 포함 (검증 필요)
    - 규제 정보 업데이트 지연 가능
    - 지역별 규제 차이 미반영 가능

  functionality:
    - 공식 API 미제공
    - 대량 데이터 추출 제한
    - 실시간 업데이트 확인 어려움

  regional:
    - 주로 미국/유럽 기준
    - 아시아 규제 정보 제한적
    - 다국어 지원 제한
```

## Best Use Cases

### Cosmily 활용 최적 시나리오

1. **빠른 성분 안전성 스크리닝**
   - 신규 원료 초기 평가
   - 소비자 문의 대응

2. **처방 비교 분석**
   - 경쟁 제품 분석
   - 벤치마킹

3. **클린뷰티 적합성 확인**
   - 성분 안전성 프로파일
   - 대체 원료 탐색

4. **소비자 교육 자료**
   - 성분 정보 제공
   - 효능 설명

5. **처방 개선 아이디어**
   - 기능별 성분 검색
   - 호환성 확인
