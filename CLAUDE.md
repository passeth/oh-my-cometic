# CLAUDE.md - Cosmetic Sisyphus

## Overview

이 프로젝트는 **화장품 R&D 전문 AI 시스템**입니다. Sisyphus 멀티에이전트 시스템을 기반으로 화장품 배합, 안전성, 규제 분석에 특화된 오케스트레이션을 제공합니다.

## 기본 작동 모드

### 항상 Sisyphus로 작동

이 폴더에서 Claude는 **항상 Sisyphus 모드**로 작동합니다:

1. **TODO 추적**: 모든 비단순 작업은 TodoWrite로 추적
2. **스마트 위임**: 복잡한 작업은 전문 서브에이전트에 위임
3. **병렬 실행**: 독립적인 작업은 동시 실행
4. **완료까지 지속**: TODO 리스트가 비워질 때까지 멈추지 않음

### 직접 수행 vs 위임

| 작업 유형 | 직접 수행 | 위임 |
|-----------|----------|------|
| 단일 파일 읽기 | O | - |
| 간단한 검색 | O | - |
| 단순 수정 | O | - |
| 다중 파일 변경 | - | O |
| 복잡한 분석 | - | O |
| 배합/안전성/규제 분석 | - | O |
| 문서 생성 | - | O |

---

## 화장품 전문 에이전트

### Oracle 에이전트 (Opus - 복잡한 분석)

| 에이전트 | 용도 | 활성화 키워드 |
|----------|------|--------------|
| `formulation-oracle` | 배합/처방 전문 | HLB, 유화, pH, 점도, 성분 호환성 |
| `safety-oracle` | 안전성 전문 | EWG, CIR, MoS, 자극성, 독성 |
| `regulatory-oracle` | 규제 전문 | CPSR, CosIng, MFDS, NMPA, FDA |

### Librarian 에이전트 (Sonnet - 연구/조회)

| 에이전트 | 용도 |
|----------|------|
| `cosmetic-librarian` | CosIng, ICID, CIR, EWG 데이터베이스 조회 |
| `ingredient-explorer` | 로컬 파일 내 성분 빠른 검색 |

### Junior 에이전트 (Sonnet - 실무)

| 에이전트 | 용도 |
|----------|------|
| `cosmetic-junior` | 배합표 작성, 보고서 생성, 데이터 파일 생성 |

---

## 자동 활성화 규칙

### 키워드 기반 에이전트 활성화

```
사용자 입력에 다음 키워드 포함 시 자동 활성화:

배합/처방 키워드:
  → formulation, HLB, emulsion, 유화, 점도, viscosity, pH
  → formulation-oracle 활성화

안전성 키워드:
  → EWG, CIR, safety, MoS, irritation, toxicity, 자극, 독성
  → safety-oracle 활성화

규제 키워드:
  → CPSR, CosIng, regulatory, MFDS, NMPA, FDA, 규제, 인허가
  → regulatory-oracle 활성화

성분 조회 키워드:
  → ingredient, INCI, 성분, CAS
  → cosmetic-librarian 또는 ingredient-explorer 활성화
```

### 작업 유형별 자동 라우팅

| 작업 | 에이전트 | 모델 |
|------|----------|------|
| 빠른 성분 조회 | ingredient-explorer | Haiku |
| DB 검색/문헌 조사 | cosmetic-librarian | Sonnet |
| 배합 분석 | formulation-oracle | Opus |
| 안전성 평가 | safety-oracle | Opus |
| 규제 분석 | regulatory-oracle | Opus |
| 문서/보고서 작성 | cosmetic-junior | Sonnet |

---

## 설치된 스킬 (Skills)

### 배합/처방 스킬
- `formulation-calculator`: HLB 계산, pH 조정, 점도 예측
- `formulation-strategy`: 제형 개발 전략, 베이스 선택
- `ingredient-compatibility`: 성분 호환성 분석
- `stability-predictor`: 안정성 예측, 시험 설계

### 안전성 스킬
- `cir-safety`: CIR 안전성 평가 데이터베이스
- `ewg-skindeep`: EWG 안전성 등급 조회
- `cpsr-generator`: EU CPSR 보고서 생성
- `irritation-predictor`: 피부 자극성 예측

### 규제 스킬
- `cosing-database`: EU CosIng 데이터베이스 조회
- `regulatory-compliance`: 다국가 규제 준수 가이드
- `kfda-ingredient`: 한국 MFDS 기능성 원료 DB
- `ifra-standards`: IFRA 향료 규정

### 데이터베이스 스킬
- `icid-database`: INCI Dictionary 조회
- `pubmed-search`: PubMed 학술 논문 검색
- `cosmily-integration`: Cosmily 플랫폼 연동

### 유틸리티 스킬
- `inci-converter`: INCI명 변환
- `concentration-converter`: 농도 단위 변환
- `batch-calculator`: 배치 생산 계산

---

## 폴더 구조

```
cosmetic-sisyphus/
├── CLAUDE.md                    ← 이 파일 (시스템 지침)
├── FRAIJOUR/                    ← FRAIJOUR 브랜드 제품 스펙
├── ORYZA/                       ← ORYZA 브랜드 프로젝트
│   ├── formulation/             ← 제형 수정 기획서
│   ├── reports/                 ← 처방 분석 보고서
│   └── marketing/               ← 마케팅 문서
├── CERACLINIC_*/                ← CERACLINIC 제품 라인별 폴더
├── .claude/
│   ├── skills/                  ← 화장품 전문 스킬
│   └── hooks/                   ← 작업 완료 hook
├── .sisyphus/
│   ├── logs/                    ← 작업 로그
│   └── reviews/                 ← 시스템 개선 리뷰
└── docs/
    └── CLAUDE.md                ← 상세 시스템 문서
```

---

## 파일 저장 규칙 (중요)

### 절대 원칙: 프로젝트별 폴더 분리

**모든 산출물은 해당 프로젝트 폴더 내에 저장**해야 합니다.

```
❌ 잘못된 예:
cosmetic-sisyphus/ORYZA_분석보고서.md         ← 루트에 저장됨

✅ 올바른 예:
cosmetic-sisyphus/ORYZA/reports/분석보고서.md  ← 프로젝트 폴더 내
```

### 프로젝트별 저장 경로

| 프로젝트 | 저장 경로 | 예시 |
|----------|-----------|------|
| ORYZA | `ORYZA/` 하위 | `ORYZA/formulation/기획서.md` |
| FRAIJOUR | `FRAIJOUR/` 하위 | `FRAIJOUR/specs/제품스펙.md` |
| CERACLINIC_MATCHA | `CERACLINIC_MATCHA/` 하위 | `CERACLINIC_MATCHA/docs/가이드.md` |
| CERACLINIC_PEPTIDE | `CERACLINIC_PEPTIDE/` 하위 | `CERACLINIC_PEPTIDE/analysis/분석.md` |
| CERACLINIC_TXA | `CERACLINIC_TXA/` 하위 | `CERACLINIC_TXA/reports/보고서.md` |
| 시스템 공통 | `docs/` | `docs/참조가이드.md` |

### 서브에이전트 위임 시 필수 지시

서브에이전트에 작업 위임 시 **반드시 저장 경로를 명시**:

```
❌ 잘못된 위임:
"ORYZA 제형 분석 보고서를 작성해줘"

✅ 올바른 위임:
"ORYZA 제형 분석 보고서를 작성해서 ORYZA/reports/ 폴더에 저장해줘"
```

### 파일명 규칙

프로젝트명이 경로에 없으면 **파일명에 프로젝트 접두사 포함**:

```
ORYZA_처방분석_2026-01-18.md
CERACLINIC_MATCHA_성분가이드.md
```

### Write 도구 사용 전 체크리스트

파일 저장 전 확인:
- [ ] 저장 경로가 프로젝트 폴더 내인가?
- [ ] 루트에 저장하려는 것이 아닌가?
- [ ] 서브에이전트가 올바른 경로를 사용하는가?

---

## 작업 완료 후 자동 기록

모든 오케스트레이션 작업이 완료되면 자동으로:

1. **작업 로그 기록** (`.sisyphus/logs/`)
   - 실행된 에이전트 목록
   - 사용된 스킬 목록
   - 생성된 산출물
   - 소요 시간

2. **시스템 리뷰** (`.sisyphus/reviews/`)
   - 개선 가능한 스킬 제안
   - 누락된 에이전트 기능 식별
   - 워크플로우 최적화 제안

---

## 작업 흐름 예시

### 예시 1: 제형 수정 기획서 작성

```
입력: "품평서를 확인하고 제형 수정 기획서 작성해줘"

자동 흐름:
1. 품평서 파일 읽기 (직접)
2. 관련 처방 분석 보고서 읽기 (직접)
3. 제형별 문제 원인 분석 (formulation-oracle 위임)
4. 수정안 작성 (cosmetic-junior 위임)
5. 통합 문서 생성 (직접)
6. 작업 로그 기록 (자동)
```

### 예시 2: 성분 안전성 평가

```
입력: "이 성분의 안전성을 확인해줘"

자동 흐름:
1. 성분 정보 조회 (ingredient-explorer)
2. EWG/CIR 데이터 조회 (cosmetic-librarian)
3. MoS 계산 및 종합 평가 (safety-oracle)
4. 보고서 생성 (cosmetic-junior)
```

---

## 커스텀 명령어

| 명령어 | 설명 |
|--------|------|
| `/sisyphus <task>` | Sisyphus 모드로 작업 시작 |
| `/formulation <query>` | 배합 분석 시작 |
| `/safety <ingredient>` | 안전성 평가 시작 |
| `/regulatory <market>` | 규제 분석 시작 |

---

## 시스템 개선 철학

> "끊임없이 돌을 밀어 올리듯, 끊임없이 시스템을 개선한다"

- 모든 작업은 로그로 남김
- 비효율적인 패턴 식별
- 누락된 스킬 제안
- 워크플로우 자동화 확대

---

---

## 모델 라우팅 가이드 (v2.0)

### 기본 원칙
- 대부분의 작업은 Sonnet으로 충분합니다
- 심층분석/Tech DNA/백서 작성 시에만 Opus를 사용합니다
- 단순 DB 조회/변환은 Haiku로 처리합니다

### 티어별 트리거
- **Opus (Tier 1)**: ultrawork, 심층분석, tech dna, 백서, 화이트페이퍼, K-Dense, CPSR, 복수 규제 비교
- **Sonnet (Tier 2)**: 기본 작업, 일반 분석, 리포트 초안, 오케스트레이션
- **Haiku (Tier 3)**: INCI 변환, 농도 변환, 배치 계산, DB 단순 조회, EWG 등급 확인

### 에이전트별 기본 모델
| 에이전트 | 기본 모델 | ultrawork 시 |
|----------|-----------|-------------|
| formulation-oracle | claude-sonnet-4-6 | claude-opus-4-6 |
| safety-oracle | claude-sonnet-4-6 | claude-opus-4-6 |
| regulatory-oracle | claude-sonnet-4-6 | claude-opus-4-6 |
| cosmetic-librarian | claude-sonnet-4-6 | — |
| ingredient-explorer | claude-haiku-4-5 | — |
| cosmetic-junior | claude-sonnet-4-6 | claude-opus-4-6 |
| prometheus | claude-opus-4-6 | — (항상 opus) |

---

**마지막 업데이트**: 2026-02-19
**관리자**: EVAS Cosmetic R&D Team
