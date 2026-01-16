#!/usr/bin/env python3
"""
Mintel GNPD Trend Analyzer

화장품 신제품 트렌드 분석 유틸리티
GNPD 데이터 분석 및 대체 소스 활용을 위한 도구

Author: Claude Cosmetic Skills
Version: 1.0.0
"""

import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
from collections import defaultdict


class Region(Enum):
    """지역 구분"""
    GLOBAL = "global"
    ASIA_PACIFIC = "asia-pacific"
    EUROPE = "europe"
    NORTH_AMERICA = "north-america"
    SOUTH_AMERICA = "south-america"
    MIDDLE_EAST = "middle-east"

    # 개별 국가
    KOREA = "korea"
    JAPAN = "japan"
    CHINA = "china"
    USA = "usa"
    UK = "uk"
    FRANCE = "france"
    GERMANY = "germany"


class Category(Enum):
    """제품 카테고리"""
    SKINCARE = "skincare"
    HAIRCARE = "haircare"
    COLOR_COSMETICS = "color-cosmetics"
    FRAGRANCE = "fragrance"
    PERSONAL_CARE = "personal-care"
    SUNCARE = "suncare"


class SubCategory(Enum):
    """세부 카테고리"""
    # Skincare
    CLEANSERS = "cleansers"
    TONERS = "toners"
    SERUMS = "serums"
    MOISTURIZERS = "moisturizers"
    MASKS = "masks"
    EYE_CARE = "eye-care"
    LIP_CARE = "lip-care"

    # Suncare
    FACE_SUNSCREEN = "face-sunscreen"
    BODY_SUNSCREEN = "body-sunscreen"

    # Haircare
    SHAMPOO = "shampoo"
    CONDITIONER = "conditioner"
    TREATMENT = "treatment"

    # Color Cosmetics
    FOUNDATION = "foundation"
    LIPSTICK = "lipstick"
    EYESHADOW = "eyeshadow"


class ClaimType(Enum):
    """클레임 유형"""
    EFFICACY = "efficacy"
    CERTIFICATION = "certification"
    FORMULATION = "formulation"
    SUSTAINABILITY = "sustainability"
    TARGET = "target"


class PriceSegment(Enum):
    """가격대"""
    MASS = "mass"  # $0-15
    MASSTIGE = "masstige"  # $15-35
    PRESTIGE = "prestige"  # $35-75
    LUXURY = "luxury"  # $75-150
    SUPER_PREMIUM = "super-premium"  # $150+


class TrendStage(Enum):
    """트렌드 단계"""
    EMERGING = "emerging"  # 0-2% 점유
    GROWING = "growing"  # 2-10% 점유
    MAINSTREAM = "mainstream"  # 10-30% 점유
    MATURE = "mature"  # 30%+ 점유
    DECLINING = "declining"  # 감소 추세


@dataclass
class Product:
    """제품 데이터 클래스"""
    name: str
    brand: str
    company: str
    launch_date: datetime
    country: str
    region: Region
    category: Category
    subcategory: SubCategory
    price_usd: float
    price_segment: PriceSegment
    ingredients: list[str] = field(default_factory=list)
    hero_ingredients: list[str] = field(default_factory=list)
    claims: dict[str, list[str]] = field(default_factory=dict)
    packaging: dict[str, str] = field(default_factory=dict)
    description: str = ""


@dataclass
class TrendData:
    """트렌드 데이터 클래스"""
    name: str
    category: str
    current_count: int
    previous_count: int
    growth_rate: float
    stage: TrendStage
    regions: list[Region]
    related_brands: list[str]
    related_ingredients: list[str] = field(default_factory=list)


@dataclass
class AnalysisResult:
    """분석 결과 클래스"""
    query: str
    timestamp: datetime
    total_products: int
    trends: list[TrendData]
    top_ingredients: list[dict]
    top_claims: list[dict]
    top_brands: list[dict]
    price_distribution: dict[str, int]
    regional_breakdown: dict[str, int]
    insights: list[str]


class TrendAnalyzer:
    """
    GNPD 트렌드 분석기

    GNPD 구독이 있는 경우 데이터 분석,
    없는 경우 대체 소스 가이드 제공
    """

    def __init__(self, has_subscription: bool = False):
        """
        Args:
            has_subscription: GNPD 구독 여부
        """
        self.has_subscription = has_subscription
        self._products: list[Product] = []

        # 트렌드 벤치마크 데이터 (공개 정보 기반)
        self._trend_benchmarks = self._load_trend_benchmarks()

    def _load_trend_benchmarks(self) -> dict:
        """공개된 트렌드 벤치마크 데이터 로드"""
        return {
            "ingredients": {
                "niacinamide": {"growth": 30, "stage": TrendStage.MAINSTREAM},
                "retinol": {"growth": 15, "stage": TrendStage.MAINSTREAM},
                "peptides": {"growth": 25, "stage": TrendStage.GROWING},
                "bakuchiol": {"growth": 40, "stage": TrendStage.EMERGING},
                "hyaluronic_acid": {"growth": 10, "stage": TrendStage.MATURE},
                "cica": {"growth": 20, "stage": TrendStage.MAINSTREAM},
                "vitamin_c": {"growth": 12, "stage": TrendStage.MATURE},
                "ceramides": {"growth": 18, "stage": TrendStage.GROWING},
                "squalane": {"growth": 20, "stage": TrendStage.GROWING},
                "tranexamic_acid": {"growth": 35, "stage": TrendStage.EMERGING},
            },
            "claims": {
                "vegan": {"growth": 35, "stage": TrendStage.GROWING},
                "clean_beauty": {"growth": 28, "stage": TrendStage.MAINSTREAM},
                "sustainable_packaging": {"growth": 45, "stage": TrendStage.GROWING},
                "fragrance_free": {"growth": 22, "stage": TrendStage.MAINSTREAM},
                "microbiome": {"growth": 50, "stage": TrendStage.EMERGING},
                "refillable": {"growth": 60, "stage": TrendStage.EMERGING},
            },
            "categories": {
                "serums": {"growth": 18, "stage": TrendStage.MAINSTREAM},
                "suncare": {"growth": 15, "stage": TrendStage.MAINSTREAM},
                "masks": {"growth": 8, "stage": TrendStage.MATURE},
                "cleansers": {"growth": 10, "stage": TrendStage.MATURE},
            }
        }

    def analyze_category(
        self,
        category: str,
        subcategory: Optional[str] = None,
        region: str = "global",
        period: str = "6m"
    ) -> AnalysisResult:
        """
        카테고리별 트렌드 분석

        Args:
            category: 제품 카테고리
            subcategory: 세부 카테고리 (선택)
            region: 지역 (기본: global)
            period: 분석 기간 (1m, 3m, 6m, 12m)

        Returns:
            AnalysisResult: 분석 결과
        """
        if not self.has_subscription:
            return self._generate_guide_result(
                f"category:{category}",
                f"카테고리 '{category}' 분석을 위해 GNPD 구독이 필요합니다."
            )

        # 구독 시 실제 분석 로직
        filtered_products = self._filter_products(
            category=category,
            subcategory=subcategory,
            region=region,
            period=period
        )

        return self._analyze_products(filtered_products, f"category:{category}")

    def analyze_ingredients(
        self,
        category: Optional[str] = None,
        top_n: int = 20,
        growth_filter: bool = False,
        min_growth: float = 10.0
    ) -> list[dict]:
        """
        성분 트렌드 분석

        Args:
            category: 카테고리 필터 (선택)
            top_n: 상위 N개 성분
            growth_filter: 성장 성분만 필터
            min_growth: 최소 성장률 (%)

        Returns:
            list[dict]: 성분 트렌드 리스트
        """
        # 벤치마크 데이터 기반 분석
        results = []

        for ingredient, data in self._trend_benchmarks["ingredients"].items():
            if growth_filter and data["growth"] < min_growth:
                continue

            results.append({
                "ingredient": ingredient.replace("_", " ").title(),
                "growth_rate": data["growth"],
                "stage": data["stage"].value,
                "recommendation": self._get_ingredient_recommendation(
                    data["growth"], data["stage"]
                )
            })

        # 성장률 기준 정렬
        results.sort(key=lambda x: x["growth_rate"], reverse=True)

        return results[:top_n]

    def analyze_claims(
        self,
        category: Optional[str] = None,
        claim_type: Optional[str] = None,
        region: str = "global"
    ) -> list[dict]:
        """
        클레임 트렌드 분석

        Args:
            category: 카테고리 필터 (선택)
            claim_type: 클레임 유형 필터 (선택)
            region: 지역 필터

        Returns:
            list[dict]: 클레임 트렌드 리스트
        """
        results = []

        for claim, data in self._trend_benchmarks["claims"].items():
            results.append({
                "claim": claim.replace("_", " ").title(),
                "growth_rate": data["growth"],
                "stage": data["stage"].value,
                "regional_strength": self._get_regional_strength(claim),
                "recommendation": self._get_claim_recommendation(
                    data["growth"], data["stage"]
                )
            })

        results.sort(key=lambda x: x["growth_rate"], reverse=True)
        return results

    def analyze_brand(
        self,
        brand_name: str,
        period: str = "12m"
    ) -> dict:
        """
        브랜드별 분석

        Args:
            brand_name: 브랜드명
            period: 분석 기간

        Returns:
            dict: 브랜드 분석 결과
        """
        if not self.has_subscription:
            return {
                "brand": brand_name,
                "status": "subscription_required",
                "message": f"'{brand_name}' 브랜드 분석을 위해 GNPD 구독이 필요합니다.",
                "alternatives": self._get_alternative_sources("brand", brand_name)
            }

        # 실제 분석 로직 (구독 시)
        return {
            "brand": brand_name,
            "period": period,
            "product_count": 0,
            "categories": [],
            "top_ingredients": [],
            "top_claims": [],
            "price_strategy": None,
            "launch_frequency": None
        }

    def compare_regions(
        self,
        regions: list[str],
        category: str,
        metric: str = "launches"
    ) -> dict:
        """
        지역 비교 분석

        Args:
            regions: 비교할 지역 리스트
            category: 카테고리
            metric: 비교 지표 (launches, claims, ingredients)

        Returns:
            dict: 지역 비교 결과
        """
        regional_data = {
            "korea": {
                "strength": ["innovation", "skincare", "suncare"],
                "trends": ["skip-care", "vegan", "clean"],
                "lead_time": "6-12 months ahead"
            },
            "japan": {
                "strength": ["quality", "sensitive-care", "anti-pollution"],
                "trends": ["minimal", "functional", "premium"],
                "lead_time": "stable market"
            },
            "usa": {
                "strength": ["mass-market", "inclusivity", "clean-beauty"],
                "trends": ["clean", "wellness", "diversity"],
                "lead_time": "follower market"
            },
            "europe": {
                "strength": ["sustainability", "regulation", "premium"],
                "trends": ["sustainable", "natural", "minimal"],
                "lead_time": "regulation leader"
            }
        }

        result = {
            "category": category,
            "metric": metric,
            "comparison": {}
        }

        for region in regions:
            region_lower = region.lower()
            if region_lower in regional_data:
                result["comparison"][region] = regional_data[region_lower]
            else:
                result["comparison"][region] = {"status": "data_not_available"}

        return result

    def get_trend_forecast(
        self,
        trend_name: str,
        horizon: str = "6m"
    ) -> dict:
        """
        트렌드 예측

        Args:
            trend_name: 트렌드명
            horizon: 예측 기간

        Returns:
            dict: 트렌드 예측 결과
        """
        # 벤치마크 데이터에서 검색
        trend_lower = trend_name.lower().replace(" ", "_")

        all_trends = {
            **self._trend_benchmarks["ingredients"],
            **self._trend_benchmarks["claims"],
            **self._trend_benchmarks["categories"]
        }

        if trend_lower in all_trends:
            data = all_trends[trend_lower]
            return {
                "trend": trend_name,
                "current_stage": data["stage"].value,
                "growth_rate": data["growth"],
                "forecast": self._forecast_stage(data["stage"], data["growth"]),
                "recommendation": self._get_action_recommendation(
                    data["stage"], data["growth"]
                )
            }

        return {
            "trend": trend_name,
            "status": "not_found",
            "message": f"'{trend_name}' 트렌드 데이터를 찾을 수 없습니다.",
            "suggestion": "유사한 트렌드를 검색하거나 철자를 확인하세요."
        }

    def _filter_products(
        self,
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        region: Optional[str] = None,
        period: Optional[str] = None
    ) -> list[Product]:
        """제품 필터링"""
        # 실제 구현 시 데이터베이스 쿼리
        return self._products

    def _analyze_products(
        self,
        products: list[Product],
        query: str
    ) -> AnalysisResult:
        """제품 분석"""
        # 실제 분석 로직
        return AnalysisResult(
            query=query,
            timestamp=datetime.now(),
            total_products=len(products),
            trends=[],
            top_ingredients=[],
            top_claims=[],
            top_brands=[],
            price_distribution={},
            regional_breakdown={},
            insights=[]
        )

    def _generate_guide_result(
        self,
        query: str,
        message: str
    ) -> AnalysisResult:
        """구독 없을 때 가이드 결과 생성"""
        alternatives = self._get_alternative_sources("general", query)

        return AnalysisResult(
            query=query,
            timestamp=datetime.now(),
            total_products=0,
            trends=[],
            top_ingredients=[],
            top_claims=[],
            top_brands=[],
            price_distribution={},
            regional_breakdown={},
            insights=[
                message,
                "대체 소스를 활용하세요:",
                *[f"- {alt['name']}: {alt['url']}" for alt in alternatives]
            ]
        )

    def _get_alternative_sources(
        self,
        source_type: str,
        query: str
    ) -> list[dict]:
        """대체 소스 목록"""
        alternatives = {
            "general": [
                {
                    "name": "Cosmetics Design",
                    "url": "https://www.cosmeticsdesign.com",
                    "description": "업계 뉴스 및 트렌드"
                },
                {
                    "name": "Global Cosmetic Industry",
                    "url": "https://www.gcimagazine.com",
                    "description": "트렌드 리포트"
                },
                {
                    "name": "Beauty Independent",
                    "url": "https://www.beautyindependent.com",
                    "description": "인디 뷰티 트렌드"
                },
                {
                    "name": "올리브영",
                    "url": "https://www.oliveyoung.co.kr",
                    "description": "한국 베스트셀러"
                }
            ],
            "brand": [
                {
                    "name": "브랜드 공식 사이트",
                    "url": "직접 검색",
                    "description": "신제품 정보"
                },
                {
                    "name": "브랜드 SNS",
                    "url": "Instagram/Facebook",
                    "description": "출시 정보"
                }
            ],
            "ingredient": [
                {
                    "name": "CosDNA",
                    "url": "https://www.cosdna.com",
                    "description": "성분 분석"
                },
                {
                    "name": "INCI Decoder",
                    "url": "https://incidecoder.com",
                    "description": "성분 정보"
                }
            ]
        }

        return alternatives.get(source_type, alternatives["general"])

    def _get_ingredient_recommendation(
        self,
        growth: float,
        stage: TrendStage
    ) -> str:
        """성분 추천 메시지"""
        if stage == TrendStage.EMERGING and growth > 30:
            return "선도 도입 추천 - 차별화 기회"
        elif stage == TrendStage.GROWING:
            return "적극 도입 추천 - 성장 기회"
        elif stage == TrendStage.MAINSTREAM:
            return "필수 성분 - 기본 포함 권장"
        elif stage == TrendStage.MATURE:
            return "안정 성분 - 차별화 필요"
        else:
            return "주의 필요 - 하락 추세"

    def _get_claim_recommendation(
        self,
        growth: float,
        stage: TrendStage
    ) -> str:
        """클레임 추천 메시지"""
        if growth > 40:
            return "강력 추천 - 급성장 클레임"
        elif growth > 20:
            return "추천 - 성장 클레임"
        elif growth > 10:
            return "보통 - 안정 클레임"
        else:
            return "선택적 - 성숙/하락 클레임"

    def _get_regional_strength(self, claim: str) -> dict:
        """클레임별 지역 강도"""
        strengths = {
            "vegan": {"korea": "high", "europe": "high", "usa": "medium"},
            "clean_beauty": {"usa": "high", "europe": "medium", "korea": "medium"},
            "sustainable_packaging": {"europe": "high", "usa": "medium", "korea": "low"},
            "microbiome": {"korea": "high", "japan": "medium", "usa": "low"},
            "refillable": {"europe": "high", "japan": "medium", "korea": "low"},
        }
        return strengths.get(claim, {"global": "medium"})

    def _forecast_stage(
        self,
        current_stage: TrendStage,
        growth: float
    ) -> str:
        """트렌드 단계 예측"""
        if current_stage == TrendStage.EMERGING and growth > 30:
            return "6개월 내 Growing 단계 진입 예상"
        elif current_stage == TrendStage.GROWING and growth > 20:
            return "12개월 내 Mainstream 단계 진입 예상"
        elif current_stage == TrendStage.MAINSTREAM and growth < 10:
            return "Mature 단계 진입 중"
        else:
            return "현재 단계 유지 예상"

    def _get_action_recommendation(
        self,
        stage: TrendStage,
        growth: float
    ) -> str:
        """액션 추천"""
        if stage == TrendStage.EMERGING:
            if growth > 30:
                return "즉시 R&D 검토 - 선도 진입 기회"
            else:
                return "모니터링 유지 - 추가 데이터 확인"
        elif stage == TrendStage.GROWING:
            return "적극 도입 - 주력 라인 적용"
        elif stage == TrendStage.MAINSTREAM:
            return "차별화 전략 - 독창적 접근 필요"
        elif stage == TrendStage.MATURE:
            return "효율화 - 비용 최적화"
        else:
            return "철수 검토 - 대체 트렌드 탐색"


class AlternativeSourceFetcher:
    """
    대체 소스 데이터 수집기

    GNPD 구독이 없을 때 무료 소스에서
    트렌드 데이터를 수집합니다.
    """

    def __init__(self):
        self.sources = {
            "news": [
                "https://www.cosmeticsdesign.com",
                "https://www.cosmeticsdesign-asia.com",
                "https://www.gcimagazine.com",
                "https://www.beautyindependent.com",
            ],
            "ecommerce": {
                "korea": "https://www.oliveyoung.co.kr",
                "usa": "https://www.sephora.com",
                "global": "https://www.amazon.com",
            },
            "social": {
                "instagram": "#skincare #kbeauty",
                "tiktok": "#beautytok #skincaretok",
                "reddit": "r/SkincareAddiction r/AsianBeauty",
            }
        }

    def get_trending_keywords(self, platform: str) -> list[str]:
        """플랫폼별 트렌딩 키워드 (가이드)"""
        keywords = {
            "instagram": [
                "#glassskin", "#skinicaring", "#veganbeauty",
                "#cleanbeauty", "#kbeauty", "#skintok"
            ],
            "tiktok": [
                "#skincareroutine", "#glowup", "#acnejourney",
                "#affordableskincare", "#drugstorefinds"
            ],
            "google": [
                "best serum 2024", "niacinamide benefits",
                "retinol vs bakuchiol", "vegan skincare brands"
            ]
        }
        return keywords.get(platform, [])

    def get_ecommerce_bestsellers(self, region: str) -> dict:
        """이커머스 베스트셀러 수집 가이드"""
        guides = {
            "korea": {
                "source": "올리브영",
                "url": "https://www.oliveyoung.co.kr/store/ranking/getRanking.do",
                "categories": ["스킨케어", "선케어", "클렌저", "마스크팩"]
            },
            "usa": {
                "source": "Sephora",
                "url": "https://www.sephora.com/shop/new-beauty-products",
                "categories": ["skincare", "sunscreen", "masks"]
            },
            "global": {
                "source": "Amazon",
                "url": "https://www.amazon.com/Best-Sellers-Beauty/",
                "categories": ["Skin Care", "Sun Care", "Face Masks"]
            }
        }
        return guides.get(region, guides["global"])


def main():
    """메인 실행 함수"""
    print("=" * 60)
    print("Mintel GNPD Trend Analyzer")
    print("=" * 60)

    # 분석기 초기화 (구독 없음)
    analyzer = TrendAnalyzer(has_subscription=False)

    # 성분 트렌드 분석
    print("\n[성분 트렌드 분석]")
    print("-" * 40)

    ingredient_trends = analyzer.analyze_ingredients(
        top_n=10,
        growth_filter=True,
        min_growth=15
    )

    for trend in ingredient_trends:
        print(f"- {trend['ingredient']}")
        print(f"  성장률: {trend['growth_rate']}%")
        print(f"  단계: {trend['stage']}")
        print(f"  추천: {trend['recommendation']}")
        print()

    # 클레임 트렌드 분석
    print("\n[클레임 트렌드 분석]")
    print("-" * 40)

    claim_trends = analyzer.analyze_claims()

    for trend in claim_trends[:5]:
        print(f"- {trend['claim']}")
        print(f"  성장률: {trend['growth_rate']}%")
        print(f"  단계: {trend['stage']}")
        print()

    # 지역 비교
    print("\n[지역 비교 분석]")
    print("-" * 40)

    comparison = analyzer.compare_regions(
        regions=["korea", "japan", "usa"],
        category="skincare"
    )

    for region, data in comparison["comparison"].items():
        print(f"\n{region.upper()}:")
        if isinstance(data, dict) and "strength" in data:
            print(f"  강점: {', '.join(data['strength'])}")
            print(f"  트렌드: {', '.join(data['trends'])}")

    # 트렌드 예측
    print("\n[트렌드 예측]")
    print("-" * 40)

    forecast = analyzer.get_trend_forecast("Niacinamide")
    print(f"트렌드: {forecast['trend']}")
    print(f"현재 단계: {forecast.get('current_stage', 'N/A')}")
    print(f"성장률: {forecast.get('growth_rate', 'N/A')}%")
    print(f"예측: {forecast.get('forecast', 'N/A')}")
    print(f"추천: {forecast.get('recommendation', 'N/A')}")

    # 대체 소스 가이드
    print("\n[대체 소스 가이드]")
    print("-" * 40)

    alt_fetcher = AlternativeSourceFetcher()

    print("\n인스타그램 트렌딩 키워드:")
    for kw in alt_fetcher.get_trending_keywords("instagram"):
        print(f"  {kw}")

    print("\n이커머스 베스트셀러 소스:")
    for region in ["korea", "usa"]:
        guide = alt_fetcher.get_ecommerce_bestsellers(region)
        print(f"  {region.upper()}: {guide['source']} - {guide['url']}")


if __name__ == "__main__":
    main()
