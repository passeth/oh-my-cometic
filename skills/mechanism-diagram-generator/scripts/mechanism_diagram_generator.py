"""
Mechanism Diagram Generator
화장품 성분의 작용 메커니즘을 Mermaid 다이어그램으로 생성

Author: cosmetic-skills
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum
import json


class DiagramType(Enum):
    """다이어그램 유형"""
    FLOWCHART = "flowchart"
    SEQUENCE = "sequence"
    STATE = "state"


class MechanismType(Enum):
    """메커니즘 유형"""
    PRIMARY = "primary"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"
    ALL = "all"


class PathwayType(Enum):
    """경로 유형"""
    TYROSINASE_INHIBITION = "tyrosinase_inhibition"
    MELANIN_TRANSFER_BLOCK = "melanin_transfer_block"
    COLLAGEN_SYNTHESIS = "collagen_synthesis"
    MMP_INHIBITION = "mmp_inhibition"
    ANTIOXIDANT_NETWORK = "antioxidant_network"
    NAD_METABOLISM = "nad_metabolism"
    RETINOID_SIGNALING = "retinoid_signaling"
    BARRIER_LIPID = "barrier_lipid"
    HYALURONIC_HYDRATION = "hyaluronic_hydration"
    PEPTIDE_SIGNALING = "peptide_signaling"
    ANTI_INFLAMMATORY = "anti_inflammatory"
    EXFOLIATION = "exfoliation"


class Direction(Enum):
    """다이어그램 방향"""
    TD = "TD"  # Top to Down
    TB = "TB"  # Top to Bottom
    BT = "BT"  # Bottom to Top
    LR = "LR"  # Left to Right
    RL = "RL"  # Right to Left


@dataclass
class Node:
    """다이어그램 노드"""
    id: str
    label: str
    label_en: str = ""
    shape: str = "rounded"  # rounded, rect, circle, diamond, hexagon
    style: Optional[Dict[str, str]] = None
    subgraph: Optional[str] = None

    def to_mermaid(self, language: str = "ko") -> str:
        """Mermaid 노드 문법 생성"""
        shape_map = {
            "rounded": ("[", "]"),
            "rect": ("[[", "]]"),
            "circle": ("((", "))"),
            "diamond": ("{", "}"),
            "hexagon": ("{{", "}}"),
            "stadium": ("([", "])"),
            "subroutine": ("[[", "]]"),
            "database": ("[(", ")]"),
        }

        left, right = shape_map.get(self.shape, ("[", "]"))

        if language == "en":
            label = self.label_en or self.label
        elif language == "ko-en":
            label = f"{self.label}<br>{self.label_en}" if self.label_en else self.label
        else:
            label = self.label

        return f"{self.id}{left}{label}{right}"


@dataclass
class Edge:
    """다이어그램 연결"""
    source: str
    target: str
    label: str = ""
    label_en: str = ""
    edge_type: str = "arrow"  # arrow, dotted, thick, inhibit

    def to_mermaid(self, language: str = "ko") -> str:
        """Mermaid 엣지 문법 생성"""
        edge_map = {
            "arrow": "-->",
            "dotted": "-.->",
            "thick": "==>",
            "inhibit": "--|",
            "bidirectional": "<-->",
        }

        connector = edge_map.get(self.edge_type, "-->")

        if language == "en":
            label = self.label_en or self.label
        elif language == "ko-en":
            label = f"{self.label}/{self.label_en}" if self.label_en else self.label
        else:
            label = self.label

        if label:
            return f"{self.source} {connector}|{label}| {self.target}"
        return f"{self.source} {connector} {self.target}"


@dataclass
class Subgraph:
    """서브그래프 (그룹)"""
    id: str
    label: str
    label_en: str = ""
    nodes: List[str] = field(default_factory=list)

    def to_mermaid(self, language: str = "ko") -> str:
        """Mermaid subgraph 문법"""
        if language == "en":
            label = self.label_en or self.label
        elif language == "ko-en":
            label = f"{self.label}<br>{self.label_en}" if self.label_en else self.label
        else:
            label = self.label
        return f'subgraph {self.id}["{label}"]'


@dataclass
class StyleConfig:
    """스타일 설정"""
    input_color: str = "#e1f5fe"
    process_color: str = "#ffffff"
    output_color: str = "#c8e6c9"
    inhibit_color: str = "#ffcdd2"
    activate_color: str = "#dcedc8"
    highlight_color: str = "#fff9c4"
    font_size: str = "14px"
    node_shape: str = "rounded"


@dataclass
class DiagramResult:
    """다이어그램 결과"""
    ingredient: str
    mechanism_type: str
    diagram_type: DiagramType
    code: str
    language: str
    nodes: List[Node]
    edges: List[Edge]
    subgraphs: List[Subgraph]
    style: StyleConfig
    title: str = ""
    description: str = ""

    def to_mermaid(self) -> str:
        """Mermaid 코드 반환"""
        return self.code

    def to_html(self) -> str:
        """HTML 임베드 코드"""
        return f'''<div class="mermaid">
{self.code}
</div>
<script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
<script>mermaid.initialize({{startOnLoad:true}});</script>'''

    def to_markdown(self) -> str:
        """마크다운 코드 블록"""
        return f"```mermaid\n{self.code}\n```"

    def save(self, filepath: str) -> None:
        """파일로 저장"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.code)


# ============================================================
# 경로 템플릿 데이터베이스
# ============================================================

PATHWAY_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "tyrosinase_inhibition": {
        "title": "티로시나제 억제 경로",
        "title_en": "Tyrosinase Inhibition Pathway",
        "description": "미백 활성 성분의 티로시나제 효소 억제 메커니즘",
        "subgraphs": [
            {"id": "Input", "label": "🧴 성분 적용", "label_en": "Ingredient Application"},
            {"id": "Enzyme", "label": "🔬 효소 수준", "label_en": "Enzyme Level"},
            {"id": "Cellular", "label": "🔴 세포 수준", "label_en": "Cellular Level"},
            {"id": "Clinical", "label": "✨ 임상 효과", "label_en": "Clinical Effects"},
        ],
        "nodes": [
            {"id": "A", "label": "{ingredient}", "subgraph": "Input", "style": "input"},
            {"id": "B", "label": "티로시나제<br>Tyrosinase", "subgraph": "Enzyme"},
            {"id": "C", "label": "L-Tyrosine →<br>L-DOPA 반응", "subgraph": "Enzyme"},
            {"id": "D", "label": "멜라닌 합성 ↓", "subgraph": "Cellular"},
            {"id": "E", "label": "멜라노좀 성숙 ↓", "subgraph": "Cellular"},
            {"id": "F", "label": "피부톤 균일화", "subgraph": "Clinical", "style": "output"},
            {"id": "G", "label": "색소 침착 개선", "subgraph": "Clinical", "style": "output"},
        ],
        "edges": [
            {"source": "A", "target": "B", "label": "억제", "type": "inhibit"},
            {"source": "B", "target": "C", "label": "감소"},
            {"source": "C", "target": "D"},
            {"source": "D", "target": "E"},
            {"source": "E", "target": "F"},
            {"source": "E", "target": "G"},
        ],
    },

    "melanin_transfer_block": {
        "title": "멜라노좀 전달 차단 경로",
        "title_en": "Melanin Transfer Blocking Pathway",
        "description": "멜라닌세포에서 각질세포로의 멜라노좀 전달을 차단하는 메커니즘",
        "subgraphs": [
            {"id": "Input", "label": "🧴 성분 적용", "label_en": "Ingredient Application"},
            {"id": "Melanocyte", "label": "🟤 멜라닌세포", "label_en": "Melanocyte"},
            {"id": "Transfer", "label": "🔀 전달 과정", "label_en": "Transfer Process"},
            {"id": "Keratinocyte", "label": "🟡 각질세포", "label_en": "Keratinocyte"},
            {"id": "Clinical", "label": "✨ 임상 효과", "label_en": "Clinical Effects"},
        ],
        "nodes": [
            {"id": "A", "label": "{ingredient}", "subgraph": "Input", "style": "input"},
            {"id": "B", "label": "멜라노좀<br>Melanosome", "subgraph": "Melanocyte"},
            {"id": "C", "label": "PAR-2<br>수용체", "subgraph": "Transfer"},
            {"id": "D", "label": "멜라노좀<br>방출/흡수", "subgraph": "Transfer"},
            {"id": "E", "label": "각질세포 내<br>멜라닌 축적 ↓", "subgraph": "Keratinocyte"},
            {"id": "F", "label": "피부 밝아짐", "subgraph": "Clinical", "style": "output"},
        ],
        "edges": [
            {"source": "A", "target": "C", "label": "억제", "type": "inhibit"},
            {"source": "B", "target": "D"},
            {"source": "C", "target": "D", "label": "조절"},
            {"source": "D", "target": "E", "label": "감소"},
            {"source": "E", "target": "F"},
        ],
    },

    "collagen_synthesis": {
        "title": "콜라겐 합성 촉진 경로",
        "title_en": "Collagen Synthesis Pathway",
        "description": "섬유아세포의 콜라겐 생성을 촉진하는 메커니즘",
        "subgraphs": [
            {"id": "Input", "label": "🧴 성분 적용", "label_en": "Ingredient Application"},
            {"id": "Signaling", "label": "📡 신호전달", "label_en": "Signal Transduction"},
            {"id": "Synthesis", "label": "🔧 합성", "label_en": "Synthesis"},
            {"id": "ECM", "label": "🧱 세포외기질", "label_en": "Extracellular Matrix"},
            {"id": "Clinical", "label": "✨ 임상 효과", "label_en": "Clinical Effects"},
        ],
        "nodes": [
            {"id": "A", "label": "{ingredient}", "subgraph": "Input", "style": "input"},
            {"id": "B", "label": "TGF-β<br>활성화", "subgraph": "Signaling"},
            {"id": "C", "label": "SMAD<br>경로", "subgraph": "Signaling"},
            {"id": "D", "label": "COL1A1/COL3A1<br>유전자 발현 ↑", "subgraph": "Synthesis"},
            {"id": "E", "label": "프로콜라겐<br>생성", "subgraph": "Synthesis"},
            {"id": "F", "label": "콜라겐 섬유<br>조립", "subgraph": "ECM"},
            {"id": "G", "label": "진피 밀도 ↑", "subgraph": "ECM"},
            {"id": "H", "label": "탄력 증가", "subgraph": "Clinical", "style": "output"},
            {"id": "I", "label": "주름 감소", "subgraph": "Clinical", "style": "output"},
        ],
        "edges": [
            {"source": "A", "target": "B"},
            {"source": "B", "target": "C"},
            {"source": "C", "target": "D"},
            {"source": "D", "target": "E"},
            {"source": "E", "target": "F"},
            {"source": "F", "target": "G"},
            {"source": "G", "target": "H"},
            {"source": "G", "target": "I"},
        ],
    },

    "mmp_inhibition": {
        "title": "MMP 억제 경로",
        "title_en": "MMP Inhibition Pathway",
        "description": "매트릭스 금속단백분해효소 억제를 통한 콜라겐 보호 메커니즘",
        "subgraphs": [
            {"id": "Input", "label": "🧴 성분 적용", "label_en": "Ingredient Application"},
            {"id": "Enzyme", "label": "🔬 효소 억제", "label_en": "Enzyme Inhibition"},
            {"id": "Protection", "label": "🛡️ 보호 효과", "label_en": "Protection"},
            {"id": "Clinical", "label": "✨ 임상 효과", "label_en": "Clinical Effects"},
        ],
        "nodes": [
            {"id": "A", "label": "{ingredient}", "subgraph": "Input", "style": "input"},
            {"id": "B", "label": "MMP-1<br>(Collagenase)", "subgraph": "Enzyme"},
            {"id": "C", "label": "MMP-3<br>(Stromelysin)", "subgraph": "Enzyme"},
            {"id": "D", "label": "콜라겐 분해 ↓", "subgraph": "Protection"},
            {"id": "E", "label": "엘라스틴 분해 ↓", "subgraph": "Protection"},
            {"id": "F", "label": "ECM 보존", "subgraph": "Protection"},
            {"id": "G", "label": "피부 구조 유지", "subgraph": "Clinical", "style": "output"},
            {"id": "H", "label": "탄력 유지", "subgraph": "Clinical", "style": "output"},
        ],
        "edges": [
            {"source": "A", "target": "B", "label": "억제", "type": "inhibit"},
            {"source": "A", "target": "C", "label": "억제", "type": "inhibit"},
            {"source": "B", "target": "D"},
            {"source": "C", "target": "E"},
            {"source": "D", "target": "F"},
            {"source": "E", "target": "F"},
            {"source": "F", "target": "G"},
            {"source": "F", "target": "H"},
        ],
    },

    "antioxidant_network": {
        "title": "항산화 네트워크",
        "title_en": "Antioxidant Network",
        "description": "자유라디칼 중화 및 항산화 재생 네트워크",
        "subgraphs": [
            {"id": "Stress", "label": "⚠️ 산화 스트레스", "label_en": "Oxidative Stress"},
            {"id": "Input", "label": "🧴 항산화 성분", "label_en": "Antioxidants"},
            {"id": "Action", "label": "🛡️ 중화 작용", "label_en": "Neutralization"},
            {"id": "Regeneration", "label": "🔄 재생", "label_en": "Regeneration"},
            {"id": "Clinical", "label": "✨ 보호 효과", "label_en": "Protective Effects"},
        ],
        "nodes": [
            {"id": "X", "label": "UV/오염<br>외부 스트레스", "subgraph": "Stress", "style": "inhibit"},
            {"id": "Y", "label": "ROS 생성<br>자유라디칼", "subgraph": "Stress", "style": "inhibit"},
            {"id": "A", "label": "{ingredient}", "subgraph": "Input", "style": "input"},
            {"id": "B", "label": "전자 공여", "subgraph": "Action"},
            {"id": "C", "label": "라디칼 중화", "subgraph": "Action"},
            {"id": "D", "label": "Vitamin E<br>재생", "subgraph": "Regeneration"},
            {"id": "E", "label": "글루타치온<br>재생", "subgraph": "Regeneration"},
            {"id": "F", "label": "DNA 보호", "subgraph": "Clinical", "style": "output"},
            {"id": "G", "label": "콜라겐 보호", "subgraph": "Clinical", "style": "output"},
            {"id": "H", "label": "광노화 예방", "subgraph": "Clinical", "style": "output"},
        ],
        "edges": [
            {"source": "X", "target": "Y"},
            {"source": "A", "target": "B"},
            {"source": "B", "target": "C"},
            {"source": "C", "target": "Y", "label": "중화", "type": "inhibit"},
            {"source": "A", "target": "D"},
            {"source": "A", "target": "E"},
            {"source": "C", "target": "F"},
            {"source": "C", "target": "G"},
            {"source": "F", "target": "H"},
            {"source": "G", "target": "H"},
        ],
    },

    "nad_metabolism": {
        "title": "NAD+ 대사 경로",
        "title_en": "NAD+ Metabolism Pathway",
        "description": "Niacinamide의 NAD+ 대사 및 다중 효과 메커니즘",
        "subgraphs": [
            {"id": "Input", "label": "🧴 성분 적용", "label_en": "Ingredient Application"},
            {"id": "Metabolism", "label": "🔄 대사 경로", "label_en": "Metabolic Pathway"},
            {"id": "Cellular", "label": "🔴 세포 효과", "label_en": "Cellular Effects"},
            {"id": "Functions", "label": "⚙️ 기능", "label_en": "Functions"},
            {"id": "Clinical", "label": "✨ 임상 효과", "label_en": "Clinical Effects"},
        ],
        "nodes": [
            {"id": "A", "label": "{ingredient}", "subgraph": "Input", "style": "input"},
            {"id": "B", "label": "NAD+ 합성<br>Salvage Pathway", "subgraph": "Metabolism"},
            {"id": "C", "label": "NADH 생성", "subgraph": "Metabolism"},
            {"id": "D", "label": "NADPH 풀", "subgraph": "Metabolism"},
            {"id": "E", "label": "ATP 생산 ↑", "subgraph": "Cellular"},
            {"id": "F", "label": "PARP 활성화<br>DNA 복구", "subgraph": "Cellular"},
            {"id": "G", "label": "Sirtuin 활성화", "subgraph": "Cellular"},
            {"id": "H", "label": "세라마이드<br>합성 ↑", "subgraph": "Functions"},
            {"id": "I", "label": "멜라노좀<br>전달 ↓", "subgraph": "Functions"},
            {"id": "J", "label": "피지 생성<br>조절", "subgraph": "Functions"},
            {"id": "K", "label": "장벽 강화", "subgraph": "Clinical", "style": "output"},
            {"id": "L", "label": "미백", "subgraph": "Clinical", "style": "output"},
            {"id": "M", "label": "모공 케어", "subgraph": "Clinical", "style": "output"},
        ],
        "edges": [
            {"source": "A", "target": "B"},
            {"source": "B", "target": "C"},
            {"source": "B", "target": "D"},
            {"source": "C", "target": "E"},
            {"source": "B", "target": "F"},
            {"source": "B", "target": "G"},
            {"source": "G", "target": "H"},
            {"source": "A", "target": "I"},
            {"source": "A", "target": "J"},
            {"source": "H", "target": "K"},
            {"source": "I", "target": "L"},
            {"source": "J", "target": "M"},
        ],
    },

    "retinoid_signaling": {
        "title": "레티노이드 신호전달 경로",
        "title_en": "Retinoid Signaling Pathway",
        "description": "Retinol의 핵수용체 매개 유전자 조절 메커니즘",
        "subgraphs": [
            {"id": "Input", "label": "🧴 성분 적용", "label_en": "Ingredient Application"},
            {"id": "Conversion", "label": "🔄 전환", "label_en": "Conversion"},
            {"id": "Nuclear", "label": "🔵 핵 수용체", "label_en": "Nuclear Receptors"},
            {"id": "Gene", "label": "🧬 유전자 발현", "label_en": "Gene Expression"},
            {"id": "Clinical", "label": "✨ 임상 효과", "label_en": "Clinical Effects"},
        ],
        "nodes": [
            {"id": "A", "label": "{ingredient}", "subgraph": "Input", "style": "input"},
            {"id": "B", "label": "Retinaldehyde<br>(ADH)", "subgraph": "Conversion"},
            {"id": "C", "label": "Retinoic Acid<br>(RALDH)", "subgraph": "Conversion"},
            {"id": "D", "label": "RAR 결합<br>(α/β/γ)", "subgraph": "Nuclear"},
            {"id": "E", "label": "RXR 결합", "subgraph": "Nuclear"},
            {"id": "F", "label": "RAR:RXR<br>이종이합체", "subgraph": "Nuclear"},
            {"id": "G", "label": "RARE 결합", "subgraph": "Gene"},
            {"id": "H", "label": "COL1A1 ↑<br>콜라겐", "subgraph": "Gene"},
            {"id": "I", "label": "MMP-1 ↓", "subgraph": "Gene"},
            {"id": "J", "label": "분화 유전자<br>조절", "subgraph": "Gene"},
            {"id": "K", "label": "주름 감소", "subgraph": "Clinical", "style": "output"},
            {"id": "L", "label": "탄력 증가", "subgraph": "Clinical", "style": "output"},
            {"id": "M", "label": "피부결 개선", "subgraph": "Clinical", "style": "output"},
        ],
        "edges": [
            {"source": "A", "target": "B"},
            {"source": "B", "target": "C"},
            {"source": "C", "target": "D"},
            {"source": "C", "target": "E"},
            {"source": "D", "target": "F"},
            {"source": "E", "target": "F"},
            {"source": "F", "target": "G"},
            {"source": "G", "target": "H"},
            {"source": "G", "target": "I"},
            {"source": "G", "target": "J"},
            {"source": "H", "target": "K"},
            {"source": "I", "target": "L"},
            {"source": "J", "target": "M"},
        ],
    },

    "barrier_lipid": {
        "title": "피부 장벽 지질 합성 경로",
        "title_en": "Skin Barrier Lipid Synthesis Pathway",
        "description": "피부 장벽 강화를 위한 지질 합성 메커니즘",
        "subgraphs": [
            {"id": "Input", "label": "🧴 성분 적용", "label_en": "Ingredient Application"},
            {"id": "Signaling", "label": "📡 신호전달", "label_en": "Signaling"},
            {"id": "Synthesis", "label": "🔧 지질 합성", "label_en": "Lipid Synthesis"},
            {"id": "Barrier", "label": "🧱 장벽 구조", "label_en": "Barrier Structure"},
            {"id": "Clinical", "label": "✨ 임상 효과", "label_en": "Clinical Effects"},
        ],
        "nodes": [
            {"id": "A", "label": "{ingredient}", "subgraph": "Input", "style": "input"},
            {"id": "B", "label": "PPAR<br>활성화", "subgraph": "Signaling"},
            {"id": "C", "label": "지질 합성<br>유전자 발현", "subgraph": "Signaling"},
            {"id": "D", "label": "세라마이드<br>합성 ↑", "subgraph": "Synthesis"},
            {"id": "E", "label": "지방산<br>합성 ↑", "subgraph": "Synthesis"},
            {"id": "F", "label": "콜레스테롤<br>합성 ↑", "subgraph": "Synthesis"},
            {"id": "G", "label": "층판소체<br>분비", "subgraph": "Barrier"},
            {"id": "H", "label": "세포간 지질층", "subgraph": "Barrier"},
            {"id": "I", "label": "TEWL 감소", "subgraph": "Clinical", "style": "output"},
            {"id": "J", "label": "보습 증가", "subgraph": "Clinical", "style": "output"},
            {"id": "K", "label": "자극 감소", "subgraph": "Clinical", "style": "output"},
        ],
        "edges": [
            {"source": "A", "target": "B"},
            {"source": "B", "target": "C"},
            {"source": "C", "target": "D"},
            {"source": "C", "target": "E"},
            {"source": "C", "target": "F"},
            {"source": "D", "target": "G"},
            {"source": "E", "target": "G"},
            {"source": "F", "target": "G"},
            {"source": "G", "target": "H"},
            {"source": "H", "target": "I"},
            {"source": "H", "target": "J"},
            {"source": "H", "target": "K"},
        ],
    },

    "hyaluronic_hydration": {
        "title": "히알루론산 수분 경로",
        "title_en": "Hyaluronic Acid Hydration Pathway",
        "description": "분자량별 히알루론산의 수분 보유 메커니즘",
        "subgraphs": [
            {"id": "HMW", "label": "🔵 High MW (>1000 kDa)", "label_en": "High Molecular Weight"},
            {"id": "MMW", "label": "🔷 Medium MW", "label_en": "Medium Molecular Weight"},
            {"id": "LMW", "label": "🔹 Low MW (<100 kDa)", "label_en": "Low Molecular Weight"},
            {"id": "Clinical", "label": "✨ 임상 효과", "label_en": "Clinical Effects"},
        ],
        "nodes": [
            {"id": "A1", "label": "표면 잔류", "subgraph": "HMW"},
            {"id": "A2", "label": "수분막 형성", "subgraph": "HMW"},
            {"id": "A3", "label": "즉각 보습감", "subgraph": "HMW"},
            {"id": "B1", "label": "표피 상층<br>침투", "subgraph": "MMW"},
            {"id": "B2", "label": "수분 보유", "subgraph": "MMW"},
            {"id": "B3", "label": "지속적 보습", "subgraph": "MMW"},
            {"id": "C1", "label": "진피 도달", "subgraph": "LMW"},
            {"id": "C2", "label": "CD44 결합", "subgraph": "LMW"},
            {"id": "C3", "label": "신호전달 활성", "subgraph": "LMW"},
            {"id": "D", "label": "피부 수분도 ↑", "subgraph": "Clinical", "style": "output"},
            {"id": "E", "label": "탄력 개선", "subgraph": "Clinical", "style": "output"},
            {"id": "F", "label": "주름 완화", "subgraph": "Clinical", "style": "output"},
        ],
        "edges": [
            {"source": "A1", "target": "A2"},
            {"source": "A2", "target": "A3"},
            {"source": "B1", "target": "B2"},
            {"source": "B2", "target": "B3"},
            {"source": "C1", "target": "C2"},
            {"source": "C2", "target": "C3"},
            {"source": "A3", "target": "D"},
            {"source": "B3", "target": "D"},
            {"source": "C3", "target": "E"},
            {"source": "C3", "target": "F"},
        ],
    },

    "peptide_signaling": {
        "title": "펩타이드 신호전달 경로",
        "title_en": "Peptide Signaling Pathway",
        "description": "시그널 펩타이드의 세포 신호전달 메커니즘",
        "subgraphs": [
            {"id": "Input", "label": "🧴 성분 적용", "label_en": "Ingredient Application"},
            {"id": "Reception", "label": "📡 수용", "label_en": "Reception"},
            {"id": "Signaling", "label": "🔀 신호전달", "label_en": "Signal Transduction"},
            {"id": "Response", "label": "🔧 세포 반응", "label_en": "Cellular Response"},
            {"id": "Clinical", "label": "✨ 임상 효과", "label_en": "Clinical Effects"},
        ],
        "nodes": [
            {"id": "A", "label": "{ingredient}", "subgraph": "Input", "style": "input"},
            {"id": "B", "label": "세포막<br>수용체", "subgraph": "Reception"},
            {"id": "C", "label": "신호 인식", "subgraph": "Reception"},
            {"id": "D", "label": "MAPK 경로", "subgraph": "Signaling"},
            {"id": "E", "label": "TGF-β 경로", "subgraph": "Signaling"},
            {"id": "F", "label": "전사인자<br>활성화", "subgraph": "Signaling"},
            {"id": "G", "label": "ECM 단백질<br>합성 ↑", "subgraph": "Response"},
            {"id": "H", "label": "성장인자 분비", "subgraph": "Response"},
            {"id": "I", "label": "콜라겐 증가", "subgraph": "Clinical", "style": "output"},
            {"id": "J", "label": "탄력 개선", "subgraph": "Clinical", "style": "output"},
            {"id": "K", "label": "주름 감소", "subgraph": "Clinical", "style": "output"},
        ],
        "edges": [
            {"source": "A", "target": "B"},
            {"source": "B", "target": "C"},
            {"source": "C", "target": "D"},
            {"source": "C", "target": "E"},
            {"source": "D", "target": "F"},
            {"source": "E", "target": "F"},
            {"source": "F", "target": "G"},
            {"source": "F", "target": "H"},
            {"source": "G", "target": "I"},
            {"source": "H", "target": "J"},
            {"source": "I", "target": "K"},
            {"source": "J", "target": "K"},
        ],
    },

    "anti_inflammatory": {
        "title": "항염 경로",
        "title_en": "Anti-inflammatory Pathway",
        "description": "염증 반응 억제 메커니즘",
        "subgraphs": [
            {"id": "Trigger", "label": "⚠️ 염증 유발", "label_en": "Inflammation Trigger"},
            {"id": "Input", "label": "🧴 진정 성분", "label_en": "Soothing Ingredient"},
            {"id": "Inhibition", "label": "🚫 억제 작용", "label_en": "Inhibition"},
            {"id": "Reduction", "label": "📉 감소", "label_en": "Reduction"},
            {"id": "Clinical", "label": "✨ 임상 효과", "label_en": "Clinical Effects"},
        ],
        "nodes": [
            {"id": "X", "label": "자극 요인<br>(UV, 화학물질)", "subgraph": "Trigger", "style": "inhibit"},
            {"id": "Y", "label": "염증 반응 개시", "subgraph": "Trigger", "style": "inhibit"},
            {"id": "A", "label": "{ingredient}", "subgraph": "Input", "style": "input"},
            {"id": "B", "label": "NF-κB 억제", "subgraph": "Inhibition"},
            {"id": "C", "label": "COX-2 억제", "subgraph": "Inhibition"},
            {"id": "D", "label": "사이토카인<br>조절", "subgraph": "Inhibition"},
            {"id": "E", "label": "IL-6 ↓", "subgraph": "Reduction"},
            {"id": "F", "label": "TNF-α ↓", "subgraph": "Reduction"},
            {"id": "G", "label": "PGE2 ↓", "subgraph": "Reduction"},
            {"id": "H", "label": "홍반 감소", "subgraph": "Clinical", "style": "output"},
            {"id": "I", "label": "가려움 완화", "subgraph": "Clinical", "style": "output"},
            {"id": "J", "label": "자극 진정", "subgraph": "Clinical", "style": "output"},
        ],
        "edges": [
            {"source": "X", "target": "Y"},
            {"source": "A", "target": "B"},
            {"source": "A", "target": "C"},
            {"source": "A", "target": "D"},
            {"source": "B", "target": "E"},
            {"source": "C", "target": "G"},
            {"source": "D", "target": "F"},
            {"source": "E", "target": "H"},
            {"source": "F", "target": "H"},
            {"source": "G", "target": "I"},
            {"source": "H", "target": "J"},
            {"source": "I", "target": "J"},
        ],
    },

    "exfoliation": {
        "title": "각질 제거 경로",
        "title_en": "Exfoliation Pathway",
        "description": "화학적 각질 제거 메커니즘 (AHA/BHA)",
        "subgraphs": [
            {"id": "Input", "label": "🧴 성분 적용", "label_en": "Ingredient Application"},
            {"id": "Mechanism", "label": "🔬 작용 기전", "label_en": "Mechanism"},
            {"id": "Cellular", "label": "🔴 세포 수준", "label_en": "Cellular Level"},
            {"id": "Clinical", "label": "✨ 임상 효과", "label_en": "Clinical Effects"},
        ],
        "nodes": [
            {"id": "A", "label": "{ingredient}", "subgraph": "Input", "style": "input"},
            {"id": "B", "label": "데스모좀<br>결합 약화", "subgraph": "Mechanism"},
            {"id": "C", "label": "세포간 결합<br>감소", "subgraph": "Mechanism"},
            {"id": "D", "label": "각질세포<br>탈락 촉진", "subgraph": "Cellular"},
            {"id": "E", "label": "세포 턴오버 ↑", "subgraph": "Cellular"},
            {"id": "F", "label": "피부결 개선", "subgraph": "Clinical", "style": "output"},
            {"id": "G", "label": "모공 정화", "subgraph": "Clinical", "style": "output"},
            {"id": "H", "label": "피부톤 균일화", "subgraph": "Clinical", "style": "output"},
        ],
        "edges": [
            {"source": "A", "target": "B"},
            {"source": "B", "target": "C"},
            {"source": "C", "target": "D"},
            {"source": "D", "target": "E"},
            {"source": "E", "target": "F"},
            {"source": "D", "target": "G"},
            {"source": "E", "target": "H"},
        ],
    },
}


# ============================================================
# 성분별 기본 경로 매핑
# ============================================================

INGREDIENT_PATHWAY_MAP: Dict[str, List[str]] = {
    "niacinamide": ["nad_metabolism", "melanin_transfer_block", "barrier_lipid"],
    "retinol": ["retinoid_signaling", "collagen_synthesis", "mmp_inhibition"],
    "vitamin c": ["antioxidant_network", "collagen_synthesis", "tyrosinase_inhibition"],
    "ascorbic acid": ["antioxidant_network", "collagen_synthesis", "tyrosinase_inhibition"],
    "3-o-ethyl ascorbic acid": ["antioxidant_network", "tyrosinase_inhibition"],
    "arbutin": ["tyrosinase_inhibition"],
    "kojic acid": ["tyrosinase_inhibition"],
    "tranexamic acid": ["melanin_transfer_block"],
    "hyaluronic acid": ["hyaluronic_hydration"],
    "sodium hyaluronate": ["hyaluronic_hydration"],
    "ceramide": ["barrier_lipid"],
    "ceramide np": ["barrier_lipid"],
    "centella asiatica": ["anti_inflammatory", "collagen_synthesis"],
    "madecassoside": ["anti_inflammatory", "collagen_synthesis"],
    "panthenol": ["anti_inflammatory", "barrier_lipid"],
    "glycolic acid": ["exfoliation"],
    "salicylic acid": ["exfoliation"],
    "lactic acid": ["exfoliation"],
    "matrixyl": ["peptide_signaling", "collagen_synthesis"],
    "argireline": ["peptide_signaling"],
    "copper peptide": ["peptide_signaling", "collagen_synthesis"],
    "ghk-cu": ["peptide_signaling", "collagen_synthesis"],
    "vitamin e": ["antioxidant_network"],
    "tocopherol": ["antioxidant_network"],
    "ferulic acid": ["antioxidant_network"],
    "egcg": ["antioxidant_network", "mmp_inhibition"],
    "green tea": ["antioxidant_network", "mmp_inhibition"],
}


class DiagramGenerator:
    """메커니즘 다이어그램 생성기"""

    def __init__(self, style: Optional[StyleConfig] = None):
        self.style = style or StyleConfig()
        self.templates = PATHWAY_TEMPLATES
        self.ingredient_map = INGREDIENT_PATHWAY_MAP

    def generate(
        self,
        ingredient: str,
        mechanism_type: str = "primary",
        diagram_type: str = "flowchart",
        direction: str = "TD",
        language: str = "ko",
        custom_style: Optional[Dict] = None
    ) -> DiagramResult:
        """
        메커니즘 다이어그램 생성

        Args:
            ingredient: 성분명
            mechanism_type: primary, secondary, all
            diagram_type: flowchart, sequence, state
            direction: TD, TB, BT, LR, RL
            language: ko, en, ko-en
            custom_style: 커스텀 스타일 설정
        """
        # 성분 정규화
        ingredient_key = ingredient.lower().strip()

        # 해당 성분의 경로 찾기
        pathways = self.ingredient_map.get(ingredient_key, [])

        if not pathways:
            # 기본 템플릿 사용
            return self._generate_generic_diagram(ingredient, language, direction)

        # 메커니즘 유형에 따라 경로 선택
        if mechanism_type == "primary":
            template_id = pathways[0]
        elif mechanism_type == "secondary" and len(pathways) > 1:
            template_id = pathways[1]
        elif mechanism_type == "all":
            return self._generate_combined_diagram(
                ingredient, pathways, language, direction
            )
        else:
            template_id = pathways[0]

        return self.from_template(template_id, ingredient, language, direction)

    def from_template(
        self,
        template_id: str,
        ingredient: str,
        language: str = "ko",
        direction: str = "TD"
    ) -> DiagramResult:
        """템플릿에서 다이어그램 생성"""

        template = self.templates.get(template_id)
        if not template:
            raise ValueError(f"Unknown template: {template_id}")

        # 노드 생성
        nodes = []
        for node_data in template["nodes"]:
            label = node_data["label"].replace("{ingredient}", ingredient)
            node = Node(
                id=node_data["id"],
                label=label,
                label_en=node_data.get("label_en", ""),
                subgraph=node_data.get("subgraph"),
                style={"type": node_data.get("style", "default")}
            )
            nodes.append(node)

        # 엣지 생성
        edges = []
        for edge_data in template["edges"]:
            edge = Edge(
                source=edge_data["source"],
                target=edge_data["target"],
                label=edge_data.get("label", ""),
                edge_type=edge_data.get("type", "arrow")
            )
            edges.append(edge)

        # 서브그래프 생성
        subgraphs = []
        for sg_data in template["subgraphs"]:
            sg = Subgraph(
                id=sg_data["id"],
                label=sg_data["label"],
                label_en=sg_data.get("label_en", "")
            )
            # 노드를 서브그래프에 할당
            sg.nodes = [n.id for n in nodes if n.subgraph == sg.id]
            subgraphs.append(sg)

        # Mermaid 코드 생성
        code = self._build_mermaid_code(
            nodes, edges, subgraphs, direction, language
        )

        return DiagramResult(
            ingredient=ingredient,
            mechanism_type=template_id,
            diagram_type=DiagramType.FLOWCHART,
            code=code,
            language=language,
            nodes=nodes,
            edges=edges,
            subgraphs=subgraphs,
            style=self.style,
            title=template["title"] if language != "en" else template.get("title_en", template["title"]),
            description=template.get("description", "")
        )

    def _build_mermaid_code(
        self,
        nodes: List[Node],
        edges: List[Edge],
        subgraphs: List[Subgraph],
        direction: str,
        language: str
    ) -> str:
        """Mermaid 코드 빌드"""

        lines = [f"graph {direction}"]

        # 서브그래프별 노드 그룹화
        for sg in subgraphs:
            lines.append(f"    {sg.to_mermaid(language)}")
            for node in nodes:
                if node.subgraph == sg.id:
                    lines.append(f"        {node.to_mermaid(language)}")
            lines.append("    end")

        # 서브그래프에 속하지 않은 노드
        orphan_nodes = [n for n in nodes if not n.subgraph]
        for node in orphan_nodes:
            lines.append(f"    {node.to_mermaid(language)}")

        # 연결 추가
        lines.append("")
        for edge in edges:
            lines.append(f"    {edge.to_mermaid(language)}")

        # 스타일 추가
        lines.append("")
        for node in nodes:
            if node.style and node.style.get("type") == "input":
                lines.append(f"    style {node.id} fill:{self.style.input_color}")
            elif node.style and node.style.get("type") == "output":
                lines.append(f"    style {node.id} fill:{self.style.output_color}")
            elif node.style and node.style.get("type") == "inhibit":
                lines.append(f"    style {node.id} fill:{self.style.inhibit_color}")

        return "\n".join(lines)

    def _generate_generic_diagram(
        self,
        ingredient: str,
        language: str,
        direction: str
    ) -> DiagramResult:
        """일반 다이어그램 생성 (템플릿 없는 경우)"""

        nodes = [
            Node("A", ingredient, subgraph="Input", style={"type": "input"}),
            Node("B", "작용 기전", subgraph="Mechanism"),
            Node("C", "세포 반응", subgraph="Cellular"),
            Node("D", "피부 효과", subgraph="Clinical", style={"type": "output"}),
        ]

        edges = [
            Edge("A", "B"),
            Edge("B", "C"),
            Edge("C", "D"),
        ]

        subgraphs = [
            Subgraph("Input", "🧴 성분 적용"),
            Subgraph("Mechanism", "🔬 작용 기전"),
            Subgraph("Cellular", "🔴 세포 반응"),
            Subgraph("Clinical", "✨ 임상 효과"),
        ]

        code = self._build_mermaid_code(nodes, edges, subgraphs, direction, language)

        return DiagramResult(
            ingredient=ingredient,
            mechanism_type="generic",
            diagram_type=DiagramType.FLOWCHART,
            code=code,
            language=language,
            nodes=nodes,
            edges=edges,
            subgraphs=subgraphs,
            style=self.style,
            title=f"{ingredient} 작용 메커니즘",
            description="일반 메커니즘 다이어그램"
        )

    def _generate_combined_diagram(
        self,
        ingredient: str,
        pathways: List[str],
        language: str,
        direction: str
    ) -> DiagramResult:
        """다중 경로 통합 다이어그램"""

        all_nodes = []
        all_edges = []
        all_subgraphs = []

        # 입력 노드 (공통)
        input_node = Node("A0", ingredient, subgraph="Input", style={"type": "input"})
        all_nodes.append(input_node)
        all_subgraphs.append(Subgraph("Input", "🧴 성분 적용"))

        # 각 경로별 노드/엣지 추가 (첫 노드를 입력 노드에 연결)
        for idx, pathway_id in enumerate(pathways[:3]):  # 최대 3개 경로
            template = self.templates.get(pathway_id)
            if not template:
                continue

            prefix = f"P{idx}_"
            pathway_label = template["title"]

            # 경로별 서브그래프
            pathway_sg = Subgraph(
                f"Pathway{idx}",
                f"경로 {idx+1}: {pathway_label}"
            )
            all_subgraphs.append(pathway_sg)

            first_node_id = None
            for node_data in template["nodes"][1:]:  # 첫 노드(성분) 제외
                node_id = f"{prefix}{node_data['id']}"
                if first_node_id is None:
                    first_node_id = node_id

                label = node_data["label"].replace("{ingredient}", ingredient)
                node = Node(
                    id=node_id,
                    label=label,
                    subgraph=f"Pathway{idx}",
                    style={"type": node_data.get("style", "default")}
                )
                all_nodes.append(node)

            # 입력 노드에서 경로의 첫 노드로 연결
            if first_node_id:
                all_edges.append(Edge("A0", first_node_id))

            # 경로 내 연결
            for edge_data in template["edges"]:
                if edge_data["source"] == "A":  # 성분 노드 연결은 이미 처리
                    continue
                all_edges.append(Edge(
                    f"{prefix}{edge_data['source']}",
                    f"{prefix}{edge_data['target']}",
                    edge_data.get("label", "")
                ))

        code = self._build_mermaid_code(
            all_nodes, all_edges, all_subgraphs, direction, language
        )

        return DiagramResult(
            ingredient=ingredient,
            mechanism_type="combined",
            diagram_type=DiagramType.FLOWCHART,
            code=code,
            language=language,
            nodes=all_nodes,
            edges=all_edges,
            subgraphs=all_subgraphs,
            style=self.style,
            title=f"{ingredient} 다중 작용 메커니즘",
            description="통합 메커니즘 다이어그램"
        )

    # === 효능별 특화 메서드 ===

    def generate_whitening_pathway(
        self,
        ingredient: str,
        pathway_type: str = "tyrosinase_inhibition",
        language: str = "ko"
    ) -> DiagramResult:
        """미백 경로 다이어그램"""
        if pathway_type == "tyrosinase_inhibition":
            return self.from_template("tyrosinase_inhibition", ingredient, language)
        elif pathway_type == "melanin_transfer":
            return self.from_template("melanin_transfer_block", ingredient, language)
        else:
            return self.from_template("tyrosinase_inhibition", ingredient, language)

    def generate_antiaging_pathway(
        self,
        ingredient: str,
        pathway_type: str = "collagen_synthesis",
        language: str = "ko"
    ) -> DiagramResult:
        """항노화 경로 다이어그램"""
        if pathway_type == "collagen_synthesis":
            return self.from_template("collagen_synthesis", ingredient, language)
        elif pathway_type == "mmp_inhibition":
            return self.from_template("mmp_inhibition", ingredient, language)
        elif pathway_type == "retinoid":
            return self.from_template("retinoid_signaling", ingredient, language)
        else:
            return self.from_template("collagen_synthesis", ingredient, language)

    def generate_antioxidant_pathway(
        self,
        ingredient: str,
        include_regeneration: bool = True,
        language: str = "ko"
    ) -> DiagramResult:
        """항산화 경로 다이어그램"""
        return self.from_template("antioxidant_network", ingredient, language)

    def generate_barrier_pathway(
        self,
        ingredient: str,
        pathway_type: str = "lipid_synthesis",
        language: str = "ko"
    ) -> DiagramResult:
        """장벽 강화 경로 다이어그램"""
        return self.from_template("barrier_lipid", ingredient, language)

    def generate_soothing_pathway(
        self,
        ingredient: str,
        language: str = "ko"
    ) -> DiagramResult:
        """진정 경로 다이어그램"""
        return self.from_template("anti_inflammatory", ingredient, language)

    # === 고급 기능 ===

    def generate_comparison(
        self,
        ingredients: List[str],
        efficacy: str,
        language: str = "ko"
    ) -> DiagramResult:
        """성분 비교 다이어그램"""

        efficacy_map = {
            "whitening": "tyrosinase_inhibition",
            "antiaging": "collagen_synthesis",
            "antioxidant": "antioxidant_network",
            "moisturizing": "barrier_lipid",
            "soothing": "anti_inflammatory",
        }

        template_id = efficacy_map.get(efficacy, "tyrosinase_inhibition")
        template = self.templates.get(template_id)

        if not template:
            raise ValueError(f"Unknown efficacy: {efficacy}")

        # 비교 다이어그램 생성
        lines = ["graph TD"]

        # 각 성분별 입력 노드
        for idx, ing in enumerate(ingredients):
            lines.append(f"    A{idx}[{ing}]")

        # 공통 타겟
        lines.append("    B[공통 타겟]")
        lines.append("    C[효과]")

        # 연결
        for idx in range(len(ingredients)):
            lines.append(f"    A{idx} --> B")
        lines.append("    B --> C")

        # 스타일
        for idx in range(len(ingredients)):
            lines.append(f"    style A{idx} fill:{self.style.input_color}")
        lines.append(f"    style C fill:{self.style.output_color}")

        code = "\n".join(lines)

        return DiagramResult(
            ingredient=", ".join(ingredients),
            mechanism_type=f"comparison_{efficacy}",
            diagram_type=DiagramType.FLOWCHART,
            code=code,
            language=language,
            nodes=[],
            edges=[],
            subgraphs=[],
            style=self.style,
            title=f"{efficacy} 성분 비교",
            description=f"{', '.join(ingredients)} 비교 분석"
        )

    def generate_synergy(
        self,
        ingredients: List[str],
        synergy_type: str = "antioxidant_network",
        language: str = "ko"
    ) -> DiagramResult:
        """시너지 다이어그램"""

        lines = ["graph TD"]
        lines.append('    subgraph Input["🧴 시너지 성분"]')

        for idx, ing in enumerate(ingredients):
            lines.append(f"        A{idx}[{ing}]")
        lines.append("    end")

        lines.append('    subgraph Synergy["🔗 시너지 효과"]')
        lines.append("        B[상호작용]")
        lines.append("        C[증폭 효과]")
        lines.append("    end")

        lines.append('    subgraph Clinical["✨ 결과"]')
        lines.append("        D[향상된 효능]")
        lines.append("    end")

        for idx in range(len(ingredients)):
            lines.append(f"    A{idx} --> B")
        lines.append("    B --> C")
        lines.append("    C --> D")

        for idx in range(len(ingredients)):
            lines.append(f"    style A{idx} fill:{self.style.input_color}")
        lines.append(f"    style D fill:{self.style.output_color}")

        code = "\n".join(lines)

        return DiagramResult(
            ingredient=", ".join(ingredients),
            mechanism_type=f"synergy_{synergy_type}",
            diagram_type=DiagramType.FLOWCHART,
            code=code,
            language=language,
            nodes=[],
            edges=[],
            subgraphs=[],
            style=self.style,
            title="성분 시너지 효과",
            description=f"{', '.join(ingredients)} 시너지 분석"
        )


# ============================================================
# 유틸리티 함수
# ============================================================

def get_available_templates() -> List[str]:
    """사용 가능한 템플릿 목록"""
    return list(PATHWAY_TEMPLATES.keys())


def get_template_info(template_id: str) -> Optional[Dict]:
    """템플릿 정보 조회"""
    template = PATHWAY_TEMPLATES.get(template_id)
    if template:
        return {
            "id": template_id,
            "title": template["title"],
            "title_en": template.get("title_en", ""),
            "description": template.get("description", ""),
            "node_count": len(template["nodes"]),
            "edge_count": len(template["edges"]),
        }
    return None


def get_ingredient_pathways(ingredient: str) -> List[str]:
    """성분에 매핑된 경로 목록"""
    return INGREDIENT_PATHWAY_MAP.get(ingredient.lower().strip(), [])


# ============================================================
# 메인 실행
# ============================================================

if __name__ == "__main__":
    # 테스트 실행
    generator = DiagramGenerator()

    # Niacinamide 다이어그램
    result = generator.generate("Niacinamide", mechanism_type="primary")
    print("=== Niacinamide Primary Mechanism ===")
    print(result.to_markdown())
    print()

    # Retinol 다이어그램
    result = generator.generate("Retinol", mechanism_type="primary")
    print("=== Retinol Primary Mechanism ===")
    print(result.to_markdown())
    print()

    # 비교 다이어그램
    result = generator.generate_comparison(
        ingredients=["Vitamin C", "Arbutin", "Niacinamide"],
        efficacy="whitening"
    )
    print("=== Whitening Comparison ===")
    print(result.to_markdown())
