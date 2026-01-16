---
name: cosmetic-context-initialization
description: 화장품 관련 작업 시 자동으로 관련 스킬 검색 및 컨텍스트 초기화를 수행하는 스킬
version: 1.0.0
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - TodoWrite
license: MIT
metadata:
  category: workflow-management
  domain: cosmetics
  language: ko
  tags:
    - initialization
    - context-management
    - skill-routing
    - workflow-automation
  dependencies: []
  related-skills:
    - cosing-database
    - kfda-ingredient
    - formulation-calculator
    - regulatory-compliance
    - claim-substantiation
    - consumer-insight
    - trend-analysis
    - product-positioning
    - ingredient-compatibility
    - stability-predictor
---

# Cosmetic Context Initialization Skill

화장품 프로젝트 시작 시 자동으로 관련 스킬을 검색하고 적절한 컨텍스트를 초기화하는 워크플로우 관리 스킬입니다.

## Overview

이 스킬은 화장품 관련 작업의 진입점 역할을 합니다. 사용자의 요청을 분석하여 적합한 스킬을 자동으로 매칭하고, 필요한 컨텍스트를 로드하여 효율적인 작업 환경을 구성합니다.

### 핵심 가치

- **자동 스킬 매칭**: 키워드와 작업 유형 분석을 통한 지능형 스킬 추천
- **컨텍스트 연속성**: 세션 간 작업 상태 유지 및 복원
- **워크플로우 최적화**: 작업 유형별 최적의 스킬 조합 제공

## When to Use

이 스킬은 다음 상황에서 자동으로 활성화됩니다:

1. **새로운 화장품 프로젝트 시작**
   - 신제품 기획 프로젝트 착수
   - R&D 개발 과제 시작
   - 규제 대응 업무 개시

2. **새 대화 세션 시작**
   - 화장품 관련 키워드 감지 시
   - 이전 세션 컨텍스트 복원 필요 시

3. **스킬 추천 요청**
   - 사용자가 적절한 스킬을 모를 때
   - 복합적인 작업에 여러 스킬이 필요할 때

## Core Capabilities

### 1. 키워드 기반 스킬 매칭

사용자 입력에서 키워드를 감지하여 관련 스킬을 자동 매칭합니다.

| 키워드 그룹 | 예시 키워드 | 매칭 스킬 |
|------------|------------|----------|
| 성분 관련 | 성분, ingredient, INCI, 원료 | `cosing-database`, `kfda-ingredient` |
| 배합 관련 | 배합, formulation, 처방, 레시피 | `formulation-calculator` |
| 규제 관련 | 규제, regulation, 인허가, 심사 | `regulatory-compliance` |
| 클레임 관련 | 클레임, claim, 효능, 광고 | `claim-substantiation` |
| 트렌드 관련 | 트렌드, trend, 시장, 동향 | `trend-analysis` |
| 소비자 관련 | 소비자, consumer, VOC, 니즈 | `consumer-insight` |
| 안정성 관련 | 안정성, stability, 유통기한 | `stability-predictor` |
| 호환성 관련 | 호환성, compatibility, 배합금기 | `ingredient-compatibility` |

### 2. 작업 유형별 스킬 세트

프로젝트 유형에 따라 최적화된 스킬 조합을 제공합니다.

#### 신제품 기획 (Product Planning)

```
Primary Skills:
├── consumer-insight      # 소비자 니즈 분석
├── trend-analysis        # 시장 트렌드 파악
└── product-positioning   # 제품 포지셔닝 전략

Supporting Skills:
├── claim-substantiation  # 클레임 방향 검토
└── regulatory-compliance # 규제 사전 검토
```

#### R&D 개발 (Research & Development)

```
Primary Skills:
├── formulation-calculator    # 배합 계산 및 설계
├── ingredient-compatibility  # 성분 호환성 검증
└── stability-predictor       # 안정성 예측

Supporting Skills:
├── cosing-database      # EU 성분 정보 조회
└── kfda-ingredient      # 국내 원료 규제 확인
```

#### 규제 대응 (Regulatory Affairs)

```
Primary Skills:
├── cosing-database          # EU CosIng DB 조회
├── kfda-ingredient          # 식약처 원료 목록
└── regulatory-compliance    # 규제 준수 검증

Supporting Skills:
├── claim-substantiation  # 광고 심의 대응
└── formulation-calculator # 배합비 검증
```

#### 마케팅 (Marketing)

```
Primary Skills:
├── claim-substantiation  # 클레임 입증 자료
└── consumer-insight      # 소비자 인사이트

Supporting Skills:
├── trend-analysis        # 마케팅 트렌드
└── product-positioning   # 커뮤니케이션 전략
```

### 3. 자동 컨텍스트 로드

#### 프로젝트 유형 감지

사용자 입력을 분석하여 프로젝트 유형을 자동 감지합니다:

```
Detection Signals:
├── 기획/Planning: "신제품", "기획", "컨셉", "타겟"
├── R&D: "배합", "처방", "안정성", "테스트"
├── Regulatory: "인허가", "심사", "규제", "등록"
└── Marketing: "광고", "클레임", "마케팅", "홍보"
```

#### 관련 스킬 자동 활성화

감지된 프로젝트 유형에 따라 스킬을 자동 로드합니다:

1. **Primary Skills**: 즉시 활성화, 전체 기능 사용 가능
2. **Supporting Skills**: 대기 상태, 필요시 활성화
3. **Reference Skills**: 참조 모드, 정보 조회만 가능

#### 세션 상태 유지

작업 진행 상황을 추적하고 세션 간 연속성을 보장합니다:

```
Session State:
├── active_skills[]      # 현재 활성 스킬 목록
├── project_type         # 감지된 프로젝트 유형
├── context_data{}       # 로드된 컨텍스트 데이터
├── workflow_stage       # 현재 워크플로우 단계
└── history[]            # 작업 이력
```

## Common Workflows

### Workflow 1: 프로젝트 초기화

새로운 화장품 프로젝트를 시작할 때의 표준 워크플로우입니다.

```
Step 1: 요청 분석
├── 키워드 추출
├── 프로젝트 유형 감지
└── 필요 스킬 식별

Step 2: 컨텍스트 구성
├── 관련 스킬 로드
├── 참조 데이터 준비
└── 작업 환경 설정

Step 3: 스킬 활성화
├── Primary Skills 활성화
├── Supporting Skills 대기
└── 사용자에게 준비 완료 알림

Step 4: 작업 시작
├── 첫 번째 태스크 안내
├── 사용 가능한 기능 설명
└── 도움말 제공
```

### Workflow 2: 스킬 탐색

사용자가 적절한 스킬을 찾을 때의 탐색 워크플로우입니다.

```
Step 1: 요구사항 수집
├── 작업 목적 파악
├── 기대 결과물 확인
└── 제약 조건 식별

Step 2: 스킬 추천
├── 매칭 스킬 목록 제시
├── 각 스킬의 기능 설명
└── 추천 조합 제안

Step 3: 선택 및 활성화
├── 사용자 선택 확인
├── 선택된 스킬 활성화
└── 사용 가이드 제공
```

### Workflow 3: 컨텍스트 전환

작업 중 다른 영역으로 전환이 필요할 때의 워크플로우입니다.

```
Step 1: 전환 신호 감지
├── 새로운 키워드 감지
├── 명시적 전환 요청
└── 작업 완료 신호

Step 2: 현재 상태 저장
├── 진행 상황 저장
├── 중간 결과 보존
└── 복귀 포인트 설정

Step 3: 새 컨텍스트 로드
├── 새 스킬 활성화
├── 관련 데이터 로드
└── 이전 컨텍스트 참조 유지
```

## Best Practices

### 적절한 스킬 선택

1. **단일 작업에는 단일 스킬**
   - 명확한 목적이 있는 경우 해당 스킬만 활성화
   - 불필요한 스킬 로드로 인한 복잡성 방지

2. **복합 작업에는 스킬 세트**
   - 여러 영역에 걸친 작업은 스킬 세트 사용
   - Primary/Supporting 구분으로 우선순위 관리

3. **점진적 확장**
   - 필요에 따라 스킬을 추가 활성화
   - 초기에 모든 스킬을 로드하지 않음

### 컨텍스트 관리

1. **정기적 상태 저장**
   - 중요한 작업 완료 시 상태 저장
   - 긴 세션에서는 중간 체크포인트 생성

2. **불필요한 컨텍스트 정리**
   - 완료된 작업의 컨텍스트는 정리
   - 메모리 효율성 유지

3. **명시적 세션 종료**
   - 작업 완료 시 세션 명시적 종료
   - 최종 결과물 저장 확인

### 효과적인 키워드 사용

1. **명확한 키워드 사용**
   - "성분 검색" vs "그 성분 알려줘"
   - 구체적인 키워드가 정확한 매칭 유도

2. **복합 키워드 조합**
   - "성분 + 규제" → cosing-database + regulatory-compliance
   - 키워드 조합으로 정확한 스킬 세트 매칭

## Usage Examples

### Example 1: 신제품 기획 시작

```
User: "새로운 안티에이징 세럼을 기획하려고 해"

System Response:
├── 프로젝트 유형: Product Planning
├── 활성화된 스킬:
│   ├── [Primary] consumer-insight
│   ├── [Primary] trend-analysis
│   └── [Supporting] claim-substantiation
└── 다음 단계: 타겟 소비자 정의 또는 트렌드 분석
```

### Example 2: 성분 규제 확인

```
User: "나이아신아마이드 배합 한도 확인해줘"

System Response:
├── 프로젝트 유형: Regulatory Affairs
├── 활성화된 스킬:
│   ├── [Primary] cosing-database
│   └── [Primary] kfda-ingredient
└── 결과: 성분 규제 정보 제공
```

### Example 3: 스킬 탐색

```
User: "화장품 개발할 때 쓸 수 있는 스킬 뭐가 있어?"

System Response:
├── 사용 가능한 스킬 카테고리:
│   ├── 성분/원료: cosing-database, kfda-ingredient
│   ├── 배합/처방: formulation-calculator, ingredient-compatibility
│   ├── 규제/인허가: regulatory-compliance
│   ├── 마케팅/클레임: claim-substantiation, consumer-insight
│   └── 트렌드/기획: trend-analysis, product-positioning
└── 권장: 작업 목적을 알려주시면 최적의 스킬을 추천해드립니다
```

## Error Handling

### 스킬 매칭 실패

키워드로 적절한 스킬을 찾지 못한 경우:

```
Fallback Process:
1. 사용 가능한 전체 스킬 목록 제시
2. 작업 목적 재확인 요청
3. 수동 스킬 선택 가이드 제공
```

### 컨텍스트 로드 실패

스킬 또는 참조 데이터 로드 실패 시:

```
Recovery Process:
1. 실패 원인 진단
2. 대체 스킬 또는 데이터 제안
3. 수동 설정 옵션 제공
```

## Notes

- 이 스킬은 다른 모든 화장품 스킬의 진입점 역할을 합니다
- 스킬 매칭 정확도는 사용자 입력의 명확성에 비례합니다
- 새로운 스킬 추가 시 키워드 매핑 테이블 업데이트가 필요합니다
- 세션 상태는 대화 종료 시 자동으로 저장되지 않으므로 명시적 저장이 필요합니다
