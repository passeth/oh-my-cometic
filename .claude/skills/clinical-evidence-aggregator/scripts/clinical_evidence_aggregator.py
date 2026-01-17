"""
Clinical Evidence Aggregator

화장품 성분의 임상 연구 근거를 체계적으로 수집, 평가, 요약하는 모듈
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum
from datetime import datetime
import json
import re


class EvidenceGrade(Enum):
    """근거 등급"""
    A = "A"  # Strong: 3+ RCT, n>200, consistent
    B = "B"  # Moderate: 1-2 RCT or 3+ trials, n>100
    C = "C"  # Limited: 1+ trial, n≥20
    D = "D"  # Preliminary: in-vitro/in-vivo only
    E = "E"  # Insufficient: lacking or conflicting


class StudyType(Enum):
    """연구 유형"""
    META_ANALYSIS = "meta_analysis"
    SYSTEMATIC_REVIEW = "systematic_review"
    RCT = "rct"  # Randomized Controlled Trial
    CONTROLLED_TRIAL = "controlled_trial"
    COHORT = "cohort"
    CASE_CONTROL = "case_control"
    CROSS_SECTIONAL = "cross_sectional"
    CASE_SERIES = "case_series"
    CASE_REPORT = "case_report"
    IN_VIVO = "in_vivo"
    IN_VITRO = "in_vitro"
    EX_VIVO = "ex_vivo"


class BiasRisk(Enum):
    """비뚤림 위험"""
    LOW = "low"
    SOME_CONCERNS = "some_concerns"
    HIGH = "high"


class SampleAdequacy(Enum):
    """표본 크기 적절성"""
    EXCELLENT = "excellent"    # n >= 100
    GOOD = "good"              # n >= 50
    ADEQUATE = "adequate"      # n >= 30
    LIMITED = "limited"        # n >= 20
    INSUFFICIENT = "insufficient"  # n < 20


@dataclass
class StudyQuality:
    """연구 품질 평가"""
    jadad_score: Optional[int] = None  # 0-5 for RCTs
    randomization_mentioned: bool = False
    randomization_appropriate: bool = False
    blinding_mentioned: bool = False
    blinding_appropriate: bool = False
    withdrawals_reported: bool = False
    bias_risk: BiasRisk = BiasRisk.HIGH
    sample_adequacy: SampleAdequacy = SampleAdequacy.INSUFFICIENT
    conflict_of_interest: Optional[str] = None
    funding_source: Optional[str] = None

    def calculate_jadad(self) -> int:
        """Jadad 점수 계산"""
        score = 0
        if self.randomization_mentioned:
            score += 1
        if self.randomization_appropriate:
            score += 1
        if self.blinding_mentioned:
            score += 1
        if self.blinding_appropriate:
            score += 1
        if self.withdrawals_reported:
            score += 1
        self.jadad_score = score
        return score

    @property
    def is_high_quality(self) -> bool:
        """고품질 연구 여부 (Jadad >= 3)"""
        if self.jadad_score is not None:
            return self.jadad_score >= 3
        return False


@dataclass
class EffectSize:
    """효과 크기"""
    metric: str  # e.g., "ITA°", "Melanin Index", "L* value"
    baseline: Optional[float] = None
    final: Optional[float] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None
    p_value: Optional[float] = None
    confidence_interval: Optional[Tuple[float, float]] = None

    @property
    def is_significant(self) -> bool:
        """통계적 유의성"""
        if self.p_value is not None:
            return self.p_value < 0.05
        return False


@dataclass
class StudyRecord:
    """개별 연구 기록"""
    pmid: Optional[str] = None
    doi: Optional[str] = None
    authors: List[str] = field(default_factory=list)
    title: str = ""
    journal: str = ""
    year: int = 0
    study_type: StudyType = StudyType.IN_VITRO
    sample_size: int = 0
    duration_weeks: Optional[int] = None
    ingredient: str = ""
    concentration: Optional[str] = None
    vehicle: Optional[str] = None
    comparator: Optional[str] = None
    population: Optional[str] = None
    age_range: Optional[Tuple[int, int]] = None
    skin_type: Optional[str] = None
    primary_outcome: Optional[str] = None
    secondary_outcomes: List[str] = field(default_factory=list)
    effect_sizes: List[EffectSize] = field(default_factory=list)
    key_findings: List[str] = field(default_factory=list)
    adverse_events: Optional[str] = None
    quality: StudyQuality = field(default_factory=StudyQuality)

    @property
    def is_rct(self) -> bool:
        """RCT 여부"""
        return self.study_type == StudyType.RCT

    @property
    def is_clinical(self) -> bool:
        """임상 연구 여부"""
        return self.study_type in [
            StudyType.META_ANALYSIS,
            StudyType.SYSTEMATIC_REVIEW,
            StudyType.RCT,
            StudyType.CONTROLLED_TRIAL,
            StudyType.COHORT,
            StudyType.CASE_CONTROL,
            StudyType.CROSS_SECTIONAL,
            StudyType.CASE_SERIES
        ]

    @property
    def citation(self) -> str:
        """인용 형식"""
        first_author = self.authors[0] if self.authors else "Unknown"
        if len(self.authors) > 1:
            author_str = f"{first_author} et al."
        else:
            author_str = first_author
        return f"{author_str} ({self.year})"

    def to_dict(self) -> Dict:
        """딕셔너리 변환"""
        return {
            "pmid": self.pmid,
            "doi": self.doi,
            "authors": self.authors,
            "title": self.title,
            "journal": self.journal,
            "year": self.year,
            "study_type": self.study_type.value,
            "sample_size": self.sample_size,
            "duration_weeks": self.duration_weeks,
            "ingredient": self.ingredient,
            "concentration": self.concentration,
            "key_findings": self.key_findings
        }


@dataclass
class GradeJustification:
    """등급 판정 근거"""
    grade: EvidenceGrade
    rct_count: int
    total_subjects: int
    consistency_score: float
    quality_score: float
    justification: str
    confidence_level: str  # high, moderate, low
    limitations: List[str] = field(default_factory=list)


@dataclass
class EvidenceSummary:
    """근거 요약"""
    ingredient: str
    efficacy: str
    total_studies: int
    total_subjects: int
    rct_count: int
    clinical_count: int
    preclinical_count: int
    evidence_grade: EvidenceGrade
    grade_justification: GradeJustification
    key_findings: List[str] = field(default_factory=list)
    effect_size_range: Optional[str] = None
    optimal_concentration: Optional[str] = None
    recommended_duration: Optional[str] = None
    confidence_level: str = "moderate"
    limitations: List[str] = field(default_factory=list)
    studies: List[StudyRecord] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_table(
        self,
        format: str = "markdown",
        columns: Optional[List[str]] = None,
        sort_by: str = "year",
        language: str = "ko"
    ) -> str:
        """근거 테이블 생성"""
        if columns is None:
            columns = ["study", "year", "design", "n", "duration",
                      "concentration", "key_finding", "quality"]

        # 정렬
        sorted_studies = sorted(
            self.studies,
            key=lambda s: getattr(s, sort_by, 0),
            reverse=True
        )

        if format == "markdown":
            return self._to_markdown_table(sorted_studies, columns, language)
        elif format == "html":
            return self._to_html_table(sorted_studies, columns, language)
        elif format == "latex":
            return self._to_latex_table(sorted_studies, columns, language)
        else:
            return self._to_markdown_table(sorted_studies, columns, language)

    def _to_markdown_table(
        self,
        studies: List[StudyRecord],
        columns: List[str],
        language: str
    ) -> str:
        """Markdown 테이블 생성"""
        headers = self._get_headers(columns, language)

        lines = []
        lines.append(f"## {self.ingredient} {self._get_efficacy_name(language)} 임상 근거\n")
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("|" + "|".join(["------" for _ in headers]) + "|")

        for study in studies:
            row = self._format_row(study, columns)
            lines.append("| " + " | ".join(row) + " |")

        lines.append("")
        lines.append(f"**Evidence Grade: {self.evidence_grade.value}**")
        lines.append(f"**근거 요약**: {self.grade_justification.justification}")

        return "\n".join(lines)

    def _to_html_table(
        self,
        studies: List[StudyRecord],
        columns: List[str],
        language: str
    ) -> str:
        """HTML 테이블 생성"""
        headers = self._get_headers(columns, language)

        html = ['<table class="evidence-table">']
        html.append('<thead><tr>')
        for h in headers:
            html.append(f'<th>{h}</th>')
        html.append('</tr></thead>')

        html.append('<tbody>')
        for study in studies:
            row = self._format_row(study, columns)
            html.append('<tr>')
            for cell in row:
                html.append(f'<td>{cell}</td>')
            html.append('</tr>')
        html.append('</tbody>')
        html.append('</table>')

        return '\n'.join(html)

    def _to_latex_table(
        self,
        studies: List[StudyRecord],
        columns: List[str],
        language: str
    ) -> str:
        """LaTeX 테이블 생성"""
        headers = self._get_headers(columns, language)
        col_format = "l" * len(columns)

        lines = []
        lines.append(f"\\begin{{tabular}}{{{col_format}}}")
        lines.append("\\hline")
        lines.append(" & ".join(headers) + " \\\\")
        lines.append("\\hline")

        for study in studies:
            row = self._format_row(study, columns)
            lines.append(" & ".join(row) + " \\\\")

        lines.append("\\hline")
        lines.append("\\end{tabular}")

        return '\n'.join(lines)

    def _get_headers(self, columns: List[str], language: str) -> List[str]:
        """컬럼 헤더 반환"""
        header_map_ko = {
            "study": "Study",
            "year": "Year",
            "design": "Design",
            "n": "N",
            "duration": "Duration",
            "concentration": "Conc.",
            "key_finding": "Key Finding",
            "quality": "Quality"
        }
        header_map_en = header_map_ko  # 동일하게 사용

        headers = header_map_ko if language == "ko" else header_map_en
        return [headers.get(c, c) for c in columns]

    def _format_row(self, study: StudyRecord, columns: List[str]) -> List[str]:
        """행 데이터 포맷"""
        row = []
        for col in columns:
            if col == "study":
                row.append(study.citation)
            elif col == "year":
                row.append(str(study.year))
            elif col == "design":
                row.append(self._format_study_type(study.study_type))
            elif col == "n":
                row.append(str(study.sample_size))
            elif col == "duration":
                if study.duration_weeks:
                    row.append(f"{study.duration_weeks}주")
                else:
                    row.append("-")
            elif col == "concentration":
                row.append(study.concentration or "-")
            elif col == "key_finding":
                finding = study.key_findings[0] if study.key_findings else "-"
                row.append(finding[:50] + "..." if len(finding) > 50 else finding)
            elif col == "quality":
                row.append(self._format_quality(study.quality))
            else:
                row.append("-")
        return row

    def _format_study_type(self, study_type: StudyType) -> str:
        """연구 유형 포맷"""
        type_map = {
            StudyType.META_ANALYSIS: "MA",
            StudyType.SYSTEMATIC_REVIEW: "SR",
            StudyType.RCT: "RCT",
            StudyType.CONTROLLED_TRIAL: "CT",
            StudyType.COHORT: "Cohort",
            StudyType.CASE_CONTROL: "CC",
            StudyType.CROSS_SECTIONAL: "CS",
            StudyType.CASE_SERIES: "Case",
            StudyType.IN_VIVO: "In vivo",
            StudyType.IN_VITRO: "In vitro",
            StudyType.EX_VIVO: "Ex vivo"
        }
        return type_map.get(study_type, str(study_type.value))

    def _format_quality(self, quality: StudyQuality) -> str:
        """품질 등급 포맷"""
        if quality.jadad_score is not None:
            if quality.jadad_score >= 4:
                return "High"
            elif quality.jadad_score >= 3:
                return "Good"
            elif quality.jadad_score >= 2:
                return "Medium"
            else:
                return "Low"
        return "N/A"

    def _get_efficacy_name(self, language: str) -> str:
        """효능명 반환"""
        efficacy_map_ko = {
            "brightening": "미백",
            "whitening": "미백",
            "anti-aging": "항노화",
            "antiaging": "항노화",
            "moisturizing": "보습",
            "hydrating": "보습",
            "soothing": "진정",
            "anti-inflammatory": "진정",
            "antioxidant": "항산화",
            "barrier": "장벽"
        }
        return efficacy_map_ko.get(self.efficacy.lower(), self.efficacy)

    def to_json(self) -> str:
        """JSON 내보내기"""
        data = {
            "ingredient": self.ingredient,
            "efficacy": self.efficacy,
            "total_studies": self.total_studies,
            "total_subjects": self.total_subjects,
            "rct_count": self.rct_count,
            "evidence_grade": self.evidence_grade.value,
            "key_findings": self.key_findings,
            "effect_size_range": self.effect_size_range,
            "optimal_concentration": self.optimal_concentration,
            "recommended_duration": self.recommended_duration,
            "confidence_level": self.confidence_level,
            "limitations": self.limitations,
            "studies": [s.to_dict() for s in self.studies],
            "generated_at": self.generated_at
        }
        return json.dumps(data, ensure_ascii=False, indent=2)


class EvidenceAggregator:
    """임상 근거 수집 및 평가기"""

    # 효능별 평가 지표
    EFFICACY_METRICS = {
        "brightening": {
            "ITA°": {"significant_change": 3, "unit": "°", "direction": "increase"},
            "Melanin Index": {"significant_change": 10, "unit": "%", "direction": "decrease"},
            "L* value": {"significant_change": 2, "unit": "", "direction": "increase"}
        },
        "anti-aging": {
            "Wrinkle depth": {"significant_change": 10, "unit": "%", "direction": "decrease"},
            "Skin elasticity": {"significant_change": 10, "unit": "%", "direction": "increase"},
            "Skin thickness": {"significant_change": 5, "unit": "%", "direction": "increase"}
        },
        "moisturizing": {
            "Corneometer": {"significant_change": 10, "unit": "%", "direction": "increase"},
            "TEWL": {"significant_change": 10, "unit": "%", "direction": "decrease"}
        },
        "soothing": {
            "Erythema index": {"significant_change": 15, "unit": "%", "direction": "decrease"},
            "TEWL": {"significant_change": 10, "unit": "%", "direction": "decrease"}
        }
    }

    def __init__(self):
        self.studies: List[StudyRecord] = []

    def add_study(self, study: StudyRecord) -> None:
        """연구 추가"""
        self.studies.append(study)

    def aggregate(
        self,
        ingredient: str,
        efficacy: Optional[str] = None,
        min_studies: int = 1,
        study_types: Optional[List[str]] = None,
        year_range: Optional[Tuple[int, int]] = None
    ) -> EvidenceSummary:
        """근거 수집 및 종합"""
        # 필터링
        filtered = self._filter_studies(
            ingredient=ingredient,
            efficacy=efficacy,
            study_types=study_types,
            year_range=year_range
        )

        if len(filtered) < min_studies:
            return self._create_insufficient_evidence(ingredient, efficacy)

        # 통계 계산
        rct_count = sum(1 for s in filtered if s.is_rct)
        clinical_count = sum(1 for s in filtered if s.is_clinical)
        preclinical_count = len(filtered) - clinical_count
        total_subjects = sum(s.sample_size for s in filtered)

        # 등급 산정
        grade_result = self.calculate_evidence_grade(filtered)

        # 주요 발견점 추출
        key_findings = self._extract_key_findings(filtered)

        # 최적 농도/기간 추론
        optimal_conc = self._infer_optimal_concentration(filtered)
        rec_duration = self._infer_recommended_duration(filtered)

        return EvidenceSummary(
            ingredient=ingredient,
            efficacy=efficacy or "general",
            total_studies=len(filtered),
            total_subjects=total_subjects,
            rct_count=rct_count,
            clinical_count=clinical_count,
            preclinical_count=preclinical_count,
            evidence_grade=grade_result.grade,
            grade_justification=grade_result,
            key_findings=key_findings,
            effect_size_range=self._calculate_effect_range(filtered),
            optimal_concentration=optimal_conc,
            recommended_duration=rec_duration,
            confidence_level=grade_result.confidence_level,
            limitations=grade_result.limitations,
            studies=filtered
        )

    def _filter_studies(
        self,
        ingredient: str,
        efficacy: Optional[str] = None,
        study_types: Optional[List[str]] = None,
        year_range: Optional[Tuple[int, int]] = None
    ) -> List[StudyRecord]:
        """연구 필터링"""
        filtered = []

        for study in self.studies:
            # 성분 필터
            if ingredient.lower() not in study.ingredient.lower():
                continue

            # 연도 필터
            if year_range:
                if study.year < year_range[0] or study.year > year_range[1]:
                    continue

            # 연구 유형 필터
            if study_types:
                type_values = [StudyType(t) if isinstance(t, str) else t
                              for t in study_types]
                if study.study_type not in type_values:
                    continue

            filtered.append(study)

        return filtered

    def assess_quality(self, study: StudyRecord) -> StudyQuality:
        """연구 품질 평가"""
        quality = study.quality

        # Jadad 점수 계산 (RCT인 경우)
        if study.is_rct:
            quality.calculate_jadad()

        # 표본 크기 적절성
        n = study.sample_size
        if n >= 100:
            quality.sample_adequacy = SampleAdequacy.EXCELLENT
        elif n >= 50:
            quality.sample_adequacy = SampleAdequacy.GOOD
        elif n >= 30:
            quality.sample_adequacy = SampleAdequacy.ADEQUATE
        elif n >= 20:
            quality.sample_adequacy = SampleAdequacy.LIMITED
        else:
            quality.sample_adequacy = SampleAdequacy.INSUFFICIENT

        return quality

    def calculate_evidence_grade(
        self,
        studies: List[StudyRecord]
    ) -> GradeJustification:
        """근거 등급 계산"""
        if not studies:
            return GradeJustification(
                grade=EvidenceGrade.E,
                rct_count=0,
                total_subjects=0,
                consistency_score=0.0,
                quality_score=0.0,
                justification="근거 부족: 관련 연구를 찾을 수 없음",
                confidence_level="low",
                limitations=["연구 데이터 없음"]
            )

        rct_count = sum(1 for s in studies if s.is_rct)
        total_n = sum(s.sample_size for s in studies)
        consistency = self._assess_consistency(studies)
        quality_score = self._calculate_quality_score(studies)

        # 등급 산정 로직
        if rct_count >= 3 and total_n > 200 and consistency > 0.8:
            grade = EvidenceGrade.A
            justification = "강력한 근거: 다수의 고품질 RCT에서 일관된 결과 확인"
            confidence = "high"
        elif (rct_count >= 1 and total_n > 100) or len(studies) >= 3:
            grade = EvidenceGrade.B
            justification = "적절한 근거: 임상시험에서 효과 확인, 추가 연구로 확증 가능"
            confidence = "moderate"
        elif len(studies) >= 1 and total_n >= 20:
            grade = EvidenceGrade.C
            justification = "제한적 근거: 소규모 연구에서 효과 시사, 추가 검증 필요"
            confidence = "low"
        elif self._has_preclinical_only(studies):
            grade = EvidenceGrade.D
            justification = "예비 근거: 전임상 데이터만 존재, 임상 연구 필요"
            confidence = "very low"
        else:
            grade = EvidenceGrade.E
            justification = "불충분한 근거: 데이터 부족 또는 결과 상충"
            confidence = "very low"

        # 제한점 수집
        limitations = self._identify_limitations(studies, grade)

        return GradeJustification(
            grade=grade,
            rct_count=rct_count,
            total_subjects=total_n,
            consistency_score=consistency,
            quality_score=quality_score,
            justification=justification,
            confidence_level=confidence,
            limitations=limitations
        )

    def _assess_consistency(self, studies: List[StudyRecord]) -> float:
        """결과 일관성 평가 (0-1)"""
        if len(studies) < 2:
            return 0.5  # 단일 연구는 중립

        # 효과 방향 일관성 확인
        positive_effects = 0
        total_with_findings = 0

        for study in studies:
            if study.key_findings:
                total_with_findings += 1
                # 긍정적 효과 확인 (간단한 휴리스틱)
                for finding in study.key_findings:
                    if any(word in finding.lower() for word in
                           ["증가", "감소", "개선", "향상", "significant",
                            "improved", "increased", "decreased", "reduced"]):
                        positive_effects += 1
                        break

        if total_with_findings == 0:
            return 0.5

        return positive_effects / total_with_findings

    def _calculate_quality_score(self, studies: List[StudyRecord]) -> float:
        """평균 품질 점수 (0-1)"""
        if not studies:
            return 0.0

        scores = []
        for study in studies:
            if study.quality.jadad_score is not None:
                scores.append(study.quality.jadad_score / 5.0)
            elif study.is_clinical:
                scores.append(0.5)  # 임상 연구 기본점
            else:
                scores.append(0.3)  # 전임상 연구 기본점

        return sum(scores) / len(scores)

    def _has_preclinical_only(self, studies: List[StudyRecord]) -> bool:
        """전임상 연구만 있는지 확인"""
        return all(not s.is_clinical for s in studies)

    def _identify_limitations(
        self,
        studies: List[StudyRecord],
        grade: EvidenceGrade
    ) -> List[str]:
        """제한점 식별"""
        limitations = []

        total_n = sum(s.sample_size for s in studies)
        rct_count = sum(1 for s in studies if s.is_rct)

        if total_n < 100:
            limitations.append("전체 피험자 수 부족 (n<100)")

        if rct_count == 0:
            limitations.append("무작위 대조 시험 없음")

        if len(studies) < 3:
            limitations.append("재현 연구 부족")

        # 최근 연구 확인
        recent_studies = sum(1 for s in studies if s.year >= 2020)
        if recent_studies == 0:
            limitations.append("최근 연구 없음 (2020년 이후)")

        # 이해충돌 확인
        industry_funded = sum(
            1 for s in studies
            if s.quality.funding_source and
            "industry" in s.quality.funding_source.lower()
        )
        if industry_funded > len(studies) * 0.5:
            limitations.append("대부분의 연구가 산업체 후원")

        return limitations

    def _extract_key_findings(self, studies: List[StudyRecord]) -> List[str]:
        """주요 발견점 추출"""
        all_findings = []
        for study in studies:
            all_findings.extend(study.key_findings)

        # 중복 제거하고 상위 5개 반환
        unique_findings = list(dict.fromkeys(all_findings))
        return unique_findings[:5]

    def _infer_optimal_concentration(
        self,
        studies: List[StudyRecord]
    ) -> Optional[str]:
        """최적 농도 추론"""
        concentrations = {}

        for study in studies:
            if study.concentration and study.key_findings:
                conc = study.concentration
                if conc not in concentrations:
                    concentrations[conc] = 0
                # 긍정적 결과가 있으면 가중치 증가
                if any("significant" in f.lower() or "p<" in f.lower()
                       for f in study.key_findings):
                    concentrations[conc] += 2
                else:
                    concentrations[conc] += 1

        if concentrations:
            return max(concentrations, key=concentrations.get)
        return None

    def _infer_recommended_duration(
        self,
        studies: List[StudyRecord]
    ) -> Optional[str]:
        """권장 기간 추론"""
        durations = []

        for study in studies:
            if study.duration_weeks and study.key_findings:
                durations.append(study.duration_weeks)

        if durations:
            median_duration = sorted(durations)[len(durations)//2]
            return f"{median_duration}주"
        return None

    def _calculate_effect_range(self, studies: List[StudyRecord]) -> Optional[str]:
        """효과 크기 범위 계산"""
        # 간단한 구현 - 실제로는 더 정교한 메타분석 필요
        effects = []

        for study in studies:
            for effect in study.effect_sizes:
                if effect.change_percent is not None:
                    effects.append(effect.change_percent)

        if effects:
            min_effect = min(effects)
            max_effect = max(effects)
            return f"{min_effect:.1f}% ~ {max_effect:.1f}%"
        return None

    def _create_insufficient_evidence(
        self,
        ingredient: str,
        efficacy: Optional[str]
    ) -> EvidenceSummary:
        """불충분한 근거 요약 생성"""
        return EvidenceSummary(
            ingredient=ingredient,
            efficacy=efficacy or "general",
            total_studies=0,
            total_subjects=0,
            rct_count=0,
            clinical_count=0,
            preclinical_count=0,
            evidence_grade=EvidenceGrade.E,
            grade_justification=GradeJustification(
                grade=EvidenceGrade.E,
                rct_count=0,
                total_subjects=0,
                consistency_score=0.0,
                quality_score=0.0,
                justification="관련 연구를 찾을 수 없음",
                confidence_level="very low",
                limitations=["데이터 없음"]
            ),
            key_findings=[],
            confidence_level="very low",
            limitations=["관련 연구 없음"],
            studies=[]
        )

    def generate_summary(
        self,
        evidence: EvidenceSummary,
        style: str = "technical",
        length: str = "medium",
        language: str = "ko"
    ) -> str:
        """근거 요약문 생성"""
        if style == "technical":
            return self._generate_technical_summary(evidence, length, language)
        elif style == "marketing":
            return self._generate_marketing_summary(evidence, length, language)
        elif style == "regulatory":
            return self._generate_regulatory_summary(evidence, length, language)
        else:
            return self._generate_technical_summary(evidence, length, language)

    def _generate_technical_summary(
        self,
        evidence: EvidenceSummary,
        length: str,
        language: str
    ) -> str:
        """기술 요약문 생성"""
        parts = []

        # 개요
        grade_desc = {
            EvidenceGrade.A: "강력한",
            EvidenceGrade.B: "적절한",
            EvidenceGrade.C: "제한적인",
            EvidenceGrade.D: "예비적인",
            EvidenceGrade.E: "불충분한"
        }

        parts.append(
            f"{evidence.ingredient}의 {evidence.efficacy} 효능에 대해 "
            f"{grade_desc[evidence.evidence_grade]} 근거가 확인되었습니다 "
            f"(Grade {evidence.evidence_grade.value})."
        )

        # 연구 현황
        parts.append(
            f"총 {evidence.total_studies}건의 연구 "
            f"(RCT {evidence.rct_count}건, 총 피험자 {evidence.total_subjects}명)를 "
            f"분석하였습니다."
        )

        # 주요 발견
        if evidence.key_findings and length != "short":
            parts.append("주요 발견:")
            for finding in evidence.key_findings[:3]:
                parts.append(f"- {finding}")

        # 최적 조건
        if evidence.optimal_concentration:
            parts.append(f"최적 농도: {evidence.optimal_concentration}")
        if evidence.recommended_duration:
            parts.append(f"권장 사용 기간: {evidence.recommended_duration}")

        # 제한점 (long만)
        if length == "long" and evidence.limitations:
            parts.append("제한점:")
            for limit in evidence.limitations:
                parts.append(f"- {limit}")

        return "\n".join(parts)

    def _generate_marketing_summary(
        self,
        evidence: EvidenceSummary,
        length: str,
        language: str
    ) -> str:
        """마케팅 요약문 생성"""
        if evidence.evidence_grade in [EvidenceGrade.A, EvidenceGrade.B]:
            prefix = "임상적으로 입증된"
        elif evidence.evidence_grade == EvidenceGrade.C:
            prefix = "연구에서 확인된"
        else:
            prefix = "기대되는"

        summary = f"{prefix} {evidence.ingredient}의 {evidence.efficacy} 효과"

        if evidence.key_findings:
            summary += f" - {evidence.key_findings[0]}"

        return summary

    def _generate_regulatory_summary(
        self,
        evidence: EvidenceSummary,
        length: str,
        language: str
    ) -> str:
        """규제 대응용 요약문 생성"""
        parts = []

        parts.append(f"## {evidence.ingredient} 효능 근거 요약")
        parts.append(f"- 대상 효능: {evidence.efficacy}")
        parts.append(f"- 근거 등급: Grade {evidence.evidence_grade.value}")
        parts.append(f"- 분석 연구 수: {evidence.total_studies}건")
        parts.append(f"- 총 피험자 수: {evidence.total_subjects}명")
        parts.append(f"- RCT 수: {evidence.rct_count}건")
        parts.append("")
        parts.append("### 판정 근거")
        parts.append(evidence.grade_justification.justification)

        if evidence.limitations:
            parts.append("")
            parts.append("### 제한점")
            for limit in evidence.limitations:
                parts.append(f"- {limit}")

        return "\n".join(parts)

    def from_pubmed_results(self, pubmed_results: List[Dict]) -> 'EvidenceAggregator':
        """PubMed 검색 결과로부터 연구 추가"""
        for result in pubmed_results:
            study = self._parse_pubmed_result(result)
            if study:
                self.add_study(study)
        return self

    def _parse_pubmed_result(self, result: Dict) -> Optional[StudyRecord]:
        """PubMed 결과 파싱"""
        try:
            # 연구 유형 추론
            study_type = self._infer_study_type(result)

            study = StudyRecord(
                pmid=result.get("pmid"),
                doi=result.get("doi"),
                authors=result.get("authors", []),
                title=result.get("title", ""),
                journal=result.get("journal", ""),
                year=int(result.get("year", 0)),
                study_type=study_type,
                ingredient=result.get("ingredient", ""),
                key_findings=result.get("findings", [])
            )

            return study
        except Exception:
            return None

    def _infer_study_type(self, result: Dict) -> StudyType:
        """연구 유형 추론"""
        title = result.get("title", "").lower()
        abstract = result.get("abstract", "").lower()
        text = title + " " + abstract

        if "meta-analysis" in text:
            return StudyType.META_ANALYSIS
        elif "systematic review" in text:
            return StudyType.SYSTEMATIC_REVIEW
        elif "randomized" in text and "controlled" in text:
            return StudyType.RCT
        elif "controlled trial" in text or "clinical trial" in text:
            return StudyType.CONTROLLED_TRIAL
        elif "cohort" in text:
            return StudyType.COHORT
        elif "in vivo" in text:
            return StudyType.IN_VIVO
        elif "in vitro" in text:
            return StudyType.IN_VITRO
        else:
            return StudyType.CONTROLLED_TRIAL  # 기본값


# 예제 데이터 생성 함수
def create_sample_evidence() -> EvidenceAggregator:
    """샘플 근거 데이터 생성"""
    aggregator = EvidenceAggregator()

    # Niacinamide 미백 연구 예시
    study1 = StudyRecord(
        pmid="12345678",
        authors=["Kim HJ", "Lee SY", "Park JH"],
        title="Double-blind randomized controlled trial of 5% niacinamide for skin brightening",
        journal="J Cosmet Dermatol",
        year=2023,
        study_type=StudyType.RCT,
        sample_size=60,
        duration_weeks=12,
        ingredient="Niacinamide",
        concentration="5%",
        key_findings=["ITA° +4.2 (p<0.01)", "멜라닌 지수 18% 감소"],
        quality=StudyQuality(
            randomization_mentioned=True,
            randomization_appropriate=True,
            blinding_mentioned=True,
            blinding_appropriate=True,
            withdrawals_reported=True,
            bias_risk=BiasRisk.LOW
        )
    )
    study1.quality.calculate_jadad()

    study2 = StudyRecord(
        pmid="23456789",
        authors=["Lee KS", "Park MJ"],
        title="Clinical efficacy of niacinamide on hyperpigmentation",
        journal="Skin Res Technol",
        year=2022,
        study_type=StudyType.RCT,
        sample_size=45,
        duration_weeks=8,
        ingredient="Niacinamide",
        concentration="4%",
        key_findings=["색소 면적 23% 감소 (p<0.05)"],
        quality=StudyQuality(
            randomization_mentioned=True,
            randomization_appropriate=True,
            blinding_mentioned=True,
            withdrawals_reported=True,
            bias_risk=BiasRisk.LOW
        )
    )
    study2.quality.calculate_jadad()

    study3 = StudyRecord(
        pmid="34567890",
        authors=["Park JY", "Kim SH", "Choi EH"],
        title="Open-label study of niacinamide effects on skin tone",
        journal="Ann Dermatol",
        year=2021,
        study_type=StudyType.CONTROLLED_TRIAL,
        sample_size=30,
        duration_weeks=8,
        ingredient="Niacinamide",
        concentration="5%",
        key_findings=["주관적 개선 82%", "L* value +1.8"],
        quality=StudyQuality(
            randomization_mentioned=False,
            blinding_mentioned=False,
            withdrawals_reported=True,
            bias_risk=BiasRisk.SOME_CONCERNS
        )
    )

    aggregator.add_study(study1)
    aggregator.add_study(study2)
    aggregator.add_study(study3)

    return aggregator


if __name__ == "__main__":
    # 사용 예제
    aggregator = create_sample_evidence()

    # 근거 수집
    evidence = aggregator.aggregate(
        ingredient="Niacinamide",
        efficacy="brightening",
        min_studies=1,
        year_range=(2015, 2025)
    )

    # 테이블 출력
    print(evidence.to_table(format="markdown"))
    print()

    # 요약문 출력
    summary = aggregator.generate_summary(
        evidence,
        style="technical",
        length="medium"
    )
    print(summary)
