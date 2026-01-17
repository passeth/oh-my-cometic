"""
Reference Manager

K-Dense 보고서용 학술 참고문헌 관리 및 인용 생성 모듈
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
import re
import json
from datetime import datetime


class ReferenceType(Enum):
    """참고문헌 유형"""
    JOURNAL_ARTICLE = "journal_article"
    BOOK = "book"
    BOOK_CHAPTER = "book_chapter"
    CONFERENCE_PAPER = "conference_paper"
    THESIS = "thesis"
    REPORT = "report"
    WEBPAGE = "webpage"
    PATENT = "patent"
    STANDARD = "standard"


class CitationStyle(Enum):
    """인용 스타일"""
    VANCOUVER = "vancouver"
    APA7 = "apa7"
    ACS = "acs"
    HARVARD = "harvard"
    CHICAGO = "chicago"
    IEEE = "ieee"


class SortOrder(Enum):
    """정렬 순서"""
    CITATION_ORDER = "citation_order"  # 인용 순
    AUTHOR = "author"  # 저자명 순
    YEAR = "year"  # 연도 순
    TITLE = "title"  # 제목 순


@dataclass
class Author:
    """저자 정보"""
    family: str  # 성
    given: str   # 이름
    orcid: Optional[str] = None

    def format_vancouver(self) -> str:
        """Vancouver 스타일"""
        if not self.given:
            return self.family
        initials = "".join([n[0].upper() for n in self.given.split() if n])
        return f"{self.family} {initials}"

    def format_apa(self) -> str:
        """APA 스타일"""
        if not self.given:
            return f"{self.family}"
        initials = ". ".join([n[0].upper() for n in self.given.split() if n]) + "."
        return f"{self.family}, {initials}"

    def format_acs(self) -> str:
        """ACS 스타일"""
        if not self.given:
            return f"{self.family}"
        initials = ". ".join([n[0].upper() for n in self.given.split() if n]) + "."
        return f"{self.family}, {initials}"

    def format_harvard(self) -> str:
        """Harvard 스타일"""
        if not self.given:
            return self.family
        initials = "".join([n[0].upper() for n in self.given.split() if n])
        return f"{self.family}, {initials}"

    @classmethod
    def from_string(cls, author_str: str) -> 'Author':
        """문자열에서 Author 객체 생성"""
        # "Kim HJ" 또는 "Kim, H. J." 형식 파싱
        author_str = author_str.strip()

        if ", " in author_str:
            parts = author_str.split(", ")
            family = parts[0]
            given = parts[1] if len(parts) > 1 else ""
        else:
            parts = author_str.split()
            if len(parts) >= 2:
                family = parts[0]
                given = " ".join(parts[1:])
            else:
                family = author_str
                given = ""

        return cls(family=family, given=given)


@dataclass
class Reference:
    """참고문헌"""
    id: str
    ref_type: ReferenceType = ReferenceType.JOURNAL_ARTICLE
    authors: List[Author] = field(default_factory=list)
    title: str = ""
    journal: Optional[str] = None
    journal_abbrev: Optional[str] = None
    year: int = 0
    month: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    doi: Optional[str] = None
    pmid: Optional[str] = None
    url: Optional[str] = None
    abstract: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    citation_key: str = ""
    citation_number: Optional[int] = None
    category: Optional[str] = None  # clinical, mechanism, regulatory
    notes: Optional[str] = None
    accessed_date: Optional[str] = None

    def __post_init__(self):
        if not self.citation_key and self.authors and self.year:
            first_author = self.authors[0].family.lower() if self.authors else "unknown"
            self.citation_key = f"{first_author}{self.year}"

    def format(self, style: CitationStyle, language: str = "en") -> str:
        """지정된 스타일로 포맷"""
        if style == CitationStyle.VANCOUVER:
            return self._format_vancouver()
        elif style == CitationStyle.APA7:
            return self._format_apa7()
        elif style == CitationStyle.ACS:
            return self._format_acs()
        elif style == CitationStyle.HARVARD:
            return self._format_harvard()
        else:
            return self._format_vancouver()

    def _format_vancouver(self) -> str:
        """Vancouver 스타일 포맷"""
        parts = []

        # 저자
        if self.authors:
            author_list = self._format_authors_vancouver()
            parts.append(author_list)

        # 제목
        parts.append(f"{self.title}.")

        # 저널명
        journal_name = self.journal_abbrev or self.journal
        if journal_name:
            parts.append(f"{journal_name}.")

        # 연도
        parts.append(f"{self.year}")

        # 권호
        if self.volume:
            vol_str = f";{self.volume}"
            if self.issue:
                vol_str += f"({self.issue})"
            parts.append(vol_str)

        # 페이지
        if self.pages:
            parts.append(f":{self.pages}.")
        else:
            parts[-1] += "."

        # DOI
        if self.doi:
            parts.append(f"doi:{self.doi}")

        return " ".join(parts)

    def _format_apa7(self) -> str:
        """APA 7th Edition 스타일 포맷"""
        parts = []

        # 저자
        if self.authors:
            author_list = self._format_authors_apa()
            parts.append(f"{author_list}")

        # 연도
        parts.append(f"({self.year}).")

        # 제목
        parts.append(f"{self.title}.")

        # 저널명 (이탤릭)
        if self.journal:
            journal_str = f"*{self.journal}*"
            if self.volume:
                journal_str += f", *{self.volume}*"
                if self.issue:
                    journal_str += f"({self.issue})"
            if self.pages:
                journal_str += f", {self.pages}"
            journal_str += "."
            parts.append(journal_str)

        # DOI
        if self.doi:
            parts.append(f"https://doi.org/{self.doi}")

        return " ".join(parts)

    def _format_acs(self) -> str:
        """ACS 스타일 포맷"""
        parts = []

        # 저자
        if self.authors:
            author_list = self._format_authors_acs()
            parts.append(author_list)

        # 저널명 (축약)
        journal_name = self.journal_abbrev or self.journal
        if journal_name:
            parts.append(f"*{journal_name}*")

        # 연도, 권, 페이지
        year_vol = f"**{self.year}**"
        if self.volume:
            year_vol += f", *{self.volume}*"
        if self.pages:
            year_vol += f", {self.pages}"
        parts.append(year_vol + ".")

        return " ".join(parts)

    def _format_harvard(self) -> str:
        """Harvard 스타일 포맷"""
        parts = []

        # 저자
        if self.authors:
            author_list = self._format_authors_harvard()
            parts.append(author_list)

        # 연도
        parts.append(f"{self.year},")

        # 제목 (작은따옴표)
        parts.append(f"'{self.title}',")

        # 저널명
        if self.journal:
            journal_str = f"*{self.journal}*"
            if self.volume:
                journal_str += f", vol. {self.volume}"
            if self.issue:
                journal_str += f", no. {self.issue}"
            if self.pages:
                journal_str += f", pp. {self.pages}"
            journal_str += "."
            parts.append(journal_str)

        return " ".join(parts)

    def _format_authors_vancouver(self, max_authors: int = 6) -> str:
        """Vancouver 스타일 저자 목록"""
        if not self.authors:
            return ""

        if len(self.authors) <= max_authors:
            author_strs = [a.format_vancouver() for a in self.authors]
            return ", ".join(author_strs) + "."
        else:
            author_strs = [a.format_vancouver() for a in self.authors[:3]]
            return ", ".join(author_strs) + ", et al."

    def _format_authors_apa(self, max_authors: int = 20) -> str:
        """APA 스타일 저자 목록"""
        if not self.authors:
            return ""

        if len(self.authors) == 1:
            return self.authors[0].format_apa()
        elif len(self.authors) == 2:
            return f"{self.authors[0].format_apa()}, & {self.authors[1].format_apa()}"
        elif len(self.authors) <= max_authors:
            author_strs = [a.format_apa() for a in self.authors[:-1]]
            return ", ".join(author_strs) + f", & {self.authors[-1].format_apa()}"
        else:
            author_strs = [a.format_apa() for a in self.authors[:19]]
            return ", ".join(author_strs) + f", ... {self.authors[-1].format_apa()}"

    def _format_authors_acs(self) -> str:
        """ACS 스타일 저자 목록"""
        if not self.authors:
            return ""

        author_strs = [a.format_acs() for a in self.authors]
        return "; ".join(author_strs) + "."

    def _format_authors_harvard(self) -> str:
        """Harvard 스타일 저자 목록"""
        if not self.authors:
            return ""

        if len(self.authors) == 1:
            return self.authors[0].format_harvard()
        elif len(self.authors) == 2:
            return f"{self.authors[0].format_harvard()} & {self.authors[1].format_harvard()}"
        else:
            return f"{self.authors[0].format_harvard()} et al."

    def to_bibtex(self) -> str:
        """BibTeX 형식으로 변환"""
        entry_type = "article" if self.ref_type == ReferenceType.JOURNAL_ARTICLE else "misc"

        lines = [f"@{entry_type}{{{self.citation_key},"]

        if self.authors:
            author_str = " and ".join([f"{a.family}, {a.given}" for a in self.authors])
            lines.append(f"  author = {{{author_str}}},")

        lines.append(f"  title = {{{self.title}}},")

        if self.journal:
            lines.append(f"  journal = {{{self.journal}}},")

        lines.append(f"  year = {{{self.year}}},")

        if self.volume:
            lines.append(f"  volume = {{{self.volume}}},")

        if self.issue:
            lines.append(f"  number = {{{self.issue}}},")

        if self.pages:
            lines.append(f"  pages = {{{self.pages}}},")

        if self.doi:
            lines.append(f"  doi = {{{self.doi}}},")

        lines.append("}")

        return "\n".join(lines)

    def to_ris(self) -> str:
        """RIS 형식으로 변환"""
        lines = []

        # 타입
        type_map = {
            ReferenceType.JOURNAL_ARTICLE: "JOUR",
            ReferenceType.BOOK: "BOOK",
            ReferenceType.BOOK_CHAPTER: "CHAP",
            ReferenceType.CONFERENCE_PAPER: "CONF",
            ReferenceType.THESIS: "THES",
            ReferenceType.REPORT: "RPRT",
            ReferenceType.WEBPAGE: "ELEC"
        }
        lines.append(f"TY  - {type_map.get(self.ref_type, 'GEN')}")

        # 저자
        for author in self.authors:
            lines.append(f"AU  - {author.family}, {author.given}")

        # 제목
        lines.append(f"TI  - {self.title}")

        # 저널
        if self.journal:
            lines.append(f"JO  - {self.journal}")

        # 연도
        lines.append(f"PY  - {self.year}")

        # 권호
        if self.volume:
            lines.append(f"VL  - {self.volume}")

        if self.issue:
            lines.append(f"IS  - {self.issue}")

        # 페이지
        if self.pages:
            if "-" in self.pages:
                sp, ep = self.pages.split("-")
                lines.append(f"SP  - {sp}")
                lines.append(f"EP  - {ep}")
            else:
                lines.append(f"SP  - {self.pages}")

        # DOI
        if self.doi:
            lines.append(f"DO  - {self.doi}")

        # PMID
        if self.pmid:
            lines.append(f"AN  - {self.pmid}")

        lines.append("ER  -")

        return "\n".join(lines)

    def to_dict(self) -> Dict:
        """딕셔너리 변환"""
        return {
            "id": self.id,
            "type": self.ref_type.value,
            "authors": [{"family": a.family, "given": a.given} for a in self.authors],
            "title": self.title,
            "journal": self.journal,
            "year": self.year,
            "volume": self.volume,
            "issue": self.issue,
            "pages": self.pages,
            "doi": self.doi,
            "pmid": self.pmid,
            "citation_key": self.citation_key,
            "citation_number": self.citation_number
        }


class ReferenceManager:
    """참고문헌 관리자"""

    # 화장품 관련 저널 약어
    JOURNAL_ABBREVIATIONS = {
        "Journal of Cosmetic Dermatology": "J Cosmet Dermatol",
        "International Journal of Cosmetic Science": "Int J Cosmet Sci",
        "Skin Research and Technology": "Skin Res Technol",
        "Journal of the American Academy of Dermatology": "J Am Acad Dermatol",
        "British Journal of Dermatology": "Br J Dermatol",
        "Dermatologic Surgery": "Dermatol Surg",
        "Journal of Investigative Dermatology": "J Invest Dermatol",
        "Archives of Dermatological Research": "Arch Dermatol Res",
        "Contact Dermatitis": "Contact Dermatitis",
        "Experimental Dermatology": "Exp Dermatol",
        "Pigment Cell & Melanoma Research": "Pigment Cell Melanoma Res",
        "Journal of the European Academy of Dermatology and Venereology": "J Eur Acad Dermatol Venereol",
        "Annals of Dermatology": "Ann Dermatol",
        "Clinical and Experimental Dermatology": "Clin Exp Dermatol",
        "Journal of Dermatological Science": "J Dermatol Sci",
        "Dermatology": "Dermatology",
        "Skin Pharmacology and Physiology": "Skin Pharmacol Physiol",
        "International Journal of Dermatology": "Int J Dermatol",
        "Photodermatology, Photoimmunology & Photomedicine": "Photodermatol Photoimmunol Photomed"
    }

    def __init__(self):
        self.references: Dict[str, Reference] = {}
        self._citation_counter = 0
        self._citation_order: List[str] = []

    def add(self, reference: Reference) -> Reference:
        """참고문헌 추가"""
        # 중복 확인
        existing = self._check_duplicate(reference)
        if existing:
            return existing

        # 저널명 약어 적용
        if reference.journal and not reference.journal_abbrev:
            reference.journal_abbrev = self.JOURNAL_ABBREVIATIONS.get(reference.journal)

        self.references[reference.id] = reference
        return reference

    def add_manual(
        self,
        authors: List[str],
        title: str,
        journal: Optional[str] = None,
        year: int = 0,
        volume: Optional[str] = None,
        issue: Optional[str] = None,
        pages: Optional[str] = None,
        doi: Optional[str] = None,
        pmid: Optional[str] = None,
        ref_type: ReferenceType = ReferenceType.JOURNAL_ARTICLE,
        category: Optional[str] = None
    ) -> Reference:
        """수동으로 참고문헌 추가"""
        # 저자 파싱
        author_objs = [Author.from_string(a) for a in authors]

        # ID 생성
        ref_id = doi or pmid or f"ref_{len(self.references) + 1}"

        reference = Reference(
            id=ref_id,
            ref_type=ref_type,
            authors=author_objs,
            title=title,
            journal=journal,
            year=year,
            volume=volume,
            issue=issue,
            pages=pages,
            doi=doi,
            pmid=pmid,
            category=category
        )

        return self.add(reference)

    def add_by_doi(self, doi: str) -> Optional[Reference]:
        """DOI로 참고문헌 추가 (메타데이터 자동 수집)"""
        # 실제 구현에서는 CrossRef API 호출
        # 여기서는 플레이스홀더
        reference = Reference(
            id=doi,
            doi=doi,
            title=f"Reference from DOI: {doi}"
        )
        return self.add(reference)

    def add_by_pmid(self, pmid: str) -> Optional[Reference]:
        """PMID로 참고문헌 추가 (메타데이터 자동 수집)"""
        # 실제 구현에서는 PubMed E-utilities API 호출
        # 여기서는 플레이스홀더
        reference = Reference(
            id=pmid,
            pmid=pmid,
            title=f"Reference from PMID: {pmid}"
        )
        return self.add(reference)

    def _check_duplicate(self, reference: Reference) -> Optional[Reference]:
        """중복 참고문헌 확인"""
        for existing in self.references.values():
            # DOI 일치
            if reference.doi and existing.doi == reference.doi:
                return existing
            # PMID 일치
            if reference.pmid and existing.pmid == reference.pmid:
                return existing
            # 제목 유사도 (간단한 구현)
            if (reference.title and existing.title and
                reference.title.lower() == existing.title.lower()):
                return existing
        return None

    def get(self, ref_id: str) -> Optional[Reference]:
        """참고문헌 조회"""
        return self.references.get(ref_id)

    def get_by_key(self, citation_key: str) -> Optional[Reference]:
        """인용 키로 참고문헌 조회"""
        for ref in self.references.values():
            if ref.citation_key == citation_key:
                return ref
        return None

    def remove(self, ref_id: str) -> bool:
        """참고문헌 삭제"""
        if ref_id in self.references:
            del self.references[ref_id]
            return True
        return False

    def format(
        self,
        reference: Reference,
        style: str = "vancouver"
    ) -> str:
        """단일 참고문헌 포맷"""
        try:
            style_enum = CitationStyle(style.lower())
        except ValueError:
            style_enum = CitationStyle.VANCOUVER

        return reference.format(style_enum)

    def process_citations(self, text: str) -> str:
        """본문 내 인용 처리 ([cite:key] → [번호])"""
        # 인용 패턴: [cite:key1, key2, ...]
        pattern = r'\[cite:([^\]]+)\]'

        def replace_citation(match):
            keys = [k.strip() for k in match.group(1).split(",")]
            numbers = []

            for key in keys:
                ref = self.get_by_key(key)
                if ref:
                    if ref.citation_number is None:
                        self._citation_counter += 1
                        ref.citation_number = self._citation_counter
                        self._citation_order.append(ref.id)
                    numbers.append(str(ref.citation_number))

            if numbers:
                return "[" + ",".join(numbers) + "]"
            return match.group(0)

        return re.sub(pattern, replace_citation, text)

    def generate_bibliography(
        self,
        style: str = "vancouver",
        sort_by: str = "citation_order",
        numbering: bool = True,
        language: str = "ko"
    ) -> str:
        """참고문헌 목록 생성"""
        try:
            style_enum = CitationStyle(style.lower())
        except ValueError:
            style_enum = CitationStyle.VANCOUVER

        try:
            sort_order = SortOrder(sort_by.lower())
        except ValueError:
            sort_order = SortOrder.CITATION_ORDER

        # 정렬
        refs_list = list(self.references.values())

        if sort_order == SortOrder.CITATION_ORDER:
            # 인용 순서대로 정렬
            ordered = []
            for ref_id in self._citation_order:
                if ref_id in self.references:
                    ordered.append(self.references[ref_id])
            # 인용되지 않은 참고문헌은 뒤에 추가
            for ref in refs_list:
                if ref.id not in self._citation_order:
                    ordered.append(ref)
            refs_list = ordered
        elif sort_order == SortOrder.AUTHOR:
            refs_list.sort(key=lambda r: r.authors[0].family if r.authors else "")
        elif sort_order == SortOrder.YEAR:
            refs_list.sort(key=lambda r: r.year, reverse=True)
        elif sort_order == SortOrder.TITLE:
            refs_list.sort(key=lambda r: r.title)

        # 포맷
        lines = []
        for i, ref in enumerate(refs_list, 1):
            formatted = ref.format(style_enum)
            if numbering:
                lines.append(f"{i}. {formatted}")
            else:
                lines.append(formatted)

        return "\n".join(lines)

    def generate_bibliography_by_category(
        self,
        style: str = "vancouver",
        numbering: bool = True
    ) -> str:
        """카테고리별 참고문헌 목록 생성"""
        categories = {}

        for ref in self.references.values():
            category = ref.category or "other"
            if category not in categories:
                categories[category] = []
            categories[category].append(ref)

        category_names = {
            "clinical": "임상 연구",
            "mechanism": "기전 연구",
            "regulatory": "규제/가이드라인",
            "review": "리뷰 논문",
            "other": "기타"
        }

        lines = []
        ref_num = 1

        for category, refs in categories.items():
            lines.append(f"\n### {category_names.get(category, category)}\n")
            for ref in refs:
                try:
                    style_enum = CitationStyle(style.lower())
                except ValueError:
                    style_enum = CitationStyle.VANCOUVER
                formatted = ref.format(style_enum)
                if numbering:
                    lines.append(f"{ref_num}. {formatted}")
                    ref_num += 1
                else:
                    lines.append(formatted)

        return "\n".join(lines)

    def filter_by_category(self, category: str) -> List[Reference]:
        """카테고리로 필터링"""
        return [ref for ref in self.references.values() if ref.category == category]

    def filter_by_year(self, start_year: int, end_year: int) -> List[Reference]:
        """연도 범위로 필터링"""
        return [
            ref for ref in self.references.values()
            if start_year <= ref.year <= end_year
        ]

    def export(self, format: str = "json") -> str:
        """참고문헌 내보내기"""
        if format == "bibtex":
            return "\n\n".join([ref.to_bibtex() for ref in self.references.values()])
        elif format == "ris":
            return "\n\n".join([ref.to_ris() for ref in self.references.values()])
        elif format == "json":
            data = [ref.to_dict() for ref in self.references.values()]
            return json.dumps(data, ensure_ascii=False, indent=2)
        elif format == "csv":
            lines = ["id,authors,title,journal,year,volume,issue,pages,doi,pmid"]
            for ref in self.references.values():
                authors = "; ".join([f"{a.family} {a.given}" for a in ref.authors])
                lines.append(",".join([
                    ref.id,
                    f'"{authors}"',
                    f'"{ref.title}"',
                    ref.journal or "",
                    str(ref.year),
                    ref.volume or "",
                    ref.issue or "",
                    ref.pages or "",
                    ref.doi or "",
                    ref.pmid or ""
                ]))
            return "\n".join(lines)
        else:
            return self.export("json")

    def import_bibtex(self, bibtex_str: str) -> int:
        """BibTeX 가져오기"""
        # 간단한 BibTeX 파서
        count = 0
        entries = re.findall(r'@\w+\{([^}]+)\}', bibtex_str, re.DOTALL)

        for entry in entries:
            # 파싱 로직 (간략화)
            fields = {}
            for line in entry.split("\n"):
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip().lower()
                    value = value.strip().strip(",").strip("{}")
                    fields[key] = value

            if fields:
                authors = []
                if "author" in fields:
                    author_strs = fields["author"].split(" and ")
                    authors = [Author.from_string(a) for a in author_strs]

                ref = Reference(
                    id=fields.get("doi", f"import_{count}"),
                    authors=authors,
                    title=fields.get("title", ""),
                    journal=fields.get("journal", ""),
                    year=int(fields.get("year", 0)),
                    volume=fields.get("volume"),
                    issue=fields.get("number"),
                    pages=fields.get("pages"),
                    doi=fields.get("doi")
                )
                self.add(ref)
                count += 1

        return count

    def get_statistics(self) -> Dict[str, Any]:
        """통계 정보"""
        refs = list(self.references.values())

        years = [ref.year for ref in refs if ref.year]
        categories = {}
        for ref in refs:
            cat = ref.category or "other"
            categories[cat] = categories.get(cat, 0) + 1

        return {
            "total": len(refs),
            "with_doi": sum(1 for ref in refs if ref.doi),
            "with_pmid": sum(1 for ref in refs if ref.pmid),
            "year_range": (min(years), max(years)) if years else None,
            "categories": categories,
            "cited": sum(1 for ref in refs if ref.citation_number is not None)
        }


def create_sample_references() -> ReferenceManager:
    """샘플 참고문헌 생성"""
    manager = ReferenceManager()

    # 샘플 참고문헌 추가
    manager.add_manual(
        authors=["Kim HJ", "Lee SY", "Park JH"],
        title="Double-blind randomized controlled trial of 5% niacinamide for skin brightening",
        journal="Journal of Cosmetic Dermatology",
        year=2023,
        volume="22",
        issue="3",
        pages="123-130",
        doi="10.1111/jcd.12345",
        pmid="12345678",
        category="clinical"
    )

    manager.add_manual(
        authors=["Lee KS", "Park MJ"],
        title="Clinical efficacy of niacinamide on hyperpigmentation",
        journal="Skin Research and Technology",
        year=2022,
        volume="28",
        issue="5",
        pages="456-462",
        doi="10.1111/srt.23456",
        pmid="23456789",
        category="clinical"
    )

    manager.add_manual(
        authors=["Park JY", "Kim SH", "Choi EH"],
        title="Mechanism of niacinamide in melanin transfer inhibition",
        journal="Journal of Investigative Dermatology",
        year=2021,
        volume="141",
        issue="4",
        pages="234-240",
        doi="10.1016/j.jid.2021.01.002",
        pmid="34567890",
        category="mechanism"
    )

    return manager


if __name__ == "__main__":
    # 사용 예제
    manager = create_sample_references()

    print("=== Vancouver Style Bibliography ===")
    print(manager.generate_bibliography(style="vancouver"))
    print()

    print("=== APA 7th Style Bibliography ===")
    print(manager.generate_bibliography(style="apa7"))
    print()

    # 인용 처리 예제
    text = """
    나이아신아마이드는 피부 장벽 기능 개선에 효과적인 것으로
    입증되었다 [cite:kim2023]. 멜라노좀 전달 억제를 통한
    미백 효과도 다수의 연구에서 확인되었다 [cite:lee2022, park2021].
    """

    print("=== Citation Processing ===")
    processed = manager.process_citations(text)
    print(processed)
    print()

    print("=== Final Bibliography (Citation Order) ===")
    print(manager.generate_bibliography(style="vancouver", sort_by="citation_order"))
    print()

    print("=== Export to BibTeX ===")
    print(manager.export(format="bibtex"))
