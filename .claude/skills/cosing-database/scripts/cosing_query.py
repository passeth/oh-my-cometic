"""
CosIng Database Query Module
EU 화장품 성분 데이터베이스 검색 및 분석 도구

Usage:
    from cosing_query import CosIngClient

    client = CosIngClient()
    result = client.search_by_inci("NIACINAMIDE")
    print(result)
"""

import requests
from bs4 import BeautifulSoup
import re
import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Union
from dataclasses import dataclass, asdict
from functools import wraps
import time


# ============================================================================
# Data Models
# ============================================================================

@dataclass
class IngredientInfo:
    """CosIng 성분 정보 데이터 클래스"""
    inci_name: str
    cas_number: Optional[str] = None
    ec_number: Optional[str] = None
    chemical_name: Optional[str] = None
    functions: list = None
    restrictions: dict = None
    annex_status: dict = None
    update_date: Optional[str] = None

    def __post_init__(self):
        if self.functions is None:
            self.functions = []
        if self.restrictions is None:
            self.restrictions = {}
        if self.annex_status is None:
            self.annex_status = {}

    def to_dict(self) -> dict:
        return asdict(self)

    def is_prohibited(self) -> bool:
        """Annex II 금지 물질 여부"""
        return self.annex_status.get('annex_ii', False)

    def is_restricted(self) -> bool:
        """Annex III 제한 물질 여부"""
        return bool(self.annex_status.get('annex_iii'))

    def is_preservative(self) -> bool:
        """Annex V 방부제 여부"""
        return bool(self.annex_status.get('annex_v'))

    def is_uv_filter(self) -> bool:
        """Annex VI UV 필터 여부"""
        return bool(self.annex_status.get('annex_vi'))


@dataclass
class RestrictionDetail:
    """제한 조건 상세 정보"""
    annex_ref: str
    product_type: str
    max_concentration: Optional[float] = None
    conditions: Optional[str] = None
    labeling_requirements: list = None

    def __post_init__(self):
        if self.labeling_requirements is None:
            self.labeling_requirements = []


# ============================================================================
# Cache System
# ============================================================================

class CosIngCache:
    """CosIng 데이터 로컬 캐시 시스템"""

    def __init__(self, db_path: Union[str, Path] = None):
        if db_path is None:
            db_path = Path.home() / '.cosmetic_skills' / 'cosing_cache.db'

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.conn = sqlite3.connect(str(self.db_path))
        self._init_db()

    def _init_db(self):
        """데이터베이스 초기화"""
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS ingredients (
                inci_name TEXT PRIMARY KEY,
                data JSON NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE INDEX IF NOT EXISTS idx_updated_at ON ingredients(updated_at);

            CREATE TABLE IF NOT EXISTS search_cache (
                query TEXT PRIMARY KEY,
                results JSON NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        self.conn.commit()

    def get_ingredient(self, inci_name: str, max_age_hours: int = 24) -> Optional[dict]:
        """캐시에서 성분 정보 조회"""
        cursor = self.conn.execute(
            "SELECT data, updated_at FROM ingredients WHERE inci_name = ?",
            (inci_name.upper(),)
        )
        row = cursor.fetchone()

        if row:
            data, updated_at = row
            updated = datetime.fromisoformat(updated_at)
            if datetime.now() - updated < timedelta(hours=max_age_hours):
                return json.loads(data)

        return None

    def set_ingredient(self, inci_name: str, data: dict):
        """캐시에 성분 정보 저장"""
        self.conn.execute("""
            INSERT OR REPLACE INTO ingredients (inci_name, data, updated_at)
            VALUES (?, ?, ?)
        """, (inci_name.upper(), json.dumps(data, ensure_ascii=False),
              datetime.now().isoformat()))
        self.conn.commit()

    def clear_expired(self, max_age_hours: int = 168):
        """만료된 캐시 정리 (기본 7일)"""
        cutoff = datetime.now() - timedelta(hours=max_age_hours)
        self.conn.execute(
            "DELETE FROM ingredients WHERE updated_at < ?",
            (cutoff.isoformat(),)
        )
        self.conn.commit()

    def close(self):
        """데이터베이스 연결 종료"""
        self.conn.close()


# ============================================================================
# Rate Limiting
# ============================================================================

def rate_limit(calls_per_minute: int = 30):
    """API 요청 속도 제한 데코레이터"""
    min_interval = 60.0 / calls_per_minute
    last_called = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator


# ============================================================================
# CosIng Client
# ============================================================================

class CosIngClient:
    """CosIng 데이터베이스 클라이언트"""

    BASE_URL = "https://ec.europa.eu/growth/tools-databases/cosing"

    # CosIng 기능 분류
    FUNCTIONS = {
        "ABRASIVE": "연마제",
        "ABSORBENT": "흡수제",
        "ANTIOXIDANT": "산화방지제",
        "ANTIMICROBIAL": "항균제",
        "CHELATING": "금속이온봉쇄제",
        "COLORANT": "착색제",
        "EMOLLIENT": "피부연화제",
        "EMULSIFYING": "유화제",
        "HUMECTANT": "보습제",
        "MOISTURISING": "수분공급제",
        "PRESERVATIVE": "방부제",
        "SKIN CONDITIONING": "피부컨디셔닝제",
        "SKIN PROTECTING": "피부보호제",
        "SOLVENT": "용매",
        "SURFACTANT": "계면활성제",
        "UV ABSORBER": "자외선흡수제",
        "UV FILTER": "자외선차단제",
        "VISCOSITY CONTROLLING": "점도조절제",
    }

    def __init__(self, use_cache: bool = True, cache_path: str = None):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; CosmeticSkills/1.0)',
            'Accept-Language': 'en-US,en;q=0.9',
        })

        self.use_cache = use_cache
        self.cache = CosIngCache(cache_path) if use_cache else None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cache:
            self.cache.close()

    @rate_limit(calls_per_minute=30)
    def _request(self, url: str, params: dict = None) -> requests.Response:
        """HTTP 요청 (속도 제한 적용)"""
        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response

    def search_by_inci(self, inci_name: str, force_refresh: bool = False) -> Optional[IngredientInfo]:
        """
        INCI명으로 성분 검색

        Args:
            inci_name: INCI 성분명 (예: "NIACINAMIDE")
            force_refresh: 캐시 무시하고 새로 조회

        Returns:
            IngredientInfo 또는 None
        """
        inci_upper = inci_name.upper().strip()

        # 캐시 확인
        if self.use_cache and not force_refresh:
            cached = self.cache.get_ingredient(inci_upper)
            if cached:
                return IngredientInfo(**cached)

        # CosIng 검색 (실제 구현 시 웹 스크래핑 또는 API 호출)
        # 여기서는 샘플 데이터 반환
        result = self._fetch_from_cosing(inci_upper)

        if result and self.use_cache:
            self.cache.set_ingredient(inci_upper, result.to_dict())

        return result

    def search_by_cas(self, cas_number: str) -> Optional[IngredientInfo]:
        """
        CAS 번호로 성분 검색

        Args:
            cas_number: CAS 등록 번호 (예: "98-92-0")

        Returns:
            IngredientInfo 또는 None
        """
        # CAS 번호 형식 검증
        if not self._validate_cas(cas_number):
            raise ValueError(f"Invalid CAS number format: {cas_number}")

        return self._fetch_by_cas(cas_number)

    def check_annex_status(self, inci_name: str) -> dict:
        """
        성분의 Annex 상태 확인

        Returns:
            {
                "annex_ii": bool,  # 금지
                "annex_iii": dict or None,  # 제한
                "annex_iv": dict or None,  # 색소
                "annex_v": dict or None,  # 방부제
                "annex_vi": dict or None,  # UV필터
            }
        """
        ingredient = self.search_by_inci(inci_name)
        if ingredient:
            return ingredient.annex_status
        return {}

    def get_restriction_details(self, inci_name: str) -> list:
        """
        제한 물질의 상세 조건 조회

        Returns:
            RestrictionDetail 리스트
        """
        ingredient = self.search_by_inci(inci_name)
        if not ingredient or not ingredient.is_restricted():
            return []

        restrictions = []
        annex_iii = ingredient.annex_status.get('annex_iii', {})

        for product_type, details in annex_iii.items():
            restrictions.append(RestrictionDetail(
                annex_ref=details.get('ref', ''),
                product_type=product_type,
                max_concentration=details.get('max_concentration'),
                conditions=details.get('conditions'),
                labeling_requirements=details.get('labeling', [])
            ))

        return restrictions

    def verify_formulation(self, formula: list, product_type: str = "leave-on") -> dict:
        """
        전체 처방의 규제 적합성 검증

        Args:
            formula: [{"inci": "AQUA", "percent": 70.0}, ...]
            product_type: "leave-on", "rinse-off", "eye", "oral"

        Returns:
            {
                "status": "PASS" | "REVIEW_REQUIRED" | "FAIL",
                "issues": [...],
                "warnings": [...],
                "labeling_requirements": [...]
            }
        """
        result = {
            "status": "PASS",
            "issues": [],
            "warnings": [],
            "labeling_requirements": []
        }

        for item in formula:
            inci = item.get('inci', '').upper()
            percent = item.get('percent', 0)

            ingredient = self.search_by_inci(inci)
            if not ingredient:
                result["warnings"].append({
                    "inci": inci,
                    "issue": "Not found in CosIng database",
                    "severity": "LOW"
                })
                continue

            # 금지 물질 확인
            if ingredient.is_prohibited():
                result["status"] = "FAIL"
                result["issues"].append({
                    "inci": inci,
                    "issue": "Listed in Annex II (Prohibited)",
                    "severity": "CRITICAL"
                })
                continue

            # 제한 물질 확인
            if ingredient.is_restricted():
                annex_iii = ingredient.annex_status.get('annex_iii', {})
                type_restrictions = annex_iii.get(product_type, {})
                max_conc = type_restrictions.get('max_concentration')

                if max_conc and percent > max_conc:
                    result["status"] = "FAIL"
                    result["issues"].append({
                        "inci": inci,
                        "issue": f"Exceeds max concentration ({max_conc}%) for {product_type}",
                        "severity": "HIGH",
                        "recommendation": f"Reduce to ≤ {max_conc}%"
                    })

                # 라벨 요구사항
                labeling = type_restrictions.get('labeling', [])
                if labeling:
                    result["labeling_requirements"].extend([
                        {"inci": inci, "text": text} for text in labeling
                    ])

        if result["status"] == "PASS" and result["warnings"]:
            result["status"] = "REVIEW_REQUIRED"

        return result

    def _validate_cas(self, cas_number: str) -> bool:
        """CAS 번호 형식 및 체크섬 검증"""
        pattern = r'^(\d{2,7})-(\d{2})-(\d)$'
        match = re.match(pattern, cas_number)

        if not match:
            return False

        # 체크섬 검증
        digits = match.group(1) + match.group(2)
        check_digit = int(match.group(3))

        total = sum(
            int(d) * (len(digits) - i)
            for i, d in enumerate(digits)
        )

        return total % 10 == check_digit

    def _fetch_from_cosing(self, inci_name: str) -> Optional[IngredientInfo]:
        """
        CosIng에서 성분 정보 조회

        실제 구현 시 웹 스크래핑 또는 API 호출
        여기서는 일부 샘플 데이터 제공
        """
        # 샘플 데이터 (실제 구현 시 웹 요청으로 대체)
        SAMPLE_DATA = {
            "NIACINAMIDE": IngredientInfo(
                inci_name="NIACINAMIDE",
                cas_number="98-92-0",
                ec_number="202-713-4",
                chemical_name="Pyridine-3-carboxamide",
                functions=["SKIN CONDITIONING", "SMOOTHING"],
                restrictions={},
                annex_status={
                    "annex_ii": False,
                    "annex_iii": None,
                    "annex_iv": None,
                    "annex_v": None,
                    "annex_vi": None
                }
            ),
            "SALICYLIC ACID": IngredientInfo(
                inci_name="SALICYLIC ACID",
                cas_number="69-72-7",
                ec_number="200-712-3",
                chemical_name="2-Hydroxybenzoic acid",
                functions=["KERATOLYTIC", "PRESERVATIVE"],
                restrictions={
                    "leave-on": {"max_concentration": 2.0},
                    "rinse-off": {"max_concentration": 3.0}
                },
                annex_status={
                    "annex_ii": False,
                    "annex_iii": {
                        "ref": "98",
                        "leave-on": {
                            "max_concentration": 2.0,
                            "conditions": "Not for children under 3 years",
                            "labeling": ["Not for children under 3 years of age"]
                        },
                        "rinse-off": {
                            "max_concentration": 3.0,
                            "conditions": None,
                            "labeling": []
                        }
                    },
                    "annex_v": {"ref": "3", "max_concentration": 0.5}
                }
            ),
            "HYDROQUINONE": IngredientInfo(
                inci_name="HYDROQUINONE",
                cas_number="123-31-9",
                ec_number="204-617-8",
                chemical_name="1,4-Benzenediol",
                functions=["SKIN BLEACHING"],
                restrictions={},
                annex_status={
                    "annex_ii": True,  # 금지 물질
                    "annex_iii": None,
                    "annex_iv": None,
                    "annex_v": None,
                    "annex_vi": None
                }
            ),
            "RETINOL": IngredientInfo(
                inci_name="RETINOL",
                cas_number="68-26-8",
                ec_number="200-683-7",
                chemical_name="Vitamin A",
                functions=["SKIN CONDITIONING"],
                restrictions={},
                annex_status={
                    "annex_ii": False,
                    "annex_iii": {
                        "ref": "223",
                        "face-hand": {
                            "max_concentration": 0.3,
                            "conditions": "Not for children under 3",
                            "labeling": ["Use frequency guidance required"]
                        },
                        "body": {
                            "max_concentration": 0.05,
                            "conditions": "Not for children under 3",
                            "labeling": []
                        }
                    }
                }
            ),
        }

        return SAMPLE_DATA.get(inci_name)

    def _fetch_by_cas(self, cas_number: str) -> Optional[IngredientInfo]:
        """CAS 번호로 성분 조회"""
        # 실제 구현 필요
        return None


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """CLI 인터페이스"""
    import argparse

    parser = argparse.ArgumentParser(
        description="CosIng Database Query Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python cosing_query.py search "NIACINAMIDE"
    python cosing_query.py check "SALICYLIC ACID"
    python cosing_query.py verify formula.json --type leave-on
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # search 명령
    search_parser = subparsers.add_parser('search', help='Search ingredient by INCI name')
    search_parser.add_argument('inci', help='INCI name to search')

    # check 명령
    check_parser = subparsers.add_parser('check', help='Check Annex status')
    check_parser.add_argument('inci', help='INCI name to check')

    # verify 명령
    verify_parser = subparsers.add_parser('verify', help='Verify formulation')
    verify_parser.add_argument('formula_file', help='JSON file with formula')
    verify_parser.add_argument('--type', default='leave-on',
                               choices=['leave-on', 'rinse-off', 'eye', 'oral'],
                               help='Product type')

    args = parser.parse_args()

    with CosIngClient() as client:
        if args.command == 'search':
            result = client.search_by_inci(args.inci)
            if result:
                print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
            else:
                print(f"Not found: {args.inci}")

        elif args.command == 'check':
            status = client.check_annex_status(args.inci)
            print(json.dumps(status, indent=2, ensure_ascii=False))

        elif args.command == 'verify':
            with open(args.formula_file, 'r', encoding='utf-8') as f:
                formula = json.load(f)

            result = client.verify_formulation(formula, args.type)
            print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
