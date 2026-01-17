<div align="center">

# Oh-My-Cosmetic

### 화장품 R&D 멀티에이전트 시스템

[![Version](https://img.shields.io/badge/version-1.0.0-ff6b6b)](https://github.com/passeth/oh-my-cometic/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Plugin-d97706?logo=anthropic&logoColor=white)](https://docs.anthropic.com/claude-code)

**Claude Code를 위한 화장품 R&D 전문 멀티에이전트 오케스트레이션 시스템**

*배합 분석부터 안전성 평가, 규제 검토까지 - AI가 화장품 개발을 도와드립니다*

[설치](#설치) • [사용법](#사용법) • [에이전트](#화장품-전문-에이전트) • [키워드](#자동-활성화-키워드)

</div>

---

## 이런 분들을 위한 도구입니다

- **화장품 R&D 연구원**: 배합 설계, 성분 분석, 안정성 예측
- **품질/안전성 담당자**: 안전성 평가, MoS 계산, 자극성 분석
- **RA(Regulatory Affairs)**: 글로벌 규제 검토, 수출 인허가
- **마케팅/기획**: 성분 트렌드 조사, 경쟁사 분석

---

## 주요 기능

### 1. 배합/처방 분석 (Formulation Oracle)

```
"이 에멀전 배합의 HLB 값 계산해줘"
"나이아신아마이드와 비타민C를 함께 쓸 수 있어?"
"pH 5.5에서 안정한 레티놀 처방 설계해줘"
```

- HLB (Hydrophilic-Lipophilic Balance) 계산
- 성분 호환성 분석
- 유화 시스템 설계
- pH 최적화 권장
- 점도/안정성 예측

### 2. 안전성 평가 (Safety Oracle)

```
"이 배합의 EWG 스코어 확인해줘"
"레티놀 0.5% 사용 시 MoS 계산해줘"
"민감성 피부용으로 자극성 예측해줘"
```

- EWG Skin Deep 등급 조회
- CIR (Cosmetic Ingredient Review) 평가
- MoS (Margin of Safety) 계산
- 자극성/감작성 예측
- NOAEL/SED 기반 분석

### 3. 규제 분석 (Regulatory Oracle)

```
"이 제품 EU 수출 가능해?"
"중국 NMPA 등록 시 필요한 서류 알려줘"
"한국 기능성 화장품 심사 기준 확인해줘"
```

- EU CosIng / Annex 규제
- 한국 식약처 (K-FDA) 기준
- 미국 FDA 규정
- 중국 NMPA 요구사항
- 일본 후생노동성 기준
- CPSR (Cosmetic Product Safety Report) 가이드

### 4. 성분 연구 (Cosmetic Librarian)

```
"나이아신아마이드 최신 효능 연구 찾아줘"
"트렌디한 항산화 성분 추천해줘"
"이 성분의 CAS 번호랑 INCI명 확인해줘"
```

- CosIng / ICID 데이터베이스 검색
- 학술 논문 및 특허 검색
- 시장 트렌드 분석
- 공급사 정보 조회

### 5. 빠른 조회 (Ingredient Explorer)

```
"우리 배합표에서 방부제 찾아줘"
"JSON 파일에서 계면활성제 농도 확인해줘"
```

- 로컬 파일 내 성분 빠른 검색
- 배합표/JSON 데이터 조회
- 패턴 매칭 검색

### 6. 실무 구현 (Cosmetic Junior)

```
"배합표 양식으로 정리해줘"
"안전성 보고서 초안 작성해줘"
"이 데이터를 JSON으로 변환해줘"
```

- 배합표/처방전 작성
- 안전성 보고서 초안 생성
- JSON/CSV 데이터 파일 생성
- 스케일업 계산

---

## 설치

```bash
git clone https://github.com/passeth/oh-my-cometic.git
cd oh-my-cometic
./scripts/install.sh
```

설치 완료 후 Claude Code를 재시작하면 바로 사용할 수 있습니다.

### 설치 확인

```bash
# Claude Code 시작
claude

# 설치 확인 (화장품 에이전트 목록)
/cosmetic-analyze --help
```

---

## 사용법

### 슬래시 명령어

| 명령어 | 설명 | 예시 |
|-------|-----|-----|
| `/formulation <query>` | 배합/처방 분석 | `/formulation HLB 계산` |
| `/safety-check <ingredient>` | 안전성 평가 | `/safety-check Retinol 0.5%` |
| `/regulatory <market>` | 규제 분석 | `/regulatory EU 수출` |
| `/ingredient <name>` | 성분 정보 조회 | `/ingredient Niacinamide` |
| `/cosmetic <task>` | 화장품 모드 활성화 | `/cosmetic 에센스 배합 설계` |

### 실제 사용 예시

#### 배합 설계

```
> /formulation 미백 에센스 배합 설계해줘. 나이아신아마이드 5%, 알부틴 2% 포함

📋 Formulation Oracle이 분석을 시작합니다...

## 배합 분석

### 성분 호환성
- Niacinamide 5% + Arbutin 2%: ✅ 호환 (pH 5.0-6.5)
- 권장 pH: 5.5-6.0

### 제안 배합표
| Phase | Ingredient | % | Function |
|-------|-----------|---|----------|
| A | Water | q.s. | Solvent |
| A | Niacinamide | 5.0 | Brightening |
| A | Arbutin | 2.0 | Brightening |
...
```

#### 안전성 평가

```
> /safety-check 이 배합의 안전성 평가해줘

🔬 Safety Oracle이 평가를 시작합니다...

## 안전성 평가 결과

### EWG 등급
| 성분 | 농도 | EWG | 우려사항 |
|-----|-----|-----|---------|
| Niacinamide | 5% | 1 | Low |
| Arbutin | 2% | 1 | Low |

### MoS 계산
- Niacinamide: MoS = 342 (>100 ✅ Safe)
- Arbutin: MoS = 156 (>100 ✅ Safe)
```

#### 규제 검토

```
> /regulatory EU 수출 가능 여부 확인해줘

📜 Regulatory Oracle이 검토를 시작합니다...

## EU 규제 검토

### Annex 상태
| 성분 | Annex | 제한 | 상태 |
|-----|-------|-----|-----|
| Niacinamide | - | 없음 | ✅ 허용 |
| Arbutin | - | 없음 | ✅ 허용 |

### CPSR 요구사항
- 안전성 평가 필요
- Challenge Test 권장
- PIF (Product Information File) 필수
```

---

## 자동 활성화 키워드

프롬프트에 아래 키워드가 포함되면 자동으로 관련 에이전트가 활성화됩니다:

### 배합 관련
| 키워드 | 활성화 에이전트 |
|-------|---------------|
| `HLB`, `유화`, `emulsion` | formulation-oracle |
| `배합`, `처방`, `formulation` | formulation-oracle |
| `pH`, `점도`, `안정성` | formulation-oracle |
| `성분`, `ingredient`, `INCI` | cosmetic-librarian |

### 안전성 관련
| 키워드 | 활성화 에이전트 |
|-------|---------------|
| `EWG`, `CIR`, `MoS` | safety-oracle |
| `자극성`, `irritation` | safety-oracle |
| `독성`, `toxicity`, `NOAEL` | safety-oracle |

### 규제 관련
| 키워드 | 활성화 에이전트 |
|-------|---------------|
| `규제`, `regulatory` | regulatory-oracle |
| `CPSR`, `CosIng`, `Annex` | regulatory-oracle |
| `NMPA`, `FDA`, `식약처` | regulatory-oracle |

---

## 화장품 전문 에이전트

| 에이전트 | 모델 | 역할 | 비용 |
|---------|-----|-----|-----|
| **formulation-oracle** | Opus | 배합/처방 전문가 - HLB, pH, 유화, 호환성 | 고 |
| **safety-oracle** | Opus | 안전성 전문가 - EWG, CIR, MoS, 독성 | 고 |
| **regulatory-oracle** | Opus | 규제 전문가 - EU/한국/미국/중국/일본 | 고 |
| **cosmetic-librarian** | Sonnet | 연구 전문가 - DB 검색, 문헌 조사 | 중 |
| **ingredient-explorer** | Haiku | 빠른 조회 - 로컬 파일 검색 | 저 |
| **cosmetic-junior** | Sonnet | 실무 구현 - 문서 작성, 데이터 변환 | 중 |

### 스마트 모델 라우팅

작업 복잡도에 따라 자동으로 적절한 모델이 선택됩니다:

| 작업 유형 | 모델 | 이유 |
|----------|-----|-----|
| "나이아신아마이드 INCI명 확인" | **Haiku** | 단순 조회 - 빠르고 저렴 |
| "EWG 등급 검색" | **Sonnet** | 외부 검색 - 균형잡힌 성능 |
| "복합 배합 안정성 분석" | **Opus** | 복잡한 분석 - 고급 추론 필요 |

---

## 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                    COSMETIC ORCHESTRATOR                         │
│              (화장품 R&D 작업 통합 관리)                          │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│    ANALYSIS     │  │    RESEARCH     │  │  IMPLEMENTATION │
│   (분석/평가)    │  │   (연구/조사)    │  │   (실무/구현)    │
├─────────────────┤  ├─────────────────┤  ├─────────────────┤
│ 🧪 Formulation  │  │ 📚 Cosmetic     │  │ 📝 Cosmetic     │
│    Oracle       │  │    Librarian    │  │    Junior       │
│ 🔬 Safety       │  │ 🔍 Ingredient   │  │                 │
│    Oracle       │  │    Explorer     │  │                 │
│ 📜 Regulatory   │  │                 │  │                 │
│    Oracle       │  │                 │  │                 │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

### 작업 흐름

1. **사용자 요청** → 키워드/명령어 감지
2. **에이전트 선택** → 적절한 전문 에이전트 활성화
3. **분석 수행** → Oracle 에이전트가 전문 분석
4. **데이터 수집** → Librarian/Explorer가 정보 수집
5. **결과 생성** → Junior가 문서/데이터 생성
6. **검증** → 품질 체크리스트 확인

---

## 범용 스킬 (Enhancement Skills)

기본 동작에 추가로 활성화할 수 있는 강화 스킬입니다.

### 스킬 목록

| 스킬 | 명령어 | 설명 |
|-----|-------|-----|
| **ultrawork** | `/ultrawork <task>` | 최대 성능 모드 - 병렬 실행, 백그라운드 처리 |
| **git-master** | 자동 감지 | Git 전문가 - 원자적 커밋, 스타일 감지, 히스토리 관리 |
| **frontend-ui-ux** | 자동 감지 | UI/UX 전문가 - 대담한 디자인, 접근성 |
| **deepinit** | `/deepinit [path]` | 코드베이스 문서화 - AGENTS.md 계층 생성 |
| **release** | `/release <version>` | 릴리스 자동화 - 버전 범프, 태그, npm 배포 |

### ultrawork - 최대 성능 모드

복잡한 작업을 빠르게 처리해야 할 때 사용합니다.

```
/ultrawork 전체 에센스 라인업 배합 분석 및 안전성 평가 진행해줘
```

**특징:**
- 병렬 에이전트 실행으로 속도 향상
- 백그라운드 작업 (빌드, 테스트)
- 스마트 모델 라우팅 (비용 최적화)

**모델 라우팅:**
| 작업 복잡도 | 모델 | 예시 |
|-----------|-----|-----|
| 단순 조회 | Haiku | "INCI명 확인" |
| 일반 작업 | Sonnet | "성분 검색", "문서 작성" |
| 복잡 분석 | Opus | "배합 안정성 분석", "규제 종합 검토" |

### git-master - Git 전문가

여러 파일을 변경할 때 자동으로 활성화됩니다.

**핵심 규칙:**
- 3+ 파일 변경 → 2+ 커밋
- 5+ 파일 변경 → 3+ 커밋
- 10+ 파일 변경 → 5+ 커밋

**자동 감지 항목:**
- 커밋 메시지 언어 (한국어/영어)
- 커밋 스타일 (Semantic/Plain)
- 디렉토리별 분리

**유용한 명령어:**
```bash
# 특정 코드 추가 시점 찾기
git log -S "Niacinamide" --oneline

# 파일 히스토리 탐색
git blame -L 10,20 formulation.json
```

### frontend-ui-ux - UI/UX 디자인

프론트엔드/UI 작업 시 자동으로 활성화됩니다.

**디자인 원칙:**
- 대담한 미학 방향 설정
- 구별되는 타이포그래피
- 일관된 컬러 팔레트
- 의미 있는 모션/애니메이션

**지양 패턴:**
- 일반적인 폰트 (Arial, Inter, Roboto)
- 뻔한 색상 조합
- 예측 가능한 레이아웃

### deepinit - 코드베이스 문서화

AI 에이전트가 코드베이스를 이해할 수 있도록 계층적 문서를 생성합니다.

```
/deepinit              # 현재 디렉토리 인덱싱
/deepinit ./src        # 특정 경로 인덱싱
/deepinit --update     # 기존 AGENTS.md 업데이트
```

**생성 구조:**
```
/AGENTS.md                    ← 루트 문서
├── src/AGENTS.md             ← 소스 코드 문서
│   ├── components/AGENTS.md  ← 컴포넌트 문서
│   └── utils/AGENTS.md       ← 유틸리티 문서
└── tests/AGENTS.md           ← 테스트 문서
```

### release - 릴리스 자동화

```
/release 1.1.0         # 특정 버전
/release patch         # 패치 버전 증가
/release minor         # 마이너 버전 증가
```

**자동 수행 작업:**
1. 모든 파일의 버전 업데이트
2. 테스트 실행
3. 커밋 및 태그 생성
4. npm 배포
5. GitHub 릴리스 생성

---

## 범용 에이전트

화장품 에이전트 외에 기본 제공되는 범용 에이전트입니다.

| 에이전트 | 모델 | 용도 |
|---------|-----|-----|
| **oracle** | Opus | 아키텍처 분석, 디버깅 |
| **librarian** | Sonnet | 문서 검색, 코드 이해 |
| **explore** | Haiku | 빠른 파일/패턴 검색 |
| **sisyphus-junior** | Sonnet | 집중 작업 실행 |
| **document-writer** | Haiku | README, API 문서 작성 |
| **frontend-engineer** | Sonnet | 컴포넌트 설계, 스타일링 |
| **prometheus** | Opus | 전략적 계획 수립 |
| **momus** | Opus | 계획 비평 검토 |
| **metis** | Opus | 사전 계획 분석 |
| **qa-tester** | Sonnet | CLI/서비스 테스트 |
| **multimodal-looker** | Sonnet | 스크린샷/다이어그램 분석 |

### 에이전트 사용 예시

```
# 복잡한 문제 분석
Task(subagent_type="oracle", prompt="이 배합 안정성 이슈의 근본 원인 분석")

# 빠른 파일 검색
Task(subagent_type="explore", prompt="모든 배합 JSON 파일 찾기")

# 문서 작성
Task(subagent_type="document-writer", prompt="API 엔드포인트 문서 작성")

# 계획 수립
Task(subagent_type="prometheus", prompt="신제품 개발 워크플로우 계획")
```

---

## 슬래시 명령어 전체 목록

### 화장품 명령어

| 명령어 | 설명 |
|-------|-----|
| `/formulation <query>` | 배합/처방 분석 |
| `/safety-check <ingredient>` | 안전성 평가 |
| `/regulatory <market>` | 규제 분석 |
| `/ingredient <name>` | 성분 정보 조회 |
| `/cosmetic <task>` | 화장품 모드 활성화 |

### 시스템 명령어

| 명령어 | 설명 |
|-------|-----|
| `/ultrawork <task>` | 최대 성능 모드 |
| `/deepsearch <query>` | 심층 코드베이스 검색 |
| `/deepinit [path]` | AGENTS.md 생성 |
| `/analyze <target>` | 심층 분석 |
| `/plan <description>` | 계획 세션 시작 |
| `/review [plan-path]` | 계획 검토 |
| `/prometheus <task>` | 전략적 계획 |
| `/ralph-loop <task>` | 완료까지 자기참조 루프 |
| `/cancel-ralph` | Ralph Loop 취소 |
| `/release <version>` | 릴리스 자동화 |

---

## 기반 기술

이 프로젝트는 [oh-my-claude-sisyphus](https://github.com/Yeachan-Heo/oh-my-claude-sisyphus)를 기반으로 화장품 R&D에 특화된 에이전트를 추가한 fork입니다.

### 포함된 기본 기능
- 19개 범용 에이전트 (oracle, librarian, explore 등)
- 18개 라이프사이클 훅
- 5개 빌트인 스킬 (ultrawork, git-master, frontend-ui-ux, deepinit, release)
- 매직 키워드 자동 감지
- 스마트 모델 라우팅

### 추가된 화장품 기능
- 6개 화장품 전문 에이전트
- **38개 화장품 전문 스킬**
- 화장품 키워드 자동 감지
- 화장품 슬래시 명령어
- 배합/안전성/규제 특화 프롬프트

---

## 화장품 전문 스킬 (38개)

### 1. K-Dense 핵심 스킬 (5개)

K-Dense 수준의 기술 보고서 생성을 위한 핵심 스킬

| 스킬 | 명령어 | 설명 |
|-----|-------|-----|
| **pubmed-search** | `/pubmed-search <query>` | PubMed 학술 검색 및 논문 정보 추출 |
| **ingredient-deep-dive** | `/ingredient-deep-dive <ingredient>` | 성분 심층 분석 보고서 생성 |
| **mechanism-diagram-generator** | `/mechanism-diagram <ingredient>` | 작용 기전 Mermaid 다이어그램 생성 |
| **clinical-evidence-aggregator** | `/clinical-evidence <topic>` | 임상 근거 수집 및 등급화 |
| **reference-manager** | `/reference-manager` | 학술 참고문헌 관리 및 인용 형식 |

#### K-Dense 보고서 생성 워크플로우

```
/ingredient-deep-dive Niacinamide
  ↓
/pubmed-search "niacinamide skin barrier clinical"
  ↓
/clinical-evidence niacinamide barrier repair
  ↓
/mechanism-diagram niacinamide
  ↓
/reference-manager --format APA
```

### 2. 데이터베이스/API 연동 스킬 (11개)

외부 데이터베이스 및 API 연동

| 스킬 | 데이터 소스 | 용도 |
|-----|-----------|-----|
| **cosing-database** | EU CosIng | EU 성분 규제 정보 |
| **kfda-ingredient** | 식약처 | 한국 기능성 성분 DB |
| **ewg-skindeep** | EWG Skin Deep | 성분 안전성 등급 |
| **cir-safety** | CIR | 성분 안전성 리뷰 |
| **mintel-gnpd** | Mintel GNPD | 글로벌 신제품 트렌드 |
| **ifra-standards** | IFRA | 향료 사용 기준 |
| **icid-database** | ICID | 국제 성분 사전 |
| **ulprospector-integration** | UL Prospector | 원료 공급업체 정보 |
| **cosmily-integration** | Cosmily | 성분 분석 데이터 |
| **incidecoder-analysis** | INCIDecoder | 성분 해석 정보 |
| **cosdna-analysis** | CosDNA | 성분 분석 데이터 |

#### 데이터베이스 스킬 사용 예시

```
> "나이아신아마이드 CosIng 정보 확인해줘"
📊 cosing-database 스킬 활성화...
- INCI명: NIACINAMIDE
- CAS 번호: 98-92-0
- EU 규제: 허용 (Annex 없음)
- 기능: Skin conditioning

> "이 성분 EWG 등급 알려줘"
🔬 ewg-skindeep 스킬 활성화...
- EWG 등급: 1 (Low Hazard)
- 데이터 가용성: Fair
- 우려사항: None
```

### 3. 분석/계산 스킬 (9개)

포뮬레이션 및 성분 분석 도구

| 스킬 | 기능 | 적용 |
|-----|-----|-----|
| **formulation-calculator** | 포뮬레이션 계산기 | 배합 비율 계산 |
| **ingredient-compatibility** | 성분 호환성 검사 | 배합 금기 확인 |
| **stability-predictor** | 안정성 예측 | 제형 안정성 분석 |
| **skin-penetration** | 피부 투과 예측 | 성분 전달 분석 |
| **irritation-predictor** | 자극성 예측 | 민감성 평가 |
| **rdkit-cosmetic** | 분자 특성 계산 | 화학적 분석 |
| **concentration-converter** | 농도 단위 변환 | ppm, %, mg/mL 변환 |
| **batch-calculator** | 배치 계산기 | 생산량 스케일업 |
| **ingredient-efficacy-analyzer** | 성분 효능 분석 | 효능 비교 |

#### 분석/계산 스킬 사용 예시

```
> "이 에멀전 배합의 HLB 계산해줘"
🧮 formulation-calculator 스킬 활성화...
- Required HLB: 12.5
- Emulsifier blend: Polysorbate 60 (40%) + Span 60 (60%)
- Calculated HLB: 12.48 ✅

> "레티놀과 AHA 같이 써도 돼?"
⚠️ ingredient-compatibility 스킬 활성화...
- 호환성: 주의 필요
- pH 충돌: Retinol (pH 5.5-6.5) vs AHA (pH 3.0-4.0)
- 권장: 별도 루틴 사용 또는 시간차 적용

> "100g → 5kg 스케일업 계산"
📐 batch-calculator 스킬 활성화...
- Scale factor: 50x
- 원료별 배합량 자동 계산 완료
```

### 4. 규제/문서 스킬 (5개)

규제 대응 및 문서 생성

| 스킬 | 기능 | 대상 규제 |
|-----|-----|---------|
| **regulatory-compliance** | 규제 준수 확인 | 글로벌 |
| **regulatory-checker** | 규제 요건 검사 | 한국/EU/미국 |
| **claim-substantiation** | 클레임 근거 생성 | 마케팅 클레임 |
| **cpsr-generator** | CPSR 문서 생성 | EU 규정 |
| **inci-converter** | INCI명 변환 | 전성분 표기 |

#### 규제/문서 스킬 사용 예시

```
> "EU 수출용 CPSR 초안 생성해줘"
📜 cpsr-generator 스킬 활성화...
- Part A: 안전성 정보 수집 중...
- Part B: 안전성 평가 템플릿 생성 중...
- MoS 계산 포함 완료

> "이 클레임 사용해도 돼? '주름 개선'"
✅ claim-substantiation 스킬 활성화...
- 한국: 기능성 화장품 심사 필요 (인증번호 표기)
- EU: "fine lines" 표현 권장 (의약품 클레임 주의)
- 미국: 합리적 근거 (substantiation) 필요
```

### 5. 마케팅/전략 스킬 (4개)

제품 기획 및 마케팅 지원

| 스킬 | 기능 | 적용 |
|-----|-----|-----|
| **product-positioning** | 제품 포지셔닝 분석 | 시장 전략 |
| **consumer-insight** | 소비자 인사이트 | 고객 분석 |
| **trend-analysis** | 트렌드 분석 | 시장 동향 |
| **formulation-strategy** | 포뮬레이션 전략 | 제형 기획 |

#### 마케팅/전략 스킬 사용 예시

```
> "2025년 스킨케어 트렌드 분석해줘"
📈 trend-analysis 스킬 활성화...
- 핵심 트렌드: 스킨 배리어, 펩타이드, 지속가능성
- 떠오르는 성분: 바쿠치올, 에크토인, 트라넥삼산
- 주목할 포맷: 하이브리드 제형, 리필 시스템

> "30대 여성 타겟 에센스 포지셔닝 제안"
🎯 product-positioning 스킬 활성화...
- 타겟 페르소나: 바쁜 직장인, 효율 중시
- 포지셔닝 키워드: "올인원", "시간 절약", "검증된 효능"
- 경쟁 차별점: 고농축 + 간편 사용성
```

### 6. 시스템/유틸리티 스킬 (4개)

시스템 운영 및 통합

| 스킬 | 기능 | 용도 |
|-----|-----|-----|
| **cosmetic-context-initialization** | 컨텍스트 초기화 | 세션 설정 |
| **get-available-resources** | 리소스 확인 | 사용 가능 도구 |
| **cosmetic-orchestrator** | 워크플로우 오케스트레이션 | 스킬 조합 |
| **cosmetic-clinical-reports** | 임상 보고서 생성 | 문서 출력 |

---

## 스킬 조합 워크플로우

### 신제품 개발 워크플로우

```
1. trend-analysis: 시장 트렌드 파악
   ↓
2. product-positioning: 포지셔닝 설정
   ↓
3. formulation-strategy: 포뮬레이션 전략
   ↓
4. ingredient-compatibility: 성분 조합 검증
   ↓
5. regulatory-checker: 규제 적합성 확인
```

### 성분 리서치 워크플로우

```
1. ingredient-deep-dive: 기본 정보 수집
   ↓
2. pubmed-search: 학술 논문 검색
   ↓
3. ewg-skindeep + cir-safety: 안전성 평가
   ↓
4. clinical-evidence-aggregator: 근거 종합
   ↓
5. mechanism-diagram-generator: 시각화
```

### EU 수출 준비 워크플로우

```
1. cosing-database: EU CosIng 규제 확인
   ↓
2. ifra-standards: 향료 기준 검토
   ↓
3. regulatory-compliance: 규제 준수 확인
   ↓
4. cpsr-generator: CPSR 문서 생성
   ↓
5. inci-converter: 전성분 표기 검증
```

---

## 스킬 통계

| 카테고리 | 스킬 수 | 용도 |
|---------|--------|-----|
| K-Dense 핵심 | 5 | 심층 기술 보고서 |
| 데이터베이스/API | 11 | 외부 데이터 연동 |
| 분석/계산 | 9 | 포뮬레이션 분석 |
| 규제/문서 | 5 | 규제 대응 |
| 마케팅/전략 | 4 | 제품 기획 |
| 시스템/유틸리티 | 4 | 시스템 운영 |
| **총계** | **38** | - |

---

## 요구사항

- [Claude Code](https://docs.anthropic.com/claude-code) 설치됨
- Anthropic API 키 (`ANTHROPIC_API_KEY` 환경변수)
- Node.js (hooks 실행용, 대부분의 시스템에 기본 설치됨)

---

## 라이선스

MIT License

---

## 크레딧

- 원본 Sisyphus: [oh-my-claude-sisyphus](https://github.com/Yeachan-Heo/oh-my-claude-sisyphus) by Yeachan Heo
- 과학 리서치 스킬: [claude-scientific-skills](https://github.com/passeth/claude-scientific-skills) (화장품 특화 커스텀)
- 화장품 특화 Fork: PASSETH

---

<div align="center">

*AI와 함께하는 스마트한 화장품 R&D*

**더 안전하고, 더 효과적인 화장품을 만들어갑니다.**

</div>
