# Initialization Rules Reference

화장품 스킬 컨텍스트 초기화를 위한 규칙과 매핑 정보를 정의합니다.

## 1. 키워드-스킬 매핑 테이블

### 1.1 Primary Keyword Mappings

직접적인 1:1 또는 1:N 매핑을 정의합니다.

```yaml
# 성분/원료 관련
ingredient_keywords:
  keywords:
    - 성분
    - ingredient
    - INCI
    - 원료
    - 물질
    - 화학명
    - CAS
    - 성분표
  skills:
    primary: cosing-database
    secondary: kfda-ingredient
  confidence: high

# 배합/처방 관련
formulation_keywords:
  keywords:
    - 배합
    - formulation
    - 처방
    - 레시피
    - formula
    - 배합비
    - 조성
    - 함량
  skills:
    primary: formulation-calculator
    secondary: ingredient-compatibility
  confidence: high

# 규제/인허가 관련
regulatory_keywords:
  keywords:
    - 규제
    - regulation
    - 인허가
    - 심사
    - 등록
    - 신고
    - 허가
    - 법규
    - 기준
    - 규격
  skills:
    primary: regulatory-compliance
    secondary:
      - cosing-database
      - kfda-ingredient
  confidence: high

# 클레임/효능 관련
claim_keywords:
  keywords:
    - 클레임
    - claim
    - 효능
    - 광고
    - 표현
    - 효과
    - 입증
    - 실증
    - 심의
  skills:
    primary: claim-substantiation
    secondary: regulatory-compliance
  confidence: high

# 트렌드/시장 관련
trend_keywords:
  keywords:
    - 트렌드
    - trend
    - 시장
    - 동향
    - 유행
    - 인기
    - 핫한
    - 떠오르는
  skills:
    primary: trend-analysis
    secondary: consumer-insight
  confidence: medium

# 소비자 관련
consumer_keywords:
  keywords:
    - 소비자
    - consumer
    - VOC
    - 니즈
    - 고객
    - 타겟
    - 페르소나
    - 구매
  skills:
    primary: consumer-insight
    secondary: product-positioning
  confidence: medium

# 안정성 관련
stability_keywords:
  keywords:
    - 안정성
    - stability
    - 유통기한
    - 변색
    - 변취
    - 분리
    - 침전
    - 보존
  skills:
    primary: stability-predictor
    secondary: formulation-calculator
  confidence: high

# 호환성 관련
compatibility_keywords:
  keywords:
    - 호환성
    - compatibility
    - 배합금기
    - 상극
    - 반응
    - 충돌
    - 불가
  skills:
    primary: ingredient-compatibility
    secondary: formulation-calculator
  confidence: high

# 포지셔닝 관련
positioning_keywords:
  keywords:
    - 포지셔닝
    - positioning
    - 컨셉
    - 차별화
    - USP
    - 경쟁
    - 벤치마킹
  skills:
    primary: product-positioning
    secondary:
      - consumer-insight
      - trend-analysis
  confidence: medium
```

### 1.2 Compound Keyword Mappings

복합 키워드 조합에 대한 매핑을 정의합니다.

```yaml
compound_mappings:
  # 성분 + 규제
  - patterns:
      - ["성분", "규제"]
      - ["원료", "허가"]
      - ["INCI", "등록"]
    skills:
      - cosing-database
      - kfda-ingredient
      - regulatory-compliance
    priority: 1

  # 배합 + 안정성
  - patterns:
      - ["배합", "안정성"]
      - ["처방", "유통기한"]
      - ["formula", "stability"]
    skills:
      - formulation-calculator
      - stability-predictor
      - ingredient-compatibility
    priority: 1

  # 클레임 + 마케팅
  - patterns:
      - ["클레임", "광고"]
      - ["효능", "마케팅"]
      - ["표현", "홍보"]
    skills:
      - claim-substantiation
      - consumer-insight
    priority: 1

  # 신제품 + 기획
  - patterns:
      - ["신제품", "기획"]
      - ["새로운", "개발"]
      - ["출시", "계획"]
    skills:
      - consumer-insight
      - trend-analysis
      - product-positioning
    priority: 2
```

### 1.3 Context-Sensitive Mappings

문맥에 따라 다르게 매핑되는 키워드입니다.

```yaml
context_sensitive:
  "검색":
    contexts:
      - context: ingredient
        skill: cosing-database
      - context: trend
        skill: trend-analysis
      - context: regulation
        skill: regulatory-compliance
    default: cosing-database

  "분석":
    contexts:
      - context: consumer
        skill: consumer-insight
      - context: market
        skill: trend-analysis
      - context: formulation
        skill: formulation-calculator
    default: trend-analysis

  "확인":
    contexts:
      - context: regulation
        skill: regulatory-compliance
      - context: compatibility
        skill: ingredient-compatibility
      - context: claim
        skill: claim-substantiation
    default: regulatory-compliance
```

## 2. 우선순위 규칙

### 2.1 스킬 활성화 우선순위

```yaml
activation_priority:
  levels:
    1_critical:
      description: "필수 활성화 - 작업 수행에 반드시 필요"
      activation: immediate
      resources: full
      examples:
        - cosing-database (성분 조회 시)
        - formulation-calculator (배합 계산 시)

    2_primary:
      description: "기본 활성화 - 주요 작업 지원"
      activation: immediate
      resources: standard
      examples:
        - regulatory-compliance (규제 확인 시)
        - claim-substantiation (클레임 작성 시)

    3_supporting:
      description: "보조 활성화 - 필요시 활성화"
      activation: on_demand
      resources: minimal
      examples:
        - ingredient-compatibility (호환성 확인 필요 시)
        - stability-predictor (안정성 예측 필요 시)

    4_reference:
      description: "참조용 - 정보 조회만 가능"
      activation: lazy
      resources: minimal
      examples:
        - trend-analysis (참고 정보로만 사용 시)
        - consumer-insight (배경 정보로만 사용 시)
```

### 2.2 키워드 매칭 우선순위

```yaml
keyword_matching_priority:
  rules:
    - name: exact_match
      priority: 1
      description: "정확히 일치하는 키워드"
      weight: 1.0

    - name: compound_match
      priority: 2
      description: "복합 키워드 조합 일치"
      weight: 0.9

    - name: partial_match
      priority: 3
      description: "부분 일치 (키워드 포함)"
      weight: 0.7

    - name: semantic_match
      priority: 4
      description: "의미적 유사성"
      weight: 0.5

    - name: context_inferred
      priority: 5
      description: "문맥에서 추론"
      weight: 0.3
```

### 2.3 충돌 해결 규칙

```yaml
conflict_resolution:
  # 여러 스킬이 동시에 매칭될 때
  multiple_match:
    strategy: priority_based
    rules:
      - "더 높은 confidence 스킬 우선"
      - "더 구체적인 매칭 우선"
      - "최근 사용된 스킬 우선"
    fallback: "사용자에게 선택 요청"

  # 스킬 간 리소스 충돌 시
  resource_conflict:
    strategy: sequential
    rules:
      - "Primary 스킬 먼저 실행"
      - "결과 의존성에 따라 순차 실행"
    fallback: "병렬 실행 가능 여부 확인"
```

## 3. 스킬 의존성

### 3.1 의존성 그래프

```yaml
skill_dependencies:
  # cosing-database
  cosing-database:
    depends_on: []
    provides_to:
      - formulation-calculator
      - regulatory-compliance
      - ingredient-compatibility
    data_flow:
      output:
        - ingredient_info
        - safety_data
        - regulatory_limits

  # kfda-ingredient
  kfda-ingredient:
    depends_on: []
    provides_to:
      - formulation-calculator
      - regulatory-compliance
    data_flow:
      output:
        - korea_ingredient_info
        - usage_limits
        - notification_requirements

  # formulation-calculator
  formulation-calculator:
    depends_on:
      - cosing-database (optional)
      - kfda-ingredient (optional)
    provides_to:
      - stability-predictor
      - ingredient-compatibility
    data_flow:
      input:
        - ingredient_limits
        - usage_restrictions
      output:
        - formulation_data
        - composition_breakdown

  # ingredient-compatibility
  ingredient-compatibility:
    depends_on:
      - cosing-database (optional)
    provides_to:
      - formulation-calculator
      - stability-predictor
    data_flow:
      input:
        - ingredient_properties
      output:
        - compatibility_matrix
        - warning_flags

  # stability-predictor
  stability-predictor:
    depends_on:
      - formulation-calculator (recommended)
      - ingredient-compatibility (recommended)
    provides_to: []
    data_flow:
      input:
        - formulation_data
        - compatibility_data
      output:
        - stability_prediction
        - shelf_life_estimate

  # regulatory-compliance
  regulatory-compliance:
    depends_on:
      - cosing-database (optional)
      - kfda-ingredient (optional)
    provides_to:
      - claim-substantiation
    data_flow:
      input:
        - ingredient_info
        - formulation_data
      output:
        - compliance_status
        - required_actions

  # claim-substantiation
  claim-substantiation:
    depends_on:
      - regulatory-compliance (recommended)
    provides_to: []
    data_flow:
      input:
        - compliance_status
        - product_info
      output:
        - approved_claims
        - evidence_requirements

  # consumer-insight
  consumer-insight:
    depends_on: []
    provides_to:
      - product-positioning
      - trend-analysis
    data_flow:
      output:
        - consumer_needs
        - preference_data

  # trend-analysis
  trend-analysis:
    depends_on:
      - consumer-insight (optional)
    provides_to:
      - product-positioning
    data_flow:
      input:
        - consumer_data
      output:
        - trend_insights
        - market_opportunities

  # product-positioning
  product-positioning:
    depends_on:
      - consumer-insight (recommended)
      - trend-analysis (recommended)
    provides_to: []
    data_flow:
      input:
        - consumer_needs
        - trend_data
      output:
        - positioning_strategy
        - differentiation_points
```

### 3.2 자동 의존성 해결

```yaml
auto_dependency_resolution:
  enabled: true

  rules:
    # 필수 의존성 자동 활성화
    - condition: "required dependency not active"
      action: "activate dependency skill"
      notification: true

    # 권장 의존성 제안
    - condition: "recommended dependency not active"
      action: "suggest activation"
      notification: true

    # 선택적 의존성 무시
    - condition: "optional dependency not active"
      action: "proceed without"
      notification: false

  cascade_activation:
    enabled: true
    max_depth: 2
    confirmation_required: true
```

## 4. 세션 관리

### 4.1 세션 상태 구조

```yaml
session_state_schema:
  session_id: string
  created_at: timestamp
  updated_at: timestamp

  project:
    type: enum[planning, rnd, regulatory, marketing, general]
    name: string
    description: string

  active_skills:
    - skill_id: string
      activation_level: enum[critical, primary, supporting, reference]
      activated_at: timestamp
      state: object

  context_data:
    loaded_references: array
    cached_results: object
    user_preferences: object

  workflow:
    current_stage: string
    completed_stages: array
    pending_tasks: array

  history:
    - timestamp: timestamp
      action: string
      skill: string
      result: object
```

### 4.2 세션 생명주기

```yaml
session_lifecycle:
  creation:
    trigger: "첫 화장품 관련 요청"
    actions:
      - initialize_session
      - detect_project_type
      - load_default_skills
    timeout: null

  active:
    maintain_conditions:
      - "활성 대화 진행 중"
      - "스킬 사용 중"
    auto_save_interval: 5_minutes

  suspended:
    trigger: "사용자 비활성 15분"
    actions:
      - save_current_state
      - release_resources
    resume_conditions:
      - "새로운 요청"
      - "명시적 재개 요청"

  terminated:
    trigger:
      - "명시적 종료 요청"
      - "비활성 24시간"
    actions:
      - save_final_state
      - generate_summary
      - release_all_resources
```

### 4.3 상태 저장/복원

```yaml
state_persistence:
  save:
    triggers:
      - skill_completion
      - stage_transition
      - explicit_save_request
      - auto_save_interval

    data_to_save:
      - active_skills_state
      - context_data
      - workflow_progress
      - user_inputs

    storage:
      method: memory_system
      key_format: "cosmetic_session_{session_id}"
      expiry: 7_days

  restore:
    triggers:
      - session_resume
      - explicit_restore_request

    validation:
      - check_skill_availability
      - verify_data_integrity
      - update_stale_references

    fallback:
      on_failure: "새 세션 시작 제안"
```

### 4.4 멀티세션 관리

```yaml
multi_session:
  max_concurrent: 3

  switching:
    method: explicit_request
    preserve_state: true
    notification: true

  naming:
    auto_generate: true
    format: "{project_type}_{date}_{index}"
    allow_rename: true

  cleanup:
    auto_cleanup: true
    cleanup_after: 7_days
    archive_option: true
```

## 5. 초기화 프로세스

### 5.1 표준 초기화 순서

```yaml
initialization_sequence:
  step_1_analyze:
    name: "요청 분석"
    actions:
      - extract_keywords
      - detect_project_type
      - identify_required_skills
    output: analysis_result
    timeout: 2_seconds

  step_2_match:
    name: "스킬 매칭"
    input: analysis_result
    actions:
      - match_primary_skills
      - identify_dependencies
      - determine_activation_levels
    output: skill_list
    timeout: 1_second

  step_3_load:
    name: "컨텍스트 로드"
    input: skill_list
    actions:
      - activate_skills
      - load_references
      - initialize_skill_states
    output: context_ready
    timeout: 5_seconds

  step_4_prepare:
    name: "작업 환경 준비"
    input: context_ready
    actions:
      - setup_workflow
      - generate_guidance
      - notify_user
    output: session_ready
    timeout: 1_second
```

### 5.2 빠른 초기화 (캐시 활용)

```yaml
quick_initialization:
  conditions:
    - "동일 프로젝트 유형 재방문"
    - "최근 세션 존재 (24시간 이내)"

  process:
    - restore_cached_state
    - validate_and_update
    - notify_resume

  fallback: standard_initialization
```

### 5.3 초기화 실패 처리

```yaml
initialization_failure_handling:
  skill_load_failure:
    action: "대체 스킬 탐색"
    fallback: "수동 스킬 선택 안내"
    notification: true

  dependency_resolution_failure:
    action: "부분 기능으로 진행"
    fallback: "의존성 없이 단독 실행"
    notification: true

  context_load_failure:
    action: "기본 컨텍스트로 시작"
    fallback: "빈 컨텍스트로 시작"
    notification: true

  complete_failure:
    action: "오류 보고 및 수동 설정 안내"
    recovery: "기본 대화 모드로 전환"
```

## 6. 성능 최적화

### 6.1 지연 로딩 (Lazy Loading)

```yaml
lazy_loading:
  enabled: true

  immediate_load:
    - matched_primary_skills
    - critical_dependencies

  deferred_load:
    - supporting_skills
    - optional_references
    - historical_data

  on_demand_load:
    - reference_skills
    - archived_context
```

### 6.2 캐싱 전략

```yaml
caching:
  skill_results:
    enabled: true
    ttl: 30_minutes
    invalidation: "source_data_change"

  reference_data:
    enabled: true
    ttl: 24_hours
    preload: true

  user_preferences:
    enabled: true
    ttl: 7_days
    persist: true
```

### 6.3 리소스 관리

```yaml
resource_management:
  max_active_skills: 5
  max_loaded_references: 10
  memory_limit: "적정 수준"

  cleanup_trigger:
    - "리소스 한도 도달"
    - "스킬 비활성화"
    - "세션 종료"

  cleanup_priority:
    1: "미사용 캐시"
    2: "완료된 작업 결과"
    3: "비활성 스킬 상태"
```
