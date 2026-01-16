# EU 화장품 규정 (EC 1223/2009) 상세 가이드

## 개요

**Regulation (EC) No 1223/2009**는 EU 화장품 규제의 핵심 법령입니다.

- **발효일**: 2009년 12월 22일
- **적용일**: 2013년 7월 11일
- **범위**: EU 27개국 + EEA (노르웨이, 아이슬란드, 리히텐슈타인)
- **관리**: European Commission DG GROW

## Annex 체계

### Annex I: 화장품 안전성 보고서 (CPSR)

모든 화장품은 시장 출시 전 안전성 평가 필수:

```
Part A: 화장품 안전성 정보
├── 1. 정량적/정성적 성분 구성
├── 2. 물리/화학적 특성 및 안정성
├── 3. 미생물학적 품질
├── 4. 불순물, 미량물질, 포장재 정보
├── 5. 정상/합리적 예측 가능 사용
├── 6. 화장품 노출
├── 7. 성분 노출
├── 8. 성분의 독성학적 프로파일
├── 9. 바람직하지 않은 효과
└── 10. 화장품에 대한 정보

Part B: 화장품 안전성 평가
├── 평가 결론
├── 경고문 및 사용 지침
├── 평가 근거
└── 평가자 자격 및 서명
```

### Annex II: 금지 물질 목록

화장품 사용이 **전면 금지**된 물질:

| Ref No | 물질명 | CAS | 비고 |
|--------|--------|-----|------|
| 1 | 2-Acetylamino-5-nitro-4-propionamidoanisole | - | |
| 2 | 2-Chloracetamide | 79-07-2 | |
| ... | ... | ... | |
| 1373 | Hydroquinone | 123-31-9 | 2020년 추가 |

**총 물질 수**: 약 1,400개 이상 (지속 업데이트)

```python
# 금지 물질 확인 예시
def is_prohibited(inci_name: str) -> bool:
    """Annex II 금지 물질 여부 확인"""
    prohibited_list = load_annex_ii()
    return inci_name.upper() in prohibited_list
```

### Annex III: 제한 물질 목록

**조건부 사용 허가** 물질 (농도, 용도, 라벨 제한):

#### 구조
| 열 | 내용 |
|----|------|
| a | 참조 번호 |
| b | 성분명/CAS |
| c | 제품 유형 |
| d | 최대 농도 |
| e | 기타 제한 |
| f | 사용 조건 및 경고 |
| g | 표시 문구 |

#### 주요 제한 물질 예시

**살리실산 (SALICYLIC ACID)**
```
Ref: 98
CAS: 69-72-7
제한:
- Leave-on: max 2.0%
- Rinse-off: max 3.0%
- Rinse-off hair products: max 3.0%
조건: 3세 미만 어린이용 제품 사용 금지 (린스오프 헤어 제외)
표시: "3세 미만 어린이 사용금지" (leave-on)
```

**레티놀 (RETINOL)**
```
Ref: 223
CAS: 68-26-8
제한:
- Face/hand products: max 0.3%
- Body products: max 0.05%
조건:
- 3세 미만 사용 금지
- 임산부 사용 주의
표시: 사용 빈도 지침 포함
```

**알파하이드록시산 (AHA)**
```
Ref: 별도 규정
대상: Glycolic Acid, Lactic Acid 등
제한:
- Leave-on (face): max 10%
- Rinse-off: max 30%
- Professional use: max 70%
조건: pH 3.5 이상
표시: "자외선차단제 사용 권장"
```

### Annex IV: 허용 색소

화장품에 사용 가능한 **색소** 목록:

#### 색소 분류
| 분류 | 용도 | 예시 |
|------|------|------|
| Column 1 | 모든 화장품 | CI 77891 (Titanium Dioxide) |
| Column 2 | 점막/눈 제외 | CI 15985 (Yellow 6) |
| Column 3 | 점막 접촉 제품 제외 | CI 16035 (Red 40) |
| Column 4 | 피부 단시간 접촉만 | CI 12490 |

#### 색소 순도 기준
- 중금속 함량 제한 (납, 비소, 수은 등)
- 미생물 오염 기준
- 불순물 제한

### Annex V: 허용 방부제

화장품에 사용 가능한 **방부제** 목록:

#### 주요 방부제

**페녹시에탄올 (PHENOXYETHANOL)**
```
Ref: 29
CAS: 122-99-6
최대 농도: 1.0%
제한: 없음
```

**벤질알코올 (BENZYL ALCOHOL)**
```
Ref: 34
CAS: 100-51-6
최대 농도: 1.0%
제한: 없음
비고: 향료로도 사용 (별도 표기 필요)
```

**파라벤류 (PARABENS)**
```
Methylparaben: max 0.4% (단독), 0.8% (혼합)
Ethylparaben: max 0.4% (단독), 0.8% (혼합)
Propylparaben: max 0.14%
Butylparaben: max 0.14%
제한: 3세 미만 기저귀 부위 leave-on 제품 금지
```

### Annex VI: 허용 UV 필터

화장품에 사용 가능한 **자외선차단제** 목록:

#### 주요 UV 필터

**유기 UV 필터**
```
ETHYLHEXYL METHOXYCINNAMATE (Ref: 12)
- 최대 농도: 10%
- 비고: UVB 차단

BUTYL METHOXYDIBENZOYLMETHANE (Ref: 10)
- 최대 농도: 5%
- 비고: UVA 차단 (Avobenzone)

OCTOCRYLENE (Ref: 7)
- 최대 농도: 10%
```

**무기 UV 필터**
```
TITANIUM DIOXIDE (CI 77891)
- 최대 농도: 25%
- 비고: 나노 형태 별도 규정

ZINC OXIDE (CI 77947)
- 최대 농도: 25%
- 비고: 나노 형태 별도 규정
```

## 나노물질 규정

### 정의
- 크기: 1-100 nm 범위의 입자가 50% 이상

### 요구사항
1. **사전 통지**: 시장 출시 6개월 전 EU Commission 통지
2. **라벨 표기**: `(NANO)` 접미사 필수
3. **안전성 평가**: 나노 특성 고려한 CPSR

```
예시: TITANIUM DIOXIDE (NANO)
```

### 통지 정보
- 나노물질 식별 (INCI, CAS, IUPAC)
- 물리화학적 특성 (크기 분포, 표면적, 형태)
- 예상 노출량
- 독성학적 프로파일

## CMR 물질 규정

**CMR**: Carcinogenic (발암성), Mutagenic (변이원성), Reprotoxic (생식독성)

### 분류
- **Category 1A/1B**: 사용 금지 (확인된 CMR)
- **Category 2**: 사용 금지 (의심되는 CMR)
- **예외**: 과학적 안전성 입증 시 SCCS 평가 후 허용 가능

## 향료 알레르겐 규정

### 26개 알레르겐 표시 의무

농도 초과 시 성분표 별도 표기 필수:

| 물질 | Leave-on | Rinse-off |
|------|----------|-----------|
| LINALOOL | 0.001% | 0.01% |
| LIMONENE | 0.001% | 0.01% |
| CITRONELLOL | 0.001% | 0.01% |
| GERANIOL | 0.001% | 0.01% |
| COUMARIN | 0.001% | 0.01% |
| EUGENOL | 0.001% | 0.01% |
| ... | ... | ... |

### 알레르겐 목록
```
1. AMYL CINNAMAL
2. AMYLCINNAMYL ALCOHOL
3. ANISE ALCOHOL
4. BENZYL ALCOHOL
5. BENZYL BENZOATE
6. BENZYL CINNAMATE
7. BENZYL SALICYLATE
8. CINNAMAL
9. CINNAMYL ALCOHOL
10. CITRAL
11. CITRONELLOL
12. COUMARIN
13. EUGENOL
14. FARNESOL
15. GERANIOL
16. HEXYL CINNAMAL
17. HYDROXYCITRONELLAL
18. HYDROXYISOHEXYL 3-CYCLOHEXENE CARBOXALDEHYDE (HICC)
19. ISOEUGENOL
20. LILIAL (BUTYLPHENYL METHYLPROPIONAL) - 금지됨
21. LIMONENE
22. LINALOOL
23. METHYL 2-OCTYNOATE
24. ALPHA-ISOMETHYL IONONE
25. OAK MOSS EXTRACT
26. TREE MOSS EXTRACT
```

## CPNP (Cosmetic Products Notification Portal)

### 의무
모든 EU 판매 화장품은 CPNP 등록 필수

### 등록 정보
1. 제품 카테고리 및 명칭
2. 책임자 정보
3. 원산지 국가
4. 제품 프레임 포뮬레이션 또는 전성분
5. 라벨 (사진)
6. 나노물질 정보 (해당 시)
7. CMR 물질 정보 (해당 시)

### 독극물센터 통지
- 심각한 건강 위험 초래 가능 제품
- UFI (Unique Formula Identifier) 포함
- 2025년 완전 시행

## 클레임 규정

### 공통 기준 (Common Criteria)

EU Regulation 655/2013에 따른 6가지 원칙:

1. **법률 준수** (Legal Compliance)
2. **진실성** (Truthfulness)
3. **증거 기반** (Evidence)
4. **정직성** (Honesty)
5. **공정성** (Fairness)
6. **정보에 기반한 결정** (Informed Decision Making)

### 금지 클레임
- 질병 치료/예방 (의약품 영역)
- 허위/오인 유발
- 경쟁 제품 비방
- 무의미한 주장 ("100% 화학물질 무첨가")

## 규정 업데이트 추적

### 공식 소스
1. **EUR-Lex**: https://eur-lex.europa.eu
2. **EU Commission**: https://ec.europa.eu/growth/sectors/cosmetics_en
3. **SCCS**: https://health.ec.europa.eu/scientific-committees

### 업데이트 유형
- **Commission Regulation**: Annex 직접 수정
- **Commission Decision**: 특정 물질 결정
- **Corrigendum**: 오류 수정

### 최근 주요 업데이트 (2023-2025)

```
EU 2023/1545: Annex III 업데이트 (레티놀 제한)
EU 2022/2195: Annex VI 업데이트 (UV 필터)
EU 2022/1531: Annex III 업데이트 (Butylphenyl methylpropional 금지)
```

## 실무 체크리스트

### 신제품 개발 시

```markdown
□ 모든 성분 Annex II 확인 (금지)
□ 제한 물질 Annex III 확인 (농도/용도)
□ 색소 Annex IV 확인
□ 방부제 Annex V 확인
□ UV필터 Annex VI 확인
□ 나노물질 해당 여부 확인
□ CMR 물질 해당 여부 확인
□ 향료 알레르겐 확인
□ CPSR 작성
□ CPNP 등록
□ 라벨 검토
```

### 정기 규제 검토

```markdown
□ EUR-Lex 업데이트 확인 (월 1회)
□ SCCS 의견서 검토 (분기 1회)
□ 기존 제품 규정 준수 재확인 (년 1회)
□ CPNP 정보 업데이트 (변경 시)
```

## 참고 자료

- [EU 화장품 규정 원문](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32009R1223)
- [CosIng Database](https://ec.europa.eu/growth/tools-databases/cosing/)
- [CPNP Portal](https://ec.europa.eu/growth/tools-databases/cpnp/)
- [SCCS 의견서](https://health.ec.europa.eu/scientific-committees/scientific-committee-consumer-safety-sccs_en)
- [Cosmetics Europe](https://cosmeticseurope.eu/)
