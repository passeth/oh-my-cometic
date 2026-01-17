# GNPD (Global New Products Database) 주요 기능

## 데이터베이스 개요

Mintel GNPD는 1996년부터 글로벌 신제품 데이터를 수집해온 세계 최대의 소비재 신제품 데이터베이스입니다.

## 커버리지

### 지역별 커버리지
| 지역 | 국가 수 | 주요 국가 |
|------|---------|-----------|
| 아시아 태평양 | 15+ | 한국, 일본, 중국, 호주, 인도 |
| 유럽 | 25+ | 영국, 독일, 프랑스, 이탈리아, 스페인 |
| 북미 | 3 | 미국, 캐나다, 멕시코 |
| 남미 | 10+ | 브라질, 아르헨티나, 칠레 |
| 중동/아프리카 | 8+ | UAE, 사우디아라비아, 남아공 |

### 카테고리 커버리지

#### Beauty & Personal Care (BPC)
```
├── Skincare (스킨케어)
│   ├── Facial Care (페이셜 케어)
│   │   ├── Cleansers (클렌저)
│   │   ├── Toners (토너)
│   │   ├── Serums (세럼)
│   │   ├── Moisturizers (모이스처라이저)
│   │   ├── Masks (마스크)
│   │   ├── Eye Care (아이케어)
│   │   └── Lip Care (립케어)
│   ├── Sun Care (선케어)
│   ├── Body Care (바디케어)
│   └── Hand Care (핸드케어)
│
├── Haircare (헤어케어)
│   ├── Shampoo (샴푸)
│   ├── Conditioner (컨디셔너)
│   ├── Treatment (트리트먼트)
│   ├── Styling (스타일링)
│   └── Color (컬러)
│
├── Color Cosmetics (색조화장품)
│   ├── Face (페이스)
│   ├── Eyes (아이즈)
│   ├── Lips (립스)
│   └── Nails (네일)
│
├── Fragrance (향수)
│   ├── Women's (여성용)
│   ├── Men's (남성용)
│   └── Unisex (유니섹스)
│
└── Personal Care (퍼스널케어)
    ├── Bath & Shower (바스/샤워)
    ├── Deodorant (데오도란트)
    ├── Oral Care (구강케어)
    └── Men's Grooming (남성 그루밍)
```

## 제품 데이터 포인트

### 기본 정보
| 필드 | 설명 | 예시 |
|------|------|------|
| Product Name | 제품명 | "Cica Repair Serum" |
| Brand | 브랜드명 | "COSRX" |
| Company | 제조/판매사 | "COSRX Inc." |
| Launch Date | 출시일 | "2024-01-15" |
| Country | 출시국가 | "South Korea" |
| Category | 카테고리 | "Skincare > Serums" |
| Subcategory | 서브카테고리 | "Anti-aging" |

### 가격 정보
| 필드 | 설명 |
|------|------|
| Price (Local) | 현지 통화 가격 |
| Price (USD) | 미국 달러 환산 가격 |
| Price per Unit | 단위당 가격 |
| Price Positioning | 가격 포지셔닝 (Mass/Prestige) |

### 성분 정보
| 필드 | 설명 |
|------|------|
| Full Ingredient List | 전성분 (INCI 표기) |
| Key Ingredients | 주요 활성 성분 |
| Ingredient Count | 총 성분 수 |
| Hero Ingredients | 마케팅 강조 성분 |

### 클레임 정보
| 클레임 타입 | 예시 |
|-------------|------|
| Functional | 주름개선, 미백, 보습, 진정 |
| Certification | Vegan, Organic, Cruelty-free |
| Formulation | Fragrance-free, Alcohol-free |
| Sustainability | Recyclable, Refillable, Carbon Neutral |
| Target | For Sensitive Skin, For Oily Skin |
| Lifestyle | K-Beauty, J-Beauty, Clean Beauty |

### 포장 정보
| 필드 | 설명 |
|------|------|
| Pack Type | 용기 타입 (Pump, Tube, Jar 등) |
| Pack Size | 용량/중량 |
| Pack Material | 소재 (Glass, Plastic, Metal) |
| Sustainable Packaging | 지속가능 포장 여부 |
| Closure Type | 마개 타입 |

## 검색 및 필터 기능

### 기본 검색
- **키워드 검색**: 제품명, 브랜드, 성분명
- **불리언 검색**: AND, OR, NOT 연산자
- **와일드카드**: * 사용 가능

### 고급 필터
```
필터 카테고리:
├── 기간 (Date Range)
│   ├── 최근 1개월
│   ├── 최근 3개월
│   ├── 최근 6개월
│   ├── 최근 12개월
│   └── 사용자 정의
│
├── 지역/국가
│   ├── 대륙별
│   ├── 국가별
│   └── 경제권별 (APAC, EMEA, Americas)
│
├── 카테고리
│   ├── 대분류
│   ├── 중분류
│   └── 소분류
│
├── 가격대
│   ├── Mass (저가)
│   ├── Masstige (중저가)
│   ├── Prestige (프리미엄)
│   └── Super Premium (럭셔리)
│
├── 클레임
│   ├── 기능성 클레임
│   ├── 인증 클레임
│   └── 환경 클레임
│
└── 성분
    ├── 포함 성분
    └── 제외 성분
```

## 분석 도구

### 트렌드 분석
- **시계열 분석**: 기간별 출시 추이
- **성장률 분석**: YoY, QoQ 성장률
- **점유율 분석**: 브랜드/카테고리 점유율

### 비교 분석
- **지역 비교**: 국가/지역 간 비교
- **카테고리 비교**: 카테고리 간 비교
- **브랜드 비교**: 경쟁 브랜드 비교

### 시각화
- **차트 생성**: 라인, 바, 파이 차트
- **대시보드**: 커스텀 대시보드 생성
- **인포그래픽**: 프레젠테이션용 자료

## 내보내기 기능

### 내보내기 형식
| 형식 | 구독 티어 | 용도 |
|------|-----------|------|
| PDF | Standard | 리포트/발표 |
| Excel | Standard | 데이터 분석 |
| CSV | Professional | 대량 데이터 |
| PowerPoint | Professional | 프레젠테이션 |
| API | Enterprise | 시스템 연동 |

### 내보내기 제한
- Standard: 월 100건
- Professional: 월 500건
- Enterprise: 무제한

## 알림 기능

### 알림 설정
- 키워드 알림: 특정 키워드 신제품
- 브랜드 알림: 특정 브랜드 신제품
- 카테고리 알림: 특정 카테고리 신제품
- 성분 알림: 특정 성분 포함 제품

### 알림 빈도
- 실시간 (Enterprise)
- 일간 (Professional)
- 주간 (Standard)

## 데이터 품질

### 수집 방식
1. **현장 수집**: 전 세계 리서처 네트워크
2. **제조사 제출**: 브랜드 직접 등록
3. **이커머스 스크래핑**: 온라인 리테일러

### 검증 프로세스
1. 제품 실물 확인
2. 성분 정보 검증
3. 가격 정보 검증
4. 클레임 정확성 확인

### 데이터 업데이트
- 신제품: 출시 후 2-4주 내 등록
- 기존 제품: 연 1회 업데이트
- 단종 제품: 별도 표시

## 활용 사례

### R&D 활용
- 경쟁 제품 성분 분석
- 혁신 성분 트렌드 파악
- 제형/텍스처 트렌드 분석

### 마케팅 활용
- 클레임 트렌드 분석
- 가격 포지셔닝 전략
- 패키지 디자인 트렌드

### 전략 기획 활용
- 시장 진입 전략
- 포트폴리오 갭 분석
- 경쟁사 벤치마킹

## 구독 플랜

### Standard
- 기본 검색 및 필터
- 제한된 내보내기
- 월간 트렌드 리포트

### Professional
- 고급 검색 및 분석
- 확장된 내보내기
- 주간 알림

### Enterprise
- 전체 기능 접근
- API 연동
- 커스텀 리포트
- 전담 어카운트 매니저

## 관련 Mintel 서비스

- **Mintel Trends**: 글로벌 소비자 트렌드
- **Mintel Reports**: 시장 분석 리포트
- **Mintel Comperemedia**: 마케팅 캠페인 분석
- **Mintel Menu Insights**: F&B 메뉴 트렌드
