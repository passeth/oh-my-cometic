---
name: reference-manager
description: K-Dense 보고서용 학술 참고문헌 관리 및 인용 생성 스킬
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - WebFetch
license: MIT
metadata:
  version: "1.0.0"
  category: documentation
  region: Global
  language: ko/en
  last-updated: "2026-01-16"
  maintainer: cosmetic-skills
  tags:
    - citation
    - reference
    - bibliography
    - academic
    - formatting
---

# Reference Manager Skill

K-Dense 수준의 기술 보고서를 위한 학술 참고문헌 관리 스킬

## Overview

**Reference Manager**는 화장품 기술 보고서에 필요한 학술 참고문헌을 체계적으로 관리하고, 다양한 인용 형식으로 변환하는 스킬입니다. PubMed, CrossRef 등의 데이터베이스와 연동하여 메타데이터를 자동 수집하고, APA, Vancouver 등 표준 형식으로 인용을 생성합니다.

### 주요 기능

- **자동 메타데이터 수집**: DOI, PMID로 논문 정보 자동 가져오기
- **다중 인용 형식**: APA 7th, Vancouver, ACS, Harvard 지원
- **인용 번호 관리**: 본문 내 인용 번호 자동 관리
- **참고문헌 목록 생성**: 표준 형식의 Bibliography 자동 생성
- **중복 검사**: 동일 참고문헌 중복 방지
- **내보내기**: BibTeX, RIS, EndNote 형식 지원

## When to Use This Skill

이 스킬은 다음과 같은 상황에서 사용합니다:

- **기술 보고서**: 참고문헌 섹션 생성
- **심사 자료**: 기능성 화장품 인용 형식 관리
- **마케팅 자료**: 과학적 근거 인용 관리
- **프레젠테이션**: 출처 명시
- **문헌 정리**: 연구 자료 체계화

## Core Capabilities

### 1. 참고문헌 추가

```python
from reference_manager import ReferenceManager

manager = ReferenceManager()

# DOI로 추가
ref1 = manager.add_by_doi("10.1111/bjd.12345")

# PMID로 추가
ref2 = manager.add_by_pmid("12345678")

# 수동 추가
ref3 = manager.add_manual(
    authors=["Kim HJ", "Lee SY"],
    title="Effects of niacinamide on skin barrier function",
    journal="J Cosmet Dermatol",
    year=2023,
    volume="22",
    issue="3",
    pages="123-130",
    doi="10.1111/jcd.12345"
)
```

### 2. 인용 형식 변환

```python
# APA 7th Edition
apa_citation = manager.format(ref1, style="apa7")
# Kim, H. J., & Lee, S. Y. (2023). Effects of niacinamide...

# Vancouver Style
vancouver_citation = manager.format(ref1, style="vancouver")
# Kim HJ, Lee SY. Effects of niacinamide... J Cosmet Dermatol. 2023;22(3):123-130.

# ACS Style
acs_citation = manager.format(ref1, style="acs")
# Kim, H. J.; Lee, S. Y. J. Cosmet. Dermatol. 2023, 22, 123-130.

# Harvard Style
harvard_citation = manager.format(ref1, style="harvard")
# Kim, HJ & Lee, SY 2023, 'Effects of niacinamide...', Journal of Cosmetic Dermatology...
```

### 3. 인용 번호 관리

```python
# 본문 내 인용 삽입
text = """
Niacinamide has been shown to improve skin barrier function [cite:kim2023].
Multiple studies confirm its efficacy in brightening [cite:lee2022, park2021].
"""

# 인용 번호 자동 할당
formatted_text = manager.process_citations(text)
# "Niacinamide has been shown to improve skin barrier function [1]."
# "Multiple studies confirm its efficacy in brightening [2,3]."

# 참고문헌 목록 생성
bibliography = manager.generate_bibliography(style="vancouver")
```

### 4. 참고문헌 목록 생성

```python
# 전체 참고문헌 목록
bibliography = manager.generate_bibliography(
    style="vancouver",
    sort_by="citation_order",  # citation_order, author, year
    language="ko",  # 한국어 형식
    numbering=True  # 번호 포함
)

print(bibliography)
```

출력 예시:
```
## References

1. Kim HJ, Lee SY. Effects of niacinamide on skin barrier function.
   J Cosmet Dermatol. 2023;22(3):123-130.
2. Lee KS, Park MJ. Clinical efficacy of niacinamide on hyperpigmentation.
   Skin Res Technol. 2022;28(5):456-462.
3. Park JY, Kim SH, Choi EH. Open-label study of niacinamide effects on skin tone.
   Ann Dermatol. 2021;33(4):234-240.
```

### 5. 내보내기

```python
# BibTeX 형식
bibtex = manager.export(format="bibtex")

# RIS 형식
ris = manager.export(format="ris")

# EndNote XML
endnote = manager.export(format="endnote")

# CSV
csv = manager.export(format="csv")

# JSON
json_refs = manager.export(format="json")
```

## Citation Styles

### Vancouver Style (권장)

의학/과학 분야 표준. K-Dense 보고서 기본 형식.

```
Kim HJ, Lee SY. Effects of niacinamide on skin barrier function.
J Cosmet Dermatol. 2023;22(3):123-130. doi:10.1111/jcd.12345
```

**특징**:
- 저자명: 성 + 이니셜
- 저자 6명 이상: "et al." 사용
- 연도 위치: 제목 후
- 약어: 저널명 MEDLINE 약어

### APA 7th Edition

심리학, 사회과학 분야 표준.

```
Kim, H. J., & Lee, S. Y. (2023). Effects of niacinamide on skin barrier
function. Journal of Cosmetic Dermatology, 22(3), 123-130.
https://doi.org/10.1111/jcd.12345
```

**특징**:
- 저자명: 성, 이니셜.
- 연도 위치: 저자 후 괄호
- 저널명: 이탤릭체
- DOI: URL 형식

### ACS Style

화학 분야 표준.

```
Kim, H. J.; Lee, S. Y. J. Cosmet. Dermatol. 2023, 22, 123-130.
```

**특징**:
- 저자 구분: 세미콜론
- 저널명: 축약
- 권호: 이탤릭

### Harvard Style

영국/호주 학술 표준.

```
Kim, HJ & Lee, SY 2023, 'Effects of niacinamide on skin barrier function',
Journal of Cosmetic Dermatology, vol. 22, no. 3, pp. 123-130.
```

## Reference Data Structure

### Reference 객체

```python
@dataclass
class Reference:
    id: str                      # 고유 식별자
    ref_type: ReferenceType      # journal_article, book, etc.
    authors: List[Author]        # 저자 목록
    title: str                   # 제목
    journal: Optional[str]       # 저널명
    year: int                    # 출판년도
    volume: Optional[str]        # 권
    issue: Optional[str]         # 호
    pages: Optional[str]         # 페이지
    doi: Optional[str]           # DOI
    pmid: Optional[str]          # PubMed ID
    url: Optional[str]           # URL
    abstract: Optional[str]      # 초록
    keywords: List[str]          # 키워드
    citation_key: str            # 인용 키 (예: kim2023)
    citation_number: Optional[int]  # 인용 번호
```

### Author 객체

```python
@dataclass
class Author:
    family: str      # 성
    given: str       # 이름
    orcid: Optional[str] = None  # ORCID

    def format_apa(self) -> str:
        return f"{self.family}, {self.given[0]}."

    def format_vancouver(self) -> str:
        initials = "".join([n[0] for n in self.given.split()])
        return f"{self.family} {initials}"
```

## Integration

### pubmed-search 연동

```python
from pubmed_search import PubMedClient
from reference_manager import ReferenceManager

pubmed = PubMedClient()
manager = ReferenceManager()

# PubMed 검색 결과를 참고문헌으로 추가
results = pubmed.search("niacinamide skin", limit=10)
for result in results:
    manager.add_by_pmid(result["pmid"])
```

### clinical-evidence-aggregator 연동

```python
from clinical_evidence_aggregator import EvidenceAggregator
from reference_manager import ReferenceManager

aggregator = EvidenceAggregator()
manager = ReferenceManager()

# 근거 테이블의 연구들을 참고문헌에 추가
evidence = aggregator.aggregate(ingredient="Niacinamide")
for study in evidence.studies:
    if study.pmid:
        manager.add_by_pmid(study.pmid)
    elif study.doi:
        manager.add_by_doi(study.doi)
```

### ingredient-deep-dive 연동

```python
from ingredient_deep_dive import DeepDiveGenerator
from reference_manager import ReferenceManager

deep_dive = DeepDiveGenerator()
manager = ReferenceManager()

# Deep-dive 리포트에 참고문헌 추가
report = deep_dive.generate(ingredient="Niacinamide")
bibliography = manager.generate_bibliography(style="vancouver")
report.references = bibliography
```

## K-Dense Report Integration

### 인용 워크플로우

```python
# 1. 연구 수집
manager = ReferenceManager()
for pmid in research_pmids:
    manager.add_by_pmid(pmid)

# 2. 본문 작성 시 인용
text = """
나이아신아마이드는 피부 장벽 기능 개선에 효과적인 것으로
입증되었다 [cite:kim2023]. 멜라노좀 전달 억제를 통한
미백 효과도 다수의 연구에서 확인되었다 [cite:lee2022, park2021].
"""

# 3. 최종 문서 생성
formatted_text = manager.process_citations(text)
bibliography = manager.generate_bibliography(style="vancouver")

final_document = f"""
{formatted_text}

## 참고문헌

{bibliography}
"""
```

### K-Dense 템플릿 적용

```python
# K-Dense 보고서 참고문헌 섹션 템플릿
template = """
## 참고문헌 (References)

### 임상 연구
{clinical_refs}

### 기전 연구
{mechanism_refs}

### 규제/가이드라인
{regulatory_refs}
"""

# 카테고리별 분류
clinical_refs = manager.filter_by_category("clinical")
mechanism_refs = manager.filter_by_category("mechanism")
regulatory_refs = manager.filter_by_category("regulatory")
```

## Best Practices

### 1. 일관된 형식 유지

```
권장사항:
- 전체 문서에 단일 인용 스타일 사용
- K-Dense 보고서: Vancouver 스타일 권장
- 모든 DOI 포함
- 저널명 약어 일관성
```

### 2. 신뢰할 수 있는 출처

```
우선순위:
1. PubMed 인덱싱 저널
2. Peer-reviewed 학술지
3. 공인 기관 가이드라인
4. 교과서/전문 서적
5. 신뢰할 수 있는 웹사이트

피해야 할 출처:
- 비학술 웹사이트
- 미검토 preprint (단독 인용)
- 상업적 자료 (단독 인용)
```

### 3. 인용 윤리

```
- 원저자 정확히 인용
- 2차 인용 명시
- 이해충돌 확인
- 철회 논문 확인
```

## Reference Files

| File | Description |
|------|-------------|
| [references/citation_styles.md](references/citation_styles.md) | 인용 스타일 상세 |
| [references/journal_abbreviations.md](references/journal_abbreviations.md) | 화장품 관련 저널 약어 |
| [scripts/reference_manager.py](scripts/reference_manager.py) | Python 구현체 |

## Usage Examples

### 기본 사용

```
"이 연구들의 참고문헌을 Vancouver 형식으로 정리해줘"
→ [형식화된 참고문헌 목록]
```

### DOI로 추가

```
"DOI 10.1111/bjd.12345 참고문헌에 추가해줘"
→ [메타데이터 자동 수집 + 추가]
```

### 인용 번호 처리

```
"본문의 인용을 번호로 바꾸고 참고문헌 목록 만들어줘"
→ [인용 번호 할당 + Bibliography 생성]
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-16 | Initial release |
