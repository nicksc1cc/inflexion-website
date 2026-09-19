"""Inflexion Site Intelligence Suite - Core Data Models"""

from __future__ import annotations
import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4


class PageType(Enum):
    HOMEPAGE = "homepage"
    SERVICE = "service"
    THOUGHT_LEADERSHIP = "thought_leadership"
    ARTICLE = "article"
    WHITEPAPER = "whitepaper"
    CONTACT = "contact"
    BLOG_INDEX = "blog_index"
    OTHER = "other"


class QuestionTheme(Enum):
    PAGE_PURPOSE = "page_purpose"
    ARGUMENT_QUALITY = "argument_quality"
    DISTINCTIVENESS = "distinctiveness"
    SITE_DIFFERENTIATION = "site_differentiation"
    HUMAN_WRITING = "human_writing"
    STRUCTURE = "structure"
    EVIDENCE = "evidence"
    TECHNICAL_PRECISION = "technical_precision"
    COMMERCIAL_USEFULNESS = "commercial_usefulness"
    HEADLINES = "headlines"
    REPETITION_SLOP = "repetition_slop"
    WRITERS_EYE = "writers_eye"
    SEO_AEO = "seo_aeo"
    VISUAL_EDITORIAL = "visual_editorial"
    KNOWLEDGE_GRAPH = "knowledge_graph"
    CHANGE_IMPACT = "change_impact"


class Severity(Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Ownership(Enum):
    OWNER = "owner"
    SUPPORTING = "supporting"
    SHARED = "shared"
    DUPLICATIVE = "duplicative"
    UNRESOLVED = "unresolved"


class IssueType(Enum):
    CONTENT = "content"
    STRUCTURE = "structure"
    LANGUAGE = "language"
    TECHNICAL = "technical"
    EVIDENCE = "evidence"
    VISUAL = "visual"
    SITE_ARCHITECTURE = "site_architecture"


@dataclass
class JevResult:
    question_id: str
    theme: QuestionTheme
    result: str  # YES, NO, UNCLEAR, or specific value
    confidence: float
    evidence: list[dict[str, Any]]
    location: Optional[str] = None
    severity: Optional[Severity] = None
    ownership: Optional[Ownership] = None


@dataclass
class Statistic:
    value: str
    label: str
    source: str
    context: str
    date: Optional[str] = None
    page_id: str = ""
    is_vendor_claim: bool = False
    is_forecast: bool = False


@dataclass
class Source:
    name: str
    url: Optional[str]
    type: str  # vendor, independent_research, platform, analyst, government
    date: Optional[str]
    geography: Optional[str] = None
    sample: Optional[str] = None
    methodology: Optional[str] = None


@dataclass
class Claim:
    text: str
    claim_type: str  # factual, vendor_claim, forecast, inference, observation
    evidence: list[Statistic]
    sources: list[Source]
    confidence: float
    location: str


@dataclass
class Argument:
    id: str
    text: str
    argument_type: str  # core, secondary, observation, conclusion, recommendation
    strength: float  # 0-1
    evidence: list[Statistic]
    is_distinctive: bool = False
    is_conventional: bool = False
    owner_page: Optional[str] = None
    supporting_pages: list[str] = field(default_factory=list)
    duplicative_pages: list[str] = field(default_factory=list)


@dataclass
class QualityDimension:
    name: str
    score: float  # 0-100
    confidence: float
    supporting_questions: list[str]
    failed_questions: list[str]
    issues: list[str]


@dataclass
class QualityVector:
    intellectual_distinctiveness: QualityDimension
    evidence_quality: QualityDimension
    subject_specificity: QualityDimension
    human_writing: QualityDimension
    structural_quality: QualityDimension
    site_differentiation: QualityDimension
    technical_accuracy: QualityDimension
    commercial_usefulness: QualityDimension
    editorial_quality: QualityDimension

    @property
    def critical_dimensions(self) -> list[QualityDimension]:
        return [
            self.intellectual_distinctiveness,
            self.evidence_quality,
            self.site_differentiation,
            self.technical_accuracy,
        ]

    @property
    def overall_score(self) -> float:
        dims = [
            self.intellectual_distinctiveness,
            self.evidence_quality,
            self.subject_specificity,
            self.human_writing,
            self.structural_quality,
            self.site_differentiation,
            self.technical_accuracy,
            self.commercial_usefulness,
            self.editorial_quality,
        ]
        return sum(d.score * d.confidence for d in dims) / sum(d.confidence for d in dims)


@dataclass
class PageState:
    page_id: str
    url: str
    file_path: str
    title: str
    meta_title: str
    meta_description: str
    page_type: PageType
    headings: list[str]
    sections: list[dict[str, Any]]
    body_text: str
    claims: list[Claim]
    statistics: list[Statistic]
    sources: list[Source]
    citations: list[str]
    arguments: list[Argument]
    observations: list[str]
    recommendations: list[str]
    conclusions: list[str]
    services: list[str]
    platforms: list[str]
    technologies: list[str]
    concepts: list[str]
    images: list[dict[str, str]]
    internal_links: list[str]
    external_links: list[str]
    source_links: list[str]
    previous_evaluations: list[str]
    quality_vector: Optional[QualityVector] = None
    issues: list[str] = field(default_factory=list)
    protected_content: list[str] = field(default_factory=list)
    relationships: dict[str, list[str]] = field(default_factory=dict)

    def to_dict(self) -> dict:
        result = asdict(self)
        # Fix enum serialization
        result["page_type"] = self.page_type.value
        return result


@dataclass
class KnowledgeNode:
    id: str
    node_type: str  # PAGE, TOPIC, ARGUMENT, CLAIM, EVIDENCE, SOURCE, STATISTIC, PLATFORM, TECHNOLOGY, SERVICE, CONCEPT, OBSERVATION, RECOMMENDATION, ISSUE, IMAGE
    label: str
    properties: dict[str, Any]
    page_ids: list[str] = field(default_factory=list)


@dataclass
class KnowledgeEdge:
    id: str
    source: str
    target: str
    relationship: str  # OWNS, SUPPORTS, EXPANDS, REFERENCES, CITES, DEPENDS_ON, OVERLAPS, DUPLICATES, CONTRADICTS, PRECEDES, SPECIALISES, GENERALISES, EXEMPLIFIES, USES_EVIDENCE, USES_CONCEPT, USES_PLATFORM, USES_SERVICE, LINKS_TO, RELATED_TO
    weight: float = 1.0
    confidence: float = 1.0
    evidence: list[str] = field(default_factory=list)


def _qv_to_dict(qv: QualityVector) -> dict:
    return {
        "intellectual_distinctiveness": qv.intellectual_distinctiveness.__dict__,
        "evidence_quality": qv.evidence_quality.__dict__,
        "subject_specificity": qv.subject_specificity.__dict__,
        "human_writing": qv.human_writing.__dict__,
        "structural_quality": qv.structural_quality.__dict__,
        "site_differentiation": qv.site_differentiation.__dict__,
        "technical_accuracy": qv.technical_accuracy.__dict__,
        "commercial_usefulness": qv.commercial_usefulness.__dict__,
        "editorial_quality": qv.editorial_quality.__dict__,
    }


@dataclass
class IntelligenceRun:
    run_id: str
    timestamp: datetime
    git_commit: str
    pages_analyzed: list[str]
    page_states: dict[str, PageState]
    jev_results: dict[str, list[JevResult]]
    quality_vectors: dict[str, QualityVector]
    knowledge_nodes: list[KnowledgeNode]
    knowledge_edges: list[KnowledgeEdge]
    llm_interpretations: dict[str, str]
    site_interpretation: str
    issues: list[dict[str, Any]]
    recommendations: list[dict[str, Any]]
    tickets: list[dict[str, Any]]

    def to_json(self) -> str:
        return json.dumps({
            "run_id": self.run_id,
            "timestamp": self.timestamp.isoformat(),
            "git_commit": self.git_commit,
            "pages_analyzed": self.pages_analyzed,
            "page_states": {k: v.to_dict() for k, v in self.page_states.items()},
            "jev_results": {k: [r.__dict__ for r in v] for k, v in self.jev_results.items()},
            "quality_vectors": {k: _qv_to_dict(v) for k, v in self.quality_vectors.items()},
            "knowledge_nodes": [n.__dict__ for n in self.knowledge_nodes],
            "knowledge_edges": [e.__dict__ for e in self.knowledge_edges],
            "llm_interpretations": self.llm_interpretations,
            "site_interpretation": self.site_interpretation,
            "issues": self.issues,
            "recommendations": self.recommendations,
            "tickets": self.tickets,
        }, indent=2, default=str)