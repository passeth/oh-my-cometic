# 트렌드 카테고리 분류

GNPD 데이터 분석을 위한 트렌드 카테고리 체계입니다.

## 1. 제품 카테고리 분류

### Skincare (스킨케어)

#### Facial Care
```
├── Cleansers (클렌저)
│   ├── Foam Cleansers (폼 클렌저)
│   ├── Gel Cleansers (젤 클렌저)
│   ├── Oil Cleansers (오일 클렌저)
│   ├── Micellar Water (미셀라워터)
│   ├── Cleansing Balms (클렌징 밤)
│   ├── Cleansing Pads (클렌징 패드)
│   └── Enzyme Cleansers (효소 클렌저)
│
├── Toners (토너)
│   ├── Hydrating Toners (수분 토너)
│   ├── Exfoliating Toners (각질 토너)
│   ├── Essence Toners (에센스 토너)
│   └── Treatment Toners (트리트먼트 토너)
│
├── Serums & Treatments (세럼/트리트먼트)
│   ├── Anti-aging (안티에이징)
│   ├── Brightening (브라이트닝)
│   ├── Hydrating (하이드레이팅)
│   ├── Acne Treatment (여드름)
│   ├── Soothing (진정)
│   └── Ampoules (앰플)
│
├── Moisturizers (모이스처라이저)
│   ├── Creams (크림)
│   ├── Gels (젤)
│   ├── Lotions (로션)
│   └── Oil-free (오일프리)
│
├── Masks (마스크)
│   ├── Sheet Masks (시트마스크)
│   ├── Wash-off Masks (워시오프 마스크)
│   ├── Sleeping Masks (슬리핑 마스크)
│   ├── Peel-off Masks (필오프 마스크)
│   └── Clay Masks (클레이 마스크)
│
├── Eye Care (아이케어)
│   ├── Eye Creams (아이크림)
│   ├── Eye Serums (아이세럼)
│   └── Eye Masks (아이마스크)
│
└── Lip Care (립케어)
    ├── Lip Balms (립밤)
    ├── Lip Masks (립마스크)
    └── Lip Treatments (립트리트먼트)
```

#### Sun Care
```
├── Face Sunscreen (페이스 선크림)
│   ├── Physical/Mineral (물리적 차단)
│   ├── Chemical (화학적 차단)
│   └── Hybrid (하이브리드)
│
├── Body Sunscreen (바디 선크림)
├── Sunscreen Sticks (선스틱)
├── Sunscreen Sprays (선스프레이)
├── Sunscreen Cushions (선쿠션)
└── After Sun (애프터선)
```

### Haircare (헤어케어)

```
├── Shampoo
│   ├── Daily Use (데일리)
│   ├── Anti-Dandruff (비듬)
│   ├── Color Protection (컬러 보호)
│   ├── Scalp Care (두피 케어)
│   └── Hair Loss Prevention (탈모 방지)
│
├── Conditioner
│   ├── Rinse-off (린스오프)
│   └── Leave-in (리브인)
│
├── Treatment
│   ├── Hair Masks (헤어마스크)
│   ├── Hair Oils (헤어오일)
│   └── Scalp Treatments (두피 트리트먼트)
│
└── Styling
    ├── Sprays (스프레이)
    ├── Wax/Pomade (왁스/포마드)
    └── Serums (세럼)
```

### Color Cosmetics (색조화장품)

```
├── Face
│   ├── Foundation (파운데이션)
│   ├── BB/CC Cream (BB/CC 크림)
│   ├── Primer (프라이머)
│   ├── Concealer (컨실러)
│   ├── Powder (파우더)
│   ├── Blush (블러쉬)
│   ├── Bronzer (브론저)
│   └── Highlighter (하이라이터)
│
├── Eyes
│   ├── Eyeshadow (아이섀도우)
│   ├── Eyeliner (아이라이너)
│   ├── Mascara (마스카라)
│   └── Eyebrow (아이브로우)
│
├── Lips
│   ├── Lipstick (립스틱)
│   ├── Lip Gloss (립글로스)
│   ├── Lip Tint (립틴트)
│   └── Lip Liner (립라이너)
│
└── Nails
    ├── Nail Polish (네일폴리시)
    └── Nail Care (네일케어)
```

## 2. 클레임 트렌드 분류

### Efficacy Claims (효능 클레임)

```
├── Anti-aging (안티에이징)
│   ├── Anti-wrinkle (주름개선)
│   ├── Firming (탄력)
│   ├── Lifting (리프팅)
│   └── Collagen Boosting (콜라겐 부스팅)
│
├── Brightening (브라이트닝)
│   ├── Whitening (미백)
│   ├── Dark Spot (다크스팟)
│   ├── Tone Correction (톤보정)
│   └── Radiance (광채)
│
├── Hydrating (수분)
│   ├── Moisturizing (보습)
│   ├── Deep Hydration (딥하이드레이션)
│   └── Barrier Repair (장벽 회복)
│
├── Soothing (진정)
│   ├── Calming (카밍)
│   ├── Anti-redness (안티레드니스)
│   └── Sensitive Skin (민감성 피부)
│
└── Acne/Blemish (여드름/트러블)
    ├── Acne Fighting (여드름 케어)
    ├── Pore Care (모공 케어)
    └── Oil Control (유분 조절)
```

### Certification Claims (인증 클레임)

```
├── Animal Welfare
│   ├── Vegan (비건)
│   ├── Cruelty-free (크루얼티프리)
│   └── Leaping Bunny Certified
│
├── Organic/Natural
│   ├── USDA Organic
│   ├── ECOCERT
│   ├── COSMOS Organic
│   ├── NATRUE
│   └── EWG Verified
│
├── Sustainability
│   ├── B Corp Certified
│   ├── Fair Trade
│   ├── Rainforest Alliance
│   └── Climate Neutral
│
└── Halal/Kosher
    ├── Halal Certified
    └── Kosher Certified
```

### Formulation Claims (제형 클레임)

```
├── Free-from Claims
│   ├── Fragrance-free (무향)
│   ├── Alcohol-free (무알콜)
│   ├── Paraben-free (파라벤프리)
│   ├── Sulfate-free (설페이트프리)
│   ├── Silicone-free (실리콘프리)
│   └── Oil-free (오일프리)
│
├── Hypoallergenic (저자극)
│   ├── Dermatologically Tested (피부과 테스트)
│   └── For Sensitive Skin (민감성 피부용)
│
└── Texture/Format
    ├── Lightweight (가벼운)
    ├── Non-greasy (번들거리지 않는)
    ├── Fast-absorbing (빠른 흡수)
    └── Multi-functional (다기능)
```

### Sustainability Claims (지속가능성 클레임)

```
├── Packaging
│   ├── Recyclable (재활용 가능)
│   ├── Recycled Materials (재활용 소재)
│   ├── Refillable (리필)
│   ├── Plastic-free (플라스틱프리)
│   └── Ocean Plastic (해양 플라스틱)
│
├── Sourcing
│   ├── Sustainably Sourced (지속가능 원료)
│   ├── Upcycled Ingredients (업사이클 성분)
│   └── Local Sourcing (로컬 소싱)
│
└── Carbon/Water
    ├── Carbon Neutral (탄소 중립)
    ├── Carbon Negative (탄소 네거티브)
    ├── Water-saving (물 절약)
    └── Waterless (워터리스)
```

## 3. 성분 트렌드 분류

### Hero Ingredients by Function

#### Anti-aging
| 성분 | 트렌드 | 성장률 |
|------|--------|--------|
| Retinol/Retinoids | 지속 성장 | +15% |
| Peptides | 급성장 | +25% |
| Bakuchiol | 신규 성장 | +40% |
| Collagen | 안정 | +5% |
| Adenosine | 안정 | +8% |

#### Hydrating
| 성분 | 트렌드 | 성장률 |
|------|--------|--------|
| Hyaluronic Acid | 주류 | +10% |
| Ceramides | 성장 | +18% |
| Squalane | 성장 | +20% |
| Glycerin | 안정 | +3% |
| Panthenol | 성장 | +15% |

#### Brightening
| 성분 | 트렌드 | 성장률 |
|------|--------|--------|
| Niacinamide | 급성장 | +30% |
| Vitamin C | 주류 | +12% |
| Alpha Arbutin | 성장 | +22% |
| Tranexamic Acid | 신규 성장 | +35% |
| Glutathione | 성장 | +18% |

#### Soothing
| 성분 | 트렌드 | 성장률 |
|------|--------|--------|
| Centella Asiatica (CICA) | 주류 | +20% |
| Aloe Vera | 안정 | +5% |
| Mugwort (쑥) | 성장 | +25% |
| Tea Tree | 안정 | +8% |
| Calendula | 성장 | +15% |

### Emerging Ingredients (신규 트렌드 성분)

```
2024-2025 주목 성분:
├── Postbiotics (포스트바이오틱스)
├── Ectoin (엑토인)
├── Polyglutamic Acid (PGA)
├── Adaptogens (어댑토겐)
│   ├── Ashwagandha
│   ├── Reishi Mushroom
│   └── Rhodiola
├── Blue Light Protection (블루라이트 차단)
│   ├── Lutein
│   └── Zeaxanthin
└── Microbiome-focused (마이크로바이옴)
    ├── Prebiotics
    ├── Probiotics
    └── Synbiotics
```

## 4. 지역별 트렌드 특성

### Asia-Pacific

#### Korea (한국)
- **주요 트렌드**: 스킵케어, 비건뷰티, 클린뷰티
- **인기 카테고리**: 선케어, 토너, 앰플
- **특징**: 혁신 선도, 빠른 트렌드 변화

#### Japan (일본)
- **주요 트렌드**: 안티폴루션, 센서티브케어, 미니멀
- **인기 카테고리**: 선케어, 클렌저, 에센스
- **특징**: 품질 중심, 기능성 강조

#### China (중국)
- **주요 트렌드**: C-Beauty, 허브 성분, 럭셔리
- **인기 카테고리**: 마스크, 세럼, 선케어
- **특징**: 대규모 시장, 빠른 성장

### Europe

#### Western Europe
- **주요 트렌드**: 지속가능성, 클린뷰티, 미니멀
- **인기 카테고리**: 스킨케어, 향수, 헤어케어
- **특징**: 규제 선도, 환경 중심

#### UK
- **주요 트렌드**: 비건, 인디 브랜드, 멀티펑셔널
- **인기 카테고리**: 스킨케어, 색조, 헤어케어
- **특징**: 트렌드 민감, 인디 브랜드 선호

### Americas

#### USA
- **주요 트렌드**: 클린뷰티, 인클루시브, 웰니스
- **인기 카테고리**: 스킨케어, 선케어, 헤어케어
- **특징**: 대중 시장, 다양성 강조

#### Brazil
- **주요 트렌드**: 헤어케어, 바디케어, 자연 성분
- **인기 카테고리**: 헤어케어, 바디케어, 향수
- **특징**: 헤어 중심, 자연 지향

## 5. 가격대 분류

### Price Segments

| 세그먼트 | 가격대 (USD) | 특징 |
|----------|--------------|------|
| Mass | $0-15 | 드럭스토어, 마트 |
| Masstige | $15-35 | 프리미엄 매스 |
| Prestige | $35-75 | 백화점, 세포라 |
| Luxury | $75-150 | 럭셔리 브랜드 |
| Super Premium | $150+ | 울트라 럭셔리 |

### Price Trend Analysis

```
가격대별 성장률 (2023-2024):
├── Mass: +3% (안정)
├── Masstige: +12% (성장)
├── Prestige: +8% (성장)
├── Luxury: +5% (안정)
└── Super Premium: +15% (급성장)
```

## 6. 트렌드 분석 프레임워크

### 트렌드 수명 주기

```
1. Emerging (신규): 0-2% 시장 점유
2. Growing (성장): 2-10% 시장 점유
3. Mainstream (주류): 10-30% 시장 점유
4. Mature (성숙): 30%+ 시장 점유
5. Declining (하락): 감소 추세
```

### 트렌드 확산 경로

```
일반적 확산:
한국 → 아시아 → 글로벌 (K-Beauty 트렌드)

대안적 확산:
유럽 → 글로벌 (지속가능성 트렌드)
미국 → 글로벌 (클린뷰티 트렌드)
```

### 트렌드 분석 지표

| 지표 | 설명 | 해석 |
|------|------|------|
| YoY Growth | 전년 대비 성장률 | +20% 이상 = 급성장 |
| Share of NPD | 신제품 비중 | 5% 이상 = 주목 트렌드 |
| Regional Spread | 지역 확산도 | 3개+ 지역 = 글로벌 트렌드 |
| Brand Adoption | 브랜드 채택률 | 주요 브랜드 10+ = 메인스트림 |
