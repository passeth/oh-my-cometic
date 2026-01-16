#!/usr/bin/env python3
"""
CosDNA 성분 안전성 정보 스크래핑 모듈

검증 완료:
- SSR 기반 (requests로 접근 가능)
- 다국어 지원 (영어, 한국어, 일본어, 중국어)
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import json
from typing import Optional, List
from dataclasses import dataclass, asdict


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

BASE_URL = "https://www.cosdna.com"


@dataclass
class SearchResult:
    """검색 결과"""

    name: str
    ingredient_id: str
    url: str
    has_safety: bool = False


@dataclass
class IngredientSafety:
    """성분 안전성 정보"""

    name: str
    aliases: List[str]
    cas_no: str
    formula: str
    molecular_weight: str
    safety: Optional[int]
    acne: Optional[int]
    irritant: Optional[int]
    function: str
    url: str
    error: Optional[str] = None


def search_ingredient(query: str, lang: str = "eng") -> List[SearchResult]:
    """
    CosDNA 성분 검색

    Args:
        query: 검색어 (성분명)
        lang: 언어 코드 (eng, kor, jpn, cht, chs)

    Returns:
        SearchResult 리스트
    """
    url = f"{BASE_URL}/{lang}/stuff.php?q={query}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    # 검색 결과 리스트에서 성분 추출
    items = soup.select('ul.divide-y li a[href*=".html"]')

    for item in items:
        href = item.get("href", "")
        # /eng/af81356377.html 형태에서 ID 추출
        match = re.search(r"/(\w+)\.html$", href)
        if match:
            ingredient_id = match.group(1)
            name_elem = item.select_one("span")
            name = (
                name_elem.get_text(strip=True)
                if name_elem
                else item.get_text(strip=True)
            )

            # 안전성 점수 존재 여부 확인
            has_safety = bool(item.select_one("i.iconify"))

            results.append(
                SearchResult(
                    name=name,
                    ingredient_id=ingredient_id,
                    url=f"{BASE_URL}/{lang}/{ingredient_id}.html",
                    has_safety=has_safety,
                )
            )

    return results


def get_ingredient_safety(ingredient_id: str, lang: str = "eng") -> IngredientSafety:
    """
    CosDNA 성분 상세 정보 조회

    Args:
        ingredient_id: 성분 ID (예: "af81356377")
        lang: 언어 코드

    Returns:
        IngredientSafety 데이터클래스
    """
    url = f"{BASE_URL}/{lang}/{ingredient_id}.html"

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        return IngredientSafety(
            name="",
            aliases=[],
            cas_no="",
            formula="",
            molecular_weight="",
            safety=None,
            acne=None,
            irritant=None,
            function="",
            url=url,
            error=str(e),
        )

    soup = BeautifulSoup(response.text, "html.parser")

    # 성분명 추출
    h1 = soup.find("h1")
    name = h1.get_text(strip=True) if h1 else ""

    # 별칭 추출
    aliases = []
    alias_div = soup.select_one("h1 + div.mt-2")
    if alias_div:
        alias_text = alias_div.get_text(strip=True)
        if alias_text:
            aliases = [a.strip() for a in alias_text.split(",")]

    # 화학 정보 추출
    cas_no = ""
    formula = ""
    molecular_weight = ""

    info_spans = soup.select("span.bg-stone-100")
    for span in info_spans:
        text = span.get_text()
        if "Cas No" in text:
            cas_no = text.split(":")[-1].strip()
        elif "Formula" in text:
            formula = text.replace("Formula:", "").strip()
        elif "Molecular Weight" in text:
            molecular_weight = text.replace("Molecular Weight:", "").strip()

    # 안전성 점수 추출
    safety = _extract_score(soup, "Safety")
    acne = _extract_score(soup, "Acne")
    irritant = _extract_score(soup, "Irritant")

    # 기능 추출
    function = ""
    func_div = soup.select_one("div.linkb1.tracking-wider")
    if func_div:
        function = func_div.get_text(strip=True)

    return IngredientSafety(
        name=name,
        aliases=aliases,
        cas_no=cas_no,
        formula=formula,
        molecular_weight=molecular_weight,
        safety=safety,
        acne=acne,
        irritant=irritant,
        function=function,
        url=url,
    )


def _extract_score(soup: BeautifulSoup, score_type: str) -> Optional[int]:
    """안전성 점수 추출"""
    # 점수 타입별 div 찾기
    score_divs = soup.select("div.border.rounded")

    for div in score_divs:
        label = div.find("div")
        if label and score_type in label.get_text():
            # 점수 span 찾기
            score_span = div.select_one('span.safety, span[class*="safety"]')
            if score_span:
                score_text = score_span.get_text(strip=True)
                try:
                    return int(score_text)
                except ValueError:
                    pass

    return None


def search_and_get_safety(
    query: str, lang: str = "eng", delay: float = 1.0
) -> Optional[IngredientSafety]:
    """
    성분명으로 검색 후 첫 번째 결과의 안전성 정보 반환

    Args:
        query: 검색어 (성분명)
        lang: 언어 코드
        delay: 검색과 상세 조회 사이 간격 (초)

    Returns:
        IngredientSafety 또는 None
    """
    results = search_ingredient(query, lang)

    if not results:
        return None

    time.sleep(delay)
    return get_ingredient_safety(results[0].ingredient_id, lang)


def batch_search_safety(
    ingredients: List[str], lang: str = "eng", delay: float = 1.5
) -> List[IngredientSafety]:
    """
    여러 성분 일괄 안전성 조회

    Args:
        ingredients: 성분명 리스트
        lang: 언어 코드
        delay: 요청 간 간격 (초)

    Returns:
        IngredientSafety 리스트
    """
    results = []

    for i, ingredient in enumerate(ingredients):
        if i > 0:
            time.sleep(delay)

        safety = search_and_get_safety(ingredient, lang, delay=0.5)

        if safety:
            results.append(safety)
            status = f"Safety={safety.safety}" if safety.safety else "No score"
        else:
            status = "Not found"

        print(f"[{i + 1}/{len(ingredients)}] {ingredient}: {status}")

    return results


# CLI 지원
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CosDNA 성분 안전성 조회")
    parser.add_argument("--ingredient", "-i", required=True, help="성분명")
    parser.add_argument("--lang", "-l", default="eng", help="언어 (eng, kor, jpn)")
    parser.add_argument("--output", "-o", choices=["json", "text"], default="text")

    args = parser.parse_args()

    safety = search_and_get_safety(args.ingredient, args.lang)

    if args.output == "json":
        if safety:
            print(json.dumps(asdict(safety), indent=2, ensure_ascii=False))
        else:
            print(json.dumps({"error": "Not found"}, indent=2))
    else:
        if safety and not safety.error:
            print(f"Name: {safety.name}")
            print(f"Aliases: {', '.join(safety.aliases[:3])}")
            print(f"CAS No: {safety.cas_no}")
            print(f"Safety: {safety.safety}")
            print(f"Acne: {safety.acne}")
            print(f"Irritant: {safety.irritant}")
            print(f"Function: {safety.function}")
        else:
            print(f"Not found or error: {safety.error if safety else 'No results'}")
