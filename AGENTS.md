# PROJECT KNOWLEDGE BASE

**Project:** Oh-My-Cosmetic (Cosmetic Sisyphus)
**Version:** 1.0.0
**Purpose:** 화장품 R&D 전문 멀티에이전트 오케스트레이션 시스템
**Based on:** oh-my-claude-sisyphus

## OVERVIEW

Oh-My-Cosmetic은 Claude Code를 위한 **화장품 R&D 전문 멀티에이전트 시스템**입니다. 기존 oh-my-claude-sisyphus의 강력한 오케스트레이션 기능에 화장품 배합, 안전성, 규제 분석 전문 에이전트와 38개의 화장품 스킬을 추가했습니다.

**화장품 R&D 전문 기능:**
- 🧪 **Formulation Oracle** - HLB 계산, pH 최적화, 유화 시스템 설계
- 🔬 **Safety Oracle** - EWG/CIR 안전성 평가, MoS 계산, NOAEL 분석
- 📜 **Regulatory Oracle** - EU/한국/미국/중국/일본 규제 검토, CPSR 가이드
- 📚 **Cosmetic Librarian** - CosIng/ICID 데이터베이스, PubMed 연구 검색
- 🔍 **Ingredient Explorer** - 빠른 INCI/CAS 조회
- 📝 **Cosmetic Junior** - 배합표/보고서 작성, 스케일업 계산

**Key Features:**
- **🚀 NEW: Intelligent Model Routing** - Orchestrator analyzes complexity and routes to optimal model (Haiku/Sonnet/Opus)
- Multi-agent orchestration with specialized subagents
- Persistent work loops (Ralph Loop)
- Boulder state management for complex plans
- Magic keyword detection (ultrawork, ultrathink, analyze, search)
- Todo continuation enforcement
- Rules injection from project/user config
- Automatic edit error recovery

## v2.0 INTELLIGENT MODEL ROUTING

The orchestrator (always Opus) analyzes task complexity BEFORE delegation:

| Task Type | Routes To | Example |
|-----------|-----------|---------|
| Simple lookup | **Haiku** | "Where is auth configured?" |
| Module work | **Sonnet** | "Add validation to login form" |
| Complex/risky | **Opus** | "Debug this race condition" |

**All agents are adaptive** (except orchestrators). See `src/features/model-routing/` for implementation.

## STRUCTURE

```
oh-my-claude-sisyphus/
├── src/
│   ├── agents/              # 12 agent definitions
│   │   ├── definitions.ts   # Agent registry & configs
│   │   ├── types.ts         # Agent type definitions
│   │   ├── utils.ts         # Shared utilities
│   │   ├── oracle.ts        # Complex debugging/architecture
│   │   ├── explore.ts       # Fast codebase search
│   │   ├── librarian.ts     # Documentation research
│   │   ├── sisyphus-junior.ts  # Focused execution
│   │   ├── frontend-engineer.ts # UI/UX work
│   │   ├── document-writer.ts   # Technical docs
│   │   ├── multimodal-looker.ts # Visual analysis
│   │   ├── momus.ts         # Critical plan review
│   │   ├── metis.ts         # Pre-planning analysis
│   │   ├── orchestrator-sisyphus.ts  # Todo coordination
│   │   ├── prometheus.ts    # Strategic planning
│   │   └── qa-tester.ts     # CLI/service testing with tmux
│   ├── hooks/               # 8 hook modules
│   │   ├── keyword-detector/    # Magic keyword detection
│   │   ├── ralph-loop/          # Self-referential work loops
│   │   ├── todo-continuation/   # Task completion enforcement
│   │   ├── edit-error-recovery/ # Edit failure handling
│   │   ├── think-mode/          # Enhanced thinking modes
│   │   ├── rules-injector/      # Rule file injection
│   │   ├── sisyphus-orchestrator/ # Orchestrator behavior
│   │   ├── auto-slash-command/  # Slash command detection
│   │   └── bridge.ts            # Shell hook bridge
│   ├── features/            # 6 feature modules
│   │   ├── model-routing/       # 🆕 v2.0: Intelligent model routing
│   │   │   ├── types.ts         # Routing types & config
│   │   │   ├── signals.ts       # Complexity signal extraction
│   │   │   ├── scorer.ts        # Weighted complexity scoring
│   │   │   ├── rules.ts         # Routing rules engine
│   │   │   ├── router.ts        # Main routing logic
│   │   │   └── prompts/         # Tier-specific prompt adaptations
│   │   ├── boulder-state/       # Plan state management
│   │   ├── context-injector/    # Context enhancement
│   │   ├── background-agent/    # Background task management
│   │   ├── builtin-skills/      # Bundled skill definitions
│   │   ├── magic-keywords.ts    # Keyword processing
│   │   ├── continuation-enforcement.ts
│   │   └── auto-update.ts       # Silent auto-update
│   ├── installer/           # Installation system
│   │   ├── index.ts         # Main installer (SKILL_DEFINITIONS, etc.)
│   │   └── hooks.ts         # Hook generation
│   └── index.ts             # Main exports
├── dist/                    # Build output (ESM)
└── .sisyphus/               # Runtime state directory
    ├── plans/               # Prometheus plans
    └── notepads/            # Session notes
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| Add agent | `src/agents/` | Create .ts, add to agentDefinitions in definitions.ts |
| Add hook | `src/hooks/` | Create dir, export from index.ts, add to bridge.ts |
| Add feature | `src/features/` | Create dir, export from index.ts |
| Add skill | `src/installer/index.ts` | Add to SKILL_DEFINITIONS |
| Agent types | `src/agents/types.ts` | AgentDefinition, AgentMetadata interfaces |
| Hook types | `src/hooks/<name>/types.ts` | Hook-specific types |
| State mgmt | `src/features/boulder-state/` | BoulderState, plan progress |
| Background tasks | `src/features/background-agent/` | BackgroundManager class |
| Shell hooks | `src/hooks/bridge.ts` | processHook() entry point |

## AGENTS

### 화장품 전문 에이전트 (Cosmetic Specialists)

| Agent | Model | Purpose | Key Skills |
|-------|-------|---------|------------|
| **formulation-oracle** | Opus | 배합/처방 전문가 | formulation-calculator, stability-predictor, ingredient-compatibility |
| **safety-oracle** | Opus | 안전성 전문가 | ewg-skindeep, cir-safety, irritation-predictor, cpsr-generator |
| **regulatory-oracle** | Opus | 규제 전문가 | regulatory-compliance, regulatory-checker, cpsr-generator |
| **cosmetic-librarian** | Sonnet | 연구/DB 전문가 | cosing-database, kfda-ingredient, pubmed-search, icid-database |
| **ingredient-explorer** | Haiku | 빠른 성분 조회 | incidecoder-analysis, cosdna-analysis |
| **cosmetic-junior** | Sonnet | 실무 구현 | batch-calculator, inci-converter, report generation |

### 범용 에이전트 (General Purpose)

| Agent | Model | Purpose | Key Traits |
|-------|-------|---------|------------|
| **oracle** | Opus | Architecture, debugging | Deep analysis, root cause finding, cosmetic domain routing |
| **librarian** | Sonnet | Documentation, research | Multi-repo analysis, doc lookup, cosmetic delegation |
| **explore** | Haiku | Fast codebase search | Quick pattern matching, cosmetic file patterns |
| **sisyphus-junior** | Sonnet | Focused execution | Direct task implementation |
| **frontend-engineer** | Sonnet | UI/UX work | Component design, styling |
| **document-writer** | Haiku | Technical docs | README, API docs |
| **multimodal-looker** | Sonnet | Visual analysis | Screenshots, diagrams |
| **momus** | Opus | Plan review | Critical evaluation |
| **metis** | Opus | Pre-planning | Hidden requirements |
| **prometheus** | Opus | Strategic planning | Interview-style planning |
| **qa-tester** | Sonnet | CLI/service testing | Interactive tmux testing |

### 에이전트 라우팅 (Agent Routing)

화장품 관련 쿼리는 자동으로 전문 에이전트에게 위임됩니다:

| 키워드 | 위임 대상 | 예시 |
|-------|----------|-----|
| 배합, 처방, HLB, 유화, pH | **formulation-oracle** | "이 에멀전 HLB 계산해줘" |
| 안전성, EWG, CIR, MoS, 자극성 | **safety-oracle** | "레티놀 0.5% MoS 계산해줘" |
| 규제, CPSR, CosIng, FDA, NMPA | **regulatory-oracle** | "EU 수출 가능 여부 확인해줘" |
| 성분, INCI, CAS, PubMed | **cosmetic-librarian** | "나이아신아마이드 연구 찾아줘" |
| 빠른 조회, INCIDecoder, CosDNA | **ingredient-explorer** | "레티놀 CAS 번호 확인해줘" |

## HOOKS

| Hook | Event | Purpose |
|------|-------|---------|
| **keyword-detector** | UserPromptSubmit | Detect ultrawork/ultrathink/search/analyze |
| **ralph-loop** | Stop | Enforce work continuation until completion |
| **todo-continuation** | Stop | Block stop if todos remain |
| **edit-error-recovery** | PostToolUse | Inject recovery hints on edit failures |
| **think-mode** | UserPromptSubmit | Activate extended thinking |
| **rules-injector** | PostToolUse (Read/Edit) | Inject matching rule files |
| **sisyphus-orchestrator** | PreToolUse, PostToolUse | Enforce delegation, add verification |
| **auto-slash-command** | UserPromptSubmit | Detect and expand /commands |

## SKILLS

### 시스템 스킬 (System Skills)

| Skill | Description |
|-------|-------------|
| **orchestrator** | Master coordinator for complex tasks |
| **sisyphus** | Multi-agent orchestration mode |
| **ralph-loop** | Self-referential loop until completion |
| **frontend-ui-ux** | Designer-turned-developer aesthetic |
| **git-master** | Atomic commits, rebasing, history search |
| **ultrawork** | Maximum performance parallel mode |

### 화장품 스킬 (Cosmetic Skills - 38개)

#### K-Dense 핵심 스킬 (5개)

| Skill | Description |
|-------|-------------|
| **pubmed-search** | PubMed 학술 검색 및 논문 정보 추출 |
| **ingredient-deep-dive** | 성분 심층 분석 보고서 생성 |
| **mechanism-diagram-generator** | 작용 기전 Mermaid 다이어그램 생성 |
| **clinical-evidence-aggregator** | 임상 근거 수집 및 등급화 |
| **reference-manager** | 학술 참고문헌 관리 및 인용 형식 |

#### 데이터베이스/API 연동 스킬 (11개)

| Skill | Description |
|-------|-------------|
| **cosing-database** | EU CosIng 성분 규제 정보 |
| **kfda-ingredient** | 한국 식약처 기능성 성분 DB |
| **ewg-skindeep** | EWG Skin Deep 안전성 등급 |
| **cir-safety** | CIR 성분 안전성 리뷰 |
| **mintel-gnpd** | Mintel GNPD 글로벌 신제품 트렌드 |
| **ifra-standards** | IFRA 향료 사용 기준 |
| **icid-database** | ICID 국제 성분 사전 |
| **ulprospector-integration** | UL Prospector 원료 공급업체 정보 |
| **cosmily-integration** | Cosmily 성분 분석 데이터 |
| **incidecoder-analysis** | INCIDecoder 성분 해석 정보 |
| **cosdna-analysis** | CosDNA 성분 분석 데이터 |

#### 분석/계산 스킬 (9개)

| Skill | Description |
|-------|-------------|
| **formulation-calculator** | 포뮬레이션 계산기 - 배합 비율 계산 |
| **ingredient-compatibility** | 성분 호환성 검사 - 배합 금기 확인 |
| **stability-predictor** | 안정성 예측 - 제형 안정성 분석 |
| **skin-penetration** | 피부 투과 예측 - 성분 전달 분석 |
| **irritation-predictor** | 자극성 예측 - 민감성 평가 |
| **rdkit-cosmetic** | 분자 특성 계산 - 화학적 분석 |
| **concentration-converter** | 농도 단위 변환 - ppm, %, mg/mL |
| **batch-calculator** | 배치 계산기 - 생산량 스케일업 |
| **ingredient-efficacy-analyzer** | 성분 효능 분석 - 효능 비교 |

#### 규제/문서 스킬 (5개)

| Skill | Description |
|-------|-------------|
| **regulatory-compliance** | 규제 준수 확인 - 글로벌 |
| **regulatory-checker** | 규제 요건 검사 - 한국/EU/미국 |
| **claim-substantiation** | 클레임 근거 생성 - 마케팅 클레임 |
| **cpsr-generator** | CPSR 문서 생성 - EU 규정 |
| **inci-converter** | INCI명 변환 - 전성분 표기 |

#### 마케팅/전략 스킬 (4개)

| Skill | Description |
|-------|-------------|
| **product-positioning** | 제품 포지셔닝 분석 - 시장 전략 |
| **consumer-insight** | 소비자 인사이트 - 고객 분석 |
| **trend-analysis** | 트렌드 분석 - 시장 동향 |
| **formulation-strategy** | 포뮬레이션 전략 - 제형 기획 |

#### 시스템/유틸리티 스킬 (4개)

| Skill | Description |
|-------|-------------|
| **cosmetic-context-initialization** | 컨텍스트 초기화 - 세션 설정 |
| **get-available-resources** | 리소스 확인 - 사용 가능 도구 |
| **cosmetic-orchestrator** | 워크플로우 오케스트레이션 - 스킬 조합 |
| **cosmetic-clinical-reports** | 임상 보고서 생성 - 문서 출력 |

## CONVENTIONS

- **Runtime**: Node.js (not Bun)
- **Build**: TypeScript with ESM output
- **Package**: npm
- **Testing**: Manual verification (no test framework)
- **Hooks**: Shell-based (Claude Code native)
- **State**: JSON files in `~/.claude/.sisyphus/`
- **Naming**: kebab-case directories, createXXXHook factories

## ANTI-PATTERNS

- **Direct implementation by orchestrator**: Must delegate via Task tool
- **Skipping verification**: Always verify subagent claims
- **Sequential when parallel possible**: Use multiple Task calls
- **Batching todos**: Mark complete immediately
- **Giant commits**: 3+ files = 2+ commits minimum
- **Trusting self-reports**: Verify with own tool calls
- **Stopping with incomplete todos**: Ralph Loop prevents this

## COMMANDS

```bash
npm run build        # Build TypeScript
npm run typecheck    # Type check only
npm run install:dev  # Install to ~/.claude
```

## STATE FILES

| File | Purpose |
|------|---------|
| `~/.claude/.sisyphus/boulder.json` | Active plan state |
| `~/.claude/.sisyphus/ralph.json` | Ralph Loop state |
| `~/.claude/.sisyphus/rules-injector/*.json` | Injected rules tracking |
| `~/.claude/.sisyphus/background-tasks/*.json` | Background task state |

## CONFIGURATION

Settings live in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      "~/.claude/sisyphus/hooks/keyword-detector.sh"
    ],
    "Stop": [
      "~/.claude/sisyphus/hooks/todo-continuation.sh"
    ]
  }
}
```

## SLASH COMMANDS

### 시스템 명령어

| Command | Description |
|---------|-------------|
| `/sisyphus <task>` | Activate multi-agent orchestration |
| `/ultrawork <task>` | Maximum performance mode |
| `/plan <description>` | Start planning with Prometheus |
| `/review [plan]` | Review plan with Momus |
| `/ralph-loop <task>` | Self-referential loop |
| `/cancel-ralph` | Cancel active Ralph Loop |
| `/orchestrator <task>` | Complex task coordination |
| `/deepsearch <query>` | Thorough codebase search |
| `/analyze <target>` | Deep analysis |

### 화장품 명령어

| Command | Description | 예시 |
|---------|-------------|-----|
| `/formulation <query>` | 배합/처방 분석 | `/formulation HLB 계산해줘` |
| `/safety-check <ingredient>` | 안전성 평가 | `/safety-check Retinol 0.5%` |
| `/regulatory <market>` | 규제 분석 | `/regulatory EU 수출` |
| `/ingredient <name>` | 성분 정보 조회 | `/ingredient Niacinamide` |
| `/cosmetic <task>` | 화장품 모드 활성화 | `/cosmetic 에센스 배합 설계` |
| `/pubmed-search <query>` | PubMed 학술 검색 | `/pubmed-search niacinamide barrier` |
| `/ingredient-deep-dive <name>` | 성분 심층 분석 | `/ingredient-deep-dive Retinol` |

## COMPLEXITY HOTSPOTS

| File | Lines | Description |
|------|-------|-------------|
| `src/installer/index.ts` | 2000+ | SKILL_DEFINITIONS, CLAUDE_MD_CONTENT |
| `src/agents/definitions.ts` | 600+ | All agent configurations |
| `src/hooks/bridge.ts` | 320+ | Main hook processor |
| `src/features/boulder-state/storage.ts` | 200+ | Plan state management |

## NOTES

- **Claude Code Version**: Requires Claude Code CLI
- **Installation**: `git clone && npm install && npm run build && ./scripts/install.sh`
- **Updates**: Silent auto-update checks
- **Compatibility**: Designed for Claude Code, not OpenCode
- **State Persistence**: Uses ~/.claude/.sisyphus/ directory
- **Hook System**: Shell scripts → TypeScript bridge → JSON output
- **Cosmetic Skills**: 38개 화장품 전문 스킬 (`skills/` 디렉토리)
- **Skill Structure**: 각 스킬은 `SKILL.md`, `scripts/`, `references/` 포함
- **Output Directory**: `outputs/` - 생성된 보고서 및 분석 결과
- **Reports Directory**: `reports/` - 분석 보고서

## COSMETIC PROJECT STRUCTURE

```
oh-my-cosmetic/
├── skills/                     # 38개 화장품 스킬
│   ├── formulation-calculator/ # 배합 계산
│   ├── ewg-skindeep/           # EWG 안전성 조회
│   ├── cosing-database/        # EU CosIng DB
│   ├── pubmed-search/          # PubMed 검색
│   └── ...                     # 34개 추가 스킬
├── src/agents/                 # 에이전트 정의
│   ├── formulation-oracle.ts   # 배합 전문가
│   ├── safety-oracle.ts        # 안전성 전문가
│   ├── regulatory-oracle.ts    # 규제 전문가
│   ├── cosmetic-librarian.ts   # 연구 전문가
│   ├── ingredient-explorer.ts  # 빠른 조회
│   └── cosmetic-junior.ts      # 실무 구현
├── outputs/                    # 생성된 결과물
├── reports/                    # 분석 보고서
└── docs/                       # 문서
    ├── COSMETIC_CLAUDE.md      # 화장품 오케스트레이션 가이드
    └── SKILL_INVENTORY.md      # 스킬 인벤토리
```
