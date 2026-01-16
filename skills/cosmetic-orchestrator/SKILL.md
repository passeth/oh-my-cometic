---
name: cosmetic-orchestrator
description: 화장품 R&D 멀티 에이전트 오케스트레이터. 사용자 요청을 분석하여 적절한 에이전트를 순차적으로 실행하고, 각 단계의 결과를 취합하여 최종 보고서를 생성합니다.
version: 1.0.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - TodoWrite
  - WebFetch
license: MIT
metadata:
  category: workflow-orchestration
  domain: cosmetics
  language: ko
  tags:
    - orchestrator
    - multi-agent
    - workflow-automation
    - session-management
  dependencies:
    - cosmetic-context-initialization
    - get-available-resources
  related-skills:
    - cosmetic-context-initialization
    - get-available-resources
    - formulation-calculator
    - regulatory-compliance
    - claim-substantiation
---

# Cosmetic Orchestrator Skill

## Overview

화장품 R&D 작업을 위한 멀티 에이전트 오케스트레이션 시스템입니다. 사용자의 요청을 받아 5단계 에이전트 파이프라인을 통해 종합적인 결과물을 생성합니다.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    COSMETIC ORCHESTRATOR (Main)                         │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  - Creates session directory (./sessions/{timestamp}/)            │  │
│  │  - Manages TodoWrite state across all phases                      │  │
│  │  - Passes context between subagents                               │  │
│  │  - Collects and validates all phase reports                       │  │
│  │  - Generates final consolidated output                            │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
         spawn + {user_request, session_dir, SKILL_DIR}
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Phase 1: CONTEXT INITIALIZATION AGENT                                  │
│  ────────────────────────────────────                                   │
│  Skill: cosmetic-context-initialization                                 │
│  Tasks:                                                                 │
│    - Parse user request and extract keywords                           │
│    - Detect project type (planning/R&D/regulatory/marketing)           │
│    - Identify required skill categories                                 │
│    - Establish session context                                          │
│                                                                         │
│  Returns: context_report.md + {project_type, keywords[], domain}        │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
         spawn + {context_report, session_dir}
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Phase 2: RESOURCE DISCOVERY AGENT                                      │
│  ────────────────────────────────                                       │
│  Skill: get-available-resources                                         │
│  Tasks:                                                                 │
│    - Scan available skills and capabilities                            │
│    - Match skills to detected project type                             │
│    - Generate skill recommendations (primary/secondary)                 │
│    - Check skill implementation status                                  │
│                                                                         │
│  Returns: resource_report.md + {recommended_skills[], available_mcps[]} │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
         spawn + {context_report, resource_report, recommended_skills[]}
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Phase 3: SPECIALIST EXECUTION AGENT(S)                                 │
│  ─────────────────────────────────────                                  │
│  Dynamic: Uses recommended skills from Phase 2                          │
│  Agent Types:                                                           │
│    - formulation-agent: HLB, pH, stability calculations                 │
│    - safety-agent: EWG, CIR, toxicity analysis                         │
│    - regulatory-agent: Multi-country compliance check                   │
│    - trend-agent: Market analysis, consumer insights                    │
│    - efficacy-agent: Claim substantiation, clinical design              │
│                                                                         │
│  Returns: specialist_report.md + {task_results[], artifacts[]}          │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
         spawn + {all_reports, task_results[]}
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Phase 4: VALIDATION AGENT                                              │
│  ─────────────────────────────                                          │
│  Tasks:                                                                 │
│    - Verify completeness of specialist outputs                         │
│    - Cross-check data consistency                                       │
│    - Identify gaps or missing information                               │
│    - Generate action items for unresolved issues                        │
│                                                                         │
│  Returns: validation_report.md + {issues[], revised_action_items[]}     │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
         spawn + {all_reports, validation_report, revised_action_items[]}
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Phase 5: SYNTHESIS AGENT                                               │
│  ──────────────────────────                                             │
│  Tasks:                                                                 │
│    - Consolidate all phase outputs                                      │
│    - Generate executive summary                                         │
│    - Create actionable recommendations                                  │
│    - Produce final deliverable document                                 │
│                                                                         │
│  Returns: final_report.md + {summary, recommendations[], next_steps[]}  │
└─────────────────────────────────────────────────────────────────────────┘
```

## When to Use

이 오케스트레이터는 다음과 같은 복잡한 작업에 사용합니다:

1. **신제품 개발 전체 사이클**
   - 트렌드 분석 → 성분 선정 → 배합 설계 → 규제 검토 → 클레임 개발

2. **종합 성분 분석**
   - 안전성 + 효능 + 규제 상태 + 호환성 종합 평가

3. **수출 규제 대응**
   - 다중 국가 규제 확인 + CPSR 생성 + 라벨링 검토

4. **제형 최적화**
   - 기존 제형 분석 → 개선점 도출 → 안정성 예측 → 최적화 제안

## Session Management

### 세션 디렉토리 구조

```
sessions/
└── {YYYYMMDD_HHMMSS}_{project_type}/
    ├── session_config.json          # 세션 설정
    ├── phase1_context_report.md     # Phase 1 출력
    ├── phase2_resource_report.md    # Phase 2 출력
    ├── phase3_specialist_report.md  # Phase 3 출력
    ├── phase4_validation_report.md  # Phase 4 출력
    ├── phase5_final_report.md       # Phase 5 출력 (최종)
    ├── artifacts/                   # 생성된 아티팩트
    │   ├── calculations/            # 계산 결과
    │   ├── charts/                  # 시각화
    │   └── data/                    # 데이터 파일
    └── logs/                        # 실행 로그
        └── orchestrator.log
```

### session_config.json 구조

```json
{
  "session_id": "20250116_143022_formulation",
  "created_at": "2025-01-16T14:30:22",
  "user_request": "비타민C 20% 세럼 제형 개발",
  "project_type": "R&D",
  "detected_keywords": ["비타민C", "세럼", "제형"],
  "phases": {
    "phase1": {
      "status": "completed",
      "agent": "context-initialization",
      "output": "phase1_context_report.md",
      "duration_sec": 12
    },
    "phase2": {
      "status": "completed",
      "agent": "resource-discovery",
      "output": "phase2_resource_report.md",
      "duration_sec": 8
    },
    "phase3": {
      "status": "in_progress",
      "agent": "formulation-specialist",
      "output": null,
      "started_at": "2025-01-16T14:30:42"
    },
    "phase4": {"status": "pending"},
    "phase5": {"status": "pending"}
  },
  "recommended_skills": [
    "formulation-calculator",
    "formulation-strategy",
    "ingredient-compatibility",
    "stability-predictor"
  ],
  "artifacts": [],
  "total_duration_sec": null
}
```

## Agent Definitions

### Phase 1: Context Initialization Agent

```yaml
agent_id: context-initialization-agent
skill_dependency: cosmetic-context-initialization
inputs:
  - user_request: string
  - session_dir: path
  - skill_dir: path

tasks:
  1. parse_request:
     - Extract cosmetic-related keywords
     - Identify product types (serum, cream, toner, etc.)
     - Detect active ingredients mentioned

  2. detect_project_type:
     - Categories: planning, r_and_d, regulatory, marketing, safety
     - Analyze intent signals

  3. establish_context:
     - Create session_config.json
     - Initialize TodoWrite with high-level tasks
     - Set up logging

outputs:
  report_path: phase1_context_report.md
  context_data:
    project_type: string
    keywords: string[]
    intent: string
    domain_signals: object
```

### Phase 2: Resource Discovery Agent

```yaml
agent_id: resource-discovery-agent
skill_dependency: get-available-resources
inputs:
  - context_report: path
  - session_dir: path
  - project_type: string

tasks:
  1. scan_skills:
     - Read all SKILL.md files
     - Check implementation status
     - Catalog available scripts and references

  2. match_skills:
     - Map project_type to skill categories
     - Rank skills by relevance
     - Check dependencies

  3. check_mcps:
     - Detect available MCP servers
     - Match MCPs to task requirements
     - Note API key requirements

outputs:
  report_path: phase2_resource_report.md
  resource_data:
    recommended_skills:
      primary: string[]
      secondary: string[]
    available_mcps: string[]
    skill_status: object
```

### Phase 3: Specialist Execution Agent

```yaml
agent_id: specialist-agent
skill_dependency: [dynamic based on Phase 2]
inputs:
  - context_report: path
  - resource_report: path
  - recommended_skills: string[]
  - session_dir: path

specialist_types:
  formulation:
    skills: [formulation-calculator, formulation-strategy, ingredient-compatibility]
    tasks: [HLB calculation, base selection, compatibility check]

  safety:
    skills: [ewg-skindeep, cir-safety, cosdna-analysis, irritation-predictor]
    tasks: [safety scoring, toxicity review, irritation prediction]

  regulatory:
    skills: [regulatory-compliance, regulatory-checker, cosing-database, cpsr-generator]
    tasks: [multi-country check, compliance verification, CPSR generation]

  trend:
    skills: [trend-analysis, consumer-insight, mintel-gnpd, product-positioning]
    tasks: [market analysis, consumer research, positioning strategy]

  efficacy:
    skills: [claim-substantiation, ingredient-efficacy-analyzer, cosmetic-clinical-reports]
    tasks: [claim design, efficacy analysis, clinical study design]

outputs:
  report_path: phase3_specialist_report.md
  task_results:
    - task_name: string
      skill_used: string
      result: object
      artifacts: path[]
```

### Phase 4: Validation Agent

```yaml
agent_id: validation-agent
inputs:
  - all_phase_reports: path[]
  - task_results: object[]
  - session_dir: path

tasks:
  1. completeness_check:
     - Verify all required outputs present
     - Check for empty or null values
     - Validate data formats

  2. consistency_check:
     - Cross-reference data across phases
     - Detect contradictions
     - Verify calculation accuracy

  3. gap_analysis:
     - Identify missing information
     - Note unanswered questions
     - Flag incomplete analyses

  4. generate_action_items:
     - Create list of issues
     - Prioritize by impact
     - Suggest remediation steps

outputs:
  report_path: phase4_validation_report.md
  validation_data:
    completeness_score: number (0-100)
    issues: object[]
    revised_action_items: string[]
    warnings: string[]
```

### Phase 5: Synthesis Agent

```yaml
agent_id: synthesis-agent
inputs:
  - all_phase_reports: path[]
  - validation_report: path
  - revised_action_items: string[]
  - session_dir: path

tasks:
  1. consolidate:
     - Merge all phase outputs
     - Remove duplicates
     - Organize by category

  2. summarize:
     - Create executive summary
     - Highlight key findings
     - Note critical decisions

  3. recommend:
     - Generate actionable recommendations
     - Prioritize next steps
     - Suggest follow-up tasks

  4. format_deliverable:
     - Create final report document
     - Include all artifacts
     - Add appendices

outputs:
  report_path: phase5_final_report.md
  final_data:
    executive_summary: string
    key_findings: string[]
    recommendations: string[]
    next_steps: string[]
    deliverables: path[]
```

## Usage Examples

### Example 1: 신제품 개발 요청

```
User: "민감성 피부용 CICA 크림 개발하려고 해. 트렌드 분석부터 배합 설계, 규제 검토까지 전체 프로세스 진행해줘."

Orchestrator Flow:
├── Phase 1: Context Initialization
│   ├── Project Type: R&D + Planning
│   ├── Keywords: ["민감성 피부", "CICA", "크림", "센텔라"]
│   └── Domain: skincare, sensitive-skin
│
├── Phase 2: Resource Discovery
│   ├── Primary Skills: trend-analysis, consumer-insight, formulation-strategy
│   ├── Secondary Skills: ingredient-compatibility, regulatory-checker
│   └── MCPs: brave-search (트렌드), supabase (데이터)
│
├── Phase 3: Specialist Execution
│   ├── Trend Agent: CICA 시장 트렌드, 경쟁 제품 분석
│   ├── Formulation Agent: 크림 베이스 설계, 센텔라 배합
│   └── Regulatory Agent: 한국/EU 규제 확인
│
├── Phase 4: Validation
│   ├── Completeness: 95%
│   ├── Issues: [성분 농도 미결정]
│   └── Action Items: ["센텔라 추출물 농도 확정 필요"]
│
└── Phase 5: Synthesis
    └── Final Report: 종합 개발 계획서 + 배합 제안 + 규제 체크리스트
```

### Example 2: 성분 안전성 종합 분석

```
User: "레티놀 0.5% 포함 제품의 안전성 종합 분석해줘"

Orchestrator Flow:
├── Phase 1: Project Type: Safety
├── Phase 2: Skills: [ewg-skindeep, cir-safety, cpsr-generator, irritation-predictor]
├── Phase 3:
│   ├── EWG 등급 조회
│   ├── CIR 안전성 결론 확인
│   ├── MoS 계산 (CPSR용)
│   └── 자극성 예측
├── Phase 4: 데이터 일관성 검증
└── Phase 5: 안전성 종합 보고서 생성
```

## Error Handling

### Phase 실패 시 처리

```yaml
on_phase_failure:
  phase1:
    - Log error to orchestrator.log
    - Attempt keyword-free detection
    - If still fails: request user clarification

  phase2:
    - Use default skill set for detected project type
    - Continue with reduced capability warning

  phase3:
    - Retry failed skill once
    - Skip unavailable skills
    - Document gaps in validation

  phase4:
    - Mark validation as partial
    - Include caveat in final report

  phase5:
    - Generate partial report
    - List incomplete sections
    - Suggest manual follow-up
```

### Timeout 관리

```yaml
timeouts:
  phase1: 30s
  phase2: 30s
  phase3: 300s  # 5 minutes (longest phase)
  phase4: 60s
  phase5: 120s
  total_session: 600s  # 10 minutes max
```

## Integration with MCP

### 사용 가능한 MCP 서버

| MCP Server | Phase | 용도 |
|------------|-------|------|
| supabase | 3, 5 | 데이터 저장/조회 |
| brave-search | 3 | 트렌드 검색 |
| sequential-thinking | 3, 4 | 복잡한 분석 |
| infranodus | 3, 5 | 지식 그래프 생성 |
| github | 5 | 코드/문서 관리 |

### MCP 연동 예시

```python
# Phase 3에서 brave-search MCP 사용
async def search_trend(keyword: str):
    results = await mcp.brave_search.web_search(
        query=f"{keyword} cosmetic trend 2025",
        count=10
    )
    return parse_trend_results(results)

# Phase 5에서 supabase MCP로 결과 저장
async def save_session_result(session_data: dict):
    await mcp.supabase.execute_sql(
        query="INSERT INTO cosmetic_sessions (...) VALUES (...)",
        params=session_data
    )
```

## Best Practices

1. **세션 재사용**: 이전 세션 결과를 참조하여 반복 작업 최소화
2. **단계별 검증**: 각 Phase 완료 후 결과 확인 후 다음 단계 진행
3. **점진적 상세화**: 초기에는 넓은 분석, 점차 특정 영역에 집중
4. **아티팩트 보존**: 모든 중간 결과물 세션 디렉토리에 저장
5. **명시적 종료**: 작업 완료 시 세션 상태 명시적으로 마감

## Notes

- 이 스킬은 claude-cosmetic-skills의 최상위 진입점입니다
- 모든 다른 스킬은 Phase 3의 Specialist Agent를 통해 호출됩니다
- 세션 데이터는 로컬에 저장되며, Supabase 연동 시 클라우드 동기화 가능
- 복잡한 작업은 여러 세션에 걸쳐 진행될 수 있습니다
