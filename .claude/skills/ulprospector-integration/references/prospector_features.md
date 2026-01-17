# UL Prospector Platform Features

## Platform Overview

UL Prospector는 UL Solutions(구 UL)에서 운영하는 B2B 원료 데이터베이스 플랫폼입니다. 화장품(Personal Care), 식품(Food), 코팅(Coatings), 접착제(Adhesives) 등 다양한 산업 분야의 원료 정보를 제공합니다.

### Personal Care 포털
- **URL**: https://www.ulprospector.com/en/na/PersonalCare
- **대상**: 화장품, 개인위생용품 제조업체
- **컨텐츠**: 원료, 공급사, 기술 문서, 포뮬레이션 가이드

## Search Features

### 1. Basic Search

#### 키워드 검색
```
검색 대상:
- Product Name (상품명)
- Trade Name (상표명)
- INCI Name (국제 화장품 성분명)
- Chemical Name (화학명)
- CAS Number
- Supplier Name (공급사명)
```

#### 검색 URL 구조
```
https://www.ulprospector.com/en/na/PersonalCare/search?
    q={검색어}
    &function={기능코드}
    &supplier={공급사ID}
    &chemistry={화학분류코드}
```

### 2. Advanced Search

#### 필터 옵션

| 필터 | 설명 | 예시 값 |
|------|------|---------|
| Function | 기능 분류 | Emollients, Thickeners |
| Chemistry | 화학적 분류 | Silicones, Esters |
| Supplier | 공급사 | BASF, Evonik |
| Region | 공급 지역 | North America, Asia Pacific |
| Certification | 인증 | COSMOS, ECOCERT, Natural |
| Compliance | 규제 준수 | EU Cosmetics, China NMPA |

#### 기능별 카테고리 코드

```python
FUNCTION_CATEGORIES = {
    # Actives
    "active_anti_aging": "Anti-Aging Actives",
    "active_brightening": "Skin Brightening Actives",
    "active_moisturizing": "Moisturizing Actives",
    "active_soothing": "Soothing & Calming Actives",

    # Emollients & Moisturizers
    "emollient_natural": "Natural Emollients",
    "emollient_synthetic": "Synthetic Emollients",
    "emollient_silicone": "Silicone Emollients",
    "humectant": "Humectants",

    # Rheology & Texture
    "thickener_natural": "Natural Thickeners",
    "thickener_synthetic": "Synthetic Thickeners",
    "rheology_modifier": "Rheology Modifiers",
    "sensory_modifier": "Sensory Modifiers",

    # Surfactants & Emulsifiers
    "surfactant_anionic": "Anionic Surfactants",
    "surfactant_nonionic": "Nonionic Surfactants",
    "surfactant_amphoteric": "Amphoteric Surfactants",
    "emulsifier_ow": "O/W Emulsifiers",
    "emulsifier_wo": "W/O Emulsifiers",
    "solubilizer": "Solubilizers",

    # Sun Care
    "uv_filter_organic": "Organic UV Filters",
    "uv_filter_inorganic": "Inorganic UV Filters",
    "sunscreen_booster": "Sunscreen Boosters",

    # Preservation
    "preservative_traditional": "Traditional Preservatives",
    "preservative_alternative": "Alternative Preservatives",
    "antioxidant": "Antioxidants",
    "chelating_agent": "Chelating Agents",

    # Color & Fragrance
    "colorant_natural": "Natural Colorants",
    "colorant_synthetic": "Synthetic Colorants",
    "fragrance": "Fragrances & Masking Agents",

    # Hair Care
    "hair_conditioning": "Hair Conditioning Agents",
    "hair_styling": "Hair Styling Polymers",
    "hair_colorant": "Hair Colorants"
}
```

### 3. Chemistry Classification

```python
CHEMISTRY_TYPES = {
    # Lipid-based
    "fatty_acids": "Fatty Acids & Derivatives",
    "fatty_alcohols": "Fatty Alcohols",
    "esters": "Esters",
    "triglycerides": "Triglycerides & Oils",
    "waxes": "Waxes",

    # Silicone-based
    "silicone_fluid": "Silicone Fluids",
    "silicone_resin": "Silicone Resins",
    "silicone_elastomer": "Silicone Elastomers",
    "silicone_functional": "Functional Silicones",

    # Polymer-based
    "polymer_synthetic": "Synthetic Polymers",
    "polymer_natural": "Natural Polymers",
    "polymer_modified": "Modified Natural Polymers",

    # Sugar-based
    "sugar_derivative": "Sugar Derivatives",
    "polysaccharide": "Polysaccharides",

    # Protein-based
    "protein_hydrolyzed": "Hydrolyzed Proteins",
    "peptide": "Peptides",
    "amino_acid": "Amino Acids",

    # Botanical
    "botanical_extract": "Botanical Extracts",
    "essential_oil": "Essential Oils",
    "botanical_active": "Botanical Actives"
}
```

## Product Information

### Product Page Structure

```
1. Header
   - Product Name
   - Trade Name
   - Supplier Logo & Name
   - Quick Actions (Sample Request, Compare, Save)

2. Basic Information
   - INCI Name
   - CAS Number
   - Chemical Name
   - Description

3. Technical Specifications
   - Physical Form
   - Appearance
   - Color
   - Odor
   - pH
   - Viscosity
   - Specific Gravity
   - Solubility

4. Application Information
   - Function Categories
   - Recommended Use Level
   - Suggested Applications
   - Processing Guidelines

5. Regulatory Information
   - Regional Compliance
   - Certifications
   - Claims

6. Documents
   - Technical Data Sheet (TDS)
   - Safety Data Sheet (SDS)
   - Certificate of Analysis (CoA)
   - Brochures

7. Related Products
   - Same Supplier
   - Similar Function
   - Alternatives
```

### Document Types

| 문서 유형 | 약어 | 내용 |
|----------|------|------|
| Technical Data Sheet | TDS | 기술 사양, 사용법, 물성 |
| Safety Data Sheet | SDS/MSDS | 안전 정보, GHS 분류, 응급조치 |
| Certificate of Analysis | CoA | 배치별 품질 분석 결과 |
| Regulatory Compliance | - | 국가별 규제 준수 정보 |
| Formulation Guide | - | 배합 가이드, 예시 처방 |
| Marketing Claims | - | 마케팅 클레임, 효능 데이터 |

## Supplier Features

### Supplier Profile

```
1. Company Overview
   - Company Name
   - Headquarters Location
   - Founded Year
   - Company Description

2. Products
   - Total Product Count
   - Category Breakdown
   - Featured Products

3. Capabilities
   - Manufacturing Locations
   - R&D Centers
   - Technical Support

4. Certifications
   - Quality (ISO, GMP)
   - Sustainability (COSMOS, ECOCERT)
   - Regional (NMPA, FDA)

5. Contact Information
   - Regional Offices
   - Sales Contacts
   - Technical Support
   - Website
```

### Regional Availability

| 지역 | 코드 | 포함 국가 |
|------|------|----------|
| North America | NA | USA, Canada, Mexico |
| Latin America | LATAM | Brazil, Argentina, etc. |
| Europe | EU | EU 27, UK, Switzerland |
| Middle East & Africa | MEA | UAE, Saudi, South Africa |
| Asia Pacific | APAC | China, Japan, Korea, SEA |
| Australia/NZ | ANZ | Australia, New Zealand |

## Comparison Tool

### Side-by-Side Comparison

최대 4개 제품 동시 비교 가능:

```
비교 항목:
- Basic Info (INCI, CAS, Supplier)
- Physical Properties (Form, Appearance, pH)
- Technical Specs (Use Level, Processing)
- Certifications
- Regulatory Compliance
- Price Range (Premium only)
```

### Export Options
- PDF 비교표
- Excel 다운로드
- Print View

## Sample Request System

### Request Flow

```
1. Select Product
   ↓
2. Add to Sample Cart
   ↓
3. Fill Request Form
   - Company Information
   - Contact Details
   - Purpose/Application
   - Quantity Needed
   ↓
4. Submit Request
   ↓
5. Supplier Review (1-3 days)
   ↓
6. Sample Shipped / Declined
   ↓
7. Tracking & Notification
```

### Request Form Fields

```yaml
required:
  - company_name: "회사명"
  - industry: "산업 분야"
  - country: "국가"
  - contact_name: "담당자명"
  - contact_email: "이메일"
  - contact_phone: "전화번호"
  - shipping_address: "배송 주소"
  - sample_purpose: "샘플 사용 목적"

optional:
  - company_website: "회사 웹사이트"
  - job_title: "직책"
  - project_timeline: "프로젝트 일정"
  - expected_volume: "예상 사용량"
  - additional_notes: "추가 요청 사항"
```

## Account Features

### Free Account

```
포함 기능:
- 기본 검색 (월 제한 있음)
- 제품 목록 조회
- 기본 제품 정보 확인
- 일부 TDS 다운로드
- 샘플 요청 (월 제한 있음)
- 제품 저장 (제한된 수)
- 뉴스레터 구독
```

### Premium Account

```
추가 기능:
- 무제한 검색
- 전체 문서 다운로드
- 상세 비교 도구
- 가격 정보 접근
- 무제한 샘플 요청
- API 접근 (Enterprise)
- 맞춤 알림 설정
- 전담 고객 지원
```

## API Access (Enterprise)

### Available Endpoints

```
/api/v1/products/search
/api/v1/products/{id}
/api/v1/products/{id}/documents
/api/v1/suppliers
/api/v1/suppliers/{id}
/api/v1/suppliers/{id}/products
/api/v1/categories
/api/v1/samples/request
/api/v1/samples/{id}/status
```

### Rate Limits

| Tier | Requests/Hour | Requests/Day |
|------|--------------|--------------|
| Standard | 100 | 1,000 |
| Professional | 500 | 5,000 |
| Enterprise | 2,000 | 20,000 |

## Notification Features

### Alert Types

```
1. New Products
   - 특정 공급사 신제품
   - 특정 카테고리 신제품
   - 키워드 매칭 제품

2. Document Updates
   - TDS 업데이트
   - SDS 개정
   - 규제 정보 변경

3. Supplier Updates
   - 새로운 인증 획득
   - 지역 확장
   - 가격 변동

4. Regulatory Alerts
   - 규제 변경 사항
   - 새로운 인증 요건
   - 국가별 업데이트
```

### Notification Channels
- Email (즉시/일간/주간)
- Platform Dashboard
- Mobile App (Premium)

## Mobile Features

### Mobile Web
- 반응형 웹 디자인
- 기본 검색 기능
- 제품 정보 조회
- 샘플 요청

### Mobile App (Premium)
- QR 코드 스캔 (전시회용)
- 오프라인 문서 저장
- 푸시 알림
- 비교 도구

## Integration Options

### Data Export
- CSV/Excel 다운로드
- PDF 문서 저장
- Bulk export (Enterprise)

### Third-Party Integration
- ERP 시스템 연동
- PLM 시스템 연동
- 조달 시스템 연동

## Tips for Effective Use

### 검색 최적화
1. **정확한 용어**: INCI명 우선 사용
2. **필터 활용**: 카테고리 + 기능 조합
3. **공급사 지정**: 알려진 공급사로 범위 축소
4. **저장 기능**: 관심 제품 폴더 정리

### 문서 활용
1. **TDS 비교**: 동일 기능 제품 TDS 비교 분석
2. **SDS 확인**: 안전성, 취급 주의사항 필수 확인
3. **규제 정보**: 목표 시장 규제 준수 확인

### 공급사 관계
1. **직접 연락**: 상세 정보는 직접 문의
2. **전시회 활용**: in-cosmetics 등 전시회 참가
3. **기술 지원**: 공급사 기술팀 활용

## Troubleshooting

### 로그인 문제
```
증상: 로그인 실패
해결:
1. 비밀번호 재설정
2. 쿠키 삭제 후 재시도
3. 다른 브라우저 시도
4. 고객 지원 문의
```

### 문서 다운로드 오류
```
증상: TDS 다운로드 불가
해결:
1. 로그인 상태 확인
2. 팝업 차단 해제
3. PDF 리더 확인
4. 공급사 직접 요청
```

### 검색 결과 문제
```
증상: 예상 결과 미출력
해결:
1. 검색어 철자 확인
2. 필터 조건 완화
3. 동의어/대체명 검색
4. 공급사 직접 확인
```
