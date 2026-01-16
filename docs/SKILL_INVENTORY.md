# Claude Cosmetic Skills - 스킬 인벤토리

총 **38개** 스킬 구현 완료 (2026-01-16 기준)

## 1. K-Dense 핵심 스킬 (5개)

K-Dense 수준의 기술 보고서 생성을 위한 핵심 스킬

| 스킬명 | 설명 | 구성 요소 |
|-------|------|----------|
| **pubmed-search** | PubMed 학술 검색 및 논문 정보 추출 | SKILL.md, scripts/, references/ |
| **ingredient-deep-dive** | 성분 심층 분석 보고서 생성 | SKILL.md, scripts/, references/ |
| **mechanism-diagram-generator** | 작용 기전 Mermaid 다이어그램 생성 | SKILL.md, scripts/, references/ |
| **clinical-evidence-aggregator** | 임상 근거 수집 및 등급화 | SKILL.md, scripts/, references/ |
| **reference-manager** | 학술 참고문헌 관리 및 인용 형식 | SKILL.md, scripts/, references/ |

---

## 2. 데이터베이스/API 연동 스킬 (11개)

외부 데이터베이스 및 API 연동

| 스킬명 | 데이터 소스 | 용도 |
|-------|------------|------|
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

---

## 3. 분석/계산 스킬 (9개)

포뮬레이션 및 성분 분석 도구

| 스킬명 | 기능 | 적용 |
|-------|------|------|
| **formulation-calculator** | 포뮬레이션 계산기 | 배합 비율 계산 |
| **ingredient-compatibility** | 성분 호환성 검사 | 배합 금기 확인 |
| **stability-predictor** | 안정성 예측 | 제형 안정성 분석 |
| **skin-penetration** | 피부 투과 예측 | 성분 전달 분석 |
| **irritation-predictor** | 자극성 예측 | 민감성 평가 |
| **rdkit-cosmetic** | 분자 특성 계산 | 화학적 분석 |
| **concentration-converter** | 농도 단위 변환 | ppm, %, mg/mL 변환 |
| **batch-calculator** | 배치 계산기 | 생산량 스케일업 |
| **ingredient-efficacy-analyzer** | 성분 효능 분석 | 효능 비교 |

---

## 4. 규제/문서 스킬 (5개)

규제 대응 및 문서 생성

| 스킬명 | 기능 | 대상 규제 |
|-------|------|----------|
| **regulatory-compliance** | 규제 준수 확인 | 글로벌 |
| **regulatory-checker** | 규제 요건 검사 | 한국/EU/미국 |
| **claim-substantiation** | 클레임 근거 생성 | 마케팅 클레임 |
| **cpsr-generator** | CPSR 문서 생성 | EU 규정 |
| **inci-converter** | INCI명 변환 | 전성분 표기 |

---

## 5. 마케팅/전략 스킬 (4개)

제품 기획 및 마케팅 지원

| 스킬명 | 기능 | 적용 |
|-------|------|------|
| **product-positioning** | 제품 포지셔닝 분석 | 시장 전략 |
| **consumer-insight** | 소비자 인사이트 | 고객 분석 |
| **trend-analysis** | 트렌드 분석 | 시장 동향 |
| **formulation-strategy** | 포뮬레이션 전략 | 제형 기획 |

---

## 6. 시스템/유틸리티 스킬 (4개)

시스템 운영 및 통합

| 스킬명 | 기능 | 용도 |
|-------|------|------|
| **cosmetic-context-initialization** | 컨텍스트 초기화 | 세션 설정 |
| **get-available-resources** | 리소스 확인 | 사용 가능 도구 |
| **cosmetic-orchestrator** | 워크플로우 오케스트레이션 | 스킬 조합 |
| **cosmetic-clinical-reports** | 임상 보고서 생성 | 문서 출력 |

---

## 스킬 사용 예시

### K-Dense 수준 보고서 생성 워크플로우

```
1. ingredient-deep-dive: 성분 기본 분석
   ↓
2. pubmed-search: 관련 논문 검색
   ↓
3. clinical-evidence-aggregator: 근거 수집 및 등급화
   ↓
4. mechanism-diagram-generator: 작용 기전 시각화
   ↓
5. reference-manager: 참고문헌 정리
```

### 제품 기획 워크플로우

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

---

## 통계 요약

| 카테고리 | 스킬 수 |
|---------|--------|
| K-Dense 핵심 | 5 |
| 데이터베이스/API | 11 |
| 분석/계산 | 9 |
| 규제/문서 | 5 |
| 마케팅/전략 | 4 |
| 시스템/유틸리티 | 4 |
| **총계** | **38** |

---

## 버전 정보

- **버전**: 1.0.0
- **최종 업데이트**: 2026-01-16
- **관리자**: EVAS Cosmetic
