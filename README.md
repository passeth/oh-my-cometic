<div align="center">

# Oh-My-Cosmetic

### 화장품 R&D 멀티에이전트 시스템

[![Version](https://img.shields.io/badge/version-1.0.0-ff6b6b)](https://github.com/passeth/oh-my-cometic/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-20+-339933?logo=node.js&logoColor=white)](https://nodejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178c6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
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

### 방법 1: 설치 스크립트 (권장)

```bash
git clone https://github.com/passeth/oh-my-cometic.git
cd oh-my-cometic
npm install
npm run build
./scripts/install.sh
```

### 방법 2: npm 글로벌 설치

```bash
npm install -g oh-my-cosmetic
```

### 설치 후 설정

```bash
# Claude Code 시작
claude

# 프로젝트별 설정 (권장)
/sisyphus-default

# 또는 전역 설정
/sisyphus-default-global
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
- 화장품 키워드 자동 감지
- 화장품 슬래시 명령어
- 배합/안전성/규제 특화 프롬프트

---

## 요구사항

- [Claude Code](https://docs.anthropic.com/claude-code) 설치됨
- Anthropic API 키 (`ANTHROPIC_API_KEY` 환경변수)
- Node.js 20+

---

## 라이선스

MIT License

---

## 크레딧

- 원본 프로젝트: [oh-my-claude-sisyphus](https://github.com/Yeachan-Heo/oh-my-claude-sisyphus) by Yeachan Heo
- 화장품 특화 확장: EVAS Cosmetic

---

<div align="center">

*AI와 함께하는 스마트한 화장품 R&D*

**더 안전하고, 더 효과적인 화장품을 만들어갑니다.**

</div>
