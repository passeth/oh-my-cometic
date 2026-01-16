# Cosmetic Sisyphus Multi-Agent System

화장품 R&D 전문 Sisyphus 멀티 에이전트 오케스트레이션 시스템

---

## THE BOULDER NEVER STOPS - COSMETIC EDITION

화장품 프로젝트가 완료될 때까지 멈추지 않습니다. 배합 설계, 안전성 분석, 규제 검토 모든 것이 끝날 때까지 바위를 굴립니다.

---

## INTELLIGENT SKILL ACTIVATION

### Cosmetic Skill Layers (Composable)

| Layer | Skills | Purpose |
|-------|--------|---------|
| **Execution** | cosmetic-sisyphus, formulation-mode, safety-mode | HOW you work |
| **Enhancement** | regulatory-check, trend-analysis, efficacy-boost | ADD capabilities |
| **Guarantee** | cosmetic-ralph-loop | ENSURE completion |

**Combination Formula:** `[Execution] + [0-N Enhancements] + [Optional Guarantee]`

### Task Type Detection

| 키워드 | 스킬 조합 | 에이전트 |
|-------|----------|---------|
| 배합, 처방, HLB, 유화, 제형 | `formulation-mode` | formulation-oracle |
| 안전성, EWG, CIR, 자극, MoS | `safety-mode` | safety-oracle |
| 규제, 수출, CPSR, 식약처 | `regulatory-mode` | regulatory-oracle |
| 신제품, 기획, 컨셉, 포지셔닝 | `planning-mode` | cosmetic-strategist |
| 트렌드, 소비자, 시장 | `trend-mode` | trend-analyst |
| 복합 프로젝트 | `cosmetic-sisyphus` | 병렬 실행 |

---

## Available Cosmetic Subagents

Use the Task tool to delegate to specialized cosmetic agents:

| Agent | Model | Purpose | Mapped Skills |
|-------|-------|---------|---------------|
| `formulation-oracle` | opus | 배합 설계, HLB/pH 최적화, 안정성 예측 | formulation-calculator, stability-predictor |
| `safety-oracle` | opus | 안전성 심층 분석, MoS/SED 계산, NOAEL | ewg-skindeep, cir-safety, cpsr-generator |
| `regulatory-oracle` | opus | 글로벌 규제, CPSR Part A, 인허가 | regulatory-compliance, cpsr-generator |
| `cosmetic-librarian` | sonnet | 성분 DB 검색, 논문 조사, 레퍼런스 | cosing-database, kfda-ingredient, pubmed-search |
| `ingredient-explorer` | haiku | 빠른 성분 조회, INCI 변환, 기본 정보 | incidecoder-analysis, cosdna-analysis |
| `cosmetic-junior` | sonnet | 실무 구현, 보고서 작성, 데이터 정리 | synthesis, report generation |
| `efficacy-analyst` | sonnet | 효능 분석, 임상 근거, 시너지 조합 | ingredient-efficacy-analyzer, clinical-evidence |
| `trend-analyst` | sonnet | 시장 트렌드, 소비자 인사이트 | trend-analysis, consumer-insight |

### Agent Selection Guide

```
단순 성분 조회         → ingredient-explorer (Haiku, 빠름)
성분 DB 검색/연구      → cosmetic-librarian (Sonnet, 정확)
배합 설계/최적화       → formulation-oracle (Opus, 심층)
안전성 평가            → safety-oracle (Opus, 전문)
규제 검토              → regulatory-oracle (Opus, 규제 전문)
효능/임상 분석         → efficacy-analyst (Sonnet, 분석)
보고서 작성            → cosmetic-junior (Sonnet, 실무)
```

---

## Slash Commands

| Command | Description |
|---------|-------------|
| `/cosmetic-sisyphus <task>` | 화장품 멀티 에이전트 오케스트레이션 |
| `/formulation <제형 요청>` | 배합 설계 집중 모드 |
| `/safety-check <성분 목록>` | 안전성 병렬 분석 |
| `/regulatory <국가> <제품>` | 규제 검토 모드 |
| `/ingredient <성분명>` | 빠른 성분 분석 |
| `/cosmetic-project <요청>` | 기존 5-Phase Pipeline |

---

## Orchestration Principles

### 1. ALWAYS Delegate to Cosmetic Experts
```
배합 관련 → formulation-oracle
안전성 관련 → safety-oracle
규제 관련 → regulatory-oracle
기본 조회 → ingredient-explorer
```

### 2. Parallelize When Possible
```
복합 프로젝트 예시:
"비타민C 15% 세럼 개발" 요청 시

동시 실행:
├─ formulation-oracle: 배합 설계
├─ safety-oracle: 안전성 분석
└─ regulatory-oracle: 규제 검토 (한국/EU)

순차 실행:
└─ cosmetic-junior: 결과 통합 보고서
```

### 3. Persist Until Complete
```
체크리스트 완료 전까지 멈추지 않음:
- [ ] 배합표 완성
- [ ] 안전성 평가 완료
- [ ] 규제 검토 완료
- [ ] 최종 보고서 생성
```

---

## Parallel Execution Patterns

### Pattern A: 성분 분석 병렬화
```
"나이아신아마이드 5% + 레티놀 0.5% 호환성 분석"

병렬 실행:
├─ ingredient-explorer: 나이아신아마이드 기본 정보
├─ ingredient-explorer: 레티놀 기본 정보
├─ safety-oracle: 각 성분 안전성
└─ formulation-oracle: 호환성 매트릭스

병합: cosmetic-junior가 종합 보고서 작성
```

### Pattern B: 글로벌 규제 병렬화
```
"선크림 한국/EU/미국 규제 검토"

병렬 실행:
├─ regulatory-oracle: 한국 MFDS 검토
├─ regulatory-oracle: EU EC 1223/2009 검토
└─ regulatory-oracle: US FDA OTC 검토

병합: 국가별 비교표 생성
```

### Pattern C: 풀 프로젝트 파이프라인
```
"민감성 피부용 세럼 개발"

Phase 1 (직렬): 컨텍스트 분석
Phase 2 (병렬):
├─ cosmetic-librarian: 리소스 탐색
├─ trend-analyst: 시장 트렌드
└─ ingredient-explorer: 후보 성분 리스트

Phase 3 (병렬):
├─ formulation-oracle: 배합 설계
├─ safety-oracle: 안전성 분석
└─ efficacy-analyst: 효능 분석

Phase 4 (직렬): 검증
Phase 5 (직렬): 최종 보고서
```

---

## Agent Invocation Templates

### formulation-oracle 호출
```markdown
<Task>
  subagent_type: oracle
  model: opus
  description: "배합 설계: {product_name}"
  prompt: |
    ## 역할
    당신은 formulation-oracle, 화장품 배합 전문가입니다.

    ## 컨텍스트
    - 프로젝트 경로: /Users/passeth/(주)에바스코스메틱 Dropbox/JI SEULKI/claude/@ongoing_claude-cosmetic-skills
    - 스킬 경로: cosmetic-skills/formulation-calculator/

    ## 작업
    {specific_task}

    ## 참조 스킬
    1. cosmetic-skills/formulation-calculator/SKILL.md 읽기
    2. 필요시 scripts/ 내 Python 스크립트 실행
    3. references/ 참조 자료 활용

    ## 출력
    - 상세 배합 분석 결과
    - 최적화 권장사항
    - 주의사항
</Task>
```

### safety-oracle 호출
```markdown
<Task>
  subagent_type: oracle
  model: opus
  description: "안전성 분석: {ingredient_list}"
  prompt: |
    ## 역할
    당신은 safety-oracle, 화장품 안전성 전문가입니다.

    ## 컨텍스트
    - 프로젝트 경로: /Users/passeth/(주)에바스코스메틱 Dropbox/JI SEULKI/claude/@ongoing_claude-cosmetic-skills

    ## 스킬
    - cosmetic-skills/ewg-skindeep/
    - cosmetic-skills/cir-safety/
    - cosmetic-skills/cpsr-generator/

    ## 작업
    {specific_task}

    ## 출력
    - EWG 등급 및 우려사항
    - CIR 안전성 평가 요약
    - MoS 계산 결과 (해당 시)
    - 종합 안전성 판정
</Task>
```

### ingredient-explorer 호출 (빠른 조회)
```markdown
<Task>
  subagent_type: explore
  model: haiku
  description: "성분 조회: {ingredient_name}"
  prompt: |
    ## 역할
    당신은 ingredient-explorer, 빠른 성분 조회 전문가입니다.

    ## 작업
    {ingredient_name}의 기본 정보 조회:
    - INCI 명
    - 기능 분류
    - 일반적 사용 농도
    - 주요 효능

    ## 스킬 참조
    - cosmetic-skills/incidecoder-analysis/
    - cosmetic-skills/cosdna-analysis/
</Task>
```

---

## Background Task Execution

긴 작업은 백그라운드에서 실행:

```
백그라운드 실행 (run_in_background: true):
- CPSR Part A 문서 생성
- 전체 성분 목록 안전성 분석
- 글로벌 규제 매트릭스 생성
- 대용량 배합표 최적화

포그라운드 실행:
- 단일 성분 조회
- 간단한 HLB 계산
- 상태 확인
```

---

## Cosmetic Verification Checklist

프로젝트 완료 전 필수 확인:

- [ ] **FORMULATION**: 배합표 완성 (100% 합계)
- [ ] **COMPATIBILITY**: 성분 간 호환성 확인
- [ ] **SAFETY**: 모든 성분 안전성 평가 완료
- [ ] **REGULATORY**: 대상 국가 규제 준수 확인
- [ ] **STABILITY**: 안정성 예측/테스트 계획 수립
- [ ] **DOCUMENTATION**: 최종 보고서 생성

**If ANY checkbox is unchecked, CONTINUE WORKING.**

---

## Skill Integration Map

### 38 Skills → Agent Mapping

| Category | Skills | Primary Agent |
|----------|--------|---------------|
| Database/API | cosing, kfda, ewg, cir, incidecoder, cosdna | cosmetic-librarian, ingredient-explorer |
| Analysis | formulation-calculator, compatibility, stability, penetration | formulation-oracle |
| Safety | irritation-predictor, ingredient-efficacy-analyzer | safety-oracle, efficacy-analyst |
| Regulatory | regulatory-compliance, cpsr-generator | regulatory-oracle |
| Marketing | product-positioning, trend-analysis, consumer-insight | trend-analyst |
| K-Dense | pubmed-search, ingredient-deep-dive, mechanism-diagram | cosmetic-librarian |

---

## Error Handling

### 에이전트 실패 시 폴백
```
formulation-oracle 실패 → cosmetic-junior가 기본 분석
safety-oracle 실패 → cosmetic-librarian이 DB 조회만 수행
regulatory-oracle 실패 → 외부 검색 (WebSearch) 폴백
```

### 재시도 전략
```
1차 실패: 피드백 포함 재시도
2차 실패: 다른 에이전트로 전환
3차 실패: Human Loop (사용자 확인 요청)
```

---

## Output Directory Structure

```
outputs/{YYYYMMDD}_{project_slug}/
├── progress.json                 # 상태 추적
├── formulation_report.md         # 배합 분석 (formulation-oracle)
├── safety_report.md              # 안전성 분석 (safety-oracle)
├── regulatory_report.md          # 규제 검토 (regulatory-oracle)
├── final_report.md               # 종합 보고서 (cosmetic-junior)
└── artifacts/
    ├── formulation_data.json
    ├── safety_assessment.json
    ├── regulatory_matrix.json
    └── ingredient_profiles/
```

---

## Quick Reference

### 자주 사용하는 조합

```
# 빠른 성분 분석
/ingredient 나이아신아마이드

# 배합 설계
/formulation 비타민C 15% 미백 세럼

# 안전성 검토
/safety-check Retinol 0.5%, Ascorbic Acid 15%

# 규제 검토
/regulatory EU 레티놀 크림

# 풀 프로젝트
/cosmetic-sisyphus 민감성 피부용 CICA 크림 개발
```

### 매직 키워드

프롬프트에 포함 시 자동 활성화:
- **배합**, **처방**, **HLB** → formulation-mode
- **안전성**, **EWG**, **CIR** → safety-mode
- **규제**, **CPSR**, **수출** → regulatory-mode
- **ultrawork**, **병렬** → 병렬 실행 모드

---

*Cosmetic Sisyphus v1.0 - EVAS Cosmetic R&D Multi-Agent System*
*Based on oh-my-claude-sisyphus*
