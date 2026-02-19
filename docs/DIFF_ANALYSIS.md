# DIFF ANALYSIS — oh-my-opencode v3.7.4 vs cosmetic-sisyphus v1.0

**작성일**: 2026-02-19
**oh-my-opencode 버전**: v3.7.4 (커밋 31dc6e20)
**cosmetic-sisyphus 기준**: 2026-01 포크

---

## 1. 구조 비교 요약

| 영역 | oh-my-opencode v3.7 | cosmetic-sisyphus v1.0 | 상태 |
|------|---------------------|----------------------|------|
| 에이전트 | 11개 (TS 코드) | 25개 (.md 에이전트 파일) | 구조 다름 |
| 훅 | 44개 (TS 코드) | 6개 (스크립트 + hooks.json) | 대폭 부족 |
| 피처 | 19개 모듈 | 없음 (Claude Code 네이티브) | 해당 없음 |
| 스킬 | 6개 빌트인 | 44개 (화장품 특화) | ✅ 시지푸스 우위 |
| 도구 | 14개 커스텀 | Claude Code 기본 | 부분 부족 |

---

## 2. 새 에이전트 (v3.7에 추가)

### Hephaestus — 자율 심층 작업자
- **모델**: gpt-5.3-codex (폴백 없음 — 필수)
- **역할**: 독립적 깊은 작업 수행. Sisyphus가 위임하면 자율적으로 완료
- **특징**: 병렬 도구 호출 강화, subagent_type 제한 제거
- **화장품 적용**: Tech DNA, 백서 작성 등 장시간 심층 작업에 적합
- **시지푸스 대안**: Opus 모델로 대체 가능 (gpt-5.3-codex 미사용 시)

### Atlas — TODO 리스트 오케스트레이터
- **모델**: claude-sonnet-4-6 (폴백: kimi-k2.5 → gpt-5.2 → gemini-3-pro)
- **역할**: Boulder/백그라운드 세션의 마스터 오케스트레이터
- **동작 방식**: 4-phase critical QA + 의무적 실행 검증
  1. Session type 판별 → 2. Abort check → 3. Failure count → 4. Background tasks → Agent match → Plan completeness → Cooldown(5s)
- **GPT/Claude 이중 프롬프트**: 모델별 최적화된 프롬프트 분기
- **화장품 적용**: 멀티 제품 라인 동시 분석 시 유용

### Metis — 사전 계획 컨설턴트
- **모델**: claude-opus-4-6 (온도 0.3 — 유일하게 높음)
- **역할**: 계획 수립 전 상담 역할. 계획의 타당성 검토
- **화장품 적용**: 복잡한 제품 개발 로드맵 수립 시 활용

### Momus — 계획 리뷰어
- **모델**: gpt-5.2 (폴백: claude-opus-4-6 → gemini-3-pro)
- **역할**: 계획을 비판적으로 검토
- **도구 제한**: write, edit, task 불가 (읽기 전용)
- **화장품 적용**: Safety/Regulatory 리포트 교차 검증에 활용

### Multimodal-Looker — 시각 분석
- **모델**: gemini-3-flash (6단계 폴백 체인)
- **역할**: PDF/이미지 분석 전용
- **도구 제한**: read만 허용
- **화장품 적용**: CoA, 시험성적서 PDF 분석에 매우 유용

---

## 3. 새 훅 (v3.7 주요 추가)

### ultrawork-model-override (제거됨 — v3.7.4에서 dead code 정리)
- ⚠️ 원래 에이전트별 모델 스왑 기능이었으나 **v3.7.4에서 제거**
- 커밋: `575fc383` "remove dead ultrawork model override code"
- **대안**: 에이전트 정의 시 직접 모델 지정 방식으로 전환

### atlas hook (17 파일, ~1976 LOC)
- Boulder/백그라운드 세션의 중앙 제어
- 결정 게이트: session type → abort → failure count → background → agent match → plan → cooldown
- 지수 백오프: 30초 기본, ×2 배수, 최대 5회 연속 실패 시 5분 대기

### todo-continuation-enforcer (13 파일, ~2061 LOC)
- "Boulder" 메커니즘: TODO 미완료 시 계속 실행 강제
- 2초 카운트다운 토스트 → 연속 주입
- **시지푸스의 persistent-mode.sh와 동일 목적**, 훨씬 정교

### ralph-loop (14 파일, ~1687 LOC)
- `/ralph-loop` 자기 참조 개발 루프
- `.sisyphus/ralph-loop.local.md`에 상태 저장
- `<promise>DONE</promise>` 감지로 종료
- 최대 100회 반복
- **시지푸스에 이미 ralph-loop 커맨드 존재** — 동기화 필요

### keyword-detector (~1665 LOC)
- ultrawork, search, analyze, prove-yourself 모드 감지
- 모드별 시스템 프롬프트 주입
- **시지푸스의 keyword-detector.sh 대응** — 기능 동일, 구현 다름

### anthropic-context-window-limit-recovery (31 파일, ~2232 LOC)
- 컨텍스트 한도 도달 시 다중 전략 복구
- 전략: 잘라내기, 압축, 요약
- **시지푸스에 없음 — 추가 권장**

### hashline-read-enhancer
- Read 출력에 라인 해시 추가 (v3.7.4에서 기본 활성화)
- 정밀 편집 지원

### session-recovery
- 크래시 세션 자동 복구
- **시지푸스의 session-start.sh 대응** — 더 정교

### compaction-context-injector / compaction-todo-preserver
- 압축 후 컨텍스트/TODO 재주입
- **시지푸스에 없음 — 장시간 작업 안정성에 중요**

### background-notification
- 백그라운드 작업 완료 알림

### write-existing-file-guard
- 기존 파일 쓰기 전 Read 필수
- 실수로 파일 덮어쓰기 방지

---

## 4. 새 피처 모듈 (v3.7)

| 피처 | LOC | 시지푸스 대응 | 적용 필요성 |
|------|-----|-------------|------------|
| background-agent | ~10k | 없음 | ⭐ 높음 (병렬 제품 분석) |
| tmux-subagent | ~3.6k | 없음 | 중간 (CLI 환경에서만) |
| opencode-skill-loader | ~3.2k | .claude/skills/ | 부분 (YAML 프론트매터 호환) |
| mcp-oauth | ~1k | 없음 | 낮음 |
| boulder-state | ~400 | .sisyphus/ | 유사 구현 있음 |
| claude-tasks | ~500 | TodoWrite | 대체 가능 |
| run-continuation-state | ~500 | persistent-mode | 부분 |

---

## 5. 시지푸스 화장품 특화 부분 (보존 대상)

### 에이전트 (6개 핵심 + 부속)
1. **formulation-oracle** — 배합/처방 전문 (HLB, 유화, pH)
2. **safety-oracle** — 안전성 전문 (EWG, CIR, MoS)
3. **regulatory-oracle** — 규제 전문 (CPSR, CosIng, MFDS, NMPA)
4. **cosmetic-librarian** — DB 조회 전문
5. **ingredient-explorer** — 성분 빠른 검색
6. **cosmetic-junior** — 실무 작업

### 스킬 (44개)
화장품 특화 스킬 전량 보존:
- DB 연동: cosing-database, icid-database, ewg-skindeep, cosdna-analysis, incidecoder-analysis, cosmily-integration, ulprospector-integration, kfda-ingredient, mintel-gnpd
- 분석: ingredient-deep-dive, ingredient-compatibility, ingredient-efficacy-analyzer, skin-penetration, stability-predictor, irritation-predictor, clinical-evidence-aggregator
- 규제: regulatory-checker, regulatory-compliance, cpsr-generator, cir-safety, ifra-standards, claim-substantiation
- 배합: formulation-calculator, formulation-strategy, batch-calculator, concentration-converter, inci-converter, rdkit-cosmetic
- 문서: cosmetic-clinical-reports, reference-manager, mechanism-diagram-generator
- 마케팅: consumer-insight, product-positioning, trend-analysis
- 오케스트레이션: cosmetic-orchestrator, cosmetic-context-initialization, deepinit, get-available-resources
- 기타: pubmed-search, ultrawork, session-review, release, git-master, frontend-ui-ux

### 커맨드 (15개)
analyze, cancel-ralph, cosmetic-analyze, deepinit, deepsearch, doctor, plan, prometheus, ralph-loop, review, safety-check, sisyphus, sisyphus-default, sisyphus-default-global, ultrawork

### 산출물 폴더
BAERE/, CERACLINIC_MATCHA/, CERACLINIC_PEPTIDE/, CERACLINIC_TXA/, FRAIJOUR/, ORYZA/ — 모두 보존

---

## 6. 충돌 가능 지점

| 영역 | 충돌 유형 | 난이도 | 해결 방안 |
|------|---------|--------|---------|
| 에이전트 구조 | TS 코드 vs .md 파일 | 높음 | .md 방식 유지 (Claude Code 호환) |
| 훅 시스템 | TS 훅 vs hooks.json + 스크립트 | 높음 | hooks.json 확장 방식 유지 |
| keyword-detector | 양쪽 다 존재 | 중간 | 시지푸스 버전에 v3.7 키워드 추가 |
| persistent-mode | 시지푸스 vs todo-continuation-enforcer | 중간 | 병합 (시지푸스 방식 기반) |
| ralph-loop | 양쪽 다 존재 | 낮음 | 시지푸스 버전 보강 |
| 모델 라우팅 | 직접 지정 vs AGENT_MODEL_REQUIREMENTS | 중간 | .md 에이전트의 model 필드 활용 |

---

## 7. 마이그레이션 난이도 평가

| Phase | 내용 | 난이도 | 예상 시간 |
|-------|------|--------|---------|
| Phase 1 | 멀티모델 라우팅 + 훅 보강 | ⭐⭐ 중간 | 2-3시간 |
| Phase 2 | Atlas/Multimodal-Looker 도입 | ⭐⭐⭐ 높음 | 3-4시간 |
| Phase 3 | 스킬 재점검 + 통합 테스트 | ⭐⭐ 중간 | 2-3시간 |
| **전체** | | | **7-10시간** |

### 핵심 제약
- oh-my-opencode는 **Sustainable Use License** (상업적 사용 제한 있음)
- 시지푸스는 Claude Code (.md 에이전트) 기반 → TS 코드 직접 이식 불가
- 패턴과 로직만 참고하여 .md/.json 기반으로 재구현 필요

---

## 8. 라이선스 확인

**oh-my-opencode License**: Sustainable Use License v1.0
- 비상업적 사용: 허용
- 상업적 사용: 제한적 (경쟁 제품 금지)
- 시지푸스 용도 (사내 R&D 도구): ✅ 허용 (경쟁 제품이 아님)
- 코드 직접 복사: 라이선스 조건 확인 필요 → **패턴 참고 + 자체 구현 권장**
