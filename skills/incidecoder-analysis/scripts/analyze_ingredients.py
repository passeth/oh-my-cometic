#!/usr/bin/env python3
"""
전성분 분석 모듈

전성분 리스트를 파싱하고 INCIDecoder 데이터를 기반으로
핵심 활성 성분 분류, 경쟁 제품 벤치마킹 인사이트 도출
"""

import re
import time
import json
from typing import Optional
from dataclasses import dataclass, asdict, field

from fetch_incidecoder import get_ingredient_info, to_slug, IngredientInfo


# 핵심 활성 성분 분류 (slug 기준)
KEY_ACTIVES = {
    "brightening": [
        "niacinamide",
        "arbutin",
        "alpha-arbutin",
        "tranexamic-acid",
        "ascorbic-acid",
        "vitamin-c",
        "ascorbyl-glucoside",
        "3-o-ethyl-ascorbic-acid",
        "magnesium-ascorbyl-phosphate",
        "sodium-ascorbyl-phosphate",
        "ascorbyl-tetraisopalmitate",
        "kojic-acid",
        "licorice-root-extract",
        "glutathione",
    ],
    "anti_aging": [
        "retinol",
        "retinal",
        "retinaldehyde",
        "adenosine",
        "retinyl-palmitate",
        "retinyl-acetate",
        "hydroxypinacolone-retinoate",
        "bakuchiol",
        "peptide",
        "palmitoyl-tripeptide",
        "palmitoyl-tetrapeptide",
        "matrixyl",
        "argireline",
        "copper-peptide",
        "epidermal-growth-factor",
        "coenzyme-q10",
        "ubiquinone",
        "resveratrol",
    ],
    "exfoliating": [
        "salicylic-acid",
        "glycolic-acid",
        "lactic-acid",
        "mandelic-acid",
        "azelaic-acid",
        "pha",
        "gluconolactone",
        "lactobionic-acid",
        "citric-acid",
        "malic-acid",
        "tartaric-acid",
        "polyhydroxy-acid",
        "bha",
        "aha",
    ],
    "soothing": [
        "centella-asiatica",
        "madecassoside",
        "asiaticoside",
        "panthenol",
        "allantoin",
        "bisabolol",
        "cica",
        "mugwort",
        "artemisia",
        "chamomile",
        "calendula",
        "aloe-vera",
        "green-tea",
        "licorice",
        "oat",
        "colloidal-oatmeal",
    ],
    "hydrating": [
        "hyaluronic-acid",
        "sodium-hyaluronate",
        "ceramide",
        "ceramide-np",
        "ceramide-ap",
        "ceramide-eop",
        "ceramide-ng",
        "ceramide-ns",
        "squalane",
        "squalene",
        "glycerin",
        "beta-glucan",
        "polyglutamic-acid",
        "trehalose",
        "urea",
        "sodium-pca",
        "honey",
        "propolis",
        "lecithin",
        "cholesterol",
    ],
    "antioxidant": [
        "vitamin-e",
        "tocopherol",
        "tocotrienol",
        "ferulic-acid",
        "astaxanthin",
        "lycopene",
        "grape-seed-extract",
        "green-tea-extract",
        "superoxide-dismutase",
    ],
    "acne_care": [
        "salicylic-acid",
        "benzoyl-peroxide",
        "tea-tree",
        "zinc",
        "sulfur",
        "azelaic-acid",
        "niacinamide",
    ],
}

# 분석 제외 베이스/보조 성분
BASE_INGREDIENTS = [
    "water",
    "aqua",
    "butylene-glycol",
    "propanediol",
    "1-2-hexanediol",
    "pentylene-glycol",
    "glycerin",
    "dimethicone",
    "cyclomethicone",
    "cyclopentasiloxane",
    "carbomer",
    "xanthan-gum",
    "acrylates",
    "phenoxyethanol",
    "ethylhexylglycerin",
    "chlorphenesin",
    "disodium-edta",
    "sodium-hydroxide",
    "triethanolamine",
    "fragrance",
    "parfum",
    "citric-acid",
]


@dataclass
class IngredientAnalysis:
    """개별 성분 분석 결과"""

    name: str
    slug: str
    position: int  # 전성분 내 순서 (1부터 시작)
    rating: str
    categories: list  # 분류된 카테고리들
    is_key_active: bool
    is_base: bool
    functions: list
    error: Optional[str] = None


@dataclass
class FullAnalysisResult:
    """전성분 분석 전체 결과"""

    total_count: int
    key_actives_count: int
    base_count: int
    analyzed_count: int

    # 카테고리별 핵심 성분
    by_category: dict = field(default_factory=dict)

    # 전체 성분 분석 결과
    ingredients: list = field(default_factory=list)

    # 기획 인사이트
    insights: list = field(default_factory=list)

    # 오류
    errors: list = field(default_factory=list)


def parse_ingredients(full_ingredients: str) -> list:
    """
    전성분 텍스트를 파싱하여 성분 리스트로 변환

    Args:
        full_ingredients: 쉼표로 구분된 전성분 텍스트

    Returns:
        정제된 성분명 리스트 (순서 유지)
    """
    # 괄호 내용 제거 (예: "Niacinamide (Vitamin B3)" → "Niacinamide")
    text = re.sub(r"\([^)]*\)", "", full_ingredients)

    # 쉼표, 세미콜론, 슬래시로 분리
    ingredients = re.split(r"[,;/]", text)

    # 정제
    result = []
    for ing in ingredients:
        cleaned = ing.strip()
        # 빈 문자열 및 숫자만 있는 경우 제외
        if cleaned and not cleaned.isdigit():
            result.append(cleaned)

    return result


def classify_ingredient(slug: str) -> list:
    """
    성분을 카테고리로 분류

    Args:
        slug: 성분 slug

    Returns:
        해당하는 카테고리 리스트
    """
    categories = []
    for category, slugs in KEY_ACTIVES.items():
        # 완전 일치 또는 부분 일치
        for active_slug in slugs:
            if active_slug in slug or slug in active_slug:
                categories.append(category)
                break

    return list(set(categories))


def is_base_ingredient(slug: str) -> bool:
    """베이스/보조 성분 여부 확인"""
    for base in BASE_INGREDIENTS:
        if base in slug or slug in base:
            return True
    return False


def analyze_full_ingredients(
    full_ingredients: str,
    fetch_details: bool = True,
    delay: float = 1.0,
    max_fetch: int = 15,
) -> FullAnalysisResult:
    """
    전성분 분석 메인 함수

    Args:
        full_ingredients: 쉼표로 구분된 전성분 텍스트
        fetch_details: INCIDecoder에서 상세 정보 조회 여부
        delay: 요청 간 간격 (초)
        max_fetch: 최대 조회 성분 수

    Returns:
        FullAnalysisResult 데이터클래스
    """
    # 1. 파싱
    ingredients = parse_ingredients(full_ingredients)

    result = FullAnalysisResult(
        total_count=len(ingredients),
        key_actives_count=0,
        base_count=0,
        analyzed_count=0,
        by_category={cat: [] for cat in KEY_ACTIVES.keys()},
    )

    # 2. 각 성분 분석
    fetched = 0
    for i, name in enumerate(ingredients, start=1):
        slug = to_slug(name)
        categories = classify_ingredient(slug)
        is_base = is_base_ingredient(slug)
        is_key = len(categories) > 0 and not is_base

        analysis = IngredientAnalysis(
            name=name,
            slug=slug,
            position=i,
            rating="",
            categories=categories,
            is_key_active=is_key,
            is_base=is_base,
            functions=[],
        )

        # INCIDecoder 상세 조회 (핵심 성분만, 최대 개수 제한)
        if fetch_details and is_key and fetched < max_fetch:
            if fetched > 0:
                time.sleep(delay)

            info = get_ingredient_info(slug)
            fetched += 1

            if info.error:
                analysis.error = info.error
                result.errors.append(f"{name}: {info.error}")
            else:
                analysis.rating = info.rating
                analysis.functions = info.functions

            result.analyzed_count += 1

        # 카테고리별 분류
        if is_key:
            result.key_actives_count += 1
            for cat in categories:
                result.by_category[cat].append(
                    {
                        "name": name,
                        "position": i,
                        "rating": analysis.rating,
                        "slug": slug,
                    }
                )

        if is_base:
            result.base_count += 1

        result.ingredients.append(asdict(analysis))

    # 3. 인사이트 도출
    result.insights = _generate_insights(result)

    return result


def _generate_insights(result: FullAnalysisResult) -> list:
    """분석 결과 기반 기획 인사이트 생성"""
    insights = []

    # 카테고리 조합 분석
    active_categories = [cat for cat, items in result.by_category.items() if items]

    if len(active_categories) == 0:
        insights.append("핵심 활성 성분이 거의 없는 베이스 제품입니다.")
        return insights

    # 주요 컨셉 도출
    if "brightening" in active_categories and "anti_aging" in active_categories:
        insights.append("미백 + 안티에이징 멀티 기능성 컨셉")

    if "hydrating" in active_categories and "soothing" in active_categories:
        insights.append("진정 보습 컨셉 - 민감성 피부 타겟 가능")

    if "exfoliating" in active_categories:
        insights.append("각질 케어 포함 - 사용 빈도 가이드 필요")

    if "acne_care" in active_categories:
        insights.append("트러블 케어 성분 포함 - 여드름성 피부 타겟")

    # Superstar 성분 강조
    superstars = []
    for ing in result.ingredients:
        if ing.get("rating") == "Superstar":
            superstars.append(ing["name"])

    if superstars:
        insights.append(
            f"Superstar 등급 성분: {', '.join(superstars)} - 마케팅 포인트로 활용"
        )

    # 성분 순서 분석
    for cat, items in result.by_category.items():
        if items:
            top_item = min(items, key=lambda x: x["position"])
            if top_item["position"] <= 5:
                insights.append(
                    f"{cat} 성분({top_item['name']})이 상위 배합 - 고농도 기대"
                )

    # 성분 다양성 분석
    if result.key_actives_count >= 5:
        insights.append(
            f"다양한 핵심 성분({result.key_actives_count}개) - 올인원/멀티 기능 강조 가능"
        )

    return insights


def compare_products(products: dict) -> dict:
    """
    여러 제품 전성분 비교 분석

    Args:
        products: {"제품A": "전성분...", "제품B": "전성분..."}

    Returns:
        비교 분석 결과
    """
    analyses = {}
    all_actives = set()

    for name, ingredients in products.items():
        result = analyze_full_ingredients(ingredients, fetch_details=False)
        analyses[name] = result

        for ing in result.ingredients:
            if ing["is_key_active"]:
                all_actives.add(ing["slug"])

    # 공통 성분 vs 차별 성분
    comparison = {
        "products": list(products.keys()),
        "analyses": {k: asdict(v) for k, v in analyses.items()},
        "common_actives": [],
        "unique_actives": {name: [] for name in products.keys()},
    }

    for slug in all_actives:
        in_products = []
        for name, result in analyses.items():
            if any(ing["slug"] == slug for ing in result.ingredients):
                in_products.append(name)

        if len(in_products) == len(products):
            comparison["common_actives"].append(slug)
        else:
            for name in in_products:
                comparison["unique_actives"][name].append(slug)

    return comparison


# CLI 지원
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="전성분 분석")
    parser.add_argument("--input", "-i", required=True, help="전성분 텍스트")
    parser.add_argument("--fetch", action="store_true", help="INCIDecoder 상세 조회")
    parser.add_argument("--output", "-o", choices=["json", "text"], default="text")

    args = parser.parse_args()

    result = analyze_full_ingredients(args.input, fetch_details=args.fetch)

    if args.output == "json":
        print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
    else:
        print(f"\n=== 전성분 분석 결과 ===")
        print(f"총 성분 수: {result.total_count}")
        print(f"핵심 활성 성분: {result.key_actives_count}")
        print(f"베이스 성분: {result.base_count}")
        print(f"상세 조회: {result.analyzed_count}")

        print(f"\n--- 카테고리별 핵심 성분 ---")
        for cat, items in result.by_category.items():
            if items:
                names = [f"{x['name']}(#{x['position']})" for x in items]
                print(f"{cat}: {', '.join(names)}")

        print(f"\n--- 기획 인사이트 ---")
        for insight in result.insights:
            print(f"  - {insight}")

        if result.errors:
            print(f"\n--- 오류 ---")
            for err in result.errors:
                print(f"  ! {err}")
