---
name: clinical-evidence-aggregator
description: 화장품 성분의 임상 근거를 수집, 평가, 테이블화하는 스킬 - K-Dense 수준의 근거 요약 생성
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - WebFetch
  - Task
license: MIT
metadata:
  version: "1.0.0"
  category: evidence-synthesis
  region: Global
  language: ko/en
  last-updated: "2026-01-16"
  maintainer: cosmetic-skills
  tags:
    - clinical-evidence
    - evidence-table
    - study-synthesis
    - evidence-grading
    - systematic-review
---

# Clinical Evidence Aggregator Skill

화장품 성분의 임상 연구 근거를 체계적으로 수집, 평가, 요약하는 스킬

## Overview

**Clinical Evidence Aggregator**는 화장품 활성 성분의 효능을 뒷받침하는 임상 연구를 수집하고, 표준화된 형식으로 정리하여 K-Dense 수준의 근거 테이블을 생성합니다. PubMed, ClinicalTrials.gov 등의 데이터 소스와 연동하여 최신 연구 정보를 반영합니다.

### 주요 기능

- **연구 수집**: PubMed 검색 결과 자동 수집
- **품질 평가**: 연구 품질 자동 평가 (Jadad score 등)
- **근거 등급화**: A-E 등급 자동 산정
- **테이블 생성**: 표준화된 근거 테이블 출력
- **요약 생성**: 연구 결과 종합 요약문 작성

## When to Use This Skill

이 스킬은 다음과 같은 상황에서 사용합니다:

- **기술 보고서**: 성분 효능의 임상적 근거 섹션
- **클레임 지원**: 마케팅 클레임의 과학적 뒷받침
- **원료 평가**: 신규 원료의 근거 수준 검토
- **규제 대응**: 기능성 화장품 심사 자료
- **경쟁 분석**: 경쟁 성분 대비 근거 비교

## Core Capabilities

### 1. 기본 근거 수집

```python
from clinical_evidence_aggregator import EvidenceAggregator

aggregator = EvidenceAggregator()

# 성분별 근거 수집
evidence = aggregator.aggregate(
    ingredient="Niacinamide",
    efficacy="brightening",  # 특정 효능 필터
    min_studies=5,           # 최소 연구 수
    study_types=["RCT", "Clinical Trial"],  # 연구 유형 필터
    year_range=(2015, 2025)  # 출판 연도 범위
)

print(evidence.to_table())
```

### 2. 연구 품질 평가

```python
# 개별 연구 품질 평가
quality = aggregator.assess_quality(study)
print(f"Jadad Score: {quality.jadad_score}")
print(f"Risk of Bias: {quality.bias_risk}")
print(f"Sample Size Adequacy: {quality.sample_adequacy}")
```

### 3. 근거 등급 산정

```python
# 종합 근거 등급 계산
grade = aggregator.calculate_evidence_grade(evidence)
print(f"Evidence Grade: {grade.grade}")  # A, B, C, D, E
print(f"Justification: {grade.justification}")
print(f"Confidence: {grade.confidence_level}")
```

### 4. 근거 테이블 생성

```python
# 표준 근거 테이블
table = evidence.to_table(
    format="markdown",  # markdown, html, latex
    columns=["study", "year", "design", "n", "duration",
             "concentration", "key_finding", "quality"],
    sort_by="year",
    language="ko"
)
```

### 5. 종합 요약문 생성

```python
# 근거 요약문 자동 생성
summary = aggregator.generate_summary(
    evidence,
    style="technical",  # technical, marketing, regulatory
    length="medium"     # short, medium, long
)
```

## Output Formats

### Evidence Table (Markdown)

```markdown
## Niacinamide 미백 효능 임상 근거

| Study | Year | Design | N | Duration | Conc. | Key Finding | Quality |
|-------|------|--------|---|----------|-------|-------------|---------|
| Kim et al. | 2023 | DB-RCT | 60 | 12주 | 5% | ITA° +4.2 (p<0.01) | High |
| Lee et al. | 2022 | RCT | 45 | 8주 | 4% | 색소 면적 -23% | High |
| Park et al. | 2021 | Open | 30 | 8주 | 5% | 주관적 개선 82% | Medium |

**Evidence Grade: B**
**근거 요약**: 적절한 임상 근거가 있음. 다수의 임상시험에서 일관된 미백 효과 확인.
```

### Evidence Summary Object

```python
@dataclass
class EvidenceSummary:
    ingredient: str
    efficacy: str
    total_studies: int
    total_subjects: int
    rct_count: int
    evidence_grade: str
    grade_justification: str
    key_findings: List[str]
    effect_size_range: str
    optimal_concentration: str
    recommended_duration: str
    confidence_level: str
    limitations: List[str]
    studies: List[StudyRecord]
```

## Study Quality Assessment

### Jadad Score (RCT용)

| 항목 | 점수 | 기준 |
|-----|------|------|
| 무작위화 언급 | +1 | "randomized" 명시 |
| 적절한 무작위화 | +1 | 방법 적절히 기술 |
| 이중맹검 언급 | +1 | "double-blind" 명시 |
| 적절한 맹검 | +1 | 방법 적절히 기술 |
| 탈락 보고 | +1 | 탈락자 수/사유 기술 |
| **총점** | **0-5** | 3점 이상: 고품질 |

### Risk of Bias (비뚤림 위험)

| 영역 | 평가 항목 |
|-----|----------|
| Selection | 무작위 배정 방법 |
| Performance | 참여자/연구자 맹검 |
| Detection | 평가자 맹검 |
| Attrition | 불완전 결과 처리 |
| Reporting | 선택적 보고 |
| Other | 기타 비뚤림 |

### Sample Size Adequacy

```
Excellent: n ≥ 100
Good: n ≥ 50
Adequate: n ≥ 30
Limited: n ≥ 20
Insufficient: n < 20
```

## Evidence Grading System

### 등급 정의

| Grade | 명칭 | 기준 |
|-------|------|------|
| **A** | Strong | 3+ RCT, n>200, 일관된 결과 |
| **B** | Moderate | 1-2 RCT 또는 3+ 임상시험, n>100 |
| **C** | Limited | 1+ 임상시험, n≥20 |
| **D** | Preliminary | In-vitro/In-vivo만 존재 |
| **E** | Insufficient | 근거 부족 또는 상반됨 |

### 등급 산정 알고리즘

```python
def calculate_grade(studies: List[Study]) -> str:
    rct_count = sum(1 for s in studies if s.is_rct)
    total_n = sum(s.sample_size for s in studies)
    consistency = assess_consistency(studies)

    if rct_count >= 3 and total_n > 200 and consistency > 0.8:
        return "A"
    elif (rct_count >= 1 and total_n > 100) or len(studies) >= 3:
        return "B"
    elif len(studies) >= 1 and total_n >= 20:
        return "C"
    elif has_preclinical_only(studies):
        return "D"
    else:
        return "E"
```

## Integration

### pubmed-search 연동

```python
from pubmed_search import PubMedClient
from clinical_evidence_aggregator import EvidenceAggregator

pubmed = PubMedClient()
aggregator = EvidenceAggregator()

# PubMed 검색 결과를 근거 테이블로 변환
search_result = pubmed.search_ingredient(
    ingredient="Niacinamide",
    efficacy="brightening",
    study_types=["Clinical Trial"]
)

evidence = aggregator.from_pubmed_results(search_result)
```

### ingredient-deep-dive 연동

```python
from ingredient_deep_dive import DeepDiveGenerator
from clinical_evidence_aggregator import EvidenceAggregator

deep_dive = DeepDiveGenerator()
aggregator = EvidenceAggregator()

# Deep-dive 리포트에 근거 테이블 추가
report = deep_dive.generate(ingredient="Niacinamide")
evidence = aggregator.aggregate(ingredient="Niacinamide")

report.clinical_evidence = evidence
```

## Efficacy-Specific Evidence

### 효능별 평가 지표

#### 미백 (Brightening)

| 지표 | 측정 방법 | 유의미한 변화 |
|-----|----------|--------------|
| ITA° | 분광측색계 | ≥3° 증가 |
| Melanin Index | Mexameter | ≥10% 감소 |
| L* value | Chromameter | ≥2 증가 |

#### 항노화 (Anti-aging)

| 지표 | 측정 방법 | 유의미한 변화 |
|-----|----------|--------------|
| 주름 깊이 | Profilometry | ≥10% 감소 |
| 탄력도 | Cutometer | ≥10% 증가 |
| 피부 두께 | Ultrasound | ≥5% 증가 |

#### 보습 (Moisturizing)

| 지표 | 측정 방법 | 유의미한 변화 |
|-----|----------|--------------|
| 수분도 | Corneometer | ≥10% 증가 |
| TEWL | Tewameter | ≥10% 감소 |

## Output Formats

### Markdown Table

```python
evidence.to_markdown()
```

### HTML Table

```python
evidence.to_html(styled=True)
```

### LaTeX Table

```python
evidence.to_latex()
```

### JSON Export

```python
evidence.to_json()
```

### Excel Export

```python
evidence.to_excel("evidence_table.xlsx")
```

## Best Practices

### 1. 검색 전략

```
- 다양한 동의어 사용
- MeSH Terms 활용
- 연도 범위 적절히 설정 (최근 10년 권장)
- 연구 유형 필터 활용
```

### 2. 품질 평가

```
- 자동 평가 후 수동 검토 권장
- 이해충돌 확인 필수
- 샘플 크기 적절성 검토
```

### 3. 등급 해석

```
- Grade A/B: 효능 클레임 가능
- Grade C: 제한적 클레임
- Grade D/E: 클레임 자제
```

## Reference Files

| File | Description |
|------|-------------|
| [references/evidence_criteria.md](references/evidence_criteria.md) | 근거 평가 기준 상세 |
| [references/study_types.md](references/study_types.md) | 연구 유형 분류 |
| [scripts/clinical_evidence_aggregator.py](scripts/clinical_evidence_aggregator.py) | Python 구현체 |

## Usage Examples

### 기본 사용

```
"나이아신아마이드 미백 효능 임상 근거 정리해줘"
→ [근거 테이블 + 등급 + 요약문]
```

### 특정 효능 분석

```
"레티놀의 항노화 효과 임상 연구 요약"
→ [항노화 효능 관련 연구만 필터링하여 정리]
```

### 비교 분석

```
"비타민C와 아르부틴의 미백 효과 근거 비교"
→ [두 성분 근거 테이블 비교 + 근거 수준 비교]
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-16 | Initial release |
