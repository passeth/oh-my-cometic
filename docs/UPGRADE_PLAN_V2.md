# UPGRADE PLAN V2 — Cosmetic Sisyphus v2.0

**작성일**: 2026-02-19
**목표**: oh-my-opencode v3.7.4 동기화 + 멀티모델 라우팅 적용
**예상 총 소요**: 7-10시간 (3 Phase)

---

## 1. 현재 vs 최신 구조 비교

| 항목 | cosmetic-sisyphus v1.0 | oh-my-opencode v3.7.4 | 갭 |
|------|----------------------|---------------------|-----|
| **에이전트** | 6개 화장품 특화 + 보조 19개 | 11개 범용 | 구조 다름 (md vs ts) |
| **스킬** | 44개 화장품 특화 | 6개 빌트인 | ✅ 시지푸스 우위 |
| **훅** | 6개 (스크립트) | 44개 (TS 모듈) | ⚠️ 대폭 부족 |
| **모델 라우팅** | 단일 모델 (Opus) | 에이전트별 모델 + 폴백 체인 | 개선 필요 |
| **백그라운드** | 없음 | background-agent (10k LOC) | 추가 검토 |
| **세션 복구** | session-start.sh (기본) | 다중 전략 복구 | 개선 필요 |
| **컨텍스트 관리** | 없음 | 압축 + 재주입 + 모니터링 | 추가 필요 |

---

## 2. 새 기능 목록

### 즉시 적용 가능 (Phase 1)
1. **멀티모델 라우팅** — Opus/Sonnet/Haiku 3티어 (→ MODEL_ROUTING_V2.md)
2. **컨텍스트 창 모니터** — 장시간 작업 시 한도 도달 방지
3. **압축 후 컨텍스트 재주입** — 압축으로 잃어버린 맥락 복원
4. **write-existing-file-guard** — 기존 파일 실수 덮어쓰기 방지
5. **hashline-read-enhancer** — 정밀 편집 지원
6. **keyword-detector 보강** — ultrawork 트리거 시 모델 업그레이드

### 중기 도입 (Phase 2)
7. **Atlas 에이전트** — TODO 오케스트레이터 (화장품 멀티제품 동시 분석)
8. **Multimodal-Looker** — PDF/이미지 분석 (CoA, 시험성적서)
9. **Momus 에이전트** — 리포트 교차 검증
10. **todo-continuation-enforcer 보강** — 현재 persistent-mode 대체

### 장기 검토 (Phase 3)
11. **Hephaestus 패턴 적용** — 자율 심층 작업 (Opus로 대체)
12. **Metis 패턴 적용** — 계획 수립 전 상담
13. **background-agent 패턴** — 병렬 제품 분석 (Claude Code 호환 여부 확인 필요)

---

## 3. 보존해야 할 화장품 특화 부분

### ✅ 절대 보존 (변경 금지)
- `.claude/agents/` 화장품 에이전트 6개 (formulation-oracle, safety-oracle, regulatory-oracle, cosmetic-librarian, ingredient-explorer, cosmetic-junior)
- `.claude/skills/` 44개 전부
- 브랜드 산출물 폴더 (BAERE, CERACLINIC_*, FRAIJOUR, ORYZA)
- `.claude/commands/` 화장품 커맨드 (cosmetic-analyze, safety-check 등)
- `CLAUDE.md` 화장품 오케스트레이션 규칙

### ⚠️ 수정하되 보존
- `.claude/hooks/hooks.json` — 새 훅 추가하되 기존 유지
- `.claude/hooks/keyword-detector.sh` — ultrawork 모델 스왑 로직 추가
- `.claude/hooks/persistent-mode.sh` — todo-continuation-enforcer 패턴 반영

---

## 4. Phase별 실행 계획

### Phase 1: 멀티모델 라우팅 + 훅 보강 (2-3시간)

**Step 1.1: 에이전트 .md에 model 필드 추가** (30분)
```
각 .claude/agents/*.md 파일 수정:
- formulation-oracle.md → model: claude-sonnet-4-6
- safety-oracle.md → model: claude-sonnet-4-6
- regulatory-oracle.md → model: claude-sonnet-4-6
- cosmetic-librarian.md → model: claude-sonnet-4-6
- ingredient-explorer.md → model: claude-haiku-4-5
- cosmetic-junior.md → model: claude-sonnet-4-6
- prometheus.md → model: claude-opus-4-6
```

**Step 1.2: keyword-detector 보강** (30분)
```
keyword-detector.sh 수정:
- ultrawork 감지 시 모델 → Opus 스왑 로직 추가
- "심층분석", "tech dna", "백서" 등 한국어 키워드 추가
```

**Step 1.3: 안전 훅 추가** (1시간)
```
새 스크립트 작성:
- write-guard.sh — 기존 파일 Write 전 Read 확인
- context-monitor.sh — 컨텍스트 사용량 추적
hooks.json에 등록
```

**Step 1.4: CLAUDE.md 모델 라우팅 규칙 추가** (30분)
```
CLAUDE.md에 모델 선택 가이드라인 추가:
- 기본: Sonnet
- ultrawork/심층: Opus
- 단순 조회: Haiku
```

### Phase 2: 새 에이전트 도입 (3-4시간)

**Step 2.1: Atlas 에이전트 생성** (1.5시간)
```
.claude/agents/atlas.md 작성:
- TODO 리스트 오케스트레이터
- 4-phase QA 검증 로직 (oh-my-opencode 참고)
- 화장품 멀티제품 동시 분석 시나리오 최적화
```

**Step 2.2: Multimodal-Looker 에이전트 생성** (1시간)
```
.claude/agents/multimodal-looker.md 작성:
- PDF/이미지 분석 전용
- CoA, 시험성적서, 인증서 분석 프롬프트
- 도구 제한: read만 허용
```

**Step 2.3: Momus (리뷰어) 에이전트 생성** (1시간)
```
.claude/agents/review-oracle.md 작성:
- 리포트 교차 검증
- 안전성↔배합 일관성 체크
- 규제 누락 검출
```

**Step 2.4: CLAUDE.md 업데이트** (30분)
```
새 에이전트 위임 규칙 추가
```

### Phase 3: 통합 테스트 + 안정화 (2-3시간)

**Step 3.1: 스킬 호환성 테스트** (1시간)
```
모델별 스킬 동작 확인:
- Haiku로 inci-converter, batch-calculator 테스트
- Sonnet으로 formulation-oracle 기본 질문 테스트
- Opus로 ultrawork Tech DNA 테스트
```

**Step 3.2: 멀티제품 시나리오 테스트** (1시간)
```
ORYZA 라인 제품 1개로 전체 파이프라인 테스트:
1. 배합 분석 → 안전성 → 규제 → 리포트
2. 모델 라우팅 확인 (Sonnet 기본, ultrawork 시 Opus)
```

**Step 3.3: 문서 정리 + CHANGELOG** (30분)
```
CHANGELOG.md 업데이트
docs/ 정리
```

---

## 5. 모델 라우팅 설계 요약

→ 상세: `MODEL_ROUTING_V2.md`

| 에이전트 | 기본 | ultrawork | 예상 절감 |
|----------|------|-----------|---------|
| sisyphus | Sonnet | Opus | 80% |
| oracle 계열 | Sonnet | Opus | 60% |
| librarian | Sonnet | — | 80% |
| explorer | Haiku | — | 98% |
| junior | Sonnet | Opus | 60% |
| prometheus | Opus | — | 0% |

---

## 6. 예상 비용 절감 효과

| 시나리오 | v1.0 (Opus Only) | v2.0 (3티어) | 절감률 |
|----------|-----------------|-------------|--------|
| 단일 제품 분석 | ~$35 | ~$10-20 | 43-71% |
| 5제품 라인 분석 | ~$175 | ~$50-105 | 40-71% |
| 월간 예상 (주 2회) | ~$1,400 | ~$400-840 | 40-71% |

---

## 7. 리스크 및 대응

| 리스크 | 영향 | 대응 |
|--------|------|------|
| Sonnet으로 품질 저하 | 분석 깊이 감소 | ultrawork 트리거 조건 넓히기 |
| Haiku 정확도 부족 | DB 조회 오류 | 단순 조회만 Haiku, 분석은 Sonnet |
| Claude Code model 필드 미지원 | 라우팅 불가 | CLAUDE.md 가이드라인 방식으로 전환 |
| 기존 스킬 호환성 | 스킬 동작 안 됨 | Phase 3에서 개별 테스트 |

---

## 8. 실행 체크리스트

```
Phase 1 (즉시)
□ 에이전트 .md에 model 필드 추가
□ keyword-detector.sh에 모델 스왑 로직 추가
□ write-guard.sh 작성 + hooks.json 등록
□ CLAUDE.md 모델 라우팅 규칙 추가
□ 단일 테스트 (formulation-oracle Sonnet 동작 확인)

Phase 2 (1주 내)
□ atlas.md 에이전트 작성
□ multimodal-looker.md 에이전트 작성
□ review-oracle.md 에이전트 작성
□ CLAUDE.md 위임 규칙 업데이트

Phase 3 (2주 내)
□ Haiku 스킬 테스트 (5개)
□ Sonnet 에이전트 테스트 (6개)
□ Opus ultrawork 테스트
□ 멀티제품 통합 테스트
□ CHANGELOG.md 업데이트
□ 완료!
```
