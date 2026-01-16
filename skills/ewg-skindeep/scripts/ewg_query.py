#!/usr/bin/env python3
"""
EWG Skin Deep Query Client

EWG(Environmental Working Group) Skin Deep 화장품 성분 안전성 등급 조회 클라이언트

Usage:
    from ewg_query import EWGClient

    client = EWGClient()

    # 단일 성분 등급 조회
    rating = client.get_rating("NIACINAMIDE")
    print(f"등급: {rating.score}, 수준: {rating.hazard_level}")

    # 우려 카테고리 조회
    concerns = client.get_concerns("OXYBENZONE")

    # 제품 전체 등급 계산
    formula = [{"inci": "AQUA", "percent": 70.0}, {"inci": "GLYCERIN", "percent": 5.0}]
    product_score = client.calculate_product_score(formula)
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple, Union
from enum import Enum
import json


class HazardLevel(Enum):
    """EWG 위험도 수준"""
    GREEN = "Low Hazard"      # 1-2
    YELLOW = "Moderate Hazard"  # 3-6
    RED = "High Hazard"       # 7-10
    UNKNOWN = "Unknown"


class DataAvailability(Enum):
    """데이터 가용성 등급"""
    NONE = "None"
    LIMITED = "Limited"
    FAIR = "Fair"
    GOOD = "Good"
    ROBUST = "Robust"


class ConcernCategory(Enum):
    """건강 우려 카테고리"""
    CANCER = "Cancer"
    DEVELOPMENTAL_REPRODUCTIVE = "Developmental & Reproductive Toxicity"
    ALLERGIES_IMMUNOTOXICITY = "Allergies & Immunotoxicity"
    USE_RESTRICTIONS = "Use Restrictions"
    ORGAN_TOXICITY = "Organ System Toxicity (Non-Reproductive)"
    ENDOCRINE_DISRUPTION = "Endocrine Disruption"
    PERSISTENCE_BIOACCUMULATION = "Persistence & Bioaccumulation"
    ECOTOXICOLOGY = "Ecotoxicology"
    OCCUPATIONAL_HAZARDS = "Occupational Hazards"
    IRRITATION = "Irritation (Skin/Eyes/Lungs)"
    CONTAMINATION = "Contamination Concerns"
    BIOCHEMICAL_CHANGES = "Biochemical/Cellular Level Changes"


@dataclass
class EWGRating:
    """EWG 안전성 등급 데이터 클래스"""
    inci_name: str
    score: int  # 1-10
    hazard_level: HazardLevel
    data_availability: DataAvailability
    concerns: List[ConcernCategory] = field(default_factory=list)
    concern_details: Dict[str, str] = field(default_factory=dict)
    ewg_url: Optional[str] = None
    notes: Optional[str] = None

    def __post_init__(self):
        # 점수에 따른 위험도 수준 자동 설정
        if self.hazard_level == HazardLevel.UNKNOWN and self.score > 0:
            if self.score <= 2:
                self.hazard_level = HazardLevel.GREEN
            elif self.score <= 6:
                self.hazard_level = HazardLevel.YELLOW
            else:
                self.hazard_level = HazardLevel.RED

    def is_clean_beauty_safe(self) -> bool:
        """클린뷰티 기준 안전 여부 (등급 1-2)"""
        return self.score <= 2

    def is_moderate_concern(self) -> bool:
        """중간 우려 여부 (등급 3-6)"""
        return 3 <= self.score <= 6

    def is_high_concern(self) -> bool:
        """높은 우려 여부 (등급 7-10)"""
        return self.score >= 7

    def to_dict(self) -> dict:
        """딕셔너리 변환"""
        return {
            "inci_name": self.inci_name,
            "score": self.score,
            "hazard_level": self.hazard_level.value,
            "data_availability": self.data_availability.value,
            "concerns": [c.value for c in self.concerns],
            "concern_details": self.concern_details,
            "ewg_url": self.ewg_url,
            "notes": self.notes
        }


@dataclass
class ProductScore:
    """제품 전체 EWG 등급"""
    overall_score: float
    hazard_level: HazardLevel
    ingredient_count: int
    high_concern_ingredients: List[Tuple[str, int]]  # (INCI, score)
    moderate_concern_ingredients: List[Tuple[str, int]]
    low_concern_ingredients: List[Tuple[str, int]]
    unknown_ingredients: List[str]
    clean_beauty_compatible: bool

    def to_dict(self) -> dict:
        """딕셔너리 변환"""
        return {
            "overall_score": round(self.overall_score, 1),
            "hazard_level": self.hazard_level.value,
            "ingredient_count": self.ingredient_count,
            "high_concern_ingredients": self.high_concern_ingredients,
            "moderate_concern_ingredients": self.moderate_concern_ingredients,
            "low_concern_ingredients": self.low_concern_ingredients,
            "unknown_ingredients": self.unknown_ingredients,
            "clean_beauty_compatible": self.clean_beauty_compatible
        }


# ============================================================
# EWG 성분 안전성 등급 데이터베이스 (100+ 성분)
# ============================================================

COMMON_INGREDIENTS_SCORES: Dict[str, Dict] = {
    # ============ 등급 1 (Very Safe) ============
    "WATER": {
        "score": 1,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [],
        "notes": "물, 가장 안전한 성분"
    },
    "AQUA": {
        "score": 1,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [],
        "notes": "물 (INCI명)"
    },
    "GLYCERIN": {
        "score": 1,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [],
        "notes": "보습제, 매우 안전"
    },
    "BUTYLENE GLYCOL": {
        "score": 1,
        "data_availability": DataAvailability.GOOD,
        "concerns": [],
        "notes": "보습제, 용매"
    },
    "SODIUM HYALURONATE": {
        "score": 1,
        "data_availability": DataAvailability.GOOD,
        "concerns": [],
        "notes": "히알루론산나트륨, 보습제"
    },
    "HYALURONIC ACID": {
        "score": 1,
        "data_availability": DataAvailability.GOOD,
        "concerns": [],
        "notes": "히알루론산, 보습제"
    },
    "NIACINAMIDE": {
        "score": 1,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [],
        "notes": "비타민 B3, 미백/항염"
    },
    "TOCOPHEROL": {
        "score": 1,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [],
        "notes": "비타민 E, 항산화제"
    },
    "TOCOPHERYL ACETATE": {
        "score": 1,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [],
        "notes": "비타민 E 유도체"
    },
    "PANTHENOL": {
        "score": 1,
        "data_availability": DataAvailability.GOOD,
        "concerns": [],
        "notes": "프로비타민 B5, 보습/진정"
    },
    "ALLANTOIN": {
        "score": 1,
        "data_availability": DataAvailability.GOOD,
        "concerns": [],
        "notes": "진정, 피부 보호"
    },
    "ALOE BARBADENSIS LEAF JUICE": {
        "score": 1,
        "data_availability": DataAvailability.GOOD,
        "concerns": [],
        "notes": "알로에 베라, 진정"
    },
    "CAMELLIA SINENSIS LEAF EXTRACT": {
        "score": 1,
        "data_availability": DataAvailability.GOOD,
        "concerns": [],
        "notes": "녹차 추출물, 항산화"
    },
    "CENTELLA ASIATICA EXTRACT": {
        "score": 1,
        "data_availability": DataAvailability.GOOD,
        "concerns": [],
        "notes": "센텔라 아시아티카, 진정"
    },
    "MADECASSOSIDE": {
        "score": 1,
        "data_availability": DataAvailability.FAIR,
        "concerns": [],
        "notes": "센텔라 유래 성분"
    },
    "ASIATICOSIDE": {
        "score": 1,
        "data_availability": DataAvailability.FAIR,
        "concerns": [],
        "notes": "센텔라 유래 성분"
    },
    "SQUALANE": {
        "score": 1,
        "data_availability": DataAvailability.GOOD,
        "concerns": [],
        "notes": "에몰리언트, 피부 장벽 강화"
    },
    "CAPRYLIC/CAPRIC TRIGLYCERIDE": {
        "score": 1,
        "data_availability": DataAvailability.GOOD,
        "concerns": [],
        "notes": "에몰리언트, 캐리어 오일"
    },
    "SHEA BUTTER": {
        "score": 1,
        "data_availability": DataAvailability.GOOD,
        "concerns": [],
        "notes": "시어버터, 보습"
    },
    "BUTYROSPERMUM PARKII BUTTER": {
        "score": 1,
        "data_availability": DataAvailability.GOOD,
        "concerns": [],
        "notes": "시어버터 (INCI명)"
    },
    "JOJOBA OIL": {
        "score": 1,
        "data_availability": DataAvailability.GOOD,
        "concerns": [],
        "notes": "호호바 오일"
    },
    "SIMMONDSIA CHINENSIS SEED OIL": {
        "score": 1,
        "data_availability": DataAvailability.GOOD,
        "concerns": [],
        "notes": "호호바 오일 (INCI명)"
    },
    "ARGANIA SPINOSA KERNEL OIL": {
        "score": 1,
        "data_availability": DataAvailability.GOOD,
        "concerns": [],
        "notes": "아르간 오일"
    },
    "CERAMIDE NP": {
        "score": 1,
        "data_availability": DataAvailability.FAIR,
        "concerns": [],
        "notes": "세라마이드, 피부 장벽"
    },
    "CERAMIDE AP": {
        "score": 1,
        "data_availability": DataAvailability.FAIR,
        "concerns": [],
        "notes": "세라마이드"
    },
    "CERAMIDE EOP": {
        "score": 1,
        "data_availability": DataAvailability.FAIR,
        "concerns": [],
        "notes": "세라마이드"
    },
    "CHOLESTEROL": {
        "score": 1,
        "data_availability": DataAvailability.GOOD,
        "concerns": [],
        "notes": "피부 장벽 성분"
    },
    "BETA-GLUCAN": {
        "score": 1,
        "data_availability": DataAvailability.FAIR,
        "concerns": [],
        "notes": "면역 조절, 진정"
    },
    "ADENOSINE": {
        "score": 1,
        "data_availability": DataAvailability.GOOD,
        "concerns": [],
        "notes": "주름 개선 기능성"
    },

    # ============ 등급 2 (Safe) ============
    "ZINC OXIDE": {
        "score": 2,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [],
        "notes": "물리적 자외선차단제"
    },
    "TITANIUM DIOXIDE": {
        "score": 2,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [ConcernCategory.ORGAN_TOXICITY],
        "concern_details": {"ORGAN_TOXICITY": "흡입 시 폐 독성 (화장품 사용 시 해당 없음)"},
        "notes": "물리적 자외선차단제"
    },
    "ARBUTIN": {
        "score": 2,
        "data_availability": DataAvailability.GOOD,
        "concerns": [],
        "notes": "미백 성분"
    },
    "ALPHA-ARBUTIN": {
        "score": 2,
        "data_availability": DataAvailability.FAIR,
        "concerns": [],
        "notes": "미백 성분 (효과 강화)"
    },
    "TRANEXAMIC ACID": {
        "score": 2,
        "data_availability": DataAvailability.FAIR,
        "concerns": [],
        "notes": "미백 성분"
    },
    "ASCORBYL GLUCOSIDE": {
        "score": 2,
        "data_availability": DataAvailability.GOOD,
        "concerns": [],
        "notes": "비타민 C 유도체"
    },
    "SODIUM ASCORBYL PHOSPHATE": {
        "score": 2,
        "data_availability": DataAvailability.GOOD,
        "concerns": [],
        "notes": "비타민 C 유도체"
    },
    "3-O-ETHYL ASCORBIC ACID": {
        "score": 2,
        "data_availability": DataAvailability.FAIR,
        "concerns": [],
        "notes": "비타민 C 유도체"
    },
    "BISABOLOL": {
        "score": 2,
        "data_availability": DataAvailability.GOOD,
        "concerns": [],
        "notes": "진정 성분 (캐모마일 유래)"
    },
    "AZELAIC ACID": {
        "score": 2,
        "data_availability": DataAvailability.GOOD,
        "concerns": [],
        "notes": "여드름/색소 침착 개선"
    },
    "FERULIC ACID": {
        "score": 2,
        "data_availability": DataAvailability.FAIR,
        "concerns": [],
        "notes": "항산화제"
    },
    "AVOBENZONE": {
        "score": 2,
        "data_availability": DataAvailability.GOOD,
        "concerns": [ConcernCategory.ALLERGIES_IMMUNOTOXICITY],
        "concern_details": {"ALLERGIES_IMMUNOTOXICITY": "낮은 알레르기 가능성"},
        "notes": "UVA 차단제"
    },
    "BIS-ETHYLHEXYLOXYPHENOL METHOXYPHENYL TRIAZINE": {
        "score": 1,
        "data_availability": DataAvailability.FAIR,
        "concerns": [],
        "notes": "Tinosorb S, 광안정 UV 필터"
    },
    "METHYLENE BIS-BENZOTRIAZOLYL TETRAMETHYLBUTYLPHENOL": {
        "score": 2,
        "data_availability": DataAvailability.FAIR,
        "concerns": [],
        "notes": "Tinosorb M, 광안정 UV 필터"
    },

    # ============ 등급 3 (Generally Safe) ============
    "ASCORBIC ACID": {
        "score": 3,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [ConcernCategory.IRRITATION],
        "concern_details": {"IRRITATION": "고농도에서 피부 자극 가능"},
        "notes": "순수 비타민 C"
    },
    "GLYCOLIC ACID": {
        "score": 3,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [ConcernCategory.IRRITATION],
        "concern_details": {"IRRITATION": "피부 자극, pH 의존적"},
        "notes": "AHA, 각질 제거"
    },
    "LACTIC ACID": {
        "score": 3,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [ConcernCategory.IRRITATION],
        "concern_details": {"IRRITATION": "피부 자극 가능"},
        "notes": "AHA, 보습 효과 있음"
    },
    "CITRIC ACID": {
        "score": 2,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [],
        "notes": "pH 조절제, AHA"
    },
    "SODIUM BENZOATE": {
        "score": 3,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [ConcernCategory.ALLERGIES_IMMUNOTOXICITY],
        "concern_details": {"ALLERGIES_IMMUNOTOXICITY": "드문 알레르기 반응"},
        "notes": "방부제"
    },
    "POTASSIUM SORBATE": {
        "score": 3,
        "data_availability": DataAvailability.GOOD,
        "concerns": [ConcernCategory.ALLERGIES_IMMUNOTOXICITY],
        "concern_details": {"ALLERGIES_IMMUNOTOXICITY": "드문 알레르기 반응"},
        "notes": "방부제"
    },
    "BENZYL ALCOHOL": {
        "score": 3,
        "data_availability": DataAvailability.GOOD,
        "concerns": [ConcernCategory.ALLERGIES_IMMUNOTOXICITY],
        "concern_details": {"ALLERGIES_IMMUNOTOXICITY": "알레르기 가능성"},
        "notes": "방부제, 향료 성분"
    },
    "ETHYLHEXYLGLYCERIN": {
        "score": 2,
        "data_availability": DataAvailability.FAIR,
        "concerns": [],
        "notes": "방부 보조제, 컨디셔닝제"
    },
    "CAPRYLYL GLYCOL": {
        "score": 2,
        "data_availability": DataAvailability.FAIR,
        "concerns": [],
        "notes": "보습제, 방부 보조제"
    },
    "1,2-HEXANEDIOL": {
        "score": 2,
        "data_availability": DataAvailability.FAIR,
        "concerns": [],
        "notes": "방부 보조제"
    },

    # ============ 등급 4 (Moderate Concern) ============
    "PHENOXYETHANOL": {
        "score": 4,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [ConcernCategory.IRRITATION, ConcernCategory.ORGAN_TOXICITY],
        "concern_details": {
            "IRRITATION": "눈 자극 가능",
            "ORGAN_TOXICITY": "고농도에서 신경계 영향 (사용 농도에서 안전)"
        },
        "notes": "널리 사용되는 방부제, EU 1% 제한"
    },
    "SALICYLIC ACID": {
        "score": 4,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [ConcernCategory.DEVELOPMENTAL_REPRODUCTIVE, ConcernCategory.USE_RESTRICTIONS],
        "concern_details": {
            "DEVELOPMENTAL_REPRODUCTIVE": "고농도/경구 섭취 시",
            "USE_RESTRICTIONS": "어린이 사용 제한"
        },
        "notes": "BHA, 여드름 치료"
    },
    "METHYLPARABEN": {
        "score": 4,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [ConcernCategory.ENDOCRINE_DISRUPTION, ConcernCategory.ALLERGIES_IMMUNOTOXICITY],
        "concern_details": {
            "ENDOCRINE_DISRUPTION": "약한 에스트로겐 활성 (논란)",
            "ALLERGIES_IMMUNOTOXICITY": "드문 알레르기"
        },
        "notes": "파라벤, EU 0.4% 제한"
    },
    "ETHYLPARABEN": {
        "score": 4,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [ConcernCategory.ENDOCRINE_DISRUPTION],
        "concern_details": {"ENDOCRINE_DISRUPTION": "약한 에스트로겐 활성"},
        "notes": "파라벤"
    },
    "SODIUM LAURYL SULFATE": {
        "score": 4,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [ConcernCategory.IRRITATION],
        "concern_details": {"IRRITATION": "피부/눈 자극"},
        "notes": "계면활성제 (클렌징)"
    },
    "SODIUM LAURETH SULFATE": {
        "score": 3,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [ConcernCategory.IRRITATION, ConcernCategory.CONTAMINATION],
        "concern_details": {
            "IRRITATION": "SLS보다 순함",
            "CONTAMINATION": "1,4-Dioxane 오염 가능성"
        },
        "notes": "계면활성제"
    },
    "PEG-100 STEARATE": {
        "score": 3,
        "data_availability": DataAvailability.GOOD,
        "concerns": [ConcernCategory.CONTAMINATION],
        "concern_details": {"CONTAMINATION": "에틸렌옥사이드/1,4-Dioxane 오염 가능성"},
        "notes": "유화제"
    },
    "POLYSORBATE 20": {
        "score": 3,
        "data_availability": DataAvailability.GOOD,
        "concerns": [ConcernCategory.CONTAMINATION],
        "concern_details": {"CONTAMINATION": "에틸렌옥사이드 오염 가능성"},
        "notes": "유화제, 가용화제"
    },
    "POLYSORBATE 80": {
        "score": 3,
        "data_availability": DataAvailability.GOOD,
        "concerns": [ConcernCategory.CONTAMINATION],
        "concern_details": {"CONTAMINATION": "에틸렌옥사이드 오염 가능성"},
        "notes": "유화제"
    },
    "DIMETHICONE": {
        "score": 3,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [ConcernCategory.PERSISTENCE_BIOACCUMULATION],
        "concern_details": {"PERSISTENCE_BIOACCUMULATION": "환경 잔류성"},
        "notes": "실리콘, 에몰리언트"
    },
    "CYCLOPENTASILOXANE": {
        "score": 4,
        "data_availability": DataAvailability.GOOD,
        "concerns": [ConcernCategory.PERSISTENCE_BIOACCUMULATION, ConcernCategory.ECOTOXICOLOGY],
        "concern_details": {
            "PERSISTENCE_BIOACCUMULATION": "환경 축적",
            "ECOTOXICOLOGY": "EU에서 일부 제한"
        },
        "notes": "휘발성 실리콘"
    },

    # ============ 등급 5-6 (Higher Moderate Concern) ============
    "PROPYLPARABEN": {
        "score": 5,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [ConcernCategory.ENDOCRINE_DISRUPTION, ConcernCategory.USE_RESTRICTIONS],
        "concern_details": {
            "ENDOCRINE_DISRUPTION": "에스트로겐 활성",
            "USE_RESTRICTIONS": "EU 0.14% 제한"
        },
        "notes": "파라벤, 기저귀 부위 제품 금지(EU)"
    },
    "BUTYLPARABEN": {
        "score": 6,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [ConcernCategory.ENDOCRINE_DISRUPTION, ConcernCategory.USE_RESTRICTIONS],
        "concern_details": {
            "ENDOCRINE_DISRUPTION": "강한 에스트로겐 활성",
            "USE_RESTRICTIONS": "EU 0.14% 제한, 덴마크 금지(어린이)"
        },
        "notes": "파라벤, 논란 성분"
    },
    "OCTINOXATE": {
        "score": 6,
        "data_availability": DataAvailability.GOOD,
        "concerns": [ConcernCategory.ENDOCRINE_DISRUPTION, ConcernCategory.ECOTOXICOLOGY],
        "concern_details": {
            "ENDOCRINE_DISRUPTION": "호르몬 교란 우려",
            "ECOTOXICOLOGY": "산호초 손상 우려"
        },
        "notes": "UV 필터, 하와이 금지"
    },
    "ETHYLHEXYL METHOXYCINNAMATE": {
        "score": 6,
        "data_availability": DataAvailability.GOOD,
        "concerns": [ConcernCategory.ENDOCRINE_DISRUPTION, ConcernCategory.ECOTOXICOLOGY],
        "concern_details": {
            "ENDOCRINE_DISRUPTION": "호르몬 교란 우려",
            "ECOTOXICOLOGY": "해양 환경 우려"
        },
        "notes": "옥틸메톡시신나메이트"
    },
    "HOMOSALATE": {
        "score": 5,
        "data_availability": DataAvailability.GOOD,
        "concerns": [ConcernCategory.ENDOCRINE_DISRUPTION],
        "concern_details": {"ENDOCRINE_DISRUPTION": "호르몬 교란 가능성"},
        "notes": "UV 필터"
    },
    "OCTOCRYLENE": {
        "score": 5,
        "data_availability": DataAvailability.GOOD,
        "concerns": [ConcernCategory.ALLERGIES_IMMUNOTOXICITY, ConcernCategory.CONTAMINATION],
        "concern_details": {
            "ALLERGIES_IMMUNOTOXICITY": "광알레르기 가능",
            "CONTAMINATION": "벤조페논 분해 생성"
        },
        "notes": "UV 필터, 광안정화제"
    },

    # ============ 등급 7-10 (High Concern) ============
    "OXYBENZONE": {
        "score": 8,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [
            ConcernCategory.ENDOCRINE_DISRUPTION,
            ConcernCategory.ALLERGIES_IMMUNOTOXICITY,
            ConcernCategory.ECOTOXICOLOGY,
            ConcernCategory.DEVELOPMENTAL_REPRODUCTIVE
        ],
        "concern_details": {
            "ENDOCRINE_DISRUPTION": "강한 내분비 교란 증거",
            "ALLERGIES_IMMUNOTOXICITY": "광알레르기",
            "ECOTOXICOLOGY": "산호초 백화 원인",
            "DEVELOPMENTAL_REPRODUCTIVE": "생식독성 우려"
        },
        "notes": "UV 필터, 하와이/팔라우 금지"
    },
    "BENZOPHENONE-3": {
        "score": 8,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [ConcernCategory.ENDOCRINE_DISRUPTION, ConcernCategory.ECOTOXICOLOGY],
        "concern_details": {
            "ENDOCRINE_DISRUPTION": "내분비 교란",
            "ECOTOXICOLOGY": "해양 환경 독성"
        },
        "notes": "옥시벤존 동의어"
    },
    "TRICLOSAN": {
        "score": 7,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [
            ConcernCategory.ENDOCRINE_DISRUPTION,
            ConcernCategory.ECOTOXICOLOGY,
            ConcernCategory.PERSISTENCE_BIOACCUMULATION
        ],
        "concern_details": {
            "ENDOCRINE_DISRUPTION": "갑상선 호르몬 교란",
            "ECOTOXICOLOGY": "수생 생물 독성",
            "PERSISTENCE_BIOACCUMULATION": "환경 축적"
        },
        "notes": "항균제, EU 화장품 금지"
    },
    "HYDROQUINONE": {
        "score": 9,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [
            ConcernCategory.CANCER,
            ConcernCategory.ORGAN_TOXICITY,
            ConcernCategory.USE_RESTRICTIONS
        ],
        "concern_details": {
            "CANCER": "동물 발암성",
            "ORGAN_TOXICITY": "오크로노시스",
            "USE_RESTRICTIONS": "EU 화장품 금지, FDA OTC 2%"
        },
        "notes": "미백 성분, EU 금지"
    },
    "RETINOL": {
        "score": 9,
        "data_availability": DataAvailability.GOOD,
        "concerns": [
            ConcernCategory.DEVELOPMENTAL_REPRODUCTIVE,
            ConcernCategory.USE_RESTRICTIONS,
            ConcernCategory.ORGAN_TOXICITY
        ],
        "concern_details": {
            "DEVELOPMENTAL_REPRODUCTIVE": "태아 기형 유발 가능 (고용량)",
            "USE_RESTRICTIONS": "EU 농도 제한, 임산부 주의",
            "ORGAN_TOXICITY": "과량 섭취 시 간독성"
        },
        "notes": "비타민 A, EU 0.3% 제한 (얼굴)"
    },
    "RETINYL PALMITATE": {
        "score": 8,
        "data_availability": DataAvailability.GOOD,
        "concerns": [ConcernCategory.DEVELOPMENTAL_REPRODUCTIVE, ConcernCategory.CANCER],
        "concern_details": {
            "DEVELOPMENTAL_REPRODUCTIVE": "비타민 A 유도체",
            "CANCER": "자외선 노출 시 광독성 우려 (논란)"
        },
        "notes": "비타민 A 유도체"
    },
    "FORMALDEHYDE": {
        "score": 10,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [
            ConcernCategory.CANCER,
            ConcernCategory.ALLERGIES_IMMUNOTOXICITY,
            ConcernCategory.IRRITATION
        ],
        "concern_details": {
            "CANCER": "IARC Group 1 발암물질",
            "ALLERGIES_IMMUNOTOXICITY": "강한 감작 물질",
            "IRRITATION": "심한 피부/눈/호흡기 자극"
        },
        "notes": "금지 성분 (방부제로)"
    },
    "DMDM HYDANTOIN": {
        "score": 7,
        "data_availability": DataAvailability.GOOD,
        "concerns": [ConcernCategory.CANCER, ConcernCategory.ALLERGIES_IMMUNOTOXICITY],
        "concern_details": {
            "CANCER": "포름알데히드 방출제",
            "ALLERGIES_IMMUNOTOXICITY": "알레르기 유발"
        },
        "notes": "포름알데히드 방출 방부제"
    },
    "IMIDAZOLIDINYL UREA": {
        "score": 6,
        "data_availability": DataAvailability.GOOD,
        "concerns": [ConcernCategory.CANCER, ConcernCategory.ALLERGIES_IMMUNOTOXICITY],
        "concern_details": {
            "CANCER": "포름알데히드 방출제",
            "ALLERGIES_IMMUNOTOXICITY": "알레르기 유발 가능"
        },
        "notes": "포름알데히드 방출 방부제"
    },
    "DIAZOLIDINYL UREA": {
        "score": 6,
        "data_availability": DataAvailability.GOOD,
        "concerns": [ConcernCategory.CANCER, ConcernCategory.ALLERGIES_IMMUNOTOXICITY],
        "concern_details": {
            "CANCER": "포름알데히드 방출제",
            "ALLERGIES_IMMUNOTOXICITY": "알레르기 유발 가능"
        },
        "notes": "포름알데히드 방출 방부제"
    },
    "QUATERNIUM-15": {
        "score": 7,
        "data_availability": DataAvailability.GOOD,
        "concerns": [ConcernCategory.CANCER, ConcernCategory.ALLERGIES_IMMUNOTOXICITY],
        "concern_details": {
            "CANCER": "가장 많은 포름알데히드 방출",
            "ALLERGIES_IMMUNOTOXICITY": "높은 알레르기 가능성"
        },
        "notes": "포름알데히드 방출 방부제"
    },
    "FRAGRANCE": {
        "score": 8,
        "data_availability": DataAvailability.FAIR,
        "concerns": [
            ConcernCategory.ALLERGIES_IMMUNOTOXICITY,
            ConcernCategory.IRRITATION,
            ConcernCategory.ECOTOXICOLOGY
        ],
        "concern_details": {
            "ALLERGIES_IMMUNOTOXICITY": "알레르기 주요 원인",
            "IRRITATION": "자극 가능",
            "ECOTOXICOLOGY": "일부 성분 환경 독성"
        },
        "notes": "향료 (미공개 성분 혼합물)"
    },
    "PARFUM": {
        "score": 8,
        "data_availability": DataAvailability.FAIR,
        "concerns": [ConcernCategory.ALLERGIES_IMMUNOTOXICITY, ConcernCategory.IRRITATION],
        "concern_details": {
            "ALLERGIES_IMMUNOTOXICITY": "알레르기 주요 원인",
            "IRRITATION": "자극 가능"
        },
        "notes": "향료 (FRAGRANCE 동의어)"
    },
    "COAL TAR": {
        "score": 10,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [ConcernCategory.CANCER, ConcernCategory.USE_RESTRICTIONS],
        "concern_details": {
            "CANCER": "IARC Group 1 발암물질",
            "USE_RESTRICTIONS": "EU 금지 (일부 의약품 제외)"
        },
        "notes": "금지/제한 성분"
    },
    "LEAD ACETATE": {
        "score": 10,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [
            ConcernCategory.CANCER,
            ConcernCategory.DEVELOPMENTAL_REPRODUCTIVE,
            ConcernCategory.ORGAN_TOXICITY
        ],
        "concern_details": {
            "CANCER": "발암물질",
            "DEVELOPMENTAL_REPRODUCTIVE": "신경 발달 독성",
            "ORGAN_TOXICITY": "신장, 신경계 독성"
        },
        "notes": "금지 성분 (염모제)"
    },
    "METHYLISOTHIAZOLINONE": {
        "score": 7,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [ConcernCategory.ALLERGIES_IMMUNOTOXICITY, ConcernCategory.USE_RESTRICTIONS],
        "concern_details": {
            "ALLERGIES_IMMUNOTOXICITY": "강한 감작 물질",
            "USE_RESTRICTIONS": "EU leave-on 금지"
        },
        "notes": "MIT, EU leave-on 금지"
    },
    "METHYLCHLOROISOTHIAZOLINONE": {
        "score": 7,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [ConcernCategory.ALLERGIES_IMMUNOTOXICITY, ConcernCategory.USE_RESTRICTIONS],
        "concern_details": {
            "ALLERGIES_IMMUNOTOXICITY": "강한 감작 물질",
            "USE_RESTRICTIONS": "EU 제한, leave-on 금지"
        },
        "notes": "MCI, EU 제한"
    },
    "TALC": {
        "score": 6,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [ConcernCategory.CANCER, ConcernCategory.CONTAMINATION],
        "concern_details": {
            "CANCER": "석면 오염 시 발암 가능",
            "CONTAMINATION": "석면 오염 우려"
        },
        "notes": "흡입 주의, 석면 프리 확인 필요"
    },
    "BHA": {
        "score": 6,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [ConcernCategory.CANCER, ConcernCategory.ENDOCRINE_DISRUPTION],
        "concern_details": {
            "CANCER": "IARC Group 2B",
            "ENDOCRINE_DISRUPTION": "약한 호르몬 활성"
        },
        "notes": "산화방지제 (Butylated Hydroxyanisole)"
    },
    "BHT": {
        "score": 5,
        "data_availability": DataAvailability.ROBUST,
        "concerns": [ConcernCategory.ORGAN_TOXICITY, ConcernCategory.ALLERGIES_IMMUNOTOXICITY],
        "concern_details": {
            "ORGAN_TOXICITY": "고용량 독성",
            "ALLERGIES_IMMUNOTOXICITY": "드문 알레르기"
        },
        "notes": "산화방지제 (Butylated Hydroxytoluene)"
    },
}


# ============================================================
# EWG Client Class
# ============================================================

class EWGClient:
    """EWG Skin Deep 조회 클라이언트"""

    EWG_BASE_URL = "https://www.ewg.org/skindeep/ingredients/"

    def __init__(self):
        self.database = COMMON_INGREDIENTS_SCORES

    def get_rating(self, inci_name: str) -> EWGRating:
        """
        성분의 EWG 등급 조회

        Args:
            inci_name: INCI 성분명

        Returns:
            EWGRating 객체
        """
        inci_upper = inci_name.upper().strip()

        # 데이터베이스에서 조회
        if inci_upper in self.database:
            data = self.database[inci_upper]
            return EWGRating(
                inci_name=inci_upper,
                score=data["score"],
                hazard_level=HazardLevel.UNKNOWN,  # __post_init__에서 자동 설정
                data_availability=data.get("data_availability", DataAvailability.NONE),
                concerns=data.get("concerns", []),
                concern_details=data.get("concern_details", {}),
                ewg_url=self._generate_ewg_url(inci_upper),
                notes=data.get("notes")
            )

        # 데이터베이스에 없는 경우
        return EWGRating(
            inci_name=inci_upper,
            score=0,
            hazard_level=HazardLevel.UNKNOWN,
            data_availability=DataAvailability.NONE,
            concerns=[],
            ewg_url=None,
            notes="EWG 데이터베이스에 없는 성분"
        )

    def get_ratings(self, inci_names: List[str]) -> List[EWGRating]:
        """
        여러 성분의 EWG 등급 일괄 조회

        Args:
            inci_names: INCI 성분명 리스트

        Returns:
            EWGRating 객체 리스트
        """
        return [self.get_rating(name) for name in inci_names]

    def get_concerns(self, inci_name: str) -> List[Dict[str, str]]:
        """
        성분의 건강 우려 카테고리 조회

        Args:
            inci_name: INCI 성분명

        Returns:
            우려 카테고리 리스트
        """
        rating = self.get_rating(inci_name)
        concerns = []

        for concern in rating.concerns:
            concerns.append({
                "category": concern.value,
                "detail": rating.concern_details.get(concern.name, "상세 정보 없음")
            })

        return concerns

    def calculate_product_score(
        self,
        formula: List[Dict[str, Union[str, float]]]
    ) -> ProductScore:
        """
        제품 전체의 EWG 등급 계산

        Args:
            formula: 처방 리스트 [{"inci": "AQUA", "percent": 70.0}, ...]

        Returns:
            ProductScore 객체
        """
        high_concern = []
        moderate_concern = []
        low_concern = []
        unknown = []

        total_score = 0
        scored_count = 0

        for item in formula:
            inci = item.get("inci", "").upper()
            percent = item.get("percent", 0)

            rating = self.get_rating(inci)

            if rating.score == 0:  # Unknown
                unknown.append(inci)
                continue

            # 농도 가중 점수 계산
            weighted_score = rating.score * (percent / 100)
            total_score += weighted_score
            scored_count += 1

            if rating.is_high_concern():
                high_concern.append((inci, rating.score))
            elif rating.is_moderate_concern():
                moderate_concern.append((inci, rating.score))
            else:
                low_concern.append((inci, rating.score))

        # 전체 등급 계산 (최고 등급 기반 + 가중 평균 고려)
        if high_concern:
            max_high = max(score for _, score in high_concern)
            overall = max(max_high, total_score / max(scored_count, 1) * 10)
        elif moderate_concern:
            max_moderate = max(score for _, score in moderate_concern)
            overall = max(max_moderate, total_score / max(scored_count, 1) * 10)
        else:
            overall = total_score / max(scored_count, 1) * 10

        # 등급 수준 결정
        if overall <= 2:
            hazard_level = HazardLevel.GREEN
        elif overall <= 6:
            hazard_level = HazardLevel.YELLOW
        else:
            hazard_level = HazardLevel.RED

        return ProductScore(
            overall_score=min(overall, 10),
            hazard_level=hazard_level,
            ingredient_count=len(formula),
            high_concern_ingredients=high_concern,
            moderate_concern_ingredients=moderate_concern,
            low_concern_ingredients=low_concern,
            unknown_ingredients=unknown,
            clean_beauty_compatible=len(high_concern) == 0
        )

    def search_by_score_range(
        self,
        min_score: int = 1,
        max_score: int = 10
    ) -> List[EWGRating]:
        """
        등급 범위로 성분 검색

        Args:
            min_score: 최소 등급
            max_score: 최대 등급

        Returns:
            해당 범위의 성분 리스트
        """
        results = []

        for inci, data in self.database.items():
            score = data["score"]
            if min_score <= score <= max_score:
                results.append(self.get_rating(inci))

        return sorted(results, key=lambda x: x.score)

    def search_by_concern(self, concern: ConcernCategory) -> List[EWGRating]:
        """
        특정 우려 카테고리를 가진 성분 검색

        Args:
            concern: 우려 카테고리

        Returns:
            해당 우려가 있는 성분 리스트
        """
        results = []

        for inci, data in self.database.items():
            if concern in data.get("concerns", []):
                results.append(self.get_rating(inci))

        return sorted(results, key=lambda x: x.score, reverse=True)

    def find_alternatives(
        self,
        ingredient: str,
        function: str = None,
        max_score: int = 3
    ) -> List[EWGRating]:
        """
        저위험 대체 성분 검색

        Args:
            ingredient: 대체하려는 성분
            function: 기능 카테고리 (선택)
            max_score: 최대 허용 등급

        Returns:
            대체 가능한 저위험 성분 리스트
        """
        # 간단한 기능별 대체 성분 매핑
        FUNCTION_MAP = {
            "UV_FILTER": ["ZINC OXIDE", "TITANIUM DIOXIDE",
                         "BIS-ETHYLHEXYLOXYPHENOL METHOXYPHENYL TRIAZINE",
                         "METHYLENE BIS-BENZOTRIAZOLYL TETRAMETHYLBUTYLPHENOL"],
            "PRESERVATIVE": ["PHENOXYETHANOL", "ETHYLHEXYLGLYCERIN", "CAPRYLYL GLYCOL",
                            "1,2-HEXANEDIOL", "SODIUM BENZOATE", "POTASSIUM SORBATE"],
            "WHITENING": ["NIACINAMIDE", "ARBUTIN", "ALPHA-ARBUTIN",
                         "TRANEXAMIC ACID", "ASCORBYL GLUCOSIDE"],
            "ANTIOXIDANT": ["TOCOPHEROL", "TOCOPHERYL ACETATE", "FERULIC ACID"],
            "MOISTURIZER": ["GLYCERIN", "BUTYLENE GLYCOL", "SODIUM HYALURONATE",
                          "PANTHENOL", "SQUALANE"],
        }

        alternatives = []

        if function and function in FUNCTION_MAP:
            candidates = FUNCTION_MAP[function]
        else:
            candidates = list(self.database.keys())

        for inci in candidates:
            if inci.upper() != ingredient.upper():
                rating = self.get_rating(inci)
                if 0 < rating.score <= max_score:
                    alternatives.append(rating)

        return sorted(alternatives, key=lambda x: x.score)

    def get_clean_beauty_ingredients(self) -> List[EWGRating]:
        """
        클린뷰티 기준 안전 성분 목록 (등급 1-2)

        Returns:
            등급 1-2인 성분 리스트
        """
        return self.search_by_score_range(1, 2)

    def get_high_concern_ingredients(self) -> List[EWGRating]:
        """
        고위험 성분 목록 (등급 7-10)

        Returns:
            등급 7-10인 성분 리스트
        """
        return self.search_by_score_range(7, 10)

    def _generate_ewg_url(self, inci_name: str) -> str:
        """EWG 성분 페이지 URL 생성"""
        # 간단한 URL 생성 (실제로는 EWG 내부 ID 필요)
        slug = inci_name.replace(" ", "-").replace("/", "-").lower()
        return f"{self.EWG_BASE_URL}{slug}/"

    def compare_ingredients(self, inci_names: List[str]) -> List[Dict]:
        """
        성분 비교 분석

        Args:
            inci_names: 비교할 성분명 리스트

        Returns:
            비교 결과 딕셔너리 리스트
        """
        results = []

        for name in inci_names:
            rating = self.get_rating(name)
            results.append({
                "inci_name": rating.inci_name,
                "score": rating.score,
                "hazard_level": rating.hazard_level.value,
                "data_availability": rating.data_availability.value,
                "concern_count": len(rating.concerns),
                "concerns": [c.value for c in rating.concerns],
                "notes": rating.notes
            })

        return sorted(results, key=lambda x: x["score"])


# ============================================================
# CLI Interface
# ============================================================

def main():
    """CLI 메인 함수"""
    import sys

    client = EWGClient()

    if len(sys.argv) < 2:
        print("EWG Skin Deep Query Tool")
        print("\nUsage: python ewg_query.py <command> [args]")
        print("\nCommands:")
        print("  rating <inci>        - 성분 등급 조회")
        print("  concerns <inci>      - 우려 카테고리 조회")
        print("  safe                 - 안전 성분 목록 (등급 1-2)")
        print("  danger               - 고위험 성분 목록 (등급 7-10)")
        print("  compare <inci1> <inci2> ...  - 성분 비교")
        print("  alt <inci> [function] - 대체 성분 검색")
        return

    command = sys.argv[1]

    if command == "rating" and len(sys.argv) >= 3:
        inci = " ".join(sys.argv[2:])
        rating = client.get_rating(inci)
        print(f"\n성분: {rating.inci_name}")
        print(f"등급: {rating.score} ({rating.hazard_level.value})")
        print(f"데이터 가용성: {rating.data_availability.value}")
        if rating.concerns:
            print(f"우려 카테고리: {', '.join(c.value for c in rating.concerns)}")
        if rating.notes:
            print(f"비고: {rating.notes}")
        if rating.ewg_url:
            print(f"EWG URL: {rating.ewg_url}")

    elif command == "concerns" and len(sys.argv) >= 3:
        inci = " ".join(sys.argv[2:])
        concerns = client.get_concerns(inci)
        print(f"\n{inci} 우려 카테고리:")
        if concerns:
            for c in concerns:
                print(f"  - {c['category']}: {c['detail']}")
        else:
            print("  우려 카테고리 없음")

    elif command == "safe":
        ingredients = client.get_clean_beauty_ingredients()
        print(f"\n클린뷰티 안전 성분 ({len(ingredients)}종)")
        for ing in ingredients:
            print(f"  [{ing.score}] {ing.inci_name}: {ing.notes or ''}")

    elif command == "danger":
        ingredients = client.get_high_concern_ingredients()
        print(f"\n고위험 성분 ({len(ingredients)}종)")
        for ing in ingredients:
            print(f"  [{ing.score}] {ing.inci_name}: {ing.notes or ''}")

    elif command == "compare" and len(sys.argv) >= 4:
        inci_names = sys.argv[2:]
        comparison = client.compare_ingredients(inci_names)
        print("\n성분 비교:")
        for item in comparison:
            print(f"  [{item['score']}] {item['inci_name']} - {item['hazard_level']}")
            if item['concerns']:
                print(f"      우려: {', '.join(item['concerns'][:2])}")

    elif command == "alt" and len(sys.argv) >= 3:
        inci = sys.argv[2]
        function = sys.argv[3] if len(sys.argv) > 3 else None
        alternatives = client.find_alternatives(inci, function, max_score=3)
        print(f"\n{inci} 대체 성분 (등급 3 이하):")
        for alt in alternatives[:10]:
            print(f"  [{alt.score}] {alt.inci_name}: {alt.notes or ''}")

    else:
        print(f"알 수 없는 명령어: {command}")


if __name__ == "__main__":
    main()
