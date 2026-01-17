---
description: 화장품 성분 안전성 빠른 평가 (EWG/CIR/MoS)
---

[SAFETY CHECK MODE ACTIVATED]

평가 대상: $ARGUMENTS

## 안전성 빠른 평가 워크플로우

### 입력 정보 확인
필수 정보:
- 성분명 (INCI Name)
- 사용 농도 (%)
- 제품 유형 (Leave-on/Rinse-off)

### 평가 항목

#### 1. EWG Skin Deep
| Score | 평가 |
|-------|-----|
| 1-2 | 🟢 Low Hazard - 안전 |
| 3-6 | 🟡 Moderate - 주의 |
| 7-10 | 🔴 High Hazard - 고위험 |

#### 2. CIR Status
- Safe as used
- Safe with qualifications
- Insufficient data
- Unsafe

#### 3. MoS 계산 (고위험 성분)
```
MoS = NOAEL × BW / (SED × 100)
MoS ≥ 100: SAFE
MoS < 100: NOT SAFE
```

### 출력 형식

| INCI Name | % | EWG | CIR | MoS | Status |
|-----------|---|-----|-----|-----|--------|

---

safety-oracle 에이전트를 사용하여 평가를 시작합니다.
