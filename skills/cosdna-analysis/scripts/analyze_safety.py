#!/usr/bin/env python3
"""
전성분 안전성 분석 모듈

CosDNA 데이터를 활용하여 전성분 리스트의 안전성을 분석하고
민감성 피부 적합성을 평가합니다.
"""

import re
import time
import json
from typing import Optional, List
from dataclasses import dataclass, asdict, field

from fetch_cosdna import search_and_get_safety, IngredientSafety


# 안전성 점수 기준
SAFETY_THRESHOLDS = {
    "safe": (1, 2),  # 안전
    "moderate": (3, 4),  # 보통
    "concern": (5, 9),  # 주의
}

ACNE_THRESHOLDS = {"safe": (0, 1), "moderate": (2, 3), "concern": (4, 5)}

IRRITANT_THRESHOLDS = {"safe": (0, 1), "moderate": (2, 3), "concern": (4, 5)}

# 일반적으로 주의가 필요한 성분
KNOWN_IRRITANTS = [
    "sodium-lauryl-sulfate",
    "sls",
    "sodium-laureth-sulfate",
    "sles",
    "alcohol-denat",
    "sd-alcohol",
    "denatured-alcohol",
    "fragrance",
    "parfum",
    "synthetic-fragrance",
    "essential-oil",
    "citrus-oil",
    "lemon-oil",
    "lime-oil",
    "menthol",
    "camphor",
    "peppermint",
]

# 분석 제외 베이스 성분
BASE_INGREDIENTS = ["water", "aqua", "purified-water"]


@dataclass
class IngredientAnalysis:
    """개별 성분 분석 결과"""

    name: str
    position: int
    safety: Optional[int]
    acne: Optional[int]
    irritant: Optional[int]
    safety_level: str  # safe, moderate, concern
    is_flagged: bool
    flag_reasons: List[str] = field(default_factory=list)
    cosdna_url: str = ""


@dataclass
class SafetyAnalysisResult:
    """전성분 안전성 분석 결과"""

    total_count: int
    analyzed_count: int
    skipped_count: int

    # 안전성 등급별 분류
    safe_ingredients: List[str]
    moderate_ingredients: List[str]
    concern_ingredients: List[str]

    # 특정 문제 성분
    acne_triggers: List[str]
    irritants: List[str]

    # 상세 분석
    ingredients: List[IngredientAnalysis]

    # 요약
    overall_safety: str  # safe, moderate, concern
    sensitive_skin_suitable: bool
    summary: str
    recommendations: List[str]


def parse_ingredients(full_ingredients: str) -> List[str]:
    """전성분 텍스트를 개별 성분 리스트로 파싱"""
    text = full_ingredients.replace("\n", ",").replace("\r", "")
    ingredients = [i.strip() for i in text.split(",")]
    return [i for i in ingredients if i and len(i) > 1]


def to_slug(name: str) -> str:
    """성분명을 slug로 변환"""
    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    return slug


def is_known_irritant(slug: str) -> bool:
    """알려진 자극성 성분인지 확인"""
    for irritant in KNOWN_IRRITANTS:
        if irritant in slug or slug in irritant:
            return True
    return False


def get_safety_level(score: Optional[int], thresholds: dict) -> str:
    """점수를 안전성 레벨로 변환"""
    if score is None:
        return "unknown"

    for level, (min_val, max_val) in thresholds.items():
        if min_val <= score <= max_val:
            return level
    return "unknown"


def analyze_ingredients_safety(
    full_ingredients: str,
    fetch_details: bool = True,
    delay: float = 1.5,
    max_fetch: int = 15,
) -> SafetyAnalysisResult:
    """
    전성분 안전성 분석

    Args:
        full_ingredients: 쉼표로 구분된 전성분 텍스트
        fetch_details: CosDNA에서 상세 정보 조회 여부
        delay: 요청 간 간격 (초)
        max_fetch: 최대 조회 성분 수

    Returns:
        SafetyAnalysisResult 데이터클래스
    """
    ingredients = parse_ingredients(full_ingredients)

    analyses = []
    safe_list = []
    moderate_list = []
    concern_list = []
    acne_triggers = []
    irritants = []

    fetch_count = 0
    skipped_count = 0

    for idx, ingredient in enumerate(ingredients):
        slug = to_slug(ingredient)
        is_base = slug in BASE_INGREDIENTS

        # 기본 분석
        analysis = IngredientAnalysis(
            name=ingredient,
            position=idx + 1,
            safety=None,
            acne=None,
            irritant=None,
            safety_level="unknown",
            is_flagged=False,
            flag_reasons=[],
        )

        # 베이스 성분 스킵
        if is_base:
            skipped_count += 1
            safe_list.append(ingredient)
            analysis.safety_level = "safe"
            analyses.append(analysis)
            continue

        # 알려진 자극성 성분 체크
        if is_known_irritant(slug):
            analysis.is_flagged = True
            analysis.flag_reasons.append("알려진 자극성 성분")
            irritants.append(ingredient)

        # CosDNA 조회
        if fetch_details and fetch_count < max_fetch:
            if fetch_count > 0:
                time.sleep(delay)

            safety_info = search_and_get_safety(ingredient)
            fetch_count += 1

            if safety_info and not safety_info.error:
                analysis.safety = safety_info.safety
                analysis.acne = safety_info.acne
                analysis.irritant = safety_info.irritant
                analysis.cosdna_url = safety_info.url

                # 안전성 레벨 결정
                analysis.safety_level = get_safety_level(
                    safety_info.safety, SAFETY_THRESHOLDS
                )

                # 여드름 유발 체크
                if safety_info.acne and safety_info.acne >= 3:
                    acne_triggers.append(ingredient)
                    analysis.is_flagged = True
                    analysis.flag_reasons.append(
                        f"여드름 유발 가능성 (Acne={safety_info.acne})"
                    )

                # 자극성 체크
                if safety_info.irritant and safety_info.irritant >= 3:
                    if ingredient not in irritants:
                        irritants.append(ingredient)
                    analysis.is_flagged = True
                    analysis.flag_reasons.append(
                        f"자극 가능성 (Irritant={safety_info.irritant})"
                    )

                # 안전성 점수 체크
                if safety_info.safety and safety_info.safety >= 5:
                    analysis.is_flagged = True
                    analysis.flag_reasons.append(
                        f"안전성 주의 (Safety={safety_info.safety})"
                    )

                print(
                    f"[{fetch_count}/{max_fetch}] {ingredient}: Safety={safety_info.safety}"
                )
            else:
                print(f"[{fetch_count}/{max_fetch}] {ingredient}: Not found")

        # 분류
        if analysis.safety_level == "safe":
            safe_list.append(ingredient)
        elif analysis.safety_level == "moderate":
            moderate_list.append(ingredient)
        elif analysis.safety_level == "concern":
            concern_list.append(ingredient)

        analyses.append(analysis)

    # 전체 안전성 평가
    overall_safety = "safe"
    if concern_list:
        overall_safety = "concern"
    elif moderate_list or irritants:
        overall_safety = "moderate"

    # 민감성 피부 적합성 평가
    sensitive_suitable = len(irritants) == 0 and len(concern_list) == 0

    # 요약 및 권장사항 생성
    summary = _generate_summary(
        len(ingredients),
        fetch_count,
        safe_list,
        moderate_list,
        concern_list,
        irritants,
        acne_triggers,
    )

    recommendations = _generate_recommendations(
        concern_list, irritants, acne_triggers, sensitive_suitable
    )

    return SafetyAnalysisResult(
        total_count=len(ingredients),
        analyzed_count=fetch_count,
        skipped_count=skipped_count,
        safe_ingredients=safe_list,
        moderate_ingredients=moderate_list,
        concern_ingredients=concern_list,
        acne_triggers=acne_triggers,
        irritants=irritants,
        ingredients=[asdict(a) for a in analyses],
        overall_safety=overall_safety,
        sensitive_skin_suitable=sensitive_suitable,
        summary=summary,
        recommendations=recommendations,
    )


def _generate_summary(
    total: int,
    analyzed: int,
    safe: list,
    moderate: list,
    concern: list,
    irritants: list,
    acne_triggers: list,
) -> str:
    """분석 요약 생성"""
    parts = [f"총 {total}개 성분 중 {analyzed}개 분석"]

    if concern:
        parts.append(f"주의 성분 {len(concern)}개")
    if irritants:
        parts.append(f"자극 성분 {len(irritants)}개")
    if acne_triggers:
        parts.append(f"여드름 유발 성분 {len(acne_triggers)}개")
    if not concern and not irritants:
        parts.append("전반적으로 안전")

    return " | ".join(parts)


def _generate_recommendations(
    concern: list, irritants: list, acne_triggers: list, sensitive_suitable: bool
) -> list:
    """권장사항 생성"""
    recommendations = []

    if concern:
        recommendations.append(f"주의 성분 확인 필요: {', '.join(concern[:3])}")

    if irritants:
        recommendations.append(f"민감성 피부 주의: {', '.join(irritants[:3])} 포함")

    if acne_triggers:
        recommendations.append(
            f"여드름성 피부 주의: {', '.join(acne_triggers[:3])} 포함"
        )

    if sensitive_suitable:
        recommendations.append("민감성 피부에 적합한 처방")

    if not recommendations:
        recommendations.append("특별한 주의 사항 없음")

    return recommendations


def quick_safety_check(full_ingredients: str) -> dict:
    """
    빠른 안전성 체크 (CosDNA 조회 없이)

    알려진 자극 성분만 체크
    """
    ingredients = parse_ingredients(full_ingredients)

    flagged = []
    for ingredient in ingredients:
        slug = to_slug(ingredient)
        if is_known_irritant(slug):
            flagged.append(ingredient)

    return {
        "total": len(ingredients),
        "flagged_count": len(flagged),
        "flagged_ingredients": flagged,
        "sensitive_skin_caution": len(flagged) > 0,
    }


# CLI 지원
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="전성분 안전성 분석")
    parser.add_argument("--input", "-i", required=True, help="전성분 텍스트")
    parser.add_argument("--fetch", "-f", action="store_true", help="CosDNA 조회")
    parser.add_argument("--max", "-m", type=int, default=10, help="최대 조회 수")
    parser.add_argument("--output", "-o", choices=["json", "text"], default="text")

    args = parser.parse_args()

    if args.fetch:
        result = analyze_ingredients_safety(
            args.input, fetch_details=True, max_fetch=args.max
        )

        if args.output == "json":
            print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
        else:
            print(f"\n{'=' * 50}")
            print(f"안전성 분석 결과")
            print(f"{'=' * 50}")
            print(f"총 성분: {result.total_count}")
            print(f"분석됨: {result.analyzed_count}")
            print(f"전체 평가: {result.overall_safety}")
            print(f"민감성 피부 적합: {result.sensitive_skin_suitable}")
            print(f"\n[요약]")
            print(f"  {result.summary}")
            print(f"\n[권장사항]")
            for rec in result.recommendations:
                print(f"  - {rec}")
            if result.concern_ingredients:
                print(f"\n[주의 성분]")
                for ing in result.concern_ingredients[:5]:
                    print(f"  ! {ing}")
    else:
        result = quick_safety_check(args.input)
        print(json.dumps(result, indent=2, ensure_ascii=False))
