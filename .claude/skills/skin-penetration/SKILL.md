# Skin Penetration and Permeability Prediction Skill

```yaml
name: skin-penetration
version: 1.0.0
description: 화장품 활성 성분의 피부 투과도 예측 및 전달 시스템 설계
category: formulation-science
keywords:
  - skin penetration
  - permeability
  - transdermal delivery
  - Potts-Guy model
  - Lipinski rules
  - drug delivery
  - cosmetic actives
triggers:
  - 피부 투과
  - 침투율
  - 흡수율
  - 전달 시스템
  - penetration
  - permeability
  - transdermal
  - delivery system
```

## Overview

화장품 활성 성분의 피부 투과도를 예측하고, 최적의 전달 시스템을 설계하기 위한 스킬입니다. 정량적 구조-투과성 관계(QSPR) 모델과 약물 유사성 규칙을 활용하여 성분의 피부 침투 가능성을 평가합니다.

### Why This Matters

피부 투과는 화장품 효능의 핵심 요소입니다:
- **표적 부위 도달**: 활성 성분이 작용 부위까지 도달해야 효과 발현
- **농도 유지**: 적정 농도를 유지해야 치료/미용 효과 지속
- **안전성**: 과도한 침투는 전신 흡수로 이어질 수 있음
- **제형 최적화**: 투과 특성에 맞는 제형 설계 필요

## When to Use This Skill

### Primary Use Cases

1. **활성 성분 선택**
   - 목표 피부층에 도달 가능한 성분 선별
   - 분자량, 친유성 기반 스크리닝
   - 투과 계수 예측

2. **전달 시스템 설계**
   - 리포좀, 나노에멀전 등 캐리어 선택
   - 투과 촉진제 조합 결정
   - 제형 타입 최적화

3. **효능 예측**
   - 피부 내 농도 추정
   - 플럭스(flux) 계산
   - 치료 효과 가능성 평가

4. **규제 대응**
   - 전신 흡수량 추정
   - 안전성 마진 계산
   - NOAEL 대비 노출량 평가

### When NOT to Use

- 정확한 임상 데이터가 필요한 경우 (예측 모델의 한계)
- 복잡한 제형 상호작용 고려 시
- 손상된 피부/질환 피부 조건

## Core Capabilities

### 1. Potts-Guy 모델

피부 투과 계수 예측의 표준 모델:

```
log Kp = 0.71 × log P - 0.0061 × MW - 6.3
```

**파라미터:**
- **Kp**: 투과 계수 (cm/h) - 단위 면적, 단위 농도 구배당 투과 속도
- **log P**: 옥탄올/물 분배계수 (친유성 지표)
- **MW**: 분자량 (Da)

**해석:**
| log Kp 범위 | 투과성 | 예시 성분 |
|------------|--------|----------|
| > -4 | 매우 높음 | 니코틴, 에스트라디올 |
| -4 ~ -5 | 높음 | 카페인, 살리실산 |
| -5 ~ -6 | 중간 | 레티놀, 나이아신아마이드 |
| -6 ~ -7 | 낮음 | 히알루론산 (저분자) |
| < -7 | 매우 낮음 | 콜라겐, 고분자 HA |

**적용 예시:**
```python
# 나이아신아마이드 (MW=122, log P=-0.37)
log_kp = 0.71 * (-0.37) - 0.0061 * 122 - 6.3
log_kp = -7.31  # Kp = 4.9 × 10^-8 cm/h
```

### 2. Lipinski's Rule of 5 적용

원래 경구 생체이용률 예측용이나, 피부 투과에도 적용:

| 파라미터 | 경구 기준 | 경피 최적 범위 |
|---------|----------|---------------|
| 분자량 (MW) | < 500 Da | < 500 Da (이상적: < 300) |
| 친유성 (log P) | < 5 | 1 ~ 3 (이상적: 1.5 ~ 2.5) |
| H-bond donors | < 5 | < 3 |
| H-bond acceptors | < 10 | < 5 |

**피부 투과 최적 조건:**
- MW: 100-300 Da (작을수록 유리)
- log P: 1-3 (중간 친유성이 최적)
- 극성 표면적: < 60 Å²

**화장품 활성 성분 분류:**
```
높은 투과성:    레티놀, 비타민 E, 카페인
중간 투과성:    나이아신아마이드, 살리실산, 아젤라산
낮은 투과성:    아스코르빈산, 펩타이드 (작은)
매우 낮은 투과성: 히알루론산, 콜라겐, 대형 펩타이드
```

### 3. 피부층별 투과 예측

#### 각질층 (Stratum Corneum) - 주요 장벽
- 두께: 10-20 μm
- 구조: Brick-and-mortar (각질세포 + 지질 매트릭스)
- 통과 경로:
  - **세포간 경로** (Intercellular): 지질 친화성 물질
  - **경세포 경로** (Transcellular): 친수성 물질
  - **부속기관 경로** (Appendageal): 모낭, 땀샘

```
투과 저항: R_total ≈ R_SC (각질층이 전체 저항의 ~90%)
```

#### 표피 (Epidermis)
- 두께: 50-100 μm
- 특성: 친수성 환경
- 역할: 대사 활성 (효소에 의한 성분 변환)

#### 진피 (Dermis)
- 두께: 1-4 mm
- 특성: 혈관 분포 → 전신 순환 진입점
- 역할: 피부 탄력, 수분 유지

**층별 농도 프로파일:**
```
C_SC > C_epidermis > C_dermis > C_systemic
```

### 4. 투과 촉진제 효과

#### 화학적 촉진제

| 촉진제 | 작용 기전 | 촉진 배수 | 주의사항 |
|-------|----------|----------|---------|
| **에탄올** | 지질 추출, 유동화 | 2-5x | 자극, 건조 |
| **프로필렌글라이콜** | 각질층 수화 | 2-3x | 비교적 안전 |
| **올레산** | 지질 이중층 교란 | 5-10x | 자극 가능 |
| **DMSO** | 단백질 변성 | 10-20x | 높은 자극 |
| **Azone** | 지질 유동화 | 5-15x | 화장품 제한 |
| **테르펜** (리모넨 등) | 지질 추출 | 3-8x | 향료 역할 겸함 |

#### 물리적 방법

| 방법 | 원리 | 촉진 효과 | 적용 |
|-----|------|----------|------|
| **마이크로니들** | 물리적 천공 | 100-1000x | 패치 제형 |
| **이온토포레시스** | 전기적 구동력 | 10-100x | 전하 분자 |
| **초음파** | 캐비테이션 | 5-20x | 대형 분자 |
| **전기천공** | 순간 기공 형성 | 1000x+ | 연구용 |

### 5. 나노 전달 시스템

#### 리포좀 (Liposomes)
- 크기: 50-500 nm
- 구조: 인지질 이중층 소포
- 장점: 생체적합성, 친수/친유성 성분 모두 봉입
- 피부 투과: 융합, 혼합 기전

```
최적 조건:
- 크기: 100-200 nm
- 막 유동성: 콜레스테롤 30-40%
- 전하: 음전하 (피부 친화성)
```

#### 나노에멀전 (Nanoemulsion)
- 크기: 20-200 nm
- 구조: O/W 또는 W/O
- 장점: 높은 안정성, 투명한 외관
- 피부 투과: 계면활성제 효과 + 나노 크기

#### 고체 지질 나노입자 (SLN)
- 크기: 50-1000 nm
- 구조: 고체 지질 코어
- 장점: 안정성, 서방 효과
- 피부 투과: 폐쇄 효과 + 지질 상호작용

#### 나노구조 지질 캐리어 (NLC)
- SLN 개선형
- 구조: 고체 + 액체 지질 혼합
- 장점: 높은 봉입률, 누출 감소

**전달 시스템 선택 가이드:**
```
친수성 활성 (log P < 0):
  → 리포좀 (내부 수상 봉입)
  → W/O 나노에멀전

친유성 활성 (log P > 2):
  → 나노에멀전 (O/W)
  → SLN/NLC (지질 매트릭스)

중간 친유성 (0 < log P < 2):
  → 모든 시스템 적용 가능
  → 리포좀 이중층 봉입 권장
```

## Workflow Example

### 신규 활성 성분 투과 평가

```
1. 분자 특성 확인
   ├── MW, log P, H-bond 수 조사
   └── Lipinski 규칙 체크

2. Potts-Guy 예측
   ├── log Kp 계산
   └── 예상 플럭스 추정

3. 표적 피부층 결정
   ├── 각질층: 보호/보습
   ├── 표피: 미백/각질제거
   └── 진피: 주름개선/탄력

4. 전달 시스템 설계
   ├── 기본 제형 선택
   ├── 촉진제 조합
   └── 나노 캐리어 검토

5. 예상 효능 평가
   ├── 목표 농도 도달 가능성
   └── 안전성 마진 확인
```

## Integration with Other Skills

- **ingredient-database**: 성분 물성 데이터 조회
- **formulation-science**: 제형 설계 최적화
- **stability-testing**: 전달 시스템 안정성 평가
- **safety-assessment**: 전신 노출량 평가

## References

상세 참고 자료:
- [Potts-Guy 모델](references/potts_guy_model.md)
- [Lipinski 규칙](references/lipinski_rules.md)
- [투과 촉진제](references/penetration_enhancers.md)

계산 도구:
- [투과도 계산 스크립트](scripts/permeability_calc.py)

## Literature

1. Potts, R.O. & Guy, R.H. (1992). Predicting skin permeability. *Pharm Res*, 9(5), 663-669.
2. Lipinski, C.A. et al. (2001). Experimental and computational approaches to estimate solubility and permeability. *Adv Drug Deliv Rev*, 46(1-3), 3-26.
3. Bos, J.D. & Meinardi, M.M. (2000). The 500 Dalton rule for the skin penetration of chemical compounds and drugs. *Exp Dermatol*, 9(3), 165-169.
4. Williams, A.C. & Barry, B.W. (2004). Penetration enhancers. *Adv Drug Deliv Rev*, 56(5), 603-618.
