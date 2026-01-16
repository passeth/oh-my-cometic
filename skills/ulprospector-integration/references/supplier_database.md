# Supplier and Product Database Structure

## Database Schema Overview

UL Prospector의 데이터베이스 구조를 이해하면 효율적인 검색과 데이터 활용이 가능합니다.

## Entity Relationships

```
[Supplier] 1 ──── N [Product]
    │                   │
    │                   │
    N                   N
    │                   │
[Region]           [Function]
    │                   │
    N                   N
    │                   │
[Certification]    [Chemistry]
                        │
                        N
                        │
                  [Document]
```

## Supplier Entity

### Schema

```python
@dataclass
class Supplier:
    # Primary Key
    supplier_id: str                    # 고유 식별자

    # Basic Information
    name: str                           # 공급사명
    legal_name: str                     # 법적 상호
    headquarters_country: str           # 본사 소재국
    headquarters_city: str              # 본사 소재 도시
    founded_year: int                   # 설립 연도

    # Description
    description: str                    # 회사 설명
    specialties: List[str]              # 전문 분야

    # Contact
    website: str                        # 공식 웹사이트
    general_email: str                  # 대표 이메일
    general_phone: str                  # 대표 전화

    # Regional Presence
    regions: List[str]                  # 공급 가능 지역
    regional_offices: List[Dict]        # 지역 사무소 정보
    distributors: List[Dict]            # 대리점 정보

    # Certifications
    certifications: List[str]           # 보유 인증
    quality_standards: List[str]        # 품질 표준

    # Stats
    product_count: int                  # 등록 제품 수
    category_breakdown: Dict[str, int]  # 카테고리별 제품 수

    # Metadata
    created_at: datetime
    updated_at: datetime
    verified: bool
```

### Major Personal Care Suppliers

```python
MAJOR_SUPPLIERS = {
    # Global Chemical Companies
    "basf": {
        "name": "BASF SE",
        "headquarters": "Germany",
        "product_count": 2500,
        "specialties": ["Surfactants", "Emulsifiers", "Actives", "UV Filters"],
        "brands": ["Plantacare", "Eumulgin", "Myritol", "Uvinul"],
        "korea_contact": "BASF Korea",
        "website": "https://www.basf.com/care-chemicals"
    },

    "evonik": {
        "name": "Evonik Industries AG",
        "headquarters": "Germany",
        "product_count": 1800,
        "specialties": ["Silicones", "Surfactants", "Rheology"],
        "brands": ["Abil", "Tego", "Varisoft"],
        "korea_contact": "Evonik Korea",
        "website": "https://personal-care.evonik.com"
    },

    "dow": {
        "name": "Dow Inc.",
        "headquarters": "USA",
        "product_count": 1200,
        "specialties": ["Silicones", "Polymers", "Cellulosics"],
        "brands": ["Dowsil", "Carbowax", "Cellosize"],
        "korea_contact": "Dow Korea",
        "website": "https://www.dow.com/personalcare"
    },

    "croda": {
        "name": "Croda International",
        "headquarters": "UK",
        "product_count": 1500,
        "specialties": ["Emollients", "Actives", "Sustainability"],
        "brands": ["Crodamol", "Sederma", "Crodasinic"],
        "korea_contact": "Croda Korea",
        "website": "https://www.crodaretail.com"
    },

    # Specialty Ingredients
    "ashland": {
        "name": "Ashland Global Holdings",
        "headquarters": "USA",
        "product_count": 800,
        "specialties": ["Polymers", "Rheology", "Film Formers"],
        "brands": ["Natrosol", "Gantrez", "Styleze"],
        "korea_contact": "Ashland Korea",
        "website": "https://www.ashland.com/personalcare"
    },

    "dsm": {
        "name": "DSM-Firmenich",
        "headquarters": "Netherlands",
        "product_count": 600,
        "specialties": ["Vitamins", "Actives", "UV Filters"],
        "brands": ["Parsol", "Pentavitin", "Alpaflor"],
        "korea_contact": "DSM Korea",
        "website": "https://www.dsm.com/personalcare"
    },

    "lubrizol": {
        "name": "Lubrizol Corporation",
        "headquarters": "USA",
        "product_count": 900,
        "specialties": ["Polymers", "Thickeners", "Sensory"],
        "brands": ["Carbopol", "Pemulen", "Novethix"],
        "korea_contact": "Lubrizol Korea",
        "website": "https://www.lubrizol.com/personalcare"
    },

    "seppic": {
        "name": "Seppic (Air Liquide)",
        "headquarters": "France",
        "product_count": 500,
        "specialties": ["Emulsifiers", "Polymers", "Actives"],
        "brands": ["Montanov", "Sepimax", "Sepitonic"],
        "korea_contact": "Seppic Korea (via distributor)",
        "website": "https://www.seppic.com"
    },

    # Fragrance & Flavor
    "givaudan": {
        "name": "Givaudan SA",
        "headquarters": "Switzerland",
        "product_count": 400,
        "specialties": ["Fragrances", "Actives"],
        "brands": ["Active Beauty", "Sensityl"],
        "korea_contact": "Givaudan Korea",
        "website": "https://www.givaudan.com/activebeauty"
    },

    "symrise": {
        "name": "Symrise AG",
        "headquarters": "Germany",
        "product_count": 450,
        "specialties": ["Fragrances", "Actives", "Botanicals"],
        "brands": ["SymSitive", "SymHair", "SymWhite"],
        "korea_contact": "Symrise Korea",
        "website": "https://www.symrise.com/cosmetic-ingredients"
    },

    # Asian Suppliers
    "shin-etsu": {
        "name": "Shin-Etsu Chemical",
        "headquarters": "Japan",
        "product_count": 600,
        "specialties": ["Silicones"],
        "brands": ["KF", "KSG", "KP"],
        "korea_contact": "Shin-Etsu Korea",
        "website": "https://www.shinetsusilicone-global.com"
    },

    "nikkol": {
        "name": "Nikkol Group",
        "headquarters": "Japan",
        "product_count": 400,
        "specialties": ["Emulsifiers", "Surfactants", "Actives"],
        "brands": ["Nikkol", "Nikkomulese"],
        "korea_contact": "Distributor",
        "website": "https://www.nikkol.co.jp"
    }
}
```

## Product Entity

### Schema

```python
@dataclass
class Product:
    # Primary Key
    product_id: str                     # 고유 식별자

    # Basic Information
    product_name: str                   # 제품명
    trade_name: str                     # 상표명
    supplier_id: str                    # 공급사 ID (FK)
    supplier_name: str                  # 공급사명

    # Chemical Identity
    inci_name: str                      # INCI 성분명
    inci_names: List[str]               # 복합 INCI (혼합물)
    cas_number: str                     # CAS 등록번호
    cas_numbers: List[str]              # 복합 CAS
    ec_number: str                      # EC 번호
    chemical_name: str                  # 화학명
    molecular_formula: str              # 분자식
    molecular_weight: float             # 분자량

    # Classification
    chemistry_type: str                 # 화학적 분류
    function_categories: List[str]      # 기능 분류
    application_areas: List[str]        # 적용 분야

    # Physical Properties
    physical_form: str                  # 물리적 형태
    appearance: str                     # 외관
    color: str                          # 색상
    odor: str                           # 냄새
    ph: str                             # pH (range)
    viscosity: str                      # 점도 (range)
    density: str                        # 밀도
    melting_point: str                  # 녹는점
    boiling_point: str                  # 끓는점
    flash_point: str                    # 인화점
    solubility: Dict[str, str]          # 용해도 (용매별)

    # Usage Information
    recommended_use_level: str          # 권장 사용량 (%)
    typical_use_level: str              # 일반 사용량 (%)
    max_use_level: str                  # 최대 사용량 (%)
    suggested_applications: List[str]   # 권장 적용 제품
    processing_guidelines: str          # 가공 지침
    compatibility_notes: str            # 호환성 참고

    # Regulatory Information
    regulatory_status: Dict[str, str]   # 국가별 규제 상태
    certifications: List[str]           # 인증 목록
    claims: List[str]                   # 마케팅 클레임
    safety_notes: str                   # 안전 참고

    # Commercial Information
    availability: List[str]             # 공급 가능 지역
    packaging_options: List[str]        # 포장 옵션
    moq: str                            # 최소 주문 수량 (Premium)
    price_range: str                    # 가격대 (Premium)

    # Documents
    tds_url: str                        # TDS 링크
    sds_url: str                        # SDS 링크
    brochure_url: str                   # 브로슈어 링크

    # Metadata
    created_at: datetime
    updated_at: datetime
    featured: bool
    status: str                         # active, discontinued
```

### Product Categories Hierarchy

```yaml
Personal Care:
  Skin Care:
    Face Care:
      - Anti-Aging
      - Brightening
      - Moisturizing
      - Acne Treatment
    Body Care:
      - Body Lotion
      - Body Wash
      - Hand Care
    Sun Care:
      - Sunscreen
      - After Sun
      - Self Tanning

  Hair Care:
    Shampoo:
      - Cleansing
      - Anti-Dandruff
      - Color Care
    Conditioner:
      - Rinse-Off
      - Leave-In
      - Deep Treatment
    Styling:
      - Gels & Waxes
      - Sprays
      - Serums

  Color Cosmetics:
    Face Makeup:
      - Foundation
      - Concealer
      - Powder
    Eye Makeup:
      - Mascara
      - Eyeshadow
      - Eyeliner
    Lip Products:
      - Lipstick
      - Lip Gloss
      - Lip Care

  Toiletries:
    Oral Care:
      - Toothpaste
      - Mouthwash
    Deodorants:
      - Antiperspirants
      - Natural Deodorants
    Bath Products:
      - Bath Bombs
      - Bath Salts
```

## Function Entity

### Schema

```python
@dataclass
class Function:
    function_id: str
    name: str
    display_name: str
    description: str
    parent_category: str
    product_count: int
```

### Function Taxonomy

```python
FUNCTION_TAXONOMY = {
    "actives": {
        "display_name": "Active Ingredients",
        "children": {
            "anti_aging": "Anti-Aging Actives",
            "brightening": "Skin Brightening",
            "moisturizing": "Moisturizing Actives",
            "soothing": "Soothing & Calming",
            "firming": "Firming & Tightening",
            "exfoliating": "Exfoliating Agents",
            "antimicrobial": "Antimicrobial Actives"
        }
    },

    "emollients": {
        "display_name": "Emollients & Moisturizers",
        "children": {
            "natural_oils": "Natural Oils",
            "esters": "Esters",
            "fatty_alcohols": "Fatty Alcohols",
            "silicones": "Silicone Emollients",
            "waxes": "Waxes",
            "butters": "Butters",
            "humectants": "Humectants"
        }
    },

    "surfactants": {
        "display_name": "Surfactants & Cleansing",
        "children": {
            "anionic": "Anionic Surfactants",
            "nonionic": "Nonionic Surfactants",
            "amphoteric": "Amphoteric Surfactants",
            "cationic": "Cationic Surfactants",
            "mild": "Mild/Baby Surfactants"
        }
    },

    "emulsifiers": {
        "display_name": "Emulsifiers & Solubilizers",
        "children": {
            "ow_emulsifiers": "O/W Emulsifiers",
            "wo_emulsifiers": "W/O Emulsifiers",
            "cold_process": "Cold Process Emulsifiers",
            "solubilizers": "Solubilizers",
            "co_emulsifiers": "Co-Emulsifiers"
        }
    },

    "rheology": {
        "display_name": "Rheology & Texture",
        "children": {
            "natural_thickeners": "Natural Thickeners",
            "synthetic_thickeners": "Synthetic Thickeners",
            "rheology_modifiers": "Rheology Modifiers",
            "sensory_modifiers": "Sensory Modifiers",
            "film_formers": "Film Formers"
        }
    },

    "sun_care": {
        "display_name": "Sun Care",
        "children": {
            "organic_filters": "Organic UV Filters",
            "inorganic_filters": "Inorganic UV Filters",
            "boosters": "Sunscreen Boosters",
            "after_sun": "After Sun Care"
        }
    },

    "preservation": {
        "display_name": "Preservation & Stability",
        "children": {
            "preservatives": "Preservatives",
            "preservative_boosters": "Preservative Boosters",
            "antioxidants": "Antioxidants",
            "chelating": "Chelating Agents"
        }
    },

    "hair_care": {
        "display_name": "Hair Care",
        "children": {
            "conditioning": "Conditioning Agents",
            "styling": "Styling Polymers",
            "silicones": "Hair Silicones",
            "proteins": "Hair Proteins",
            "colorants": "Hair Colorants"
        }
    },

    "colorants": {
        "display_name": "Color & Effects",
        "children": {
            "pigments": "Pigments",
            "dyes": "Dyes",
            "pearls": "Pearls & Effects",
            "natural_colorants": "Natural Colorants"
        }
    },

    "fragrances": {
        "display_name": "Fragrances",
        "children": {
            "fragrance_oils": "Fragrance Oils",
            "essential_oils": "Essential Oils",
            "masking_agents": "Masking Agents"
        }
    }
}
```

## Chemistry Entity

### Schema

```python
@dataclass
class Chemistry:
    chemistry_id: str
    name: str
    description: str
    parent_category: str
    typical_inci_prefix: str
    product_count: int
```

### Chemistry Classification

```python
CHEMISTRY_CLASSIFICATION = {
    "silicones": {
        "description": "Silicon-based polymers and compounds",
        "sub_types": {
            "dimethicone": "Dimethicone and derivatives",
            "cyclomethicone": "Cyclic silicones",
            "phenyl_silicone": "Phenyl-modified silicones",
            "amino_silicone": "Amino-functional silicones",
            "silicone_elastomer": "Cross-linked silicone elastomers",
            "silicone_resin": "Silicone resins"
        }
    },

    "fatty_derivatives": {
        "description": "Fatty acid-based compounds",
        "sub_types": {
            "fatty_acids": "Free fatty acids",
            "fatty_alcohols": "Fatty alcohols (cetyl, cetearyl)",
            "fatty_esters": "Fatty acid esters",
            "triglycerides": "Triglycerides and natural oils",
            "glycerides": "Mono/Di-glycerides"
        }
    },

    "polymers": {
        "description": "Synthetic and modified natural polymers",
        "sub_types": {
            "acrylates": "Acrylate copolymers",
            "carbomers": "Carbomer/Carbopol",
            "peg_compounds": "PEG and derivatives",
            "silicone_polymers": "Silicone-containing polymers",
            "natural_modified": "Modified natural polymers"
        }
    },

    "polysaccharides": {
        "description": "Natural sugar-based polymers",
        "sub_types": {
            "cellulose": "Cellulose derivatives",
            "gums": "Natural gums (xanthan, guar)",
            "starches": "Modified starches",
            "hyaluronic": "Hyaluronic acid derivatives",
            "chitin": "Chitin/Chitosan"
        }
    },

    "amino_acids_proteins": {
        "description": "Amino acids and protein derivatives",
        "sub_types": {
            "amino_acids": "Free amino acids",
            "peptides": "Peptides",
            "hydrolyzed_proteins": "Hydrolyzed proteins",
            "protein_derivatives": "Protein derivatives"
        }
    },

    "botanicals": {
        "description": "Plant-derived ingredients",
        "sub_types": {
            "extracts": "Botanical extracts",
            "oils": "Botanical oils",
            "butters": "Botanical butters",
            "essential_oils": "Essential oils",
            "actives": "Botanical active compounds"
        }
    }
}
```

## Document Entity

### Schema

```python
@dataclass
class Document:
    document_id: str
    product_id: str                     # FK
    supplier_id: str                    # FK

    document_type: str                  # TDS, SDS, CoA, Brochure
    title: str
    filename: str
    file_format: str                    # PDF, DOC, XLS
    file_size: int                      # bytes
    language: str
    version: str
    revision_date: date

    download_url: str
    requires_login: bool
    premium_only: bool

    created_at: datetime
    updated_at: datetime
```

### Document Types Detail

```python
DOCUMENT_TYPES = {
    "TDS": {
        "name": "Technical Data Sheet",
        "typical_sections": [
            "Product Description",
            "INCI Name",
            "CAS Number",
            "Physical Properties",
            "Chemical Properties",
            "Typical Use Levels",
            "Applications",
            "Processing Guidelines",
            "Compatibility",
            "Storage & Handling",
            "Regulatory Status",
            "Packaging"
        ],
        "access": "Free (login required)"
    },

    "SDS": {
        "name": "Safety Data Sheet",
        "typical_sections": [
            "1. Identification",
            "2. Hazard Identification",
            "3. Composition/Ingredients",
            "4. First-Aid Measures",
            "5. Fire-Fighting Measures",
            "6. Accidental Release Measures",
            "7. Handling and Storage",
            "8. Exposure Controls/PPE",
            "9. Physical/Chemical Properties",
            "10. Stability and Reactivity",
            "11. Toxicological Information",
            "12. Ecological Information",
            "13. Disposal Considerations",
            "14. Transport Information",
            "15. Regulatory Information",
            "16. Other Information"
        ],
        "access": "Free (login required)"
    },

    "CoA": {
        "name": "Certificate of Analysis",
        "typical_sections": [
            "Product Information",
            "Batch/Lot Number",
            "Manufacturing Date",
            "Expiry Date",
            "Test Results",
            "Specifications",
            "QC Approval"
        ],
        "access": "Request only"
    },

    "BROCHURE": {
        "name": "Product Brochure",
        "typical_sections": [
            "Product Overview",
            "Key Benefits",
            "Applications",
            "Marketing Claims",
            "Formulation Examples"
        ],
        "access": "Free"
    },

    "FORMULATION": {
        "name": "Formulation Guide",
        "typical_sections": [
            "Example Formulations",
            "Processing Instructions",
            "Tips & Tricks",
            "Troubleshooting"
        ],
        "access": "Free/Premium"
    }
}
```

## Certification Entity

### Schema

```python
@dataclass
class Certification:
    certification_id: str
    name: str
    full_name: str
    description: str
    issuing_body: str
    website: str
    logo_url: str
    category: str                       # Natural, Organic, Quality, Regional
```

### Common Certifications

```python
CERTIFICATIONS = {
    # Natural & Organic
    "cosmos_organic": {
        "name": "COSMOS Organic",
        "issuing_body": "COSMOS-standard",
        "description": "European organic cosmetics certification"
    },
    "cosmos_natural": {
        "name": "COSMOS Natural",
        "issuing_body": "COSMOS-standard",
        "description": "European natural cosmetics certification"
    },
    "ecocert": {
        "name": "ECOCERT",
        "issuing_body": "ECOCERT Group",
        "description": "French organic/natural certification"
    },
    "natrue": {
        "name": "NATRUE",
        "issuing_body": "NATRUE",
        "description": "International natural/organic certification"
    },
    "usda_organic": {
        "name": "USDA Organic",
        "issuing_body": "USDA",
        "description": "US organic certification"
    },

    # Quality Standards
    "iso_9001": {
        "name": "ISO 9001",
        "issuing_body": "ISO",
        "description": "Quality management system"
    },
    "iso_22716": {
        "name": "ISO 22716 (GMP)",
        "issuing_body": "ISO",
        "description": "Cosmetics GMP"
    },
    "halal": {
        "name": "Halal",
        "issuing_body": "Various",
        "description": "Islamic compliance"
    },

    # Sustainability
    "rspo": {
        "name": "RSPO",
        "issuing_body": "Roundtable on Sustainable Palm Oil",
        "description": "Sustainable palm oil certification"
    },
    "vegan": {
        "name": "Vegan",
        "issuing_body": "Various",
        "description": "No animal-derived ingredients"
    },
    "cruelty_free": {
        "name": "Cruelty Free",
        "issuing_body": "Leaping Bunny, PETA",
        "description": "No animal testing"
    },

    # Regional Compliance
    "china_nmpa": {
        "name": "China NMPA Registered",
        "issuing_body": "China NMPA",
        "description": "Registered for China market"
    },
    "eu_compliant": {
        "name": "EU Cosmetics Regulation Compliant",
        "issuing_body": "EU",
        "description": "EC 1223/2009 compliant"
    }
}
```

## Query Examples

### SQL-like Queries

```sql
-- 특정 기능의 모든 제품 검색
SELECT p.*
FROM products p
JOIN product_functions pf ON p.product_id = pf.product_id
JOIN functions f ON pf.function_id = f.function_id
WHERE f.name = 'Emollients'
  AND p.status = 'active';

-- 특정 공급사의 COSMOS 인증 제품
SELECT p.*
FROM products p
JOIN product_certifications pc ON p.product_id = pc.product_id
JOIN certifications c ON pc.certification_id = c.certification_id
WHERE p.supplier_id = 'basf'
  AND c.name = 'COSMOS Natural';

-- 실리콘 대체 원료 검색
SELECT p.*
FROM products p
JOIN product_functions pf ON p.product_id = pf.product_id
WHERE pf.function_id IN (
    SELECT function_id FROM functions WHERE name LIKE '%Emollient%'
)
AND p.chemistry_type != 'silicone'
AND 'natural' = ANY(p.certifications);
```

### API Query Examples

```python
# WebSearch를 활용한 검색 예시
def search_products_example():
    """WebSearch 도구를 활용한 UL Prospector 검색"""

    # 1. 기본 검색
    query1 = "site:ulprospector.com personal care niacinamide"

    # 2. 공급사 특정 검색
    query2 = "site:ulprospector.com BASF emollient personal care"

    # 3. 인증 검색
    query3 = "site:ulprospector.com COSMOS organic emulsifier"

    # 4. 대체 원료 검색
    query4 = "site:ulprospector.com silicone alternative natural emollient"

    return [query1, query2, query3, query4]
```

## Data Relationships Summary

```
Supplier (공급사)
  ├── Products (제품) - 1:N
  │     ├── Functions (기능) - N:N
  │     ├── Chemistry (화학분류) - N:1
  │     ├── Documents (문서) - 1:N
  │     ├── Certifications (인증) - N:N
  │     └── Regions (지역) - N:N
  ├── Certifications (인증) - N:N
  └── Regions (지역) - N:N
```

이 구조를 이해하면 UL Prospector에서 효율적으로 원료를 검색하고 비교 분석할 수 있습니다.
