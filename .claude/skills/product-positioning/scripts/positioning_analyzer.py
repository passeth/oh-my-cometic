#!/usr/bin/env python3
"""
Product Positioning Analyzer for Cosmetics

A comprehensive tool for analyzing and visualizing product positioning
in the cosmetic market. Supports competitive analysis, price-value mapping,
and positioning strategy development.

Author: claude-cosmetic-skills
Version: 1.0.0
"""

import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional
from datetime import datetime


class PriceTier(Enum):
    """Korean cosmetic market price tiers"""
    MASS_ENTRY = "mass_entry"
    MASS_PREMIUM = "mass_premium"
    MASSTIGE = "masstige"
    PRESTIGE = "prestige"
    LUXURY = "luxury"


class ProductCategory(Enum):
    """Standard cosmetic product categories"""
    CLEANSER = "cleanser"
    TONER = "toner"
    SERUM = "serum"
    ESSENCE = "essence"
    AMPOULE = "ampoule"
    EYE_CREAM = "eye_cream"
    MOISTURIZER = "moisturizer"
    SUNSCREEN = "sunscreen"
    MASK = "mask"
    LIP_CARE = "lip_care"
    BODY_CARE = "body_care"


@dataclass
class Product:
    """Represents a cosmetic product for positioning analysis"""
    name: str
    brand: str
    category: str
    price_krw: int
    size_ml: float
    key_ingredients: list[str] = field(default_factory=list)
    key_claims: list[str] = field(default_factory=list)
    target_age_min: int = 18
    target_age_max: int = 65
    target_concerns: list[str] = field(default_factory=list)
    launch_date: Optional[str] = None

    @property
    def price_per_ml(self) -> float:
        """Calculate price per ml"""
        if self.size_ml > 0:
            return self.price_krw / self.size_ml
        return 0

    def get_price_tier(self) -> PriceTier:
        """Determine price tier based on Korean market standards"""
        if self.price_krw < 10000:
            return PriceTier.MASS_ENTRY
        elif self.price_krw < 25000:
            return PriceTier.MASS_PREMIUM
        elif self.price_krw < 50000:
            return PriceTier.MASSTIGE
        elif self.price_krw < 100000:
            return PriceTier.PRESTIGE
        else:
            return PriceTier.LUXURY


@dataclass
class Competitor:
    """Represents a competitor brand or product"""
    name: str
    products: list[Product] = field(default_factory=list)
    market_share: float = 0.0
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    positioning_statement: str = ""
    primary_tier: Optional[str] = None


@dataclass
class PositioningAnalysis:
    """Complete positioning analysis result"""
    product: Product
    competitors: list[Competitor] = field(default_factory=list)
    price_index: float = 100.0
    positioning_statement: str = ""
    usp: str = ""
    differentiation_factors: list[str] = field(default_factory=list)
    white_space_opportunities: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    analysis_date: str = field(default_factory=lambda: datetime.now().isoformat())


class PositioningAnalyzer:
    """
    Main analyzer class for product positioning analysis.

    Provides methods for:
    - Competitive analysis
    - Price positioning assessment
    - White space identification
    - USP development
    - Positioning statement generation
    """

    # Korean market price tier boundaries (KRW)
    TIER_BOUNDARIES = {
        PriceTier.MASS_ENTRY: (0, 10000),
        PriceTier.MASS_PREMIUM: (10000, 25000),
        PriceTier.MASSTIGE: (25000, 50000),
        PriceTier.PRESTIGE: (50000, 100000),
        PriceTier.LUXURY: (100000, float('inf'))
    }

    # Reference brands by tier
    TIER_REFERENCE_BRANDS = {
        PriceTier.MASS_ENTRY: ["The Face Shop", "Missha", "Etude House", "Holika Holika"],
        PriceTier.MASS_PREMIUM: ["Innisfree", "Cosrx", "Some By Mi", "Klairs"],
        PriceTier.MASSTIGE: ["Laneige", "Mamonde", "Dr. Jart+", "AHC", "Primera"],
        PriceTier.PRESTIGE: ["Sulwhasoo", "Hera", "Ohui", "Su:m37"],
        PriceTier.LUXURY: ["Whoo", "Donginbi", "Sisley", "La Mer"]
    }

    def __init__(self):
        self.products: list[Product] = []
        self.competitors: list[Competitor] = []

    def add_product(self, product: Product) -> None:
        """Add a product to the analysis"""
        self.products.append(product)

    def add_competitor(self, competitor: Competitor) -> None:
        """Add a competitor to the analysis"""
        self.competitors.append(competitor)

    def calculate_price_index(self, product: Product, competitor_products: list[Product]) -> float:
        """
        Calculate price index relative to competitors.

        Price Index = (Product Price / Average Competitor Price) x 100

        Interpretation:
        - < 90: Aggressively priced
        - 90-95: Competitively priced
        - 95-105: Market-aligned
        - 105-115: Premium priced
        - > 115: Super-premium
        """
        if not competitor_products:
            return 100.0

        # Filter to same category for fair comparison
        same_category = [p for p in competitor_products if p.category == product.category]

        if not same_category:
            return 100.0

        avg_price = sum(p.price_krw for p in same_category) / len(same_category)

        if avg_price == 0:
            return 100.0

        return (product.price_krw / avg_price) * 100

    def identify_white_space(self, products: list[Product]) -> list[dict]:
        """
        Identify positioning white spaces based on price-value gaps.

        Returns list of opportunities with price ranges and positioning suggestions.
        """
        opportunities = []

        if not products:
            return opportunities

        # Sort products by price
        sorted_products = sorted(products, key=lambda p: p.price_krw)

        # Look for gaps between adjacent products
        for i in range(len(sorted_products) - 1):
            current = sorted_products[i]
            next_product = sorted_products[i + 1]

            price_gap = next_product.price_krw - current.price_krw
            gap_percentage = (price_gap / current.price_krw) * 100 if current.price_krw > 0 else 0

            # If gap is significant (>50% price difference), it's a potential opportunity
            if gap_percentage > 50:
                mid_price = (current.price_krw + next_product.price_krw) // 2
                opportunities.append({
                    "price_range": f"{current.price_krw:,} - {next_product.price_krw:,} KRW",
                    "suggested_price": mid_price,
                    "lower_reference": current.name,
                    "upper_reference": next_product.name,
                    "positioning_suggestion": f"Position between {current.brand} and {next_product.brand} with enhanced value proposition"
                })

        # Check for unoccupied tier opportunities
        occupied_tiers = set(p.get_price_tier() for p in products)
        for tier in PriceTier:
            if tier not in occupied_tiers:
                low, high = self.TIER_BOUNDARIES[tier]
                opportunities.append({
                    "tier": tier.value,
                    "price_range": f"{low:,} - {high:,} KRW" if high != float('inf') else f"{low:,}+ KRW",
                    "reference_brands": self.TIER_REFERENCE_BRANDS.get(tier, []),
                    "positioning_suggestion": f"Opportunity to enter {tier.value} tier market"
                })

        return opportunities

    def generate_positioning_statement(
        self,
        product: Product,
        target_description: str,
        key_insight: str,
        key_benefit: str,
        reason_to_believe: str,
        competitor_differentiation: str
    ) -> str:
        """
        Generate a positioning statement using the standard framework.

        Template:
        FOR [target segment] WHO [key insight],
        [Product] IS THE [category] THAT [key benefit]
        BECAUSE [reason to believe].
        UNLIKE [competitor differentiation].
        """
        return f"""FOR {target_description}
WHO {key_insight},
{product.name} IS THE {product.category}
THAT {key_benefit}
BECAUSE {reason_to_believe}.
UNLIKE competitors, {competitor_differentiation}."""

    def develop_usp(
        self,
        product: Product,
        unique_features: list[str],
        competitor_gaps: list[str]
    ) -> dict:
        """
        Develop Unique Selling Proposition based on product features and competitor analysis.

        Returns a structured USP recommendation.
        """
        # Categorize features
        functional_benefits = []
        emotional_benefits = []

        functional_keywords = ["효과", "성분", "기술", "특허", "임상", "efficacy", "ingredient", "technology"]
        emotional_keywords = ["느낌", "감성", "자신감", "행복", "feel", "confidence", "luxury", "pleasure"]

        for feature in unique_features:
            feature_lower = feature.lower()
            if any(kw in feature_lower for kw in functional_keywords):
                functional_benefits.append(feature)
            elif any(kw in feature_lower for kw in emotional_keywords):
                emotional_benefits.append(feature)
            else:
                functional_benefits.append(feature)  # Default to functional

        # Generate USP components
        usp_structure = {
            "product_name": product.name,
            "primary_benefit": functional_benefits[0] if functional_benefits else "Superior quality",
            "secondary_benefit": emotional_benefits[0] if emotional_benefits else "Enhanced experience",
            "proof_points": unique_features[:3],
            "competitive_advantage": competitor_gaps[0] if competitor_gaps else "Unique positioning",
            "suggested_tagline": self._generate_tagline(product, functional_benefits, emotional_benefits)
        }

        return usp_structure

    def _generate_tagline(
        self,
        product: Product,
        functional_benefits: list[str],
        emotional_benefits: list[str]
    ) -> list[str]:
        """Generate tagline suggestions based on benefits"""
        taglines = []

        # Functional-focused tagline
        if functional_benefits:
            taglines.append(f"Experience {functional_benefits[0].split()[0]} results with {product.name}")

        # Emotional-focused tagline
        if emotional_benefits:
            taglines.append(f"Feel {emotional_benefits[0].split()[0]} every day")

        # Balanced tagline
        taglines.append(f"{product.brand}: Where science meets beauty")

        return taglines

    def analyze_competitive_landscape(
        self,
        target_product: Product,
        competitor_products: list[Product]
    ) -> dict:
        """
        Comprehensive competitive landscape analysis.

        Returns detailed competitive positioning insights.
        """
        if not competitor_products:
            return {"error": "No competitor products provided"}

        # Calculate metrics
        price_index = self.calculate_price_index(target_product, competitor_products)
        target_tier = target_product.get_price_tier()

        # Segment competitors
        same_tier_competitors = [
            p for p in competitor_products
            if p.get_price_tier() == target_tier
        ]

        adjacent_tier_competitors = [
            p for p in competitor_products
            if abs(list(PriceTier).index(p.get_price_tier()) -
                   list(PriceTier).index(target_tier)) == 1
        ]

        # Calculate positioning metrics
        avg_competitor_price = (
            sum(p.price_krw for p in same_tier_competitors) / len(same_tier_competitors)
            if same_tier_competitors else 0
        )

        price_position = "premium" if target_product.price_krw > avg_competitor_price else "value"

        # Ingredient overlap analysis
        all_competitor_ingredients = set()
        for comp in competitor_products:
            all_competitor_ingredients.update(comp.key_ingredients)

        unique_ingredients = set(target_product.key_ingredients) - all_competitor_ingredients
        common_ingredients = set(target_product.key_ingredients) & all_competitor_ingredients

        return {
            "target_product": {
                "name": target_product.name,
                "brand": target_product.brand,
                "price": target_product.price_krw,
                "tier": target_tier.value
            },
            "competitive_metrics": {
                "price_index": round(price_index, 1),
                "price_position": price_position,
                "avg_competitor_price": round(avg_competitor_price),
                "same_tier_competitor_count": len(same_tier_competitors),
                "adjacent_tier_competitor_count": len(adjacent_tier_competitors)
            },
            "differentiation_analysis": {
                "unique_ingredients": list(unique_ingredients),
                "common_ingredients": list(common_ingredients),
                "differentiation_score": len(unique_ingredients) / max(len(target_product.key_ingredients), 1) * 100
            },
            "recommendations": self._generate_recommendations(
                price_index, price_position, unique_ingredients, same_tier_competitors
            )
        }

    def _generate_recommendations(
        self,
        price_index: float,
        price_position: str,
        unique_ingredients: set,
        same_tier_competitors: list[Product]
    ) -> list[str]:
        """Generate strategic recommendations based on analysis"""
        recommendations = []

        # Price-based recommendations
        if price_index > 115:
            recommendations.append(
                "Consider strengthening value justification - price index suggests super-premium positioning"
            )
        elif price_index < 90:
            recommendations.append(
                "Aggressive pricing may signal lower quality - consider slight price increase with value communication"
            )

        # Differentiation recommendations
        if len(unique_ingredients) == 0:
            recommendations.append(
                "Low ingredient differentiation - consider adding unique hero ingredient or technology"
            )
        elif len(unique_ingredients) >= 3:
            recommendations.append(
                "Strong ingredient differentiation - emphasize unique formulation in positioning"
            )

        # Competitive density recommendations
        if len(same_tier_competitors) > 5:
            recommendations.append(
                "High competitive density in tier - focus on sharp differentiation and niche targeting"
            )
        elif len(same_tier_competitors) < 2:
            recommendations.append(
                "Low competition in tier - opportunity for category leadership positioning"
            )

        return recommendations

    def generate_full_analysis(self, product: Product) -> PositioningAnalysis:
        """
        Generate complete positioning analysis for a product.

        Returns a comprehensive PositioningAnalysis object.
        """
        # Gather competitor products
        all_competitor_products = []
        for competitor in self.competitors:
            all_competitor_products.extend(competitor.products)

        # Calculate metrics
        price_index = self.calculate_price_index(product, all_competitor_products)
        white_spaces = self.identify_white_space(all_competitor_products + [product])

        # Generate insights
        competitive_analysis = self.analyze_competitive_landscape(product, all_competitor_products)

        # Build analysis result
        analysis = PositioningAnalysis(
            product=product,
            competitors=self.competitors,
            price_index=price_index,
            white_space_opportunities=[ws.get("positioning_suggestion", "") for ws in white_spaces],
            recommendations=competitive_analysis.get("recommendations", [])
        )

        return analysis

    def export_analysis(self, analysis: PositioningAnalysis, format: str = "json") -> str:
        """Export analysis results in specified format"""
        if format == "json":
            return json.dumps(asdict(analysis), indent=2, ensure_ascii=False, default=str)
        elif format == "markdown":
            return self._format_as_markdown(analysis)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _format_as_markdown(self, analysis: PositioningAnalysis) -> str:
        """Format analysis as markdown report"""
        product = analysis.product

        md = f"""# Product Positioning Analysis Report

## Product Overview
- **Name**: {product.name}
- **Brand**: {product.brand}
- **Category**: {product.category}
- **Price**: {product.price_krw:,} KRW
- **Size**: {product.size_ml}ml
- **Price/ml**: {product.price_per_ml:,.0f} KRW
- **Price Tier**: {product.get_price_tier().value.replace('_', ' ').title()}

## Competitive Position
- **Price Index**: {analysis.price_index:.1f}
  - Interpretation: {"Super-premium" if analysis.price_index > 115 else "Premium" if analysis.price_index > 105 else "Market-aligned" if analysis.price_index > 95 else "Competitive" if analysis.price_index > 90 else "Aggressive"}

## Positioning Statement
{analysis.positioning_statement or "Not yet developed"}

## Unique Selling Proposition
{analysis.usp or "Not yet developed"}

## Differentiation Factors
{chr(10).join(f"- {factor}" for factor in analysis.differentiation_factors) or "- None identified"}

## White Space Opportunities
{chr(10).join(f"- {opp}" for opp in analysis.white_space_opportunities) or "- None identified"}

## Recommendations
{chr(10).join(f"1. {rec}" for i, rec in enumerate(analysis.recommendations)) or "- No specific recommendations"}

---
*Analysis Date: {analysis.analysis_date}*
*Generated by Product Positioning Analyzer*
"""
        return md


def demo():
    """Demonstrate the positioning analyzer capabilities"""

    # Initialize analyzer
    analyzer = PositioningAnalyzer()

    # Create sample product
    our_product = Product(
        name="Glow Vitamin C Serum",
        brand="GlowLab",
        category="serum",
        price_krw=38000,
        size_ml=30,
        key_ingredients=["15% Vitamin C", "Niacinamide", "Hyaluronic Acid", "Centella Asiatica"],
        key_claims=["Brightening", "Anti-oxidant", "Hydrating"],
        target_age_min=25,
        target_age_max=40,
        target_concerns=["Dullness", "Dark spots", "Uneven tone"]
    )

    # Create competitor products
    competitor_a = Product(
        name="Freshly Juiced Vitamin C Serum",
        brand="Klairs",
        category="serum",
        price_krw=23000,
        size_ml=35,
        key_ingredients=["5% Vitamin C", "Centella Asiatica"],
        key_claims=["Gentle brightening", "Sensitive skin friendly"]
    )

    competitor_b = Product(
        name="Galactomyces Pure Vitamin C Glow Serum",
        brand="Some By Mi",
        category="serum",
        price_krw=18000,
        size_ml=30,
        key_ingredients=["10% Vitamin C", "Galactomyces", "Niacinamide"],
        key_claims=["Brightening", "Pore care"]
    )

    competitor_c = Product(
        name="Pure Vitamin C 21.5 Advanced Serum",
        brand="By Wishtrend",
        category="serum",
        price_krw=28000,
        size_ml=30,
        key_ingredients=["21.5% Vitamin C", "Hippophae Rhamnoides"],
        key_claims=["High concentration", "Rapid brightening"]
    )

    # Add to analyzer
    competitor = Competitor(
        name="K-Beauty Vitamin C Brands",
        products=[competitor_a, competitor_b, competitor_c],
        strengths=["Established brands", "Strong online presence"],
        weaknesses=["Lower concentration", "Less stability"]
    )

    analyzer.add_competitor(competitor)

    # Run analysis
    print("=" * 60)
    print("PRODUCT POSITIONING ANALYSIS DEMO")
    print("=" * 60)

    # Basic metrics
    print(f"\nProduct: {our_product.name}")
    print(f"Price Tier: {our_product.get_price_tier().value}")
    print(f"Price/ml: {our_product.price_per_ml:,.0f} KRW")

    # Competitive analysis
    all_competitors = [competitor_a, competitor_b, competitor_c]
    landscape = analyzer.analyze_competitive_landscape(our_product, all_competitors)

    print("\n--- Competitive Landscape ---")
    print(f"Price Index: {landscape['competitive_metrics']['price_index']}")
    print(f"Position: {landscape['competitive_metrics']['price_position']}")
    print(f"Same Tier Competitors: {landscape['competitive_metrics']['same_tier_competitor_count']}")

    print("\n--- Differentiation ---")
    print(f"Unique Ingredients: {landscape['differentiation_analysis']['unique_ingredients']}")
    print(f"Differentiation Score: {landscape['differentiation_analysis']['differentiation_score']:.0f}%")

    print("\n--- Recommendations ---")
    for i, rec in enumerate(landscape['recommendations'], 1):
        print(f"{i}. {rec}")

    # White space analysis
    white_spaces = analyzer.identify_white_space(all_competitors + [our_product])
    print("\n--- White Space Opportunities ---")
    for ws in white_spaces[:3]:  # Show top 3
        print(f"- {ws.get('positioning_suggestion', ws.get('tier', 'Opportunity'))}")

    # Generate positioning statement
    positioning = analyzer.generate_positioning_statement(
        product=our_product,
        target_description="skincare-conscious millennials (25-40)",
        key_insight="want visible brightening results without irritation from high-concentration vitamin C",
        key_benefit="delivers clinical-grade brightening with a gentle, stabilized formula",
        reason_to_believe="our patented encapsulation technology maintains 15% vitamin C potency while minimizing irritation",
        competitor_differentiation="our formula combines effective concentration with skin-friendly delivery, eliminating the trade-off between efficacy and gentleness"
    )

    print("\n--- Positioning Statement ---")
    print(positioning)

    # Full analysis export
    analysis = analyzer.generate_full_analysis(our_product)
    analysis.positioning_statement = positioning
    analysis.usp = "Effective brightening without irritation - the best of both worlds"
    analysis.differentiation_factors = [
        "15% stabilized vitamin C (higher than most K-beauty competitors)",
        "Patented encapsulation technology",
        "Multi-benefit formula (brightening + hydrating + soothing)"
    ]

    print("\n--- Full Analysis (Markdown) ---")
    print(analyzer.export_analysis(analysis, format="markdown"))


if __name__ == "__main__":
    demo()
