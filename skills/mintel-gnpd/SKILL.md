---
name: Mintel GNPD
category: cosmetic-databases
description: 글로벌 신제품 트렌드 분석
tools:
  - WebFetch
  - WebSearch
---

# Mintel GNPD (Global New Products Database) Skill

Mintel GNPD를 활용한 글로벌 화장품 신제품 트렌드 분석 스킬입니다.

## 개요

Mintel GNPD는 전 세계 86개국 이상의 신제품 출시 정보를 수집하는 데이터베이스로, 화장품 기획자와 마케터에게 필수적인 트렌드 인사이트를 제공합니다.

## 주요 기능

### 1. 신제품 모니터링
- 86개국 이상의 일일 신제품 업데이트
- 뷰티 & 퍼스널케어 카테고리 전문 트래킹
- 경쟁사 제품 출시 모니터링

### 2. 트렌드 분석
- 성분 트렌드 (Ingredient Trends)
- 클레임 트렌드 (Claim Trends)
- 포장 트렌드 (Packaging Trends)
- 가격대별 포지셔닝

### 3. 시장 비교
- 지역별 시장 비교 (아시아, 유럽, 북미 등)
- 국가별 출시 현황
- 카테고리별 성장률 분석

### 4. 벤치마킹
- 브랜드별 포트폴리오 분석
- 카테고리 리더 분석
- 혁신 제품 사례 연구

## 데이터 포인트

GNPD에서 추출 가능한 주요 데이터:

```
제품 정보:
- 제품명, 브랜드, 제조사
- 출시일, 출시 국가
- 가격 (현지 통화 및 USD)
- 제품 설명 및 마케팅 카피

성분 정보:
- 전성분 리스트 (INCI)
- 주요 활성 성분
- 성분 기능 분류

클레임 정보:
- 기능성 클레임
- 인증 클레임 (Vegan, Organic 등)
- 환경/지속가능성 클레임
- 타겟 소비자 클레임

포장 정보:
- 용기 타입
- 용량/중량
- 포장 소재
- 지속가능 포장 여부
```

## 활용 시나리오

### 시나리오 1: 신제품 기획
```
사용자: "2024년 한국 클렌저 시장 트렌드 분석해줘"

분석 항목:
1. 최근 6개월 클렌저 신제품 출시 현황
2. 상위 클레임 (저자극, 약산성, 비건 등)
3. 인기 성분 (CICA, 녹차, 효소 등)
4. 가격대별 분포
5. 혁신 제품 사례
```

### 시나리오 2: 경쟁사 분석
```
사용자: "이니스프리 최근 출시 제품 분석"

분석 항목:
1. 최근 12개월 출시 제품 리스트
2. 카테고리별 분포
3. 가격 전략
4. 주요 성분/클레임 패턴
5. 포장 전략
```

### 시나리오 3: 글로벌 확장
```
사용자: "일본 vs 한국 선케어 시장 비교"

분석 항목:
1. 출시 제품 수 비교
2. SPF/PA 분포
3. 제형 선호도 (크림, 에센스, 스틱 등)
4. 가격대 비교
5. 클레임 차이점
```

## 접근 방법

### 유료 구독 (Full Access)
- 전체 데이터베이스 접근
- 고급 필터링 및 검색
- 데이터 다운로드 (Excel, CSV)
- API 접근 (엔터프라이즈)
- 커스텀 리포트 생성

### 무료 접근 (Limited)
- Mintel 웹사이트 공개 리포트
- 프레스 릴리즈
- 트렌드 아티클 (일부)

## 대체 무료 소스

GNPD 구독이 없는 경우 활용 가능한 대체 소스:

### 1. 공개 트렌드 리포트
- Mintel Press Office (무료 리포트 요약)
- Cosmetics Design (업계 뉴스)
- Global Cosmetic Industry
- Beauty Independent

### 2. 소셜 트렌드
- Instagram/TikTok 해시태그 분석
- Reddit (r/SkincareAddiction, r/AsianBeauty)
- YouTube 뷰티 크리에이터

### 3. 이커머스 데이터
- 올리브영 베스트셀러
- Amazon Best Sellers (Beauty)
- Sephora New Arrivals
- 큐텐 뷰티 랭킹

### 4. 브랜드 직접 모니터링
- 브랜드 공식 사이트
- 브랜드 SNS 계정
- 신제품 발표 뉴스

## 스크립트 활용

### 트렌드 분석 스크립트
```python
# scripts/trend_analyzer.py 활용

from trend_analyzer import TrendAnalyzer

analyzer = TrendAnalyzer()

# 카테고리별 트렌드 분석
skincare_trends = analyzer.analyze_category(
    category="skincare",
    subcategory="serums",
    region="asia-pacific",
    period="6m"
)

# 성분 트렌드 분석
ingredient_trends = analyzer.analyze_ingredients(
    category="skincare",
    top_n=20,
    growth_filter=True
)

# 클레임 트렌드 분석
claim_trends = analyzer.analyze_claims(
    category="skincare",
    claim_type="sustainability",
    region="global"
)
```

## 데이터 해석 가이드

### 트렌드 지표 해석
- **Growth Rate > 20%**: 급성장 트렌드, 빠른 대응 필요
- **Growth Rate 10-20%**: 안정 성장, 중기 기획 적합
- **Growth Rate 5-10%**: 성숙 트렌드, 차별화 필요
- **Growth Rate < 5%**: 포화 또는 하락, 혁신 필요

### 지역별 특성
- **한국**: 혁신 리더, 6개월~1년 후 글로벌 확산
- **일본**: 품질/기능 중심, 안정적 시장
- **미국**: 대중 시장, 클린/비건 강세
- **유럽**: 규제 선도, 지속가능성 중심
- **중국**: 대규모 시장, C-Beauty 성장

## 레퍼런스 문서

- [GNPD 주요 기능](references/gnpd_features.md)
- [트렌드 카테고리 분류](references/trend_categories.md)

## 주의사항

1. **데이터 정확성**: GNPD 데이터는 제조사 공개 정보 기반
2. **시차**: 데이터 입력까지 2-4주 소요 가능
3. **지역 편차**: 일부 국가는 커버리지 낮음
4. **저작권**: 데이터 외부 공유 시 라이선스 확인 필요

## 관련 스킬

- [CosDNA Analyzer](../cosdna-analyzer/SKILL.md) - 성분 분석
- [EWG Database](../ewg-database/SKILL.md) - 안전성 데이터
- [Ingredient Trend Tracker](../ingredient-trends/SKILL.md) - 성분 트렌드
