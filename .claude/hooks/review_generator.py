#!/usr/bin/env python3
"""
Sisyphus Review Generator
작업 세션 완료 후 시스템 개선 리뷰를 생성하는 스크립트

사용법:
- 수동 실행: python review_generator.py --project ORYZA
- Claude가 호출: /review-session 명령
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def get_project_root():
    """프로젝트 루트 경로 반환"""
    script_path = Path(__file__).resolve()
    return script_path.parent.parent.parent


def create_review_template(project: str, session_summary: str = "",
                           agents_used: list = None, skills_used: list = None,
                           issues: list = None, suggestions: list = None):
    """리뷰 템플릿 생성"""

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    filename = f"{date_str}_review_{project.lower()}.md"

    agents_used = agents_used or []
    skills_used = skills_used or []
    issues = issues or []
    suggestions = suggestions or []

    review_content = f"""# 시스템 리뷰: {project}

**생성일**: {date_str} {time_str}
**프로젝트**: {project}

---

## 1. 세션 요약

{session_summary if session_summary else "(세션 요약을 작성해주세요)"}

---

## 2. 에이전트 활용 분석

### 사용된 에이전트

| 에이전트 | 호출 횟수 | 효율성 |
|----------|----------|--------|
"""

    for agent in agents_used:
        if isinstance(agent, dict):
            review_content += f"| `{agent.get('name', 'unknown')}` | {agent.get('count', 1)} | {agent.get('efficiency', '적절')} |\n"
        else:
            review_content += f"| `{agent}` | 1 | 적절 |\n"

    if not agents_used:
        review_content += "| (직접 수행) | - | - |\n"

    review_content += """
### 에이전트 선택 적절성

- [ ] 복잡한 분석에 Opus 사용
- [ ] 표준 작업에 Sonnet 사용
- [ ] 단순 조회에 Haiku 사용
- [ ] 불필요한 에이전트 호출 없음

---

## 3. 스킬 활용 분석

### 사용된 스킬

"""

    if skills_used:
        for skill in skills_used:
            review_content += f"- `{skill}`\n"
    else:
        review_content += "- (없음)\n"

    review_content += """
### 누락된 스킬 제안

| 상황 | 제안 스킬 | 이유 |
|------|----------|------|
"""

    for suggestion in suggestions:
        if isinstance(suggestion, dict):
            review_content += f"| {suggestion.get('situation', '')} | `{suggestion.get('skill', '')}` | {suggestion.get('reason', '')} |\n"

    if not suggestions:
        review_content += "| - | - | - |\n"

    review_content += """
---

## 4. 워크플로우 분석

### 병렬 처리 활용

- [ ] 독립적인 작업 병렬 실행됨
- [ ] 순차 의존성 있는 작업 순서대로 실행됨
- [ ] 불필요한 대기 없음

### 발견된 이슈

"""

    if issues:
        for i, issue in enumerate(issues, 1):
            review_content += f"{i}. {issue}\n"
    else:
        review_content += "- (특이사항 없음)\n"

    review_content += """
---

## 5. 개선 제안

### 단기 개선 (즉시 적용 가능)

1.

### 중기 개선 (스킬 추가/수정 필요)

1.

### 장기 개선 (시스템 구조 변경 필요)

1.

---

## 6. 다음 액션

- [ ]
- [ ]
- [ ]

---

## 7. 메모

(자유 형식 메모)

---

*자동 생성됨: {0}*
""".format(now.strftime("%Y-%m-%d %H:%M:%S"))

    return filename, review_content


def save_review(filename: str, content: str):
    """리뷰 파일 저장"""
    project_root = get_project_root()
    reviews_dir = project_root / ".sisyphus" / "reviews"
    reviews_dir.mkdir(parents=True, exist_ok=True)

    review_path = reviews_dir / filename
    with open(review_path, "w", encoding="utf-8") as f:
        f.write(content)

    return review_path


def read_stdin_json():
    """stdin에서 JSON 입력 읽기"""
    try:
        input_data = sys.stdin.read()
        return json.loads(input_data) if input_data else {}
    except json.JSONDecodeError:
        return {}


def main():
    """메인 함수"""
    import argparse

    parser = argparse.ArgumentParser(description="Sisyphus Review Generator")
    parser.add_argument("--project", default="Unknown", help="프로젝트명")
    parser.add_argument("--summary", default="", help="세션 요약")
    parser.add_argument("--agents", nargs="*", default=[], help="사용된 에이전트 목록")
    parser.add_argument("--skills", nargs="*", default=[], help="사용된 스킬 목록")
    parser.add_argument("--stdin", action="store_true", help="stdin에서 JSON 입력 받기")

    args = parser.parse_args()

    if args.stdin:
        data = read_stdin_json()
        project = data.get("project", args.project)
        summary = data.get("summary", args.summary)
        agents = data.get("agents", args.agents)
        skills = data.get("skills", args.skills)
        issues = data.get("issues", [])
        suggestions = data.get("suggestions", [])
    else:
        project = args.project
        summary = args.summary
        agents = args.agents
        skills = args.skills
        issues = []
        suggestions = []

    filename, content = create_review_template(
        project=project,
        session_summary=summary,
        agents_used=agents,
        skills_used=skills,
        issues=issues,
        suggestions=suggestions
    )

    review_path = save_review(filename, content)
    print(f"Review saved: {review_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
