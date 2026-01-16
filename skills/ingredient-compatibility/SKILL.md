---
name: ingredient-compatibility
description: 화장품 성분 간 호환성 및 비호환성 분석. pH 의존성, 전하 상호작용, 산화-환원 반응, 킬레이트화, 결정화 등 다양한 비호환성 유형을 평가하고 안정화 전략을 제시. 처방 설계, 안정성 예측, 문제 해결에 사용.
allowed-tools: [Read, Write, Edit, Bash, WebFetch]
license: MIT license
metadata:
    skill-author: EVAS Cosmetic
    original-source: K-Dense Inc. (claude-scientific-skills structure)
    version: 1.0.0
    category: formulation-analysis
---

# Ingredient Compatibility Skill

## Overview

화장품 처방에서 **성분 간 호환성(Ingredient Compatibility)**은 제품의 안정성, 효능, 안전성을 결정하는 핵심 요소입니다. 이 스킬은 성분 간의 물리화학적 상호작용을 분석하여 잠재적인 비호환성을 예측하고, 문제 발생 시 해결 전략을 제시합니다.

비호환성은 제품의 색 변화, 분리, 침전, 점도 변화, 활성 성분 분해 등 다양한 형태로 나타날 수 있으며, 이는 소비자 경험과 제품 효능에 직접적인 영향을 미칩니다.

## When to Use This Skill

- **처방 설계**: 신규 처방 개발 시 성분 조합의 적합성 사전 검토
- **안정성 예측**: 잠재적 안정성 문제 조기 식별
- **문제 해결**: 기존 제품의 안정성 문제 원인 분석 및 해결책 제시
- **원료 대체**: 특정 원료 대체 시 호환성 영향 평가
- **pH 최적화**: 다중 활성 성분의 최적 pH 범위 결정
- **처방 리뷰**: 생산 전 처방 검토 시 호환성 체크리스트 활용

## Core Capabilities

### 1. 비호환성 유형 (Incompatibility Types)

화장품 처방에서 발생하는 주요 비호환성 메커니즘:

#### 1.1 pH 의존성 비호환 (pH-Dependent Incompatibility)

특정 pH 범위에서만 안정하거나 효과적인 성분들의 충돌:

```python
pH_DEPENDENT_INCOMPATIBILITIES = {
    "ASCORBIC ACID + NIACINAMIDE": {
        "condition": "pH < 3.5",
        "mechanism": "낮은 pH에서 Niacinamide가 Nicotinic Acid로 전환, 홍조 유발 가능",
        "reality_check": "실제로는 상온에서 매우 느린 반응, 일반적 사용 조건에서 문제 적음",
        "recommendation": "pH 5-6 범위에서 안정적 공존 가능"
    },
    "AHA + RETINOL": {
        "condition": "AHA 최적 pH 3-4, Retinol 최적 pH 5.5-6.5",
        "mechanism": "상이한 최적 pH 범위로 인한 효능/안정성 저하",
        "recommendation": "별도 제품으로 분리 사용 권장 (AM/PM)"
    },
    "BHA + HIGH pH INGREDIENTS": {
        "condition": "pH > 4",
        "mechanism": "Salicylic Acid의 각질 용해 효과 감소",
        "recommendation": "pH 3-4 유지, 알칼리성 원료와 분리"
    }
}
```

#### 1.2 전하 상호작용 (Charge Interaction)

양이온/음이온 성분 간의 정전기적 상호작용:

```python
CHARGE_INCOMPATIBILITIES = {
    "cationic_anionic": {
        "examples": [
            ("CETRIMONIUM CHLORIDE", "SODIUM LAURYL SULFATE"),
            ("BEHENTRIMONIUM CHLORIDE", "SODIUM LAURETH SULFATE"),
            ("POLYQUATERNIUM-7", "SODIUM COCOYL ISETHIONATE")
        ],
        "result": "침전물 형성, 클럼핑, 제품 탁화",
        "mechanism": "반대 전하의 정전기적 결합으로 불용성 복합체 형성",
        "solution": [
            "양쪽성 또는 비이온 계면활성제로 대체",
            "동일 전하 계열 내에서 선택",
            "양이온 성분을 최종 컨디셔닝 단계에서 별도 적용"
        ]
    },
    "cationic_with_negative_polymers": {
        "examples": [
            ("CETRIMONIUM CHLORIDE", "CARBOMER"),
            ("POLYQUATERNIUM-10", "XANTHAN GUM")
        ],
        "result": "점도 저하, 상분리, 겔 파괴",
        "mechanism": "음이온 폴리머의 전하 중화로 증점 효과 상실",
        "solution": [
            "양이온 적합 증점제 사용 (HYDROXYETHYLCELLULOSE)",
            "비이온 증점제 선택 (HYDROXYPROPYL STARCH PHOSPHATE)"
        ]
    }
}
```

#### 1.3 산화-환원 반응 (Oxidation-Reduction Reactions)

산화제와 환원제의 상호 반응:

```python
REDOX_INCOMPATIBILITIES = {
    "BENZOYL PEROXIDE + RETINOIDS": {
        "oxidizer": "BENZOYL PEROXIDE",
        "reducer": "RETINOL, RETINALDEHYDE, TRETINOIN",
        "result": "Retinoid 산화 분해, 효능 상실",
        "visual_signs": "색상 변화 (황색 -> 갈색)",
        "solution": "별도 제품으로 분리 (AM: BPO, PM: Retinoid)"
    },
    "VITAMIN C + COPPER PEPTIDES": {
        "mechanism": "Cu2+ 이온이 Ascorbic Acid 산화 촉매",
        "result": "Vitamin C 급속 분해, 갈변",
        "visual_signs": "용액 황변 -> 갈변",
        "solution": "별도 루틴에서 사용, 킬레이트제 충분히 첨가"
    },
    "VITAMIN C + VITAMIN E": {
        "type": "Synergistic",
        "mechanism": "Vitamin E가 Vitamin C 라디칼 재생",
        "result": "상호 안정화 효과 (POSITIVE interaction)",
        "recommendation": "함께 사용 권장"
    }
}
```

#### 1.4 킬레이트화 (Chelation)

금속 이온과 킬레이트제 간의 상호작용:

```python
CHELATION_INTERACTIONS = {
    "EDTA + METAL-BASED ACTIVES": {
        "affected_ingredients": [
            "ZINC OXIDE",
            "TITANIUM DIOXIDE",
            "COPPER PEPTIDES",
            "ZINC PCA"
        ],
        "mechanism": "금속 이온 봉쇄로 활성 성분 기능 저하",
        "solution": "금속 기반 활성 성분 사용 시 EDTA 최소화 또는 제거"
    },
    "PHYTIC ACID + MINERALS": {
        "mechanism": "강력한 금속 이온 킬레이트화",
        "affected_functions": "미네랄 기반 성분의 기능 저하",
        "recommendation": "미네랄 활성 성분과 분리"
    }
}
```

#### 1.5 결정화/침전 (Crystallization/Precipitation)

용해도 한계 초과 또는 온도 변화에 의한 고체 형성:

```python
PRECIPITATION_ISSUES = {
    "SALICYLIC ACID": {
        "solubility_limit": "pH 3에서 약 0.2%",
        "common_issue": "과포화 상태에서 결정 석출",
        "signs": "백색 입자, 텍스처 변화",
        "solution": [
            "용해 보조제 사용 (PROPYLENE GLYCOL, BUTYLENE GLYCOL)",
            "pH 조절로 용해도 향상",
            "BHA-HYDROTROPE 복합체 활용"
        ]
    },
    "NIACINAMIDE": {
        "high_concentration_issue": "10% 이상에서 결정화 가능",
        "temperature_sensitive": "저온에서 결정화 경향",
        "solution": [
            "용해 보조제 추가",
            "온도 관리",
            "농도 최적화 (5% 권장)"
        ]
    },
    "ZINC SALTS": {
        "issue": "높은 pH에서 Zinc Hydroxide 침전",
        "ph_range": "pH > 7에서 침전 가능",
        "solution": "pH 5-6.5 유지"
    }
}
```

### 2. 주요 비호환 쌍 (Key Incompatible Pairs)

실무에서 자주 발생하는 비호환 조합:

| 성분 1 | 성분 2 | 비호환 유형 | 심각도 | 현실적 대응 |
|--------|--------|-------------|--------|-------------|
| Retinol | AHA/BHA | pH 충돌, 자극 증폭 | HIGH | AM/PM 분리 |
| Benzoyl Peroxide | Retinoids | 산화 분해 | CRITICAL | 별도 제품 |
| Vitamin C | Niacinamide | pH 의존적 (myth vs reality) | LOW | pH 5-6에서 공존 가능 |
| Cationic surfactant | Anionic surfactant | 전하 충돌 | CRITICAL | 계열 통일 |
| Vitamin C | Copper peptides | 촉매 산화 | HIGH | 시간차 적용 |
| EDTA | Zinc compounds | 킬레이트화 | MEDIUM | EDTA 최소화 |
| Salicylic Acid | Niacinamide | pH 범위 차이 | MEDIUM | pH 절충점 탐색 |

#### Vitamin C + Niacinamide: Myth vs Reality

**오래된 우려**:
- 낮은 pH에서 Niacinamide -> Nicotinic Acid 전환
- Nicotinic Acid는 피부 홍조(flushing) 유발

**현실**:
```python
VITAMIN_C_NIACINAMIDE_REALITY = {
    "conversion_conditions": {
        "temperature": "> 60C",
        "ph": "< 3",
        "time": "extended exposure required"
    },
    "practical_assessment": {
        "room_temperature": "전환 반응 매우 느림 (무시 가능)",
        "typical_formulation_ph": "pH 3.5-5 (안정 범위)",
        "shelf_life_stability": "일반적인 유통기한 내 문제 없음"
    },
    "recommendation": "pH 5-6 범위에서 안전하게 병용 가능",
    "synergy_benefits": [
        "Niacinamide의 세라마이드 합성 촉진",
        "Vitamin C의 콜라겐 합성 지원",
        "상호 보완적 미백 효과"
    ]
}
```

### 3. pH 민감 성분 (pH-Sensitive Ingredients)

pH에 따라 안정성과 효능이 변하는 주요 성분들:

| 성분 | 최적 pH | 허용 범위 | pH 벗어날 때 영향 |
|------|---------|-----------|-------------------|
| L-Ascorbic Acid | 2.5-3.5 | 2.0-4.0 | 산화 가속, 갈변 |
| Ascorbyl Glucoside | 5.0-7.0 | 4.0-7.5 | 가수분해 속도 변화 |
| Retinol | 5.5-6.5 | 5.0-7.0 | 이성질화, 분해 |
| Niacinamide | 5.0-7.0 | 4.0-7.5 | 낮은 pH에서 가수분해 |
| Glycolic Acid | 3.0-4.0 | 2.5-4.5 | 높은 pH에서 효과 감소 |
| Salicylic Acid | 3.0-4.0 | 2.5-4.5 | 높은 pH에서 효과 감소 |
| Azelaic Acid | 4.5-5.5 | 4.0-6.0 | 용해도/효능 변화 |
| Hyaluronic Acid | 5.0-7.0 | 4.0-8.0 | 극단적 pH에서 분해 |
| Peptides (대부분) | 5.0-7.0 | 4.5-7.5 | 가수분해, 응집 |
| Ceramides | 5.0-6.0 | 4.5-7.0 | 가수분해 |

```python
def find_optimal_ph_range(ingredients: list) -> dict:
    """
    여러 성분의 공통 최적 pH 범위 계산

    Args:
        ingredients: INCI명 리스트

    Returns:
        {
            "optimal_ph": 5.5,
            "acceptable_range": (5.0, 6.0),
            "compromises": [
                {"ingredient": "ASCORBIC ACID", "impact": "약간의 안정성 저하"}
            ]
        }
    """
    pass
```

### 4. 안정화 전략 (Stabilization Strategies)

비호환 성분들을 함께 사용하기 위한 전략:

#### 4.1 캡슐화 (Encapsulation)

```python
ENCAPSULATION_STRATEGIES = {
    "liposome": {
        "suitable_for": ["RETINOL", "VITAMIN C", "PEPTIDES"],
        "benefits": [
            "산소/광 차단",
            "pH 환경으로부터 보호",
            "서방출 효과"
        ],
        "considerations": "리포좀 안정성 자체 확보 필요"
    },
    "cyclodextrin_inclusion": {
        "suitable_for": ["RETINOL", "BAKUCHIOL", "FRAGRANCE"],
        "benefits": [
            "용해도 향상",
            "산화 방지",
            "비호환 성분 격리"
        ],
        "common_types": ["ALPHA-CYCLODEXTRIN", "BETA-CYCLODEXTRIN", "HYDROXYPROPYL CYCLODEXTRIN"]
    },
    "silica_microsphere": {
        "suitable_for": ["RETINOL", "VITAMIN C"],
        "benefits": [
            "물리적 격리",
            "서방출",
            "감촉 개선"
        ]
    },
    "double_emulsion": {
        "type": "W/O/W or O/W/O",
        "suitable_for": "호환되지 않는 수용성/유용성 성분 분리",
        "benefits": "내부 상에서 민감 성분 보호"
    }
}
```

#### 4.2 pH 분리 (pH Separation)

```python
def design_ph_separated_formula(actives: list) -> dict:
    """
    pH가 다른 활성 성분들을 위한 이중/다중 시스템 설계

    예: Vitamin C 세럼 + Niacinamide 크림 이중 시스템
    """
    return {
        "system_type": "dual_chamber" | "layered" | "separate_products",
        "phase_1": {
            "ph": 3.0,
            "actives": ["ASCORBIC ACID"],
            "delivery": "first_application"
        },
        "phase_2": {
            "ph": 6.0,
            "actives": ["NIACINAMIDE", "PEPTIDES"],
            "delivery": "second_application"
        },
        "mixing_recommendation": "피부 위에서 혼합 또는 시간차 적용"
    }
```

#### 4.3 산화방지제 첨가 (Antioxidant Addition)

```python
ANTIOXIDANT_STRATEGIES = {
    "for_vitamin_c": {
        "primary": "TOCOPHEROL (Vitamin E)",
        "synergist": "FERULIC ACID",
        "mechanism": "Vitamin E가 Vitamin C 라디칼 재생, Ferulic Acid가 전체 시스템 안정화",
        "famous_formula": "C E Ferulic (15% C + 1% E + 0.5% Ferulic)"
    },
    "for_retinol": {
        "primary": ["TOCOPHEROL", "BHT", "ROSEMARY EXTRACT"],
        "mechanism": "지용성 항산화제가 Retinol 산화 방지",
        "packaging": "에어리스 펌프, 불투명 용기 필수"
    },
    "general_formula_protection": {
        "chelating_agents": ["DISODIUM EDTA", "PHYTIC ACID", "SODIUM PHYTATE"],
        "mechanism": "금속 이온 봉쇄로 산화 촉매 제거"
    }
}
```

#### 4.4 용해 보조제 (Solubilization Aids)

```python
SOLUBILIZATION_STRATEGIES = {
    "hydrotropes": {
        "examples": ["SODIUM XYLENE SULFONATE", "PROPYLENE GLYCOL", "BUTYLENE GLYCOL"],
        "use_for": ["SALICYLIC ACID", "NIACINAMIDE at high %"],
        "mechanism": "용해도 한계 극복, 결정화 방지"
    },
    "surfactant_solubilization": {
        "examples": ["POLYSORBATE 20", "PEG-40 HYDROGENATED CASTOR OIL"],
        "use_for": ["FRAGRANCE", "ESSENTIAL OILS", "OIL-SOLUBLE VITAMINS"],
        "mechanism": "미셀 형성으로 유용성 성분 수상 분산"
    },
    "cosolvents": {
        "examples": ["ETHOXYDIGLYCOL", "PROPYLENE GLYCOL", "ETHANOL"],
        "mechanism": "용매 극성 조절로 난용성 물질 용해"
    }
}
```

## Common Workflows

### Workflow 1: 처방 호환성 검토 (Formula Compatibility Review)

신규 처방 개발 시 전체 성분의 호환성 사전 검토:

```python
def review_formula_compatibility(formula: list[dict]) -> dict:
    """
    전체 처방의 성분 호환성 분석

    Args:
        formula: [
            {"inci": "AQUA", "percent": 70.0},
            {"inci": "NIACINAMIDE", "percent": 5.0},
            {"inci": "ASCORBIC ACID", "percent": 15.0},
            ...
        ]

    Returns:
        {
            "overall_status": "PASS" | "REVIEW_REQUIRED" | "FAIL",
            "critical_issues": [...],
            "warnings": [...],
            "recommendations": [...],
            "ph_recommendation": {"min": 4.5, "max": 5.5}
        }
    """

    # 1. 모든 성분 쌍에 대해 비호환성 검사
    issues = []
    for i, ing1 in enumerate(formula):
        for ing2 in formula[i+1:]:
            compatibility = check_compatibility(ing1["inci"], ing2["inci"])
            if compatibility.has_issue:
                issues.append(compatibility)

    # 2. pH 요구사항 분석
    ph_requirements = analyze_ph_requirements([ing["inci"] for ing in formula])

    # 3. 전하 균형 확인
    charge_analysis = analyze_charge_balance(formula)

    # 4. 산화 민감 성분 확인
    oxidation_risks = check_oxidation_sensitive_ingredients(formula)

    return compile_compatibility_report(issues, ph_requirements, charge_analysis, oxidation_risks)
```

### Workflow 2: 안정성 문제 진단 (Stability Issue Diagnosis)

기존 제품의 안정성 문제 원인 분석:

```python
def diagnose_stability_issue(formula: list, symptoms: list) -> dict:
    """
    안정성 문제 증상을 바탕으로 원인 진단

    Args:
        formula: 처방 정보
        symptoms: [
            "color_change",      # 색상 변화
            "phase_separation",  # 상분리
            "viscosity_drop",    # 점도 저하
            "precipitation",     # 침전
            "odor_change",       # 냄새 변화
            "pH_drift"           # pH 변화
        ]

    Returns:
        {
            "probable_causes": [
                {
                    "cause": "Vitamin C 산화",
                    "confidence": 0.85,
                    "evidence": ["color_change", "pH_drift"],
                    "culprit_ingredients": ["ASCORBIC ACID"]
                }
            ],
            "recommended_tests": [...],
            "solution_options": [...]
        }
    """

    symptom_cause_map = {
        "color_change": ["oxidation", "maillard_reaction", "pH_incompatibility"],
        "phase_separation": ["charge_incompatibility", "temperature_cycling", "emulsifier_failure"],
        "viscosity_drop": ["polymer_degradation", "charge_neutralization", "microbial"],
        "precipitation": ["supersaturation", "pH_shift", "temperature_change"],
        "odor_change": ["oxidation", "microbial", "fragrance_degradation"],
        "pH_drift": ["acid_release", "base_consumption", "buffer_failure"]
    }

    # 증상과 처방을 교차 분석하여 원인 추론
    pass
```

### Workflow 3: 원료 대체 영향 평가 (Ingredient Substitution Assessment)

특정 원료 대체 시 호환성 영향 분석:

```python
def assess_substitution_impact(
    current_formula: list,
    original_ingredient: str,
    replacement_ingredient: str
) -> dict:
    """
    원료 대체가 처방 호환성에 미치는 영향 평가

    Returns:
        {
            "substitution_safe": True | False,
            "new_incompatibilities": [...],
            "resolved_incompatibilities": [...],
            "ph_impact": "none" | "minor" | "significant",
            "charge_impact": "none" | "minor" | "significant",
            "recommendations": [...]
        }
    """
    pass
```

## Best Practices

### 1. 처방 설계 단계에서의 호환성 고려

```
1. 주요 활성 성분 선정
2. 각 활성 성분의 최적 pH 범위 확인
3. pH 범위가 충돌하는 성분 식별
4. 전하 특성 확인 (양이온/음이온/비이온)
5. 산화 민감 성분 파악
6. 비호환 조합에 대한 해결 전략 수립
   - 캡슐화
   - pH 분리
   - 제품 분리 (AM/PM)
   - 대체 성분 선택
```

### 2. 안정성 테스트 프로토콜

```python
STABILITY_TEST_PROTOCOL = {
    "accelerated_conditions": {
        "40C_75RH": "3개월",
        "50C": "1개월 (스크리닝)"
    },
    "real_time_conditions": {
        "25C_60RH": "24개월",
        "4C": "냉장 보관 제품"
    },
    "stress_conditions": {
        "freeze_thaw_cycles": "5회 (-10C <-> 40C)",
        "light_exposure": "ICH Q1B 조건",
        "centrifuge": "3000rpm 30분"
    },
    "check_points": [
        "외관 (색상, 분리, 침전)",
        "pH",
        "점도",
        "향취",
        "미생물",
        "활성 성분 함량 (HPLC)"
    ]
}
```

### 3. 비호환성 발생 시 우선순위 대응

```
Critical (즉시 해결):
- 전하 충돌로 인한 침전
- Benzoyl Peroxide + Retinoid 조합
- 금지 물질 조합

High (처방 수정 필요):
- pH 범위 충돌 (효능 저하)
- 산화-환원 반응
- 용해도 한계 초과

Medium (최적화 권장):
- 마이너 pH 절충
- 킬레이트제 조절

Low (모니터링):
- 장기 안정성에서만 영향
- 이론적 우려 (실제 문제 적음)
```

## Reference Files

상세 정보는 아래 참조 문서 확인:

| 파일 | 내용 |
|------|------|
| `references/incompatibility_matrix.md` | 성분별 비호환성 매트릭스 |
| `references/ph_sensitive_ingredients.md` | pH 민감 성분 상세 정보 |
| `references/oxidation_prone.md` | 산화 민감 성분 및 보호 전략 |
| `scripts/compatibility_check.py` | 호환성 체크 Python 스크립트 |

## Troubleshooting

### 문제: 처방 색상 변화 (Browning/Yellowing)

```
원인 1: Vitamin C 산화
해결: pH 3.0-3.5 유지, Vitamin E/Ferulic Acid 추가, 에어리스 패키징

원인 2: Maillard 반응 (환원당 + 아민)
해결: Niacinamide와 환원당(글루코스 등) 분리

원인 3: 철 이온 오염
해결: EDTA 첨가, 원료 순도 확인
```

### 문제: 상분리

```
원인 1: 양이온-음이온 계면활성제 충돌
해결: 동일 계열 계면활성제로 통일

원인 2: 고농도 전해질
해결: 염 농도 조절, 유화제 재선정

원인 3: 온도 사이클링
해결: 내열/내한성 유화제 선택, 폴리머 안정화제 추가
```

### 문제: 점도 저하

```
원인 1: Carbomer + 양이온 성분
해결: HYDROXYETHYLCELLULOSE로 대체

원인 2: 효소/미생물 오염
해결: 방부 시스템 강화, 원료 품질 확인

원인 3: pH 변화
해결: 버퍼 시스템 강화, pH 모니터링
```

## Quick Reference

```python
# 빠른 호환성 체크
result = check_compatibility("RETINOL", "GLYCOLIC ACID")
# Output: CompatibilityResult(compatible=False, severity="HIGH", reason="pH conflict")

# 처방 전체 분석
issues = analyze_formula([
    {"inci": "ASCORBIC ACID", "percent": 15},
    {"inci": "NIACINAMIDE", "percent": 5},
    {"inci": "FERULIC ACID", "percent": 0.5}
])
# Output: [Issue(type="pH_concern", severity="LOW", note="pH 5-6에서 안정적 공존")]

# 최적 pH 범위 찾기
ph_range = find_optimal_ph_range(["ASCORBIC ACID", "NIACINAMIDE", "HYALURONIC ACID"])
# Output: {"recommended": 5.0, "range": (4.5, 5.5)}
```

## Summary

**ingredient-compatibility** 스킬은 화장품 처방 안정성의 핵심입니다:

1. **비호환성 유형 이해**: pH, 전하, 산화-환원, 킬레이트, 침전
2. **주요 비호환 쌍 파악**: 실무에서 자주 발생하는 문제 조합
3. **pH 민감 성분 관리**: 각 성분의 최적 pH 범위 이해
4. **안정화 전략 적용**: 캡슐화, pH 분리, 항산화제, 용해 보조제
5. **문제 해결**: 증상 기반 원인 진단 및 해결책 제시

체계적인 호환성 분석으로 안정적이고 효과적인 화장품 처방을 개발할 수 있습니다.
