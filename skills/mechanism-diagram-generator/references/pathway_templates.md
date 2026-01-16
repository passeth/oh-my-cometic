# 경로 템플릿 전체 목록

화장품 성분 작용 메커니즘 다이어그램을 위한 사전 정의 템플릿

## 1. 템플릿 카탈로그

### 미백 관련 (Whitening)

| Template ID | 한국어명 | 영어명 | 적용 성분 |
|------------|---------|--------|----------|
| `tyrosinase_inhibition` | 티로시나제 억제 경로 | Tyrosinase Inhibition | Arbutin, Kojic Acid, Vitamin C |
| `melanin_transfer_block` | 멜라노좀 전달 차단 | Melanin Transfer Block | Niacinamide, Tranexamic Acid |

### 항노화 관련 (Anti-aging)

| Template ID | 한국어명 | 영어명 | 적용 성분 |
|------------|---------|--------|----------|
| `collagen_synthesis` | 콜라겐 합성 촉진 | Collagen Synthesis | Retinol, Vitamin C, Peptides |
| `mmp_inhibition` | MMP 억제 경로 | MMP Inhibition | Retinol, EGCG, 녹차 |
| `retinoid_signaling` | 레티노이드 신호전달 | Retinoid Signaling | Retinol, Retinaldehyde |
| `peptide_signaling` | 펩타이드 신호전달 | Peptide Signaling | Matrixyl, GHK-Cu |

### 항산화 관련 (Antioxidant)

| Template ID | 한국어명 | 영어명 | 적용 성분 |
|------------|---------|--------|----------|
| `antioxidant_network` | 항산화 네트워크 | Antioxidant Network | Vitamin C, E, Ferulic Acid |

### 보습/장벽 관련 (Moisturizing/Barrier)

| Template ID | 한국어명 | 영어명 | 적용 성분 |
|------------|---------|--------|----------|
| `barrier_lipid` | 피부 장벽 지질 합성 | Barrier Lipid Synthesis | Ceramide, Niacinamide |
| `hyaluronic_hydration` | 히알루론산 수분 경로 | Hyaluronic Hydration | Hyaluronic Acid |

### 진정 관련 (Soothing)

| Template ID | 한국어명 | 영어명 | 적용 성분 |
|------------|---------|--------|----------|
| `anti_inflammatory` | 항염 경로 | Anti-inflammatory | Centella, Panthenol |

### 각질 케어 (Exfoliation)

| Template ID | 한국어명 | 영어명 | 적용 성분 |
|------------|---------|--------|----------|
| `exfoliation` | 각질 제거 경로 | Exfoliation | AHA, BHA |

### 대사 관련 (Metabolism)

| Template ID | 한국어명 | 영어명 | 적용 성분 |
|------------|---------|--------|----------|
| `nad_metabolism` | NAD+ 대사 경로 | NAD+ Metabolism | Niacinamide |

---

## 2. 템플릿 상세

### tyrosinase_inhibition

```
노드 수: 7
엣지 수: 6
서브그래프: 4

주요 경로:
성분 → 티로시나제 억제 → 멜라닌 합성 감소 → 색소 개선

적용 가능 성분:
- Arbutin (α, β)
- Kojic Acid
- Vitamin C
- Tranexamic Acid (부분적)
- Licorice Extract
- Mulberry Extract
```

### melanin_transfer_block

```
노드 수: 6
엣지 수: 5
서브그래프: 5

주요 경로:
성분 → PAR-2 억제 → 멜라노좀 전달 감소 → 각질세포 색소 감소

적용 가능 성분:
- Niacinamide
- Soy Extract
- Undecylenoyl Phenylalanine
```

### collagen_synthesis

```
노드 수: 9
엣지 수: 8
서브그래프: 5

주요 경로:
성분 → TGF-β → SMAD → 콜라겐 유전자 발현 → 프로콜라겐 → 콜라겐 섬유

적용 가능 성분:
- Retinol / Retinoids
- Vitamin C
- Peptides (Matrixyl, GHK-Cu)
- Growth Factors
- Centella Asiatica
```

### mmp_inhibition

```
노드 수: 8
엣지 수: 7
서브그래프: 4

주요 경로:
성분 → MMP-1/MMP-3 억제 → 콜라겐/엘라스틴 분해 감소 → ECM 보존

적용 가능 성분:
- Retinol
- EGCG (녹차)
- Resveratrol
- Peptides
```

### antioxidant_network

```
노드 수: 10
엣지 수: 10
서브그래프: 5

주요 경로:
스트레스 → ROS 생성 → 항산화 성분 → 라디칼 중화 → 세포 보호

적용 가능 성분:
- Vitamin C
- Vitamin E
- Ferulic Acid
- CoQ10
- Resveratrol
- EGCG
```

### nad_metabolism

```
노드 수: 13
엣지 수: 12
서브그래프: 5

주요 경로:
Niacinamide → NAD+ → 다중 세포 경로 (에너지, DNA 복구, 지질 합성)

특이사항:
- Niacinamide 전용 템플릿
- 다중 효과 (장벽, 미백, 피지) 동시 표현
```

### retinoid_signaling

```
노드 수: 13
엣지 수: 12
서브그래프: 5

주요 경로:
Retinol → Retinaldehyde → Retinoic Acid → RAR/RXR → 유전자 조절

적용 가능 성분:
- Retinol
- Retinaldehyde
- Retinyl Palmitate
- Tretinoin (전문의약품)
```

### barrier_lipid

```
노드 수: 11
엣지 수: 11
서브그래프: 5

주요 경로:
성분 → PPAR 활성화 → 지질 합성 유전자 → 세라마이드/지방산/콜레스테롤

적용 가능 성분:
- Niacinamide
- Ceramides
- Phytosphingosine
- Cholesterol
```

### hyaluronic_hydration

```
노드 수: 12
엣지 수: 10
서브그래프: 4

주요 경로:
분자량별 분리 경로 (HMW → 표면, LMW → 진피)

특이사항:
- 분자량별 다른 효과 표현
- CD44 수용체 신호전달 포함
```

### peptide_signaling

```
노드 수: 11
엣지 수: 11
서브그래프: 5

주요 경로:
펩타이드 → 수용체 결합 → MAPK/TGF-β → ECM 단백질 합성

적용 가능 성분:
- Matrixyl (Palmitoyl Pentapeptide-4)
- Argireline (Acetyl Hexapeptide-8)
- GHK-Cu (Copper Tripeptide-1)
- EGF, FGF 등 성장인자
```

### anti_inflammatory

```
노드 수: 12
엣지 수: 12
서브그래프: 5

주요 경로:
자극 → 염증 반응 → 진정 성분 → NF-κB/COX 억제 → 사이토카인 감소

적용 가능 성분:
- Centella Asiatica
- Panthenol
- Allantoin
- Bisabolol
- Madecassoside
```

### exfoliation

```
노드 수: 8
엣지 수: 7
서브그래프: 4

주요 경로:
성분 → 데스모좀 약화 → 세포간 결합 감소 → 각질 탈락

적용 가능 성분:
- Glycolic Acid (AHA)
- Lactic Acid (AHA)
- Salicylic Acid (BHA)
- PHA
- LHA
```

---

## 3. 성분-템플릿 매핑

### 비타민류

| 성분 | Primary | Secondary | Tertiary |
|-----|---------|-----------|----------|
| Niacinamide | nad_metabolism | melanin_transfer_block | barrier_lipid |
| Retinol | retinoid_signaling | collagen_synthesis | mmp_inhibition |
| Vitamin C | antioxidant_network | collagen_synthesis | tyrosinase_inhibition |
| Vitamin E | antioxidant_network | - | - |
| Panthenol | anti_inflammatory | barrier_lipid | - |

### 펩타이드류

| 성분 | Primary | Secondary |
|-----|---------|-----------|
| Matrixyl | peptide_signaling | collagen_synthesis |
| Argireline | peptide_signaling | - |
| GHK-Cu | peptide_signaling | collagen_synthesis |

### 식물 추출물

| 성분 | Primary | Secondary |
|-----|---------|-----------|
| Centella | anti_inflammatory | collagen_synthesis |
| Green Tea | antioxidant_network | mmp_inhibition |
| Licorice | tyrosinase_inhibition | anti_inflammatory |

### 산류

| 성분 | Primary |
|-----|---------|
| Glycolic Acid | exfoliation |
| Lactic Acid | exfoliation |
| Salicylic Acid | exfoliation |

### 보습 성분

| 성분 | Primary |
|-----|---------|
| Hyaluronic Acid | hyaluronic_hydration |
| Ceramide | barrier_lipid |

### 미백 성분

| 성분 | Primary | Secondary |
|-----|---------|-----------|
| Arbutin | tyrosinase_inhibition | - |
| Kojic Acid | tyrosinase_inhibition | - |
| Tranexamic Acid | melanin_transfer_block | - |

---

## 4. 템플릿 사용 가이드

### 단일 성분 분석

```python
# 기본 사용
diagram = generator.generate("Niacinamide", mechanism_type="primary")

# 특정 템플릿 지정
diagram = generator.from_template("nad_metabolism", "Niacinamide")
```

### 다중 경로 분석

```python
# 모든 관련 경로 통합
diagram = generator.generate("Niacinamide", mechanism_type="all")
```

### 성분 비교

```python
# 동일 효능 성분 비교
diagram = generator.generate_comparison(
    ingredients=["Vitamin C", "Arbutin", "Niacinamide"],
    efficacy="whitening"
)
```

### 시너지 분석

```python
# 시너지 효과 시각화
diagram = generator.generate_synergy(
    ingredients=["Vitamin C", "Vitamin E", "Ferulic Acid"],
    synergy_type="antioxidant_network"
)
```

---

## 5. 커스터마이징

### 템플릿 수정

기존 템플릿을 기반으로 커스터마이징:

```python
# 템플릿 복사 후 수정
template = generator.templates["collagen_synthesis"].copy()
template["nodes"].append({
    "id": "NEW",
    "label": "추가 노드",
    "subgraph": "Clinical"
})
```

### 새 템플릿 추가

```python
CUSTOM_TEMPLATE = {
    "title": "커스텀 경로",
    "title_en": "Custom Pathway",
    "description": "설명",
    "subgraphs": [...],
    "nodes": [...],
    "edges": [...]
}

generator.templates["custom_pathway"] = CUSTOM_TEMPLATE
```

---

## 6. 참고사항

### 템플릿 선택 기준

1. **Primary**: 성분의 가장 대표적인 작용 기전
2. **Secondary**: 부가적이지만 중요한 기전
3. **Tertiary**: 알려져 있지만 덜 중요한 기전

### 다이어그램 복잡도 권장사항

- **간단 분석**: 1개 템플릿, 5-8 노드
- **표준 분석**: 1-2개 템플릿, 8-12 노드
- **심층 분석**: 2-3개 템플릿 통합, 12-20 노드

### 언어 설정

- `ko`: 한국어 라벨
- `en`: 영어 라벨
- `ko-en`: 한영 병기 (기술 보고서용)
