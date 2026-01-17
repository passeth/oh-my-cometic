"""
Cosmily Web Client Module
Cosmily 화장품 성분 데이터베이스 웹 클라이언트

Usage:
    from cosmily_client import CosmilyClient

    client = CosmilyClient()
    result = client.search_ingredient("NIACINAMIDE")
    print(result)

Note:
    Cosmily does not provide an official API.
    This module uses web scraping to extract data.
    Please respect rate limits and terms of service.
"""

import requests
from bs4 import BeautifulSoup
import re
import sqlite3
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Union, List, Dict, Any
from dataclasses import dataclass, asdict, field
from functools import wraps
from enum import Enum
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# Enums and Constants
# ============================================================================

class SafetyGrade(Enum):
    """Safety grade enumeration"""
    A = "A"  # Excellent
    B = "B"  # Good
    C = "C"  # Average
    D = "D"  # Below Average
    F = "F"  # Poor
    UNKNOWN = "?"


class CompatibilityStatus(Enum):
    """Ingredient compatibility status"""
    COMPATIBLE = "Compatible"
    CAUTION = "Caution"
    INCOMPATIBLE = "Incompatible"
    UNKNOWN = "Unknown"


# ============================================================================
# Data Models
# ============================================================================

@dataclass
class SafetyRating:
    """Safety rating data class"""
    grade: SafetyGrade
    score: int = 0
    description: str = ""
    concerns: List[str] = field(default_factory=list)

    def is_safe(self) -> bool:
        """Check if rating is considered safe (A or B)"""
        return self.grade in [SafetyGrade.A, SafetyGrade.B]

    def to_dict(self) -> dict:
        return {
            "grade": self.grade.value,
            "score": self.score,
            "description": self.description,
            "concerns": self.concerns
        }


@dataclass
class IngredientInfo:
    """Cosmily ingredient information"""
    inci_name: str
    slug: str = ""
    common_names: List[str] = field(default_factory=list)
    cas_number: Optional[str] = None
    ec_number: Optional[str] = None

    # Safety
    safety_rating: Optional[SafetyRating] = None
    comedogenic_rating: int = 0
    irritancy_rating: int = 0

    # Functionality
    functions: List[str] = field(default_factory=list)
    benefits: List[str] = field(default_factory=list)
    concerns: List[str] = field(default_factory=list)

    # Usage
    recommended_concentration: Dict[str, float] = field(default_factory=dict)
    description: str = ""

    # Metadata
    url: str = ""
    last_updated: Optional[str] = None

    def __post_init__(self):
        if not self.slug:
            self.slug = self._generate_slug(self.inci_name)

    @staticmethod
    def _generate_slug(name: str) -> str:
        """Generate URL slug from ingredient name"""
        return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

    def to_dict(self) -> dict:
        data = asdict(self)
        if self.safety_rating:
            data['safety_rating'] = self.safety_rating.to_dict()
        return data

    def get_grade(self) -> str:
        """Get safety grade letter"""
        if self.safety_rating:
            return self.safety_rating.grade.value
        return "?"

    def get_score(self) -> int:
        """Get safety score"""
        if self.safety_rating:
            return self.safety_rating.score
        return 0


@dataclass
class FormulaAnalysis:
    """Formula analysis result"""
    overall_grade: SafetyGrade
    overall_score: int
    ingredients: List[Dict[str, Any]] = field(default_factory=list)
    flagged_ingredients: List[Dict[str, Any]] = field(default_factory=list)
    function_coverage: Dict[str, List[str]] = field(default_factory=dict)
    compatibility_issues: List[Dict[str, Any]] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "overall_grade": self.overall_grade.value,
            "overall_score": self.overall_score,
            "ingredients": self.ingredients,
            "flagged_ingredients": self.flagged_ingredients,
            "function_coverage": self.function_coverage,
            "compatibility_issues": self.compatibility_issues,
            "suggestions": self.suggestions
        }


@dataclass
class CompatibilityResult:
    """Compatibility check result"""
    ingredients: List[str]
    status: CompatibilityStatus
    can_use_together: bool
    recommendation: str = ""
    reason: str = ""
    tips: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "ingredients": self.ingredients,
            "status": self.status.value,
            "can_use_together": self.can_use_together,
            "recommendation": self.recommendation,
            "reason": self.reason,
            "tips": self.tips
        }


# ============================================================================
# Cache System
# ============================================================================

class CosmilyCache:
    """Local cache system for Cosmily data"""

    DEFAULT_TTL = {
        "ingredient": 86400,      # 24 hours
        "search": 3600,           # 1 hour
        "compatibility": 86400,   # 24 hours
        "formula": 1800,          # 30 minutes
    }

    def __init__(self, db_path: Union[str, Path] = None):
        if db_path is None:
            db_path = Path.home() / '.cosmetic_skills' / 'cosmily_cache.db'

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.conn = sqlite3.connect(str(self.db_path))
        self._init_db()

    def _init_db(self):
        """Initialize database tables"""
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS cache (
                key TEXT PRIMARY KEY,
                value JSON NOT NULL,
                type TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_expires ON cache(expires_at);
            CREATE INDEX IF NOT EXISTS idx_type ON cache(type);
        """)
        self.conn.commit()

    def _generate_key(self, cache_type: str, identifier: str) -> str:
        """Generate cache key"""
        return f"cosmily:{cache_type}:{identifier.lower()}"

    def get(self, cache_type: str, identifier: str) -> Optional[dict]:
        """Get cached data"""
        key = self._generate_key(cache_type, identifier)

        cursor = self.conn.execute(
            "SELECT value FROM cache WHERE key = ? AND expires_at > ?",
            (key, datetime.now().isoformat())
        )
        row = cursor.fetchone()

        if row:
            return json.loads(row[0])
        return None

    def set(self, cache_type: str, identifier: str, data: dict, ttl: int = None):
        """Set cache data"""
        key = self._generate_key(cache_type, identifier)
        ttl = ttl or self.DEFAULT_TTL.get(cache_type, 3600)
        expires_at = datetime.now() + timedelta(seconds=ttl)

        self.conn.execute("""
            INSERT OR REPLACE INTO cache (key, value, type, created_at, expires_at)
            VALUES (?, ?, ?, ?, ?)
        """, (key, json.dumps(data, ensure_ascii=False), cache_type,
              datetime.now().isoformat(), expires_at.isoformat()))
        self.conn.commit()

    def clear_expired(self):
        """Remove expired cache entries"""
        self.conn.execute(
            "DELETE FROM cache WHERE expires_at < ?",
            (datetime.now().isoformat(),)
        )
        self.conn.commit()

    def clear_all(self):
        """Clear all cache"""
        self.conn.execute("DELETE FROM cache")
        self.conn.commit()

    def close(self):
        """Close database connection"""
        self.conn.close()


# ============================================================================
# Rate Limiting
# ============================================================================

def rate_limit(calls_per_minute: int = 20, min_delay: float = 3.0):
    """Rate limiting decorator"""
    min_interval = max(60.0 / calls_per_minute, min_delay)
    last_called = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                sleep_time = min_interval - elapsed
                logger.debug(f"Rate limiting: sleeping {sleep_time:.2f}s")
                time.sleep(sleep_time)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator


# ============================================================================
# Exceptions
# ============================================================================

class CosmilyError(Exception):
    """Base exception for Cosmily client"""
    pass


class IngredientNotFoundError(CosmilyError):
    """Ingredient not found in database"""
    pass


class RateLimitError(CosmilyError):
    """Rate limit exceeded"""
    pass


class ParseError(CosmilyError):
    """HTML parsing error"""
    pass


class ConnectionError(CosmilyError):
    """Network connection error"""
    pass


# ============================================================================
# Cosmily Client
# ============================================================================

class CosmilyClient:
    """Cosmily web client for ingredient data extraction"""

    BASE_URL = "https://cosmily.com"

    # CSS Selectors (estimated - may need updates)
    SELECTORS = {
        "inci_name": "h1.ingredient-name, .ingredient-header h1",
        "common_names": ".ingredient-aliases, .also-known-as",
        "cas_number": ".cas-number, [data-cas]",
        "safety_grade": ".safety-grade, .safety-badge",
        "safety_score": ".safety-score, .score-value",
        "comedogenic": ".comedogenic-rating .value, [data-comedogenic]",
        "irritancy": ".irritancy-rating .value, [data-irritancy]",
        "functions": ".function-list li, .functions .tag",
        "benefits": ".benefits-list li, .benefits p",
        "concerns": ".concerns-list li, .concerns p",
        "concentration_min": ".concentration .min",
        "concentration_max": ".concentration .max",
        "description": ".ingredient-description, .description p",
        "search_results": ".ingredient-card, .search-result",
    }

    # User agent rotation
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    ]

    def __init__(self, use_cache: bool = True, cache_path: str = None):
        """
        Initialize Cosmily client

        Args:
            use_cache: Enable local caching
            cache_path: Custom cache database path
        """
        self.session = requests.Session()
        self._user_agent_index = 0
        self._update_headers()

        self.use_cache = use_cache
        self.cache = CosmilyCache(cache_path) if use_cache else None

        # Known ingredient data for fallback
        self._sample_data = self._load_sample_data()

    def _update_headers(self):
        """Update request headers with rotating user agent"""
        self.session.headers.update({
            'User-Agent': self.USER_AGENTS[self._user_agent_index % len(self.USER_AGENTS)],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
        self._user_agent_index += 1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cache:
            self.cache.close()

    @rate_limit(calls_per_minute=20, min_delay=3.0)
    def _request(self, url: str, params: dict = None) -> requests.Response:
        """Make HTTP request with rate limiting"""
        self._update_headers()

        try:
            response = self.session.get(url, params=params, timeout=30)

            if response.status_code == 429:
                raise RateLimitError("Rate limit exceeded")
            elif response.status_code == 404:
                raise IngredientNotFoundError(f"Not found: {url}")
            elif response.status_code >= 400:
                raise CosmilyError(f"Request failed: {response.status_code}")

            return response

        except requests.exceptions.Timeout:
            raise ConnectionError("Request timed out")
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"Connection error: {e}")

    def _parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML content"""
        return BeautifulSoup(html, 'html.parser')

    def _extract_text(self, soup: BeautifulSoup, selector: str) -> Optional[str]:
        """Extract text from element"""
        element = soup.select_one(selector)
        return element.get_text(strip=True) if element else None

    def _extract_list(self, soup: BeautifulSoup, selector: str) -> List[str]:
        """Extract list of text from elements"""
        elements = soup.select(selector)
        return [el.get_text(strip=True) for el in elements if el.get_text(strip=True)]

    def _generate_slug(self, name: str) -> str:
        """Generate URL slug from name"""
        return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

    # ========================================================================
    # Public Methods
    # ========================================================================

    def search_ingredient(self, query: str, force_refresh: bool = False) -> Optional[IngredientInfo]:
        """
        Search for ingredient by name

        Args:
            query: INCI name, common name, or CAS number
            force_refresh: Skip cache and fetch fresh data

        Returns:
            IngredientInfo or None if not found
        """
        query_normalized = query.upper().strip()
        slug = self._generate_slug(query)

        # Check cache
        if self.use_cache and not force_refresh:
            cached = self.cache.get("ingredient", query_normalized)
            if cached:
                logger.info(f"Cache hit: {query_normalized}")
                return self._dict_to_ingredient(cached)

        # Try sample data first (for demo/offline)
        if query_normalized in self._sample_data:
            logger.info(f"Using sample data: {query_normalized}")
            return self._sample_data[query_normalized]

        # Fetch from web
        try:
            url = f"{self.BASE_URL}/ingredients/{slug}"
            response = self._request(url)
            soup = self._parse_html(response.text)

            ingredient = self._parse_ingredient_page(soup, url)

            # Cache result
            if ingredient and self.use_cache:
                self.cache.set("ingredient", query_normalized, ingredient.to_dict())

            return ingredient

        except IngredientNotFoundError:
            logger.warning(f"Ingredient not found: {query}")
            return None
        except Exception as e:
            logger.error(f"Error searching ingredient: {e}")
            return None

    def search_by_cas(self, cas_number: str) -> Optional[IngredientInfo]:
        """
        Search ingredient by CAS number

        Args:
            cas_number: CAS registry number (e.g., "98-92-0")

        Returns:
            IngredientInfo or None
        """
        if not self._validate_cas(cas_number):
            raise ValueError(f"Invalid CAS number format: {cas_number}")

        return self.search_ingredient(cas_number)

    def get_safety_rating(self, inci_name: str) -> Optional[SafetyRating]:
        """
        Get safety rating for ingredient

        Args:
            inci_name: INCI ingredient name

        Returns:
            SafetyRating or None
        """
        ingredient = self.search_ingredient(inci_name)
        if ingredient:
            return ingredient.safety_rating
        return None

    def get_inci_name(self, common_name: str) -> Optional[str]:
        """
        Convert common name to INCI name

        Args:
            common_name: Common/trade name (e.g., "Vitamin B3")

        Returns:
            INCI name or None
        """
        ingredient = self.search_ingredient(common_name)
        if ingredient:
            return ingredient.inci_name
        return None

    def get_functions(self, inci_name: str) -> List[str]:
        """
        Get ingredient functions

        Args:
            inci_name: INCI ingredient name

        Returns:
            List of function names
        """
        ingredient = self.search_ingredient(inci_name)
        if ingredient:
            return ingredient.functions
        return []

    def find_alternatives(self,
                          ingredient: str,
                          min_rating: str = "B",
                          max_results: int = 5) -> List[IngredientInfo]:
        """
        Find alternative ingredients with similar function

        Args:
            ingredient: Original ingredient INCI name
            min_rating: Minimum safety rating (A, B, C, D, F)
            max_results: Maximum number of alternatives

        Returns:
            List of alternative IngredientInfo
        """
        original = self.search_ingredient(ingredient)
        if not original or not original.functions:
            return []

        # Get ingredients with similar functions
        primary_function = original.functions[0] if original.functions else None
        if not primary_function:
            return []

        alternatives = self.get_ingredients_by_function(primary_function)

        # Filter by rating and exclude original
        filtered = []
        for alt in alternatives:
            if alt.inci_name == original.inci_name:
                continue
            if alt.safety_rating and alt.safety_rating.grade.value <= min_rating:
                filtered.append(alt)

        return filtered[:max_results]

    def get_ingredients_by_function(self, function: str) -> List[IngredientInfo]:
        """
        Get ingredients by function category

        Args:
            function: Function name (e.g., "Humectant", "Preservative")

        Returns:
            List of IngredientInfo
        """
        # This would require searching/scraping the function filter page
        # For now, return from sample data
        results = []
        for ingredient in self._sample_data.values():
            if function.lower() in [f.lower() for f in ingredient.functions]:
                results.append(ingredient)
        return results

    def analyze_formula(self, ingredients: List[str]) -> FormulaAnalysis:
        """
        Analyze a complete formula

        Args:
            ingredients: List of INCI names

        Returns:
            FormulaAnalysis result
        """
        analyzed = []
        flagged = []
        all_functions = []
        total_score = 0
        valid_count = 0

        for i, inci in enumerate(ingredients):
            info = self.search_ingredient(inci)

            if info:
                valid_count += 1
                score = info.get_score()
                total_score += score

                item = {
                    "inci": info.inci_name,
                    "grade": info.get_grade(),
                    "score": score,
                    "functions": info.functions,
                    "position": i + 1
                }
                analyzed.append(item)
                all_functions.extend(info.functions)

                # Flag concerning ingredients
                if info.get_grade() in ["D", "F"]:
                    flagged.append({
                        "inci": info.inci_name,
                        "grade": info.get_grade(),
                        "concern": ", ".join(info.concerns) if info.concerns else "Low safety rating"
                    })
            else:
                analyzed.append({
                    "inci": inci.upper(),
                    "grade": "?",
                    "score": 0,
                    "functions": [],
                    "position": i + 1,
                    "note": "Not found in database"
                })

        # Calculate overall score
        avg_score = total_score // valid_count if valid_count > 0 else 0
        overall_grade = self._score_to_grade(avg_score)

        # Determine function coverage
        unique_functions = list(set(all_functions))
        expected_functions = ["Humectant", "Emollient", "Preservative", "Antioxidant"]
        missing = [f for f in expected_functions if f not in unique_functions]

        # Generate suggestions
        suggestions = []
        if flagged:
            suggestions.append(f"Consider replacing {len(flagged)} concerning ingredient(s)")
        if "Antioxidant" in missing:
            suggestions.append("Consider adding an antioxidant for formula stability")
        if "Preservative" not in unique_functions and len(ingredients) > 3:
            suggestions.append("Consider adding a preservative system")

        return FormulaAnalysis(
            overall_grade=overall_grade,
            overall_score=avg_score,
            ingredients=analyzed,
            flagged_ingredients=flagged,
            function_coverage={
                "present": unique_functions,
                "missing": missing
            },
            compatibility_issues=[],
            suggestions=suggestions
        )

    def check_compatibility(self, ingredient1: str, ingredient2: str) -> CompatibilityResult:
        """
        Check compatibility between two ingredients

        Args:
            ingredient1: First INCI name
            ingredient2: Second INCI name

        Returns:
            CompatibilityResult
        """
        ing1 = ingredient1.upper()
        ing2 = ingredient2.upper()

        # Known incompatibilities
        known_issues = self._get_known_compatibility(ing1, ing2)
        if known_issues:
            return known_issues

        # Default: compatible (unknown)
        return CompatibilityResult(
            ingredients=[ing1, ing2],
            status=CompatibilityStatus.COMPATIBLE,
            can_use_together=True,
            recommendation="No known compatibility issues",
            reason="",
            tips=[]
        )

    def check_formula_compatibility(self, ingredients: List[str]) -> List[CompatibilityResult]:
        """
        Check compatibility for all ingredient pairs in formula

        Args:
            ingredients: List of INCI names

        Returns:
            List of CompatibilityResult for incompatible/caution pairs
        """
        issues = []
        checked = set()

        for i, ing1 in enumerate(ingredients):
            for ing2 in ingredients[i+1:]:
                pair_key = tuple(sorted([ing1.upper(), ing2.upper()]))
                if pair_key in checked:
                    continue
                checked.add(pair_key)

                result = self.check_compatibility(ing1, ing2)
                if result.status != CompatibilityStatus.COMPATIBLE:
                    issues.append(result)

        return issues

    # ========================================================================
    # Private Methods
    # ========================================================================

    def _parse_ingredient_page(self, soup: BeautifulSoup, url: str) -> Optional[IngredientInfo]:
        """Parse ingredient detail page"""
        try:
            # Extract INCI name
            inci_name = self._extract_text(soup, self.SELECTORS["inci_name"])
            if not inci_name:
                return None

            inci_name = inci_name.upper()

            # Extract common names
            common_names_text = self._extract_text(soup, self.SELECTORS["common_names"])
            common_names = []
            if common_names_text:
                common_names = [n.strip() for n in common_names_text.replace("Also known as:", "").split(",")]

            # Extract CAS number
            cas_number = self._extract_text(soup, self.SELECTORS["cas_number"])
            if cas_number:
                cas_match = re.search(r'\d{2,7}-\d{2}-\d', cas_number)
                cas_number = cas_match.group() if cas_match else None

            # Extract safety info
            grade_text = self._extract_text(soup, self.SELECTORS["safety_grade"])
            score_text = self._extract_text(soup, self.SELECTORS["safety_score"])

            grade = SafetyGrade.UNKNOWN
            if grade_text and grade_text.upper() in ["A", "B", "C", "D", "F"]:
                grade = SafetyGrade(grade_text.upper())

            score = 0
            if score_text:
                score_match = re.search(r'\d+', score_text)
                score = int(score_match.group()) if score_match else 0

            safety_rating = SafetyRating(
                grade=grade,
                score=score,
                description=self._grade_to_description(grade),
                concerns=self._extract_list(soup, self.SELECTORS["concerns"])
            )

            # Extract ratings
            comedogenic = self._extract_rating(soup, self.SELECTORS["comedogenic"])
            irritancy = self._extract_rating(soup, self.SELECTORS["irritancy"])

            # Extract functions and benefits
            functions = self._extract_list(soup, self.SELECTORS["functions"])
            benefits = self._extract_list(soup, self.SELECTORS["benefits"])

            # Extract concentration
            conc_min = self._extract_text(soup, self.SELECTORS["concentration_min"])
            conc_max = self._extract_text(soup, self.SELECTORS["concentration_max"])

            concentration = {}
            if conc_min:
                concentration["min"] = self._parse_percentage(conc_min)
            if conc_max:
                concentration["max"] = self._parse_percentage(conc_max)

            # Extract description
            description = self._extract_text(soup, self.SELECTORS["description"]) or ""

            return IngredientInfo(
                inci_name=inci_name,
                common_names=common_names,
                cas_number=cas_number,
                safety_rating=safety_rating,
                comedogenic_rating=comedogenic,
                irritancy_rating=irritancy,
                functions=functions,
                benefits=benefits,
                concerns=safety_rating.concerns,
                recommended_concentration=concentration,
                description=description,
                url=url,
                last_updated=datetime.now().isoformat()
            )

        except Exception as e:
            logger.error(f"Error parsing ingredient page: {e}")
            raise ParseError(f"Failed to parse ingredient page: {e}")

    def _extract_rating(self, soup: BeautifulSoup, selector: str) -> int:
        """Extract numeric rating (0-5)"""
        text = self._extract_text(soup, selector)
        if text:
            match = re.search(r'\d', text)
            if match:
                return min(5, max(0, int(match.group())))
        return 0

    def _parse_percentage(self, text: str) -> float:
        """Parse percentage from text"""
        if text:
            match = re.search(r'[\d.]+', text)
            if match:
                return float(match.group())
        return 0.0

    def _validate_cas(self, cas_number: str) -> bool:
        """Validate CAS number format and checksum"""
        pattern = r'^(\d{2,7})-(\d{2})-(\d)$'
        match = re.match(pattern, cas_number)

        if not match:
            return False

        # Checksum validation
        digits = match.group(1) + match.group(2)
        check_digit = int(match.group(3))

        total = sum(
            int(d) * (len(digits) - i)
            for i, d in enumerate(digits)
        )

        return total % 10 == check_digit

    def _score_to_grade(self, score: int) -> SafetyGrade:
        """Convert numeric score to letter grade"""
        if score >= 90:
            return SafetyGrade.A
        elif score >= 70:
            return SafetyGrade.B
        elif score >= 50:
            return SafetyGrade.C
        elif score >= 30:
            return SafetyGrade.D
        else:
            return SafetyGrade.F

    def _grade_to_description(self, grade: SafetyGrade) -> str:
        """Get description for grade"""
        descriptions = {
            SafetyGrade.A: "Excellent - Very safe ingredient",
            SafetyGrade.B: "Good - Safe with minor considerations",
            SafetyGrade.C: "Average - Use with some caution",
            SafetyGrade.D: "Below Average - Significant concerns",
            SafetyGrade.F: "Poor - High risk, avoid if possible",
            SafetyGrade.UNKNOWN: "Unknown - No rating available"
        }
        return descriptions.get(grade, "")

    def _dict_to_ingredient(self, data: dict) -> IngredientInfo:
        """Convert dictionary to IngredientInfo"""
        safety_data = data.pop('safety_rating', None)
        safety_rating = None
        if safety_data:
            safety_rating = SafetyRating(
                grade=SafetyGrade(safety_data.get('grade', '?')),
                score=safety_data.get('score', 0),
                description=safety_data.get('description', ''),
                concerns=safety_data.get('concerns', [])
            )

        return IngredientInfo(
            safety_rating=safety_rating,
            **{k: v for k, v in data.items() if k not in ['safety_rating']}
        )

    def _get_known_compatibility(self, ing1: str, ing2: str) -> Optional[CompatibilityResult]:
        """Check known compatibility issues"""
        known_issues = [
            {
                "pair": {"RETINOL", "BENZOYL PEROXIDE"},
                "status": CompatibilityStatus.INCOMPATIBLE,
                "can_use": False,
                "reason": "Benzoyl peroxide can deactivate retinol",
                "tips": ["Use at different times of day", "AM: Benzoyl Peroxide, PM: Retinol"]
            },
            {
                "pair": {"RETINOL", "ASCORBIC ACID"},
                "status": CompatibilityStatus.CAUTION,
                "can_use": True,
                "reason": "Both are potent actives, may increase sensitivity",
                "tips": ["Use Vitamin C in AM, Retinol in PM", "Start with lower concentrations"]
            },
            {
                "pair": {"RETINOL", "GLYCOLIC ACID"},
                "status": CompatibilityStatus.CAUTION,
                "can_use": True,
                "reason": "Both can cause irritation, may be too much for sensitive skin",
                "tips": ["Alternate nights", "Use lower concentrations"]
            },
            {
                "pair": {"RETINOL", "SALICYLIC ACID"},
                "status": CompatibilityStatus.CAUTION,
                "can_use": True,
                "reason": "Both can increase skin sensitivity",
                "tips": ["Use on different nights", "Build tolerance gradually"]
            },
            {
                "pair": {"NIACINAMIDE", "ASCORBIC ACID"},
                "status": CompatibilityStatus.COMPATIBLE,
                "can_use": True,
                "reason": "Generally safe together (old concerns debunked)",
                "tips": ["Can use in same routine", "Layer with lighter product first"]
            },
        ]

        pair_set = {ing1, ing2}
        for issue in known_issues:
            if issue["pair"] == pair_set:
                return CompatibilityResult(
                    ingredients=[ing1, ing2],
                    status=issue["status"],
                    can_use_together=issue["can_use"],
                    reason=issue["reason"],
                    recommendation=issue["tips"][0] if issue["tips"] else "",
                    tips=issue["tips"]
                )

        return None

    def _load_sample_data(self) -> Dict[str, IngredientInfo]:
        """Load sample ingredient data for demo/offline use"""
        return {
            "NIACINAMIDE": IngredientInfo(
                inci_name="NIACINAMIDE",
                common_names=["Vitamin B3", "Nicotinamide"],
                cas_number="98-92-0",
                safety_rating=SafetyRating(
                    grade=SafetyGrade.A,
                    score=95,
                    description="Excellent - Very safe ingredient",
                    concerns=[]
                ),
                comedogenic_rating=0,
                irritancy_rating=0,
                functions=["Skin Conditioning", "Brightening", "Anti-Aging", "Antioxidant"],
                benefits=[
                    "Improves skin texture",
                    "Reduces appearance of pores",
                    "Brightens skin tone",
                    "Helps with fine lines"
                ],
                concerns=[],
                recommended_concentration={"min": 2.0, "max": 10.0},
                description="Niacinamide is a form of vitamin B3 that offers multiple skin benefits."
            ),
            "RETINOL": IngredientInfo(
                inci_name="RETINOL",
                common_names=["Vitamin A", "Retinoid"],
                cas_number="68-26-8",
                safety_rating=SafetyRating(
                    grade=SafetyGrade.C,
                    score=55,
                    description="Average - Use with some caution",
                    concerns=["Photosensitivity", "Irritation", "Not for pregnancy"]
                ),
                comedogenic_rating=0,
                irritancy_rating=3,
                functions=["Anti-Aging", "Skin Conditioning", "Cell Turnover"],
                benefits=[
                    "Reduces fine lines and wrinkles",
                    "Improves skin texture",
                    "Promotes cell renewal",
                    "Helps with acne"
                ],
                concerns=["Photosensitivity", "Irritation", "Not for pregnancy"],
                recommended_concentration={"min": 0.025, "max": 1.0},
                description="Retinol is a powerful anti-aging ingredient that promotes cell turnover."
            ),
            "GLYCERIN": IngredientInfo(
                inci_name="GLYCERIN",
                common_names=["Glycerol", "Vegetable Glycerin"],
                cas_number="56-81-5",
                safety_rating=SafetyRating(
                    grade=SafetyGrade.A,
                    score=98,
                    description="Excellent - Very safe ingredient",
                    concerns=[]
                ),
                comedogenic_rating=0,
                irritancy_rating=0,
                functions=["Humectant", "Moisturizer", "Solvent"],
                benefits=[
                    "Attracts and retains moisture",
                    "Softens skin",
                    "Non-irritating"
                ],
                concerns=[],
                recommended_concentration={"min": 1.0, "max": 10.0},
                description="Glycerin is a powerful humectant that draws moisture to the skin."
            ),
            "HYALURONIC ACID": IngredientInfo(
                inci_name="HYALURONIC ACID",
                common_names=["HA", "Sodium Hyaluronate"],
                cas_number="9004-61-9",
                safety_rating=SafetyRating(
                    grade=SafetyGrade.A,
                    score=97,
                    description="Excellent - Very safe ingredient",
                    concerns=[]
                ),
                comedogenic_rating=0,
                irritancy_rating=0,
                functions=["Humectant", "Moisturizer", "Skin Conditioning"],
                benefits=[
                    "Holds 1000x its weight in water",
                    "Plumps skin",
                    "Reduces appearance of fine lines"
                ],
                concerns=[],
                recommended_concentration={"min": 0.1, "max": 2.0},
                description="Hyaluronic acid is a naturally occurring substance that provides intense hydration."
            ),
            "PHENOXYETHANOL": IngredientInfo(
                inci_name="PHENOXYETHANOL",
                common_names=["PE", "2-Phenoxyethanol"],
                cas_number="122-99-6",
                safety_rating=SafetyRating(
                    grade=SafetyGrade.B,
                    score=72,
                    description="Good - Safe with minor considerations",
                    concerns=["May cause sensitivity in some individuals"]
                ),
                comedogenic_rating=0,
                irritancy_rating=1,
                functions=["Preservative", "Stabilizer"],
                benefits=["Prevents microbial growth", "Extends product shelf life"],
                concerns=["May cause sensitivity in some individuals"],
                recommended_concentration={"min": 0.5, "max": 1.0},
                description="Phenoxyethanol is a widely used preservative considered safe at standard concentrations."
            ),
            "ASCORBIC ACID": IngredientInfo(
                inci_name="ASCORBIC ACID",
                common_names=["Vitamin C", "L-Ascorbic Acid"],
                cas_number="50-81-7",
                safety_rating=SafetyRating(
                    grade=SafetyGrade.B,
                    score=75,
                    description="Good - Safe with minor considerations",
                    concerns=["Unstable", "Can cause irritation at high concentrations"]
                ),
                comedogenic_rating=0,
                irritancy_rating=2,
                functions=["Antioxidant", "Brightening", "Anti-Aging"],
                benefits=[
                    "Brightens skin",
                    "Fights free radicals",
                    "Boosts collagen",
                    "Fades dark spots"
                ],
                concerns=["Unstable", "Can cause irritation at high concentrations"],
                recommended_concentration={"min": 5.0, "max": 20.0},
                description="Vitamin C is a potent antioxidant that brightens and protects skin."
            ),
            "SALICYLIC ACID": IngredientInfo(
                inci_name="SALICYLIC ACID",
                common_names=["BHA", "Beta Hydroxy Acid"],
                cas_number="69-72-7",
                safety_rating=SafetyRating(
                    grade=SafetyGrade.B,
                    score=70,
                    description="Good - Safe with minor considerations",
                    concerns=["Not for children under 3", "May cause dryness"]
                ),
                comedogenic_rating=0,
                irritancy_rating=2,
                functions=["Exfoliant", "Acne Treatment", "Keratolytic"],
                benefits=[
                    "Unclogs pores",
                    "Reduces acne",
                    "Exfoliates inside pores",
                    "Oil-soluble"
                ],
                concerns=["Not for children under 3", "May cause dryness"],
                recommended_concentration={"min": 0.5, "max": 2.0},
                description="Salicylic acid is an oil-soluble BHA that penetrates pores to clear acne."
            ),
            "FRAGRANCE": IngredientInfo(
                inci_name="FRAGRANCE",
                common_names=["Parfum", "Aroma"],
                cas_number=None,
                safety_rating=SafetyRating(
                    grade=SafetyGrade.C,
                    score=45,
                    description="Average - Use with some caution",
                    concerns=["Potential sensitizer", "Undisclosed ingredients", "Allergen risk"]
                ),
                comedogenic_rating=0,
                irritancy_rating=3,
                functions=["Fragrance", "Masking"],
                benefits=["Pleasant scent", "Masks raw material odors"],
                concerns=["Potential sensitizer", "Undisclosed ingredients", "Allergen risk"],
                recommended_concentration={"min": 0.1, "max": 1.0},
                description="Fragrance is a catch-all term for scent ingredients, which may contain allergens."
            ),
        }


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Cosmily Web Client Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python cosmily_client.py search "NIACINAMIDE"
    python cosmily_client.py rating "RETINOL"
    python cosmily_client.py analyze "AQUA,GLYCERIN,NIACINAMIDE"
    python cosmily_client.py compatibility "RETINOL" "VITAMIN C"
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # search command
    search_parser = subparsers.add_parser('search', help='Search ingredient')
    search_parser.add_argument('query', help='Ingredient name to search')

    # rating command
    rating_parser = subparsers.add_parser('rating', help='Get safety rating')
    rating_parser.add_argument('ingredient', help='INCI name')

    # analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze formula')
    analyze_parser.add_argument('ingredients', help='Comma-separated INCI names')

    # compatibility command
    compat_parser = subparsers.add_parser('compatibility', help='Check compatibility')
    compat_parser.add_argument('ingredient1', help='First ingredient')
    compat_parser.add_argument('ingredient2', help='Second ingredient')

    args = parser.parse_args()

    with CosmilyClient() as client:
        if args.command == 'search':
            result = client.search_ingredient(args.query)
            if result:
                print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
            else:
                print(f"Not found: {args.query}")

        elif args.command == 'rating':
            rating = client.get_safety_rating(args.ingredient)
            if rating:
                print(json.dumps(rating.to_dict(), indent=2, ensure_ascii=False))
            else:
                print(f"Rating not found for: {args.ingredient}")

        elif args.command == 'analyze':
            ingredients = [i.strip() for i in args.ingredients.split(',')]
            result = client.analyze_formula(ingredients)
            print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))

        elif args.command == 'compatibility':
            result = client.check_compatibility(args.ingredient1, args.ingredient2)
            print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))

        else:
            parser.print_help()


if __name__ == "__main__":
    main()
