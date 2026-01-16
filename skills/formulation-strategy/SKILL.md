---
name: formulation-strategy
description: 제형 개발 전략 수립 및 베이스 선택 가이드. 에멀전 유형(O/W, W/O, W/S) 선택, 전달 시스템(리포좀, 사이클로덱스트린 등) 추천, 활성 성분별 최적 제형 설계 및 제품 유형별 배합 가이드 제공.
allowed-tools: [Read, Write, Edit, Bash, WebFetch]
license: MIT license
metadata:
    skill-author: EVAS Cosmetic
    original-source: K-Dense Inc. (claude-scientific-skills structure)
    version: 1.0.0
    category: formulation-methodology
---

# Formulation Strategy Skill

## Overview

화장품 제형 개발 전략 수립 및 최적 베이스 선택을 위한 종합 가이드입니다. 제품 목적, 타겟 피부, 활성 성분 특성을 고려하여 최적의 에멀전 시스템, 전달 시스템, 배합 구성을 제안합니다.

## When to Use This Skill

- **신제품 기획**: 제품 컨셉에 맞는 제형 시스템 선택
- **베이스 선택**: O/W, W/O, W/S, 무수 제형 결정
- **활성 성분 안정화**: 불안정 성분의 전달 시스템 선택
- **제형 최적화**: 피부 타입, 계절별 텍스처 조정
- **스케일업 준비**: 양산 가능한 제형 설계

## Core Capabilities

### 1. 에멀전 시스템 선택

#### 1.1 O/W 에멀전 (Oil-in-Water)

| 특성 | 내용 |
|------|------|
| 연속상 | 물 |
| 분산상 | 오일 방울 |
| HLB 범위 | 8-18 |
| 텍스처 | 가볍고 산뜻 |
| 흡수 | 빠름 |

권장 상황:
- 데일리 보습제
- 여름철 제품
- 지성/복합성 피부
- 수용성 활성 성분
- 세럼/에센스

#### 1.2 W/O 에멀전 (Water-in-Oil)

| 특성 | 내용 |
|------|------|
| 연속상 | 오일 |
| 분산상 | 물 방울 |
| HLB 범위 | 3-8 |
| 텍스처 | 리치하고 무거움 |
| 흡수 | 느림 |

권장 상황:
- 나이트 크림
- 겨울철 제품
- 건성/성숙 피부
- 장벽 보호
- 지용성 활성 성분

#### 1.3 W/S 에멀전 (Water-in-Silicone)

| 특성 | 내용 |
|------|------|
| 연속상 | 실리콘 오일 |
| 분산상 | 물 방울 |
| 텍스처 | 실키, 벨벳 |
| 내수성 | 우수 |

권장 상황:
- 선크림
- 메이크업 프라이머
- 지속력 중시 제품

### 2. 전달 시스템 선택 가이드

| 시스템 | 적합 성분 | 장점 | 비용 |
|--------|-----------|------|------|
| 리포좀 | 수용성/지용성 | 피부 침투 증진 | 높음 |
| 사이클로덱스트린 | 소수성 분자 | 수용성/안정성 향상 | 중간 |
| SLN/NLC | 지용성 | 서방형 방출 | 높음 |
| 나노에멀전 | 지용성 | 투명, 빠른 흡수 | 중간 |

### 3. 활성 성분별 제형 전략

#### 비타민C
- 문제: 산화, pH 민감
- 1순위: 무수 오일 세럼
- 2순위: 저pH 수성 세럼 (pH 2.5-3.5)
- 전달: 리포좀, 마이크로캡슐

#### 레티놀
- 문제: 광분해, 산화
- 1순위: 무수 오일 세럼
- 2순위: W/O 크림
- 전달: 사이클로덱스트린, SLN

#### 나이아신아마이드
- 특성: 매우 안정
- 권장: O/W 세럼/크림
- pH: 5.0-7.0
- 농도: 2-10%

### 4. 제품 유형별 기본 배합

#### 수성 세럼 (기본)
```
정제수                  to 100%
Glycerin                5.0%
Butylene Glycol         5.0%
Sodium Hyaluronate      0.5%
Carbomer                0.2%
Triethanolamine         q.s.
활성 성분               as needed
Phenoxyethanol          0.8%
```

#### O/W 크림 (기본)
```
A상 (수상) - 70°C
정제수                  to 100%
Glycerin                5.0%
Disodium EDTA           0.05%

B상 (유상) - 70°C
Cetearyl Alcohol        3.0%
Glyceryl Stearate       2.0%
PEG-100 Stearate        1.5%
오일상                  15-20%

C상 (냉각 후)
활성 성분               as needed
Phenoxyethanol          0.8%
```

## Usage Examples

### 기본 쿼리
- "비타민C 세럼 제형 전략 제안해줘"
- "민감성 피부용 보습 크림 베이스 추천"

### 상세 분석
- "건성 피부용 겨울 나이트 크림 전체 배합 설계"
- "SPF50+ 선크림 W/S 에멀전 개발 전략"

## Related Skills

- [ingredient-compatibility](../ingredient-compatibility/SKILL.md)
- [stability-predictor](../stability-predictor/SKILL.md)
- [formulation-calculator](../formulation-calculator/SKILL.md)

## References

- [베이스 선택 가이드](./references/base_selection.md)
- [전달 시스템](./references/delivery_systems.md)
- [제형 유형별 특성](./references/formulation_types.md)
