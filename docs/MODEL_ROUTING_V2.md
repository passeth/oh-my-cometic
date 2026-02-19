# MODEL ROUTING V2 — 멀티모델 라우팅 설계

**작성일**: 2026-02-19
**적용 대상**: cosmetic-sisyphus v2.0

---

## 1. 설계 원칙

1. **비용 최적화**: 작업 복잡도에 맞는 모델 사용
2. **품질 보장**: 핵심 분석은 최고 모델 유지
3. **단순한 구현**: .md 에이전트 파일의 model 필드로 관리
4. **확장 가능**: 추후 xAI/OpenAI API 추가 용이

---

## 2. 에이전트 × 모델 매트릭스

### 기본 매핑

| 에이전트 | 기본 모델 | ultrawork 모델 | 용도 |
|----------|----------|---------------|------|
| **sisyphus (메인)** | Sonnet 4.6 | Opus 4.6 | 오케스트레이션 |
| **formulation-oracle** | Sonnet 4.6 | Opus 4.6 | 배합 심층분석 |
| **safety-oracle** | Sonnet 4.6 | Opus 4.6 | 안전성 심층분석 |
| **regulatory-oracle** | Sonnet 4.6 | Opus 4.6 | 규제 심층분석 |
| **cosmetic-librarian** | Sonnet 4.6 | — | DB 조회 (Opus 불필요) |
| **ingredient-explorer** | Haiku 4.5 | — | 단순 검색 (저가) |
| **cosmetic-junior** | Sonnet 4.6 | Opus 4.6 | 실무 작업 |
| **document-writer** | Sonnet 4.6 | Opus 4.6 | 문서 생성 |
| **prometheus** | Opus 4.6 | — | 전략 계획 (항상 Opus) |
| **metis** | Opus 4.6 | — | 사전 계획 (항상 Opus) |

### 모델 티어 정의

| 티어 | 모델 | 토큰 비용 (input/output) | 용도 |
|------|------|------------------------|------|
| **Tier 1 (Premium)** | Opus 4.6 | $15/$75 per 1M | 심층분석, Tech DNA, 카피라이팅 |
| **Tier 2 (Standard)** | Sonnet 4.6 | $3/$15 per 1M | 일반 작업, 오케스트레이션 |
| **Tier 3 (Economy)** | Haiku 4.5 | $0.25/$1.25 per 1M | 단순 검색, 단위 변환, INCI 조회 |

---

## 3. 작업 복잡도 판단 기준

### Tier 1 (Opus) 트리거 조건
- `ultrawork` 키워드 감지
- Tech DNA Framework 생성
- 백서/학술 리포트 작성
- 성분 심층분석 (mechanism of action, 임상 근거)
- 마케팅 카피라이팅 (USP, 태그라인)
- CPSR 생성
- 복수 규제 비교 분석 (EU + 한국 + 중국)
- 경쟁사 종합 분석

### Tier 2 (Sonnet) 기본 작업
- 일반 배합 컨설팅
- 단일 규제 체크
- 리포트 초안
- 데이터 정리/요약
- 오케스트레이션/위임

### Tier 3 (Haiku) 단순 작업
- INCI명 변환
- 단위/농도 변환
- CosIng/ICID DB 조회
- EWG 등급 확인
- 파일 내 성분 검색
- 배치 계산

---

## 4. 구현 방법

### 방법 A: .md 에이전트 파일 model 필드 (권장)

각 에이전트 .md 파일에 model 필드 추가:

```markdown
---
model: claude-sonnet-4-6
ultrawork_model: claude-opus-4-6
---
# formulation-oracle

(기존 프롬프트)
```

### 방법 B: keyword-detector 연동

keyword-detector.sh에서 ultrawork 감지 시 환경변수 설정:

```bash
# keyword-detector.sh 수정
if echo "$USER_PROMPT" | grep -qi "ultrawork\|심층분석\|tech dna\|백서"; then
  export SISYPHUS_MODEL_TIER="premium"
fi
```

### 방법 C: hooks.json에 모델 오버라이드 추가

```json
{
  "UserPromptSubmit": [{
    "matcher": "*ultrawork*",
    "hooks": [{
      "type": "command",
      "command": "echo '{\"model\": \"claude-opus-4-6\"}'",
      "timeout": 2
    }]
  }]
}
```

### 권장: 방법 A + B 병행
- 기본 모델은 .md 파일에 명시
- ultrawork 트리거 시 keyword-detector가 모델 업그레이드

---

## 5. API 키 관리 방안

### 현재 (Anthropic Only)
```
ANTHROPIC_API_KEY=sk-ant-xxx
```

### 확장 시 (멀티 프로바이더)
```
# .env 또는 환경변수
ANTHROPIC_API_KEY=sk-ant-xxx       # Opus/Sonnet/Haiku
OPENAI_API_KEY=sk-xxx              # GPT-5.x (Hephaestus 등)
XAI_API_KEY=xai-xxx                # Grok (Explore 대안)
```

### 현실적 권장
- **단기**: Anthropic만 사용 (Opus + Sonnet + Haiku 3티어)
- **중기**: OpenAI 추가 (GPT-5 계열 Hephaestus용)
- **장기**: xAI/Google 추가 (비용 최적화)

---

## 6. 비용 시뮬레이션

### 시나리오: 제품 1개 풀 분석 (ORYZA 라인 5제품 기준)

#### 현재 (v1.0 — Opus Only)
| 작업 | 에이전트 호출 | 모델 | input 토큰 | output 토큰 | 비용 |
|------|-------------|------|-----------|------------|------|
| 오케스트레이션 | 10회 | Opus | 500K | 100K | $15.00 |
| 성분분석 × 5 | 25회 | Opus | 2M | 500K | $67.50 |
| 안전성 × 5 | 15회 | Opus | 1M | 300K | $37.50 |
| 규제 × 5 | 10회 | Opus | 500K | 150K | $18.75 |
| DB조회 | 20회 | Opus | 400K | 100K | $13.50 |
| 문서작성 | 5회 | Opus | 500K | 200K | $22.50 |
| **합계** | | | | | **$174.75** |

#### v2.0 (멀티모델 라우팅)
| 작업 | 에이전트 호출 | 모델 | input 토큰 | output 토큰 | 비용 |
|------|-------------|------|-----------|------------|------|
| 오케스트레이션 | 10회 | Sonnet | 500K | 100K | $3.00 |
| 성분분석 × 5 | 25회 | Sonnet→Opus | 2M | 500K | $13.50~$67.50 |
| 안전성 × 5 | 15회 | Sonnet | 1M | 300K | $7.50 |
| 규제 × 5 | 10회 | Sonnet | 500K | 150K | $3.75 |
| DB조회 | 20회 | Haiku | 400K | 100K | $0.23 |
| 문서작성(ultrawork) | 5회 | Opus | 500K | 200K | $22.50 |
| **합계 (기본)** | | | | | **$50.48** |
| **합계 (ultrawork 多)** | | | | | **$104.48** |

### 절감 효과
- **기본 사용**: 약 **71% 절감** ($174 → $50)
- **ultrawork 빈번**: 약 **40% 절감** ($174 → $104)
- **현실적 예상**: **50-60% 절감**

---

## 7. Haiku 적용 가능 스킬 목록

다음 스킬은 Haiku로 충분:
- inci-converter
- concentration-converter
- batch-calculator
- cosing-database (조회만)
- icid-database (조회만)
- ewg-skindeep (등급 확인)
- kfda-ingredient (규격 조회)
- get-available-resources
- ingredient-explorer (검색만)

---

## 8. 향후 확장: xAI/OpenAI 검토

| 프로바이더 | 모델 | 장점 | 단점 | 적용 가능 에이전트 |
|-----------|------|------|------|------------------|
| OpenAI | GPT-5.2/5.3 | 코드 생성 강점 | 화장품 도메인 약함 | Hephaestus (자율 작업) |
| xAI | Grok Code Fast | 빠른 검색 | 도메인 지식 부족 | Explore (grep) |
| Google | Gemini 3 Flash | 멀티모달 강점, 저가 | API 안정성 | Multimodal-Looker (PDF) |

**결론**: 단기적으로 Anthropic 3티어로 충분. 멀티모달(PDF 분석)이 필요해지면 Gemini 추가 검토.
