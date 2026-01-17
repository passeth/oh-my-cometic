---
name: stability-predictor
description: 화장품 제형 안정성 예측 및 시험 설계. Arrhenius 모델 기반 수명 예측, 가속 안정성 시험 설계, 에멀전 안정성 분석, 광안정성 평가 및 미생물 안정성 Challenge test 가이드 제공.
allowed-tools: [Read, Write, Edit, Bash, WebFetch]
license: MIT license
metadata:
    skill-author: EVAS Cosmetic
    original-source: K-Dense Inc. (claude-scientific-skills structure)
    version: 1.0.0
    category: stability-analysis
---

# Stability Predictor Skill

## Overview

화장품 제형의 **안정성 예측(Stability Prediction)**은 제품 품질 보증과 유통기한 설정의 핵심입니다. 이 스킬은 가속 안정성 시험 설계, Arrhenius 모델 기반 수명 예측, 에멀전 안정성 분석, 광안정성 평가 및 미생물 안정성 평가를 포괄적으로 지원합니다.

제형의 물리적, 화학적, 미생물학적 안정성을 예측하고 모니터링함으로써, 제품 개발 기간을 단축하고 시장 출시 후 품질 문제를 예방할 수 있습니다.

## When to Use This Skill

- **처방 개발**: 신규 처방의 잠재적 안정성 문제 조기 예측
- **안정성 시험 계획**: 가속 시험 프로토콜 설계 및 평가 기준 수립
- **수명 예측**: Arrhenius 모델을 활용한 실온 유통기한 추정
- **문제 해결**: 기존 제품의 안정성 실패 원인 분석
- **제형 최적화**: 에멀전 안정성 개선을 위한 처방 조정
- **규제 대응**: ICH 가이드라인 준수 시험 설계

## Core Capabilities

### 1. 가속 안정성 시험 설계 (Accelerated Stability Testing)

가속 조건에서의 안정성 시험을 통해 실시간 안정성을 예측합니다.

#### 1.1 온도 조건 (Temperature Conditions)

```python
TEMPERATURE_CONDITIONS = {
    "refrigerated": {
        "temperature": 4,  # °C
        "purpose": "냉장 보관 제품, 결정화/침전 확인",
        "products": ["열민감성 제품", "불안정 활성 성분 함유 제품"]
    },
    "room_temperature": {
        "temperature": 25,  # °C
        "humidity": "60% RH",
        "purpose": "실제 보관 조건 시뮬레이션",
        "icH_zone": "Zone I & II"
    },
    "intermediate": {
        "temperature": 30,  # °C
        "humidity": "65% RH",
        "purpose": "온대 및 아열대 조건",
        "icH_zone": "Zone III"
    },
    "accelerated_mild": {
        "temperature": 37,  # °C
        "purpose": "체온 조건, 중간 가속",
        "application": "에멀전 안정성 스크리닝"
    },
    "accelerated_standard": {
        "temperature": 40,  # °C
        "humidity": "75% RH",
        "purpose": "ICH 표준 가속 조건",
        "duration": "6개월",
        "sampling": ["0", "1", "2", "3", "6 개월"]
    },
    "accelerated_harsh": {
        "temperature": 45,  # °C
        "purpose": "빠른 스크리닝, 단기 평가",
        "duration": "3개월",
        "note": "일부 성분은 45°C에서 비정상 분해 가능"
    },
    "stress": {
        "temperature": 50,  # °C
        "purpose": "극한 스트레스 테스트, 패키징 평가",
        "duration": "1개월",
        "caution": "실제 안정성과 상관 관계 제한적"
    }
}
```

#### 1.2 사이클 테스트 (Cycle/Freeze-Thaw Test)

```python
CYCLE_TEST_PROTOCOLS = {
    "standard_freeze_thaw": {
        "low_temp": -10,  # °C
        "high_temp": 45,  # °C
        "cycle_duration": 24,  # hours per temperature
        "total_cycles": 6,
        "purpose": "물리적 안정성 평가 (분리, 결정화, 점도 변화)",
        "evaluation_points": ["각 사이클 종료 후"]
    },
    "mild_thermal_cycling": {
        "low_temp": 4,  # °C
        "high_temp": 40,  # °C
        "cycle_duration": 24,
        "total_cycles": 10,
        "purpose": "일반 유통 환경 시뮬레이션"
    },
    "extreme_cycling": {
        "low_temp": -20,  # °C
        "high_temp": 50,  # °C
        "cycle_duration": 12,
        "total_cycles": 5,
        "purpose": "운송/보관 극한 조건 평가",
        "application": "수출용 제품, OEM 납품"
    }
}
```

#### 1.3 광안정성 (Photostability - ICH Q1B)

```python
PHOTOSTABILITY_CONDITIONS = {
    "ich_q1b_option1": {
        "light_source": "D65 (Xenon lamp)",
        "uv_exposure": "200 Wh/m²",  # 320-400nm
        "visible_exposure": "1.2 million lux·hours",
        "duration": "varies based on lamp intensity",
        "note": "UV와 VIS를 동시에 조사"
    },
    "ich_q1b_option2": {
        "light_source": "Cool white fluorescent + Near UV lamp",
        "uv_exposure": "200 Wh/m²",
        "visible_exposure": "1.2 million lux·hours",
        "separate_sources": True
    },
    "screening_test": {
        "light_source": "Window light simulation",
        "duration": "2-4 weeks",
        "purpose": "빠른 광민감성 스크리닝"
    }
}

PHOTOSENSITIVE_INGREDIENTS = {
    "high_sensitivity": [
        "RETINOL",
        "RETINALDEHYDE",
        "TRETINOIN",
        "ASCORBIC ACID",
        "UBIQUINONE (CoQ10)",
        "ALPHA-LIPOIC ACID",
        "RESVERATROL"
    ],
    "moderate_sensitivity": [
        "NIACINAMIDE",
        "FERULIC ACID",
        "TOCOPHEROL",
        "CAROTENOIDS",
        "FLAVONOIDS"
    ],
    "photosensitizing": [
        "BERGAMOT OIL",
        "CITRUS AURANTIUM OIL",
        "PSORALEN derivatives",
        "COAL TAR"
    ]
}
```

### 2. Arrhenius 모델 수명 예측 (Shelf-Life Prediction)

온도에 따른 반응 속도 변화를 기반으로 실온 수명을 예측합니다.

#### 2.1 Arrhenius 방정식

```python
"""
Arrhenius Equation:
k = A × exp(-Ea / RT)

Where:
- k: 반응 속도 상수 (rate constant)
- A: 빈도 인자 (pre-exponential factor)
- Ea: 활성화 에너지 (activation energy, kJ/mol)
- R: 기체 상수 (8.314 J/mol·K)
- T: 절대 온도 (K)
"""

ARRHENIUS_PARAMETERS = {
    "gas_constant": 8.314,  # J/(mol·K)
    "typical_Ea_range": {
        "hydrolysis": (50, 100),  # kJ/mol
        "oxidation": (40, 80),
        "isomerization": (80, 120),
        "photodegradation": (20, 60),
        "microbial_growth": (50, 150)
    }
}

# 활성화 에너지 데이터베이스 (화장품 관련)
ACTIVATION_ENERGY_DATABASE = {
    "RETINOL": {
        "Ea": 83.7,  # kJ/mol
        "degradation_type": "oxidation, isomerization",
        "Q10": 2.8,
        "reference": "Int J Cosmet Sci. 2015"
    },
    "ASCORBIC_ACID": {
        "Ea": 54.5,  # kJ/mol
        "degradation_type": "oxidation",
        "Q10": 2.0,
        "reference": "J Pharm Sci. 2011"
    },
    "TOCOPHEROL": {
        "Ea": 67.2,  # kJ/mol
        "degradation_type": "oxidation",
        "Q10": 2.3
    },
    "NIACINAMIDE": {
        "Ea": 91.4,  # kJ/mol
        "degradation_type": "hydrolysis",
        "Q10": 3.1
    },
    "EMULSION_STABILITY": {
        "Ea": 45.6,  # kJ/mol (average)
        "degradation_type": "physical separation",
        "Q10": 1.8
    }
}
```

#### 2.2 Q10 Factor (Temperature Coefficient)

```python
"""
Q10: 온도가 10°C 상승할 때 반응 속도 증가 배수

Q10 = k(T+10) / k(T)

화장품 일반적인 Q10 범위: 2-4
- Q10 = 2: 10°C 상승 시 반응 속도 2배 (안정한 성분)
- Q10 = 3: 10°C 상승 시 반응 속도 3배 (중간)
- Q10 = 4: 10°C 상승 시 반응 속도 4배 (불안정한 성분)
"""

Q10_INTERPRETATION = {
    "q10_low": {
        "range": (1.5, 2.0),
        "meaning": "온도에 상대적으로 안정",
        "typical_Ea": "< 50 kJ/mol",
        "examples": ["물리적 분리", "색상 변화"]
    },
    "q10_moderate": {
        "range": (2.0, 3.0),
        "meaning": "보통의 온도 민감성",
        "typical_Ea": "50-80 kJ/mol",
        "examples": ["단순 산화", "가수분해"]
    },
    "q10_high": {
        "range": (3.0, 4.5),
        "meaning": "온도에 민감",
        "typical_Ea": "80-120 kJ/mol",
        "examples": ["복합 분해 반응", "효소 반응"]
    }
}
```

#### 2.3 실온 수명 추정 계산

```python
def predict_shelf_life(accelerated_data, target_temp=25):
    """
    가속 시험 데이터로부터 실온 수명 예측

    Parameters:
    -----------
    accelerated_data: list of dict
        각 온도에서의 분해 속도 데이터
        예: [{"temp": 40, "rate": 0.05}, {"temp": 50, "rate": 0.15}]
    target_temp: float
        예측하려는 보관 온도 (°C)

    Returns:
    --------
    dict: 예측 결과
    """
    import math

    R = 8.314  # J/(mol·K)

    # 최소 2개 온도 데이터 필요
    if len(accelerated_data) < 2:
        raise ValueError("최소 2개 온도에서의 데이터가 필요합니다")

    # Arrhenius plot (ln(k) vs 1/T)
    temps_k = [d["temp"] + 273.15 for d in accelerated_data]
    ln_rates = [math.log(d["rate"]) for d in accelerated_data]

    # 선형 회귀로 Ea 계산
    n = len(temps_k)
    inv_temps = [1/t for t in temps_k]

    sum_x = sum(inv_temps)
    sum_y = sum(ln_rates)
    sum_xy = sum(x*y for x, y in zip(inv_temps, ln_rates))
    sum_x2 = sum(x*x for x in inv_temps)

    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    intercept = (sum_y - slope * sum_x) / n

    Ea = -slope * R / 1000  # kJ/mol
    A = math.exp(intercept)

    # 목표 온도에서의 반응 속도 예측
    target_temp_k = target_temp + 273.15
    k_target = A * math.exp(-Ea * 1000 / (R * target_temp_k))

    # 수명 계산 (90% 잔존 기준)
    shelf_life_days = 0.105 / k_target  # -ln(0.9) ≈ 0.105

    return {
        "activation_energy_kJ_mol": round(Ea, 2),
        "frequency_factor": A,
        "rate_at_target_temp": k_target,
        "estimated_shelf_life_days": round(shelf_life_days, 0),
        "estimated_shelf_life_months": round(shelf_life_days / 30, 1),
        "q10_calculated": round(math.exp(Ea * 1000 * 10 / (R * 298.15 * 308.15)), 2)
    }
```

### 3. 에멀전 안정성 예측 (Emulsion Stability)

에멀전 제형의 물리적 안정성을 예측하고 최적화합니다.

#### 3.1 크리밍/침강 (Creaming/Sedimentation)

```python
"""
Stokes' Law를 기반으로 한 분리 속도 예측

v = (2 * r² * Δρ * g) / (9 * η)

Where:
- v: 분리 속도 (m/s)
- r: 입자 반경 (m)
- Δρ: 밀도 차이 (kg/m³)
- g: 중력 가속도 (9.81 m/s²)
- η: 연속상 점도 (Pa·s)
"""

CREAMING_FACTORS = {
    "particle_size": {
        "impact": "HIGH - v ∝ r²",
        "optimal_range": "< 1 μm",
        "concern_threshold": "> 5 μm",
        "control_methods": [
            "균질화 조건 최적화",
            "적절한 유화제 선택",
            "입자 크기 분포 좁게 유지"
        ]
    },
    "density_difference": {
        "impact": "MODERATE - v ∝ Δρ",
        "typical_values": {
            "oil_in_water": -100,  # kg/m³ (오일이 가벼움 → 크리밍)
            "water_in_oil": +100,  # kg/m³ (물이 무거움 → 침강)
            "silicone_in_water": -50  # 실리콘이 가벼움
        },
        "control_methods": [
            "오일 블렌딩으로 밀도 조절",
            "중량 오일 첨가 (밀도 균형)"
        ]
    },
    "continuous_phase_viscosity": {
        "impact": "HIGH - v ∝ 1/η",
        "recommendation": "> 1000 cP for stability",
        "control_methods": [
            "증점제 사용",
            "구조화제 첨가",
            "겔 네트워크 형성"
        ]
    }
}
```

#### 3.2 합일/융합 (Coalescence)

```python
COALESCENCE_FACTORS = {
    "film_strength": {
        "description": "계면막의 기계적 강도",
        "enhancers": [
            "폴리머 유화제 (ACRYLATES/C10-30 ALKYL ACRYLATE CROSSPOLYMER)",
            "복합 유화 시스템",
            "고분자량 계면활성제"
        ],
        "weakeners": [
            "과량의 친유성 유화제",
            "높은 온도",
            "전해질"
        ]
    },
    "interfacial_tension": {
        "target": "< 5 mN/m for stable emulsion",
        "measurement": "Du Nouy ring, Wilhelmy plate",
        "control": "유화제 농도 및 HLB 최적화"
    },
    "HLB_system": {
        "o_w_emulsion": {
            "required_hlb_range": (8, 16),
            "common_emulsifiers": {
                "POLYSORBATE 60": {"hlb": 14.9},
                "CETEARETH-20": {"hlb": 15.7},
                "PEG-100 STEARATE": {"hlb": 18.8}
            }
        },
        "w_o_emulsion": {
            "required_hlb_range": (3, 8),
            "common_emulsifiers": {
                "SORBITAN OLEATE": {"hlb": 4.3},
                "GLYCERYL MONOSTEARATE": {"hlb": 3.8},
                "PEG-30 DIPOLYHYDROXYSTEARATE": {"hlb": 5.5}
            }
        }
    }
}
```

#### 3.3 Ostwald Ripening

```python
"""
Ostwald Ripening: 작은 입자가 녹아 큰 입자로 이동하는 현상

r³ - r₀³ = ω × t

Where:
- r: 시간 t에서의 평균 반경
- r₀: 초기 평균 반경
- ω: Ostwald ripening rate
- t: 시간
"""

OSTWALD_RIPENING_FACTORS = {
    "oil_solubility": {
        "impact": "CRITICAL - 연속상에서 오일 용해도가 높을수록 빠름",
        "high_solubility_oils": [
            "SHORT-CHAIN TRIGLYCERIDES",
            "ISOPROPYL MYRISTATE",
            "ETHYL OLEATE",
            "LIMONENE"
        ],
        "low_solubility_oils": [
            "LONG-CHAIN TRIGLYCERIDES",
            "MINERAL OIL",
            "SILICONES (DIMETHICONE)",
            "SQUALANE"
        ],
        "control_strategy": "난용성 오일 블렌딩으로 ripening 억제"
    },
    "particle_size_distribution": {
        "impact": "MODERATE - 분포가 넓을수록 빠름",
        "target": "좁은 입자 크기 분포 (PDI < 0.2)",
        "control": "균질화 조건 최적화"
    },
    "ripening_inhibitors": {
        "triglycerides": "장쇄 트리글리세리드 5-10% 첨가",
        "silicones": "고분자량 실리콘 첨가",
        "waxes": "왁스 에스터 소량 첨가"
    }
}
```

### 4. 미생물 안정성 (Microbiological Stability)

#### 4.1 Challenge Test (방부 효력 시험)

```python
CHALLENGE_TEST_PROTOCOLS = {
    "USP_51": {
        "name": "Antimicrobial Effectiveness Testing",
        "organisms": {
            "bacteria": [
                "Escherichia coli (ATCC 8739)",
                "Pseudomonas aeruginosa (ATCC 9027)",
                "Staphylococcus aureus (ATCC 6538)"
            ],
            "yeast": ["Candida albicans (ATCC 10231)"],
            "mold": ["Aspergillus brasiliensis (ATCC 16404)"]
        },
        "inoculum_level": "10⁵ - 10⁶ CFU/mL",
        "sampling_days": [0, 7, 14, 28],
        "criteria": {
            "category_1": {  # 안구/무균 제품
                "bacteria": "99.9% reduction by Day 7, no increase",
                "yeast_mold": "99.0% reduction by Day 7, no increase"
            },
            "category_2": {  # 일반 국소 제품
                "bacteria": "99.0% reduction by Day 14, no increase Day 28",
                "yeast_mold": "90.0% reduction by Day 14, no increase Day 28"
            }
        }
    },
    "ISO_11930": {
        "name": "Evaluation of Antimicrobial Protection",
        "organisms": [
            "Pseudomonas aeruginosa",
            "Staphylococcus aureus",
            "Candida albicans",
            "Aspergillus brasiliensis"
        ],
        "sampling_days": [7, 14, 28],
        "criteria": {
            "A_criterion": "가장 엄격 - 의약부외품 수준",
            "B_criterion": "표준 - 일반 화장품"
        }
    },
    "EP_5.1.3": {
        "name": "European Pharmacopoeia",
        "similar_to": "USP 51",
        "additional_organism": "Zygosaccharomyces rouxii (고삼투압 환경)"
    }
}
```

#### 4.2 미생물 취약성 요인

```python
MICROBIOLOGICAL_RISK_FACTORS = {
    "water_activity": {
        "critical_threshold": 0.6,  # Aw
        "high_risk": "> 0.85",
        "moderate_risk": "0.65 - 0.85",
        "low_risk": "< 0.65",
        "measurement": "Aw meter"
    },
    "ph_effect": {
        "bacteria_optimal": (6.5, 7.5),
        "yeast_optimal": (4.5, 6.5),
        "mold_optimal": (4.0, 7.0),
        "protective_ph": "< 4.0 or > 10.0"
    },
    "nutrient_availability": {
        "high_risk_ingredients": [
            "BOTANICAL EXTRACTS",
            "HYDROLYZED PROTEINS",
            "CARBOHYDRATES",
            "AMINO ACIDS"
        ],
        "low_risk_ingredients": [
            "SILICONES",
            "MINERAL OIL",
            "SYNTHETIC ESTERS"
        ]
    }
}

PRESERVATIVE_SYSTEMS = {
    "traditional": {
        "broad_spectrum": [
            {"name": "PHENOXYETHANOL", "level": "0.5-1.0%", "effective_ph": "< 8"},
            {"name": "ETHYLHEXYLGLYCERIN", "level": "0.3-0.5%", "booster": True}
        ],
        "paraben_free": [
            {"name": "BENZISOTHIAZOLINONE", "level": "0.01%", "caution": "sensitizer"},
            {"name": "METHYLISOTHIAZOLINONE", "level": "0.01%", "restricted": True}
        ]
    },
    "alternative_hurdle": {
        "concept": "다중 장벽 접근법",
        "components": [
            {"name": "CAPRYLYL GLYCOL", "function": "skin conditioning, antimicrobial booster"},
            {"name": "PENTYLENE GLYCOL", "function": "humectant, antimicrobial"},
            {"name": "1,2-HEXANEDIOL", "function": "solvent, antimicrobial"}
        ],
        "combination_example": "Phenoxyethanol 0.3% + Ethylhexylglycerin 0.3% + Caprylyl Glycol 0.3%"
    }
}
```

### 5. 안정성 지표 모니터링 (Stability Indicators)

#### 5.1 물리화학적 지표

```python
STABILITY_INDICATORS = {
    "ph": {
        "method": "pH meter (calibrated)",
        "frequency": "모든 시점",
        "acceptance_criteria": "초기값 ± 0.5 unit",
        "warning_sign": "지속적인 pH drift"
    },
    "viscosity": {
        "method": "Brookfield viscometer",
        "spindle_selection": "Based on expected viscosity",
        "frequency": "모든 시점",
        "acceptance_criteria": "초기값 ± 15%",
        "note": "온도 평형 후 측정 (25°C)"
    },
    "color": {
        "method": {
            "visual": "표준 조명 하에서 백색 배경 대비",
            "instrumental": "Colorimeter (L*a*b* values)"
        },
        "acceptance_criteria": "ΔE < 3.0",
        "common_changes": {
            "yellowing": "산화, 갈변 반응",
            "fading": "색소 분해",
            "darkening": "Maillard 반응, 금속 오염"
        }
    },
    "odor": {
        "method": "관능 평가 (trained panel)",
        "scoring": "1-5 scale",
        "acceptance_criteria": "no significant change",
        "concerns": [
            "산패취",
            "식초취 (산 형성)",
            "암모니아취 (아민 형성)"
        ]
    },
    "particle_size": {
        "method": {
            "laser_diffraction": "Malvern Mastersizer",
            "dynamic_light_scattering": "Zetasizer (for nano)"
        },
        "parameters": ["D10", "D50", "D90", "PDI"],
        "acceptance_criteria": "D50 ± 20%, PDI < 0.3"
    },
    "zeta_potential": {
        "method": "Electrophoretic light scattering",
        "interpretation": {
            "stable": "|ζ| > 30 mV",
            "moderately_stable": "|ζ| 20-30 mV",
            "unstable": "|ζ| < 20 mV"
        },
        "note": "pH 의존적 - 측정 pH 기록 필수"
    }
}
```

#### 5.2 화학적 분석

```python
CHEMICAL_ANALYSIS_METHODS = {
    "active_assay": {
        "method": "HPLC",
        "acceptance_criteria": "90-110% of label claim",
        "degradation_products": "identify and quantify",
        "stability_indicating": "method validation required"
    },
    "preservative_efficacy": {
        "method": "HPLC",
        "frequency": "0, 3, 6, 12 months",
        "acceptance_criteria": "> 90% of initial"
    },
    "antioxidant_level": {
        "method": "HPLC or titration",
        "frequency": "key time points",
        "purpose": "산화 방지제 소모 모니터링"
    }
}
```

### 6. 안정성 문제 해결 가이드 (Troubleshooting)

```python
STABILITY_PROBLEMS = {
    "phase_separation": {
        "symptoms": ["크리밍", "침강", "물 분리"],
        "root_causes": [
            "부적절한 HLB",
            "불충분한 유화제",
            "온도 스트레스",
            "전해질 영향"
        ],
        "solutions": [
            "HLB 최적화 (Required HLB 계산)",
            "유화제 농도 증가 (0.5-1% 단계)",
            "복합 유화 시스템 적용",
            "증점제 추가로 구조 안정화",
            "전해질 제거 또는 감소"
        ]
    },
    "color_change": {
        "symptoms": ["황변", "갈변", "퇴색"],
        "root_causes": [
            "산화",
            "광분해",
            "Maillard 반응",
            "금속 오염",
            "pH 변화"
        ],
        "solutions": [
            "산화방지제 추가/증량",
            "불투명 용기 사용",
            "킬레이트제 첨가",
            "식물 추출물 정제",
            "질소 치환 포장"
        ]
    },
    "odor_change": {
        "symptoms": ["산패취", "이취", "향 약화"],
        "root_causes": [
            "지질 산화",
            "미생물 오염",
            "향료 변성",
            "화학 반응"
        ],
        "solutions": [
            "산화방지제 시스템 강화",
            "방부 시스템 검토",
            "향료 캡슐화",
            "원료 품질 관리"
        ]
    },
    "viscosity_change": {
        "symptoms": ["묽어짐", "굳어짐", "요변성 변화"],
        "root_causes": [
            "폴리머 분해",
            "전해질 영향",
            "미생물 오염",
            "온도 이력",
            "pH 변화"
        ],
        "solutions": [
            "폴리머 안정화",
            "전해질 조절",
            "방부력 강화",
            "가공 온도 관리"
        ]
    },
    "crystallization": {
        "symptoms": ["입자 형성", "gritty 감촉", "석출"],
        "root_causes": [
            "과포화",
            "저온 노출",
            "용해도 한계 초과"
        ],
        "solutions": [
            "용해 보조제 추가",
            "농도 조절",
            "결정화 억제제",
            "보관 온도 관리"
        ]
    }
}
```

## Workflow Examples

### Example 1: 가속 안정성 시험 설계

```
User: 비타민C 세럼의 안정성 시험 프로토콜을 설계해주세요.

Response:
비타민C 세럼 안정성 시험 프로토콜:

**1. 시험 조건:**
- 4C (냉장), 25C/60%RH (실온), 40C/75%RH (가속), 45C (스트레스)
- 광안정성: ICH Q1B (200 Wh/m2 UV, 1.2M lux hr VIS)
- 사이클: -10C to 45C, 6 사이클

**2. 평가 항목:**
- 외관, pH, 점도, 색상 (L*a*b*)
- Ascorbic Acid 함량 (HPLC)
- 산화 분해물 (Dehydroascorbic acid)

**3. 시험 기간:**
- 가속 40C: 0, 1, 2, 3, 6개월
- 실온 25C: 0, 3, 6, 9, 12개월
- 광안정성: 노출 전후

**4. 예상 Q10:** 2.0 (Ascorbic acid 기준)
```

### Example 2: Arrhenius 수명 예측

```
User: 45C에서 2개월, 50C에서 1개월 만에 10% 분해되었습니다.
      25C에서의 수명을 예측해주세요.

Response:
Arrhenius 분석 결과:

**입력 데이터:**
- 45C: k = 0.105 / 60 = 0.00175 /day
- 50C: k = 0.105 / 30 = 0.0035 /day

**계산 결과:**
- 활성화 에너지 (Ea): 약 83 kJ/mol
- Q10: 약 2.8
- 25C 반응속도: 약 0.00022 /day
- 예측 수명 (90% 잔존): 약 477일 (약 16개월)

**신뢰도 평가:**
- 2개 온도점으로 계산 (3개 이상 권장)
- Q10이 일반 범위 내 (2-4)
- 안전 계수 적용 시: 12개월 권장
```

### Example 3: 에멀전 안정성 평가

```
User: O/W 크림이 45C에서 1주일 만에 크리밍이 발생했습니다.

Response:
에멀전 안정성 분석:

**문제 원인 분석:**
1. 입자 크기: D50 > 5um 가능성
2. 점도 불충분: 연속상 점도 < 1000 cP
3. HLB 부적합: Required HLB 계산 필요
4. 유화제 부족: 계면 커버리지 불충분

**권장 개선 조치:**
1. 균질화 조건 강화 (압력 증가, 패스 횟수 증가)
2. 증점제 추가 (Carbomer 0.2-0.3%)
3. 복합 유화제 시스템 적용
4. 입자 크기 분석 후 재균질화

**안정성 스코어:**
현재: 3/10 (불량)
개선 목표: 7/10 이상
```

## Integration Points

### scripts/ 디렉토리

Python 도구들이 위치합니다:
- `stability_model.py`: Arrhenius 모델, Q10 계산, 수명 예측
- 에멀전 안정성 스코어 계산
- 안정성 프로토콜 생성

### references/ 디렉토리

상세 참조 문서가 위치합니다:
- `accelerated_stability.md`: ICH 가이드라인, 시험 조건
- `arrhenius_model.md`: Arrhenius 공식, Ea 데이터베이스
- `photostability.md`: ICH Q1B, 광민감성 성분

## Related Skills

- **ingredient-compatibility**: 성분 간 호환성으로 인한 안정성 예측
- **formulation-calculator**: 처방 계산 및 HLB 최적화
- **regulatory-compliance**: 안정성 시험 규제 요구사항

## References

1. ICH Q1A(R2): Stability Testing of New Drug Substances and Products
2. ICH Q1B: Photostability Testing
3. USP <51> Antimicrobial Effectiveness Testing
4. ISO 11930: Evaluation of Antimicrobial Protection
5. Connors, K.A., et al. Chemical Stability of Pharmaceuticals
6. McClements, D.J. Food Emulsions: Principles, Practices, and Techniques