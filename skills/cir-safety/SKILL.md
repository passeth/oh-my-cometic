---
name: cir-safety
description: Cosmetic Ingredient Review (CIR) safety assessment database - 미국 화장품 성분 안전성 독립 평가 기관 데이터베이스
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - WebFetch
license: MIT
metadata:
  version: "1.0.0"
  category: safety
  region: USA
  language: en
  last-updated: "2025-01-16"
  maintainer: cosmetic-skills
  tags:
    - CIR
    - safety-assessment
    - ingredient-safety
    - cosmetic-safety
    - US-regulation
    - expert-panel
---

# CIR Safety Skill

Cosmetic Ingredient Review (CIR) 화장품 성분 안전성 평가 데이터베이스 스킬

## Overview

**CIR (Cosmetic Ingredient Review)**은 미국 화장품 업계에서 운영하는 **독립적인 성분 안전성 평가 기관**입니다. 1976년에 설립되어 Personal Care Products Council (PCPC)의 후원 하에 운영되며, 전문가 패널(Expert Panel)이 화장품 성분의 안전성을 과학적으로 평가합니다.

### CIR의 특징

- **독립성**: 업계 후원이지만 평가는 독립적으로 수행
- **과학적 근거**: 동물실험, 임상시험, 독성학 데이터 기반
- **투명성**: 모든 평가 보고서 공개
- **국제 인정**: FDA, EU SCCS 등에서 참고 자료로 활용

**공식 웹사이트**: https://www.cir-safety.org/

## When to Use This Skill

이 스킬은 다음과 같은 상황에서 사용합니다:

- **성분 안전성 근거 확보**: 특정 성분의 안전성 결론 및 근거 자료 조회
- **규제 대응**: FDA, EU 등 규제 기관 제출 자료 준비
- **클레임 지원**: 마케팅 클레임의 안전성 근거 확보
- **처방 검토**: 신규 처방의 안전성 사전 검토
- **원료 선정**: 안전성이 검증된 원료 선별
- **위험 평가**: 성분별 사용 조건 및 제한 사항 확인

## Core Capabilities

### 1. 안전성 결론 조회 (Safety Conclusions)

CIR Expert Panel의 공식 안전성 결론을 조회합니다:

| 결론 유형 | 영문 | 의미 |
|----------|------|------|
| **안전** | Safe as used | 현재 사용 조건에서 안전 |
| **조건부 안전** | Safe with qualifications | 특정 조건(농도, 용도) 하에서 안전 |
| **데이터 부족** | Insufficient data | 안전성 판단을 위한 데이터 부족 |
| **안전하지 않음** | Unsafe | 현재 사용 조건에서 안전하지 않음 |

```python
from cir_search import CIRClient

client = CIRClient()

# 성분 안전성 결론 조회
result = client.search_ingredient("Niacinamide")
print(f"결론: {result.conclusion}")  # Safe as used
print(f"최대 농도: {result.max_concentration}%")
```

### 2. 평가 보고서 검색 (Report Search)

CIR 평가 보고서 및 관련 문서 검색:

```python
# 성분별 보고서 조회
report = client.get_report("Retinol")
print(f"보고서 유형: {report.report_type}")  # Final Report
print(f"평가 일자: {report.assessment_date}")
print(f"PDF URL: {report.pdf_url}")

# 최근 평가 목록 조회
recent = client.list_recent_assessments(year=2024)
for item in recent:
    print(f"{item.ingredient}: {item.conclusion}")
```

### 3. 사용 조건 확인 (Use Conditions)

조건부 안전(Safe with qualifications) 성분의 상세 사용 조건:

```python
# 사용 제한 조건 조회
conditions = client.get_use_conditions("Salicylic Acid")
print(conditions)
# {
#     "max_concentration": {
#         "leave-on": 2.0,
#         "rinse-off": 3.0
#     },
#     "restricted_uses": ["Not for use in lip products"],
#     "formulation_requirements": ["pH 3.5-4.5 recommended"]
# }
```

### 4. 최신 평가/재평가 현황 (Assessment Status)

CIR은 15년 주기로 성분을 재평가합니다:

```python
# 평가 현황 조회
status = client.get_assessment_status("Parabens")
print(f"최초 평가: {status.original_date}")
print(f"최근 재평가: {status.latest_review_date}")
print(f"다음 재평가 예정: {status.next_review_due}")
print(f"현재 상태: {status.current_status}")  # Re-review in progress
```

### 5. 성분 그룹별 평가 (Ingredient Groups)

CIR은 유사 성분을 그룹으로 평가합니다:

```python
# 그룹 평가 조회
group = client.get_ingredient_group("Parabens")
print(f"그룹명: {group.group_name}")
print(f"포함 성분: {group.ingredients}")
# ["Methylparaben", "Ethylparaben", "Propylparaben", "Butylparaben", ...]

silicones = client.get_ingredient_group("Dimethicone")
# Dimethicone 관련 실리콘 계열 전체 평가 정보
```

## Common Workflows

### Workflow 1: 신원료 안전성 확인

새로운 원료 도입 전 CIR 안전성 평가 확인:

```
1. CIR 데이터베이스에서 성분 검색
2. 안전성 결론 확인 (Safe / Qualified / Insufficient / Unsafe)
3. 조건부 안전인 경우 사용 제한 조건 확인
4. 데이터 부족인 경우 추가 데이터 요구사항 파악
5. 최종 보고서 PDF 다운로드 및 보관
```

### Workflow 2: 규제 문서 작성

FDA 제출용 안전성 자료 준비:

```
1. 처방 내 전체 성분의 CIR 결론 일괄 조회
2. Safe as used 성분 → CIR 참조로 안전성 입증
3. Safe with qualifications → 사용 조건 충족 여부 확인
4. Insufficient data → 자체 안전성 데이터 준비 필요
5. CIR 보고서 참조문헌으로 인용
```

### Workflow 3: 재평가 모니터링

기존 원료의 안전성 업데이트 추적:

```
1. 사용 중인 원료의 재평가 일정 확인
2. Priority List (우선순위 목록) 모니터링
3. Draft Report 공개 시 검토 및 의견 제출
4. Final Report 발표 시 결론 변경 여부 확인
5. 필요 시 처방 또는 사용 조건 조정
```

## Safety Conclusion Categories

### Safe as Used (현재 사용 조건에서 안전)

가장 긍정적인 결론입니다:

- 현재 화장품에 사용되는 농도 및 용도에서 안전
- 추가 제한 없이 사용 가능
- 일반적인 화장품 용도 전체에 적용

**예시 성분**: Glycerin, Niacinamide, Hyaluronic Acid, Tocopherol

### Safe with Qualifications (조건부 안전)

특정 조건 하에서만 안전:

- **농도 제한**: 최대 사용 농도 지정
- **용도 제한**: 특정 제품 유형 제외
- **제형 조건**: pH, 순도, 입자 크기 등 규격 지정
- **표시 요건**: 특정 경고문 표시 필요

**예시 성분**: Retinol (농도 제한), Salicylic Acid (용도 제한), Titanium Dioxide (나노 입자 조건)

### Insufficient Data (데이터 부족)

안전성 판단을 위한 정보가 부족:

- 추가로 필요한 데이터 유형 명시
- 일반적으로 요구되는 데이터:
  - 피부 흡수 데이터
  - 감작성(Sensitization) 테스트
  - 유전독성(Genotoxicity) 테스트
  - 발달독성(Developmental toxicity) 데이터
  - 사용 농도 정보

### Unsafe (안전하지 않음)

현재 사용 조건에서 안전하지 않음:

- 특정 농도 또는 용도에서 위험성 확인
- 사용 금지 또는 대폭 제한 권고
- 매우 드문 결론 (CIR 역사상 소수)

**예시**: Coal Tar (특정 용도), Lead Acetate (염모제)

## Best Practices

### 1. CIR 보고서 인용

```
- 항상 최신 버전의 보고서 참조
- Final Report만 공식 인용 가능 (Draft 제외)
- 정확한 인용 형식:
  "Cosmetic Ingredient Review. [Year]. Safety Assessment of [Ingredient]
   as Used in Cosmetics. International Journal of Toxicology."
```

### 2. 조건부 안전 해석

```
- 모든 qualification 조건 확인 필수
- 농도 제한: 전체 처방 기준 vs 활성 성분 기준 구분
- 용도 제한: 제품 유형 명확히 파악
- 복합 조건: 모든 조건 동시 충족 필요
```

### 3. 데이터 부족 대응

```
- CIR에서 요구하는 특정 데이터 유형 확인
- 자체 시험 또는 원료사 데이터로 보완
- 원료사에 CIR 평가 요청 권고
```

### 4. 재평가 주기 고려

```
- CIR 재평가 주기: 약 15년
- 새로운 과학적 발견 시 조기 재평가 가능
- Re-review 진행 중인 성분 주의 (결론 변경 가능성)
```

## Reference Files

| File | Description |
|------|-------------|
| [references/cir_assessment.md](references/cir_assessment.md) | CIR 평가 프로세스 상세 설명 |
| [references/safety_conclusions.md](references/safety_conclusions.md) | 안전성 결론 유형 및 주요 성분별 요약 |
| [scripts/cir_search.py](scripts/cir_search.py) | Python CIR 검색 클라이언트 |

## Related Resources

- **CIR 공식**: https://www.cir-safety.org/
- **CIR 성분 데이터베이스**: https://www.cir-safety.org/ingredients
- **International Journal of Toxicology**: CIR 보고서 게재 학술지
- **FDA 화장품 규정**: https://www.fda.gov/cosmetics
- **EU SCCS 의견**: https://health.ec.europa.eu/scientific-committees/scientific-committee-consumer-safety-sccs_en

## Usage Examples

### 성분 안전성 빠른 조회
```
"나이아신아마이드 CIR 안전성 결론은?"
→ Safe as used in cosmetics (현재 사용 조건에서 안전)
→ 최대 5%까지 얼굴용 제품에서 널리 사용
→ 보고서: IJT 2005, Re-review 2020
```

### 조건부 안전 성분 확인
```
"레티놀 CIR 사용 조건은?"
→ Safe with qualifications
→ 최대 농도: Leave-on 0.5%, Rinse-off 0.05%
→ 자외선 노출 주의, 임산부 사용 자제 권고
```

### 그룹 평가 조회
```
"파라벤류 CIR 평가 현황?"
→ 2019년 재평가 완료
→ 결론: Safe as used in cosmetics
→ 총 12종 성분 포함 (Methyl-, Ethyl-, Propyl-, Butyl- 등)
→ 개별 및 총 파라벤 농도 제한 없음 (현재 사용 수준)
```

## Integration with Other Skills

### cosing-database 연동
- EU CosIng에서 규제 상태 확인 후 CIR에서 안전성 근거 보완
- EU Annex III 제한물질의 경우 CIR 평가와 비교 검토

### kfda-ingredient 연동
- 한국 기능성 고시원료의 국제적 안전성 근거로 CIR 활용
- 미백/주름개선/자외선차단 원료의 추가 안전성 확인

### regulatory-compliance 연동
- 미국 FDA 규제 대응 시 CIR 보고서 직접 인용
- 국제 규제 조화에 CIR 데이터 활용

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-01-16 | Initial release with CIR safety assessment database |
