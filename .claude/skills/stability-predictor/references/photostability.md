# Photostability Reference

## Overview

광안정성(Photostability)은 화장품이 빛에 노출되었을 때 물리적, 화학적 안정성을 유지하는 능력입니다.
많은 화장품 활성 성분들이 광민감성을 가지며, 적절한 보호 전략이 필요합니다.

## ICH Q1B Guidelines

### Option 1: D65 Standard (Xenon Lamp)

```
Light Source: D65 artificial daylight (Xenon lamp)
UV Exposure: >= 200 Wh/m2 (320-400 nm)
Visible Exposure: >= 1.2 million lux hours

Characteristics:
- 자연광에 가까운 스펙트럼
- UV와 VIS를 동시에 조사
- 산업계에서 가장 널리 사용
```

### Option 2: Separate Sources

```
Visible Light:
- Source: Cool white fluorescent
- Exposure: >= 1.2 million lux hours
- Wavelength: 400-800 nm

UV Light:
- Source: Near-UV fluorescent (UVA)
- Exposure: >= 200 Wh/m2
- Wavelength: 320-400 nm
- Peak at 350-370 nm

순차적 또는 동시 조사 가능
```

### Exposure Calculations

```python
# 노출량 계산 예시

# Visible light (lux * hours)
lux_hours_required = 1.2e6  # 1.2 million lux hours

# 조도 측정값에 따른 노출 시간
intensity_lux = 10000  # 예: 10,000 lux
exposure_time_hours = lux_hours_required / intensity_lux
# = 1,200,000 / 10,000 = 120 hours = 5 days

# UV exposure (Wh/m2)
uv_required = 200  # Wh/m2

# UV intensity에 따른 노출 시간
uv_intensity = 10  # W/m2
uv_exposure_hours = uv_required / uv_intensity
# = 200 / 10 = 20 hours
```

## Test Protocol

### Sample Preparation

```
1. 시험 시료
   - 최종 포장 형태 (primary pack)
   - 직접 노출 시료 (unprotected)
   - 음성 대조군 (wrapped in foil)

2. 배치 선택
   - 최소 1개 배치
   - 대표성 있는 배치

3. 시료 배치
   - 광원에 균일하게 노출
   - 온도 상승 최소화 (< 40C)
```

### Evaluation Points

```
평가 시점:
- T0: 노출 전 (초기)
- T1: 노출 완료 후

평가 항목:
- 외관 (색상 변화)
- 활성 성분 함량
- 분해물 생성
- pH (해당 시)
- 포장 변화
```

### Acceptance Criteria

```
Physical:
- 외관: 유의한 변화 없음
- 색상: Delta E < 3.0 (바람직), < 5.0 (허용)

Chemical:
- 활성 성분: >= 95% of initial (또는 명시 기준)
- 분해물: 명시된 한도 이하
- 알려지지 않은 분해물: < 0.5% (일반적)

Packaging:
- 변색, 균열, 변형 없음
```

## Photosensitive Ingredients

### High Sensitivity

| 성분 | 분해 메커니즘 | 반감기 (직사광) | 보호 전략 |
|------|-------------|----------------|----------|
| Retinol | 이성질화, 산화 | 수분~수시간 | 불투명 용기, 안정화 유도체 |
| Retinaldehyde | 산화 | 수시간 | 불투명 용기 |
| Tretinoin | 이성질화 | 수분 | 처방전용, 야간 사용 |
| Ascorbic Acid | 산화, 갈변 | 수시간 | 불투명 용기, 안정화 유도체 |
| Ubiquinone (CoQ10) | 산화 | 수시간 | 캡슐화, 불투명 용기 |
| Alpha-Lipoic Acid | 분해 | 수시간 | 불투명 용기 |
| Resveratrol | trans-cis 이성질화 | 수시간 | 불투명 용기, 산화방지제 |

### Moderate Sensitivity

| 성분 | 분해 메커니즘 | 주의사항 |
|------|-------------|---------|
| Niacinamide | 서서히 분해 | 장기 노출 시 주의 |
| Ferulic Acid | 산화 | UV 흡수, 자체 보호 효과 |
| Tocopherol | 산화 | 다른 성분 보호 중 소모 |
| Arbutin | 가수분해 | 갈변 가능성 |
| Adenosine | 분해 | 비교적 안정 |

### Photosensitizing Ingredients (광독성/광알러지)

```
주의 성분 (사용자 광민감성 유발):

1. Furocoumarins (Psoralens)
   - Bergaptene (5-MOP)
   - Xanthotoxin (8-MOP)
   - 출처: 감귤류 오일, 셀러리

2. Essential Oils
   - Bergamot oil (bergaptene 함유)
   - Lime oil (expressed)
   - Bitter orange oil
   - Lemon oil (expressed)

   * Cold-pressed (expressed) 오일에 더 많음
   * Bergaptene-free (FCF) 버전 사용 권장

3. Coal Tar Derivatives
   - 비듬 샴푸 성분
   - 광독성 주의

4. 일부 색소
   - Certain azo dyes
   - Eosin derivatives
```

## Photodegradation Mechanisms

### Type I: Direct Photolysis

```
분자가 빛을 직접 흡수하여 분해

A + hv -> A* -> Products

예시:
- Retinol의 trans-cis 이성질화
- Resveratrol의 cis-trans 전환
- 아조 염료의 분해
```

### Type II: Photosensitized Oxidation

```
광증감제가 빛을 흡수하여 산소를 활성화

Sens + hv -> Sens*
Sens* + 3O2 -> Sens + 1O2 (singlet oxygen)
1O2 + A -> A-oxide

예시:
- Riboflavin이 광증감제로 작용
- Chlorophyll derivatives
- 일부 염료
```

### Type III: Radical Chain Reaction

```
빛에 의해 라디칼 생성 후 연쇄 반응

A + hv -> A* -> R* (radical)
R* + O2 -> ROO* (peroxy radical)
ROO* + AH -> ROOH + A*

예시:
- 지질 과산화
- 폴리머 분해
```

## Protection Strategies

### 1. Packaging Solutions

#### Container Type

| 용기 유형 | 광 차단율 | 적용 제품 |
|----------|---------|----------|
| Amber glass | 90-95% UV 차단 | 프리미엄 제품, 고농축 제품 |
| Opaque plastic | 99%+ 차단 | 일반 제품, 대용량 |
| Aluminum tube | 100% 차단 | 연고, 크림 |
| Airless pump | 광+산소 차단 | 세럼, 고활성 제품 |
| White/colored plastic | 부분 차단 | 일반 제품 |
| Clear glass | 차단 없음 | 안정한 제품만 |

#### Secondary Packaging

```
- 종이 상자: 진열 중 보호
- 알루미늄 파우치: 샘플, 단회용
- 차광 라벨: 투명 용기에 적용
```

### 2. Formulation Strategies

#### UV Absorbers (제형 안정화용)

```python
UV_STABILIZERS = {
    "BENZOPHENONE-4": {
        "uv_range": "280-320 nm",
        "level": "0.1-0.3%",
        "function": "제형 내 UV 흡수",
        "note": "규제 확인 필요"
    },
    "ETHYLHEXYL_METHOXYCINNAMATE": {
        "uv_range": "UVB",
        "level": "0.1-0.5%",
        "function": "제형 보호",
        "note": "선스크린 성분, 규제 주의"
    },
    "BUTYL_METHOXYDIBENZOYLMETHANE": {
        "uv_range": "UVA",
        "level": "0.1-0.3%",
        "function": "UVA 차단"
    }
}
```

#### Antioxidants

```python
ANTIOXIDANT_SYSTEMS = {
    "primary": [
        {"name": "TOCOPHEROL", "level": "0.1-0.5%", "mechanism": "radical scavenger"},
        {"name": "BHT", "level": "0.01-0.05%", "mechanism": "radical scavenger"},
        {"name": "BHA", "level": "0.01-0.02%", "mechanism": "radical scavenger"},
        {"name": "ASCORBYL_PALMITATE", "level": "0.1-0.5%", "mechanism": "synergist"}
    ],
    "secondary": [
        {"name": "CITRIC_ACID", "level": "0.1-0.3%", "mechanism": "chelator"},
        {"name": "EDTA", "level": "0.05-0.1%", "mechanism": "metal chelator"},
        {"name": "PHYTIC_ACID", "level": "0.1-0.3%", "mechanism": "natural chelator"}
    ],
    "combination_example": "Tocopherol 0.2% + Ascorbyl Palmitate 0.1% + EDTA 0.05%"
}
```

#### Encapsulation

```
광민감성 성분 캡슐화:

1. Liposomes
   - 이중층 구조로 보호
   - 피부 전달 효과 추가

2. Cyclodextrin Inclusion
   - Beta-cyclodextrin 포접
   - 수용성 개선 + 안정화

3. Solid Lipid Nanoparticles (SLN)
   - 지질 매트릭스 내 봉입
   - 지속 방출 효과

4. Silica/Polymer Microencapsulation
   - 완벽한 광 차단
   - 방출 제어
```

### 3. Stable Derivatives

#### Vitamin C Derivatives

| 유도체 | 광안정성 | 효능 | 비고 |
|-------|---------|------|------|
| Ascorbic Acid | 낮음 | 높음 | 즉시 효과 |
| Sodium Ascorbyl Phosphate | 높음 | 중간 | pH 6-7에서 안정 |
| Ascorbyl Glucoside | 높음 | 중간 | 피부 내 전환 |
| Ascorbyl Tetraisopalmitate | 매우 높음 | 중간 | 지용성 |
| 3-O-Ethyl Ascorbic Acid | 높음 | 높음 | 빠른 침투 |

#### Vitamin A Derivatives

| 유도체 | 광안정성 | 효능 | 비고 |
|-------|---------|------|------|
| Retinol | 낮음 | 높음 | 야간 사용 권장 |
| Retinal (Retinaldehyde) | 중간 | 매우 높음 | Retinol보다 안정 |
| Retinyl Palmitate | 높음 | 낮음 | 전환 필요 |
| Retinyl Retinoate | 높음 | 중간 | 이중 작용 |
| Hydroxypinacolone Retinoate | 높음 | 중간 | 자극 적음 |

## Testing Methods

### Direct Exposure Test

```
목적: 성분/제형의 고유 광안정성 평가

방법:
1. 투명 용기 또는 페트리 접시에 시료 배치
2. ICH Q1B 조건 노출
3. 노출 전후 분석

평가:
- 활성 성분 잔존율
- 분해물 프로파일
- 색상 변화
```

### Forced Degradation Study

```
목적: 분해 경로 확인, stability-indicating method 개발

조건 (예시):
- UV-A: 320-400 nm, 24-48 hours
- UV-C: 254 nm, 1-4 hours (가속)
- Sunlight: 직사광 노출

분석:
- HPLC로 분해물 분리/동정
- LC-MS로 구조 확인
```

### Confirmed Package Test

```
목적: 최종 포장 상태에서의 광안정성 평가

방법:
1. 최종 포장 형태로 노출
2. ICH Q1B 조건
3. 포장 변화 + 내용물 안정성 평가

결과 해석:
- 포장이 충분한 보호 제공하면: OK
- 보호 불충분 시: 포장 변경 또는 사용 지침 추가
```

## Practical Guidelines

### Formulation Development

```
1. 광민감성 성분 확인
   - 문헌 조사
   - 예비 광안정성 시험

2. 보호 전략 선택
   - 유도체 사용
   - 항산화제 조합
   - 적절한 용기 선택

3. 제형 최적화
   - pH 조절 (일부 성분)
   - 점도/매트릭스 효과
   - 캡슐화 고려

4. 포장 선택
   - 광 차단 용기
   - Airless 시스템
   - 이중 포장
```

### Labeling Recommendations

```
광민감성 제품 라벨 권장 문구:

"직사광선을 피해 서늘한 곳에 보관하세요"
"Store away from direct sunlight in a cool place"

"사용 후 뚜껑을 꼭 닫아주세요"
"Close cap tightly after use"

야간 사용 제품:
"취침 전 사용을 권장합니다"
"Recommended for evening use"
```

### Stability Data Requirements

```
광안정성 시험 데이터 요약:

제품: [제품명]
배치: [배치 번호]

시험 조건:
- ICH Q1B Option 1
- UV: 200 Wh/m2
- VIS: 1.2 million lux hours
- 온도: < 40C 유지

결과:
| 항목 | 초기 | 노출 후 | 변화 | 판정 |
|------|-----|--------|------|------|
| 외관 | Clear, colorless | Clear, pale yellow | Slight yellowing | Monitor |
| 활성 함량 | 100.2% | 96.5% | -3.7% | Pass |
| pH | 5.5 | 5.4 | -0.1 | Pass |
| 주요 분해물 | ND | 0.8% | +0.8% | Pass (<2%) |

결론: 광안정성 시험 통과
권장사항: 불투명 용기 사용 권장, 직사광선 피하여 보관
```

## References

1. ICH Q1B: Photostability Testing of New Drug Substances and Products
2. Baertschi, S.W. (2004) J Pharm Sci 95(12):2638-2666
3. Tondoko, B. et al. (2012) Int J Cosmet Sci 34:507-514
4. Brisaert, M. et al. (2001) Int J Pharm 221:49-56
5. Piechocki, J.T., Thoma, K. (eds) (2006) Pharmaceutical Photostability and Stabilization Technology
