#!/usr/bin/env python3
"""
CIR (Cosmetic Ingredient Review) Safety Database Query Client

미국 화장품 성분 안전성 평가 기관 CIR 데이터베이스 검색 클라이언트

Usage:
    from cir_search import CIRClient

    client = CIRClient()

    # 성분 안전성 결론 조회
    result = client.search_ingredient("Niacinamide")
    print(f"결론: {result.conclusion}")

    # 보고서 URL 조회
    url = client.get_report_pdf("Retinol")
    print(f"PDF: {url}")

    # 최근 평가 목록
    recent = client.list_recent_assessments(2024)
    for item in recent:
        print(f"{item.ingredient}: {item.conclusion}")
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Union
from enum import Enum
from datetime import datetime
import json


# ============================================================
# Enums and Data Classes
# ============================================================

class SafetyConclusion(Enum):
    """CIR 안전성 결론 유형"""
    SAFE_AS_USED = "Safe as used"
    SAFE_WITH_QUALIFICATIONS = "Safe with qualifications"
    INSUFFICIENT_DATA = "Insufficient data"
    UNSAFE = "Unsafe"
    UNDER_REVIEW = "Under review"
    SPLIT = "Split (see individual reports)"


class ReportType(Enum):
    """CIR 보고서 유형"""
    FINAL_REPORT = "Final Report"
    TENTATIVE_REPORT = "Tentative Report"
    DRAFT_REPORT = "Draft Report"
    RE_REVIEW = "Re-review"
    AMENDED_REPORT = "Amended Report"


class AssessmentStatus(Enum):
    """평가 상태"""
    COMPLETED = "Completed"
    IN_PROGRESS = "In Progress"
    SCHEDULED = "Scheduled"
    RE_REVIEW_PENDING = "Re-review Pending"


@dataclass
class CIRConclusion:
    """CIR 안전성 결론 데이터 클래스"""
    ingredient_name: str
    inci_name: str
    conclusion: SafetyConclusion
    conclusion_text: str
    report_type: ReportType
    assessment_date: str
    journal_reference: Optional[str] = None
    pdf_url: Optional[str] = None
    max_concentration: Optional[Dict[str, float]] = None
    qualifications: Optional[List[str]] = None
    restricted_uses: Optional[List[str]] = None
    group_name: Optional[str] = None
    related_ingredients: Optional[List[str]] = None
    next_review_date: Optional[str] = None
    notes: Optional[str] = None

    def is_safe(self) -> bool:
        """안전 여부 (조건부 포함)"""
        return self.conclusion in [
            SafetyConclusion.SAFE_AS_USED,
            SafetyConclusion.SAFE_WITH_QUALIFICATIONS
        ]

    def has_restrictions(self) -> bool:
        """제한 조건 존재 여부"""
        return self.conclusion == SafetyConclusion.SAFE_WITH_QUALIFICATIONS

    def needs_more_data(self) -> bool:
        """추가 데이터 필요 여부"""
        return self.conclusion == SafetyConclusion.INSUFFICIENT_DATA

    def to_dict(self) -> dict:
        """딕셔너리 변환"""
        return {
            "ingredient_name": self.ingredient_name,
            "inci_name": self.inci_name,
            "conclusion": self.conclusion.value,
            "conclusion_text": self.conclusion_text,
            "report_type": self.report_type.value,
            "assessment_date": self.assessment_date,
            "journal_reference": self.journal_reference,
            "pdf_url": self.pdf_url,
            "max_concentration": self.max_concentration,
            "qualifications": self.qualifications,
            "restricted_uses": self.restricted_uses,
            "group_name": self.group_name,
            "related_ingredients": self.related_ingredients,
            "next_review_date": self.next_review_date,
            "notes": self.notes
        }


@dataclass
class IngredientGroup:
    """성분 그룹 정보"""
    group_name: str
    ingredients: List[str]
    conclusion: SafetyConclusion
    assessment_date: str
    report_reference: str


@dataclass
class AssessmentInfo:
    """평가 현황 정보"""
    ingredient: str
    status: AssessmentStatus
    original_date: Optional[str] = None
    latest_review_date: Optional[str] = None
    next_review_due: Optional[str] = None
    current_conclusion: Optional[SafetyConclusion] = None


# ============================================================
# CIR Database (Sample Data)
# ============================================================

CIR_DATABASE: Dict[str, CIRConclusion] = {
    # Safe as Used - 보습/기본 성분
    "GLYCERIN": CIRConclusion(
        ingredient_name="Glycerin",
        inci_name="GLYCERIN",
        conclusion=SafetyConclusion.SAFE_AS_USED,
        conclusion_text="Safe as used in cosmetics",
        report_type=ReportType.RE_REVIEW,
        assessment_date="2019",
        journal_reference="Int J Toxicol. 2019;38(1_suppl):5S-22S",
        pdf_url="https://www.cir-safety.org/ingredients/glycerin",
        notes="Most widely used cosmetic ingredient"
    ),
    "NIACINAMIDE": CIRConclusion(
        ingredient_name="Niacinamide",
        inci_name="NIACINAMIDE",
        conclusion=SafetyConclusion.SAFE_AS_USED,
        conclusion_text="Safe as used in cosmetics",
        report_type=ReportType.RE_REVIEW,
        assessment_date="2020",
        journal_reference="Int J Toxicol. 2005;24 Suppl 5:1-31 (Original), Re-review 2020",
        pdf_url="https://www.cir-safety.org/ingredients/niacinamide",
        notes="Commonly used up to 5%"
    ),
    "HYALURONIC ACID": CIRConclusion(
        ingredient_name="Hyaluronic Acid",
        inci_name="HYALURONIC ACID",
        conclusion=SafetyConclusion.SAFE_AS_USED,
        conclusion_text="Safe as used in cosmetics",
        report_type=ReportType.FINAL_REPORT,
        assessment_date="2022",
        journal_reference="Int J Toxicol. 2022;41(1_suppl):9S-35S",
        pdf_url="https://www.cir-safety.org/ingredients/hyaluronic-acid",
        related_ingredients=["Sodium Hyaluronate", "Hydrolyzed Hyaluronic Acid"],
        notes="All molecular weights assessed"
    ),
    "TOCOPHEROL": CIRConclusion(
        ingredient_name="Tocopherol",
        inci_name="TOCOPHEROL",
        conclusion=SafetyConclusion.SAFE_AS_USED,
        conclusion_text="Safe as used in cosmetics",
        report_type=ReportType.RE_REVIEW,
        assessment_date="2018",
        journal_reference="Int J Toxicol. 2018;37(2_suppl):61S-94S",
        pdf_url="https://www.cir-safety.org/ingredients/tocopherol",
        group_name="Vitamin E",
        related_ingredients=["Tocopheryl Acetate", "Tocopheryl Linoleate"]
    ),
    "SQUALANE": CIRConclusion(
        ingredient_name="Squalane",
        inci_name="SQUALANE",
        conclusion=SafetyConclusion.SAFE_AS_USED,
        conclusion_text="Safe as used in cosmetics",
        report_type=ReportType.FINAL_REPORT,
        assessment_date="2020",
        journal_reference="Int J Toxicol. 1982;1(2):37-56 (Original), Re-review 2020",
        pdf_url="https://www.cir-safety.org/ingredients/squalane",
        related_ingredients=["Squalene"]
    ),
    "PANTHENOL": CIRConclusion(
        ingredient_name="Panthenol",
        inci_name="PANTHENOL",
        conclusion=SafetyConclusion.SAFE_AS_USED,
        conclusion_text="Safe as used in cosmetics",
        report_type=ReportType.FINAL_REPORT,
        assessment_date="2018",
        journal_reference="Int J Toxicol. 2018;37(2_suppl):16S-37S",
        pdf_url="https://www.cir-safety.org/ingredients/panthenol",
        group_name="Panthenol and Related Ingredients",
        related_ingredients=["Calcium Pantothenate", "Pantothenic Acid"]
    ),
    "ALLANTOIN": CIRConclusion(
        ingredient_name="Allantoin",
        inci_name="ALLANTOIN",
        conclusion=SafetyConclusion.SAFE_AS_USED,
        conclusion_text="Safe as used in cosmetics",
        report_type=ReportType.FINAL_REPORT,
        assessment_date="2021",
        journal_reference="Int J Toxicol. 2010;29(3_suppl):84S-97S",
        pdf_url="https://www.cir-safety.org/ingredients/allantoin"
    ),
    "BUTYLENE GLYCOL": CIRConclusion(
        ingredient_name="Butylene Glycol",
        inci_name="BUTYLENE GLYCOL",
        conclusion=SafetyConclusion.SAFE_AS_USED,
        conclusion_text="Safe as used in cosmetics",
        report_type=ReportType.FINAL_REPORT,
        assessment_date="2019",
        journal_reference="Int J Toxicol. 1985;4(5):223-48",
        pdf_url="https://www.cir-safety.org/ingredients/butylene-glycol"
    ),

    # Safe with Qualifications - 기능성 성분
    "RETINOL": CIRConclusion(
        ingredient_name="Retinol",
        inci_name="RETINOL",
        conclusion=SafetyConclusion.SAFE_WITH_QUALIFICATIONS,
        conclusion_text="Safe as used when formulated to avoid skin irritation and when limited concentrations are used",
        report_type=ReportType.RE_REVIEW,
        assessment_date="2021",
        journal_reference="Int J Toxicol. 2017;36(5_suppl1):5S-88S",
        pdf_url="https://www.cir-safety.org/ingredients/retinol",
        max_concentration={
            "leave-on_face_hand": 0.5,
            "leave-on_body": 0.05,
            "rinse-off": 0.05
        },
        qualifications=[
            "Should be formulated to minimize irritation",
            "Sun protection recommended with use",
            "Caution advised during pregnancy"
        ],
        group_name="Vitamin A",
        related_ingredients=["Retinyl Palmitate", "Retinyl Acetate", "Retinal"]
    ),
    "RETINYL PALMITATE": CIRConclusion(
        ingredient_name="Retinyl Palmitate",
        inci_name="RETINYL PALMITATE",
        conclusion=SafetyConclusion.SAFE_WITH_QUALIFICATIONS,
        conclusion_text="Safe as used when formulated to avoid irritation",
        report_type=ReportType.RE_REVIEW,
        assessment_date="2021",
        journal_reference="Int J Toxicol. 2017;36(5_suppl1):5S-88S",
        pdf_url="https://www.cir-safety.org/ingredients/retinyl-palmitate",
        max_concentration={
            "leave-on": 0.5,
            "rinse-off": 0.1
        },
        qualifications=[
            "More stable than retinol",
            "Lower irritation potential"
        ],
        group_name="Vitamin A"
    ),
    "SALICYLIC ACID": CIRConclusion(
        ingredient_name="Salicylic Acid",
        inci_name="SALICYLIC ACID",
        conclusion=SafetyConclusion.SAFE_WITH_QUALIFICATIONS,
        conclusion_text="Safe when formulated to avoid irritation, up to 3% in rinse-off and 2% in leave-on",
        report_type=ReportType.RE_REVIEW,
        assessment_date="2018",
        journal_reference="Int J Toxicol. 2018;37(1_suppl):5S-40S",
        pdf_url="https://www.cir-safety.org/ingredients/salicylic-acid",
        max_concentration={
            "leave-on": 2.0,
            "rinse-off": 3.0
        },
        qualifications=[
            "Not for use on children under 3 years",
            "pH should be at or above 3.5"
        ],
        restricted_uses=["Not recommended for lip products at high concentrations"]
    ),
    "GLYCOLIC ACID": CIRConclusion(
        ingredient_name="Glycolic Acid",
        inci_name="GLYCOLIC ACID",
        conclusion=SafetyConclusion.SAFE_WITH_QUALIFICATIONS,
        conclusion_text="Safe when formulated at appropriate pH and concentration",
        report_type=ReportType.FINAL_REPORT,
        assessment_date="1998",
        journal_reference="Int J Toxicol. 1998;17(1):1-241",
        pdf_url="https://www.cir-safety.org/ingredients/glycolic-acid",
        max_concentration={
            "leave-on": 10.0,
            "salon_professional": 30.0
        },
        qualifications=[
            "Final product pH should be 3.5 or greater",
            "Sun protection strongly recommended"
        ],
        group_name="Alpha Hydroxy Acids",
        related_ingredients=["Lactic Acid", "Malic Acid", "Citric Acid"],
        next_review_date="2024-2025"
    ),
    "LACTIC ACID": CIRConclusion(
        ingredient_name="Lactic Acid",
        inci_name="LACTIC ACID",
        conclusion=SafetyConclusion.SAFE_WITH_QUALIFICATIONS,
        conclusion_text="Safe when formulated at appropriate pH and concentration",
        report_type=ReportType.FINAL_REPORT,
        assessment_date="1998",
        journal_reference="Int J Toxicol. 1998;17(1):1-241",
        pdf_url="https://www.cir-safety.org/ingredients/lactic-acid",
        max_concentration={
            "leave-on": 10.0,
            "salon_professional": 30.0
        },
        qualifications=[
            "Final product pH should be 3.5 or greater"
        ],
        group_name="Alpha Hydroxy Acids"
    ),
    "TITANIUM DIOXIDE": CIRConclusion(
        ingredient_name="Titanium Dioxide",
        inci_name="TITANIUM DIOXIDE",
        conclusion=SafetyConclusion.SAFE_WITH_QUALIFICATIONS,
        conclusion_text="Safe as used in cosmetics when formulated to be non-irritating and when nanoparticles are coated",
        report_type=ReportType.AMENDED_REPORT,
        assessment_date="2016",
        journal_reference="Int J Toxicol. 2016;35(2_suppl):5S-42S",
        pdf_url="https://www.cir-safety.org/ingredients/titanium-dioxide",
        qualifications=[
            "Nano form should be coated to prevent photocatalytic activity",
            "Not to be used in applications where inhalation exposure is likely"
        ],
        restricted_uses=["Inhalation exposure should be avoided"]
    ),
    "ZINC OXIDE": CIRConclusion(
        ingredient_name="Zinc Oxide",
        inci_name="ZINC OXIDE",
        conclusion=SafetyConclusion.SAFE_WITH_QUALIFICATIONS,
        conclusion_text="Safe as used when formulated to be non-irritating",
        report_type=ReportType.AMENDED_REPORT,
        assessment_date="2017",
        journal_reference="Int J Toxicol. 2017;36(5_suppl3):5S-16S",
        pdf_url="https://www.cir-safety.org/ingredients/zinc-oxide",
        qualifications=[
            "Not to be used on damaged skin",
            "Inhalation exposure should be avoided"
        ]
    ),

    # Parabens Group
    "METHYLPARABEN": CIRConclusion(
        ingredient_name="Methylparaben",
        inci_name="METHYLPARABEN",
        conclusion=SafetyConclusion.SAFE_AS_USED,
        conclusion_text="Safe as used in cosmetics",
        report_type=ReportType.RE_REVIEW,
        assessment_date="2019",
        journal_reference="Int J Toxicol. 2019;38(2_suppl):5S-27S",
        pdf_url="https://www.cir-safety.org/ingredients/parabens",
        group_name="Parabens",
        related_ingredients=[
            "Ethylparaben", "Propylparaben", "Butylparaben",
            "Isobutylparaben", "Isopropylparaben"
        ],
        notes="2019 re-review confirmed safety, including combination use"
    ),
    "PROPYLPARABEN": CIRConclusion(
        ingredient_name="Propylparaben",
        inci_name="PROPYLPARABEN",
        conclusion=SafetyConclusion.SAFE_AS_USED,
        conclusion_text="Safe as used in cosmetics",
        report_type=ReportType.RE_REVIEW,
        assessment_date="2019",
        journal_reference="Int J Toxicol. 2019;38(2_suppl):5S-27S",
        pdf_url="https://www.cir-safety.org/ingredients/parabens",
        group_name="Parabens"
    ),

    # Preservatives
    "PHENOXYETHANOL": CIRConclusion(
        ingredient_name="Phenoxyethanol",
        inci_name="PHENOXYETHANOL",
        conclusion=SafetyConclusion.SAFE_AS_USED,
        conclusion_text="Safe as used in cosmetics",
        report_type=ReportType.FINAL_REPORT,
        assessment_date="2020",
        journal_reference="Int J Toxicol. 1990;9(3):259-77",
        pdf_url="https://www.cir-safety.org/ingredients/phenoxyethanol",
        notes="Common paraben alternative"
    ),

    # Silicones
    "DIMETHICONE": CIRConclusion(
        ingredient_name="Dimethicone",
        inci_name="DIMETHICONE",
        conclusion=SafetyConclusion.SAFE_AS_USED,
        conclusion_text="Safe as used in cosmetics",
        report_type=ReportType.FINAL_REPORT,
        assessment_date="2019",
        journal_reference="Int J Toxicol. 2019;38(2_suppl):8S-49S",
        pdf_url="https://www.cir-safety.org/ingredients/dimethicone",
        group_name="Dimethicone and Related Silicones",
        related_ingredients=["Cyclomethicone", "Cyclopentasiloxane", "Dimethiconol"]
    ),
    "CYCLOPENTASILOXANE": CIRConclusion(
        ingredient_name="Cyclopentasiloxane",
        inci_name="CYCLOPENTASILOXANE",
        conclusion=SafetyConclusion.SAFE_AS_USED,
        conclusion_text="Safe as used in cosmetics",
        report_type=ReportType.FINAL_REPORT,
        assessment_date="2019",
        journal_reference="Int J Toxicol. 2019;38(2_suppl):8S-49S",
        pdf_url="https://www.cir-safety.org/ingredients/cyclopentasiloxane",
        group_name="Cyclomethicone",
        notes="D5, Environmental concerns separate from safety"
    ),

    # Surfactants
    "SODIUM LAURYL SULFATE": CIRConclusion(
        ingredient_name="Sodium Lauryl Sulfate",
        inci_name="SODIUM LAURYL SULFATE",
        conclusion=SafetyConclusion.SAFE_AS_USED,
        conclusion_text="Safe as used in cosmetics when formulated to be non-irritating",
        report_type=ReportType.RE_REVIEW,
        assessment_date="2019",
        journal_reference="Int J Toxicol. 2019;38(1_suppl):5S-42S",
        pdf_url="https://www.cir-safety.org/ingredients/sodium-lauryl-sulfate",
        qualifications=["Should be formulated to minimize irritation potential"],
        related_ingredients=["Sodium Laureth Sulfate", "Ammonium Lauryl Sulfate"]
    ),

    # Insufficient Data Examples
    "BAKUCHIOL": CIRConclusion(
        ingredient_name="Bakuchiol",
        inci_name="BAKUCHIOL",
        conclusion=SafetyConclusion.INSUFFICIENT_DATA,
        conclusion_text="Data insufficient to support safety - reproductive/developmental toxicity data needed",
        report_type=ReportType.DRAFT_REPORT,
        assessment_date="2023",
        pdf_url="https://www.cir-safety.org/ingredients/bakuchiol",
        qualifications=[
            "Need: Reproductive and developmental toxicity data",
            "Need: Additional dermal absorption data"
        ],
        notes="Retinol alternative, increasing use requires more data"
    ),
    "CANNABIDIOL": CIRConclusion(
        ingredient_name="Cannabidiol",
        inci_name="CANNABIDIOL",
        conclusion=SafetyConclusion.INSUFFICIENT_DATA,
        conclusion_text="Data insufficient to support safety",
        report_type=ReportType.DRAFT_REPORT,
        assessment_date="2024",
        pdf_url="https://www.cir-safety.org/ingredients/cannabidiol",
        qualifications=[
            "Need: Comprehensive toxicological data",
            "Need: Dermal penetration data",
            "Need: Impurity profile"
        ],
        notes="CBD - regulatory uncertainty affects data availability"
    ),

    # UV Filters
    "AVOBENZONE": CIRConclusion(
        ingredient_name="Avobenzone",
        inci_name="BUTYL METHOXYDIBENZOYLMETHANE",
        conclusion=SafetyConclusion.SAFE_AS_USED,
        conclusion_text="Safe as used in cosmetics",
        report_type=ReportType.FINAL_REPORT,
        assessment_date="2010",
        journal_reference="Int J Toxicol. 2010;29(4_suppl):165S-206S",
        pdf_url="https://www.cir-safety.org/ingredients/avobenzone",
        group_name="Benzophenone Sunscreens",
        notes="Most effective UVA1 filter"
    ),
    "OCTOCRYLENE": CIRConclusion(
        ingredient_name="Octocrylene",
        inci_name="OCTOCRYLENE",
        conclusion=SafetyConclusion.SAFE_AS_USED,
        conclusion_text="Safe as used in cosmetics",
        report_type=ReportType.FINAL_REPORT,
        assessment_date="2010",
        journal_reference="Int J Toxicol. 2010;29(4_suppl):165S-206S",
        pdf_url="https://www.cir-safety.org/ingredients/octocrylene",
        notes="Also acts as photostabilizer"
    ),
}

# Ingredient Group Database
INGREDIENT_GROUPS: Dict[str, IngredientGroup] = {
    "PARABENS": IngredientGroup(
        group_name="Parabens",
        ingredients=[
            "Methylparaben", "Ethylparaben", "Propylparaben", "Butylparaben",
            "Isobutylparaben", "Isopropylparaben", "Benzylparaben"
        ],
        conclusion=SafetyConclusion.SAFE_AS_USED,
        assessment_date="2019",
        report_reference="Int J Toxicol. 2019;38(2_suppl):5S-27S"
    ),
    "VITAMIN A": IngredientGroup(
        group_name="Vitamin A (Retinoids)",
        ingredients=[
            "Retinol", "Retinyl Palmitate", "Retinyl Acetate", "Retinal",
            "Retinyl Propionate", "Retinyl Linoleate"
        ],
        conclusion=SafetyConclusion.SAFE_WITH_QUALIFICATIONS,
        assessment_date="2021",
        report_reference="Int J Toxicol. 2017;36(5_suppl1):5S-88S"
    ),
    "ALPHA HYDROXY ACIDS": IngredientGroup(
        group_name="Alpha Hydroxy Acids (AHAs)",
        ingredients=[
            "Glycolic Acid", "Lactic Acid", "Malic Acid", "Tartaric Acid",
            "Citric Acid", "Mandelic Acid"
        ],
        conclusion=SafetyConclusion.SAFE_WITH_QUALIFICATIONS,
        assessment_date="1998",
        report_reference="Int J Toxicol. 1998;17(1):1-241"
    ),
    "DIMETHICONE": IngredientGroup(
        group_name="Dimethicone and Related Silicones",
        ingredients=[
            "Dimethicone", "Cyclomethicone", "Cyclopentasiloxane",
            "Cyclohexasiloxane", "Dimethiconol", "Phenyl Trimethicone"
        ],
        conclusion=SafetyConclusion.SAFE_AS_USED,
        assessment_date="2019",
        report_reference="Int J Toxicol. 2019;38(2_suppl):8S-49S"
    ),
    "TOCOPHEROL": IngredientGroup(
        group_name="Vitamin E",
        ingredients=[
            "Tocopherol", "Tocopheryl Acetate", "Tocopheryl Linoleate",
            "Tocopheryl Nicotinate", "Tocopheryl Succinate"
        ],
        conclusion=SafetyConclusion.SAFE_AS_USED,
        assessment_date="2018",
        report_reference="Int J Toxicol. 2018;37(2_suppl):61S-94S"
    ),
}


# ============================================================
# CIR Client Class
# ============================================================

class CIRClient:
    """CIR 안전성 평가 데이터베이스 클라이언트"""

    def __init__(self):
        self.database = CIR_DATABASE
        self.groups = INGREDIENT_GROUPS

    def search_ingredient(self, name: str) -> Optional[CIRConclusion]:
        """
        성분명으로 CIR 안전성 결론 검색

        Args:
            name: 성분명 (INCI명 또는 일반명)

        Returns:
            CIRConclusion 또는 None
        """
        name_upper = name.upper().strip()

        # 직접 매칭
        if name_upper in self.database:
            return self.database[name_upper]

        # INCI명 매칭
        for key, data in self.database.items():
            if name_upper == data.inci_name.upper():
                return data
            if name_upper in data.ingredient_name.upper():
                return data

        # 부분 매칭
        for key, data in self.database.items():
            if name_upper in key or name_upper in data.ingredient_name.upper():
                return data

        return None

    def search_all(self, query: str) -> List[CIRConclusion]:
        """
        검색어로 모든 관련 성분 검색

        Args:
            query: 검색어

        Returns:
            CIRConclusion 리스트
        """
        query_upper = query.upper().strip()
        results = []

        for key, data in self.database.items():
            if (query_upper in key or
                query_upper in data.ingredient_name.upper() or
                query_upper in data.inci_name.upper() or
                (data.group_name and query_upper in data.group_name.upper())):
                results.append(data)

        return results

    def get_report_pdf(self, ingredient: str) -> Optional[str]:
        """
        성분의 CIR 보고서 PDF URL 조회

        Args:
            ingredient: 성분명

        Returns:
            PDF URL 또는 None
        """
        result = self.search_ingredient(ingredient)
        if result:
            return result.pdf_url
        return None

    def list_recent_assessments(self, year: int = None) -> List[CIRConclusion]:
        """
        최근 평가 목록 조회

        Args:
            year: 특정 연도 (None이면 최근 5년)

        Returns:
            CIRConclusion 리스트
        """
        results = []
        current_year = datetime.now().year

        for key, data in self.database.items():
            try:
                assessment_year = int(data.assessment_date[:4])
                if year:
                    if assessment_year == year:
                        results.append(data)
                else:
                    if current_year - assessment_year <= 5:
                        results.append(data)
            except (ValueError, TypeError):
                continue

        # 날짜순 정렬 (최신순)
        results.sort(key=lambda x: x.assessment_date, reverse=True)
        return results

    def get_ingredient_group(self, ingredient_or_group: str) -> Optional[IngredientGroup]:
        """
        성분 그룹 정보 조회

        Args:
            ingredient_or_group: 성분명 또는 그룹명

        Returns:
            IngredientGroup 또는 None
        """
        query = ingredient_or_group.upper().strip()

        # 그룹명으로 검색
        if query in self.groups:
            return self.groups[query]

        # 성분이 속한 그룹 검색
        for group_key, group in self.groups.items():
            if query in [ing.upper() for ing in group.ingredients]:
                return group

        # 부분 매칭
        for group_key, group in self.groups.items():
            if query in group_key or query in group.group_name.upper():
                return group

        return None

    def get_assessment_status(self, ingredient: str) -> Optional[AssessmentInfo]:
        """
        성분의 평가 현황 조회

        Args:
            ingredient: 성분명

        Returns:
            AssessmentInfo 또는 None
        """
        result = self.search_ingredient(ingredient)
        if not result:
            return None

        return AssessmentInfo(
            ingredient=result.ingredient_name,
            status=AssessmentStatus.COMPLETED if result.conclusion != SafetyConclusion.UNDER_REVIEW
                   else AssessmentStatus.IN_PROGRESS,
            latest_review_date=result.assessment_date,
            next_review_due=result.next_review_date,
            current_conclusion=result.conclusion
        )

    def get_use_conditions(self, ingredient: str) -> Optional[Dict]:
        """
        조건부 안전 성분의 사용 조건 조회

        Args:
            ingredient: 성분명

        Returns:
            사용 조건 딕셔너리 또는 None
        """
        result = self.search_ingredient(ingredient)
        if not result:
            return None

        if result.conclusion != SafetyConclusion.SAFE_WITH_QUALIFICATIONS:
            return {"message": "No specific conditions - Safe as used"}

        return {
            "ingredient": result.ingredient_name,
            "max_concentration": result.max_concentration,
            "qualifications": result.qualifications,
            "restricted_uses": result.restricted_uses
        }

    def check_formulation_safety(
        self,
        ingredients: List[Dict[str, Union[str, float]]]
    ) -> Dict:
        """
        처방의 CIR 기반 안전성 검토

        Args:
            ingredients: [{"name": "Retinol", "concentration": 0.3}, ...]

        Returns:
            안전성 검토 결과
        """
        results = {
            "overall_status": "PASS",
            "ingredients_checked": 0,
            "safe_ingredients": [],
            "qualified_ingredients": [],
            "insufficient_data": [],
            "not_found": [],
            "issues": [],
            "recommendations": []
        }

        for item in ingredients:
            name = item.get("name", "")
            concentration = item.get("concentration", 0)

            cir_data = self.search_ingredient(name)
            results["ingredients_checked"] += 1

            if not cir_data:
                results["not_found"].append(name)
                results["recommendations"].append(
                    f"{name}: Not found in CIR database - independent safety assessment recommended"
                )
                continue

            if cir_data.conclusion == SafetyConclusion.SAFE_AS_USED:
                results["safe_ingredients"].append(name)

            elif cir_data.conclusion == SafetyConclusion.SAFE_WITH_QUALIFICATIONS:
                results["qualified_ingredients"].append(name)

                # 농도 확인
                if cir_data.max_concentration:
                    for use_type, max_conc in cir_data.max_concentration.items():
                        if concentration > max_conc:
                            results["issues"].append(
                                f"{name}: Concentration {concentration}% exceeds CIR max "
                                f"({max_conc}% for {use_type})"
                            )
                            results["overall_status"] = "REVIEW_REQUIRED"

                # 자격 조건 추가
                if cir_data.qualifications:
                    results["recommendations"].extend([
                        f"{name}: {qual}" for qual in cir_data.qualifications
                    ])

            elif cir_data.conclusion == SafetyConclusion.INSUFFICIENT_DATA:
                results["insufficient_data"].append(name)
                results["overall_status"] = "REVIEW_REQUIRED"
                results["issues"].append(
                    f"{name}: CIR concluded insufficient data - additional safety data needed"
                )

            elif cir_data.conclusion == SafetyConclusion.UNSAFE:
                results["overall_status"] = "FAIL"
                results["issues"].append(
                    f"{name}: CIR concluded UNSAFE - should not be used"
                )

        return results

    def get_all_by_conclusion(self, conclusion: SafetyConclusion) -> List[CIRConclusion]:
        """
        특정 결론 유형의 모든 성분 조회

        Args:
            conclusion: SafetyConclusion enum

        Returns:
            CIRConclusion 리스트
        """
        return [
            data for data in self.database.values()
            if data.conclusion == conclusion
        ]


# ============================================================
# CLI Interface
# ============================================================

def main():
    """CLI 메인 함수"""
    import sys

    client = CIRClient()

    if len(sys.argv) < 2:
        print("CIR Safety Database Query Tool")
        print("\nUsage: python cir_search.py <command> [args]")
        print("\nCommands:")
        print("  search <name>      - Search ingredient safety conclusion")
        print("  report <name>      - Get report PDF URL")
        print("  group <name>       - Get ingredient group info")
        print("  recent [year]      - List recent assessments")
        print("  conditions <name>  - Get use conditions for qualified ingredients")
        print("  safe               - List all 'Safe as used' ingredients")
        print("  qualified          - List all 'Safe with qualifications' ingredients")
        print("  insufficient       - List all 'Insufficient data' ingredients")
        return

    command = sys.argv[1].lower()

    if command == "search" and len(sys.argv) >= 3:
        name = " ".join(sys.argv[2:])
        result = client.search_ingredient(name)
        if result:
            print(f"\n=== {result.ingredient_name} ===")
            print(f"INCI: {result.inci_name}")
            print(f"Conclusion: {result.conclusion.value}")
            print(f"Details: {result.conclusion_text}")
            print(f"Report Type: {result.report_type.value}")
            print(f"Assessment Date: {result.assessment_date}")
            if result.journal_reference:
                print(f"Reference: {result.journal_reference}")
            if result.max_concentration:
                print(f"Max Concentration: {result.max_concentration}")
            if result.qualifications:
                print(f"Qualifications: {result.qualifications}")
            if result.pdf_url:
                print(f"PDF URL: {result.pdf_url}")
        else:
            print(f"Not found: {name}")

    elif command == "report" and len(sys.argv) >= 3:
        name = " ".join(sys.argv[2:])
        url = client.get_report_pdf(name)
        if url:
            print(f"Report URL: {url}")
        else:
            print(f"Report not found for: {name}")

    elif command == "group" and len(sys.argv) >= 3:
        name = " ".join(sys.argv[2:])
        group = client.get_ingredient_group(name)
        if group:
            print(f"\n=== {group.group_name} ===")
            print(f"Conclusion: {group.conclusion.value}")
            print(f"Assessment Date: {group.assessment_date}")
            print(f"Ingredients ({len(group.ingredients)}):")
            for ing in group.ingredients:
                print(f"  - {ing}")
        else:
            print(f"Group not found: {name}")

    elif command == "recent":
        year = int(sys.argv[2]) if len(sys.argv) >= 3 else None
        results = client.list_recent_assessments(year)
        print(f"\nRecent Assessments{f' ({year})' if year else ' (last 5 years)'}:")
        for result in results:
            print(f"  {result.assessment_date}: {result.ingredient_name} - {result.conclusion.value}")

    elif command == "conditions" and len(sys.argv) >= 3:
        name = " ".join(sys.argv[2:])
        conditions = client.get_use_conditions(name)
        if conditions:
            print(f"\nUse Conditions for {name}:")
            print(json.dumps(conditions, indent=2, ensure_ascii=False))
        else:
            print(f"Not found: {name}")

    elif command == "safe":
        results = client.get_all_by_conclusion(SafetyConclusion.SAFE_AS_USED)
        print(f"\n'Safe as Used' Ingredients ({len(results)}):")
        for result in results:
            print(f"  - {result.ingredient_name}")

    elif command == "qualified":
        results = client.get_all_by_conclusion(SafetyConclusion.SAFE_WITH_QUALIFICATIONS)
        print(f"\n'Safe with Qualifications' Ingredients ({len(results)}):")
        for result in results:
            print(f"  - {result.ingredient_name}: {result.max_concentration or 'See report'}")

    elif command == "insufficient":
        results = client.get_all_by_conclusion(SafetyConclusion.INSUFFICIENT_DATA)
        print(f"\n'Insufficient Data' Ingredients ({len(results)}):")
        for result in results:
            print(f"  - {result.ingredient_name}: {result.notes or 'Data needed'}")

    else:
        print(f"Unknown command or missing arguments: {command}")


if __name__ == "__main__":
    main()
