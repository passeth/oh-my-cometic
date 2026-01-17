# In Vitro Tests Reference

화장품 효능 입증을 위한 In Vitro (세포/효소 수준) 시험 목록입니다.

## 1. 항산화 (Antioxidant)

### DPPH Radical Scavenging Assay

**원리**: DPPH (2,2-diphenyl-1-picrylhydrazyl) 라디칼의 환원 측정

```
DPPH (보라색) + 항산화제 → DPPH-H (노란색)
흡광도 감소 → 항산화 활성 지표
```

**프로토콜**:
- 시료와 DPPH 용액 혼합 (1:1 ~ 1:4)
- 30분 암소 반응
- 517nm 흡광도 측정

**결과 표현**:
- SC50 (50% 소거 농도): IC50과 동일 개념
- % Scavenging = (1 - As/Ac) × 100
- 양성대조: Vitamin C, BHT

**장점**: 간편, 저비용, 빠른 결과
**한계**: 지용성 시료 측정 제한

---

### ABTS Radical Scavenging Assay

**원리**: ABTS+ (2,2'-azino-bis-3-ethylbenzothiazoline-6-sulfonic acid) 양이온 라디칼 소거

```
ABTS + K2S2O8 → ABTS+ (청록색)
ABTS+ + 항산화제 → 탈색
```

**프로토콜**:
- ABTS+ 용액 제조 (16시간 암소)
- OD 0.7 조정 (734nm)
- 시료 혼합 후 6분 반응
- 734nm 흡광도 측정

**결과 표현**:
- TEAC (Trolox Equivalent Antioxidant Capacity)
- mg TE/g sample

**장점**: 수용성/지용성 모두 측정 가능
**한계**: 라디칼 생성에 시간 소요

---

### ORAC (Oxygen Radical Absorbance Capacity)

**원리**: Peroxyl 라디칼에 의한 형광 감소 억제

```
AAPH → Peroxyl radical
Fluorescein + Peroxyl → 형광 감소
항산화제 → 형광 유지 (보호 효과)
```

**프로토콜**:
- Fluorescein + 시료 혼합
- AAPH 첨가 후 형광 모니터링
- 37°C, 90분간 kinetic 측정
- AUC (Area Under Curve) 계산

**결과 표현**:
- μmol TE/g sample

**장점**: 생리적 조건 반영, 국제 표준
**한계**: 장비 의존, 시간 소요

---

### SOD-like Activity

**원리**: Superoxide dismutase 유사 활성 측정

```
Xanthine + Xanthine oxidase → O2•- + Uric acid
O2•- + NBT → Formazan (보라색)
SOD/시료 → O2•- 소거 → 색 발현 억제
```

**프로토콜**:
- Xanthine oxidase 반응계 구성
- 시료 첨가 후 반응
- 560nm 흡광도 측정

**결과 표현**:
- % Inhibition
- U/mg protein (효소 단위)

---

### Catalase-like Activity

**원리**: H2O2 분해 활성 측정

```
2H2O2 → 2H2O + O2
```

**측정 방법**:
- H2O2 잔량 측정 (240nm)
- 산소 발생량 측정

---

## 2. 미백 (Whitening/Brightening)

### Tyrosinase Inhibition Assay

**원리**: Melanin 합성 핵심 효소 tyrosinase 활성 억제

```
L-Tyrosine → L-DOPA → Dopaquinone → Melanin
         Tyrosinase
```

**프로토콜 (L-DOPA 기질)**:
- Mushroom tyrosinase (1000-2000 U/mL)
- L-DOPA (0.5-2 mM)
- 시료 첨가, 37°C 반응
- 475nm 흡광도 측정 (Dopachrome 생성)

**프로토콜 (L-Tyrosine 기질)**:
- L-Tyrosine (0.5-1 mM)
- 더 낮은 감도, 전체 경로 반영

**결과 표현**:
- IC50: 50% 억제 농도
- % Inhibition at [농도]
- 양성대조: Arbutin, Kojic acid, Vitamin C

**장점**: 표준화된 방법, 재현성 높음
**한계**: Mushroom tyrosinase vs Human tyrosinase 차이

---

### Melanin Content Assay (세포 기반)

**세포**: B16F10 (마우스 멜라노마), MNT-1, Melan-A

**프로토콜**:
```
1. 세포 배양 (48-72h)
2. 시료 처리 (24-72h)
3. α-MSH 자극 (선택적)
4. 세포 수확 및 용해 (1N NaOH, 80°C)
5. 400-475nm 흡광도 측정
6. 세포 수 보정
```

**결과 표현**:
- % Melanin content vs control
- Melanin (μg/mg protein)

**자극제**:
- α-MSH (0.1-1 μM)
- IBMX (100 μM)
- Forskolin (10 μM)

---

### MITF/TRP-1/TRP-2 Expression

**원리**: Melanogenesis 관련 유전자/단백질 발현 측정

**측정 방법**:
- qRT-PCR: mRNA 수준
- Western blot: 단백질 수준
- Immunofluorescence: 세포 내 위치

**타겟**:
- MITF (Master transcription factor)
- TRP-1 (Tyrosinase-related protein 1)
- TRP-2/DCT (Dopachrome tautomerase)
- MC1R (Melanocortin 1 receptor)

---

## 3. 주름개선 (Anti-Wrinkle)

### Collagen Synthesis Assay

**세포**: HDF (Human Dermal Fibroblast), CCD-986sk

**방법 1: Procollagen Type I C-peptide (PICP) ELISA**
```
1. HDF 배양 (24-48h)
2. 시료 처리 (24-72h)
3. 배양액 수집
4. PICP ELISA Kit 측정
5. 세포 수 보정
```

**방법 2: Sircol Collagen Assay**
- Total soluble collagen 정량
- Sirius red 염색 기반

**방법 3: Hydroxyproline Assay**
- Collagen 특이 아미노산 측정

**결과 표현**:
- ng/mL or μg/mg protein
- % vs control
- 양성대조: TGF-β, Vitamin C

---

### MMP Inhibition Assay

**MMP 종류**:
- MMP-1 (Collagenase): Type I, II, III collagen 분해
- MMP-2 (Gelatinase A): Basement membrane 분해
- MMP-3 (Stromelysin): Broad substrate
- MMP-9 (Gelatinase B): Type IV collagen 분해

**방법 1: 형광 기질법**
```
MMP + Fluorogenic substrate → 형광 증가
시료 억제 → 형광 증가 억제
Ex/Em: 320/405nm (기질별 상이)
```

**방법 2: Zymography**
- Gelatin zymography (MMP-2, -9)
- Casein zymography (MMP-3)

**방법 3: 세포 기반**
```
1. HDF 배양
2. UV-B 조사 (30-50 mJ/cm2) 또는 TNF-α 처리
3. 시료 처리
4. 배양액 내 MMP 측정 (ELISA, Western)
```

**결과 표현**:
- IC50
- % Inhibition
- 양성대조: EGCG, Retinol

---

### Elastase Inhibition Assay

**원리**: Neutrophil elastase (HNE) 활성 억제

```
Elastase + SAAVNA → p-Nitroaniline (황색)
시료 억제 → 색 발현 감소
```

**프로토콜**:
- Porcine pancreatic elastase (PPE)
- SAAVNA 기질 (N-succinyl-Ala-Ala-Ala-p-nitroanilide)
- 37°C 반응, 410nm 측정

**결과 표현**:
- IC50
- 양성대조: Ursolic acid, EGCG

---

### Hyaluronidase Inhibition Assay

**원리**: Hyaluronic acid 분해 효소 억제

**프로토콜**:
- Bovine testicular hyaluronidase
- Hyaluronic acid 기질
- Morgan-Elson 반응 또는 turbidimetric 방법
- N-acetylglucosamine 생성 측정

---

## 4. 보습 (Moisturizing)

### Hyaluronic Acid Synthesis

**세포**: HaCaT, Normal Human Keratinocyte (NHK)

**방법 1: ELISA**
```
1. 세포 배양 및 시료 처리
2. 배양액 수집
3. HA ELISA Kit 측정
```

**방법 2: HABP 결합법**
- Hyaluronic Acid Binding Protein
- 비오틴 표지 HABP 사용

**결과 표현**:
- ng/mL
- % vs control

---

### Aquaporin-3 Expression

**원리**: 피부 수분 채널 단백질 발현 증가

**세포**: HaCaT, NHK

**측정 방법**:
- qRT-PCR: AQP3 mRNA
- Western blot: AQP3 protein
- Immunofluorescence

---

### Filaggrin Expression

**원리**: 각질층 수분 유지 핵심 단백질

**세포**: 분화된 keratinocyte (Ca2+ 유도 분화)

**측정**:
- qRT-PCR, Western blot, ELISA

---

## 5. 항염 (Anti-Inflammatory)

### NO Production Inhibition

**세포**: RAW 264.7 (마우스 대식세포)

**프로토콜**:
```
1. RAW 264.7 배양 (24h)
2. 시료 처리 (1h)
3. LPS 자극 (1 μg/mL, 24h)
4. 배양액 수집
5. Griess 반응: NO2- 측정
   - Griess reagent A + B
   - 540nm 흡광도
6. NaNO2 표준곡선으로 정량
```

**결과 표현**:
- IC50
- % Inhibition at [농도]
- 양성대조: L-NAME, Dexamethasone

**세포 독성 확인**: MTT assay 병행 필수

---

### PGE2 Inhibition

**원리**: Prostaglandin E2 생성 억제 (COX-2 경로)

**세포**: RAW 264.7, THP-1

**프로토콜**:
```
1. LPS (1 μg/mL) + 시료 처리 (24h)
2. 배양액 수집
3. PGE2 ELISA Kit 측정
```

**결과 표현**:
- pg/mL
- % Inhibition
- 양성대조: Indomethacin, Celecoxib

---

### COX-2 Expression/Activity

**COX-2 발현 측정**:
- Western blot
- qRT-PCR
- Immunofluorescence

**COX-2 활성 측정**:
- COX Inhibitor Screening Assay Kit
- Arachidonic acid 기질 사용

---

### Cytokine Inhibition

**Pro-inflammatory cytokines**:
- TNF-α
- IL-1β
- IL-6
- IL-8

**세포**: RAW 264.7, THP-1, HaCaT (UV 자극)

**측정**: ELISA Kit 또는 Multiplex assay

**프로토콜**:
```
1. 세포 배양
2. 시료 처리 (1h)
3. 자극 (LPS, TNF-α, UV-B)
4. 24h 배양
5. 배양액 내 cytokine 측정
```

---

### iNOS Expression

**원리**: Inducible nitric oxide synthase 발현 억제

**측정**:
- Western blot: iNOS protein
- qRT-PCR: iNOS mRNA

---

### NF-κB Activation Inhibition

**원리**: 염증 신호전달 핵심 전사인자 억제

**측정 방법**:
- Western blot: p65, IκBα, p-IκBα
- Immunofluorescence: p65 nuclear translocation
- Luciferase reporter assay

---

## 6. 기타 효능

### 항균 (Antimicrobial)

**MIC (Minimum Inhibitory Concentration)**
```
균주: S. aureus, E. coli, P. acnes, C. albicans
방법: Broth microdilution
결과: MIC (μg/mL)
```

**Disc Diffusion Assay**
```
Inhibition zone 측정 (mm)
```

---

### 피지 조절 (Sebum Control)

**5α-Reductase Inhibition**
- Testosterone → DHT 전환 억제
- 양성대조: Finasteride

**Lipogenesis Inhibition**
- 세포: SZ95 sebocyte
- Oil Red O 염색

---

### 모발 성장 (Hair Growth)

**세포**: Human Dermal Papilla Cell (HDPC)

**측정**:
- Cell proliferation (MTT)
- VEGF, KGF, IGF-1 분비
- β-catenin, Wnt 신호 활성화

---

## 시험 기관 및 비용

### 국내 주요 In Vitro 시험 기관

- 대학 연구실 (의뢰 연구)
- 원료 전문 시험 기관
- CRO (Contract Research Organization)

### 예상 비용 (2024년 기준)

| 시험 항목 | 비용 범위 | 소요 기간 |
|----------|----------|----------|
| DPPH/ABTS | 20-40만원 | 1주 |
| Tyrosinase 억제 | 30-50만원 | 1주 |
| 세포 기반 단일 항목 | 50-100만원 | 2주 |
| 세포 기반 패키지 | 150-300만원 | 3-4주 |
| mRNA/단백질 발현 | 80-150만원/항목 | 2-3주 |

---

## 결과 해석 시 주의사항

1. **농도 현실성**: 제품 내 실제 함량과 시험 농도 비교
2. **세포 독성**: 효과 농도에서 세포 독성 여부 확인
3. **양성대조 비교**: 알려진 효능 성분 대비 활성 평가
4. **In vivo 외삽**: In vitro 결과가 피부 적용 시 재현되지 않을 수 있음
5. **복합 효과**: 단일 성분 vs 완제품 시험 결과 차이
