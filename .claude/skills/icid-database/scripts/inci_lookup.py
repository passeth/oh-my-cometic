"""
INCI Name Lookup Utility
INCI명 조회 및 검증 유틸리티

Usage:
    from inci_lookup import INCILookup

    lookup = INCILookup()
    result = lookup.search("niacinamide")
    print(result)

    # CAS 번호 검증
    is_valid = lookup.validate_cas("98-92-0")
    print(f"CAS valid: {is_valid}")
"""

import re
import json
import sqlite3
from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Union
from functools import lru_cache
import urllib.parse


# ============================================================================
# Data Models
# ============================================================================

@dataclass
class INCIEntry:
    """INCI 성분 데이터 클래스"""
    inci_name: str
    cas_numbers: List[str] = field(default_factory=list)
    einecs_number: Optional[str] = None
    chemical_name: Optional[str] = None
    definition: Optional[str] = None
    synonyms: List[str] = field(default_factory=list)
    trade_names: List[str] = field(default_factory=list)
    functions: List[str] = field(default_factory=list)
    source: str = "local"  # local, cosing, cosmily

    def to_dict(self) -> dict:
        return asdict(self)

    def __str__(self) -> str:
        return f"INCIEntry({self.inci_name}, CAS: {', '.join(self.cas_numbers)})"


@dataclass
class SearchResult:
    """검색 결과 데이터 클래스"""
    query: str
    found: bool
    entry: Optional[INCIEntry] = None
    suggestions: List[str] = field(default_factory=list)
    source: str = "local"

    def to_dict(self) -> dict:
        result = {
            "query": self.query,
            "found": self.found,
            "source": self.source,
            "suggestions": self.suggestions
        }
        if self.entry:
            result["entry"] = self.entry.to_dict()
        return result


# ============================================================================
# CAS Number Validation
# ============================================================================

def validate_cas_number(cas: str) -> bool:
    """
    CAS 번호 형식 및 체크섬 검증

    CAS 형식: XXXXXXX-XX-X
    체크섬: 마지막 숫자가 나머지 숫자의 가중합 mod 10

    Args:
        cas: CAS 번호 문자열 (예: "98-92-0")

    Returns:
        bool: 유효한 CAS 번호이면 True

    Examples:
        >>> validate_cas_number("98-92-0")  # Niacinamide
        True
        >>> validate_cas_number("123-45-6")  # Invalid checksum
        False
        >>> validate_cas_number("invalid")
        False
    """
    # 형식 검증
    pattern = r'^(\d{2,7})-(\d{2})-(\d)$'
    match = re.match(pattern, cas.strip())

    if not match:
        return False

    # 체크섬 검증
    first_part = match.group(1)
    second_part = match.group(2)
    check_digit = int(match.group(3))

    digits = first_part + second_part
    total = sum(int(d) * (len(digits) - i) for i, d in enumerate(digits))

    return total % 10 == check_digit


def format_cas_number(cas: str) -> Optional[str]:
    """
    CAS 번호 정규화

    Args:
        cas: 다양한 형식의 CAS 번호

    Returns:
        정규화된 CAS 번호 또는 None

    Examples:
        >>> format_cas_number("98920")
        "98-92-0"
        >>> format_cas_number("98-92-0")
        "98-92-0"
    """
    # 숫자만 추출
    digits = re.sub(r'\D', '', cas)

    if len(digits) < 5 or len(digits) > 10:
        return None

    # 형식화: XXXXX...XX-XX-X
    check_digit = digits[-1]
    second_part = digits[-3:-1]
    first_part = digits[:-3]

    formatted = f"{first_part}-{second_part}-{check_digit}"

    if validate_cas_number(formatted):
        return formatted

    return None


# ============================================================================
# Local INCI Database
# ============================================================================

# 자주 사용되는 INCI 성분 로컬 데이터
COMMON_INCI_DATA: Dict[str, INCIEntry] = {
    "NIACINAMIDE": INCIEntry(
        inci_name="NIACINAMIDE",
        cas_numbers=["98-92-0"],
        einecs_number="202-713-4",
        chemical_name="Pyridine-3-carboxamide",
        definition="Niacinamide is the amide form of Vitamin B3 (Niacin).",
        synonyms=["Nicotinamide", "Vitamin B3", "3-Pyridinecarboxamide"],
        trade_names=["Vitamin B3"],
        functions=["SKIN CONDITIONING", "SMOOTHING"],
        source="local"
    ),
    "HYALURONIC ACID": INCIEntry(
        inci_name="HYALURONIC ACID",
        cas_numbers=["9004-61-9"],
        einecs_number="232-678-0",
        chemical_name="Hyaluronic acid",
        definition="Hyaluronic Acid is a glycosaminoglycan composed of D-glucuronic acid and N-acetyl-D-glucosamine.",
        synonyms=["HA", "Hyaluronan"],
        trade_names=[],
        functions=["HUMECTANT", "SKIN CONDITIONING"],
        source="local"
    ),
    "SODIUM HYALURONATE": INCIEntry(
        inci_name="SODIUM HYALURONATE",
        cas_numbers=["9067-32-7"],
        einecs_number="",
        chemical_name="Sodium salt of Hyaluronic Acid",
        definition="Sodium Hyaluronate is the sodium salt of Hyaluronic Acid.",
        synonyms=["Hyaluronic Acid Sodium", "HA-Na"],
        trade_names=[],
        functions=["HUMECTANT", "SKIN CONDITIONING"],
        source="local"
    ),
    "GLYCERIN": INCIEntry(
        inci_name="GLYCERIN",
        cas_numbers=["56-81-5"],
        einecs_number="200-289-5",
        chemical_name="1,2,3-Propanetriol",
        definition="Glycerin is an organic compound with three hydroxyl groups.",
        synonyms=["Glycerol", "Glycerine"],
        trade_names=[],
        functions=["HUMECTANT", "SOLVENT", "SKIN CONDITIONING"],
        source="local"
    ),
    "RETINOL": INCIEntry(
        inci_name="RETINOL",
        cas_numbers=["68-26-8", "11103-57-4"],
        einecs_number="200-683-7",
        chemical_name="Vitamin A alcohol",
        definition="Retinol is a form of Vitamin A.",
        synonyms=["Vitamin A", "Vitamin A1"],
        trade_names=["Vitamin A"],
        functions=["SKIN CONDITIONING"],
        source="local"
    ),
    "TOCOPHEROL": INCIEntry(
        inci_name="TOCOPHEROL",
        cas_numbers=["59-02-9", "10191-41-0"],
        einecs_number="200-412-2",
        chemical_name="Vitamin E",
        definition="Tocopherol is a form of Vitamin E.",
        synonyms=["Vitamin E", "d-alpha-tocopherol"],
        trade_names=["Vitamin E"],
        functions=["ANTIOXIDANT", "SKIN CONDITIONING"],
        source="local"
    ),
    "ASCORBIC ACID": INCIEntry(
        inci_name="ASCORBIC ACID",
        cas_numbers=["50-81-7"],
        einecs_number="200-066-2",
        chemical_name="L-Ascorbic acid",
        definition="Ascorbic Acid is a water-soluble vitamin (Vitamin C).",
        synonyms=["Vitamin C", "L-Ascorbic Acid"],
        trade_names=["Vitamin C"],
        functions=["ANTIOXIDANT", "SKIN CONDITIONING"],
        source="local"
    ),
    "PANTHENOL": INCIEntry(
        inci_name="PANTHENOL",
        cas_numbers=["81-13-0", "16485-10-2"],
        einecs_number="201-327-3",
        chemical_name="Provitamin B5",
        definition="Panthenol is the alcohol form of Pantothenic Acid (Vitamin B5).",
        synonyms=["Provitamin B5", "Dexpanthenol", "D-Panthenol"],
        trade_names=["Vitamin B5"],
        functions=["HAIR CONDITIONING", "SKIN CONDITIONING"],
        source="local"
    ),
    "ALLANTOIN": INCIEntry(
        inci_name="ALLANTOIN",
        cas_numbers=["97-59-6"],
        einecs_number="202-592-8",
        chemical_name="5-Ureidohydantoin",
        definition="Allantoin is a compound found in botanical extracts of the comfrey plant.",
        synonyms=["Glyoxyldiureide"],
        trade_names=[],
        functions=["SKIN CONDITIONING", "SKIN PROTECTING"],
        source="local"
    ),
    "ADENOSINE": INCIEntry(
        inci_name="ADENOSINE",
        cas_numbers=["58-61-7"],
        einecs_number="200-389-9",
        chemical_name="Adenosine",
        definition="Adenosine is a nucleoside composed of adenine and ribose.",
        synonyms=[],
        trade_names=[],
        functions=["SKIN CONDITIONING"],
        source="local"
    ),
    "CAFFEINE": INCIEntry(
        inci_name="CAFFEINE",
        cas_numbers=["58-08-2"],
        einecs_number="200-362-1",
        chemical_name="1,3,7-Trimethylxanthine",
        definition="Caffeine is a xanthine alkaloid compound.",
        synonyms=["Theine", "1,3,7-Trimethylxanthine"],
        trade_names=[],
        functions=["SKIN CONDITIONING"],
        source="local"
    ),
    "SALICYLIC ACID": INCIEntry(
        inci_name="SALICYLIC ACID",
        cas_numbers=["69-72-7"],
        einecs_number="200-712-3",
        chemical_name="2-Hydroxybenzoic acid",
        definition="Salicylic Acid is a beta hydroxy acid (BHA).",
        synonyms=["BHA", "2-Hydroxybenzoic acid"],
        trade_names=[],
        functions=["KERATOLYTIC", "PRESERVATIVE"],
        source="local"
    ),
    "ARBUTIN": INCIEntry(
        inci_name="ARBUTIN",
        cas_numbers=["497-76-7"],
        einecs_number="207-850-3",
        chemical_name="4-Hydroxyphenyl-beta-D-glucopyranoside",
        definition="Arbutin is a glycoside; a glycosylated hydroquinone extracted from the bearberry plant.",
        synonyms=["Alpha-Arbutin", "Beta-Arbutin"],
        trade_names=[],
        functions=["SKIN CONDITIONING"],
        source="local"
    ),
    "TITANIUM DIOXIDE": INCIEntry(
        inci_name="TITANIUM DIOXIDE",
        cas_numbers=["13463-67-7"],
        einecs_number="236-675-5",
        chemical_name="Titanium(IV) oxide",
        definition="Titanium Dioxide is an inorganic compound.",
        synonyms=["TiO2", "CI 77891"],
        trade_names=[],
        functions=["UV FILTER", "COLORANT", "OPACIFYING"],
        source="local"
    ),
    "ZINC OXIDE": INCIEntry(
        inci_name="ZINC OXIDE",
        cas_numbers=["1314-13-2"],
        einecs_number="215-222-5",
        chemical_name="Zinc oxide",
        definition="Zinc Oxide is an inorganic compound with the formula ZnO.",
        synonyms=["ZnO", "CI 77947"],
        trade_names=[],
        functions=["UV FILTER", "SKIN PROTECTING"],
        source="local"
    ),
    "BUTYLENE GLYCOL": INCIEntry(
        inci_name="BUTYLENE GLYCOL",
        cas_numbers=["107-88-0"],
        einecs_number="203-529-7",
        chemical_name="1,3-Butanediol",
        definition="Butylene Glycol is an organic alcohol.",
        synonyms=["1,3-Butylene Glycol", "BG"],
        trade_names=[],
        functions=["HUMECTANT", "SOLVENT", "SKIN CONDITIONING"],
        source="local"
    ),
    "PHENOXYETHANOL": INCIEntry(
        inci_name="PHENOXYETHANOL",
        cas_numbers=["122-99-6"],
        einecs_number="204-589-7",
        chemical_name="2-Phenoxyethanol",
        definition="Phenoxyethanol is a glycol ether used as a preservative.",
        synonyms=["2-Phenoxyethanol"],
        trade_names=[],
        functions=["PRESERVATIVE"],
        source="local"
    ),
}

# 한글명 → INCI 매핑
KOREAN_TO_INCI: Dict[str, str] = {
    "나이아신아마이드": "NIACINAMIDE",
    "니코틴아마이드": "NIACINAMIDE",
    "비타민B3": "NIACINAMIDE",
    "히알루론산": "HYALURONIC ACID",
    "히알루론산나트륨": "SODIUM HYALURONATE",
    "소듐히알루로네이트": "SODIUM HYALURONATE",
    "글리세린": "GLYCERIN",
    "레티놀": "RETINOL",
    "비타민A": "RETINOL",
    "토코페롤": "TOCOPHEROL",
    "비타민E": "TOCOPHEROL",
    "아스코르브산": "ASCORBIC ACID",
    "비타민C": "ASCORBIC ACID",
    "판테놀": "PANTHENOL",
    "비타민B5": "PANTHENOL",
    "알란토인": "ALLANTOIN",
    "아데노신": "ADENOSINE",
    "카페인": "CAFFEINE",
    "살리실산": "SALICYLIC ACID",
    "살리실릭애씨드": "SALICYLIC ACID",
    "알부틴": "ARBUTIN",
    "아르부틴": "ARBUTIN",
    "티타늄디옥사이드": "TITANIUM DIOXIDE",
    "이산화티타늄": "TITANIUM DIOXIDE",
    "징크옥사이드": "ZINC OXIDE",
    "산화아연": "ZINC OXIDE",
    "부틸렌글라이콜": "BUTYLENE GLYCOL",
    "페녹시에탄올": "PHENOXYETHANOL",
}


# ============================================================================
# INCI Lookup Class
# ============================================================================

class INCILookup:
    """INCI명 조회 및 검증 클래스"""

    def __init__(self, cache_path: Optional[Union[str, Path]] = None):
        """
        Args:
            cache_path: 캐시 데이터베이스 경로 (기본: ~/.cosmetic_skills/inci_cache.db)
        """
        if cache_path is None:
            cache_path = Path.home() / '.cosmetic_skills' / 'inci_cache.db'

        self.cache_path = Path(cache_path)
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)

        self._init_cache_db()

    def _init_cache_db(self):
        """캐시 데이터베이스 초기화"""
        conn = sqlite3.connect(str(self.cache_path))
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS inci_cache (
                inci_name TEXT PRIMARY KEY,
                data JSON NOT NULL,
                source TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_inci_updated
            ON inci_cache(updated_at);
        """)
        conn.commit()
        conn.close()

    def search(self, query: str) -> SearchResult:
        """
        INCI명 검색

        Args:
            query: 검색어 (INCI명, 한글명, CAS 번호, 동의어)

        Returns:
            SearchResult 객체

        Examples:
            >>> lookup = INCILookup()
            >>> result = lookup.search("niacinamide")
            >>> print(result.entry.inci_name)
            "NIACINAMIDE"
        """
        query_upper = query.strip().upper()
        query_original = query.strip()

        # 1. 한글명으로 검색
        if query_original in KOREAN_TO_INCI:
            inci_name = KOREAN_TO_INCI[query_original]
            entry = COMMON_INCI_DATA.get(inci_name)
            if entry:
                return SearchResult(
                    query=query,
                    found=True,
                    entry=entry,
                    source="local"
                )

        # 2. INCI명 직접 매칭
        if query_upper in COMMON_INCI_DATA:
            return SearchResult(
                query=query,
                found=True,
                entry=COMMON_INCI_DATA[query_upper],
                source="local"
            )

        # 3. CAS 번호로 검색
        if self._looks_like_cas(query):
            formatted_cas = format_cas_number(query)
            if formatted_cas:
                for inci_name, entry in COMMON_INCI_DATA.items():
                    if formatted_cas in entry.cas_numbers:
                        return SearchResult(
                            query=query,
                            found=True,
                            entry=entry,
                            source="local"
                        )

        # 4. 동의어/상용명 검색
        for inci_name, entry in COMMON_INCI_DATA.items():
            all_names = entry.synonyms + entry.trade_names
            if query_upper in [n.upper() for n in all_names]:
                return SearchResult(
                    query=query,
                    found=True,
                    entry=entry,
                    source="local"
                )

        # 5. 부분 매칭 (suggestions)
        suggestions = self._find_suggestions(query_upper)

        return SearchResult(
            query=query,
            found=False,
            entry=None,
            suggestions=suggestions,
            source="local"
        )

    def search_by_cas(self, cas_number: str) -> SearchResult:
        """
        CAS 번호로 INCI 검색

        Args:
            cas_number: CAS 번호

        Returns:
            SearchResult 객체
        """
        if not validate_cas_number(cas_number):
            return SearchResult(
                query=cas_number,
                found=False,
                suggestions=["Invalid CAS number format"]
            )

        formatted = format_cas_number(cas_number)
        if formatted:
            for inci_name, entry in COMMON_INCI_DATA.items():
                if formatted in entry.cas_numbers:
                    return SearchResult(
                        query=cas_number,
                        found=True,
                        entry=entry,
                        source="local"
                    )

        return SearchResult(
            query=cas_number,
            found=False,
            suggestions=["CAS number not found in local database"]
        )

    def validate_inci_name(self, inci_name: str) -> Dict[str, Union[bool, str, List[str]]]:
        """
        INCI명 형식 검증

        Args:
            inci_name: 검증할 INCI명

        Returns:
            {
                "valid": bool,
                "normalized": str,  # 정규화된 명칭
                "issues": [str]     # 발견된 문제점
            }
        """
        issues = []
        normalized = inci_name.strip().upper()

        # 대문자 검사
        if inci_name != normalized:
            issues.append("INCI names should be in uppercase")

        # 허용 문자 검사
        allowed_pattern = r'^[A-Z0-9\s\-\/\(\)\.]+$'
        if not re.match(allowed_pattern, normalized):
            issues.append("Contains invalid characters (only A-Z, 0-9, space, -, /, (), . allowed)")

        # 연속 공백 검사
        if '  ' in normalized:
            issues.append("Contains consecutive spaces")
            normalized = re.sub(r'\s+', ' ', normalized)

        # 앞뒤 공백 검사
        if inci_name != inci_name.strip():
            issues.append("Contains leading/trailing whitespace")

        return {
            "valid": len(issues) == 0,
            "normalized": normalized,
            "issues": issues
        }

    @staticmethod
    def validate_cas(cas_number: str) -> bool:
        """
        CAS 번호 검증 (정적 메서드)

        Args:
            cas_number: CAS 번호

        Returns:
            bool: 유효 여부
        """
        return validate_cas_number(cas_number)

    def get_cosing_url(self, inci_name: str) -> str:
        """
        CosIng 검색 URL 생성

        Args:
            inci_name: INCI명

        Returns:
            CosIng 검색 URL
        """
        encoded = urllib.parse.quote(inci_name.upper())
        return f"https://ec.europa.eu/growth/tools-databases/cosing/reference/search?text={encoded}"

    def get_cosmily_url(self, inci_name: str) -> str:
        """
        Cosmily 검색 URL 생성

        Args:
            inci_name: INCI명

        Returns:
            Cosmily 검색 URL
        """
        # Cosmily URL은 소문자, 하이픈으로 변환
        slug = inci_name.lower().replace(' ', '-').replace('/', '-')
        return f"https://www.cosmily.com/ingredients/{slug}"

    def _looks_like_cas(self, query: str) -> bool:
        """CAS 번호 형식인지 확인"""
        # 숫자와 하이픈만 포함
        return bool(re.match(r'^[\d\-]+$', query.strip()))

    def _find_suggestions(self, query: str, max_suggestions: int = 5) -> List[str]:
        """부분 매칭으로 제안 생성"""
        suggestions = []

        for inci_name in COMMON_INCI_DATA.keys():
            if query in inci_name:
                suggestions.append(inci_name)
            elif any(query in syn.upper() for syn in COMMON_INCI_DATA[inci_name].synonyms):
                suggestions.append(inci_name)

        return suggestions[:max_suggestions]

    def list_all(self) -> List[str]:
        """로컬 데이터베이스의 모든 INCI명 목록"""
        return list(COMMON_INCI_DATA.keys())

    def get_korean_name(self, inci_name: str) -> Optional[str]:
        """INCI명에 대응하는 한글명 반환"""
        inci_upper = inci_name.upper()
        for korean, inci in KOREAN_TO_INCI.items():
            if inci == inci_upper:
                return korean
        return None


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """CLI 인터페이스"""
    import argparse

    parser = argparse.ArgumentParser(
        description="INCI Name Lookup Utility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python inci_lookup.py search "niacinamide"
    python inci_lookup.py search "98-92-0"
    python inci_lookup.py search "나이아신아마이드"
    python inci_lookup.py validate-cas "98-92-0"
    python inci_lookup.py validate-inci "Niacinamide"
    python inci_lookup.py list
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # search 명령
    search_parser = subparsers.add_parser('search', help='Search INCI name')
    search_parser.add_argument('query', help='Search query (INCI, CAS, Korean name, synonym)')

    # validate-cas 명령
    cas_parser = subparsers.add_parser('validate-cas', help='Validate CAS number')
    cas_parser.add_argument('cas', help='CAS number to validate')

    # validate-inci 명령
    inci_parser = subparsers.add_parser('validate-inci', help='Validate INCI name format')
    inci_parser.add_argument('inci', help='INCI name to validate')

    # list 명령
    subparsers.add_parser('list', help='List all INCI names in local database')

    # url 명령
    url_parser = subparsers.add_parser('url', help='Generate database URLs')
    url_parser.add_argument('inci', help='INCI name')
    url_parser.add_argument('--db', choices=['cosing', 'cosmily', 'all'],
                           default='all', help='Database to generate URL for')

    args = parser.parse_args()

    lookup = INCILookup()

    if args.command == 'search':
        result = lookup.search(args.query)
        print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))

    elif args.command == 'validate-cas':
        is_valid = validate_cas_number(args.cas)
        formatted = format_cas_number(args.cas) if is_valid else None
        result = {
            "cas_number": args.cas,
            "valid": is_valid,
            "formatted": formatted
        }
        print(json.dumps(result, indent=2))

    elif args.command == 'validate-inci':
        result = lookup.validate_inci_name(args.inci)
        print(json.dumps(result, indent=2))

    elif args.command == 'list':
        inci_list = lookup.list_all()
        for name in sorted(inci_list):
            korean = lookup.get_korean_name(name)
            if korean:
                print(f"{name} ({korean})")
            else:
                print(name)

    elif args.command == 'url':
        if args.db in ['cosing', 'all']:
            print(f"CosIng: {lookup.get_cosing_url(args.inci)}")
        if args.db in ['cosmily', 'all']:
            print(f"Cosmily: {lookup.get_cosmily_url(args.inci)}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
