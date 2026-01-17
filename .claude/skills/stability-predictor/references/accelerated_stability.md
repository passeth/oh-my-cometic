# Accelerated Stability Testing Reference

## Overview

가속 안정성 시험(Accelerated Stability Testing)은 스트레스 조건(온도, 습도, 광)에서 제품을 보관하여
실시간 안정성 데이터 없이 유통기한을 예측하는 방법입니다.

## ICH Guidelines

### ICH Q1A(R2) - Stability Testing of New Drug Substances and Products

국제의약품규제조화위원회(ICH)에서 제정한 안정성 시험 가이드라인으로, 화장품에도 널리 적용됩니다.

#### Climate Zones

| Zone | Description | Long-term | Intermediate | Accelerated |
|------|-------------|-----------|--------------|-------------|
| I | Temperate | 21C/45% RH | - | 40C/75% RH |
| II | Mediterranean/Subtropical | 25C/60% RH | 30C/65% RH | 40C/75% RH |
| III | Hot/Dry | 30C/35% RH | - | 40C/75% RH |
| IVa | Hot/Humid | 30C/65% RH | - | 40C/75% RH |
| IVb | Hot/Very Humid | 30C/75% RH | - | 40C/75% RH |

#### Standard Test Conditions

```
Long-term (Zone II):
- Temperature: 25C +/- 2C
- Humidity: 60% RH +/- 5%
- Duration: 12, 24, 36 months
- Sampling: 0, 3, 6, 9, 12, 18, 24, 36 months

Intermediate:
- Temperature: 30C +/- 2C
- Humidity: 65% RH +/- 5%
- Duration: 12 months
- Sampling: 0, 6, 9, 12 months

Accelerated:
- Temperature: 40C +/- 2C
- Humidity: 75% RH +/- 5%
- Duration: 6 months
- Sampling: 0, 1, 2, 3, 6 months
```

## Temperature Conditions

### 4C (Refrigerated)

**목적:**
- 냉장 보관 제품 안정성 확인
- 결정화/침전 경향 평가
- 저온 민감성 확인

**적용 제품:**
- 생물학적 활성 성분 함유 제품
- 열 불안정 성분 함유 제품
- 냉장 화장품 (일부 한방 제품)

**주의사항:**
- 동결 방지 (0C 이하 노출 피함)
- 온도 변동 최소화

### 25C (Room Temperature)

**목적:**
- 실제 보관 환경 시뮬레이션
- 장기 안정성 기준선 설정
- 최종 유통기한 결정

**조건:**
- 온도: 25C +/- 2C
- 습도: 60% RH +/- 5%
- 차광 조건

**평가 주기:**
- 0, 3, 6, 9, 12, 18, 24개월
- 필요시 36개월까지 연장

### 37C (Body Temperature)

**목적:**
- 중간 가속 조건
- 에멀전 안정성 스크리닝
- 립밤, 스틱 제품 평가

**적용:**
- 립 제품 (사용 중 체온 노출)
- 스틱형 제품
- 에멀전 빠른 스크리닝

### 40C (Standard Accelerated)

**목적:**
- ICH 표준 가속 조건
- 6개월 시험으로 24개월 예측
- 규제 제출용 데이터

**조건:**
- 온도: 40C +/- 2C
- 습도: 75% RH +/- 5%
- 기간: 6개월

**예측 공식 (일반적):**
```
40C 6개월 안정 = 25C 24개월 안정 (Q10=2 가정)
```

### 45C (Harsh Accelerated)

**목적:**
- 빠른 스크리닝 테스트
- 처방 비교 평가
- 단기 안정성 경향 파악

**주의사항:**
- 일부 성분은 45C에서 비정상 분해
- 에멀전 상분리 가속
- 실제 안정성과 상관관계 제한적

**적용:**
- 초기 처방 스크리닝
- 처방 간 비교 평가
- 패키지 호환성 예비 테스트

### 50C (Stress Test)

**목적:**
- 극한 스트레스 테스트
- 패키징 평가
- 분해 경로 확인

**제한사항:**
- 실제 안정성 예측에 적합하지 않음
- 과도한 분해 가능성
- 물리적 변화 과장될 수 있음

## Humidity Conditions

### 습도 영향 평가

| 습도 | 제품 유형 | 주요 평가 항목 |
|------|----------|----------------|
| 35% RH | 파우더, 건조 제품 | 수분 흡수, 케이킹 |
| 60% RH | 일반 크림/로션 | 기본 조건 |
| 75% RH | 열대 수출용 | 수분 이동, 팽창 |
| 90% RH | 극한 조건 | 포장 투과성 |

### 수분 투과성 테스트

```
Weight Loss Test:
1. 초기 중량 측정 (W0)
2. 개봉/밀봉 상태로 보관
3. 정기적 중량 측정 (Wt)
4. 수분 손실률 계산: (W0 - Wt) / W0 x 100%

판정 기준:
- 크림/로션: < 5% 손실 (6개월)
- 겔: < 3% 손실 (6개월)
- 세럼: < 2% 손실 (6개월)
```

## Cycle Testing (Freeze-Thaw)

### Standard Protocol

```
Condition:
- Low Temperature: -10C (+/- 2C)
- High Temperature: 45C (+/- 2C)
- Cycle Duration: 24 hours each
- Total Cycles: 6 cycles

Procedure:
1. Sample at T=0 (initial)
2. Store at -10C for 24 hours
3. Transfer to 45C for 24 hours
4. Repeat steps 2-3 for 6 cycles
5. Evaluate after each cycle

Evaluation Points:
- Visual appearance (separation, crystals)
- pH
- Viscosity
- Particle size (if applicable)
- Functional test
```

### Mild Protocol (일반 유통 환경)

```
Condition:
- Low Temperature: 4C
- High Temperature: 40C
- Cycle Duration: 24 hours each
- Total Cycles: 10 cycles

Application:
- 일반 화장품
- 국내 유통 제품
- 민감 성분 함유 제품
```

### Extreme Protocol (운송/수출용)

```
Condition:
- Low Temperature: -20C
- High Temperature: 50C
- Cycle Duration: 12 hours each
- Total Cycles: 5 cycles

Application:
- 수출용 제품
- OEM 납품용
- 항공/선박 운송 제품
```

## Evaluation Criteria

### Physical Stability

| 항목 | 평가 방법 | 판정 기준 |
|------|----------|----------|
| 외관 | 육안 관찰 | 변화 없음 |
| 색상 | Colorimeter | Delta E < 3.0 |
| 냄새 | 관능 평가 | 이취 없음 |
| pH | pH meter | 초기값 +/- 0.5 |
| 점도 | Viscometer | 초기값 +/- 15% |
| 상분리 | 원심분리 | 분리 없음 |

### Chemical Stability

| 항목 | 평가 방법 | 판정 기준 |
|------|----------|----------|
| 활성 성분 함량 | HPLC/UV | 90-110% of label |
| 분해물 | HPLC | 명시된 한도 이하 |
| 방부제 함량 | HPLC | > 90% of initial |

### Microbiological Stability

| 항목 | 평가 방법 | 판정 기준 |
|------|----------|----------|
| 총균수 | Plate count | < 100 CFU/mL |
| 특정 균 | 선택 배지 | 불검출 |
| 방부 효력 | Challenge test | Pass criteria |

## Stability Protocol Template

```yaml
Product: [제품명]
Batch: [배치 번호]
Container: [용기 유형]

Test Conditions:
  - 25C/60% RH (Long-term)
  - 40C/75% RH (Accelerated)
  - Cycle test (-10C/45C x 6)
  - Photostability (ICH Q1B)

Duration:
  - Long-term: 24 months
  - Accelerated: 6 months
  - Cycle: 2 weeks
  - Photo: Per ICH Q1B

Sampling Points:
  Long-term: 0, 3, 6, 9, 12, 18, 24 months
  Accelerated: 0, 1, 2, 3, 6 months
  Cycle: After each cycle

Tests at Each Point:
  - Appearance, color, odor
  - pH
  - Viscosity
  - Active assay
  - Preservative content
  - Microbial count

Acceptance Criteria:
  - pH: Initial +/- 0.5
  - Viscosity: Initial +/- 15%
  - Active: 90-110% label
  - Color: Delta E < 3.0
  - Microbial: < 100 CFU/mL
```

## Interpretation Guidelines

### Accelerated Test Failure

가속 조건에서 실패 시 고려사항:

1. **40C 3개월 내 실패**
   - 처방 재검토 필요
   - 안정화 전략 강화
   - 예상 수명: < 12개월

2. **40C 6개월 내 실패**
   - 중간 조건 확인 (30C)
   - 보관 조건 제한 고려
   - 예상 수명: 12-18개월

3. **40C 6개월 통과**
   - 장기 시험으로 확인
   - 24개월 수명 가능

### Out of Specification (OOS) 처리

```
1. 결과 검증
   - 시험 재수행
   - 분석법 확인

2. 원인 조사
   - 배치 기록 검토
   - 보관 조건 확인

3. 영향 평가
   - 다른 배치 확인
   - 출하 가능성 검토

4. 시정 조치
   - 처방/공정 개선
   - 사양 재설정
```

## References

1. ICH Q1A(R2): Stability Testing of New Drug Substances and Products
2. ICH Q1C: Stability Testing for New Dosage Forms
3. ASEAN Guidelines on Stability Study of Drug Products
4. WHO Technical Report Series, No. 953, 2009
5. FDA Guidance for Industry: Stability Testing
