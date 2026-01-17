# INCI Dictionary 구조 및 명명 규칙

## INCI 명명 체계 개요

**INCI (International Nomenclature of Cosmetic Ingredients)**는 화장품 성분의 국제 표준 명명 체계입니다. PCPC(Personal Care Products Council)에서 관리하며, 전 세계 화장품 라벨 표기에 사용됩니다.

### 역사

| 연도 | 사건 |
|------|------|
| 1973 | CTFA (PCPC 전신) 최초 성분 사전 발행 |
| 1993 | EU에서 INCI 채택 (Cosmetics Directive 76/768/EEC 개정) |
| 2009 | EU Regulation 1223/2009에서 INCI 의무화 |
| 현재 | 30,000+ 등록 성분, 분기별 업데이트 |

## 모노그래프 구조 (Monograph Structure)

ICID의 각 성분 항목(모노그래프)에 포함되는 정보:

### 필수 항목

```
┌────────────────────────────────────────────────────────────────┐
│  INCI MONOGRAPH: NIACINAMIDE                                   │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  1. INCI NAME (필수)                                           │
│     ─────────────────                                         │
│     NIACINAMIDE                                                │
│     - 공식 표기 명칭                                            │
│     - 대문자 표기                                               │
│                                                                │
│  2. CAS NUMBER(s) (필수, 가능시)                                │
│     ────────────────────────────                              │
│     98-92-0                                                    │
│     - Chemical Abstracts Service 등록 번호                      │
│     - 복수 가능 (이성질체, 수화물 등)                            │
│                                                                │
│  3. EINECS/ELINCS NUMBER (EU 관련)                             │
│     ─────────────────────────────                             │
│     202-713-4                                                  │
│     - European Inventory of Chemical Substances               │
│                                                                │
│  4. DEFINITION (정의)                                          │
│     ────────────────                                          │
│     "Niacinamide is the organic compound that conforms        │
│      to the formula: C6H6N2O"                                  │
│                                                                │
│  5. CHEMICAL/IUPAC NAME                                        │
│     ───────────────────                                       │
│     Pyridine-3-carboxamide                                     │
│     3-Pyridinecarboxylic acid amide                            │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### 선택적 항목

```
┌────────────────────────────────────────────────────────────────┐
│  OPTIONAL INFORMATION                                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  6. EMPIRICAL FORMULA (분자식)                                  │
│     ─────────────────────────                                 │
│     C6H6N2O                                                    │
│                                                                │
│  7. MOLECULAR WEIGHT (분자량)                                   │
│     ────────────────────────                                  │
│     122.12 g/mol                                               │
│                                                                │
│  8. TRADE NAMES / SYNONYMS (상용명/동의어)                      │
│     ──────────────────────────────────                        │
│     - Vitamin B3                                               │
│     - Nicotinamide                                             │
│     - Nicotinic acid amide                                     │
│                                                                │
│  9. STRUCTURAL FORMULA (구조식)                                 │
│     ────────────────────────                                  │
│     [화학 구조 이미지]                                          │
│                                                                │
│  10. REGISTRATION DATE / AMENDMENTS                            │
│      ──────────────────────────────                           │
│      First registered: 1973                                    │
│      Last amended: 2020-Q2                                     │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

## INCI 명명 규칙

### 1. 일반 규칙

#### 대소문자 규칙
```
규칙: 항상 대문자 사용

올바른 예:
  NIACINAMIDE
  HYALURONIC ACID
  SODIUM CHLORIDE

잘못된 예:
  Niacinamide
  hyaluronic acid
  SODIUM chloride
```

#### 허용 문자
```
허용:
  - 대문자 A-Z
  - 숫자 0-9
  - 하이픈 (-)
  - 공백 ( )
  - 슬래시 (/) - 특수 경우
  - 괄호 () - 일반명, 나노 표기

비허용:
  - 소문자 a-z
  - 특수문자 (@, #, $, %, etc.)
  - 그리스 문자 (alpha -> ALPHA로 표기)
```

### 2. 식물 유래 성분 명명

#### 기본 구조
```
[속명] [종명] ([일반명]) [부위] [형태]

예시:
CAMELLIA SINENSIS LEAF EXTRACT
└──속명──┘ └종명─┘ └부위┘ └형태┘

OLEA EUROPAEA (OLIVE) FRUIT OIL
└속명┘ └종명─┘  └일반명┘ └부위┘ └형태┘
```

#### 부위 용어 (Plant Parts)
| 영어 | 한글 | 예시 |
|------|------|------|
| LEAF | 잎 | CAMELLIA SINENSIS LEAF EXTRACT |
| FLOWER | 꽃 | ROSA DAMASCENA FLOWER WATER |
| FRUIT | 열매/과실 | CITRUS LIMON FRUIT EXTRACT |
| SEED | 씨앗 | VITIS VINIFERA SEED OIL |
| KERNEL | 종자/핵 | ARGANIA SPINOSA KERNEL OIL |
| ROOT | 뿌리 | GLYCYRRHIZA GLABRA ROOT EXTRACT |
| BARK | 껍질/수피 | SALIX ALBA BARK EXTRACT |
| STEM | 줄기 | BAMBUSA VULGARIS STEM EXTRACT |
| PEEL | 과피 | CITRUS AURANTIUM DULCIS PEEL OIL |
| WHOLE PLANT | 전초 | CENTELLA ASIATICA |

#### 형태 용어 (Form/Type)
| 영어 | 한글 | 정의 |
|------|------|------|
| EXTRACT | 추출물 | 용매로 추출한 농축물 |
| OIL | 오일 | 압착/추출 유지 |
| BUTTER | 버터 | 상온 고체 유지 |
| WAX | 왁스 | 왁스상 물질 |
| WATER | 워터/증류수 | 수증기 증류액 |
| POWDER | 분말 | 건조 분말 형태 |
| JUICE | 주스/즙 | 착즙액 |

#### 일반명 포함 예시
```
학명만 사용:
  ALOE BARBADENSIS LEAF JUICE

학명 + 일반명:
  BUTYROSPERMUM PARKII (SHEA) BUTTER
  CERA ALBA (BEESWAX)
  OLEA EUROPAEA (OLIVE) FRUIT OIL

일반명 병기 이유:
  - 소비자 이해도 향상
  - 알레르겐 인식 용이
  - 일부 국가 규제 요구
```

### 3. 합성/화학 성분 명명

#### 화학명 기반
```
기본 원칙:
  - 화학명을 기반으로 간소화
  - 접두사/접미사로 유도체 구분

예시:
SODIUM HYALURONATE    (Sodium salt of Hyaluronic acid)
TOCOPHERYL ACETATE    (Acetate ester of Tocopherol)
ASCORBYL GLUCOSIDE    (Glucoside of Ascorbic acid)
```

#### PEG/PPG 계열
```
PEG-[숫자] = Polyethylene Glycol (평균 분자량 기준)
  PEG-8      → 약 MW 400
  PEG-40     → 약 MW 1,800
  PEG-100    → 약 MW 4,400

PEG-[숫자] [화학명]
  PEG-40 HYDROGENATED CASTOR OIL
  PEG-100 STEARATE

PPG-[숫자] = Polypropylene Glycol
  PPG-15 STEARYL ETHER
```

#### 폴리머 계열
```
CARBOMER
  └─ Carboxy vinyl polymer (점증제)

ACRYLATES COPOLYMER
  └─ 아크릴레이트 공중합체

POLYQUATERNIUM-[숫자]
  └─ 양이온성 폴리머
  예: POLYQUATERNIUM-7, POLYQUATERNIUM-10
```

### 4. 색소 명명 (Colorants)

#### CI 번호 체계
```
CI [5자리 숫자]
  └─ Colour Index 번호

예시:
CI 77891 = TITANIUM DIOXIDE (백색)
CI 77491 = IRON OXIDES (RED)
CI 77492 = IRON OXIDES (YELLOW)
CI 77499 = IRON OXIDES (BLACK)
CI 15985 = YELLOW 6 (합성)
CI 42090 = BLUE 1 (합성)
```

#### May Contain 표기
```
제품별로 다른 색소 조합 사용 시:
[+/- CI 77891, CI 77491, CI 77492, CI 77499]

의미: 제품에 따라 이 색소 중 일부 포함 가능
```

### 5. 향료 명명 (Fragrance)

#### 일반 표기
```
FRAGRANCE   ← 미국식
PARFUM      ← EU식
AROMA       ← 일부 지역

혼용 가능:
FRAGRANCE (PARFUM)
PARFUM (FRAGRANCE)
```

#### 알레르겐 향료 (EU 필수 표기)
```
EU Regulation 1223/2009에 따라 26종 알레르겐 향료
개별 표기 의무 (0.001% 초과 시 leave-on, 0.01% 초과 시 rinse-off)

LINALOOL
LIMONENE
CITRONELLOL
GERANIOL
HEXYL CINNAMAL
COUMARIN
EUGENOL
ISOEUGENOL
... (총 26종)
```

### 6. 나노물질 표기 (Nanomaterials)

```
EU 규정에 따른 나노 표기:
[INCI NAME] (NANO)

예시:
TITANIUM DIOXIDE (NANO)
ZINC OXIDE (NANO)
SILICA (NANO)

정의:
불용성/생체지속성 물질
크기: 1-100nm
집합체/응집체 크기 > 100nm도 포함
```

### 7. 특수 케이스

#### 물 (Water)
```
AQUA        ← EU 표기
WATER       ← 미국 표기
AQUA/WATER  ← 통합 표기
```

#### 혼합물
```
단일 상품의 복합 성분:
CETEARYL ALCOHOL (AND) CETEARYL GLUCOSIDE

슬래시 표기:
CAPRYLIC/CAPRIC TRIGLYCERIDE
C12-15 ALKYL BENZOATE
```

#### 명칭 변경/업데이트
```
구 명칭 → 신 명칭 예시:

TOCOPHERYL ACETATE (현행)
  ← 구: ALPHA-TOCOPHERYL ACETATE

DIMETHICONE (현행)
  ← 구: POLYDIMETHYLSILOXANE

PHENOXYETHANOL (현행)
  ← 동의어: 2-Phenoxyethanol
```

## CAS 번호 구조

### CAS 형식
```
XXXXXXX-XX-X
  │      │  │
  │      │  └─ Check digit (1자리)
  │      └──── 2자리 숫자
  └─────────── 2-7자리 숫자
```

### CAS 체크섬 검증
```python
def validate_cas(cas_number: str) -> bool:
    """
    CAS 번호 체크섬 검증

    예: 98-92-0 (Niacinamide)
    계산: (9*4) + (8*3) + (9*2) + (2*1) = 36 + 24 + 18 + 2 = 80
    80 mod 10 = 0 ✓
    """
    import re
    match = re.match(r'^(\d{2,7})-(\d{2})-(\d)$', cas_number)
    if not match:
        return False

    first_part = match.group(1)
    second_part = match.group(2)
    check_digit = int(match.group(3))

    digits = first_part + second_part
    total = sum(int(d) * (len(digits) - i) for i, d in enumerate(digits))

    return total % 10 == check_digit
```

### 복수 CAS 매핑
```
하나의 INCI = 여러 CAS 가능

예시: TOCOPHEROL
  - 59-02-9     (d-alpha-tocopherol)
  - 10191-41-0  (dl-alpha-tocopherol)
  - 54-28-4     (d-beta-tocopherol)
  - ... 이성질체별 다른 CAS

원인:
  - 이성질체 (광학, 기하)
  - 수화물/무수물
  - 염 형태
  - 공급원 차이
```

## EINECS/ELINCS 번호

### 개요
```
EINECS: European INventory of Existing Commercial chemical Substances
  - 1971-1981년 EU 시장 화학물질
  - 번호 형식: XXX-XXX-X

ELINCS: European List of Notified Chemical Substances
  - 1981년 이후 신규 등록
  - 번호 형식: 4XX-XXX-X

현재: EC 번호로 통합
```

### 예시
| INCI Name | CAS | EINECS/EC |
|-----------|-----|-----------|
| NIACINAMIDE | 98-92-0 | 202-713-4 |
| GLYCERIN | 56-81-5 | 200-289-5 |
| SODIUM CHLORIDE | 7647-14-5 | 231-598-3 |

## 자주 묻는 질문

### Q: INCI명과 화학명의 차이?
```
INCI명: 라벨 표기용 표준화된 명칭
  └─ NIACINAMIDE

화학명: 정확한 화학적 명명 (IUPAC 등)
  └─ Pyridine-3-carboxamide
  └─ 3-Pyridinecarboxylic acid amide

관계: INCI는 화학명을 기반으로 간소화
```

### Q: 새 원료의 INCI가 없으면?
```
옵션 1: PCPC에 신규 등록 신청
옵션 2: 화학명 임시 사용
옵션 3: 상품명 (비추천)

신청 시 필요 정보:
  - 화학명/구조식
  - CAS 번호 (있는 경우)
  - 제조 공정
  - 의도된 용도
```

### Q: INCI명이 변경되면?
```
구 명칭 → 신 명칭 전환 기간 존재
두 명칭 병기 가능: NEW NAME (OLD NAME)
규제 기관 가이드라인 확인 필요
```

## 관련 참조

- **PCPC INCI Dictionary**: https://www.personalcarecouncil.org/resources/inci/
- **CosIng Database**: https://ec.europa.eu/growth/tools-databases/cosing/
- **CAS Registry**: https://www.cas.org/
- **ECHA (EC Numbers)**: https://echa.europa.eu/
