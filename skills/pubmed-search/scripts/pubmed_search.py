#!/usr/bin/env python3
"""
PubMed Search Client for Cosmetic Ingredient Research

화장품 성분 관련 학술 문헌 검색을 위한 PubMed API 클라이언트

Usage:
    from pubmed_search import PubMedClient

    client = PubMedClient()

    # 성분 검색
    results = client.search_ingredient("Niacinamide")

    # 논문 상세 정보
    article = client.get_article_by_pmid("34567890")

    # 인용 생성
    citation = client.generate_citation("34567890", style="APA")

Requirements:
    pip install requests xmltodict

API Documentation:
    https://www.ncbi.nlm.nih.gov/books/NBK25501/
"""

import os
import time
import json
import re
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union
from enum import Enum
from datetime import datetime
from urllib.parse import urlencode

try:
    import requests
except ImportError:
    requests = None
    print("Warning: 'requests' module not installed. Run: pip install requests")

try:
    import xmltodict
except ImportError:
    xmltodict = None
    print("Warning: 'xmltodict' module not installed. Run: pip install xmltodict")


# ============================================================
# Configuration
# ============================================================

class Config:
    """PubMed API 설정"""
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    DATABASE = "pubmed"

    # API 키 (환경변수에서 읽기, 없으면 None)
    API_KEY = os.environ.get("NCBI_API_KEY", None)

    # Rate limiting
    REQUESTS_PER_SECOND = 10 if API_KEY else 3
    REQUEST_DELAY = 1.0 / REQUESTS_PER_SECOND

    # 기본 설정
    DEFAULT_RETMAX = 20
    MAX_RETMAX = 10000


# ============================================================
# Enums and Data Classes
# ============================================================

class StudyType(Enum):
    """연구 유형"""
    RCT = "Randomized Controlled Trial"
    CLINICAL_TRIAL = "Clinical Trial"
    META_ANALYSIS = "Meta-Analysis"
    SYSTEMATIC_REVIEW = "Systematic Review"
    REVIEW = "Review"
    CASE_REPORT = "Case Report"
    IN_VITRO = "In Vitro"
    IN_VIVO = "In Vivo"
    OBSERVATIONAL = "Observational Study"


class CitationStyle(Enum):
    """인용 형식"""
    APA = "APA"
    VANCOUVER = "Vancouver"
    HARVARD = "Harvard"
    CHICAGO = "Chicago"


@dataclass
class PubMedArticle:
    """PubMed 논문 데이터 클래스"""
    pmid: str
    title: str
    authors: List[str] = field(default_factory=list)
    first_author: str = ""
    journal: str = ""
    journal_abbrev: str = ""
    publication_date: str = ""
    year: int = 0
    volume: str = ""
    issue: str = ""
    pages: str = ""
    doi: str = ""
    abstract: str = ""
    keywords: List[str] = field(default_factory=list)
    mesh_terms: List[str] = field(default_factory=list)
    publication_types: List[str] = field(default_factory=list)
    pmc_id: str = ""
    full_text_url: str = ""

    def get_first_author_surname(self) -> str:
        """제1저자 성 추출"""
        if self.first_author:
            return self.first_author.split()[0] if self.first_author else ""
        elif self.authors:
            return self.authors[0].split()[0]
        return ""

    def is_clinical_trial(self) -> bool:
        """임상 시험 여부"""
        trial_types = ["Clinical Trial", "Randomized Controlled Trial"]
        return any(t in self.publication_types for t in trial_types)

    def is_review(self) -> bool:
        """리뷰 논문 여부"""
        return "Review" in self.publication_types

    def to_dict(self) -> dict:
        """딕셔너리 변환"""
        return {
            "pmid": self.pmid,
            "title": self.title,
            "authors": self.authors,
            "first_author": self.first_author,
            "journal": self.journal,
            "journal_abbrev": self.journal_abbrev,
            "publication_date": self.publication_date,
            "year": self.year,
            "volume": self.volume,
            "issue": self.issue,
            "pages": self.pages,
            "doi": self.doi,
            "abstract": self.abstract,
            "keywords": self.keywords,
            "mesh_terms": self.mesh_terms,
            "publication_types": self.publication_types,
            "pmc_id": self.pmc_id,
            "full_text_url": self.full_text_url
        }


@dataclass
class SearchResult:
    """검색 결과 컨테이너"""
    query: str
    total_count: int
    returned_count: int
    articles: List[PubMedArticle]
    search_time: float = 0.0

    def get_clinical_trials(self) -> List[PubMedArticle]:
        """임상 시험 논문만 필터링"""
        return [a for a in self.articles if a.is_clinical_trial()]

    def get_reviews(self) -> List[PubMedArticle]:
        """리뷰 논문만 필터링"""
        return [a for a in self.articles if a.is_review()]

    def get_by_year_range(self, start: int, end: int) -> List[PubMedArticle]:
        """연도 범위로 필터링"""
        return [a for a in self.articles if start <= a.year <= end]

    def to_evidence_table(self) -> str:
        """증거 테이블 마크다운 생성"""
        lines = [
            "| # | 저자 (연도) | 연구 유형 | 저널 | PMID |",
            "|---|------------|----------|------|------|"
        ]
        for i, article in enumerate(self.articles, 1):
            author = f"{article.get_first_author_surname()} et al." if len(article.authors) > 1 else article.first_author
            pub_type = article.publication_types[0] if article.publication_types else "Article"
            lines.append(
                f"| {i} | {author} ({article.year}) | {pub_type} | {article.journal_abbrev} | {article.pmid} |"
            )
        return "\n".join(lines)


# ============================================================
# Search Query Builder
# ============================================================

class QueryBuilder:
    """PubMed 검색 쿼리 빌더"""

    # 화장품 관련 필터 용어
    COSMETIC_TERMS = [
        "cosmetic[Title/Abstract]",
        "skin[Title/Abstract]",
        "dermatology[MeSH Terms]",
        "topical[Title/Abstract]",
        "cutaneous[Title/Abstract]",
        "skincare[Title/Abstract]"
    ]

    # 효능별 검색어
    EFFICACY_TERMS = {
        "anti-aging": [
            "aging[Title/Abstract]",
            "wrinkle[Title/Abstract]",
            "collagen[Title/Abstract]",
            "elasticity[Title/Abstract]",
            "anti-aging[Title/Abstract]"
        ],
        "brightening": [
            "whitening[Title/Abstract]",
            "brightening[Title/Abstract]",
            "melanin[Title/Abstract]",
            "pigmentation[Title/Abstract]",
            "hyperpigmentation[Title/Abstract]"
        ],
        "moisturizing": [
            "hydration[Title/Abstract]",
            "moisturizing[Title/Abstract]",
            "TEWL[Title/Abstract]",
            "skin barrier[Title/Abstract]"
        ],
        "anti-acne": [
            "acne[Title/Abstract]",
            "sebum[Title/Abstract]",
            "comedone[Title/Abstract]",
            "propionibacterium[Title/Abstract]"
        ],
        "antioxidant": [
            "antioxidant[Title/Abstract]",
            "oxidative stress[Title/Abstract]",
            "free radical[Title/Abstract]",
            "ROS[Title/Abstract]"
        ],
        "anti-inflammatory": [
            "anti-inflammatory[Title/Abstract]",
            "inflammation[Title/Abstract]",
            "cytokine[Title/Abstract]",
            "redness[Title/Abstract]"
        ]
    }

    # 연구 유형 필터
    STUDY_TYPE_FILTERS = {
        "rct": "Randomized Controlled Trial[Publication Type]",
        "clinical_trial": "Clinical Trial[Publication Type]",
        "meta_analysis": "Meta-Analysis[Publication Type]",
        "systematic_review": "Systematic Review[Publication Type]",
        "review": "Review[Publication Type]"
    }

    @staticmethod
    def build_ingredient_query(
        ingredient: str,
        include_cosmetic_filter: bool = True,
        efficacy: str = None,
        study_types: List[str] = None,
        year_start: int = None,
        year_end: int = None
    ) -> str:
        """
        성분 검색 쿼리 생성

        Args:
            ingredient: 성분명
            include_cosmetic_filter: 화장품/피부 관련 필터 적용
            efficacy: 효능 키워드 (anti-aging, brightening, etc.)
            study_types: 연구 유형 필터 리스트
            year_start: 시작 연도
            year_end: 종료 연도

        Returns:
            PubMed 검색 쿼리 문자열
        """
        # 기본 성분 검색
        query_parts = [f'"{ingredient}"[Title/Abstract]']

        # 화장품 필터
        if include_cosmetic_filter:
            cosmetic_query = " OR ".join(QueryBuilder.COSMETIC_TERMS)
            query_parts.append(f"({cosmetic_query})")

        # 효능 필터
        if efficacy and efficacy.lower() in QueryBuilder.EFFICACY_TERMS:
            efficacy_query = " OR ".join(QueryBuilder.EFFICACY_TERMS[efficacy.lower()])
            query_parts.append(f"({efficacy_query})")

        # 연구 유형 필터
        if study_types:
            type_filters = []
            for st in study_types:
                st_lower = st.lower().replace(" ", "_")
                if st_lower in QueryBuilder.STUDY_TYPE_FILTERS:
                    type_filters.append(QueryBuilder.STUDY_TYPE_FILTERS[st_lower])
            if type_filters:
                query_parts.append(f"({' OR '.join(type_filters)})")

        # 연도 필터
        if year_start and year_end:
            query_parts.append(f"{year_start}:{year_end}[Date - Publication]")
        elif year_start:
            query_parts.append(f"{year_start}:3000[Date - Publication]")
        elif year_end:
            query_parts.append(f"1900:{year_end}[Date - Publication]")

        return " AND ".join(query_parts)

    @staticmethod
    def build_mechanism_query(ingredient: str) -> str:
        """메커니즘 연구 쿼리 생성"""
        mechanism_terms = [
            "mechanism[Title/Abstract]",
            "pathway[Title/Abstract]",
            "signaling[Title/Abstract]",
            "molecular[Title/Abstract]"
        ]
        mechanism_query = " OR ".join(mechanism_terms)
        return f'"{ingredient}"[Title/Abstract] AND ({mechanism_query})'

    @staticmethod
    def build_safety_query(ingredient: str) -> str:
        """안전성 연구 쿼리 생성"""
        safety_terms = [
            "safety[Title/Abstract]",
            "toxicity[Title/Abstract]",
            "irritation[Title/Abstract]",
            "sensitization[Title/Abstract]",
            "adverse[Title/Abstract]"
        ]
        safety_query = " OR ".join(safety_terms)
        return f'"{ingredient}"[Title/Abstract] AND ({safety_query})'


# ============================================================
# PubMed Client
# ============================================================

class PubMedClient:
    """PubMed API 클라이언트"""

    def __init__(self, api_key: str = None):
        """
        PubMed 클라이언트 초기화

        Args:
            api_key: NCBI API 키 (선택사항, 환경변수 NCBI_API_KEY 우선)
        """
        self.api_key = api_key or Config.API_KEY
        self.last_request_time = 0
        self.query_builder = QueryBuilder()

        if not requests:
            raise ImportError("requests module is required. Install with: pip install requests")

    def _rate_limit(self):
        """API 요청 속도 제한"""
        elapsed = time.time() - self.last_request_time
        if elapsed < Config.REQUEST_DELAY:
            time.sleep(Config.REQUEST_DELAY - elapsed)
        self.last_request_time = time.time()

    def _build_params(self, **kwargs) -> Dict[str, str]:
        """API 요청 파라미터 생성"""
        params = {
            "db": Config.DATABASE,
            "retmode": kwargs.get("retmode", "json")
        }
        if self.api_key:
            params["api_key"] = self.api_key
        params.update(kwargs)
        return params

    def _make_request(self, endpoint: str, params: Dict) -> Dict:
        """API 요청 실행"""
        self._rate_limit()

        url = f"{Config.BASE_URL}{endpoint}"

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            if params.get("retmode") == "json":
                return response.json()
            elif params.get("rettype") == "xml" or params.get("retmode") == "xml":
                if xmltodict:
                    return xmltodict.parse(response.text)
                else:
                    return {"raw_xml": response.text}
            else:
                return {"raw": response.text}

        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def search(
        self,
        query: str,
        retmax: int = None,
        retstart: int = 0,
        sort: str = "relevance"
    ) -> Dict:
        """
        기본 검색 실행

        Args:
            query: 검색 쿼리
            retmax: 최대 결과 수
            retstart: 시작 위치
            sort: 정렬 방식 (relevance, pub_date)

        Returns:
            검색 결과 (PMID 목록)
        """
        retmax = retmax or Config.DEFAULT_RETMAX
        retmax = min(retmax, Config.MAX_RETMAX)

        params = self._build_params(
            term=query,
            retmax=str(retmax),
            retstart=str(retstart),
            sort=sort,
            usehistory="y"
        )

        return self._make_request("esearch.fcgi", params)

    def fetch(
        self,
        pmids: Union[str, List[str]],
        rettype: str = "xml"
    ) -> Dict:
        """
        PMID로 논문 상세 정보 조회

        Args:
            pmids: PMID 또는 PMID 리스트
            rettype: 반환 형식 (xml, abstract, medline)

        Returns:
            논문 상세 정보
        """
        if isinstance(pmids, list):
            pmids = ",".join(pmids)

        params = self._build_params(
            id=pmids,
            rettype=rettype,
            retmode="xml"
        )

        return self._make_request("efetch.fcgi", params)

    def _parse_article(self, article_data: Dict) -> Optional[PubMedArticle]:
        """XML 데이터에서 PubMedArticle 파싱"""
        try:
            # MedlineCitation에서 데이터 추출
            medline = article_data.get("MedlineCitation", {})
            article = medline.get("Article", {})

            # PMID
            pmid_data = medline.get("PMID", {})
            pmid = pmid_data.get("#text", "") if isinstance(pmid_data, dict) else str(pmid_data)

            # 제목
            title_data = article.get("ArticleTitle", "")
            title = title_data.get("#text", title_data) if isinstance(title_data, dict) else str(title_data)

            # 저자
            authors = []
            author_list = article.get("AuthorList", {}).get("Author", [])
            if isinstance(author_list, dict):
                author_list = [author_list]

            for author in author_list:
                if isinstance(author, dict):
                    last_name = author.get("LastName", "")
                    fore_name = author.get("ForeName", "")
                    if last_name:
                        authors.append(f"{last_name} {fore_name}".strip())

            first_author = authors[0] if authors else ""

            # 저널 정보
            journal_info = article.get("Journal", {})
            journal = journal_info.get("Title", "")
            journal_abbrev = journal_info.get("ISOAbbreviation", "")

            # 발행 정보
            journal_issue = journal_info.get("JournalIssue", {})
            volume = journal_issue.get("Volume", "")
            issue = journal_issue.get("Issue", "")

            pub_date = journal_issue.get("PubDate", {})
            year_str = pub_date.get("Year", "")
            month = pub_date.get("Month", "")
            day = pub_date.get("Day", "")

            year = int(year_str) if year_str and year_str.isdigit() else 0
            publication_date = f"{year_str}-{month}-{day}".strip("-")

            # 페이지
            pagination = article.get("Pagination", {})
            pages = pagination.get("MedlinePgn", "") if isinstance(pagination, dict) else ""

            # 초록
            abstract_data = article.get("Abstract", {}).get("AbstractText", "")
            if isinstance(abstract_data, list):
                abstract_parts = []
                for part in abstract_data:
                    if isinstance(part, dict):
                        label = part.get("@Label", "")
                        text = part.get("#text", "")
                        if label and text:
                            abstract_parts.append(f"{label}: {text}")
                        elif text:
                            abstract_parts.append(text)
                    else:
                        abstract_parts.append(str(part))
                abstract = " ".join(abstract_parts)
            elif isinstance(abstract_data, dict):
                abstract = abstract_data.get("#text", "")
            else:
                abstract = str(abstract_data)

            # DOI
            doi = ""
            article_ids = article.get("ELocationID", [])
            if isinstance(article_ids, dict):
                article_ids = [article_ids]
            for eid in article_ids:
                if isinstance(eid, dict) and eid.get("@EIdType") == "doi":
                    doi = eid.get("#text", "")
                    break

            # PMC ID
            pmc_id = ""
            pubmed_data = article_data.get("PubmedData", {})
            article_id_list = pubmed_data.get("ArticleIdList", {}).get("ArticleId", [])
            if isinstance(article_id_list, dict):
                article_id_list = [article_id_list]
            for aid in article_id_list:
                if isinstance(aid, dict):
                    if aid.get("@IdType") == "pmc":
                        pmc_id = aid.get("#text", "")
                    elif aid.get("@IdType") == "doi" and not doi:
                        doi = aid.get("#text", "")

            # MeSH 용어
            mesh_terms = []
            mesh_list = medline.get("MeshHeadingList", {}).get("MeshHeading", [])
            if isinstance(mesh_list, dict):
                mesh_list = [mesh_list]
            for mesh in mesh_list:
                if isinstance(mesh, dict):
                    descriptor = mesh.get("DescriptorName", {})
                    if isinstance(descriptor, dict):
                        mesh_terms.append(descriptor.get("#text", ""))
                    elif descriptor:
                        mesh_terms.append(str(descriptor))

            # 키워드
            keywords = []
            keyword_list = medline.get("KeywordList", {}).get("Keyword", [])
            if isinstance(keyword_list, dict):
                keyword_list = [keyword_list]
            for kw in keyword_list:
                if isinstance(kw, dict):
                    keywords.append(kw.get("#text", ""))
                elif kw:
                    keywords.append(str(kw))

            # 논문 유형
            publication_types = []
            pub_type_list = article.get("PublicationTypeList", {}).get("PublicationType", [])
            if isinstance(pub_type_list, dict):
                pub_type_list = [pub_type_list]
            for pt in pub_type_list:
                if isinstance(pt, dict):
                    publication_types.append(pt.get("#text", ""))
                elif pt:
                    publication_types.append(str(pt))

            # Full text URL
            full_text_url = ""
            if pmc_id:
                full_text_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_id}/"
            elif doi:
                full_text_url = f"https://doi.org/{doi}"

            return PubMedArticle(
                pmid=pmid,
                title=title,
                authors=authors,
                first_author=first_author,
                journal=journal,
                journal_abbrev=journal_abbrev,
                publication_date=publication_date,
                year=year,
                volume=volume,
                issue=issue,
                pages=pages,
                doi=doi,
                abstract=abstract,
                keywords=keywords,
                mesh_terms=mesh_terms,
                publication_types=publication_types,
                pmc_id=pmc_id,
                full_text_url=full_text_url
            )

        except Exception as e:
            print(f"Error parsing article: {e}")
            return None

    def search_ingredient(
        self,
        ingredient: str,
        retmax: int = 20,
        include_cosmetic_filter: bool = True,
        efficacy: str = None,
        study_types: List[str] = None,
        year_start: int = None,
        year_end: int = None
    ) -> SearchResult:
        """
        성분명으로 논문 검색

        Args:
            ingredient: 성분명 (INCI명 또는 일반명)
            retmax: 최대 결과 수
            include_cosmetic_filter: 화장품/피부 관련 필터 적용
            efficacy: 효능 키워드
            study_types: 연구 유형 필터
            year_start: 시작 연도
            year_end: 종료 연도

        Returns:
            SearchResult 객체
        """
        start_time = time.time()

        # 쿼리 생성
        query = self.query_builder.build_ingredient_query(
            ingredient=ingredient,
            include_cosmetic_filter=include_cosmetic_filter,
            efficacy=efficacy,
            study_types=study_types,
            year_start=year_start,
            year_end=year_end
        )

        # 검색 실행
        search_result = self.search(query, retmax=retmax)

        if "error" in search_result:
            return SearchResult(
                query=query,
                total_count=0,
                returned_count=0,
                articles=[],
                search_time=time.time() - start_time
            )

        # 결과 파싱
        esearch_result = search_result.get("esearchresult", {})
        total_count = int(esearch_result.get("count", 0))
        pmids = esearch_result.get("idlist", [])

        # 논문 상세 정보 조회
        articles = []
        if pmids:
            fetch_result = self.fetch(pmids)

            if xmltodict and "PubmedArticleSet" in fetch_result:
                article_set = fetch_result.get("PubmedArticleSet", {})
                pubmed_articles = article_set.get("PubmedArticle", [])

                if isinstance(pubmed_articles, dict):
                    pubmed_articles = [pubmed_articles]

                for article_data in pubmed_articles:
                    article = self._parse_article(article_data)
                    if article:
                        articles.append(article)

        return SearchResult(
            query=query,
            total_count=total_count,
            returned_count=len(articles),
            articles=articles,
            search_time=time.time() - start_time
        )

    def search_cosmetic_ingredient(
        self,
        ingredient: str,
        retmax: int = 20,
        filters: List[str] = None,
        study_types: List[str] = None
    ) -> SearchResult:
        """화장품 성분 특화 검색 (화장품 필터 강제 적용)"""
        return self.search_ingredient(
            ingredient=ingredient,
            retmax=retmax,
            include_cosmetic_filter=True,
            study_types=study_types
        )

    def search_efficacy(
        self,
        ingredient: str,
        efficacy: str,
        retmax: int = 20
    ) -> SearchResult:
        """효능별 검색"""
        return self.search_ingredient(
            ingredient=ingredient,
            retmax=retmax,
            include_cosmetic_filter=True,
            efficacy=efficacy
        )

    def search_clinical_trials(
        self,
        ingredient: str,
        retmax: int = 20
    ) -> SearchResult:
        """임상 시험 검색"""
        return self.search_ingredient(
            ingredient=ingredient,
            retmax=retmax,
            include_cosmetic_filter=True,
            study_types=["Clinical Trial", "RCT"]
        )

    def search_mechanism(self, ingredient: str, retmax: int = 20) -> SearchResult:
        """메커니즘 연구 검색"""
        start_time = time.time()
        query = self.query_builder.build_mechanism_query(ingredient)

        search_result = self.search(query, retmax=retmax)
        esearch_result = search_result.get("esearchresult", {})
        total_count = int(esearch_result.get("count", 0))
        pmids = esearch_result.get("idlist", [])

        articles = []
        if pmids:
            fetch_result = self.fetch(pmids)
            if xmltodict and "PubmedArticleSet" in fetch_result:
                pubmed_articles = fetch_result.get("PubmedArticleSet", {}).get("PubmedArticle", [])
                if isinstance(pubmed_articles, dict):
                    pubmed_articles = [pubmed_articles]
                for article_data in pubmed_articles:
                    article = self._parse_article(article_data)
                    if article:
                        articles.append(article)

        return SearchResult(
            query=query,
            total_count=total_count,
            returned_count=len(articles),
            articles=articles,
            search_time=time.time() - start_time
        )

    def search_safety(self, ingredient: str, retmax: int = 20) -> SearchResult:
        """안전성 연구 검색"""
        start_time = time.time()
        query = self.query_builder.build_safety_query(ingredient)

        search_result = self.search(query, retmax=retmax)
        esearch_result = search_result.get("esearchresult", {})
        total_count = int(esearch_result.get("count", 0))
        pmids = esearch_result.get("idlist", [])

        articles = []
        if pmids:
            fetch_result = self.fetch(pmids)
            if xmltodict and "PubmedArticleSet" in fetch_result:
                pubmed_articles = fetch_result.get("PubmedArticleSet", {}).get("PubmedArticle", [])
                if isinstance(pubmed_articles, dict):
                    pubmed_articles = [pubmed_articles]
                for article_data in pubmed_articles:
                    article = self._parse_article(article_data)
                    if article:
                        articles.append(article)

        return SearchResult(
            query=query,
            total_count=total_count,
            returned_count=len(articles),
            articles=articles,
            search_time=time.time() - start_time
        )

    def get_article_by_pmid(self, pmid: str) -> Optional[PubMedArticle]:
        """PMID로 단일 논문 조회"""
        fetch_result = self.fetch(pmid)

        if xmltodict and "PubmedArticleSet" in fetch_result:
            article_set = fetch_result.get("PubmedArticleSet", {})
            pubmed_article = article_set.get("PubmedArticle", {})

            if isinstance(pubmed_article, list):
                pubmed_article = pubmed_article[0] if pubmed_article else {}

            return self._parse_article(pubmed_article)

        return None

    def batch_search(
        self,
        ingredients: List[str],
        retmax_per_ingredient: int = 10
    ) -> Dict[str, SearchResult]:
        """다중 성분 배치 검색"""
        results = {}
        for ingredient in ingredients:
            results[ingredient] = self.search_ingredient(
                ingredient=ingredient,
                retmax=retmax_per_ingredient
            )
        return results

    def generate_citation(
        self,
        pmid_or_article: Union[str, PubMedArticle],
        style: str = "APA"
    ) -> str:
        """
        인용 형식 생성

        Args:
            pmid_or_article: PMID 문자열 또는 PubMedArticle 객체
            style: 인용 형식 (APA, Vancouver, Harvard)

        Returns:
            형식화된 인용 문자열
        """
        # 논문 정보 가져오기
        if isinstance(pmid_or_article, str):
            article = self.get_article_by_pmid(pmid_or_article)
        else:
            article = pmid_or_article

        if not article:
            return f"[Unable to generate citation for PMID: {pmid_or_article}]"

        style_upper = style.upper()

        if style_upper == "APA":
            # APA 형식: Author, A. A., Author, B. B., & Author, C. C. (Year). Title. Journal, Volume(Issue), Pages. DOI
            if len(article.authors) > 1:
                author_str = ", ".join(article.authors[:-1]) + f", & {article.authors[-1]}"
            elif article.authors:
                author_str = article.authors[0]
            else:
                author_str = "Unknown Author"

            citation = f"{author_str} ({article.year}). {article.title}. {article.journal}"

            if article.volume:
                citation += f", {article.volume}"
                if article.issue:
                    citation += f"({article.issue})"
            if article.pages:
                citation += f", {article.pages}"

            citation += "."

            if article.doi:
                citation += f" https://doi.org/{article.doi}"

            return citation

        elif style_upper == "VANCOUVER":
            # Vancouver 형식: Author AA, Author BB. Title. Journal. Year;Volume(Issue):Pages.
            author_strs = []
            for author in article.authors[:6]:  # 최대 6명
                parts = author.split()
                if len(parts) >= 2:
                    surname = parts[0]
                    initials = "".join(p[0] for p in parts[1:] if p)
                    author_strs.append(f"{surname} {initials}")
                else:
                    author_strs.append(author)

            if len(article.authors) > 6:
                author_strs.append("et al")

            author_str = ", ".join(author_strs)

            citation = f"{author_str}. {article.title}. {article.journal_abbrev or article.journal}. {article.year}"

            if article.volume:
                citation += f";{article.volume}"
                if article.issue:
                    citation += f"({article.issue})"
            if article.pages:
                citation += f":{article.pages}"

            citation += "."

            return citation

        elif style_upper == "HARVARD":
            # Harvard 형식: Author, A.A. (Year) 'Title', Journal, Volume(Issue), pp. Pages.
            if article.authors:
                first = article.authors[0].split()
                if len(first) >= 2:
                    author_str = f"{first[0]}, {first[1][0]}."
                else:
                    author_str = first[0]

                if len(article.authors) > 1:
                    author_str += " et al."
            else:
                author_str = "Unknown Author"

            citation = f"{author_str} ({article.year}) '{article.title}', {article.journal}"

            if article.volume:
                citation += f", {article.volume}"
                if article.issue:
                    citation += f"({article.issue})"
            if article.pages:
                citation += f", pp. {article.pages}"

            citation += "."

            return citation

        else:
            return f"[Unsupported citation style: {style}]"

    def get_in_text_citation(self, pmid_or_article: Union[str, PubMedArticle]) -> str:
        """In-text citation 생성 (예: Kim et al., 2023)"""
        if isinstance(pmid_or_article, str):
            article = self.get_article_by_pmid(pmid_or_article)
        else:
            article = pmid_or_article

        if not article:
            return "[Unknown]"

        surname = article.get_first_author_surname()

        if len(article.authors) > 2:
            return f"{surname} et al., {article.year}"
        elif len(article.authors) == 2:
            second_surname = article.authors[1].split()[0] if article.authors[1] else ""
            return f"{surname} & {second_surname}, {article.year}"
        else:
            return f"{surname}, {article.year}"


# ============================================================
# CLI Interface
# ============================================================

def main():
    """CLI 메인 함수"""
    import sys

    if not requests:
        print("Error: requests module required. Install with: pip install requests")
        return

    client = PubMedClient()

    if len(sys.argv) < 2:
        print("PubMed Search Tool for Cosmetic Ingredients")
        print("\nUsage: python pubmed_search.py <command> [args]")
        print("\nCommands:")
        print("  search <ingredient>        - Search ingredient papers")
        print("  clinical <ingredient>      - Search clinical trials only")
        print("  mechanism <ingredient>     - Search mechanism studies")
        print("  safety <ingredient>        - Search safety studies")
        print("  efficacy <ingredient> <type> - Search by efficacy")
        print("    Types: anti-aging, brightening, moisturizing, anti-acne, antioxidant")
        print("  article <pmid>             - Get article details")
        print("  cite <pmid> [style]        - Generate citation (APA/Vancouver/Harvard)")
        print("\nExamples:")
        print("  python pubmed_search.py search Niacinamide")
        print("  python pubmed_search.py clinical Retinol")
        print("  python pubmed_search.py efficacy \"Vitamin C\" brightening")
        print("  python pubmed_search.py cite 34567890 APA")
        return

    command = sys.argv[1].lower()

    if command == "search" and len(sys.argv) >= 3:
        ingredient = " ".join(sys.argv[2:])
        print(f"\nSearching PubMed for: {ingredient}")
        print("-" * 50)

        results = client.search_ingredient(ingredient)

        print(f"Total found: {results.total_count}")
        print(f"Retrieved: {results.returned_count}")
        print(f"Search time: {results.search_time:.2f}s")
        print(f"\nQuery: {results.query[:100]}...")

        if results.articles:
            print(f"\nTop {len(results.articles)} results:")
            for i, article in enumerate(results.articles, 1):
                print(f"\n{i}. {article.title[:80]}...")
                print(f"   {article.first_author} et al. ({article.year})")
                print(f"   {article.journal_abbrev or article.journal}")
                print(f"   PMID: {article.pmid}")
                if article.publication_types:
                    print(f"   Type: {', '.join(article.publication_types[:2])}")

    elif command == "clinical" and len(sys.argv) >= 3:
        ingredient = " ".join(sys.argv[2:])
        print(f"\nSearching clinical trials for: {ingredient}")
        print("-" * 50)

        results = client.search_clinical_trials(ingredient)

        print(f"Total clinical trials: {results.total_count}")
        print(f"Retrieved: {results.returned_count}")

        if results.articles:
            print(f"\nClinical trials:")
            for i, article in enumerate(results.articles, 1):
                print(f"\n{i}. {article.title[:80]}...")
                print(f"   {article.first_author} et al. ({article.year})")
                print(f"   PMID: {article.pmid}")

    elif command == "mechanism" and len(sys.argv) >= 3:
        ingredient = " ".join(sys.argv[2:])
        print(f"\nSearching mechanism studies for: {ingredient}")
        results = client.search_mechanism(ingredient)

        print(f"Total: {results.total_count}, Retrieved: {results.returned_count}")
        for i, article in enumerate(results.articles[:5], 1):
            print(f"{i}. {article.title[:70]}... ({article.year})")

    elif command == "safety" and len(sys.argv) >= 3:
        ingredient = " ".join(sys.argv[2:])
        print(f"\nSearching safety studies for: {ingredient}")
        results = client.search_safety(ingredient)

        print(f"Total: {results.total_count}, Retrieved: {results.returned_count}")
        for i, article in enumerate(results.articles[:5], 1):
            print(f"{i}. {article.title[:70]}... ({article.year})")

    elif command == "efficacy" and len(sys.argv) >= 4:
        ingredient = sys.argv[2]
        efficacy = sys.argv[3]
        print(f"\nSearching {efficacy} studies for: {ingredient}")
        results = client.search_efficacy(ingredient, efficacy)

        print(f"Total: {results.total_count}, Retrieved: {results.returned_count}")
        for i, article in enumerate(results.articles[:5], 1):
            print(f"{i}. {article.title[:70]}... ({article.year})")

    elif command == "article" and len(sys.argv) >= 3:
        pmid = sys.argv[2]
        print(f"\nFetching article: PMID {pmid}")
        print("-" * 50)

        article = client.get_article_by_pmid(pmid)

        if article:
            print(f"Title: {article.title}")
            print(f"Authors: {', '.join(article.authors[:5])}")
            if len(article.authors) > 5:
                print(f"         ... and {len(article.authors) - 5} more")
            print(f"Journal: {article.journal}")
            print(f"Date: {article.publication_date}")
            print(f"DOI: {article.doi}")
            print(f"PMID: {article.pmid}")
            if article.pmc_id:
                print(f"PMC: {article.pmc_id}")
            print(f"\nAbstract:\n{article.abstract[:500]}...")
            if article.mesh_terms:
                print(f"\nMeSH Terms: {', '.join(article.mesh_terms[:10])}")
        else:
            print(f"Article not found: {pmid}")

    elif command == "cite" and len(sys.argv) >= 3:
        pmid = sys.argv[2]
        style = sys.argv[3] if len(sys.argv) > 3 else "APA"

        print(f"\nGenerating {style} citation for PMID {pmid}:")
        print("-" * 50)

        citation = client.generate_citation(pmid, style)
        print(citation)

        print(f"\nIn-text citation:")
        in_text = client.get_in_text_citation(pmid)
        print(f"({in_text})")

    else:
        print(f"Unknown command or missing arguments: {command}")
        print("Run without arguments for usage help.")


if __name__ == "__main__":
    main()
