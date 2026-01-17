# 화장품 성분 PubMed 검색 전략 가이드

## 1. 기본 검색 전략

### 성분명 검색 패턴

#### INCI명 vs 일반명
```
# INCI명 (정확한 매칭)
"NIACINAMIDE"[Title/Abstract]

# 일반명 (동의어 포함)
(niacinamide OR "nicotinic acid amide" OR "vitamin B3")[Title/Abstract]
```

#### 동의어 확장 예시
| 성분 | 검색어 확장 |
|-----|-----------|
| Vitamin C | ascorbic acid OR "vitamin C" OR L-ascorbic acid |
| Vitamin E | tocopherol OR "vitamin E" OR alpha-tocopherol |
| Retinol | retinol OR "vitamin A" OR retinoid* |
| AHA | "alpha hydroxy acid" OR glycolic acid OR lactic acid |
| BHA | "beta hydroxy acid" OR "salicylic acid" |

### 피부/화장품 필터
```
# 기본 필터
(skin OR dermatology OR cosmetic OR topical OR cutaneous)

# 확장 필터
(
  skin[Title/Abstract] OR
  dermatology[MeSH Terms] OR
  cosmetic*[Title/Abstract] OR
  topical[Title/Abstract] OR
  cutaneous[Title/Abstract] OR
  skincare[Title/Abstract] OR
  facial[Title/Abstract]
)
```

## 2. 효능별 검색 전략

### Anti-Aging (항노화)
```
검색어 조합:
(aging OR wrinkle* OR "fine lines" OR collagen OR elastin OR elasticity OR
 "skin firmness" OR "photoaging" OR "chronological aging" OR
 "intrinsic aging" OR "extrinsic aging")

고급 검색:
{ingredient}[Title/Abstract] AND
(aging[MeSH Terms] OR "skin aging"[MeSH Terms]) AND
(efficacy OR effect* OR treatment)
```

### Brightening (미백/브라이트닝)
```
검색어 조합:
(whitening OR brightening OR "skin lightening" OR melanin OR
 tyrosinase OR pigmentation OR hyperpigmentation OR "dark spots" OR
 "melasma" OR "age spots" OR "uneven skin tone")

고급 검색:
{ingredient}[Title/Abstract] AND
(melanin[MeSH Terms] OR hyperpigmentation[MeSH Terms]) AND
(inhibit* OR reduc* OR suppress*)
```

### Moisturizing (보습)
```
검색어 조합:
(hydration OR moisturiz* OR "skin barrier" OR TEWL OR
 "transepidermal water loss" OR "water retention" OR "skin hydration" OR
 ceramide* OR "natural moisturizing factor" OR NMF)

고급 검색:
{ingredient}[Title/Abstract] AND
("skin barrier"[Title/Abstract] OR hydration[Title/Abstract]) AND
(improv* OR enhanc* OR maintain*)
```

### Anti-Acne (항여드름)
```
검색어 조합:
(acne OR sebum OR "sebaceous gland" OR comedone* OR
 "propionibacterium acnes" OR "cutibacterium acnes" OR
 pimple* OR "oily skin" OR "acne vulgaris")

고급 검색:
{ingredient}[Title/Abstract] AND
(acne vulgaris[MeSH Terms] OR sebum[Title/Abstract]) AND
(treatment OR therap* OR reduc*)
```

### Antioxidant (항산화)
```
검색어 조합:
(antioxidant* OR "oxidative stress" OR "free radical*" OR ROS OR
 "reactive oxygen species" OR "lipid peroxidation" OR
 "oxidative damage" OR "UV protection" OR photoprotect*)

고급 검색:
{ingredient}[Title/Abstract] AND
(antioxidants[MeSH Terms] OR "oxidative stress"[MeSH Terms]) AND
(skin OR dermal OR cutaneous)
```

### Anti-Inflammatory (항염)
```
검색어 조합:
(anti-inflammatory OR inflammation OR "inflammatory response" OR
 cytokine* OR interleukin* OR TNF-alpha OR NF-kB OR
 redness OR erythema OR soothing OR calming)

고급 검색:
{ingredient}[Title/Abstract] AND
(inflammation[MeSH Terms] OR "skin inflammation"[Title/Abstract]) AND
(inhibit* OR suppress* OR reduc*)
```

## 3. 연구 유형별 검색

### 임상 시험 (Clinical Trial)
```
# 넓은 범위
Clinical Trial[Publication Type]

# RCT만
Randomized Controlled Trial[Publication Type]

# 인체적용시험
(Clinical Trial[Publication Type] OR "human study"[Title/Abstract])
```

### 메타분석/체계적 문헌고찰
```
(Meta-Analysis[Publication Type] OR Systematic Review[Publication Type])
```

### In-vivo 연구
```
("in vivo"[Title/Abstract] OR "animal study"[Title/Abstract] OR
 "mouse"[Title/Abstract] OR "rat"[Title/Abstract])
```

### In-vitro 연구
```
("in vitro"[Title/Abstract] OR "cell culture"[Title/Abstract] OR
 "cell line"[Title/Abstract] OR keratinocyte* OR fibroblast*)
```

### Ex-vivo 연구
```
("ex vivo"[Title/Abstract] OR "skin explant"[Title/Abstract] OR
 "organ culture"[Title/Abstract])
```

## 4. 품질 필터

### 최근 연구 (Recent)
```
# 최근 5년
2021:2026[Date - Publication]

# 최근 10년
2016:2026[Date - Publication]
```

### 영어 논문만
```
english[Language]
```

### 무료 전문 이용 가능
```
free full text[Filter]
```

### 초록 있는 논문만
```
hasabstract
```

## 5. 복합 검색 템플릿

### 성분 효능 연구 검색
```
{INGREDIENT}[Title/Abstract] AND
(skin[Title/Abstract] OR dermatology[MeSH Terms]) AND
{EFFICACY_TERMS} AND
(efficacy OR effect* OR study OR trial) AND
2015:2026[Date - Publication]
```

### 성분 안전성 연구 검색
```
{INGREDIENT}[Title/Abstract] AND
(safety OR toxicity OR "adverse effect*" OR irritation OR
 sensitization OR "patch test" OR tolerance) AND
(skin OR dermal OR topical)
```

### 성분 메커니즘 연구 검색
```
{INGREDIENT}[Title/Abstract] AND
(mechanism* OR pathway* OR "mode of action" OR
 signaling OR molecular OR cellular) AND
(skin OR keratinocyte* OR fibroblast* OR melanocyte*)
```

## 6. 결과 정렬 전략

### 관련성 순 (기본값)
```
sort=relevance
```

### 최신순
```
sort=pub_date
```

### 인용 횟수순 (별도 API 필요)
- Semantic Scholar API와 연동
- Google Scholar 인용 정보 참조

## 7. 검색 결과 평가

### 증거 수준 분류
| 수준 | 연구 유형 | 점수 |
|-----|----------|-----|
| 1a | 메타분석/체계적 문헌고찰 | 100 |
| 1b | RCT | 90 |
| 2a | 대조군 있는 임상시험 | 80 |
| 2b | 대조군 없는 임상시험 | 70 |
| 3 | In-vivo 동물시험 | 50 |
| 4 | In-vitro/Ex-vivo | 40 |
| 5 | 전문가 의견/리뷰 | 20 |

### 논문 품질 체크리스트
- [ ] 피어리뷰 학술지 게재
- [ ] 명확한 방법론 기술
- [ ] 적절한 샘플 크기 (n≥20)
- [ ] 통계적 유의성 제시
- [ ] 이해충돌 공개

## 8. 일반적인 검색 실수

### 피해야 할 것
1. **너무 넓은 검색**: `vitamin C` → 수만 건 결과
2. **너무 좁은 검색**: 필터 과다 → 결과 없음
3. **동의어 누락**: INCI명만 검색 → 관련 연구 누락
4. **날짜 필터 과도**: 최근 1년만 → 중요 연구 누락

### 권장 사항
1. **점진적 확장**: 좁은 검색 → 넓은 검색
2. **동의어 확인**: MeSH Browser 활용
3. **적절한 날짜 범위**: 최근 10년 권장
4. **복수 검색**: 여러 전략으로 교차 검증
