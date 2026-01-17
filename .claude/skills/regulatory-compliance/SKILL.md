---
name: regulatory-compliance
description: 국가별 화장품 규제 준수 가이드. 한국(MFDS), EU(EC 1223/2009), 미국(FDA), 중국(NMPA), ASEAN(ACD) 등 주요 시장의 규제 요건, 등록 절차, 성분 제한을 종합적으로 안내. 해외 수출, 규제 검토, 인허가 준비에 사용.
allowed-tools: [Read, Write, Edit, Bash, WebFetch]
license: MIT license
metadata:
    skill-author: EVAS Cosmetic
    original-source: K-Dense Inc. (claude-scientific-skills structure)
    version: 1.0.0
    last-updated: 2025-01-16
---

# Regulatory Compliance Skill

## Overview

화장품의 국제 규제 환경은 국가마다 상이하며, 수출을 위해서는 각 시장의 규제 체계를 정확히 이해해야 합니다. 이 스킬은 **5대 주요 화장품 시장**의 규제 요건을 종합적으로 제공합니다.

| 시장 | 규제 기관 | 핵심 법령 | 특징 |
|------|-----------|-----------|------|
| **한국** | MFDS (식약처) | 화장품법 | 기능성 화장품 심사제 |
| **EU** | EC Commission | EC 1223/2009 | 사전 통지제 (CPNP) |
| **미국** | FDA | FD&C Act | 자율 규제 기반 |
| **중국** | NMPA | 화장품감독관리조례 | 등록/비안 이원화 |
| **ASEAN** | ACD | ASEAN Cosmetic Directive | 상호 인증 체계 |

## When to Use This Skill

- **해외 수출 준비**: 목표 시장의 규제 요건 파악
- **신제품 개발**: 글로벌 규제 적합성 사전 검토
- **규제 변경 대응**: 주요 시장 규정 업데이트 모니터링
- **등록/인허가**: 국가별 등록 절차 및 서류 요건 확인
- **성분 검토**: 국가별 금지/제한 물질 비교
- **라벨링 검토**: 국가별 표시 기준 확인

## Core Capabilities

### 1. 한국 (MFDS - 식품의약품안전처)

한국은 **기능성 화장품** 개념을 운영하는 대표적 시장입니다.

#### 규제 체계
```
화장품법
├── 화장품법 (법률)
├── 화장품법 시행령 (대통령령)
├── 화장품법 시행규칙 (총리령)
└── 화장품 안전기준 등에 관한 규정 (고시)
```

#### 화장품 분류
| 분류 | 정의 | 규제 방식 |
|------|------|-----------|
| **일반화장품** | 피부/모발의 청결, 미화 | 사후 관리 |
| **기능성화장품** | 피부 미백, 주름 개선, 자외선차단 등 | **사전 심사/보고** |

#### 기능성 화장품 유형 (13가지)
1. 피부 미백
2. 피부 주름 개선
3. 자외선 차단
4. 피부 탄력 개선
5. 모발의 색상 변화/제거/탈염
6. 체모 제거
7. 여드름 피부 완화
8. 아토피 피부 보습
9. 탈모 증상 완화
10. 튼살로 인한 붉은 선 완화
11. 체취 방지
12. 피부장벽 기능 회복을 통한 가려움 완화
13. 비듬/가려움을 완화시키는 모발용

#### 기능성 화장품 심사 유형
```python
FUNCTIONAL_COSMETIC_REVIEW_TYPES = {
    "품목허가": {
        "대상": "신규 성분/배합",
        "심사기간": "약 60일",
        "요건": "안전성/유효성 자료 제출"
    },
    "품목신고": {
        "대상": "고시 원료 사용",
        "심사기간": "약 10일",
        "요건": "기준규격 준수 확인"
    },
    "보고": {
        "대상": "자외선차단제 (고시 성분)",
        "심사기간": "즉시",
        "요건": "온라인 제출"
    }
}
```

#### 안전기준
```
화장품 안전기준 등에 관한 규정
├── 별표 1: 사용할 수 없는 원료 (1,500여 종)
├── 별표 2: 사용 제한 원료 (약 100종)
├── 별표 3: 인체 세포/조직 배양액 안전기준
├── 별표 4: 타르색소 종류 및 기준
├── 별표 5: 중금속/미생물 기준
└── 별표 6: 내용량 기준
```

#### 전성분 표시 기준
- **INCI명** 또는 **한글 표준화 성분명** 사용
- 함량 순 또는 1% 미만은 순서 무관
- 착향제는 "향료"로 표기 가능
- 나노물질: "(나노)" 접미사 필수

**참조**: `references/korea_mfds.md`

---

### 2. EU (European Commission)

EU는 **Regulation (EC) 1223/2009**를 통해 세계에서 가장 체계적인 화장품 규제를 운영합니다.

#### 핵심 개념
| 개념 | 설명 |
|------|------|
| **Responsible Person (RP)** | EU 내 법적 책임자 (제조사 또는 수입자) |
| **CPSR** | Cosmetic Product Safety Report (안전성 평가서) |
| **CPNP** | Cosmetic Products Notification Portal (통지 포털) |
| **PIF** | Product Information File (제품 정보 파일) |

#### 규제 절차
```
EU 화장품 출시 절차
│
├── 1. Responsible Person 지정
│   └── EU 내 법인 또는 지정 대리인
│
├── 2. CPSR 작성
│   ├── Part A: 안전성 정보
│   └── Part B: 안전성 평가 (자격자 서명)
│
├── 3. PIF 구성
│   ├── 제품 설명 및 CPSR
│   ├── 제조방법 기술서
│   ├── GMP 적합성 증명
│   ├── 효능 입증 자료
│   └── 동물실험 데이터 (기존 자료만)
│
├── 4. CPNP 등록
│   └── 시장 출시 전 완료
│
└── 5. 시장 출시
    └── 사후 감시 (Post-market surveillance)
```

#### Annex 체계
| Annex | 내용 | 물질 수 |
|-------|------|---------|
| **Annex II** | 금지 물질 | ~1,400+ |
| **Annex III** | 제한 물질 | ~300+ |
| **Annex IV** | 허용 색소 | ~150 |
| **Annex V** | 허용 방부제 | ~59 |
| **Annex VI** | 허용 UV 필터 | ~28 |

#### 나노물질 규정
- 정의: 1-100nm 입자가 50% 이상
- 사전통지: 시장 출시 6개월 전 EC 통지
- 라벨: `[INCI] (NANO)` 표기 필수

**참조**: `references/eu_regulation.md`

---

### 3. 미국 (FDA - Food and Drug Administration)

미국은 **자율 규제** 기반이지만, Drug으로 분류되면 엄격한 규제가 적용됩니다.

#### Cosmetic vs Drug 구분

| 기준 | Cosmetic | Drug (OTC) |
|------|----------|------------|
| **정의** | 신체 미화/청결/외관 변화 | 질병 치료/예방, 신체 구조/기능 영향 |
| **사전 승인** | 불필요 | **필수** (NDA 또는 Monograph) |
| **GMP** | 권고 | **의무** |
| **라벨** | FD&C Act 준수 | FDA 규정 준수 |
| **등록** | VCRP (자발적) | 의무 등록 |

#### Cosmetic으로 분류되는 제품
- 스킨케어 (클렌저, 보습제, 토너 등)
- 색조 화장품 (립스틱, 파운데이션 등)
- 헤어케어 (샴푸, 컨디셔너, 염모제 등)
- 향수, 네일 폴리시

#### Drug으로 분류되는 제품
```python
OTC_DRUG_CATEGORIES = {
    "자외선차단제": "Sunscreen Monograph (21 CFR 352)",
    "여드름 치료": "Acne Monograph (21 CFR 333.310)",
    "비듬 샴푸": "Dandruff Monograph (21 CFR 358)",
    "탈모 치료": "Hair Loss Monograph (21 CFR 310.527)",
    "피부 미백": "Skin Bleaching (21 CFR 310.545)",
    "발한 억제": "Antiperspirant Monograph (21 CFR 350)"
}
```

#### 중요 규정
- **색소 인증**: FD&C/D&C 색소는 FDA 인증 필수
- **금지/제한 물질**: 21 CFR 700 시리즈
- **경고 문구**: 특정 성분 사용 시 필수
- **동물실험**: 금지하지 않음 (캘리포니아 등 주 단위 규제 있음)

#### MoCRA (Modernization of Cosmetics Regulation Act of 2022)
2022년 12월 시행된 신규 규제:
- **시설 등록**: 2년마다 의무 등록
- **제품 리스팅**: 모든 화장품 FDA 리스팅
- **부작용 보고**: 심각한 부작용 15일 내 보고
- **GMP**: FDA GMP 가이드라인 준수
- **라벨**: 향료 알레르겐 표시 요건

**참조**: `references/us_fda.md`

---

### 4. 중국 (NMPA - 국가약품감독관리국)

중국은 **등록(주책)/비안(신고)** 이원화 체계를 운영합니다.

#### 화장품 분류
| 분류 | 등록 방식 | 심사 기간 | 대상 |
|------|-----------|-----------|------|
| **일반 화장품** | 비안 (备案) | ~5일 | 기초화장품, 색조 등 |
| **특수 화장품** | 주책 (注册) | 3-6개월 | 아래 9종 |

#### 특수 화장품 9종
1. 염발/탈염 제품
2. 파마 제품
3. 피부 미백
4. 자외선차단
5. 탈모 방지
6. 체취 방지
7. 여드름 치료
8. 제모
9. 가슴 미용

#### CSAR (Cosmetic Safety Assessment Report)
2021년부터 시행된 새로운 안전성 평가 체계:
```
CSAR 구성
├── 안전성 위험물질 식별
├── 노출 평가
├── 용량-반응 평가
├── 위험 특성화
└── 안전성 결론
```

#### 동물시험 요건
| 제품 유형 | 동물시험 | 비고 |
|-----------|----------|------|
| 일반 화장품 (국내 생산) | 면제 | 2021년 5월부터 |
| 일반 화장품 (수입) | **면제 가능** | 조건 충족 시 |
| 특수 화장품 | **필수** | 대부분 요구 |
| 영유아용 | **필수** | 추가 테스트 |

#### 동물시험 면제 조건 (일반 화장품)
1. 안전성 평가 자료 제출
2. GMP 인증 획득
3. 3년간 무부작용 이력
4. 원료 안전성 자료

**참조**: `references/china_nmpa.md`

---

### 5. ASEAN (ASEAN Cosmetic Directive)

ASEAN 10개국은 **ASEAN Cosmetic Directive (ACD)**를 통해 규제를 통일화하고 있습니다.

#### 회원국
```
브루나이, 캄보디아, 인도네시아, 라오스, 말레이시아,
미얀마, 필리핀, 싱가포르, 태국, 베트남
```

#### ACD 핵심 원칙
- EU EC 1223/2009를 기반으로 함
- **상호 인증 체계**: 한 국가 등록으로 타국 진출 용이
- **통일된 성분 목록**: 금지/제한 물질 공유

#### 국가별 등록 기관
| 국가 | 규제 기관 | 등록 시스템 |
|------|-----------|-------------|
| 인도네시아 | BPOM | e-Registration |
| 태국 | Thai FDA | e-Submission |
| 베트남 | MOH | Online Portal |
| 필리핀 | FDA Philippines | e-Registration |
| 말레이시아 | NPRA | QUEST3+ |
| 싱가포르 | HSA | PRISM |

#### ASEAN Cosmetic Claim Guideline
허용/금지 클레임 통일 기준:
- **허용**: 미용적 효과, 피부 보습, 피부 진정
- **금지**: 의약품적 효능, 질병 치료/예방
- **조건부**: 자외선차단 (SPF 테스트 필수)

**참조**: `references/asean_ahc.md`

---

## Regulatory Matrix

### 주요 규제 항목 비교

| 항목 | 한국 | EU | 미국 | 중국 | ASEAN |
|------|------|-----|------|------|-------|
| **사전 승인** | 기능성만 | 불필요 | Drug만 | 특수만 | 불필요 |
| **통지/등록** | 영업신고 | CPNP | MoCRA | 비안/주책 | 국가별 |
| **안전성 평가** | 기능성만 | CPSR 필수 | 권고 | CSAR | 자체평가 |
| **GMP** | 권장 | 의무 | MoCRA로 의무화 | CGMP 의무 | 권장 |
| **동물시험** | 금지 | 금지 | 허용 | 조건부 | 권장 안함 |
| **라벨 언어** | 한글 | 현지어 | 영어 | 중문 | 현지어 |

### 성분 규제 비교 (주요 성분)

```
성분별 국가별 허용 농도 비교
└── 상세표: assets/regulatory_matrix.md 참조
```

---

## Common Workflows

### Workflow 1: 수출 시장 진입 검토

새로운 시장 진입 시 규제 적합성 사전 평가:

```python
def assess_market_entry(product_info: dict, target_markets: list) -> dict:
    """
    수출 시장 진입 가능성 평가

    Args:
        product_info: {
            "category": "skincare",
            "claims": ["moisturizing", "whitening"],
            "ingredients": [...],
            "is_functional_kr": True
        }
        target_markets: ["EU", "US", "CN"]

    Returns:
        {
            "EU": {
                "feasibility": "HIGH",
                "requirements": [...],
                "timeline": "3-6 months",
                "estimated_cost": "€5,000-10,000"
            },
            ...
        }
    """
    results = {}

    for market in target_markets:
        # 1. 제품 분류 확인
        classification = classify_product(product_info, market)

        # 2. 성분 규제 확인
        ingredient_check = check_ingredients(product_info["ingredients"], market)

        # 3. 클레임 적합성 확인
        claim_check = verify_claims(product_info["claims"], market)

        # 4. 등록 요건 및 비용 산정
        requirements = get_registration_requirements(classification, market)

        results[market] = {
            "classification": classification,
            "ingredient_issues": ingredient_check,
            "claim_issues": claim_check,
            "requirements": requirements
        }

    return results
```

### Workflow 2: 성분 규제 다중 국가 검토

특정 성분의 다중 국가 규제 상태 확인:

```python
def check_ingredient_multi_country(inci_name: str, markets: list = None) -> dict:
    """
    성분의 다중 국가 규제 상태 확인

    Args:
        inci_name: INCI 성분명
        markets: 확인할 시장 (기본: 전체)

    Returns:
        {
            "RETINOL": {
                "KR": {"status": "RESTRICTED", "max_conc": "0.5%", "notes": "기능성 원료"},
                "EU": {"status": "RESTRICTED", "max_conc": "0.3%", "notes": "Annex III"},
                "US": {"status": "ALLOWED", "max_conc": None, "notes": "No limit"},
                "CN": {"status": "RESTRICTED", "max_conc": "0.5%", "notes": "특수화장품"},
                "ASEAN": {"status": "RESTRICTED", "max_conc": "0.3%", "notes": "EU 기준"}
            }
        }
    """
    if markets is None:
        markets = ["KR", "EU", "US", "CN", "ASEAN"]

    result = {}
    for market in markets:
        result[market] = get_ingredient_status(inci_name, market)

    return result
```

### Workflow 3: 규제 변경 모니터링

주요 시장의 규제 변경 사항 추적:

```python
def monitor_regulatory_updates(markets: list = None, since_date: str = None) -> list:
    """
    규제 변경 사항 모니터링

    Returns:
        [
            {
                "market": "EU",
                "regulation": "EU 2024/xxx",
                "effective_date": "2024-07-01",
                "type": "ANNEX_UPDATE",
                "summary": "New restrictions on...",
                "affected_ingredients": ["..."],
                "action_required": "Reformulate by 2025-01-01"
            }
        ]
    """
    pass
```

### Workflow 4: 등록 서류 체크리스트

시장별 등록 서류 목록 생성:

```python
def generate_registration_checklist(
    product_category: str,
    target_market: str
) -> dict:
    """
    등록 서류 체크리스트 생성

    Example for EU:
    {
        "market": "EU",
        "documents": [
            {"name": "CPSR", "required": True, "notes": "Qualified assessor 필요"},
            {"name": "PIF", "required": True, "notes": "RP 보관"},
            {"name": "GMP Certificate", "required": True, "notes": "ISO 22716"},
            {"name": "Label Artwork", "required": True, "notes": "현지어"},
            {"name": "CPNP Registration", "required": True, "notes": "온라인"},
            {"name": "Efficacy Data", "required": False, "notes": "클레임 있는 경우"}
        ],
        "estimated_timeline": "3-6 months",
        "estimated_cost": "€5,000-15,000"
    }
    """
    pass
```

---

## Best Practices

### 1. 글로벌 처방 설계
- 가장 엄격한 규제 기준으로 처방 설계 (EU 기준 권장)
- 국가별 금지 성분 사전 배제
- 농도 제한은 최저 기준 적용

### 2. 규제 정보 업데이트
- 공식 소스에서 규제 정보 확인
- 업데이트 발효일과 경과 조치 확인
- 정기적인 처방 규제 적합성 재검토

### 3. 전문가 협력
- 현지 RA (Regulatory Affairs) 컨설턴트 활용
- 규제 해석 불확실 시 규제 기관 사전 상담
- 산업 협회 가이드라인 참조

### 4. 문서 관리
- 모든 규제 관련 문서 버전 관리
- 등록 이력 및 갱신 일정 관리
- 규제 변경 대응 기록 유지

---

## Reference Files

상세 정보는 아래 참조 문서 확인:

| 파일 | 내용 |
|------|------|
| `references/korea_mfds.md` | 한국 화장품법 및 기능성 화장품 상세 |
| `references/eu_regulation.md` | EU EC 1223/2009 및 CPNP 절차 |
| `references/us_fda.md` | 미국 FDA 규제 및 OTC Monograph |
| `references/china_nmpa.md` | 중국 NMPA 등록/비안 및 CSAR |
| `references/asean_ahc.md` | ASEAN ACD 및 국가별 차이 |
| `assets/regulatory_matrix.md` | 국가별 규제 비교 매트릭스 |

---

## Troubleshooting

### 문제: 성분이 특정 국가에서 금지됨
```
해결 방법:
1. 대체 성분 검토 (cosing-database 스킬 활용)
2. 국가별 처방 차별화 검토
3. 규제 면제 조건 확인
4. 해당 국가 수출 포기 검토
```

### 문제: 클레임이 국가별로 상충
```
해결 방법:
1. 가장 보수적인 클레임 채택
2. 국가별 라벨/마케팅 자료 차별화
3. 클레임 입증 자료 추가 확보
4. 현지 RA 컨설턴트 자문
```

### 문제: 등록 기간이 예상보다 길어짐
```
해결 방법:
1. 서류 불비 사항 신속 보완
2. 규제 기관 담당자와 커뮤니케이션
3. 현지 에이전트 활용
4. 등록 유형 변경 검토 (예: 중국 비안→주책)
```

---

## Additional Resources

### 공식 규제 기관
- **한국 MFDS**: https://www.mfds.go.kr
- **EU Commission**: https://ec.europa.eu/growth/sectors/cosmetics
- **US FDA**: https://www.fda.gov/cosmetics
- **중국 NMPA**: https://www.nmpa.gov.cn
- **ASEAN Secretariat**: https://asean.org

### 업계 자료
- **Cosmetics Europe**: https://cosmeticseurope.eu
- **Personal Care Products Council (US)**: https://www.personalcarecouncil.org
- **대한화장품협회**: https://www.kcia.or.kr
- **중국화장품협회**: http://www.chinaccia.org

### 규제 정보 서비스
- **Chemlinked**: https://cosmetic.chemlinked.com
- **Cosmetics Design**: https://www.cosmeticsdesign.com
- **C&T (Cosmetics & Toiletries)**: https://www.cosmeticsandtoiletries.com

---

## Summary

**regulatory-compliance** 스킬은 글로벌 화장품 수출의 필수 가이드입니다:

1. **한국**: 기능성 화장품 심사/신고/보고 체계 이해
2. **EU**: CPSR, CPNP, RP 체계 및 Annex 준수
3. **미국**: Cosmetic vs Drug 구분, MoCRA 대응
4. **중국**: 비안/주책 이원화, CSAR, 동물시험 면제 조건
5. **ASEAN**: ACD 통일 기준 및 국가별 차이

글로벌 시장 진출 시 각 국가의 규제 특성을 이해하고, 최적의 등록 전략을 수립하는 데 활용하세요.
