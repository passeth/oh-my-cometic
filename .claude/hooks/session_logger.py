#!/usr/bin/env python3
"""
Sisyphus Session Logger
작업 세션 완료 시 자동으로 로그를 기록하는 hook 스크립트

사용법:
- Claude Code hook으로 자동 실행
- 또는 수동 실행: python session_logger.py --project ORYZA --task "제형 수정 기획서 작성"
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def get_project_root():
    """프로젝트 루트 경로 반환"""
    # 스크립트 위치 기준으로 프로젝트 루트 찾기
    script_path = Path(__file__).resolve()
    # .claude/hooks/session_logger.py -> 프로젝트 루트는 2단계 위
    return script_path.parent.parent.parent


def create_log_entry(project: str, task: str, agents: list, skills: list,
                     outputs: list, model: str = "claude-opus-4-5", notes: str = ""):
    """로그 엔트리 생성"""

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    # 로그 파일명 생성
    task_slug = task.lower().replace(" ", "-")[:30]
    filename = f"{date_str}_{project}_{task_slug}.md"

    # 로그 내용 생성
    log_content = f"""# 작업 로그: {task}

## 기본 정보

| 항목 | 값 |
|------|------|
| **작업 일시** | {date_str} {time_str} |
| **프로젝트** | {project} |
| **주요 모델** | {model} |

## 작업 요약

{task}

## 사용된 에이전트

| 에이전트 | 모델 티어 |
|----------|----------|
"""

    for agent in agents:
        tier = "Opus" if "oracle" in agent or "prometheus" in agent else "Sonnet" if "junior" in agent or "librarian" in agent else "Haiku"
        log_content += f"| `{agent}` | {tier} |\n"

    if not agents:
        log_content += "| (직접 수행) | Opus |\n"

    log_content += f"""
## 사용된 스킬

"""

    if skills:
        for skill in skills:
            log_content += f"- `{skill}`\n"
    else:
        log_content += "- (없음)\n"

    log_content += f"""
## 산출물

"""

    if outputs:
        for output in outputs:
            log_content += f"- `{output}`\n"
    else:
        log_content += "- (없음)\n"

    if notes:
        log_content += f"""
## 메모

{notes}
"""

    log_content += f"""
---

*자동 생성됨: {now.strftime("%Y-%m-%d %H:%M:%S")}*
"""

    return filename, log_content


def save_log(filename: str, content: str):
    """로그 파일 저장"""
    project_root = get_project_root()
    logs_dir = project_root / ".sisyphus" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    log_path = logs_dir / filename
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(content)

    return log_path


def read_stdin_json():
    """stdin에서 JSON 입력 읽기 (Claude Code hook용)"""
    try:
        input_data = sys.stdin.read()
        return json.loads(input_data) if input_data else {}
    except json.JSONDecodeError:
        return {}


def main():
    """메인 함수"""
    import argparse

    parser = argparse.ArgumentParser(description="Sisyphus Session Logger")
    parser.add_argument("--project", default="Unknown", help="프로젝트명")
    parser.add_argument("--task", default="작업 수행", help="작업 설명")
    parser.add_argument("--agents", nargs="*", default=[], help="사용된 에이전트 목록")
    parser.add_argument("--skills", nargs="*", default=[], help="사용된 스킬 목록")
    parser.add_argument("--outputs", nargs="*", default=[], help="생성된 산출물 목록")
    parser.add_argument("--model", default="claude-opus-4-5", help="주요 모델")
    parser.add_argument("--notes", default="", help="메모")
    parser.add_argument("--stdin", action="store_true", help="stdin에서 JSON 입력 받기")

    args = parser.parse_args()

    # stdin 모드일 경우 JSON에서 파라미터 읽기
    if args.stdin:
        data = read_stdin_json()
        project = data.get("project", args.project)
        task = data.get("task", args.task)
        agents = data.get("agents", args.agents)
        skills = data.get("skills", args.skills)
        outputs = data.get("outputs", args.outputs)
        model = data.get("model", args.model)
        notes = data.get("notes", args.notes)
    else:
        project = args.project
        task = args.task
        agents = args.agents
        skills = args.skills
        outputs = args.outputs
        model = args.model
        notes = args.notes

    # 로그 생성 및 저장
    filename, content = create_log_entry(
        project=project,
        task=task,
        agents=agents,
        skills=skills,
        outputs=outputs,
        model=model,
        notes=notes
    )

    log_path = save_log(filename, content)
    print(f"Log saved: {log_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
