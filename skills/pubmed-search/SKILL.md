---
name: pubmed-search
description: PubMed 학술 데이터베이스 검색 - 화장품 성분 관련 임상 연구 및 과학 문헌 검색 스킬
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - WebFetch
license: MIT
metadata:
  version: "1.0.0"
  category: literature-research
  region: Global
  language: en
  last-updated: "2026-01-16"
  maintainer: cosmetic-skills
  tags:
    - PubMed
    - literature-search
    - clinical-evidence
    - scientific-research
    - academic-citations
    - NCBI
    - ingredient-research
---

# PubMed Search Skill

화장품 성분 관련 학술 문헌 검색을 위한 PubMed/NCBI 데이터베이스 연동 스킬

## Overview

**PubMed**는 미국 국립의학도서관(NLM)에서 운영하는 세계 최대의 생의학 문헌 데이터베이스입니다. 3,600만 건 이상의 논문을 수록하고 있으며, 화장품 성분의 효능 및 안전성 연구에 필수적인 근거 자료를 제공합니다.

### PubMed의 특징

- **무료 접근**: API (E-utilities) 무료 제공
- **포괄성**: MEDLINE, PubMed Central, 출판사 제출 논문 포함
- **신뢰성**: 피어리뷰 학술지 논문 수록
- **최신성**: 매일 업데이트

**공식 API**: https://www.ncbi.nlm.nih.gov/books/NBK25501/

## When to Use This Skill

이 스킬은 다음과 같은 상황에서 사용합니다:

- **성분 효능 근거 수집**: 특정 성분의 임상 연구 결과 조회
- **안전성 문헌 검토**: 독성학, 자극성, 감작성 관련 연구 검색
- **임상 시험 정보**: RCT, 인체적용시험 결과 수집
- **메커니즘 연구**: 성분의 작용 기전 관련 기초 연구 검색
- **보고서 레퍼런스**: 기술 보고서용 학술 인용 수집
- **트렌드 분석**: 최근 연구 동향 파악

## Core Capabilities

### 1. 성분별 문헌 검색 (Ingredient Search)

특정 성분에 대한 PubMed 논문 검색:

```python
from pubmed_search import PubMedClient

client = PubMedClient()

# 기본 검색
results = client.search_ingredient("Niacinamide")
print(f"총 {results.total_count}건 발견")

for article in results.articles[:5]:
    print(f"- {article.title}")
    print(f"  {article.authors} ({article.year})")
    print(f"  PMID: {article.pmid}")
```

### 2. 피부과학 특화 검색 (Dermatology Focus)

화장품/피부과학 관련 논문으로 필터링:

```python
# 피부 관련 연구만 검색
results = client.search_cosmetic_ingredient(
    ingredient="Retinol",
    filters=["skin", "dermatology", "cosmetic"],
    study_types=["Clinical Trial", "RCT", "Meta-Analysis"]
)

# 특정 효능 연구 검색
efficacy_results = client.search_efficacy(
    ingredient="Vitamin C",
    efficacy="anti-aging"
)
```

### 3. 임상 시험 검색 (Clinical Trial Search)

인체 대상 임상 시험 논문 특화 검색:

```python
# 임상 시험만 검색
clinical = client.search_clinical_trials(
    ingredient="Hyaluronic Acid",
    min_participants=20,
    min_duration_weeks=4
)

for trial in clinical.trials:
    print(f"- {trial.title}")
    print(f"  N={trial.sample_size}, {trial.duration}")
    print(f"  결과: {trial.key_finding}")
```

### 4. 논문 상세 정보 조회 (Article Details)

PMID로 논문 전체 메타데이터 조회:

```python
# PMID로 상세 정보 조회
article = client.get_article_by_pmid("34567890")

print(f"제목: {article.title}")
print(f"저자: {article.authors}")
print(f"저널: {article.journal}")
print(f"발행일: {article.publication_date}")
print(f"DOI: {article.doi}")
print(f"초록: {article.abstract[:500]}...")
```

### 5. 인용 정보 생성 (Citation Generation)

학술 인용 형식 자동 생성:

```python
# 인용 형식 생성
citation = client.generate_citation(
    pmid="34567890",
    style="APA"  # APA, Vancouver, Harvard 지원
)
print(citation)
# Kim J, et al. (2023). Efficacy of Niacinamide...
# J Cosmet Dermatol. 22(3):456-467.

# In-text citation
in_text = client.get_in_text_citation("34567890")
print(f"According to {in_text}, ...")
# According to Kim et al. (2023), ...
```

### 6. 배치 검색 (Batch Search)

여러 성분 동시 검색:

```python
# 다중 성분 검색
ingredients = ["Niacinamide", "Retinol", "Vitamin C", "Hyaluronic Acid"]
batch_results = client.batch_search(ingredients)

for ingredient, results in batch_results.items():
    print(f"{ingredient}: {results.total_count}건")
```

## Search Strategies

### 화장품 성분 검색 최적화 쿼리

```python
# 기본 검색 쿼리 패턴
COSMETIC_QUERY_TEMPLATE = """
{ingredient}[Title/Abstract] AND (
    cosmetic[Title/Abstract] OR
    skin[Title/Abstract] OR
    dermatology[MeSH Terms] OR
    topical[Title/Abstract] OR
    cutaneous[Title/Abstract]
)
"""

# 효능별 검색 쿼리
EFFICACY_QUERIES = {
    "anti-aging": "aging OR wrinkle OR collagen OR elasticity",
    "brightening": "whitening OR brightening OR melanin OR pigmentation OR hyperpigmentation",
    "moisturizing": "hydration OR moisturizing OR TEWL OR barrier",
    "anti-acne": "acne OR sebum OR comedone OR pimple",
    "antioxidant": "antioxidant OR oxidative stress OR free radical"
}

# 연구 유형별 필터
STUDY_TYPE_FILTERS = {
    "clinical_trial": "Clinical Trial[Publication Type]",
    "rct": "Randomized Controlled Trial[Publication Type]",
    "meta_analysis": "Meta-Analysis[Publication Type]",
    "systematic_review": "Systematic Review[Publication Type]",
    "in_vitro": "in vitro[Title/Abstract]",
    "in_vivo": "in vivo[Title/Abstract]"
}
```

### 검색 결과 필터링

```python
# 고품질 논문 필터링
filters = {
    "min_year": 2015,           # 최근 10년
    "has_abstract": True,        # 초록 있는 논문
    "english_only": True,        # 영문 논문
    "free_full_text": False,     # PMC 전문 이용 가능
    "human_study": True,         # 인체 대상 연구
    "min_citations": 10          # 인용 10회 이상 (Semantic Scholar 연동 필요)
}

results = client.search_with_filters(
    query="Niacinamide skin",
    filters=filters
)
```

## Common Workflows

### Workflow 1: 성분 효능 근거 수집

```
1. 성분명으로 기본 검색 실행
2. 화장품/피부과학 필터 적용
3. 연구 유형별 분류 (RCT > 임상시험 > in-vivo > in-vitro)
4. 상위 10-20개 논문 상세 정보 수집
5. 주요 발견사항 요약 테이블 생성
6. 인용 정보 APA 형식으로 정리
```

### Workflow 2: 기술 보고서용 레퍼런스 수집

```
1. 제품의 Hero 성분 목록 확정 (3-5개)
2. 각 성분별 PubMed 검색 실행
3. 최신 연구 우선 정렬 (최근 5년)
4. 임상 시험 결과 우선 수집
5. 각 성분당 3-5개 핵심 논문 선별
6. 보고서용 Reference 섹션 자동 생성
```

### Workflow 3: 메커니즘 연구 조사

```
1. 성분명 + mechanism/pathway 검색
2. Review 논문 우선 검색
3. 관련 MeSH 용어 확인
4. 관련 논문 네트워크 확장
5. 주요 메커니즘 다이어그램용 정보 추출
```

## Output Formats

### 논문 메타데이터 구조

```python
@dataclass
class PubMedArticle:
    pmid: str                    # PubMed ID
    title: str                   # 논문 제목
    authors: List[str]           # 저자 목록
    first_author: str            # 제1저자
    journal: str                 # 저널명
    journal_abbrev: str          # 저널 약어
    publication_date: str        # 발행일
    year: int                    # 발행 연도
    volume: str                  # 권
    issue: str                   # 호
    pages: str                   # 페이지
    doi: str                     # DOI
    abstract: str                # 초록
    keywords: List[str]          # 키워드
    mesh_terms: List[str]        # MeSH 용어
    publication_types: List[str] # 논문 유형
    pmc_id: str                  # PMC ID (있는 경우)
    full_text_url: str           # 전문 URL (있는 경우)
```

### 검색 결과 요약 테이블

```markdown
| # | 저자 (연도) | 연구 유형 | N | 기간 | 주요 발견 | PMID |
|---|------------|----------|---|------|----------|------|
| 1 | Kim et al. (2023) | RCT | 60 | 12주 | 주름 32% 감소 | 34567890 |
| 2 | Lee et al. (2022) | Clinical | 40 | 8주 | 피부 탄력 증가 | 33456789 |
```

### Reference 형식 (APA)

```
Kim, J., Park, S., & Lee, H. (2023). Efficacy and safety of topical
niacinamide in the treatment of skin aging: A randomized controlled
trial. Journal of Cosmetic Dermatology, 22(3), 456-467.
https://doi.org/10.1111/jocd.15xxx
```

### Reference 형식 (Vancouver)

```
1. Kim J, Park S, Lee H. Efficacy and safety of topical niacinamide
in the treatment of skin aging: A randomized controlled trial.
J Cosmet Dermatol. 2023;22(3):456-67.
```

## API Reference

### NCBI E-utilities 엔드포인트

```python
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

ENDPOINTS = {
    "search": "esearch.fcgi",    # 검색 (PMID 목록 반환)
    "fetch": "efetch.fcgi",      # 상세 정보 조회
    "summary": "esummary.fcgi",  # 요약 정보 조회
    "info": "einfo.fcgi",        # DB 정보
    "link": "elink.fcgi"         # 관련 논문 링크
}

# 요청 제한
RATE_LIMIT = {
    "without_api_key": 3,        # 초당 3회
    "with_api_key": 10           # 초당 10회 (API 키 등록 시)
}
```

### API 키 설정

```python
# 환경변수로 API 키 설정 (선택사항이지만 권장)
# NCBI_API_KEY=your_api_key_here

# API 키 등록: https://www.ncbi.nlm.nih.gov/account/settings/
# 무료이며 요청 한도가 3배 증가 (3/초 → 10/초)
```

## Best Practices

### 1. 검색 쿼리 최적화

```
- MeSH 용어 활용: 정확한 의학 용어 매칭
- 필드 제한: [Title/Abstract], [MeSH Terms] 지정
- Boolean 연산자: AND, OR, NOT 활용
- 와일드카드: asterisk (*) for truncation
```

### 2. 결과 품질 관리

```
- 임상 시험 우선: RCT > Open-label > Case study
- 최신 연구 우선: 최근 5-10년 논문 선호
- 인용 횟수 참고: 영향력 있는 논문 식별
- 저널 영향력: Impact Factor 고려
```

### 3. 인용 정확성

```
- DOI 우선 사용: 영구 식별자로 가장 신뢰
- PMID 백업: DOI 없는 경우 PMID 사용
- 원문 확인: 인용 전 원문 초록 검토
- 형식 일관성: 보고서 전체 동일 인용 형식
```

## Reference Files

| File | Description |
|------|-------------|
| [references/pubmed_api.md](references/pubmed_api.md) | PubMed E-utilities API 상세 설명 |
| [references/search_strategies.md](references/search_strategies.md) | 화장품 성분 검색 전략 가이드 |
| [references/mesh_cosmetic.md](references/mesh_cosmetic.md) | 화장품 관련 MeSH 용어 목록 |
| [scripts/pubmed_search.py](scripts/pubmed_search.py) | Python PubMed 클라이언트 구현 |

## Related Resources

- **PubMed 공식**: https://pubmed.ncbi.nlm.nih.gov/
- **NCBI E-utilities**: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- **MeSH Browser**: https://meshb.nlm.nih.gov/
- **PubMed Central**: https://www.ncbi.nlm.nih.gov/pmc/
- **Semantic Scholar API**: https://api.semanticscholar.org/ (인용 횟수)

## Integration with Other Skills

### clinical-evidence-aggregator 연동
- PubMed 검색 결과를 증거 테이블로 변환
- 연구 유형별 증거 수준 자동 분류

### reference-manager 연동
- 검색 결과를 참고문헌 목록으로 정리
- In-text citation 자동 생성

### ingredient-deep-dive 연동
- 성분별 심층 분석에 학술 근거 제공
- 메커니즘 연구 자료 자동 수집

## Usage Examples

### 기본 성분 검색
```
"나이아신아마이드 PubMed 검색해줘"
→ 총 2,847건 발견
→ 피부 관련 연구 1,234건
→ 최근 5년 임상 시험 89건
→ [상위 10개 논문 목록 출력]
```

### 효능별 검색
```
"비타민 C 미백 효과 임상 연구 찾아줘"
→ "Ascorbic Acid" AND "brightening OR whitening OR melanin" 검색
→ 임상 시험 필터 적용
→ [미백 효능 임상 연구 목록]
```

### 레퍼런스 생성
```
"레티놀 관련 논문 5개 APA 형식으로 인용 생성해줘"
→ [최신 고품질 논문 5개 선별]
→ [APA 형식 Reference 출력]
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-16 | Initial release with PubMed E-utilities integration |
