#!/usr/bin/env python3
"""
UL Prospector Search Utility

화장품 원료 검색을 위한 UL Prospector 유틸리티.
WebFetch 및 WebSearch 도구와 함께 사용하도록 설계됨.

Author: EVAS Cosmetic
License: MIT
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime
import re
import json


class ProductCategory(Enum):
    """제품 카테고리"""
    PERSONAL_CARE = "PersonalCare"
    FOOD = "Food"
    COATINGS = "Coatings"
    ADHESIVES = "Adhesives"
    LUBRICANTS = "Lubricants"


class Region(Enum):
    """공급 지역"""
    NORTH_AMERICA = "na"
    EUROPE = "eu"
    ASIA_PACIFIC = "asia"
    LATIN_AMERICA = "latam"
    MIDDLE_EAST_AFRICA = "mea"


class FunctionCategory(Enum):
    """기능 카테고리"""
    # Actives
    ANTI_AGING = "Anti-Aging Actives"
    BRIGHTENING = "Skin Brightening"
    MOISTURIZING = "Moisturizing Actives"
    SOOTHING = "Soothing & Calming"

    # Emollients
    EMOLLIENT = "Emollients"
    HUMECTANT = "Humectants"
    NATURAL_OIL = "Natural Oils"
    SILICONE = "Silicones"

    # Surfactants
    SURFACTANT = "Surfactants"
    SURFACTANT_MILD = "Mild Surfactants"
    EMULSIFIER = "Emulsifiers"
    SOLUBILIZER = "Solubilizers"

    # Rheology
    THICKENER = "Thickeners"
    RHEOLOGY_MODIFIER = "Rheology Modifiers"
    FILM_FORMER = "Film Formers"

    # Sun Care
    UV_FILTER = "UV Filters"
    SUNSCREEN_ACTIVE = "Sunscreen Actives"

    # Preservation
    PRESERVATIVE = "Preservatives"
    ANTIOXIDANT = "Antioxidants"
    CHELATING = "Chelating Agents"

    # Hair Care
    HAIR_CONDITIONING = "Hair Conditioning"
    HAIR_STYLING = "Hair Styling"

    # Color
    COLORANT = "Colorants"
    FRAGRANCE = "Fragrances"


class Certification(Enum):
    """인증 유형"""
    COSMOS_ORGANIC = "COSMOS Organic"
    COSMOS_NATURAL = "COSMOS Natural"
    ECOCERT = "ECOCERT"
    NATRUE = "NATRUE"
    VEGAN = "Vegan"
    HALAL = "Halal"
    RSPO = "RSPO"
    CHINA_COMPLIANT = "China NMPA Compliant"


@dataclass
class SearchParams:
    """검색 파라미터"""
    keyword: str
    category: ProductCategory = ProductCategory.PERSONAL_CARE
    region: Region = Region.ASIA_PACIFIC
    function: Optional[FunctionCategory] = None
    chemistry: Optional[str] = None
    supplier: Optional[str] = None
    certifications: List[Certification] = field(default_factory=list)
    max_results: int = 20


@dataclass
class ProductResult:
    """제품 검색 결과"""
    product_id: str
    product_name: str
    trade_name: str
    supplier: str
    inci_name: str
    cas_number: Optional[str]
    functions: List[str]
    certifications: List[str]
    description: str
    url: str


@dataclass
class SupplierResult:
    """공급사 검색 결과"""
    supplier_id: str
    name: str
    headquarters: str
    product_count: int
    specialties: List[str]
    certifications: List[str]
    website: str
    contact_email: Optional[str]


@dataclass
class TechnicalDataSheet:
    """TDS 정보"""
    product_name: str
    trade_name: str
    supplier: str
    inci_name: str
    cas_number: Optional[str]

    # Physical Properties
    appearance: str
    color: str
    odor: str
    ph: Optional[str]
    viscosity: Optional[str]
    density: Optional[str]

    # Usage
    recommended_use_level: str
    applications: List[str]
    processing_guidelines: str

    # Regulatory
    regulatory_status: Dict[str, str]
    certifications: List[str]

    # Storage
    storage_conditions: str
    shelf_life: str


class ProspectorSearchBuilder:
    """
    UL Prospector 검색 URL 빌더

    WebFetch/WebSearch 도구와 함께 사용
    """

    BASE_URL = "https://www.ulprospector.com/en"

    def __init__(self, region: Region = Region.ASIA_PACIFIC):
        self.region = region

    def build_search_url(self, params: SearchParams) -> str:
        """검색 URL 생성"""
        base = f"{self.BASE_URL}/{params.region.value}/{params.category.value}/search"

        query_parts = [f"q={params.keyword}"]

        if params.function:
            query_parts.append(f"function={params.function.value}")

        if params.chemistry:
            query_parts.append(f"chemistry={params.chemistry}")

        if params.supplier:
            query_parts.append(f"supplier={params.supplier}")

        if params.certifications:
            for cert in params.certifications:
                query_parts.append(f"certification={cert.value}")

        query_string = "&".join(query_parts)
        return f"{base}?{query_string}"

    def build_product_url(self, product_id: str) -> str:
        """제품 상세 페이지 URL"""
        return f"{self.BASE_URL}/{self.region.value}/PersonalCare/Detail/{product_id}"

    def build_supplier_url(self, supplier_id: str) -> str:
        """공급사 페이지 URL"""
        return f"{self.BASE_URL}/{self.region.value}/PersonalCare/Supplier/{supplier_id}"

    def build_web_search_query(self, params: SearchParams) -> str:
        """WebSearch 도구용 검색 쿼리 생성"""
        query_parts = ["site:ulprospector.com", "personal care"]

        query_parts.append(params.keyword)

        if params.function:
            query_parts.append(params.function.value)

        if params.supplier:
            query_parts.append(params.supplier)

        if params.certifications:
            cert_names = [c.value for c in params.certifications]
            query_parts.extend(cert_names)

        return " ".join(query_parts)


class AlternativesFinder:
    """
    대체 원료 탐색기

    기존 원료의 대안을 찾기 위한 유틸리티
    """

    # 기능별 대체 매핑
    FUNCTION_ALTERNATIVES = {
        "dimethicone": {
            "function": FunctionCategory.EMOLLIENT,
            "alternatives": [
                {"inci": "SQUALANE", "type": "natural", "note": "식물성 스쿠알란"},
                {"inci": "C13-15 ALKANE", "type": "natural", "note": "헤미스쿠알란"},
                {"inci": "COCO-CAPRYLATE/CAPRATE", "type": "natural", "note": "코코넛 유래"},
                {"inci": "CAPRYLIC/CAPRIC TRIGLYCERIDE", "type": "natural", "note": "MCT 오일"},
                {"inci": "ISOAMYL COCOATE", "type": "natural", "note": "가벼운 에스터"},
            ]
        },
        "cyclomethicone": {
            "function": FunctionCategory.EMOLLIENT,
            "alternatives": [
                {"inci": "ISODODECANE", "type": "synthetic", "note": "휘발성 탄화수소"},
                {"inci": "C13-15 ALKANE", "type": "natural", "note": "휘발성 알칸"},
                {"inci": "UNDECANE", "type": "natural", "note": "휘발성"},
            ]
        },
        "phenoxyethanol": {
            "function": FunctionCategory.PRESERVATIVE,
            "alternatives": [
                {"inci": "ETHYLHEXYLGLYCERIN", "type": "booster", "note": "방부 보조제"},
                {"inci": "CAPRYLYL GLYCOL", "type": "alternative", "note": "다가 알코올"},
                {"inci": "PENTYLENE GLYCOL", "type": "alternative", "note": "다가 알코올"},
                {"inci": "BENZISOTHIAZOLINONE", "type": "traditional", "note": "전통 방부제"},
            ]
        },
        "parabens": {
            "function": FunctionCategory.PRESERVATIVE,
            "alternatives": [
                {"inci": "PHENOXYETHANOL", "type": "traditional", "note": "파라벤 대체"},
                {"inci": "SODIUM BENZOATE", "type": "food-grade", "note": "식품 등급"},
                {"inci": "POTASSIUM SORBATE", "type": "food-grade", "note": "식품 등급"},
                {"inci": "BENZISOTHIAZOLINONE", "type": "traditional", "note": "IT 계열"},
            ]
        },
        "mineral_oil": {
            "function": FunctionCategory.EMOLLIENT,
            "alternatives": [
                {"inci": "SQUALANE", "type": "natural", "note": "식물성"},
                {"inci": "JOJOBA ESTERS", "type": "natural", "note": "호호바 유래"},
                {"inci": "CAPRYLIC/CAPRIC TRIGLYCERIDE", "type": "natural", "note": "코코넛 유래"},
                {"inci": "HYDROGENATED POLYDECENE", "type": "synthetic", "note": "합성 대체"},
            ]
        },
        "carbomer": {
            "function": FunctionCategory.THICKENER,
            "alternatives": [
                {"inci": "XANTHAN GUM", "type": "natural", "note": "천연 검"},
                {"inci": "HYDROXYETHYLCELLULOSE", "type": "natural-derived", "note": "셀룰로오스 유래"},
                {"inci": "SCLEROTIUM GUM", "type": "natural", "note": "바이오 검"},
                {"inci": "ACRYLATES/C10-30 ALKYL ACRYLATE CROSSPOLYMER", "type": "synthetic", "note": "유사 아크릴레이트"},
            ]
        }
    }

    def find_alternatives(
        self,
        current_inci: str,
        prefer_natural: bool = False,
        certifications: Optional[List[Certification]] = None
    ) -> List[Dict[str, Any]]:
        """
        대체 원료 검색

        Args:
            current_inci: 현재 사용 중인 INCI명
            prefer_natural: 천연 원료 우선 여부
            certifications: 필요 인증

        Returns:
            대체 원료 후보 리스트
        """
        inci_lower = current_inci.lower().replace(" ", "_")

        # 직접 매핑 확인
        if inci_lower in self.FUNCTION_ALTERNATIVES:
            alternatives = self.FUNCTION_ALTERNATIVES[inci_lower]["alternatives"]
        else:
            # 부분 매칭 시도
            alternatives = []
            for key, value in self.FUNCTION_ALTERNATIVES.items():
                if key in inci_lower or inci_lower in key:
                    alternatives.extend(value["alternatives"])

        if not alternatives:
            return []

        # 천연 우선 필터링
        if prefer_natural:
            natural_alts = [a for a in alternatives if a["type"] == "natural"]
            other_alts = [a for a in alternatives if a["type"] != "natural"]
            alternatives = natural_alts + other_alts

        # 검색 쿼리 추가
        for alt in alternatives:
            alt["search_query"] = self._build_search_query(alt["inci"], certifications)

        return alternatives

    def _build_search_query(
        self,
        inci: str,
        certifications: Optional[List[Certification]] = None
    ) -> str:
        """검색 쿼리 생성"""
        query_parts = ["site:ulprospector.com", "personal care", inci]

        if certifications:
            for cert in certifications:
                query_parts.append(cert.value)

        return " ".join(query_parts)


class SampleRequestGenerator:
    """
    샘플 요청서 생성기
    """

    TEMPLATE = """
Subject: Sample Request - {product_name}

Dear {supplier_name} Team,

I am writing to request a sample of {product_name} ({trade_name}) for evaluation purposes.

=== COMPANY INFORMATION ===
Company Name: {company_name}
Industry: Personal Care / Cosmetics
Country: {country}
Website: {website}

=== REQUEST DETAILS ===
Product: {product_name}
Trade Name: {trade_name}
INCI Name: {inci_name}
Quantity Requested: {quantity}
Purpose: {purpose}

=== INTENDED APPLICATION ===
{application}

=== SHIPPING ADDRESS ===
{address}

=== CONTACT PERSON ===
Name: {contact_name}
Title: {contact_title}
Email: {contact_email}
Phone: {contact_phone}

=== REQUESTED DOCUMENTS ===
- Technical Data Sheet (TDS)
- Safety Data Sheet (SDS)
- Certificate of Analysis (CoA)
- Pricing information (if available)
- Regulatory compliance information

Thank you for your consideration. We look forward to evaluating your product.

Best regards,
{contact_name}
{contact_title}
{company_name}
"""

    @dataclass
    class RequestInfo:
        """샘플 요청 정보"""
        # Product
        product_name: str
        trade_name: str
        inci_name: str
        supplier_name: str

        # Company
        company_name: str
        country: str
        website: str

        # Request
        quantity: str
        purpose: str
        application: str

        # Shipping
        address: str

        # Contact
        contact_name: str
        contact_title: str
        contact_email: str
        contact_phone: str

    def generate_request(self, info: 'SampleRequestGenerator.RequestInfo') -> str:
        """샘플 요청서 생성"""
        return self.TEMPLATE.format(
            product_name=info.product_name,
            trade_name=info.trade_name,
            inci_name=info.inci_name,
            supplier_name=info.supplier_name,
            company_name=info.company_name,
            country=info.country,
            website=info.website,
            quantity=info.quantity,
            purpose=info.purpose,
            application=info.application,
            address=info.address,
            contact_name=info.contact_name,
            contact_title=info.contact_title,
            contact_email=info.contact_email,
            contact_phone=info.contact_phone
        )


class TDSParser:
    """
    TDS 정보 파서

    WebFetch로 가져온 TDS 페이지 내용을 파싱
    """

    def parse_basic_info(self, content: str) -> Dict[str, str]:
        """기본 정보 추출"""
        info = {}

        # INCI Name 추출
        inci_match = re.search(r'INCI\s*(?:Name)?[:\s]+([A-Z][A-Z\s\-/,()0-9]+)', content)
        if inci_match:
            info['inci_name'] = inci_match.group(1).strip()

        # CAS Number 추출
        cas_match = re.search(r'CAS\s*(?:Number|No\.?)?[:\s]+(\d{2,7}-\d{2}-\d)', content)
        if cas_match:
            info['cas_number'] = cas_match.group(1)

        # Trade Name 추출
        trade_match = re.search(r'Trade\s*Name[:\s]+([^\n]+)', content, re.IGNORECASE)
        if trade_match:
            info['trade_name'] = trade_match.group(1).strip()

        return info

    def parse_physical_properties(self, content: str) -> Dict[str, str]:
        """물리적 특성 추출"""
        props = {}

        patterns = {
            'appearance': r'Appearance[:\s]+([^\n]+)',
            'color': r'Color[:\s]+([^\n]+)',
            'odor': r'Odor[:\s]+([^\n]+)',
            'ph': r'pH[:\s]+([\d\.\-]+)',
            'viscosity': r'Viscosity[:\s]+([^\n]+)',
            'density': r'(?:Specific\s+)?(?:Gravity|Density)[:\s]+([\d\.\-]+)',
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                props[key] = match.group(1).strip()

        return props

    def parse_use_level(self, content: str) -> Optional[str]:
        """권장 사용량 추출"""
        patterns = [
            r'(?:Recommended|Typical|Suggested)\s+Use\s+Level[:\s]+([\d\.\-]+\s*%?)',
            r'Use\s+Level[:\s]+([\d\.\-]+\s*(?:-\s*[\d\.]+)?\s*%)',
            r'Dosage[:\s]+([\d\.\-]+\s*%)',
        ]

        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return None


# 유틸리티 함수
def validate_cas_number(cas: str) -> bool:
    """CAS 번호 형식 검증"""
    if not re.match(r'^\d{2,7}-\d{2}-\d$', cas):
        return False

    # 체크섬 검증
    digits = cas.replace('-', '')
    check_digit = int(digits[-1])
    total = sum(int(d) * (len(digits) - 1 - i) for i, d in enumerate(digits[:-1]))

    return total % 10 == check_digit


def normalize_inci_name(inci: str) -> str:
    """INCI명 정규화"""
    # 대문자 변환
    normalized = inci.upper()

    # 여분의 공백 제거
    normalized = re.sub(r'\s+', ' ', normalized).strip()

    # 특수문자 정규화
    normalized = normalized.replace('–', '-').replace('—', '-')

    return normalized


def get_supplier_search_queries(keyword: str) -> List[str]:
    """
    주요 공급사별 검색 쿼리 생성

    WebSearch 도구에서 사용
    """
    major_suppliers = [
        "BASF", "Evonik", "Dow", "Croda", "Ashland",
        "DSM", "Lubrizol", "Seppic", "Givaudan", "Symrise"
    ]

    queries = []
    for supplier in major_suppliers:
        query = f"site:ulprospector.com {supplier} {keyword} personal care"
        queries.append(query)

    return queries


# 메인 실행 예시
if __name__ == "__main__":
    # 검색 URL 빌더 예시
    builder = ProspectorSearchBuilder()

    params = SearchParams(
        keyword="niacinamide",
        category=ProductCategory.PERSONAL_CARE,
        region=Region.ASIA_PACIFIC,
        function=FunctionCategory.BRIGHTENING
    )

    search_url = builder.build_search_url(params)
    web_query = builder.build_web_search_query(params)

    print("=== Search URL ===")
    print(search_url)
    print()
    print("=== WebSearch Query ===")
    print(web_query)
    print()

    # 대체 원료 검색 예시
    finder = AlternativesFinder()
    alternatives = finder.find_alternatives(
        "dimethicone",
        prefer_natural=True,
        certifications=[Certification.COSMOS_NATURAL]
    )

    print("=== Dimethicone Alternatives ===")
    for alt in alternatives:
        print(f"- {alt['inci']}: {alt['note']} ({alt['type']})")
    print()

    # CAS 번호 검증 예시
    test_cas = "98-92-0"  # Niacinamide
    print(f"=== CAS Validation ===")
    print(f"{test_cas}: {'Valid' if validate_cas_number(test_cas) else 'Invalid'}")
