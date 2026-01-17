# EWG Skin Deep 평가 방법론

EWG(Environmental Working Group) Skin Deep 데이터베이스의 성분 안전성 평가 방법론 상세 가이드

## 1. EWG 등급 산정 기준

### 1.1 등급 체계 (1-10 Scale)

EWG Skin Deep은 1-10 스케일의 Hazard Score를 사용합니다:

| 등급 범위 | 색상 | 분류 | 의미 |
|-----------|------|------|------|
| 1-2 | 녹색 (Green) | Low Hazard | 낮은 유해성 - 현재 과학적 증거상 안전 |
| 3-6 | 노란색 (Yellow) | Moderate Hazard | 중간 유해성 - 일부 우려 존재, 주의 필요 |
| 7-10 | 빨간색 (Red) | High Hazard | 높은 유해성 - 심각한 건강 우려, 회피 권장 |

### 1.2 등급 산정 알고리즘

EWG 등급은 다음 요소들을 종합하여 산정됩니다:

```
최종 등급 = f(건강 우려 점수, 데이터 가용성, 규제 상태, 사용 제한)
```

**가중치 적용 요소**:

1. **건강 우려 카테고리별 점수**
   - Cancer (발암성): 가중치 높음
   - Developmental/Reproductive Toxicity: 가중치 높음
   - Allergies/Immunotoxicity: 가중치 중간
   - Endocrine Disruption: 가중치 중간
   - 기타 독성: 가중치 낮음-중간

2. **증거 강도 (Evidence Strength)**
   - 인체 연구 > 동물 연구 > 세포 연구 > 구조 유사성
   - 다수 연구 일관된 결과 > 단일 연구

3. **규제 기관 조치**
   - 금지/제한 성분은 자동으로 높은 등급
   - 규제 기관 우려 표명 시 등급 상향

### 1.3 데이터 가용성 등급

데이터의 양과 질에 따른 분류:

| 등급 | 설명 | 연구 수 | 신뢰도 |
|------|------|---------|--------|
| **None** | 데이터 없음 | 0 | 평가 불가 |
| **Limited** | 제한적 데이터 | 1-2 | 낮음 |
| **Fair** | 보통 데이터 | 3-5 | 중간 |
| **Good** | 충분한 데이터 | 6-10 | 높음 |
| **Robust** | 풍부한 데이터 | 10+ | 매우 높음 |

**중요**: 데이터 가용성이 낮으면 등급의 불확실성이 높습니다.

### 1.4 건강 우려 카테고리 상세

#### Cancer (발암성)
```
평가 기준:
- IARC (국제암연구소) 분류
- NTP (미국 국립독성프로그램) 분류
- EPA (미국 환경보호청) 분류
- 동물 실험 발암성 증거
- 역학 연구 결과

분류 등급:
- Group 1: 인체 발암물질 확인 → 등급 10
- Group 2A: 인체 발암 가능성 높음 → 등급 8-9
- Group 2B: 인체 발암 가능성 있음 → 등급 6-7
- Group 3: 분류 불가 → 등급 영향 없음
```

#### Developmental & Reproductive Toxicity (발달/생식 독성)
```
평가 기준:
- California Prop 65 리스트
- EU CMR 분류 (Category 1A, 1B, 2)
- 동물 실험 생식독성 증거
- 인체 역학 연구

우려 사항:
- 태아 발달 이상
- 생식 기능 장애
- 호르몬 교란
- 발달 신경독성
```

#### Allergies & Immunotoxicity (알레르기/면역독성)
```
평가 기준:
- EU Sensitizer 분류
- 임상 시험 패치 테스트 결과
- 시판 후 부작용 보고
- RIFM (향료 연구소) 데이터

우려 사항:
- 접촉성 피부염
- 호흡기 과민 반응
- 면역 체계 교란
- 광과민 반응
```

#### Use Restrictions (사용 제한)
```
평가 기준:
- EU 화장품 규정 Annex II-VI
- FDA OTC 규정
- Health Canada 제한
- ASEAN 화장품 지침

분류:
- 금지 (Banned): 등급 상향
- 제한 (Restricted): 등급 고려
- 조건부 허용: 영향 적음
```

#### Endocrine Disruption (내분비 교란)
```
평가 기준:
- EU 내분비 교란물질 후보 목록
- EPA ToxCast 스크리닝
- 동물 실험 호르몬 영향
- 체외 세포 연구

우려 물질 예:
- Parabens (일부)
- Oxybenzone
- Triclosan
- Phthalates
```

## 2. 데이터 소스

EWG는 다음 데이터 소스를 활용합니다:

### 2.1 정부 기관 데이터베이스

| 기관 | 데이터베이스 | 내용 |
|------|-------------|------|
| **US EPA** | TRI, ToxCast | 독성 데이터, 스크리닝 결과 |
| **US FDA** | CFSAN | 화장품 부작용 보고 |
| **NTP** | CERHR, RoC | 발암성, 생식독성 평가 |
| **IARC** | Monographs | 발암성 분류 |
| **California** | Prop 65 | 발암/생식독성 물질 목록 |
| **EU** | CosIng, REACH | 화장품 성분, 화학물질 등록 |
| **Health Canada** | NHPID | 천연 건강제품 성분 |

### 2.2 학술 연구 데이터베이스

- **PubMed**: 의학/독성학 연구
- **TOXNET**: 독성학 데이터 네트워크
- **ChemIDplus**: 화학물질 식별 정보
- **HSDB**: 유해물질 데이터뱅크

### 2.3 산업 자료

- **CIR (Cosmetic Ingredient Review)**: 화장품 성분 안전성 평가
- **RIFM**: 향료 성분 연구
- **PCPC**: 미국 화장품협회 자료
- **ECHA**: 유럽화학물질청 등록 정보

## 3. 등급의 한계점 및 비판

### 3.1 방법론적 한계

1. **Hazard vs Risk 혼동**
   ```
   문제점:
   - EWG는 "유해성(Hazard)"을 평가, "위험성(Risk)"과 다름
   - 농도와 노출 조건 미고려
   - 실제 사용 조건에서의 안전성과 괴리 가능

   예시:
   - Retinol: EWG 등급 9 (High Hazard)
   - EU 규제: 0.3% (얼굴), 0.05% (바디)로 안전하게 사용 가능
   - 실제 위험성: 적정 농도에서 낮음
   ```

2. **보수적 평가 경향**
   ```
   특징:
   - "의심스러우면 피하라" 원칙 적용
   - 안전 마진을 크게 설정
   - 규제 기관보다 엄격한 기준

   결과:
   - 일부 성분 과대평가 가능
   - 규제 기관 평가와 불일치
   ```

3. **농도 미고려**
   ```
   한계:
   - 0.001%도 10%도 동일 등급 부여
   - 용량-반응 관계 무시
   - 실제 노출량 미반영

   예시:
   - Phenoxyethanol: 1%에서 안전하게 사용
   - EWG: 농도 무관하게 등급 4 부여
   ```

4. **데이터 품질 변동**
   ```
   문제점:
   - 데이터 가용성이 등급 신뢰도 결정
   - 신규 성분: 데이터 부족으로 평가 불확실
   - 오래된 성분: 최신 연구 미반영 가능
   ```

### 3.2 과학계 비판

```
주요 비판:
1. "두려움 기반 마케팅에 활용됨"
   - 소비자 불안 조장
   - 과학적 맥락 부재

2. "규제 기관 평가와 불일치"
   - FDA, EU SCCS의 안전 평가와 상충
   - 이중 기준 혼란

3. "천연 성분 편향"
   - 천연 ≠ 안전 (예: 에센셜 오일 피부 자극)
   - 합성 성분 과대평가 경향

4. "투명성 부족"
   - 정확한 알고리즘 비공개
   - 등급 산정 과정 불명확
```

### 3.3 업계 비판

```
화장품 업계 입장:
1. "비과학적 평가 방법"
   - 전문 독성학자 검토 부족
   - 피어 리뷰 없음

2. "소비자 오도"
   - 안전한 성분도 높은 등급
   - 불필요한 제품 회피 유도

3. "경제적 영향"
   - 클린뷰티 트렌드 과열
   - 효능 좋은 성분 배제 압박
```

## 4. EWG vs 규제 기관 평가 비교

### 4.1 주요 성분 비교 표

| 성분 | EWG 등급 | EU SCCS | US FDA | 실제 안전성 |
|------|----------|---------|--------|-------------|
| **Retinol** | 9 (RED) | 0.3% 제한 | 허용 | 적정 농도에서 안전 |
| **Oxybenzone** | 8 (RED) | 6% 허용 | 6% 허용 | 논란 중 |
| **Phenoxyethanol** | 4 (YELLOW) | 1% 허용 | 허용 | 안전 |
| **Parabens** | 4-7 | 일부 제한 | 허용 | 논란 중 |
| **Hydroquinone** | 9 (RED) | 금지 | OTC 2% | EU 더 엄격 |
| **Niacinamide** | 1 (GREEN) | 허용 | 허용 | 안전 |
| **Glycerin** | 1 (GREEN) | 허용 | GRAS | 안전 |
| **Fragrance** | 8 (RED) | 규제 | 허용 | 개별 성분 따라 다름 |
| **Triclosan** | 7 (RED) | 화장품 금지 | 손세정제 금지 | 높은 우려 |

### 4.2 평가 차이 원인

```
1. 평가 목적 차이
   - EWG: 소비자 정보 제공, 보수적 접근
   - 규제 기관: 안전한 사용 조건 설정

2. 데이터 해석 차이
   - EWG: 잠재적 위험 강조
   - 규제 기관: 실제 노출 조건 고려

3. 전문성 차이
   - EWG: 환경/소비자 단체
   - 규제 기관: 독성학/약학 전문가 패널

4. 업데이트 주기 차이
   - EWG: 상대적으로 느린 업데이트
   - 규제 기관: 새 증거에 따라 수시 개정
```

## 5. 클린뷰티 트렌드와의 관계

### 5.1 클린뷰티 정의와 EWG

```
클린뷰티 일반 기준:
- "유해 성분" 배제
- 환경 친화적
- 투명한 성분 공개
- 동물 실험 배제

EWG의 영향:
- 클린뷰티 기준 형성에 큰 영향
- "EWG 등급" 클린뷰티 마케팅에 활용
- 소비자 인식 형성
```

### 5.2 EWG Verified 프로그램

```
EWG Verified 인증 기준:
1. 모든 성분 EWG 기준 충족
2. 금지 성분 목록 준수
3. 투명한 성분 라벨링
4. 제조 기준 충족

인증 과정:
1. 제품 성분 목록 제출
2. EWG 검토 및 평가
3. 현장 실사 (필요시)
4. 인증 마크 사용 라이선스

비용:
- 연간 라이선스 비용 발생
- 제품 수에 따라 차등
```

### 5.3 클린뷰티 마케팅 시 주의사항

```
권장 사항:
1. EWG 등급을 유일한 기준으로 사용하지 않음
2. 규제 기관 평가와 함께 고려
3. 과학적 근거 기반 커뮤니케이션
4. 소비자 불안 조장 회피

법적 주의:
1. "EWG 인증"은 공식 표현 아님
2. EWG 로고 사용 시 라이선스 필요
3. 국가별 광고 규제 준수
4. 경쟁사 비방 금지
```

## 6. 올바른 EWG 등급 활용법

### 6.1 제품 개발 시 활용

```python
def evaluate_ingredient_safety(inci_name):
    """
    종합적인 성분 안전성 평가

    1. EWG 등급 확인 (참고용)
    2. 규제 기관 평가 확인 (EU SCCS, FDA, CIR)
    3. 원료사 안전성 자료 검토
    4. 배합 농도에서의 안전성 평가
    5. 최종 안전성 판단
    """

    evaluation = {
        "ewg_score": get_ewg_rating(inci_name),
        "eu_status": get_eu_regulation_status(inci_name),
        "fda_status": get_fda_status(inci_name),
        "cir_conclusion": get_cir_assessment(inci_name),
        "supplier_data": get_supplier_safety_data(inci_name)
    }

    return comprehensive_safety_assessment(evaluation)
```

### 6.2 소비자 커뮤니케이션

```
효과적인 커뮤니케이션:
1. EWG 등급 단독 강조 피함
2. 규제 기관 승인 사실 함께 언급
3. 배합 농도의 안전성 설명
4. 과학적 증거 기반 설명
5. 소비자 질문에 대한 명확한 답변 준비
```

### 6.3 의사결정 프레임워크

```
성분 선정 시 고려 순서:
1. 규제 적합성 (EU, FDA 등)
2. 안전성 데이터 (원료사, CIR)
3. 배합 농도에서의 안전성
4. EWG 등급 (참고용)
5. 소비자 인식/트렌드
6. 최종 결정
```

## 7. 결론

EWG Skin Deep은 소비자 정보 제공에 유용한 도구이지만, 과학적 한계가 있습니다:

**장점**:
- 접근하기 쉬운 안전성 정보
- 소비자 인식 제고
- 투명성 촉진

**한계**:
- Hazard-Risk 구분 부족
- 농도 미고려
- 보수적 편향

**권장 활용법**:
- 참고 자료로 활용
- 규제 기관 평가와 함께 검토
- 과학적 맥락에서 해석
- 클린뷰티 트렌드 대응 도구로 활용

---

**참고 문헌**:
1. EWG Skin Deep Methodology: https://www.ewg.org/skindeep/contents/about-page/
2. CIR Safety Assessments: https://www.cir-safety.org/
3. EU SCCS Opinions: https://health.ec.europa.eu/scientific-committees/scientific-committee-consumer-safety-sccs_en
4. FDA Cosmetic Safety: https://www.fda.gov/cosmetics/cosmetic-ingredients
