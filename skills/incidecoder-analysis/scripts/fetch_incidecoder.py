#!/usr/bin/env python3
"""
INCIDecoder 성분 정보 스크래핑 모듈

검증 완료:
- SSR 기반 (requests로 접근 가능)
- JavaScript 렌더링 불필요
- HTML 응답에 모든 콘텐츠 포함
"""

import requests
from bs4 import BeautifulSoup
import time
import re
import json
from typing import Optional
from dataclasses import dataclass, asdict


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

BASE_URL = "https://incidecoder.com"
RATING_VALUES = ["Superstar", "Goodie", "OK", "Icky"]


@dataclass
class ProductInfo:
    """농도 명시 제품 정보"""

    name: str
    brand: str
    concentration: str
    url: Optional[str] = None


@dataclass
class IngredientInfo:
    """성분 정보 구조체"""

    url: str
    name: str
    rating: str
    also_called: list
    functions: list
    quick_facts: list
    geeky_details: str
    products_known: list
    other_products: list
    error: Optional[str] = None


def to_slug(ingredient_name: str) -> str:
    """
    성분명을 URL slug로 변환

    Args:
        ingredient_name: 원본 성분명 (예: "Ceramide NP")

    Returns:
        URL용 slug (예: "ceramide-np")
    """
    slug = ingredient_name.lower().strip()
    # 특수문자 제거 (알파벳, 숫자, 공백, 하이픈만 유지)
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    # 연속 공백 → 단일 하이픈
    slug = re.sub(r"\s+", "-", slug)
    # 연속 하이픈 정리
    slug = re.sub(r"-+", "-", slug)
    # 앞뒤 하이픈 제거
    slug = slug.strip("-")
    return slug


def get_ingredient_info(slug: str) -> IngredientInfo:
    """
    INCIDecoder 성분 정보 수집

    Args:
        slug: URL용 성분명 (예: "niacinamide")

    Returns:
        IngredientInfo 데이터클래스
    """
    url = f"{BASE_URL}/ingredients/{slug}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)

        if response.status_code == 404:
            return IngredientInfo(
                url=url,
                name="",
                rating="",
                also_called=[],
                functions=[],
                quick_facts=[],
                geeky_details="",
                products_known=[],
                other_products=[],
                error=f"Not found: {slug}",
            )

        response.raise_for_status()

    except requests.RequestException as e:
        return IngredientInfo(
            url=url,
            name="",
            rating="",
            also_called=[],
            functions=[],
            quick_facts=[],
            geeky_details="",
            products_known=[],
            other_products=[],
            error=str(e),
        )

    soup = BeautifulSoup(response.text, "html.parser")

    return IngredientInfo(
        url=url,
        name=_extract_name(soup),
        rating=_extract_rating(soup),
        also_called=_extract_aliases(soup),
        functions=_extract_functions(soup),
        quick_facts=_extract_quick_facts(soup),
        geeky_details=_extract_geeky_details(soup),
        products_known=_extract_products_with_concentration(soup),
        other_products=_extract_other_products(soup),
    )


def _extract_name(soup: BeautifulSoup) -> str:
    """<h1> 태그에서 성분명 추출"""
    h1 = soup.find("h1")
    if h1:
        return h1.get_text(strip=True)
    return ""


def _extract_rating(soup: BeautifulSoup) -> str:
    """성분 등급 추출 (Superstar, Goodie, OK, Icky)"""
    # h1 인근에서 등급 텍스트 찾기
    h1 = soup.find("h1")
    if not h1:
        return ""

    # h1의 부모 또는 형제 요소에서 등급 찾기
    parent = h1.parent
    if parent:
        text = parent.get_text()
        for rating in RATING_VALUES:
            if rating in text:
                return rating

    # 전체 페이지에서 등급 클래스나 텍스트 찾기
    for rating in RATING_VALUES:
        # 클래스명으로 찾기
        elem = soup.find(
            class_=lambda x: x and rating.lower() in x.lower() if x else False
        )
        if elem:
            return rating

        # 텍스트로 찾기 (h1 이후 첫 번째 섹션 내)
        rating_span = soup.find("span", string=rating)
        if rating_span:
            return rating

    return ""


def _extract_aliases(soup: BeautifulSoup) -> list:
    """
    동의어/별칭 추출
    "ALSO-CALLED-LIKE-THIS" 또는 유사 섹션에서 추출
    """
    aliases = []

    # id로 찾기
    section = soup.find(id="also-called-like-this")
    if section:
        text = section.get_text(separator=", ", strip=True)
        aliases = [a.strip() for a in text.split(",") if a.strip()]
        return aliases

    # 텍스트 패턴으로 찾기
    headers = soup.find_all(["h2", "h3", "div", "span"])
    for header in headers:
        if header.get_text(strip=True).lower() in [
            "also-called-like-this",
            "also called",
        ]:
            # 다음 형제 또는 자식에서 별칭 추출
            sibling = header.find_next_sibling()
            if sibling:
                text = sibling.get_text(separator=", ", strip=True)
                aliases = [a.strip() for a in text.split(",") if a.strip()]
                break

    return aliases


def _extract_functions(soup: BeautifulSoup) -> list:
    """
    기능 태그 추출
    "WHAT-IT-DOES" 섹션의 링크 텍스트들
    """
    functions = []

    # id로 찾기
    section = soup.find(id="what-it-does")
    if section:
        links = section.find_all("a")
        functions = [
            link.get_text(strip=True) for link in links if link.get_text(strip=True)
        ]
        return functions

    # 텍스트 패턴으로 찾기
    headers = soup.find_all(["h2", "h3", "div", "span"])
    for header in headers:
        header_text = header.get_text(strip=True).lower()
        if "what-it-does" in header_text or "what it does" in header_text:
            parent = header.parent
            if parent:
                links = parent.find_all("a")
                functions = [
                    link.get_text(strip=True)
                    for link in links
                    if link.get_text(strip=True)
                ]
                break

    return functions


def _extract_quick_facts(soup: BeautifulSoup) -> list:
    """
    Quick Facts 섹션의 핵심 효능 요약 추출
    """
    facts = []

    # "Quick Facts" h2 찾기
    h2_tags = soup.find_all("h2")
    for h2 in h2_tags:
        if "Quick Facts" in h2.get_text():
            # 다음 ul 태그 찾기
            next_ul = h2.find_next("ul")
            if next_ul:
                li_tags = next_ul.find_all("li")
                facts = [li.get_text(strip=True) for li in li_tags]
            break

    return facts


def _extract_geeky_details(soup: BeautifulSoup) -> str:
    """
    Geeky Details 섹션의 상세 설명 추출
    """
    h2_tags = soup.find_all("h2")
    for h2 in h2_tags:
        if "Geeky Details" in h2.get_text():
            # h2 이후 다음 h2 전까지의 모든 p 태그 수집
            details = []
            for sibling in h2.find_next_siblings():
                if sibling.name == "h2":
                    break
                if sibling.name == "p":
                    details.append(sibling.get_text(strip=True))
            return " ".join(details)

    return ""


def _extract_products_with_concentration(soup: BeautifulSoup) -> list:
    """
    농도가 명시된 제품 목록 추출
    "Products with a known amount of [성분]" 섹션
    """
    products = []

    # "Products with a known amount" 텍스트 찾기
    h2_tags = soup.find_all("h2")
    for h2 in h2_tags:
        if "Products with a known amount" in h2.get_text():
            # 해당 섹션 내 제품 카드 찾기
            section = h2.parent
            if section:
                # 제품 링크들 찾기
                product_links = section.find_all("a", href=re.compile(r"/products/"))

                for link in product_links[:20]:  # 최대 20개
                    product_text = link.get_text(strip=True)
                    href = link.get("href", "")

                    # 농도 정보 찾기 (보통 제품명에 포함)
                    concentration = ""
                    conc_match = re.search(r"(\d+(?:\.\d+)?%)", product_text)
                    if conc_match:
                        concentration = conc_match.group(1)

                    # 브랜드 추출 (첫 단어 또는 대시 전까지)
                    brand = (
                        product_text.split(" - ")[0]
                        if " - " in product_text
                        else product_text.split()[0]
                    )

                    products.append(
                        asdict(
                            ProductInfo(
                                name=product_text,
                                brand=brand,
                                concentration=concentration,
                                url=f"{BASE_URL}{href}"
                                if href.startswith("/")
                                else href,
                            )
                        )
                    )
            break

    return products


def _extract_other_products(soup: BeautifulSoup) -> list:
    """
    기타 해당 성분 포함 제품 목록 추출
    "Other products with [성분]" 섹션
    """
    products = []

    h2_tags = soup.find_all("h2")
    for h2 in h2_tags:
        if "Other products with" in h2.get_text():
            section = h2.parent
            if section:
                product_links = section.find_all("a", href=re.compile(r"/products/"))
                products = [link.get_text(strip=True) for link in product_links[:30]]
            break

    return products


def search_ingredient(query: str, delay: float = 1.0) -> IngredientInfo:
    """
    성분명으로 검색 (slug 변환 후 조회)

    Args:
        query: 검색할 성분명 (예: "Niacinamide", "Ceramide NP")
        delay: 이전 요청과의 간격 (초)

    Returns:
        IngredientInfo 데이터클래스
    """
    time.sleep(delay)  # Rate limiting
    slug = to_slug(query)
    return get_ingredient_info(slug)


def batch_search(ingredients: list, delay: float = 1.0) -> list:
    """
    여러 성분 일괄 검색

    Args:
        ingredients: 성분명 리스트
        delay: 요청 간 간격 (초)

    Returns:
        IngredientInfo 리스트
    """
    results = []
    for i, ingredient in enumerate(ingredients):
        if i > 0:
            time.sleep(delay)
        result = get_ingredient_info(to_slug(ingredient))
        results.append(result)
        print(
            f"[{i + 1}/{len(ingredients)}] {ingredient}: {result.rating or result.error}"
        )

    return results


# CLI 지원
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="INCIDecoder 성분 정보 조회")
    parser.add_argument(
        "--ingredient", "-i", required=True, help="성분명 (예: niacinamide)"
    )
    parser.add_argument(
        "--output", "-o", choices=["json", "text"], default="text", help="출력 형식"
    )

    args = parser.parse_args()

    info = search_ingredient(
        args.ingredient, delay=0
    )  # CLI는 단일 요청이므로 delay 불필요

    if args.output == "json":
        print(json.dumps(asdict(info), indent=2, ensure_ascii=False))
    else:
        if info.error:
            print(f"Error: {info.error}")
        else:
            print(f"Name: {info.name}")
            print(f"Rating: {info.rating}")
            print(f"Also Called: {', '.join(info.also_called[:5])}")
            print(f"Functions: {', '.join(info.functions)}")
            print(f"Quick Facts:")
            for fact in info.quick_facts[:3]:
                print(f"  - {fact[:100]}...")
            print(f"Products with known concentration: {len(info.products_known)}")
            print(f"Other products: {len(info.other_products)}")
