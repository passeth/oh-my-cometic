#!/usr/bin/env python3
"""
Cosmetic Orchestrator Session Manager
세션 생성, 관리, 상태 추적을 위한 스크립트

Usage:
    python session_manager.py create --request "비타민C 세럼 개발"
    python session_manager.py status --session-id 20250116_143022_r_and_d
    python session_manager.py list --limit 10
    python session_manager.py resume --session-id 20250116_143022_r_and_d
"""

import os
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, asdict
from enum import Enum


class PhaseStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class ProjectType(Enum):
    PLANNING = "planning"
    R_AND_D = "r_and_d"
    REGULATORY = "regulatory"
    MARKETING = "marketing"
    SAFETY = "safety"
    UNKNOWN = "unknown"


# 프로젝트 유형 감지를 위한 키워드
PROJECT_TYPE_KEYWORDS = {
    ProjectType.PLANNING: ["신제품", "기획", "컨셉", "타겟", "포지셔닝", "전략", "브랜드"],
    ProjectType.R_AND_D: ["배합", "처방", "제형", "안정성", "테스트", "개발", "HLB", "pH"],
    ProjectType.REGULATORY: ["인허가", "심사", "규제", "등록", "CPSR", "수출", "EU", "FDA"],
    ProjectType.MARKETING: ["광고", "클레임", "마케팅", "홍보", "효능", "캠페인"],
    ProjectType.SAFETY: ["안전성", "독성", "자극", "EWG", "CIR", "NOAEL", "MoS"],
}


@dataclass
class PhaseInfo:
    status: str = "pending"
    agent: Optional[str] = None
    output: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    duration_sec: Optional[int] = None
    error: Optional[str] = None


@dataclass
class SessionConfig:
    session_id: str
    created_at: str
    user_request: str
    project_type: str
    detected_keywords: List[str]
    phases: Dict[str, Dict]
    recommended_skills: List[str]
    artifacts: List[str]
    total_duration_sec: Optional[int] = None
    status: str = "active"


class SessionManager:
    """세션 관리 클래스"""

    def __init__(self, base_dir: str = "./sessions"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def detect_project_type(self, request: str) -> ProjectType:
        """요청에서 프로젝트 유형 감지"""
        scores = {pt: 0 for pt in ProjectType}

        request_lower = request.lower()

        for project_type, keywords in PROJECT_TYPE_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in request_lower:
                    scores[project_type] += 1

        # 최고 점수 찾기
        max_score = max(scores.values())
        if max_score == 0:
            return ProjectType.UNKNOWN

        for pt, score in scores.items():
            if score == max_score:
                return pt

        return ProjectType.UNKNOWN

    def extract_keywords(self, request: str) -> List[str]:
        """요청에서 화장품 관련 키워드 추출"""
        all_keywords = []
        for keywords in PROJECT_TYPE_KEYWORDS.values():
            all_keywords.extend(keywords)

        # 제품 유형 키워드
        product_keywords = [
            "세럼", "크림", "로션", "토너", "에센스", "앰플", "마스크",
            "선크림", "클렌저", "스킨", "오일", "미스트", "젤"
        ]
        all_keywords.extend(product_keywords)

        # 성분 키워드
        ingredient_keywords = [
            "비타민C", "레티놀", "나이아신아마이드", "히알루론산", "펩타이드",
            "세라마이드", "CICA", "센텔라", "AHA", "BHA", "글리세린"
        ]
        all_keywords.extend(ingredient_keywords)

        # 매칭된 키워드 찾기
        found_keywords = []
        request_lower = request.lower()

        for keyword in all_keywords:
            if keyword.lower() in request_lower:
                if keyword not in found_keywords:
                    found_keywords.append(keyword)

        return found_keywords

    def create_session(self, user_request: str) -> SessionConfig:
        """새 세션 생성"""
        # 프로젝트 유형 감지
        project_type = self.detect_project_type(user_request)

        # 키워드 추출
        keywords = self.extract_keywords(user_request)

        # 세션 ID 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_id = f"{timestamp}_{project_type.value}"

        # 세션 디렉토리 생성
        session_dir = self.base_dir / session_id
        session_dir.mkdir(parents=True, exist_ok=True)
        (session_dir / "artifacts").mkdir(exist_ok=True)
        (session_dir / "logs").mkdir(exist_ok=True)

        # Phase 정보 초기화
        phases = {
            "phase1": asdict(PhaseInfo(agent="context-initialization")),
            "phase2": asdict(PhaseInfo(agent="resource-discovery")),
            "phase3": asdict(PhaseInfo(agent="specialist")),
            "phase4": asdict(PhaseInfo(agent="validation")),
            "phase5": asdict(PhaseInfo(agent="synthesis")),
        }

        # 세션 설정 생성
        config = SessionConfig(
            session_id=session_id,
            created_at=datetime.now().isoformat(),
            user_request=user_request,
            project_type=project_type.value,
            detected_keywords=keywords,
            phases=phases,
            recommended_skills=[],
            artifacts=[],
        )

        # 설정 파일 저장
        config_path = session_dir / "session_config.json"
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(asdict(config), f, ensure_ascii=False, indent=2)

        return config

    def update_phase(
        self,
        session_id: str,
        phase: str,
        status: PhaseStatus,
        output: Optional[str] = None,
        error: Optional[str] = None
    ) -> SessionConfig:
        """Phase 상태 업데이트"""
        session_dir = self.base_dir / session_id
        config_path = session_dir / "session_config.json"

        with open(config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)

        # Phase 업데이트
        now = datetime.now().isoformat()

        if status == PhaseStatus.IN_PROGRESS:
            config_data["phases"][phase]["status"] = status.value
            config_data["phases"][phase]["started_at"] = now
        elif status == PhaseStatus.COMPLETED:
            config_data["phases"][phase]["status"] = status.value
            config_data["phases"][phase]["completed_at"] = now
            config_data["phases"][phase]["output"] = output

            # Duration 계산
            if config_data["phases"][phase].get("started_at"):
                started = datetime.fromisoformat(config_data["phases"][phase]["started_at"])
                completed = datetime.fromisoformat(now)
                duration = (completed - started).total_seconds()
                config_data["phases"][phase]["duration_sec"] = int(duration)
        elif status == PhaseStatus.FAILED:
            config_data["phases"][phase]["status"] = status.value
            config_data["phases"][phase]["error"] = error

        # 저장
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)

        return SessionConfig(**config_data)

    def get_session(self, session_id: str) -> Optional[SessionConfig]:
        """세션 정보 조회"""
        session_dir = self.base_dir / session_id
        config_path = session_dir / "session_config.json"

        if not config_path.exists():
            return None

        with open(config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)

        return SessionConfig(**config_data)

    def list_sessions(self, limit: int = 10, status: Optional[str] = None) -> List[Dict]:
        """세션 목록 조회"""
        sessions = []

        for session_dir in sorted(self.base_dir.iterdir(), reverse=True):
            if not session_dir.is_dir():
                continue

            config_path = session_dir / "session_config.json"
            if not config_path.exists():
                continue

            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            if status and config.get("status") != status:
                continue

            sessions.append({
                "session_id": config["session_id"],
                "created_at": config["created_at"],
                "project_type": config["project_type"],
                "user_request": config["user_request"][:50] + "..." if len(config["user_request"]) > 50 else config["user_request"],
                "status": config.get("status", "unknown"),
            })

            if len(sessions) >= limit:
                break

        return sessions

    def get_current_phase(self, session_id: str) -> Optional[str]:
        """현재 진행 중인 Phase 확인"""
        session = self.get_session(session_id)
        if not session:
            return None

        for phase_name, phase_info in session.phases.items():
            if phase_info["status"] == "in_progress":
                return phase_name
            if phase_info["status"] == "pending":
                return phase_name

        return None  # 모든 phase 완료

    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """세션 요약 정보"""
        session = self.get_session(session_id)
        if not session:
            return {"error": "Session not found"}

        completed_phases = sum(
            1 for p in session.phases.values()
            if p["status"] == "completed"
        )

        return {
            "session_id": session.session_id,
            "project_type": session.project_type,
            "progress": f"{completed_phases}/5 phases",
            "current_phase": self.get_current_phase(session_id),
            "detected_keywords": session.detected_keywords,
            "recommended_skills": session.recommended_skills,
            "artifacts_count": len(session.artifacts),
        }


def main():
    parser = argparse.ArgumentParser(description="Cosmetic Orchestrator Session Manager")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # create 명령
    create_parser = subparsers.add_parser("create", help="Create new session")
    create_parser.add_argument("--request", "-r", required=True, help="User request")
    create_parser.add_argument("--base-dir", "-d", default="./sessions", help="Sessions base directory")

    # status 명령
    status_parser = subparsers.add_parser("status", help="Get session status")
    status_parser.add_argument("--session-id", "-s", required=True, help="Session ID")
    status_parser.add_argument("--base-dir", "-d", default="./sessions", help="Sessions base directory")

    # list 명령
    list_parser = subparsers.add_parser("list", help="List sessions")
    list_parser.add_argument("--limit", "-l", type=int, default=10, help="Max sessions to list")
    list_parser.add_argument("--status", help="Filter by status")
    list_parser.add_argument("--base-dir", "-d", default="./sessions", help="Sessions base directory")

    # resume 명령
    resume_parser = subparsers.add_parser("resume", help="Resume session")
    resume_parser.add_argument("--session-id", "-s", required=True, help="Session ID")
    resume_parser.add_argument("--base-dir", "-d", default="./sessions", help="Sessions base directory")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    manager = SessionManager(args.base_dir)

    if args.command == "create":
        session = manager.create_session(args.request)
        print(json.dumps(asdict(session), ensure_ascii=False, indent=2))

    elif args.command == "status":
        summary = manager.get_session_summary(args.session_id)
        print(json.dumps(summary, ensure_ascii=False, indent=2))

    elif args.command == "list":
        sessions = manager.list_sessions(args.limit, args.status)
        print(json.dumps(sessions, ensure_ascii=False, indent=2))

    elif args.command == "resume":
        session = manager.get_session(args.session_id)
        if session:
            current_phase = manager.get_current_phase(args.session_id)
            print(f"Resuming session: {args.session_id}")
            print(f"Current phase: {current_phase}")
            print(f"Project type: {session.project_type}")
        else:
            print(f"Session not found: {args.session_id}")


if __name__ == "__main__":
    main()
