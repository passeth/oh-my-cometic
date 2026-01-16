#!/usr/bin/env python3
"""
Ingredient Deep-Dive Generator

Hero 성분에 대한 K-Dense 수준의 심층 분석 리포트 생성기

Usage:
    from ingredient_deep_dive import DeepDiveGenerator

    generator = DeepDiveGenerator()

    # 전체 리포트 생성
    report = generator.generate_full_report(
        ingredient_name="Niacinamide",
        inci_name="NIACINAMIDE",
        concentration="5%"
    )

    print(report.to_markdown())
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Tuple
from enum import Enum
from datetime import datetime
import json
import re


# ============================================================
# Enums and Constants
# ============================================================

class EvidenceGrade(Enum):
    """근거 수준 등급"""
    A = "A - Strong Evidence"
    B = "B - Moderate Evidence"
    C = "C - Limited Evidence"
    D = "D - Preliminary Evidence"
    E = "E - Insufficient Evidence"


class AnalysisDepth(Enum):
    """분석 깊이"""
    BRIEF = "brief"          # 1페이지
    STANDARD = "standard"    # 2페이지
    COMPREHENSIVE = "comprehensive"  # 3+ 페이지


class IngredientCategory(Enum):
    """성분 카테고리"""
    VITAMIN = "vitamin"
    PEPTIDE = "peptide"
    BOTANICAL = "botanical"
    HUMECTANT = "humectant"
    ACTIVE = "active"
    FERMENT = "ferment"
    ANTIOXIDANT = "antioxidant"
    OTHER = "other"


# ============================================================
# Data Classes
# ============================================================

@dataclass
class MolecularProfile:
    """분자 프로필"""
    inci_name: str
    cas_number: str = ""
    molecular_weight: str = ""
    molecular_formula: str = ""
    solubility: str = ""
    log_p: str = ""
    optimal_ph: str = ""
    stability: str = ""
    appearance: str = ""
    origin: str = ""


@dataclass
class MechanismPathway:
    """메커니즘 경로"""
    pathway_name: str
    description: str
    steps: List[str]
    target_molecules: List[str]
    cellular_effects: List[str]
    skin_effects: List[str]
    mermaid_diagram: str = ""


@dataclass
class ClinicalStudy:
    """임상 연구 데이터"""
    reference: str
    study_type: str
    sample_size: int
    duration: str
    key_finding: str
    concentration: str
    pmid: str = ""


@dataclass
class FormulationGuide:
    """처방 가이드"""
    optimal_concentration: str
    max_concentration: str
    ph_range: str
    compatible_ingredients: List[str]
    incompatible_ingredients: List[str]
    delivery_systems: List[str]
    stability_tips: List[str]


@dataclass
class SynergyInfo:
    """시너지 정보"""
    partner_ingredient: str
    synergy_type: str
    mechanism: str
    recommended_ratio: str
    evidence_level: str


@dataclass
class SafetyProfile:
    """안전성 프로필"""
    ewg_score: str
    cir_conclusion: str
    irritation_potential: str
    sensitization_risk: str
    photosensitivity: str
    pregnancy_safety: str
    precautions: List[str]


@dataclass
class DeepDiveReport:
    """Deep-Dive 전체 리포트"""
    ingredient_name: str
    inci_name: str
    category: IngredientCategory
    concentration: str
    product_context: str

    # 섹션 데이터
    scientific_background: str = ""
    molecular_profile: Optional[MolecularProfile] = None
    primary_mechanism: Optional[MechanismPathway] = None
    secondary_mechanisms: List[MechanismPathway] = field(default_factory=list)
    clinical_evidence: List[ClinicalStudy] = field(default_factory=list)
    evidence_grade: EvidenceGrade = EvidenceGrade.C
    formulation_guide: Optional[FormulationGuide] = None
    synergies: List[SynergyInfo] = field(default_factory=list)
    safety_profile: Optional[SafetyProfile] = None
    references: List[str] = field(default_factory=list)

    # 메타데이터
    generated_at: str = ""
    language: str = "ko"
    estimated_pages: float = 3.0

    def to_markdown(self) -> str:
        """마크다운 형식으로 변환"""
        sections = []

        # 헤더
        sections.append(f"## {self.ingredient_name} Deep-Dive Analysis\n")

        # 1. Scientific Background
        if self.scientific_background:
            sections.append("### 1. Scientific Background\n")
            sections.append(self.scientific_background + "\n")

        # 2. Molecular Profile
        if self.molecular_profile:
            sections.append("### 2. Molecular Profile\n")
            sections.append(self._format_molecular_profile())

        # 3. Mechanism of Action
        sections.append("### 3. Mechanism of Action\n")
        if self.primary_mechanism:
            sections.append("#### 3.1 Primary Pathway\n")
            sections.append(f"**{self.primary_mechanism.pathway_name}**\n")
            sections.append(f"{self.primary_mechanism.description}\n")

            if self.primary_mechanism.mermaid_diagram:
                sections.append("\n```mermaid")
                sections.append(self.primary_mechanism.mermaid_diagram)
                sections.append("```\n")

            sections.append("\n**Cellular Effects:**\n")
            for effect in self.primary_mechanism.cellular_effects:
                sections.append(f"- {effect}\n")

            sections.append("\n**Skin Effects:**\n")
            for effect in self.primary_mechanism.skin_effects:
                sections.append(f"- {effect}\n")

        if self.secondary_mechanisms:
            sections.append("\n#### 3.2 Secondary Pathways\n")
            for mech in self.secondary_mechanisms:
                sections.append(f"\n**{mech.pathway_name}**\n")
                sections.append(f"{mech.description}\n")

        # 4. Clinical Evidence
        sections.append("\n### 4. Clinical Evidence Summary\n")
        sections.append(self._format_evidence_table())
        sections.append(f"\n**Evidence Grade: {self.evidence_grade.value}**\n")

        # 5. Formulation Considerations
        if self.formulation_guide:
            sections.append("\n### 5. Formulation Considerations\n")
            sections.append(self._format_formulation_guide())

        # 6. Synergy Analysis
        if self.synergies:
            sections.append("\n### 6. Synergy Analysis\n")
            sections.append(self._format_synergy_analysis())

        # 7. Safety Profile
        if self.safety_profile:
            sections.append("\n### 7. Safety Profile\n")
            sections.append(self._format_safety_profile())

        # 8. References
        if self.references:
            sections.append("\n### 8. References\n")
            for i, ref in enumerate(self.references, 1):
                sections.append(f"{i}. {ref}\n")

        return "\n".join(sections)

    def _format_molecular_profile(self) -> str:
        """분자 프로필 테이블 포맷"""
        mp = self.molecular_profile
        rows = [
            "| Property | Value |",
            "|----------|-------|",
            f"| INCI Name | {mp.inci_name} |",
        ]
        if mp.cas_number:
            rows.append(f"| CAS Number | {mp.cas_number} |")
        if mp.molecular_weight:
            rows.append(f"| Molecular Weight | {mp.molecular_weight} |")
        if mp.molecular_formula:
            rows.append(f"| Molecular Formula | {mp.molecular_formula} |")
        if mp.solubility:
            rows.append(f"| Solubility | {mp.solubility} |")
        if mp.log_p:
            rows.append(f"| Log P | {mp.log_p} |")
        if mp.optimal_ph:
            rows.append(f"| Optimal pH | {mp.optimal_ph} |")
        if mp.stability:
            rows.append(f"| Stability | {mp.stability} |")
        if mp.origin:
            rows.append(f"| Origin | {mp.origin} |")

        return "\n".join(rows) + "\n"

    def _format_evidence_table(self) -> str:
        """임상 근거 테이블 포맷"""
        if not self.clinical_evidence:
            return "*임상 근거 데이터 수집 필요*\n"

        rows = [
            "| Study | Type | N | Duration | Key Finding | Conc. |",
            "|-------|------|---|----------|-------------|-------|"
        ]

        for study in self.clinical_evidence:
            rows.append(
                f"| {study.reference} | {study.study_type} | "
                f"{study.sample_size} | {study.duration} | "
                f"{study.key_finding[:40]}... | {study.concentration} |"
            )

        return "\n".join(rows) + "\n"

    def _format_formulation_guide(self) -> str:
        """처방 가이드 포맷"""
        fg = self.formulation_guide
        sections = []

        sections.append(f"**Optimal Concentration:** {fg.optimal_concentration}\n")
        sections.append(f"**Maximum Concentration:** {fg.max_concentration}\n")
        sections.append(f"**pH Range:** {fg.ph_range}\n")

        if fg.compatible_ingredients:
            sections.append("\n**Compatible Ingredients:**\n")
            for ing in fg.compatible_ingredients:
                sections.append(f"- {ing}\n")

        if fg.incompatible_ingredients:
            sections.append("\n**Incompatible Ingredients:**\n")
            for ing in fg.incompatible_ingredients:
                sections.append(f"- {ing}\n")

        if fg.delivery_systems:
            sections.append("\n**Recommended Delivery Systems:**\n")
            for ds in fg.delivery_systems:
                sections.append(f"- {ds}\n")

        if fg.stability_tips:
            sections.append("\n**Stability Tips:**\n")
            for tip in fg.stability_tips:
                sections.append(f"- {tip}\n")

        return "".join(sections)

    def _format_synergy_analysis(self) -> str:
        """시너지 분석 포맷"""
        rows = [
            "| Partner | Synergy Type | Mechanism | Ratio |",
            "|---------|--------------|-----------|-------|"
        ]

        for syn in self.synergies:
            rows.append(
                f"| {syn.partner_ingredient} | {syn.synergy_type} | "
                f"{syn.mechanism[:30]}... | {syn.recommended_ratio} |"
            )

        return "\n".join(rows) + "\n"

    def _format_safety_profile(self) -> str:
        """안전성 프로필 포맷"""
        sp = self.safety_profile
        sections = []

        sections.append(f"**EWG Score:** {sp.ewg_score}\n")
        sections.append(f"**CIR Conclusion:** {sp.cir_conclusion}\n")
        sections.append(f"**Irritation Potential:** {sp.irritation_potential}\n")
        sections.append(f"**Sensitization Risk:** {sp.sensitization_risk}\n")

        if sp.photosensitivity:
            sections.append(f"**Photosensitivity:** {sp.photosensitivity}\n")
        if sp.pregnancy_safety:
            sections.append(f"**Pregnancy Safety:** {sp.pregnancy_safety}\n")

        if sp.precautions:
            sections.append("\n**Precautions:**\n")
            for prec in sp.precautions:
                sections.append(f"- {prec}\n")

        return "".join(sections)

    def to_dict(self) -> dict:
        """딕셔너리 변환"""
        return {
            "ingredient_name": self.ingredient_name,
            "inci_name": self.inci_name,
            "category": self.category.value,
            "concentration": self.concentration,
            "product_context": self.product_context,
            "scientific_background": self.scientific_background,
            "evidence_grade": self.evidence_grade.value,
            "estimated_pages": self.estimated_pages,
            "generated_at": self.generated_at,
            "language": self.language
        }

    def to_json(self) -> str:
        """JSON 변환"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


# ============================================================
# Ingredient Knowledge Base
# ============================================================

INGREDIENT_DATABASE: Dict[str, Dict] = {
    "NIACINAMIDE": {
        "name": "Niacinamide",
        "inci": "NIACINAMIDE",
        "category": IngredientCategory.VITAMIN,
        "aliases": ["Nicotinamide", "Vitamin B3", "니아신아마이드"],
        "molecular_profile": MolecularProfile(
            inci_name="NIACINAMIDE",
            cas_number="98-92-0",
            molecular_weight="122.12 g/mol",
            molecular_formula="C6H6N2O",
            solubility="Water soluble (1000 g/L)",
            log_p="-0.37",
            optimal_ph="5.0-7.0",
            stability="Excellent (heat, light stable)",
            origin="Synthetic / Natural (B vitamin)"
        ),
        "primary_mechanism": MechanismPathway(
            pathway_name="NAD+ Biosynthesis Pathway",
            description="나이아신아마이드는 NAD+의 전구체로서 세포 에너지 대사와 DNA 복구에 핵심적인 역할을 합니다. "
                       "Sirtuin(SIRT1-7) 활성화를 통해 항노화 효과를 발휘합니다.",
            steps=[
                "Niacinamide enters cell via passive diffusion",
                "Converted to NMN by NAMPT enzyme",
                "NMN converted to NAD+ by NMNAT",
                "NAD+ activates Sirtuins (SIRT1-7)",
                "SIRT1 deacetylates FOXO, PGC-1α",
                "Enhanced mitochondrial function",
                "Improved cellular energy and repair"
            ],
            target_molecules=["NAMPT", "NAD+", "SIRT1", "FOXO3", "PGC-1α"],
            cellular_effects=[
                "NAD+ 세포 내 농도 증가",
                "Sirtuin 활성화 (SIRT1, SIRT3)",
                "미토콘드리아 기능 향상",
                "DNA 복구 촉진",
                "세포 스트레스 저항성 증가"
            ],
            skin_effects=[
                "피부 장벽 강화 (세라마이드 합성 증가)",
                "멜라닌 이동 억제 (미백)",
                "피지 분비 조절",
                "홍조 감소 (항염)",
                "주름 개선"
            ],
            mermaid_diagram="""
graph TD
    A[Niacinamide] --> B[NAMPT]
    B --> C[NMN]
    C --> D[NAD+]
    D --> E[Sirtuin Activation]
    E --> F[SIRT1]
    E --> G[SIRT3]
    F --> H[FOXO3 Deacetylation]
    F --> I[PGC-1α Activation]
    G --> J[Mitochondrial Function]
    H --> K[Antioxidant Genes]
    I --> L[Energy Metabolism]
    J --> M[ATP Production]
    K --> N[Skin Protection]
    L --> N
    M --> N
"""
        ),
        "secondary_mechanisms": [
            MechanismPathway(
                pathway_name="Melanin Transfer Inhibition",
                description="멜라노좀이 각질세포로 이동하는 것을 억제하여 미백 효과를 발휘합니다.",
                steps=["Inhibits melanosome transfer", "Reduces PAR-2 receptor activation"],
                target_molecules=["PAR-2", "Melanosome"],
                cellular_effects=["멜라노좀 이동 감소"],
                skin_effects=["피부 미백", "색소침착 감소"],
                mermaid_diagram=""
            ),
            MechanismPathway(
                pathway_name="Ceramide Synthesis Enhancement",
                description="세라마이드 합성을 촉진하여 피부 장벽을 강화합니다.",
                steps=["Upregulates ceramide synthase", "Increases ceramide production"],
                target_molecules=["Serine palmitoyltransferase", "Ceramide synthase"],
                cellular_effects=["세라마이드 합성 증가"],
                skin_effects=["피부 장벽 강화", "TEWL 감소"],
                mermaid_diagram=""
            )
        ],
        "clinical_evidence": [
            ClinicalStudy(
                reference="Bissett et al., 2005",
                study_type="RCT",
                sample_size=50,
                duration="12주",
                key_finding="5% 나이아신아마이드 주름 감소 및 탄력 개선",
                concentration="5%",
                pmid="15867531"
            ),
            ClinicalStudy(
                reference="Hakozaki et al., 2002",
                study_type="RCT",
                sample_size=18,
                duration="8주",
                key_finding="5% 농도에서 과색소침착 유의미 감소",
                concentration="5%",
                pmid="12100180"
            ),
            ClinicalStudy(
                reference="Draelos et al., 2006",
                study_type="Clinical Trial",
                sample_size=50,
                duration="12주",
                key_finding="2% 나이아신아마이드 피부장벽 기능 개선",
                concentration="2%",
                pmid="16766489"
            )
        ],
        "evidence_grade": EvidenceGrade.A,
        "formulation_guide": FormulationGuide(
            optimal_concentration="2-5%",
            max_concentration="10%",
            ph_range="5.0-7.0",
            compatible_ingredients=[
                "Hyaluronic Acid",
                "Peptides",
                "Ceramides",
                "Zinc PCA",
                "Alpha Arbutin"
            ],
            incompatible_ingredients=[
                "Pure Vitamin C (L-AA) at low pH - may convert to niacin causing flushing",
                "AHA/BHA at very low pH (pH < 3.5)"
            ],
            delivery_systems=[
                "Aqueous serum (optimal)",
                "Emulsion (O/W)",
                "Liposomal delivery"
            ],
            stability_tips=[
                "매우 안정적 - 특별한 안정화 불필요",
                "열, 빛, pH에 안정",
                "비타민 C와 함께 사용 시 pH 5.0 이상 유지",
                "2년 이상 안정성 확보 가능"
            ]
        ),
        "synergies": [
            SynergyInfo(
                partner_ingredient="Zinc PCA",
                synergy_type="피지 조절 시너지",
                mechanism="나이아신아마이드의 피지 조절 + 아연의 항균 효과 결합",
                recommended_ratio="4% Niacinamide + 1% Zinc PCA",
                evidence_level="B"
            ),
            SynergyInfo(
                partner_ingredient="Hyaluronic Acid",
                synergy_type="보습 시너지",
                mechanism="장벽 강화 + 수분 보유력 증가",
                recommended_ratio="5% Niacinamide + 1% HA",
                evidence_level="B"
            ),
            SynergyInfo(
                partner_ingredient="Alpha Arbutin",
                synergy_type="미백 시너지",
                mechanism="멜라닌 합성 억제 + 이동 억제 이중 작용",
                recommended_ratio="5% Niacinamide + 2% Alpha Arbutin",
                evidence_level="C"
            )
        ],
        "safety_profile": SafetyProfile(
            ewg_score="1 (Low Hazard)",
            cir_conclusion="Safe as used",
            irritation_potential="Very Low",
            sensitization_risk="Very Low",
            photosensitivity="None",
            pregnancy_safety="Generally considered safe",
            precautions=[
                "고농도(10% 이상) 사용 시 일부 민감 반응 가능",
                "순수 비타민 C(저 pH)와 동시 사용 시 홍조 유발 가능"
            ]
        ),
        "scientific_background": """
나이아신아마이드(Niacinamide, Nicotinamide)는 비타민 B3의 아마이드 형태로, 1937년 Conrad Elvehjem에 의해
펠라그라(pellagra) 치료제로 처음 발견되었습니다. 화장품 성분으로서의 활용은 1990년대 후반 P&G의
연구진이 피부에 대한 다양한 효능을 체계적으로 밝히면서 본격화되었습니다.

**발견 역사:**
- 1937년: 펠라그라 치료를 위한 필수 영양소로 확인
- 1990s: P&G에서 피부 장벽 및 미백 효능 연구 시작
- 2000s: 다수의 임상 연구로 효능 입증
- 2010s~: 글로벌 스킨케어 시장에서 핵심 성분으로 부상

**현재 시장 동향:**
나이아신아마이드는 현재 전 세계적으로 가장 많이 사용되는 기능성 화장품 성분 중 하나입니다.
The Ordinary의 "Niacinamide 10% + Zinc 1%"는 베스트셀러로 이 성분의 대중화에 기여했습니다.
K-beauty에서도 핵심 성분으로 광범위하게 사용됩니다.
"""
    },

    "RETINOL": {
        "name": "Retinol",
        "inci": "RETINOL",
        "category": IngredientCategory.VITAMIN,
        "aliases": ["Vitamin A", "레티놀", "비타민 A"],
        "molecular_profile": MolecularProfile(
            inci_name="RETINOL",
            cas_number="68-26-8",
            molecular_weight="286.45 g/mol",
            molecular_formula="C20H30O",
            solubility="Oil soluble",
            log_p="5.68",
            optimal_ph="5.5-6.5",
            stability="Unstable (light, air, heat sensitive)",
            origin="Synthetic / Animal derived"
        ),
        "primary_mechanism": MechanismPathway(
            pathway_name="Retinoic Acid Receptor (RAR) Pathway",
            description="레티놀은 피부 내에서 레티날, 레티노산으로 순차 전환되어 핵 수용체(RAR, RXR)에 결합, "
                       "유전자 발현을 조절하여 항노화 효과를 발휘합니다.",
            steps=[
                "Retinol penetrates stratum corneum",
                "Converted to retinal by alcohol dehydrogenase",
                "Converted to retinoic acid (RA) by aldehyde dehydrogenase",
                "RA binds to RAR/RXR nuclear receptors",
                "RAR/RXR complex binds to RARE (Retinoic Acid Response Elements)",
                "Modulates gene expression (collagen, MMPs, etc.)",
                "Increased cell turnover and collagen synthesis"
            ],
            target_molecules=["RAR-α/β/γ", "RXR", "RARE", "MMPs", "Procollagen"],
            cellular_effects=[
                "표피 세포 분화 정상화",
                "콜라겐 Type I, III 합성 증가",
                "MMP-1, MMP-3 발현 억제",
                "세포 회전율 증가",
                "GAG 합성 촉진"
            ],
            skin_effects=[
                "주름 감소",
                "피부 탄력 증가",
                "피부결 개선",
                "광노화 개선",
                "색소침착 감소"
            ],
            mermaid_diagram="""
graph TD
    A[Retinol] --> B[Retinal]
    B --> C[Retinoic Acid]
    C --> D[RAR/RXR Binding]
    D --> E[RARE Activation]
    E --> F[Collagen Synthesis ↑]
    E --> G[MMP Expression ↓]
    E --> H[Cell Turnover ↑]
    F --> I[Wrinkle Reduction]
    G --> I
    H --> J[Improved Texture]
    I --> K[Anti-Aging Effect]
    J --> K
"""
        ),
        "clinical_evidence": [
            ClinicalStudy(
                reference="Kafi et al., 2007",
                study_type="RCT",
                sample_size=36,
                duration="24주",
                key_finding="0.4% 레티놀 광노화 피부 주름 유의미 감소",
                concentration="0.4%",
                pmid="17515510"
            ),
            ClinicalStudy(
                reference="Randhawa et al., 2015",
                study_type="RCT",
                sample_size=44,
                duration="12주",
                key_finding="0.1% 레티놀 주름, 색소 침착 개선",
                concentration="0.1%",
                pmid="25607697"
            )
        ],
        "evidence_grade": EvidenceGrade.A,
        "formulation_guide": FormulationGuide(
            optimal_concentration="0.1-0.5%",
            max_concentration="1%",
            ph_range="5.5-6.5",
            compatible_ingredients=[
                "Vitamin E (안정화)",
                "Peptides",
                "Hyaluronic Acid",
                "Ceramides"
            ],
            incompatible_ingredients=[
                "Benzoyl Peroxide (산화)",
                "AHA/BHA (자극 증가)",
                "Vitamin C at low pH",
                "강한 산화제"
            ],
            delivery_systems=[
                "Encapsulation (필수)",
                "Liposomal delivery",
                "Retinol esters (더 안정적)"
            ],
            stability_tips=[
                "공기/빛 차단 필수 (airless pump, opaque packaging)",
                "항산화제(Vitamin E, BHT) 병용",
                "저온 보관 권장",
                "캡슐화 형태 사용 시 안정성 향상"
            ]
        ),
        "safety_profile": SafetyProfile(
            ewg_score="1-4 (농도 의존)",
            cir_conclusion="Safe with qualifications",
            irritation_potential="Moderate to High (농도 의존)",
            sensitization_risk="Low",
            photosensitivity="Increased (자외선 차단 필수)",
            pregnancy_safety="Avoid during pregnancy",
            precautions=[
                "점진적 농도 증가 권장 (retinization)",
                "자외선 차단제 필수 병용",
                "임신/수유 중 사용 자제",
                "초기 사용 시 건조함, 각질, 홍조 가능"
            ]
        ),
        "scientific_background": """
레티놀(Retinol)은 비타민 A의 알코올 형태로, 1913년 Elmer McCollum과 Marguerite Davis에 의해
처음 발견되었습니다. 피부과학에서의 활용은 1970년대 Kligman 박사가 트레티노인(레티노산)의
광노화 개선 효과를 발견하면서 시작되었습니다.

**발견 역사:**
- 1913년: 비타민 A 발견
- 1968년: Kligman, 트레티노인의 여드름 치료 효과 발견
- 1980s: 광노화 개선 효과 확인
- 1990s: 화장품용 레티놀 제형 개발
- 2000s~: 안정화 기술 발전으로 화장품 널리 사용

**현재 시장 동향:**
레티놀은 항노화 화장품의 "Gold Standard"로 불리며, 수많은 프리미엄 안티에이징 제품에
포함되어 있습니다. 최근에는 캡슐화 레티놀, 레티놀 대체제(Bakuchiol) 등
다양한 형태로 발전하고 있습니다.
"""
    },

    "ASCORBIC ACID": {
        "name": "Vitamin C (L-Ascorbic Acid)",
        "inci": "ASCORBIC ACID",
        "category": IngredientCategory.VITAMIN,
        "aliases": ["L-Ascorbic Acid", "Vitamin C", "비타민 C", "아스코빅애씨드"],
        "molecular_profile": MolecularProfile(
            inci_name="ASCORBIC ACID",
            cas_number="50-81-7",
            molecular_weight="176.12 g/mol",
            molecular_formula="C6H8O6",
            solubility="Water soluble (330 g/L)",
            log_p="-1.85",
            optimal_ph="2.5-3.5",
            stability="Unstable (oxidation, light, heat)",
            origin="Synthetic / Natural (citrus)"
        ),
        "primary_mechanism": MechanismPathway(
            pathway_name="Collagen Biosynthesis Cofactor",
            description="비타민 C는 콜라겐 합성에 필수적인 프롤린/라이신 수산화 효소의 조효소로 작용하며, "
                       "강력한 항산화 작용을 통해 피부를 보호합니다.",
            steps=[
                "L-Ascorbic acid penetrates skin",
                "Acts as cofactor for prolyl/lysyl hydroxylase",
                "Enables procollagen hydroxylation",
                "Proper collagen triple helix formation",
                "Neutralizes ROS directly",
                "Regenerates Vitamin E"
            ],
            target_molecules=["Prolyl hydroxylase", "Lysyl hydroxylase", "Procollagen", "ROS"],
            cellular_effects=[
                "콜라겐 합성 촉진",
                "ROS 중화",
                "비타민 E 재생",
                "티로시나아제 억제"
            ],
            skin_effects=[
                "피부 탄력 증가",
                "주름 감소",
                "미백 효과",
                "광손상 방지"
            ],
            mermaid_diagram="""
graph TD
    A[L-Ascorbic Acid] --> B[Prolyl Hydroxylase]
    A --> C[Lysyl Hydroxylase]
    B --> D[Procollagen Hydroxylation]
    C --> D
    D --> E[Stable Collagen Triple Helix]
    A --> F[ROS Neutralization]
    A --> G[Vitamin E Regeneration]
    A --> H[Tyrosinase Inhibition]
    E --> I[Skin Firmness]
    F --> J[Photoprotection]
    G --> J
    H --> K[Brightening]
"""
        ),
        "evidence_grade": EvidenceGrade.A,
        "formulation_guide": FormulationGuide(
            optimal_concentration="10-20%",
            max_concentration="20%",
            ph_range="2.5-3.5",
            compatible_ingredients=[
                "Vitamin E (시너지 + 안정화)",
                "Ferulic Acid (안정화 + 시너지)",
                "Hyaluronic Acid"
            ],
            incompatible_ingredients=[
                "Niacinamide at very low pH",
                "AHA/BHA (pH 경쟁)",
                "Copper peptides (산화 촉진)",
                "Retinol (pH 불일치)"
            ],
            delivery_systems=[
                "Anhydrous serum",
                "Vitamin C derivatives",
                "Liposomal delivery"
            ],
            stability_tips=[
                "pH 2.5-3.5 유지 필수",
                "비타민 E, 페룰산 병용 (CEF 시스템)",
                "공기/빛 차단 패키징",
                "냉장 보관 권장"
            ]
        ),
        "scientific_background": """
비타민 C(L-Ascorbic Acid)는 1928년 Albert Szent-Györgyi에 의해 발견되었으며,
이 공로로 1937년 노벨 생리의학상을 수상했습니다. 피부과학에서의 활용은
1980년대 Sheldon Pinnell 박사의 연구를 통해 본격화되었습니다.

**발견 역사:**
- 1747년: James Lind, 괴혈병과 감귤류의 관계 발견
- 1928년: Szent-Györgyi, 비타민 C 분리
- 1988년: Pinnell, 토피컬 비타민 C의 광보호 효과 발표
- 2005년: CEF(Vitamin C + E + Ferulic) 특허

**현재 시장 동향:**
비타민 C는 미백과 항산화의 대표 성분으로, SkinCeuticals C E Ferulic이 업계 기준이 되었습니다.
안정성 문제로 다양한 유도체(Ascorbyl Glucoside, 3-O-Ethyl Ascorbic Acid 등)가 개발되어 사용됩니다.
"""
    },

    "3-O-ETHYL ASCORBIC ACID": {
        "name": "3-O-Ethyl Ascorbic Acid",
        "inci": "3-O-ETHYL ASCORBIC ACID",
        "category": IngredientCategory.VITAMIN,
        "aliases": ["Ethyl Ascorbic Acid", "EAA", "에틸아스코빅애씨드", "안정화 비타민 C"],
        "molecular_profile": MolecularProfile(
            inci_name="3-O-ETHYL ASCORBIC ACID",
            cas_number="86404-04-8",
            molecular_weight="204.18 g/mol",
            molecular_formula="C8H12O6",
            solubility="Water soluble",
            log_p="-0.67",
            optimal_ph="4.0-6.0",
            stability="Excellent (L-AA 대비 86배 안정)",
            origin="Synthetic derivative"
        ),
        "primary_mechanism": MechanismPathway(
            pathway_name="Direct Cell Penetration + Conversion",
            description="3-O-Ethyl Ascorbic Acid는 에틸기가 3번 위치 수산기를 보호하여 산화를 방지합니다. "
                       "세포 내 흡수 후 에스터라아제에 의해 L-Ascorbic Acid로 전환되어 효능을 발휘합니다.",
            steps=[
                "3-O-Ethyl AA penetrates cell membrane",
                "Esterase cleaves ethyl group",
                "Releases active L-Ascorbic Acid intracellularly",
                "Same mechanisms as L-AA activate",
                "Collagen synthesis enhancement",
                "Melanin inhibition"
            ],
            target_molecules=["Esterase", "Prolyl hydroxylase", "Tyrosinase"],
            cellular_effects=[
                "세포 내 L-AA 농도 증가",
                "콜라겐 합성 촉진",
                "멜라닌 생성 억제",
                "항산화 작용"
            ],
            skin_effects=[
                "미백 효과 (L-AA와 동등)",
                "주름 개선",
                "피부 톤 균일화",
                "광손상 방지"
            ],
            mermaid_diagram="""
graph TD
    A[3-O-Ethyl Ascorbic Acid] --> B[Cell Penetration]
    B --> C[Intracellular Esterase]
    C --> D[L-Ascorbic Acid Release]
    D --> E[Collagen Synthesis]
    D --> F[Tyrosinase Inhibition]
    D --> G[ROS Neutralization]
    E --> H[Anti-Aging]
    F --> I[Brightening]
    G --> J[Photoprotection]
"""
        ),
        "evidence_grade": EvidenceGrade.B,
        "formulation_guide": FormulationGuide(
            optimal_concentration="5-15%",
            max_concentration="20%",
            ph_range="4.0-6.0",
            compatible_ingredients=[
                "Niacinamide",
                "Vitamin E",
                "Ferulic Acid",
                "Hyaluronic Acid",
                "Peptides"
            ],
            incompatible_ingredients=[
                "강한 환원제",
                "높은 pH 조건"
            ],
            delivery_systems=[
                "Aqueous serum",
                "Emulsion",
                "No special delivery needed"
            ],
            stability_tips=[
                "L-AA 대비 86배 안정적",
                "일반적인 처방 조건에서 안정",
                "특별한 패키징 불필요 (권장: 차광용기)",
                "실온 보관 가능"
            ]
        ),
        "scientific_background": """
3-O-Ethyl Ascorbic Acid는 L-Ascorbic Acid의 안정성 문제를 해결하기 위해 개발된 유도체입니다.
3번 위치 수산기에 에틸기를 도입하여 산화에 대한 저항성을 획기적으로 향상시켰습니다.

**개발 배경:**
- L-Ascorbic Acid는 뛰어난 효능에도 불구하고 불안정성이 문제
- 에틸기 보호로 산화 방지 + 친유성 증가
- 세포 내 흡수 후 활성 형태로 전환 (프로드럭 개념)

**장점:**
- 안정성: L-AA 대비 86배 향상
- 넓은 pH 범위 (4.0-6.0)에서 안정
- 나이아신아마이드와 병용 가능
- 자극 감소 (낮은 pH 불필요)

**현재 시장 동향:**
일본, 한국에서 특히 인기 있으며, 순수 비타민 C의 대안으로 각광받고 있습니다.
"""
    },
}


# ============================================================
# Deep-Dive Generator
# ============================================================

class DeepDiveGenerator:
    """Hero 성분 심층 분석 생성기"""

    def __init__(self):
        self.database = INGREDIENT_DATABASE

    def _find_ingredient(self, name: str) -> Optional[Dict]:
        """성분 데이터베이스에서 검색"""
        name_upper = name.upper().strip()

        # 직접 매칭
        if name_upper in self.database:
            return self.database[name_upper]

        # INCI명 또는 별칭으로 검색
        for key, data in self.database.items():
            if name_upper == data["inci"]:
                return data
            if "aliases" in data:
                for alias in data["aliases"]:
                    if name_upper == alias.upper():
                        return data

        # 부분 매칭
        for key, data in self.database.items():
            if name_upper in key or name_upper in data["name"].upper():
                return data

        return None

    def generate_scientific_background(self, ingredient_name: str) -> str:
        """과학적 배경 섹션 생성"""
        data = self._find_ingredient(ingredient_name)
        if data and "scientific_background" in data:
            return data["scientific_background"]
        return f"*{ingredient_name}에 대한 과학적 배경 정보를 수집 중입니다.*"

    def generate_mechanism_analysis(
        self,
        ingredient_name: str
    ) -> Optional[MechanismPathway]:
        """메커니즘 분석 생성"""
        data = self._find_ingredient(ingredient_name)
        if data and "primary_mechanism" in data:
            return data["primary_mechanism"]
        return None

    def generate_clinical_evidence(
        self,
        ingredient_name: str,
        min_studies: int = 3
    ) -> Tuple[List[ClinicalStudy], EvidenceGrade]:
        """임상 근거 수집"""
        data = self._find_ingredient(ingredient_name)
        if data:
            evidence = data.get("clinical_evidence", [])
            grade = data.get("evidence_grade", EvidenceGrade.C)
            return evidence, grade
        return [], EvidenceGrade.E

    def generate_formulation_guide(
        self,
        ingredient_name: str
    ) -> Optional[FormulationGuide]:
        """처방 가이드 생성"""
        data = self._find_ingredient(ingredient_name)
        if data and "formulation_guide" in data:
            return data["formulation_guide"]
        return None

    def generate_synergy_analysis(
        self,
        ingredient_name: str
    ) -> List[SynergyInfo]:
        """시너지 분석 생성"""
        data = self._find_ingredient(ingredient_name)
        if data and "synergies" in data:
            return data["synergies"]
        return []

    def generate_full_report(
        self,
        ingredient_name: str,
        inci_name: str = None,
        concentration: str = "",
        product_type: str = "",
        target_efficacy: List[str] = None,
        include_diagram: bool = True,
        include_evidence_table: bool = True,
        language: str = "ko"
    ) -> DeepDiveReport:
        """전체 Deep-Dive 리포트 생성"""

        # 데이터베이스 검색
        data = self._find_ingredient(ingredient_name)

        if data:
            # 데이터베이스에서 정보 로드
            report = DeepDiveReport(
                ingredient_name=data["name"],
                inci_name=data["inci"],
                category=data["category"],
                concentration=concentration or "N/A",
                product_context=product_type or "General skincare",
                scientific_background=data.get("scientific_background", ""),
                molecular_profile=data.get("molecular_profile"),
                primary_mechanism=data.get("primary_mechanism"),
                secondary_mechanisms=data.get("secondary_mechanisms", []),
                clinical_evidence=data.get("clinical_evidence", []),
                evidence_grade=data.get("evidence_grade", EvidenceGrade.C),
                formulation_guide=data.get("formulation_guide"),
                synergies=data.get("synergies", []),
                safety_profile=data.get("safety_profile"),
                references=[],
                generated_at=datetime.now().isoformat(),
                language=language,
                estimated_pages=3.5
            )
        else:
            # 기본 빈 리포트 생성
            report = DeepDiveReport(
                ingredient_name=ingredient_name,
                inci_name=inci_name or ingredient_name.upper(),
                category=IngredientCategory.OTHER,
                concentration=concentration or "N/A",
                product_context=product_type or "General skincare",
                scientific_background=f"*{ingredient_name}에 대한 정보를 수집 중입니다.*",
                generated_at=datetime.now().isoformat(),
                language=language,
                estimated_pages=1.0
            )

        return report

    def generate_brief_report(
        self,
        ingredient_name: str,
        concentration: str = ""
    ) -> DeepDiveReport:
        """간단 분석 리포트 (1페이지)"""
        report = self.generate_full_report(
            ingredient_name=ingredient_name,
            concentration=concentration
        )
        report.estimated_pages = 1.0
        report.secondary_mechanisms = []
        report.synergies = []
        return report

    def batch_generate(
        self,
        ingredients: List[Dict[str, str]]
    ) -> List[DeepDiveReport]:
        """다중 성분 배치 분석"""
        reports = []
        for item in ingredients:
            report = self.generate_full_report(
                ingredient_name=item.get("name", ""),
                inci_name=item.get("inci"),
                concentration=item.get("concentration", "")
            )
            reports.append(report)
        return reports


# ============================================================
# CLI Interface
# ============================================================

def main():
    """CLI 메인 함수"""
    import sys

    generator = DeepDiveGenerator()

    if len(sys.argv) < 2:
        print("Ingredient Deep-Dive Generator")
        print("\nUsage: python ingredient_deep_dive.py <command> [args]")
        print("\nCommands:")
        print("  analyze <ingredient>      - Generate full deep-dive analysis")
        print("  brief <ingredient>        - Generate brief analysis (1 page)")
        print("  mechanism <ingredient>    - Show mechanism pathway")
        print("  formulation <ingredient>  - Show formulation guide")
        print("  synergy <ingredient>      - Show synergy information")
        print("  list                      - List available ingredients")
        print("\nExamples:")
        print("  python ingredient_deep_dive.py analyze Niacinamide")
        print("  python ingredient_deep_dive.py mechanism Retinol")
        return

    command = sys.argv[1].lower()

    if command == "analyze" and len(sys.argv) >= 3:
        ingredient = " ".join(sys.argv[2:])
        print(f"\nGenerating Deep-Dive Analysis for: {ingredient}")
        print("=" * 60)

        report = generator.generate_full_report(ingredient)
        print(report.to_markdown())

    elif command == "brief" and len(sys.argv) >= 3:
        ingredient = " ".join(sys.argv[2:])
        print(f"\nGenerating Brief Analysis for: {ingredient}")
        print("=" * 60)

        report = generator.generate_brief_report(ingredient)
        print(report.to_markdown())

    elif command == "mechanism" and len(sys.argv) >= 3:
        ingredient = " ".join(sys.argv[2:])
        mechanism = generator.generate_mechanism_analysis(ingredient)

        if mechanism:
            print(f"\n=== {mechanism.pathway_name} ===\n")
            print(mechanism.description)
            print("\nSteps:")
            for i, step in enumerate(mechanism.steps, 1):
                print(f"  {i}. {step}")
            print("\nCellular Effects:")
            for effect in mechanism.cellular_effects:
                print(f"  - {effect}")
            print("\nSkin Effects:")
            for effect in mechanism.skin_effects:
                print(f"  - {effect}")
            if mechanism.mermaid_diagram:
                print("\nMermaid Diagram:")
                print("```mermaid")
                print(mechanism.mermaid_diagram)
                print("```")
        else:
            print(f"Mechanism data not found for: {ingredient}")

    elif command == "formulation" and len(sys.argv) >= 3:
        ingredient = " ".join(sys.argv[2:])
        guide = generator.generate_formulation_guide(ingredient)

        if guide:
            print(f"\n=== Formulation Guide for {ingredient} ===\n")
            print(f"Optimal Concentration: {guide.optimal_concentration}")
            print(f"Maximum Concentration: {guide.max_concentration}")
            print(f"pH Range: {guide.ph_range}")
            print("\nCompatible Ingredients:")
            for ing in guide.compatible_ingredients:
                print(f"  + {ing}")
            print("\nIncompatible Ingredients:")
            for ing in guide.incompatible_ingredients:
                print(f"  - {ing}")
            print("\nStability Tips:")
            for tip in guide.stability_tips:
                print(f"  * {tip}")
        else:
            print(f"Formulation guide not found for: {ingredient}")

    elif command == "synergy" and len(sys.argv) >= 3:
        ingredient = " ".join(sys.argv[2:])
        synergies = generator.generate_synergy_analysis(ingredient)

        if synergies:
            print(f"\n=== Synergy Analysis for {ingredient} ===\n")
            for syn in synergies:
                print(f"Partner: {syn.partner_ingredient}")
                print(f"  Type: {syn.synergy_type}")
                print(f"  Mechanism: {syn.mechanism}")
                print(f"  Ratio: {syn.recommended_ratio}")
                print(f"  Evidence: {syn.evidence_level}")
                print()
        else:
            print(f"Synergy data not found for: {ingredient}")

    elif command == "list":
        print("\nAvailable Ingredients in Database:")
        print("-" * 40)
        for key, data in generator.database.items():
            print(f"  {data['name']} ({data['inci']})")
            if "aliases" in data:
                print(f"    Aliases: {', '.join(data['aliases'][:3])}")

    else:
        print(f"Unknown command: {command}")
        print("Run without arguments for usage help.")


if __name__ == "__main__":
    main()
