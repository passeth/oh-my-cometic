---
description: 화장품 배합/성분 종합 분석 (HLB, pH, 호환성, 안전성, 규제)
---

[COSMETIC ANALYZE MODE ACTIVATED]

분석 대상: $ARGUMENTS

## 화장품 종합 분석 워크플로우

### Phase 1: 성분 탐색 (ingredient-explorer)
- 프로젝트 내 성분 데이터 빠른 검색
- 배합표, JSON 파일 위치 파악
- 병렬 검색으로 모든 관련 데이터 수집

### Phase 2: 배합 분석 (formulation-oracle)
- HLB 계산 및 유화제 조합 최적화
- pH 호환성 분석
- 성분간 호환성 매트릭스 생성
- 안정성 예측

### Phase 3: 안전성 평가 (safety-oracle)
- EWG/CIR/CosDNA 등급 조회
- MoS (Margin of Safety) 계산
- 자극성/코메도제닉 평가
- 위험 성분 식별

### Phase 4: 규제 검토 (regulatory-oracle)
- EU/한국/미국/중국/일본 규제 확인
- Annex 제한 성분 확인
- 기능성 심사 요건 확인
- 클레임 규제 검토

### Phase 5: 외부 리서치 (cosmetic-librarian)
- CosIng 데이터베이스 조회
- 최신 안전성 연구 검색
- 트렌드 및 시장 정보

### Phase 6: 문서화 (cosmetic-junior)
- 분석 보고서 작성
- 권장사항 정리

---

**주의**: 각 Oracle 에이전트는 READ-ONLY입니다. 문서 작성은 cosmetic-junior가 담당합니다.

분석을 시작합니다.
