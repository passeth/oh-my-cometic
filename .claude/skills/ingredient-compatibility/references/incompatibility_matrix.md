# Ingredient Incompatibility Matrix

## Overview

이 문서는 화장품 처방에서 자주 사용되는 활성 성분들 간의 호환성/비호환성 매트릭스를 제공합니다. 각 조합에 대한 심각도 등급, 비호환 메커니즘, 해결 방안을 포함합니다.

## Severity Levels

| 등급 | 의미 | 권장 조치 |
|------|------|-----------|
| **CRITICAL** | 즉각적인 물리적/화학적 반응, 제품 사용 불가 | 절대 함께 배합하지 않음 |
| **HIGH** | 유의미한 효능 저하 또는 안정성 문제 | 처방 분리 또는 안정화 전략 필수 |
| **MEDIUM** | 장기 안정성 우려 또는 부분적 효능 저하 | 안정성 테스트 강화, 조건부 사용 |
| **LOW** | 경미한 영향 또는 이론적 우려 | 모니터링, 일반적 사용 가능 |
| **OK** | 호환 가능, 문제 없음 | 안전하게 함께 사용 |
| **SYNERGY** | 상호 강화 효과 | 함께 사용 권장 |

---

## 1. Vitamin C (L-Ascorbic Acid) Compatibility Matrix

### 1.1 L-Ascorbic Acid (순수 비타민 C)

| 성분 | 호환성 | 심각도 | 메커니즘 | 해결 방안 |
|------|--------|--------|----------|-----------|
| **Niacinamide** | 조건부 | LOW | 낮은 pH에서 Nicotinic Acid 전환 가능 | pH 5-6에서 안정적 공존, 실제 문제 드묾 |
| **Vitamin E (Tocopherol)** | SYNERGY | - | E가 C 라디칼 재생 | 함께 사용 강력 권장 |
| **Ferulic Acid** | SYNERGY | - | 시너지 안정화 효과 | C E Ferulic 조합 권장 |
| **Retinol** | 비호환 | MEDIUM | pH 차이 (C: 2.5-3.5, Retinol: 5.5-6.5) | AM/PM 분리 사용 |
| **AHA (Glycolic/Lactic)** | 비호환 | MEDIUM | pH 범위 중첩되나 자극 증폭 가능 | 별도 제품 권장 |
| **BHA (Salicylic Acid)** | 비호환 | MEDIUM | 유사 pH지만 자극 증폭 | 별도 제품 권장 |
| **Copper Peptides** | 비호환 | HIGH | Cu2+가 산화 촉매 역할 | 시간차 사용 (최소 10분) |
| **Benzoyl Peroxide** | 비호환 | CRITICAL | 강력한 산화로 Vit C 분해 | 절대 함께 사용 불가 |
| **Zinc Oxide** | 조건부 | MEDIUM | 금속 이온 촉매 산화 | 킬레이트제 충분히 사용 |
| **Hyaluronic Acid** | OK | - | 상호작용 없음 | 함께 사용 가능 |
| **Peptides (대부분)** | 조건부 | LOW | pH 차이로 펩타이드 안정성 저하 가능 | pH 절충 또는 분리 |

### 1.2 Vitamin C Derivatives

| 유도체 | Niacinamide | Retinol | AHA | BHA | Peptides |
|--------|-------------|---------|-----|-----|----------|
| Ascorbyl Glucoside | OK | OK | OK | OK | OK |
| Sodium Ascorbyl Phosphate | OK | OK | OK | OK | OK |
| Ascorbyl Tetraisopalmitate | OK | OK | MEDIUM | MEDIUM | OK |
| Ethyl Ascorbic Acid | OK | OK | OK | OK | OK |
| 3-O-Ethyl Ascorbic Acid | OK | OK | OK | OK | OK |

> **Note**: Vitamin C 유도체들은 순수 L-Ascorbic Acid보다 안정적이며, 대부분의 다른 성분들과 호환됩니다.

---

## 2. Retinoids Compatibility Matrix

| 성분 | Retinol | Retinaldehyde | Tretinoin | Retinyl Palmitate |
|------|---------|---------------|-----------|-------------------|
| **Benzoyl Peroxide** | CRITICAL | CRITICAL | CRITICAL | HIGH |
| **AHA (Glycolic)** | HIGH | HIGH | HIGH | MEDIUM |
| **BHA (Salicylic)** | HIGH | HIGH | HIGH | MEDIUM |
| **L-Ascorbic Acid** | MEDIUM | MEDIUM | MEDIUM | LOW |
| **Vit C Derivatives** | LOW | LOW | LOW | OK |
| **Niacinamide** | OK | OK | OK | OK |
| **Hyaluronic Acid** | OK | OK | OK | OK |
| **Azelaic Acid** | LOW | LOW | MEDIUM | OK |
| **Peptides** | OK | OK | OK | OK |
| **Vitamin E** | SYNERGY | SYNERGY | SYNERGY | SYNERGY |
| **Bakuchiol** | OK | OK | OK | OK |
| **Ceramides** | SYNERGY | SYNERGY | SYNERGY | SYNERGY |

### Retinoid + Exfoliating Acids 상세

```
조합: Retinol + AHA/BHA

위험:
- 피부 장벽 손상 증폭
- 자극, 건조, 벗겨짐 악화
- 감작(sensitization) 위험 증가

현실적 대응:
1. 초보자: 절대 동시 사용 불가
2. 내성 있는 사용자: 교대 사용 (격일)
3. 전문가: 낮은 농도로 점진적 병용 가능

권장:
- PM: Retinol
- AM: AHA/BHA (선크림 필수)
또는
- 격일 교대 사용
```

---

## 3. AHA/BHA Compatibility Matrix

| 성분 | Glycolic Acid | Lactic Acid | Salicylic Acid | Mandelic Acid |
|------|---------------|-------------|----------------|---------------|
| **다른 AHA** | 조건부 | 조건부 | MEDIUM | 조건부 |
| **BHA** | HIGH | MEDIUM | - | LOW |
| **Retinol** | HIGH | HIGH | HIGH | MEDIUM |
| **L-Ascorbic Acid** | MEDIUM | LOW | MEDIUM | LOW |
| **Niacinamide** | OK | OK | LOW* | OK |
| **Hyaluronic Acid** | OK | OK | OK | OK |
| **Benzoyl Peroxide** | MEDIUM | MEDIUM | MEDIUM | LOW |
| **Copper Peptides** | LOW | LOW | LOW | LOW |
| **Vitamin E** | OK | OK | OK | OK |

> *Salicylic Acid + Niacinamide: pH 범위 차이 (SA: 3-4, Niacinamide: 5-7)로 동일 제품 내 최적화 어려움

### AHA/BHA 조합 시 주의사항

```python
EXFOLIANT_COMBINATION_RULES = {
    "same_product": {
        "max_total_concentration": "10% AHA + 2% BHA 이하",
        "ph_target": "3.5-4.0",
        "buffer_capacity": "충분한 버퍼링으로 pH 안정화"
    },
    "layering": {
        "order": "낮은 pH 먼저 (BHA -> AHA or vice versa)",
        "wait_time": "최소 5분",
        "risk": "자극 증폭, 초보자 비권장"
    },
    "rotation": {
        "recommended": "격일 사용 또는 AM/PM 분리",
        "benefit": "자극 최소화하며 다양한 효과"
    }
}
```

---

## 4. Surfactant Compatibility Matrix

### 4.1 계면활성제 전하별 호환성

| | 음이온 | 양이온 | 양쪽성 | 비이온 |
|---|--------|--------|--------|--------|
| **음이온** | OK | CRITICAL | OK | OK |
| **양이온** | CRITICAL | OK | OK | OK |
| **양쪽성** | OK | OK | OK | OK |
| **비이온** | OK | OK | OK | OK |

### 4.2 주요 계면활성제 비호환 쌍

| 음이온 계면활성제 | 양이온 계면활성제 | 결과 |
|------------------|------------------|------|
| Sodium Lauryl Sulfate | Cetrimonium Chloride | 침전, 클럼핑 |
| Sodium Laureth Sulfate | Behentrimonium Chloride | 침전, 탁화 |
| Sodium Cocoyl Isethionate | Polyquaternium-7 | 불용성 복합체 |
| Sodium C14-16 Olefin Sulfonate | Stearalkonium Chloride | 상분리 |

### 4.3 해결 방안

```
옵션 1: 계열 통일
- 클렌저: 음이온 + 양쪽성 + 비이온
- 컨디셔너: 양이온 + 비이온

옵션 2: 비이온/양쪽성 중심 설계
- Cocamidopropyl Betaine (양쪽성)
- Decyl Glucoside (비이온)
- Coco-Glucoside (비이온)

옵션 3: 순차적 적용
- 클렌징 단계: 음이온 계면활성제
- 컨디셔닝 단계: 양이온 계면활성제 (린스 후)
```

---

## 5. Polymer/Thickener Compatibility Matrix

| 증점제/폴리머 | 양이온 성분 | 음이온 성분 | 전해질 | pH 민감성 |
|--------------|------------|------------|--------|-----------|
| **Carbomer** | CRITICAL | OK | HIGH | HIGH (pH 5-7) |
| **Xanthan Gum** | MEDIUM | OK | MEDIUM | LOW |
| **Hydroxyethylcellulose** | OK | OK | LOW | LOW |
| **Acrylates Copolymer** | HIGH | OK | MEDIUM | HIGH |
| **Cellulose Gum** | LOW | OK | MEDIUM | LOW |
| **Sclerotium Gum** | OK | OK | OK | LOW |
| **Hydroxypropyl Starch Phosphate** | OK | OK | OK | LOW |

### Carbomer + 양이온 비호환성 상세

```
문제:
- Carbomer의 음이온 카르복실기가 양이온과 결합
- 전하 중화로 점도 급격히 저하
- 겔 구조 붕괴

영향받는 양이온 성분:
- Cetrimonium Chloride
- Behentrimonium Chloride
- Polyquaternium 계열
- 양이온 단백질/폴리머
- 일부 양이온성 활성 성분

대체 증점제:
1. Hydroxyethylcellulose: 비이온, 양이온 안정
2. Sclerotium Gum: 자연 유래, 전하 중립
3. Hydroxypropyl Methylcellulose: 비이온
4. Xanthan + Carbomer 혼합: 부분적 완화
```

---

## 6. Preservative Compatibility Matrix

| 방부제 | pH 범위 | 비호환 성분 | 주의사항 |
|--------|---------|------------|----------|
| **Phenoxyethanol** | 3-10 | 비이온 계면활성제 (효과 감소) | PEG류와 상호작용 |
| **Methylparaben** | 4-8 | 양이온 계면활성제 | 높은 pH에서 가수분해 |
| **Sodium Benzoate** | < 5 | - | pH 4 이하에서만 효과 |
| **Potassium Sorbate** | < 6 | 산화제 | pH 5 이하 권장 |
| **Benzisothiazolinone** | 3-9 | 환원제 | 알러지 주의 |
| **Caprylyl Glycol** | 3-10 | - | 보조 방부제 역할 |

---

## 7. Metal-Based Active Compatibility Matrix

| 성분 | EDTA | Phytic Acid | Vitamin C | 고pH |
|------|------|-------------|-----------|------|
| **Zinc Oxide** | HIGH | HIGH | MEDIUM | CRITICAL |
| **Zinc PCA** | MEDIUM | MEDIUM | LOW | HIGH |
| **Copper Peptides** | CRITICAL | HIGH | HIGH | MEDIUM |
| **Titanium Dioxide** | LOW | LOW | LOW | OK |
| **Iron Oxides** | LOW | LOW | HIGH | OK |

### Copper Peptides 상세

```
비호환 성분:
- L-Ascorbic Acid (촉매 산화)
- EDTA (킬레이트화)
- Phytic Acid (킬레이트화)
- AHA/BHA (pH 충돌, Cu 이온 방출)

안전한 조합:
- Niacinamide
- Hyaluronic Acid
- Peptides (구리 비함유)
- Ceramides
- 식물 추출물 (대부분)

권장 사용법:
- 별도 제품으로 분리
- 다른 활성 성분과 시간차 적용 (10-15분)
- 밤 루틴에서 단독 사용
```

---

## 8. Complete Cross-Reference Matrix

### 8.1 활성 성분 간 호환성 요약표

```
범례: O = OK, X = 비호환, △ = 조건부, S = 시너지

           L-AA  NAM  RET  GLA  SAL  AZE  PEP  CuP  HA   VE   BPO
L-AA        -    △    △    △    △    O    △    X    O    S    X
NAM         △    -    O    O    △    O    O    O    O    O    O
RET         △    O    -    X    X    △    O    O    O    S    X
GLA         △    O    X    -    △    O    △    △    O    O    △
SAL         △    △    X    △    -    O    △    △    O    O    △
AZE         O    O    △    O    O    -    O    O    O    O    O
PEP         △    O    O    △    △    O    -    O    O    O    O
CuP         X    O    O    △    △    O    O    -    O    O    O
HA          O    O    O    O    O    O    O    O    -    O    O
VE          S    O    S    O    O    O    O    O    O    -    O
BPO         X    O    X    △    △    O    O    O    O    O    -

L-AA: L-Ascorbic Acid
NAM: Niacinamide
RET: Retinol
GLA: Glycolic Acid
SAL: Salicylic Acid
AZE: Azelaic Acid
PEP: Peptides
CuP: Copper Peptides
HA: Hyaluronic Acid
VE: Vitamin E
BPO: Benzoyl Peroxide
```

### 8.2 제형 타입별 주의 조합

| 제형 | 특히 주의할 조합 | 이유 |
|------|-----------------|------|
| **에센스/세럼** | 고농도 활성 성분 조합 | pH 충돌, 안정성 |
| **에멀전/크림** | 양이온/음이온 성분 | 유화 시스템 파괴 |
| **토너/미스트** | 저점도 + 다성분 | 용해도 한계 |
| **선크림** | 금속 산화물 + 킬레이트 | 자외선 차단 효과 저하 |
| **마스크팩** | 고농도 산 + 레티놀 | 자극 증폭 |

---

## 9. Quick Decision Guide

### 9.1 즉시 분리가 필요한 조합

```
1. Benzoyl Peroxide + ANY Retinoid
   -> 별도 제품 (AM: BPO, PM: Retinoid)

2. 양이온 계면활성제 + 음이온 계면활성제
   -> 계열 통일

3. Copper Peptides + L-Ascorbic Acid
   -> 시간차 적용 (최소 10분)

4. Carbomer + 고농도 양이온 성분
   -> 증점제 변경 (HEC 등)
```

### 9.2 조건부 사용 가능 조합

```
1. Vitamin C + Niacinamide
   조건: pH 5-6 유지
   방법: 같은 제품 또는 순차 적용

2. Retinol + AHA/BHA
   조건: 내성 있는 피부, 낮은 농도
   방법: 격일 사용 또는 AM/PM 분리

3. Multiple Exfoliating Acids
   조건: 총 농도 제한, 충분한 버퍼링
   방법: 총 10% AHA + 2% BHA 이하
```

### 9.3 함께 사용 권장 조합 (Synergies)

```
1. Vitamin C + Vitamin E + Ferulic Acid
   효과: 상호 안정화, 광보호 증강

2. Retinol + Ceramides
   효과: 장벽 회복 지원, 자극 완화

3. Niacinamide + Hyaluronic Acid
   효과: 보습 + 장벽 강화

4. Peptides + Growth Factors
   효과: 시너지 안티에이징

5. Azelaic Acid + Niacinamide
   효과: 피지/염증 컨트롤 증강
```

---

## References

- Draelos, Z.D. (2019). Cosmetic Dermatology: Products and Procedures. Wiley-Blackwell.
- Baki, G., & Alexander, K.S. (2015). Introduction to Cosmetic Formulation and Technology. Wiley.
- Fiume, M.Z., et al. (2010). Safety Assessment of Retinol. CIR Expert Panel.
- Telang, P.S. (2013). Vitamin C in dermatology. Indian Dermatology Online Journal.
