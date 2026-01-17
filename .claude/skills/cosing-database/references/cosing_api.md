# CosIng API 및 데이터 추출 가이드

## CosIng 웹 인터페이스

### 접속 URL
- **메인**: https://ec.europa.eu/growth/tools-databases/cosing/
- **성분 검색**: https://ec.europa.eu/growth/tools-databases/cosing/ingredients

### 검색 옵션

| 필드 | 설명 | 예시 |
|------|------|------|
| INCI name | 국제 화장품 성분명 | NIACINAMIDE |
| CAS No | Chemical Abstracts Service 등록번호 | 98-92-0 |
| EC No | European Community 번호 | 202-713-4 |
| Chem/IUPAC Name | 화학명/IUPAC 명명법 | pyridine-3-carboxamide |
| Function | 기능 분류 | Skin conditioning |
| Restriction | 규제 상태 | Annex III |

### 검색 결과 필드

```
INCI Name          : NIACINAMIDE
CAS No             : 98-92-0
EC No              : 202-713-4
Chem/IUPAC Name    : Pyridine-3-carboxamide
Restriction        : -
Function           : Skin conditioning, Smoothing
Update Date        : 2023-05-15
```

## 데이터 추출 방법

### 방법 1: 웹 스크래핑

```python
import requests
from bs4 import BeautifulSoup
import re

class CosIngScraper:
    BASE_URL = "https://ec.europa.eu/growth/tools-databases/cosing"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; CosmeticSkills/1.0)'
        })

    def search_ingredient(self, inci_name: str) -> dict:
        """INCI명으로 성분 검색"""
        search_url = f"{self.BASE_URL}/index.cfm"
        params = {
            'fuession': 'search.results',
            'search': inci_name
        }

        response = self.session.get(search_url, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 검색 결과 파싱
        results = self._parse_search_results(soup)
        return results

    def get_ingredient_details(self, cosing_ref: str) -> dict:
        """CosIng 참조번호로 상세 정보 조회"""
        detail_url = f"{self.BASE_URL}/details/{cosing_ref}"
        response = self.session.get(detail_url)

        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_ingredient_details(soup)

    def _parse_search_results(self, soup) -> list:
        """검색 결과 테이블 파싱"""
        results = []
        table = soup.find('table', class_='results')

        if table:
            rows = table.find_all('tr')[1:]  # 헤더 제외
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 5:
                    results.append({
                        'inci_name': cols[0].text.strip(),
                        'cas_number': cols[1].text.strip(),
                        'ec_number': cols[2].text.strip(),
                        'functions': cols[3].text.strip(),
                        'restriction': cols[4].text.strip()
                    })
        return results

    def _parse_ingredient_details(self, soup) -> dict:
        """상세 정보 페이지 파싱"""
        details = {}

        # 기본 정보
        info_table = soup.find('table', class_='ingredient-info')
        if info_table:
            for row in info_table.find_all('tr'):
                label = row.find('th')
                value = row.find('td')
                if label and value:
                    key = label.text.strip().lower().replace(' ', '_')
                    details[key] = value.text.strip()

        # Annex 정보
        annex_section = soup.find('div', class_='annex-info')
        if annex_section:
            details['annexes'] = self._parse_annex_info(annex_section)

        return details

    def _parse_annex_info(self, section) -> dict:
        """Annex 정보 파싱"""
        annexes = {}

        for annex_div in section.find_all('div', class_='annex-entry'):
            annex_num = annex_div.find('span', class_='annex-number')
            if annex_num:
                annex_key = annex_num.text.strip()
                annexes[annex_key] = {
                    'reference': annex_div.get('data-ref', ''),
                    'conditions': self._extract_conditions(annex_div)
                }

        return annexes

    def _extract_conditions(self, div) -> dict:
        """제한 조건 추출"""
        conditions = {}

        conc_elem = div.find('span', class_='max-concentration')
        if conc_elem:
            conditions['max_concentration'] = conc_elem.text.strip()

        type_elem = div.find('span', class_='product-type')
        if type_elem:
            conditions['product_types'] = type_elem.text.strip().split(', ')

        warn_elem = div.find('span', class_='warnings')
        if warn_elem:
            conditions['labeling'] = warn_elem.text.strip()

        return conditions
```

### 방법 2: EU Open Data Portal

EU는 일부 데이터셋을 Open Data 형식으로 제공:

```python
import pandas as pd

def load_cosing_dataset():
    """
    EU Open Data Portal에서 CosIng 데이터셋 로드
    주의: 최신 데이터는 직접 스크래핑 필요
    """
    # CSV 다운로드 URL (예시)
    url = "https://data.europa.eu/euodp/data/dataset/cosing"

    try:
        df = pd.read_csv(url)
        return df
    except:
        print("Direct download not available. Use web scraping instead.")
        return None
```

### 방법 3: 캐시된 로컬 데이터베이스

```python
import sqlite3
import json
from datetime import datetime, timedelta

class CosIngCache:
    def __init__(self, db_path: str = "cosing_cache.db"):
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        """캐시 테이블 생성"""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS ingredients (
                inci_name TEXT PRIMARY KEY,
                data JSON,
                updated_at TIMESTAMP
            )
        """)
        self.conn.commit()

    def get(self, inci_name: str, max_age_hours: int = 24) -> dict:
        """캐시에서 조회 (유효기간 확인)"""
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

    def set(self, inci_name: str, data: dict):
        """캐시에 저장"""
        self.conn.execute("""
            INSERT OR REPLACE INTO ingredients (inci_name, data, updated_at)
            VALUES (?, ?, ?)
        """, (inci_name.upper(), json.dumps(data), datetime.now().isoformat()))
        self.conn.commit()

    def clear_expired(self, max_age_hours: int = 168):  # 7일
        """만료된 캐시 정리"""
        cutoff = datetime.now() - timedelta(hours=max_age_hours)
        self.conn.execute(
            "DELETE FROM ingredients WHERE updated_at < ?",
            (cutoff.isoformat(),)
        )
        self.conn.commit()
```

## API Rate Limiting

CosIng 웹사이트는 공식 API가 없으므로 스크래핑 시 주의:

```python
import time
from functools import wraps

def rate_limit(calls_per_minute: int = 30):
    """요청 속도 제한 데코레이터"""
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

class CosIngAPI:
    @rate_limit(calls_per_minute=30)
    def search(self, query: str):
        """속도 제한이 적용된 검색"""
        pass
```

## 데이터 신뢰성

### 업데이트 주기
- CosIng: 비정기 업데이트 (규정 개정 시)
- Annex: EU 공식 저널 발행 후 반영
- 일반적으로 규정 발효 전 수개월 내 반영

### 검증 권장
1. 중요 규제 정보는 EUR-Lex에서 원문 확인
2. SCCS(Scientific Committee on Consumer Safety) 의견서 참조
3. 국가별 competent authority 가이드라인 확인

## 참고 링크

- EUR-Lex 화장품 규정: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32009R1223
- CosIng FAQ: https://ec.europa.eu/growth/sectors/cosmetics/cosing_en
- SCCS 의견서: https://health.ec.europa.eu/scientific-committees/scientific-committee-consumer-safety-sccs_en
