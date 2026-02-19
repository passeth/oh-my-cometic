# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),

## v2.0.0 (2026-02-19)

### 🆕 멀티모델 라우팅
- 3티어 모델 라우팅 도입 (Opus/Sonnet/Haiku)
- 에이전트별 기본 모델 설정 (claude-sonnet-4-6, claude-haiku-4-5, claude-opus-4-6)
- ultrawork 키워드 감지 시 자동 모델 업그레이드
- 예상 비용 절감: 50-60%

### 🔧 훅 보강
- keyword-detector: 한국어 키워드 추가 (심층분석, 백서, 화이트페이퍼, 카피라이팅, K-Dense, tech dna)
- write-guard: 기존 파일 덮어쓰기 방지 (PreToolUse hook)
- context-monitor: 컨텍스트 사용량 추적 (PostToolUse hook)

### 📝 문서
- UPGRADE_PLAN_V2.md: 업그레이드 전체 계획서
- DIFF_ANALYSIS.md: oh-my-opencode v3.7.4 비교 분석
- MODEL_ROUTING_V2.md: 멀티모델 라우팅 설계
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

# Cosmetic Sisyphus (PASSETH Fork)

## [1.0.0] - 2025-01-17

### 🧪 Cosmetic Sisyphus - 화장품 R&D 특화 멀티에이전트 시스템

**oh-my-claude-sisyphus를 기반으로 화장품 연구개발에 특화된 에이전트 시스템으로 포크.**

### Added

- **6개 화장품 전문 에이전트**
  - `formulation-oracle` (Opus): 배합 설계, HLB 계산, 유화 시스템 전문가
  - `safety-oracle` (Opus): EWG/CIR/MoS 안전성 평가 전문가
  - `regulatory-oracle` (Opus): EU/한국/미국/중국/일본 규제 전문가
  - `cosmetic-librarian` (Sonnet): CosIng, 논문, 특허 리서치 전문가
  - `cosmetic-junior` (Sonnet): 배합표/보고서 작성 실무 담당
  - `ingredient-explorer` (Haiku): 성분 데이터 빠른 검색

- **2개 화장품 슬래시 커맨드**
  - `/cosmetic-analyze`: 배합/성분 종합 분석 (HLB, pH, 호환성, 안전성, 규제)
  - `/safety-check`: 성분 안전성 빠른 평가 (EWG/CIR/MoS)

### Changed

- **프로젝트 구조 정리**
  - `agents/`, `commands/`, `hooks/`, `skills/` → `.claude/` 폴더로 이동
  - 개발용 파일 제거: `src/`, `dist/`, `node_modules/` (212MB 절약)
  - 런타임 필수 파일만 유지: `.claude/`, `scripts/`

- **패키지 정보 업데이트**
  - 이름: `oh-my-cosmetic`
  - 저자: PASSETH
  - 키워드: cosmetic, formulation, skincare, r&d, inci, safety-assessment

### Technical

- hooks는 `scripts/*.mjs` 파일 사용 (Node.js 내장 모듈만 의존)
- npm 패키지 의존성 불필요 (순수 Claude Code 프로젝트)

---

# Original Sisyphus Changelog

> 아래는 원본 oh-my-claude-sisyphus의 변경 이력입니다.

## [2.0.1] - 2025-01-13

### Added
- **Vitest test framework** with comprehensive test suite (231 tests)
- **Windows native support improvements**

### Changed
- Synced shell script installer with TypeScript installer
- Removed deprecated orchestrator command

### Fixed
- Cross-platform `which` command replaced with platform-aware detection
- Auto-update now handles Windows gracefully

---

## [2.0.0-beta.2] - 2025-01-13

### Added
- **QA-Tester Agent** for interactive CLI testing using tmux
- **Smart Gating** for qa-tester in ultrawork/skills

### Refactored
- Merged sisyphus+orchestrator+ultrawork into default mode
- Removed deprecated orchestrator command

---

## [2.0.0-beta.1] - 2025-01-13

### Added
- **Intelligent Model Routing System** - Adaptive model routing for all agents
- **Complexity Signal Detection** - Lexical, structural, context analysis
- **Tiered Prompt Adaptations** - Haiku/Sonnet/Opus specific prompts

---

## [1.11.0] - 2025-01-13

### Added
- **Enhanced Hook Enforcement System**
  - `pre-tool-enforcer.sh`: PreToolUse hook
  - `post-tool-verifier.sh`: PostToolUse hook
  - Enhanced `persistent-mode.sh`: Stop hook verification

---

## [1.10.0] - 2025-01-11

### Added
- **Persistent Mode System** - Auto-continuation across sessions
- **Claude Code Native Hooks Integration**
- **Popular Plugin Patterns Module**

---

## [1.9.0] - 2025-01-10

### Changed
- Synced all builtin skills with oh-my-opencode source implementation

### Fixed
- Installer improvements and template escaping

---

## [1.8.0] - 2025-01-10

### Added
- Intelligent Skill Composition with task-type routing

---

## [1.7.0] - Previous Release

### Added
- Windows support with Node.js hooks

---

## Links

- [Cosmetic Sisyphus](https://github.com/passeth/oh-my-cometic)
- [Original Sisyphus](https://github.com/Yeachan-Heo/oh-my-claude-sisyphus)
