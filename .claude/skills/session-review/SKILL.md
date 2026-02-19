# Session Review Skill

## Metadata
- **Name**: session-review
- **Version**: 1.0.0
- **Category**: System Management
- **Trigger**: /review-session, 세션 종료 시 자동

## Description

작업 세션 완료 후 시스템 개선을 위한 리뷰 리포트를 생성합니다.
에이전트 활용도, 스킬 사용 패턴, 워크플로우 효율성을 분석하여 지속적인 시스템 개선에 기여합니다.

## Usage

### 수동 호출
```
/review-session --project ORYZA
```

### 자동 호출
세션 종료 시 Stop hook에서 자동 실행됩니다.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| project | string | Yes | - | 프로젝트명 (ORYZA, FRAIJOUR 등) |
| summary | string | No | "" | 세션 요약 |
| agents | list | No | [] | 사용된 에이전트 목록 |
| skills | list | No | [] | 사용된 스킬 목록 |
| issues | list | No | [] | 발견된 이슈 |
| suggestions | list | No | [] | 개선 제안 |

## Output

`.sisyphus/reviews/` 폴더에 마크다운 리뷰 파일 생성:

```
{YYYY-MM-DD}_review_{project}.md
```

### 리뷰 파일 구조

1. **세션 요약**: 수행한 작업 개요
2. **에이전트 활용 분석**: 사용된 에이전트, 호출 횟수, 효율성 평가
3. **스킬 활용 분석**: 사용된 스킬, 누락된 스킬 제안
4. **워크플로우 분석**: 병렬 처리 활용도, 병목 지점
5. **개선 제안**: 단기/중기/장기 개선 사항
6. **다음 액션**: 후속 작업 체크리스트

## Analysis Criteria

### 에이전트 선택 적절성
- [ ] 복잡한 분석에 Opus 에이전트 사용 (oracle 계열)
- [ ] 표준 작업에 Sonnet 에이전트 사용 (junior 계열)
- [ ] 단순 조회에 Haiku 에이전트 사용 (explorer, librarian-low)
- [ ] 불필요한 에이전트 호출 없음

### 스킬 활용도
- [ ] 적절한 스킬이 활성화되었는지
- [ ] 수동으로 처리한 작업 중 스킬로 자동화 가능한 것
- [ ] 새로운 스킬 필요 여부

### 워크플로우 효율성
- [ ] 독립적 작업의 병렬 실행 여부
- [ ] 순차 의존성 적절히 처리되었는지
- [ ] 불필요한 반복 작업 여부

## Example Review

```markdown
# 시스템 리뷰: ORYZA

**생성일**: 2026-01-18 15:30:00
**프로젝트**: ORYZA

---

## 1. 세션 요약

ORYZA 제형 수정 통합 기획서 작성 완료.
4개 제품(토너, 버퍼크림, 글로우팩, 모찌클렌저)의 제형 수정 기획서 개별 작성.

---

## 2. 에이전트 활용 분석

### 사용된 에이전트

| 에이전트 | 호출 횟수 | 효율성 |
|----------|----------|--------|
| `formulation-oracle` | 4 | 적절 |
| `ingredient-explorer` | 2 | 적절 |

### 에이전트 선택 적절성

- [x] 복잡한 분석에 Opus 사용
- [x] 표준 작업에 Sonnet 사용
- [ ] 단순 조회에 Haiku 사용 → 개선 필요
- [x] 불필요한 에이전트 호출 없음

---

## 3. 스킬 활용 분석

### 사용된 스킬

- `formulation-calculator`
- `ingredient-compatibility`

### 누락된 스킬 제안

| 상황 | 제안 스킬 | 이유 |
|------|----------|------|
| 성분명 변환 | `inci-converter` | INCI명 일관성 확보 |

---

## 4. 워크플로우 분석

### 병렬 처리 활용

- [x] 독립적인 작업 병렬 실행됨 (4개 제품 동시 작업)
- [x] 순차 의존성 있는 작업 순서대로 실행됨
- [ ] 불필요한 대기 없음 → API rate limit으로 대기 발생

### 발견된 이슈

1. API rate limit으로 인한 병렬 처리 제한
2. 일부 성분 정보 수동 입력 필요

---

## 5. 개선 제안

### 단기 개선 (즉시 적용 가능)

1. 단순 성분 조회에 Haiku 모델 사용

### 중기 개선 (스킬 추가/수정 필요)

1. rate limit 발생 시 자동 재시도 로직

### 장기 개선 (시스템 구조 변경 필요)

1. 성분 DB 로컬 캐싱으로 API 의존도 감소
```

## Related Files

- **Hook Script**: `.claude/hooks/review_generator.py`
- **Log Script**: `.claude/hooks/session_logger.py`
- **Reviews Folder**: `.sisyphus/reviews/`
- **Logs Folder**: `.sisyphus/logs/`

## Integration

### Stop Hook에서 자동 호출
```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "command": "python .claude/hooks/review_generator.py --stdin"
      }
    ]
  }
}
```

### 수동 호출 방법
```bash
# CLI에서 직접 실행
python .claude/hooks/review_generator.py --project ORYZA --summary "제형 수정 작업 완료"

# JSON 입력으로 실행
echo '{"project": "ORYZA", "agents": ["formulation-oracle"], "skills": ["formulation-calculator"]}' | python .claude/hooks/review_generator.py --stdin
```

## Best Practices

1. **매 세션마다 리뷰 생성**: 작업 패턴 파악에 도움
2. **주간 리뷰 집계**: 반복되는 개선점 식별
3. **개선 사항 즉시 반영**: 리뷰에서 발견된 문제점 해결
4. **스킬 업데이트**: 반복 작업은 스킬로 자동화
