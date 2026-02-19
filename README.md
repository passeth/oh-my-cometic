<div align="center">

# Oh-My-Cosmetic

### Cosmetic R&D Multi-Agent System

[![Version](https://img.shields.io/badge/version-2.0.0-ff6b6b)](https://github.com/passeth/oh-my-cometic/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Native-d97706?logo=anthropic&logoColor=white)](https://docs.anthropic.com/claude-code)

**화장품 R&D를 위한 멀티에이전트 오케스트레이션 시스템**  
**Multi-agent orchestration system for cosmetic R&D**

*배합 → 안전성 → 규제 → 리서치 → 보고서까지, 전문가 에이전트가 협업합니다*

[한국어](#개요) • [English](#overview) • [Agents](#에이전트-agents) • [Install](#설치-installation)

</div>

---

## 개요

Oh-My-Cosmetic은 [oh-my-claude-sisyphus](https://github.com/Yeachan-Heo/oh-my-claude-sisyphus)를 포크하여 **화장품 연구개발(R&D)**에 특화한 Claude Code 멀티에이전트 시스템입니다.

복잡한 화장품 개발 업무를 전문 에이전트에게 자동 위임하고, 병렬로 실행하며, 완료될 때까지 멈추지 않습니다.

### 왜 만들었는가

화장품 하나를 만들려면 **배합 설계, 안전성 평가, 규제 검토, 성분 리서치, 보고서 작성**을 각각 다른 전문가가 해야 합니다. 이 시스템은 각 전문 영역을 에이전트로 분리하고, 오케스트레이터가 자동 조율합니다.

---

## Overview

Oh-My-Cosmetic is a fork of [oh-my-claude-sisyphus](https://github.com/Yeachan-Heo/oh-my-claude-sisyphus), specialized for **cosmetic R&D**. It runs on Claude Code as a multi-agent orchestration system.

It automatically delegates complex cosmetic development tasks to specialized agents, runs them in parallel, and persists until all tasks are complete.

### Why

Developing a single cosmetic product requires **formulation design, safety assessment, regulatory review, ingredient research, and report generation** — each handled by different specialists. This system separates each domain into an agent, orchestrated automatically.

---

## v2.0의 변화 | What's New in v2.0

### 🏆 3-Tier Model Routing

v1에서는 모든 에이전트가 동일 모델을 사용했습니다. v2는 작업 복잡도에 따라 모델을 자동 배분합니다.

| Tier | Model | Agents | Role |
|------|-------|--------|------|
| **Heavy** | Claude Opus | formulation-oracle, safety-oracle, regulatory-oracle | 복잡한 분석·판단 |
| **Mid** | Claude Sonnet | cosmetic-librarian, cosmetic-junior | 리서치·실무 작성 |
| **Light** | Claude Haiku | ingredient-explorer | 빠른 검색·조회 |

→ **50-60% cost reduction** while maintaining quality for complex tasks.

### 🔧 Hook System

| Hook | Function |
|------|----------|
| **keyword-detector** | 한국어/영어 키워드 감지 → 자동 에이전트 활성화 |
| **write-guard** | 기존 파일 덮어쓰기 방지 |
| **context-monitor** | 컨텍스트 사용량 추적 → 오버플로우 방지 |

### 📦 Zero Dependencies

- npm 패키지 의존성 없음 — 순수 Claude Code 프로젝트
- Hooks는 Node.js 내장 모듈만 사용 (`scripts/*.mjs`)
- v1 대비 212MB 경량화

---

## 에이전트 | Agents

### Oracle Agents (Opus — Deep Analysis)

#### 🧪 Formulation Oracle
배합/처방 전문가. HLB 계산, 유화 시스템 설계, pH 최적화, 성분 호환성 분석.

```
"이 에멀전 배합의 HLB 값 계산해줘"
"나이아신아마이드와 비타민C를 함께 쓸 수 있어?"
```

#### 🛡️ Safety Oracle
안전성 전문가. EWG/CIR 등급, MoS 계산, 자극성·감작성 예측, NOAEL/SED 분석.

```
"레티놀 0.5% 사용 시 MoS 계산해줘"
"민감성 피부용으로 자극성 예측해줘"
```

#### ⚖️ Regulatory Oracle
규제 전문가. EU CosIng, 한국 식약처, 미국 FDA, 중국 NMPA, 일본 기준.

```
"이 제품 EU 수출 가능해?"
"중국 NMPA 등록 시 필요한 서류 알려줘"
```

### Research Agent (Sonnet — Research & Writing)

#### 📚 Cosmetic Librarian
CosIng, ICID, CIR, EWG 데이터베이스 조회. 논문·특허 검색. 트렌드 분석.

```
"나이아신아마이드 최신 효능 연구 찾아줘"
"트렌디한 항산화 성분 추천해줘"
```

#### ✍️ Cosmetic Junior
실무 담당. 배합표 작성, 안전성 보고서 초안, 데이터 변환, 스케일업 계산.

```
"배합표 양식으로 정리해줘"
"안전성 보고서 초안 작성해줘"
```

### Search Agent (Haiku — Fast Lookup)

#### 🔍 Ingredient Explorer
로컬 파일 내 성분 빠른 검색. 배합표/JSON 데이터 조회.

```
"우리 배합표에서 방부제 찾아줘"
"JSON 파일에서 계면활성제 농도 확인해줘"
```

---

## 자동 활성화 | Auto-Activation

키워드를 감지하여 적합한 에이전트를 자동으로 활성화합니다.

| Keywords | Agent |
|----------|-------|
| HLB, emulsion, 유화, 점도, pH, 배합, 처방 | formulation-oracle |
| EWG, CIR, safety, MoS, 자극, 독성, 안전성 | safety-oracle |
| CPSR, CosIng, FDA, MFDS, NMPA, 규제, 인허가 | regulatory-oracle |
| ingredient, INCI, 성분, CAS | cosmetic-librarian |
| 심층분석, 백서, 화이트페이퍼, Tech DNA, K-Dense | → auto-upgrade to Opus |

---

## 설치 | Installation

### Requirements

- [Claude Code CLI](https://docs.anthropic.com/claude-code) installed
- Claude API key (Opus/Sonnet/Haiku access)

### Setup

```bash
# Clone
git clone https://github.com/passeth/oh-my-cometic.git
cd oh-my-cometic

# That's it. Open Claude Code in this directory.
claude
```

No `npm install`. No build step. Just clone and use.

### Verify

```bash
# Inside Claude Code
/cosmetic-analyze HLB 계산해줘
/safety-check Retinol 0.5%
```

---

## 프로젝트 구조 | Structure

```
oh-my-cometic/
├── .claude/
│   ├── agents/              # 6 specialist agents
│   │   ├── formulation-oracle.md
│   │   ├── safety-oracle.md
│   │   ├── regulatory-oracle.md
│   │   ├── cosmetic-librarian.md
│   │   ├── cosmetic-junior.md
│   │   └── ingredient-explorer.md
│   ├── commands/            # Slash commands
│   ├── hooks/               # Hook configs
│   └── skills/              # Additional skills
├── scripts/                 # Hook scripts (Node.js)
│   ├── keyword-detector.mjs
│   ├── write-guard.sh
│   └── context-monitor.sh
├── docs/                    # Design documents
├── CLAUDE.md                # System prompt
└── CHANGELOG.md
```

---

## 작동 방식 | How It Works

```
사용자 입력
    ↓
[keyword-detector] → 키워드 분석 → 에이전트 선택
    ↓
[prometheus orchestrator] → TODO 생성 → 작업 분배
    ↓
┌─────────────┬──────────────┬─────────────┐
│ Opus Agent  │ Sonnet Agent │ Haiku Agent │
│ (분석·판단)  │ (리서치·작성) │ (빠른 검색)  │
└─────────────┴──────────────┴─────────────┘
    ↓
[write-guard] → 파일 안전 검증
    ↓
[context-monitor] → 컨텍스트 추적
    ↓
완료 (TODO 리스트 비워질 때까지 반복)
```

---

## Credits

- [oh-my-claude-sisyphus](https://github.com/Yeachan-Heo/oh-my-claude-sisyphus) by Yeachan Heo — Original multi-agent framework
- Forked and specialized for cosmetic R&D by [PASSETH](https://github.com/passeth)

## License

MIT License — See [LICENSE](LICENSE) for details.

---

<div align="center">

*Built with 🧪 by PASSETH × EVAS Cosmetic*

</div>
