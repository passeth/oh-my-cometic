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

## 기반 기술

이 프로젝트는 [oh-my-claude-sisyphus](https://github.com/Yeachan-Heo/oh-my-claude-sisyphus)를 기반으로 화장품 R&D에 특화된 에이전트를 추가한 fork입니다.

### 포함된 기본 기능
- 19개 범용 에이전트 (oracle, librarian, explore 등)
- 18개 라이프사이클 훅
- 8개 빌트인 스킬 (ultrawork, git-master 등)
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
