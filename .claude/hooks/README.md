# Sisyphus Hook Scripts

세션 로깅 및 리뷰 생성을 위한 Python 스크립트입니다.

## 스크립트 목록

| 스크립트 | 용도 |
|----------|------|
| `session_logger.py` | 작업 세션 로그 기록 |
| `review_generator.py` | 시스템 개선 리뷰 생성 |

## 사용법

### 1. 세션 로거 (session_logger.py)

작업 완료 시 로그를 기록합니다.

```bash
# 기본 사용
python .claude/hooks/session_logger.py --project ORYZA --task "제형 수정 기획서 작성"

# 상세 정보 포함
python .claude/hooks/session_logger.py \
  --project ORYZA \
  --task "제형 수정 기획서 작성" \
  --agents formulation-oracle ingredient-explorer \
  --skills formulation-calculator inci-converter \
  --outputs "01_토너_제형수정_기획서.md" "02_버퍼크림_제형수정_기획서.md" \
  --model claude-opus-4-5 \
  --notes "4개 제품 병렬 처리 완료"

# JSON 입력 (stdin)
echo '{"project": "ORYZA", "task": "제형 분석", "agents": ["formulation-oracle"]}' | python .claude/hooks/session_logger.py --stdin
```

**출력 위치**: `.sisyphus/logs/{date}_{project}_{task}.md`

### 2. 리뷰 생성기 (review_generator.py)

시스템 개선을 위한 리뷰 리포트를 생성합니다.

```bash
# 기본 사용
python .claude/hooks/review_generator.py --project ORYZA

# 상세 정보 포함
python .claude/hooks/review_generator.py \
  --project ORYZA \
  --summary "ORYZA 4종 제품 제형 수정 기획 완료"

# JSON 입력 (stdin)
echo '{
  "project": "ORYZA",
  "summary": "제형 수정 작업 완료",
  "agents": [
    {"name": "formulation-oracle", "count": 4, "efficiency": "적절"},
    {"name": "ingredient-explorer", "count": 2, "efficiency": "적절"}
  ],
  "skills": ["formulation-calculator", "inci-converter"],
  "issues": ["API rate limit 발생", "일부 성분 수동 입력 필요"],
  "suggestions": [
    {"situation": "성분명 변환", "skill": "inci-converter", "reason": "INCI명 일관성 확보"}
  ]
}' | python .claude/hooks/review_generator.py --stdin
```

**출력 위치**: `.sisyphus/reviews/{date}_review_{project}.md`

## Claude에서 호출하기

### 방법 1: 수동 호출 (권장)

세션 종료 전 Claude에게 요청:

```
세션 로그를 기록해줘:
- 프로젝트: ORYZA
- 작업: 제형 수정 기획서 작성
- 사용 에이전트: formulation-oracle, ingredient-explorer
- 사용 스킬: formulation-calculator
- 산출물: 01_토너_제형수정_기획서.md 외 3개
```

### 방법 2: /review-session 스킬

```
/review-session --project ORYZA
```

## 자동 Hook 설정 (선택사항)

자동 실행을 원하는 경우 OS별로 설정이 다릅니다.

### macOS/Linux

`.claude/settings.local.json`:
```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/session_logger.py --project cosmetic-sisyphus --task 'Session completed'"
          }
        ]
      }
    ]
  }
}
```

### Windows

`.claude/settings.local.json`:
```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/hooks/session_logger.py --project cosmetic-sisyphus --task \"Session completed\""
          }
        ]
      }
    ]
  }
}
```

## 파일 구조

```
.claude/
├── hooks/
│   ├── README.md              ← 이 문서
│   ├── session_logger.py      ← 세션 로거
│   └── review_generator.py    ← 리뷰 생성기
│
├── skills/
│   └── session-review/
│       └── SKILL.md           ← /review-session 스킬 정의
│
└── settings.local.json        ← 프로젝트 설정

.sisyphus/
├── logs/
│   ├── README.md              ← 로그 폴더 설명
│   └── {date}_{project}_{task}.md
│
└── reviews/
    ├── README.md              ← 리뷰 폴더 설명
    └── {date}_review_{project}.md
```

## 트러블슈팅

### Python 실행 오류

```bash
# Windows
python --version  # Python 3.x 확인

# macOS
python3 --version
```

### 경로 오류

프로젝트 루트에서 실행 확인:
```bash
# 올바른 위치에서 실행
cd cosmetic-sisyphus
python .claude/hooks/session_logger.py --project ORYZA
```

### 인코딩 오류 (Windows)

```bash
# UTF-8 인코딩 강제
chcp 65001
python .claude/hooks/session_logger.py --project ORYZA
```
