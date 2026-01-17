#!/usr/bin/env python3
"""
KFDA Functional Cosmetic Ingredient Query Client

한국 식약처(MFDS) 기능성 화장품 고시원료 조회 클라이언트

Usage:
    from kfda_query import KFDAClient

    client = KFDAClient()

    # 미백 원료 검색
    whitening = client.search_whitening("나이아신아마이드")

    # 주름개선 원료 검색
    wrinkle = client.search_wrinkle("레티놀")

    # 자외선차단 원료 검색
    sunscreen = client.search_sunscreen("징크옥사이드")

    # 농도 확인
    is_valid = client.check_concentration_limit("나이아신아마이드", 3.0, "whitening")

    # 처방 검증
    result = client.verify_functional_formula(formula_dict)
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple
from enum import Enum


class FunctionalType(Enum):
    """기능성 유형"""
    WHITENING = "미백"
    WRINKLE = "주름개선"
    SUNSCREEN = "자외선차단"


class ApprovalType(Enum):
    """심사 유형"""
    REPORT = "보고"  # 고시원료, 고시농도
    REVIEW = "심사"  # 고시외 원료 또는 농도 초과


@dataclass
class FunctionalIngredient:
    """기능성 원료 정보"""
    korean_name: str
    inci_name: str
    cas_number: Optional[str]
    functional_type: FunctionalType
    min_concentration: Optional[float]  # 최소 농도 (%)
    max_concentration: float  # 최대 농도 (%) or IU/g
    concentration_unit: str = "%"  # "%" or "IU/g"
    mechanism: Optional[str] = None
    stability_notes: Optional[str] = None
    incompatible_with: List[str] = field(default_factory=list)
    special_notes: Optional[str] = None


# ============================================================
# 미백 기능성 고시원료 데이터베이스 (22종)
# ============================================================

WHITENING_INGREDIENTS: Dict[str, FunctionalIngredient] = {
    "나이아신아마이드": FunctionalIngredient(
        korean_name="나이아신아마이드",
        inci_name="Niacinamide",
        cas_number="98-92-0",
        functional_type=FunctionalType.WHITENING,
        min_concentration=2.0,
        max_concentration=5.0,
        mechanism="타이로시나제 억제, 멜라노좀 전이 억제",
        stability_notes="pH 5~7에서 안정, 순수 비타민C와 동시 사용 시 니코틴산 생성 가능",
        incompatible_with=["L-Ascorbic Acid (동시 사용 시 자극 가능)"]
    ),
    "알부틴": FunctionalIngredient(
        korean_name="알부틴",
        inci_name="Arbutin",
        cas_number="497-76-7",
        functional_type=FunctionalType.WHITENING,
        min_concentration=2.0,
        max_concentration=5.0,
        mechanism="타이로시나제 경쟁적 억제",
        stability_notes="pH 5~7 권장, 산성 조건에서 가수분해 → 하이드로퀴논 생성"
    ),
    "에칠아스코빌에텔": FunctionalIngredient(
        korean_name="에칠아스코빌에텔",
        inci_name="3-O-Ethyl Ascorbic Acid",
        cas_number="86404-04-8",
        functional_type=FunctionalType.WHITENING,
        min_concentration=1.0,
        max_concentration=2.0,
        mechanism="비타민C 안정화 유도체, 타이로시나제 억제",
        stability_notes="pH 4~6에서 안정, 친유성으로 피부 침투력 우수"
    ),
    "아스코빌글루코사이드": FunctionalIngredient(
        korean_name="아스코빌글루코사이드",
        inci_name="Ascorbyl Glucoside",
        cas_number="129499-78-1",
        functional_type=FunctionalType.WHITENING,
        min_concentration=None,
        max_concentration=2.0,
        mechanism="피부 내 효소에 의해 활성형 비타민C로 전환",
        stability_notes="pH 6~7에서 최적 안정성, 열에 안정"
    ),
    "마그네슘아스코빌포스페이트": FunctionalIngredient(
        korean_name="마그네슘아스코빌포스페이트",
        inci_name="Magnesium Ascorbyl Phosphate",
        cas_number="113170-55-1",
        functional_type=FunctionalType.WHITENING,
        min_concentration=None,
        max_concentration=3.0,
        mechanism="수용성 비타민C 유도체",
        stability_notes="pH 7 근처에서 안정, 금속 이온 킬레이트제 병용 권장"
    ),
    "아스코빌테트라이소팔미테이트": FunctionalIngredient(
        korean_name="아스코빌테트라이소팔미테이트",
        inci_name="Ascorbyl Tetraisopalmitate",
        cas_number="183476-82-6",
        functional_type=FunctionalType.WHITENING,
        min_concentration=None,
        max_concentration=2.0,
        mechanism="지용성 비타민C 유도체, 피부 침투력 우수",
        stability_notes="오일상에 용해, 산화 방지제 병용 권장"
    ),
    "소듐아스코빌포스페이트": FunctionalIngredient(
        korean_name="소듐아스코빌포스페이트",
        inci_name="Sodium Ascorbyl Phosphate",
        cas_number="66170-10-3",
        functional_type=FunctionalType.WHITENING,
        min_concentration=None,
        max_concentration=3.0,
        mechanism="수용성 비타민C 유도체, 항균 작용"
    ),
    "유용성감초추출물": FunctionalIngredient(
        korean_name="유용성감초추출물",
        inci_name="Glycyrrhiza Glabra (Licorice) Root Extract",
        cas_number="59870-68-7",
        functional_type=FunctionalType.WHITENING,
        min_concentration=0.05,
        max_concentration=0.1,
        mechanism="글라브리딘 함유, 타이로시나제 억제",
        stability_notes="글라브리딘으로서 농도 기준, 유용성으로 오일상에 용해",
        special_notes="글라브리딘으로서 0.05~0.1%"
    ),
    "닥나무추출물": FunctionalIngredient(
        korean_name="닥나무추출물",
        inci_name="Broussonetia Kazinoki Root Extract",
        cas_number=None,
        functional_type=FunctionalType.WHITENING,
        min_concentration=None,
        max_concentration=2.0,
        mechanism="타이로시나제 억제"
    ),
    "알파-비사보롤": FunctionalIngredient(
        korean_name="알파-비사보롤",
        inci_name="Bisabolol",
        cas_number="23089-26-1",
        functional_type=FunctionalType.WHITENING,
        min_concentration=None,
        max_concentration=0.5,
        mechanism="캐모마일 유래, 항염 + 미백 효과",
        stability_notes="지용성"
    ),
    "아스코빌팔미테이트": FunctionalIngredient(
        korean_name="아스코빌팔미테이트",
        inci_name="Ascorbyl Palmitate",
        cas_number="137-66-6",
        functional_type=FunctionalType.WHITENING,
        min_concentration=None,
        max_concentration=2.0,
        mechanism="지용성 비타민C 유도체"
    ),
    "디옥시알부틴": FunctionalIngredient(
        korean_name="디옥시알부틴",
        inci_name="Deoxyarbutin",
        cas_number="53936-56-4",
        functional_type=FunctionalType.WHITENING,
        min_concentration=None,
        max_concentration=3.0,
        mechanism="알부틴 탈산소 유도체, 강화된 미백 효과"
    ),
    "4-부틸레조시놀": FunctionalIngredient(
        korean_name="4-부틸레조시놀",
        inci_name="4-Butylresorcinol",
        cas_number="18979-61-8",
        functional_type=FunctionalType.WHITENING,
        min_concentration=None,
        max_concentration=0.5,
        mechanism="강력한 타이로시나제 억제, TRP-1/TRP-2 억제"
    ),
    "운데실레노일페닐알라닌": FunctionalIngredient(
        korean_name="운데실레노일페닐알라닌",
        inci_name="Undecylenoyl Phenylalanine",
        cas_number="175357-18-3",
        functional_type=FunctionalType.WHITENING,
        min_concentration=None,
        max_concentration=2.0,
        mechanism="α-MSH 길항제, 멜라노사이트 신호전달 억제"
    ),
    "트라넥사믹애씨드": FunctionalIngredient(
        korean_name="트라넥사믹애씨드",
        inci_name="Tranexamic Acid",
        cas_number="1197-18-8",
        functional_type=FunctionalType.WHITENING,
        min_concentration=2.0,
        max_concentration=3.0,
        mechanism="플라스민 억제로 멜라닌 생성 억제",
        stability_notes="pH 4~8에서 안정"
    ),
    "택시폴린": FunctionalIngredient(
        korean_name="택시폴린",
        inci_name="Taxifolin",
        cas_number="480-18-2",
        functional_type=FunctionalType.WHITENING,
        min_concentration=None,
        max_concentration=0.1,
        mechanism="플라보노이드 계열, 항산화 + 미백",
        special_notes="택시폴린으로서 0.1%"
    ),
    "에틸페록시디하이드로사이클리그난": FunctionalIngredient(
        korean_name="에틸페록시디하이드로사이클리그난",
        inci_name="Ethyl 4-Hydroxydihydrocinnamate",
        cas_number=None,
        functional_type=FunctionalType.WHITENING,
        min_concentration=None,
        max_concentration=1.5
    ),
    "아스코빌메틸실란올펙테이트": FunctionalIngredient(
        korean_name="아스코빌메틸실란올펙테이트",
        inci_name="Ascorbyl Methylsilanol Pectinate",
        cas_number=None,
        functional_type=FunctionalType.WHITENING,
        min_concentration=None,
        max_concentration=3.0,
        mechanism="실리콘 결합 비타민C 유도체"
    ),
    "메틸젠틴산에스터및칼슘판토테네이트혼합물": FunctionalIngredient(
        korean_name="메틸젠틴산에스터 및 칼슘판토테네이트 혼합물",
        inci_name="Methyl Gentisate + Calcium Pantothenate",
        cas_number=None,
        functional_type=FunctionalType.WHITENING,
        min_concentration=None,
        max_concentration=0.75,
        special_notes="메틸젠틴산에스터 0.3% + 칼슘판토테네이트 0.45% 혼합물"
    ),
    "화이트루핀추출물": FunctionalIngredient(
        korean_name="화이트루핀추출물",
        inci_name="Lupinus Albus Seed Extract",
        cas_number=None,
        functional_type=FunctionalType.WHITENING,
        min_concentration=None,
        max_concentration=2.0,
        mechanism="펩타이드 성분 함유"
    ),
    "뽕나무추출물": FunctionalIngredient(
        korean_name="뽕나무추출물",
        inci_name="Morus Alba Root Extract",
        cas_number=None,
        functional_type=FunctionalType.WHITENING,
        min_concentration=None,
        max_concentration=2.0,
        mechanism="모루신 등 활성 성분, 타이로시나제 억제"
    ),
    "3-에톡시아스코빅애씨드": FunctionalIngredient(
        korean_name="3-에톡시아스코빅애씨드",
        inci_name="3-O-Ethyl Ascorbic Acid",
        cas_number="86404-04-8",
        functional_type=FunctionalType.WHITENING,
        min_concentration=1.0,
        max_concentration=2.0,
        special_notes="에칠아스코빌에텔과 동일 물질"
    ),
}


# ============================================================
# 주름개선 기능성 고시원료 데이터베이스 (6종)
# ============================================================

WRINKLE_INGREDIENTS: Dict[str, FunctionalIngredient] = {
    "레티놀": FunctionalIngredient(
        korean_name="레티놀",
        inci_name="Retinol",
        cas_number="68-26-8",
        functional_type=FunctionalType.WRINKLE,
        min_concentration=None,
        max_concentration=2500,
        concentration_unit="IU/g",
        mechanism="세포 분화 및 재생 촉진, 콜라겐 합성 증가",
        stability_notes="광안정성 불안정, 산소 민감, 열 민감, pH 민감(산성 불안정)",
        incompatible_with=["AHA", "BHA", "Vitamin C (순수형)"],
        special_notes="야간 사용 권장, 차광 용기 필수, 임산부 사용 자제"
    ),
    "레티닐팔미테이트": FunctionalIngredient(
        korean_name="레티닐팔미테이트",
        inci_name="Retinyl Palmitate",
        cas_number="79-81-2",
        functional_type=FunctionalType.WRINKLE,
        min_concentration=None,
        max_concentration=10000,
        concentration_unit="IU/g",
        mechanism="피부 내에서 레티놀로 전환",
        stability_notes="레티놀보다 안정적, 차광 용기 권장"
    ),
    "아데노신": FunctionalIngredient(
        korean_name="아데노신",
        inci_name="Adenosine",
        cas_number="58-61-7",
        functional_type=FunctionalType.WRINKLE,
        min_concentration=None,
        max_concentration=0.04,
        mechanism="세포 에너지 공급, 콜라겐 합성, 항염 효과",
        stability_notes="넓은 pH 범위에서 안정(4~9), 열에 안정적",
        special_notes="민감성 피부 적합, 임산부 사용 가능, 주간 사용 가능"
    ),
    "폴리에톡실레이티드레틴아마이드": FunctionalIngredient(
        korean_name="폴리에톡실레이티드레틴아마이드",
        inci_name="Polyethoxylated Retinamide",
        cas_number=None,
        functional_type=FunctionalType.WRINKLE,
        min_concentration=0.05,
        max_concentration=0.1,
        mechanism="레티노이드 수용체 활성화",
        stability_notes="수용성, 레티놀 대비 안정성 향상"
    ),
    "레티닐아세테이트": FunctionalIngredient(
        korean_name="레티닐아세테이트",
        inci_name="Retinyl Acetate",
        cas_number="127-47-9",
        functional_type=FunctionalType.WRINKLE,
        min_concentration=None,
        max_concentration=5500,
        concentration_unit="IU/g",
        mechanism="피부 침투 후 레티놀로 전환",
        stability_notes="지용성, 빛에 민감, 산화 방지제 병용 권장"
    ),
    "레티닐프로피오네이트": FunctionalIngredient(
        korean_name="레티닐프로피오네이트",
        inci_name="Retinyl Propionate",
        cas_number="7069-42-3",
        functional_type=FunctionalType.WRINKLE,
        min_concentration=None,
        max_concentration=5500,
        concentration_unit="IU/g",
        mechanism="피부 침투 후 레티놀로 전환"
    ),
}


# ============================================================
# 자외선차단 기능성 고시원료 데이터베이스 (28종)
# ============================================================

SUNSCREEN_INGREDIENTS: Dict[str, FunctionalIngredient] = {
    # 무기 자외선차단제
    "징크옥사이드": FunctionalIngredient(
        korean_name="징크옥사이드",
        inci_name="Zinc Oxide",
        cas_number="1314-13-2",
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=25.0,
        mechanism="물리적 반사/산란 (UVA+UVB 광범위)",
        stability_notes="광안정성 우수, 나노 원료 사용 시 [나노] 표시 필수",
        special_notes="항염/진정 효과, 여드름 피부 적합"
    ),
    "티타늄디옥사이드": FunctionalIngredient(
        korean_name="티타늄디옥사이드",
        inci_name="Titanium Dioxide",
        cas_number="13463-67-7",
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=25.0,
        mechanism="물리적 반사/산란 (UVB>UVA)",
        stability_notes="광안정성 우수, 코팅 처리로 광촉매 활성 억제"
    ),

    # UVB 필터
    "옥틸메톡시신나메이트": FunctionalIngredient(
        korean_name="옥틸메톡시신나메이트",
        inci_name="Ethylhexyl Methoxycinnamate",
        cas_number="5466-77-3",
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=7.5,
        mechanism="UVB 흡수 (311nm)",
        stability_notes="광안정성 낮음 (단독 사용 시), 아보벤존과 병용 시 안정화제 필요",
        special_notes="하와이, 팔라우 등에서 사용 규제"
    ),
    "옥토크릴렌": FunctionalIngredient(
        korean_name="옥토크릴렌",
        inci_name="Octocrylene",
        cas_number="6197-30-4",
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=10.0,
        mechanism="UVB 차단 + 광안정화제 역할 (303nm)",
        stability_notes="광안정성 우수, 아보벤존 안정화 효과"
    ),
    "에칠헥실살리실레이트": FunctionalIngredient(
        korean_name="에칠헥실살리실레이트",
        inci_name="Ethylhexyl Salicylate",
        cas_number="118-60-5",
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=5.0,
        mechanism="UVB 흡수 (307nm)"
    ),
    "호모살레이트": FunctionalIngredient(
        korean_name="호모살레이트",
        inci_name="Homosalate",
        cas_number="118-56-9",
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=10.0,
        mechanism="UVB 흡수 (306nm)"
    ),
    "4-메틸벤질리덴캠퍼": FunctionalIngredient(
        korean_name="4-메틸벤질리덴캠퍼",
        inci_name="4-Methylbenzylidene Camphor",
        cas_number="36861-47-9",
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=4.0,
        mechanism="UVB 흡수 (300nm)"
    ),
    "디갈로일트리올리에이트": FunctionalIngredient(
        korean_name="디갈로일트리올리에이트",
        inci_name="Diethylhexyl Butamido Triazone",
        cas_number="154702-15-5",
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=10.0,
        mechanism="UVB 흡수 (312nm)",
        stability_notes="고분자량, 피부 침투 적음, 광안정성 우수"
    ),
    "에칠헥실트리아존": FunctionalIngredient(
        korean_name="에칠헥실트리아존",
        inci_name="Ethylhexyl Triazone",
        cas_number="88122-99-0",
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=5.0,
        mechanism="UVB 흡수 (314nm)",
        stability_notes="높은 흡광 계수, 광안정성 우수"
    ),
    "폴리실리콘-15": FunctionalIngredient(
        korean_name="폴리실리콘-15",
        inci_name="Polysilicone-15",
        cas_number=None,
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=10.0,
        mechanism="UVB 흡수",
        stability_notes="실리콘 결합 UV 필터, 내수성 우수"
    ),
    "페닐벤지미다졸설포닉애씨드": FunctionalIngredient(
        korean_name="페닐벤지미다졸설포닉애씨드",
        inci_name="Phenylbenzimidazole Sulfonic Acid",
        cas_number="27503-81-7",
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=4.0,
        mechanism="UVB 흡수 (302nm)",
        special_notes="산으로서 4%"
    ),
    "벤조페논-3": FunctionalIngredient(
        korean_name="벤조페논-3",
        inci_name="Oxybenzone",
        cas_number="131-57-7",
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=5.0,
        mechanism="UVB+UVA 흡수 (288, 325nm)",
        special_notes="환경 규제 증가 추세"
    ),
    "벤조페논-4": FunctionalIngredient(
        korean_name="벤조페논-4",
        inci_name="Benzophenone-4",
        cas_number="4065-45-6",
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=5.0,
        mechanism="UVB+UVA 흡수"
    ),
    "벤조페논-8": FunctionalIngredient(
        korean_name="벤조페논-8",
        inci_name="Benzophenone-8",
        cas_number="131-53-3",
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=3.0
    ),
    "PABA": FunctionalIngredient(
        korean_name="PABA",
        inci_name="4-Aminobenzoic Acid",
        cas_number="150-13-0",
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=4.0,
        mechanism="UVB 흡수 (283nm)",
        special_notes="알레르기 반응 가능성, 현재 거의 미사용"
    ),
    "시녹세이트": FunctionalIngredient(
        korean_name="시녹세이트",
        inci_name="Cinoxate",
        cas_number="104-28-9",
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=3.0,
        mechanism="UVB 흡수 (289nm)"
    ),

    # UVA 필터
    "아보벤존": FunctionalIngredient(
        korean_name="아보벤존",
        inci_name="Butyl Methoxydibenzoylmethane",
        cas_number="70356-09-1",
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=3.0,
        mechanism="UVA1 흡수 (360nm) - 가장 효과적인 UVA1 필터",
        stability_notes="광안정성 매우 낮음, 옥토크릴렌/비스에칠헥실옥시페놀메톡시페닐트리아진과 병용 필수",
        incompatible_with=["옥틸메톡시신나메이트 (단독 사용 시)"]
    ),
    "드로메트리졸트리실록산": FunctionalIngredient(
        korean_name="드로메트리졸트리실록산",
        inci_name="Drometrizole Trisiloxane",
        cas_number="155633-54-8",
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=15.0,
        mechanism="UVA+UVB 광범위 차단 (303, 344nm)",
        stability_notes="실리콘 결합, 광안정성 우수",
        special_notes="Mexoryl XL"
    ),
    "테레프탈릴리덴디캠퍼설포닉애씨드": FunctionalIngredient(
        korean_name="테레프탈릴리덴디캠퍼설포닉애씨드",
        inci_name="Terephthalylidene Dicamphor Sulfonic Acid",
        cas_number="90457-82-2",
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=10.0,
        mechanism="UVA2 흡수 (345nm)",
        stability_notes="수용성, 광안정성 우수",
        special_notes="Mexoryl SX, 산으로서 10%"
    ),
    "디에칠아미노히드록시벤조일헥실벤조에이트": FunctionalIngredient(
        korean_name="디에칠아미노히드록시벤조일헥실벤조에이트",
        inci_name="Diethylamino Hydroxybenzoyl Hexyl Benzoate",
        cas_number="302776-68-7",
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=10.0,
        mechanism="UVA 흡수 (354nm)",
        stability_notes="광안정성 우수, 아보벤존 안정화",
        special_notes="Uvinul A Plus"
    ),
    "비스에칠헥실옥시페놀메톡시페닐트리아진": FunctionalIngredient(
        korean_name="비스에칠헥실옥시페놀메톡시페닐트리아진",
        inci_name="Bis-Ethylhexyloxyphenol Methoxyphenyl Triazine",
        cas_number="187393-00-6",
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=10.0,
        mechanism="UVA+UVB 광범위 차단 (310, 343nm)",
        stability_notes="뛰어난 광안정성, 다른 UV 필터 안정화",
        special_notes="Tinosorb S, 고분자량으로 피부 침투 적음"
    ),
    "메칠렌비스벤조트리아졸릴테트라메칠부틸페놀": FunctionalIngredient(
        korean_name="메칠렌비스벤조트리아졸릴테트라메칠부틸페놀",
        inci_name="Methylene Bis-Benzotriazolyl Tetramethylbutylphenol",
        cas_number="103597-45-1",
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=10.0,
        mechanism="UVA+UVB 광범위 차단 (흡수+반사/산란)",
        stability_notes="유기/무기 하이브리드 필터",
        special_notes="Tinosorb M"
    ),
    "디소듐페닐디벤지미다졸테트라설포네이트": FunctionalIngredient(
        korean_name="디소듐페닐디벤지미다졸테트라설포네이트",
        inci_name="Disodium Phenyl Dibenzimidazole Tetrasulfonate",
        cas_number="180898-37-7",
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=10.0,
        mechanism="UVA 흡수"
    ),
    "이소프로필디벤조일메탄": FunctionalIngredient(
        korean_name="이소프로필디벤조일메탄",
        inci_name="Isopropyl Dibenzoylmethane",
        cas_number="63250-25-9",
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=5.0,
        mechanism="UVA 흡수"
    ),
    "에칠헥실디메톡시벤질리덴디옥소이미다졸린프로피오네이트": FunctionalIngredient(
        korean_name="에칠헥실디메톡시벤질리덴디옥소이미다졸린프로피오네이트",
        inci_name="Ethylhexyl Dimethoxybenzylidene Dioxoimidazolidine Propionate",
        cas_number=None,
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=3.0,
        mechanism="UVA 흡수"
    ),
    "폴리아크릴아미도메틸벤질리덴캠퍼": FunctionalIngredient(
        korean_name="폴리아크릴아미도메틸벤질리덴캠퍼",
        inci_name="Polyacrylamidomethyl Benzylidene Camphor",
        cas_number=None,
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=6.0,
        mechanism="UVA 흡수"
    ),
    "에칠헥실메톡시크릴렌": FunctionalIngredient(
        korean_name="에칠헥실메톡시크릴렌",
        inci_name="Ethylhexyl Methoxycrylene",
        cas_number=None,
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=8.0,
        mechanism="UVA 흡수"
    ),
    "디에칠헥실시린길리덴디말로네이트": FunctionalIngredient(
        korean_name="디에칠헥실시린길리덴디말로네이트",
        inci_name="Diethylhexyl Syringylidenemalonate",
        cas_number=None,
        functional_type=FunctionalType.SUNSCREEN,
        min_concentration=None,
        max_concentration=10.0,
        mechanism="광안정화제 (다른 UV 필터 안정화)"
    ),
}


# ============================================================
# KFDA Client Class
# ============================================================

class KFDAClient:
    """KFDA 기능성 화장품 원료 조회 클라이언트"""

    def __init__(self):
        self.whitening = WHITENING_INGREDIENTS
        self.wrinkle = WRINKLE_INGREDIENTS
        self.sunscreen = SUNSCREEN_INGREDIENTS

    def search_whitening(self, query: str) -> List[FunctionalIngredient]:
        """미백 기능성 원료 검색

        Args:
            query: 검색어 (한글명, INCI명, CAS 번호)

        Returns:
            검색 결과 리스트
        """
        return self._search_database(self.whitening, query)

    def search_wrinkle(self, query: str) -> List[FunctionalIngredient]:
        """주름개선 기능성 원료 검색

        Args:
            query: 검색어 (한글명, INCI명, CAS 번호)

        Returns:
            검색 결과 리스트
        """
        return self._search_database(self.wrinkle, query)

    def search_sunscreen(self, query: str) -> List[FunctionalIngredient]:
        """자외선차단 기능성 원료 검색

        Args:
            query: 검색어 (한글명, INCI명, CAS 번호)

        Returns:
            검색 결과 리스트
        """
        return self._search_database(self.sunscreen, query)

    def search_all(self, query: str) -> Dict[str, List[FunctionalIngredient]]:
        """전체 기능성 원료 검색

        Args:
            query: 검색어

        Returns:
            기능성 유형별 검색 결과
        """
        return {
            "whitening": self.search_whitening(query),
            "wrinkle": self.search_wrinkle(query),
            "sunscreen": self.search_sunscreen(query)
        }

    def _search_database(
        self,
        database: Dict[str, FunctionalIngredient],
        query: str
    ) -> List[FunctionalIngredient]:
        """데이터베이스 검색"""
        query = query.lower().strip()
        results = []

        for key, ingredient in database.items():
            if (query in key.lower() or
                query in ingredient.inci_name.lower() or
                (ingredient.cas_number and query in ingredient.cas_number)):
                results.append(ingredient)

        return results

    def check_concentration_limit(
        self,
        ingredient_name: str,
        concentration: float,
        functional_type: str
    ) -> Dict[str, any]:
        """농도 기준 충족 여부 확인

        Args:
            ingredient_name: 원료명
            concentration: 배합 농도
            functional_type: 기능성 유형 ("whitening", "wrinkle", "sunscreen")

        Returns:
            검증 결과 딕셔너리
        """
        database_map = {
            "whitening": self.whitening,
            "wrinkle": self.wrinkle,
            "sunscreen": self.sunscreen
        }

        database = database_map.get(functional_type.lower())
        if not database:
            return {"valid": False, "error": f"Unknown functional type: {functional_type}"}

        ingredient = database.get(ingredient_name)
        if not ingredient:
            # 검색으로 찾기
            results = self._search_database(database, ingredient_name)
            if not results:
                return {"valid": False, "error": f"Ingredient not found: {ingredient_name}"}
            ingredient = results[0]

        min_conc = ingredient.min_concentration or 0
        max_conc = ingredient.max_concentration
        unit = ingredient.concentration_unit

        is_valid = min_conc <= concentration <= max_conc

        return {
            "valid": is_valid,
            "ingredient": ingredient.korean_name,
            "inci_name": ingredient.inci_name,
            "input_concentration": concentration,
            "min_concentration": min_conc,
            "max_concentration": max_conc,
            "unit": unit,
            "approval_type": ApprovalType.REPORT.value if is_valid else ApprovalType.REVIEW.value,
            "message": (
                f"고시 농도 범위 내 ({min_conc}~{max_conc}{unit}) - 보고 대상" if is_valid
                else f"고시 농도 범위 초과 - 심사 대상 (최대 {max_conc}{unit})"
            )
        }

    def verify_functional_formula(
        self,
        formula: Dict[str, Dict[str, float]]
    ) -> Dict[str, any]:
        """처방의 기능성 규제 적합성 검증

        Args:
            formula: 처방 딕셔너리
                {
                    "whitening": {"나이아신아마이드": 3.0, "알부틴": 2.0},
                    "wrinkle": {"아데노신": 0.04},
                    "sunscreen": {"징크옥사이드": 15.0}
                }

        Returns:
            검증 결과 딕셔너리
        """
        results = {
            "overall_valid": True,
            "overall_approval_type": ApprovalType.REPORT.value,
            "functional_types": [],
            "ingredients": [],
            "issues": []
        }

        for func_type, ingredients in formula.items():
            if func_type not in ["whitening", "wrinkle", "sunscreen"]:
                results["issues"].append(f"Unknown functional type: {func_type}")
                continue

            results["functional_types"].append(func_type)

            for ingredient_name, concentration in ingredients.items():
                check_result = self.check_concentration_limit(
                    ingredient_name, concentration, func_type
                )

                results["ingredients"].append({
                    "name": ingredient_name,
                    "type": func_type,
                    "concentration": concentration,
                    **check_result
                })

                if not check_result.get("valid", False):
                    results["overall_valid"] = False
                    results["overall_approval_type"] = ApprovalType.REVIEW.value
                    results["issues"].append(check_result.get("message", "Invalid concentration"))

        # 복합 기능성 여부 확인
        if len(results["functional_types"]) > 1:
            results["is_multi_functional"] = True
            results["multi_functional_types"] = results["functional_types"]
        else:
            results["is_multi_functional"] = False

        return results

    def get_all_whitening(self) -> List[FunctionalIngredient]:
        """미백 고시원료 전체 목록"""
        return list(self.whitening.values())

    def get_all_wrinkle(self) -> List[FunctionalIngredient]:
        """주름개선 고시원료 전체 목록"""
        return list(self.wrinkle.values())

    def get_all_sunscreen(self) -> List[FunctionalIngredient]:
        """자외선차단 고시원료 전체 목록"""
        return list(self.sunscreen.values())

    def get_incompatible_pairs(self, ingredient_name: str) -> List[str]:
        """배합 금기 성분 조회

        Args:
            ingredient_name: 원료명

        Returns:
            배합 금기 성분 리스트
        """
        for db in [self.whitening, self.wrinkle, self.sunscreen]:
            if ingredient_name in db:
                return db[ingredient_name].incompatible_with

            # 검색으로 찾기
            for key, ingredient in db.items():
                if (ingredient_name.lower() in key.lower() or
                    ingredient_name.lower() in ingredient.inci_name.lower()):
                    return ingredient.incompatible_with

        return []


# ============================================================
# CLI Interface
# ============================================================

def main():
    """CLI 메인 함수"""
    import sys

    client = KFDAClient()

    if len(sys.argv) < 2:
        print("Usage: python kfda_query.py <command> [args]")
        print("\nCommands:")
        print("  search <query>           - 전체 검색")
        print("  whitening [query]        - 미백 원료 검색/목록")
        print("  wrinkle [query]          - 주름개선 원료 검색/목록")
        print("  sunscreen [query]        - 자외선차단 원료 검색/목록")
        print("  check <name> <conc> <type> - 농도 확인")
        return

    command = sys.argv[1]

    if command == "search" and len(sys.argv) >= 3:
        query = sys.argv[2]
        results = client.search_all(query)
        for func_type, ingredients in results.items():
            if ingredients:
                print(f"\n[{func_type.upper()}]")
                for ing in ingredients:
                    print(f"  - {ing.korean_name} ({ing.inci_name}): "
                          f"{ing.min_concentration or 0}~{ing.max_concentration}{ing.concentration_unit}")

    elif command == "whitening":
        if len(sys.argv) >= 3:
            results = client.search_whitening(sys.argv[2])
        else:
            results = client.get_all_whitening()

        print(f"\n미백 기능성 고시원료 ({len(results)}종)")
        for ing in results:
            print(f"  - {ing.korean_name} ({ing.inci_name}): "
                  f"{ing.min_concentration or 0}~{ing.max_concentration}%")

    elif command == "wrinkle":
        if len(sys.argv) >= 3:
            results = client.search_wrinkle(sys.argv[2])
        else:
            results = client.get_all_wrinkle()

        print(f"\n주름개선 기능성 고시원료 ({len(results)}종)")
        for ing in results:
            print(f"  - {ing.korean_name} ({ing.inci_name}): "
                  f"최대 {ing.max_concentration}{ing.concentration_unit}")

    elif command == "sunscreen":
        if len(sys.argv) >= 3:
            results = client.search_sunscreen(sys.argv[2])
        else:
            results = client.get_all_sunscreen()

        print(f"\n자외선차단 기능성 고시원료 ({len(results)}종)")
        for ing in results:
            print(f"  - {ing.korean_name} ({ing.inci_name}): "
                  f"최대 {ing.max_concentration}%")

    elif command == "check" and len(sys.argv) >= 5:
        name = sys.argv[2]
        conc = float(sys.argv[3])
        func_type = sys.argv[4]

        result = client.check_concentration_limit(name, conc, func_type)
        print(f"\n농도 검증 결과:")
        print(f"  원료: {result.get('ingredient', name)}")
        print(f"  배합 농도: {conc}")
        print(f"  고시 범위: {result.get('min_concentration', 0)}~{result.get('max_concentration')}{result.get('unit', '%')}")
        print(f"  적합 여부: {'적합' if result.get('valid') else '부적합'}")
        print(f"  심사 유형: {result.get('approval_type')}")

    else:
        print(f"Unknown command or missing arguments: {command}")


if __name__ == "__main__":
    main()
