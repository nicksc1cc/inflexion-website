#!/usr/bin/env python3
"""Inflexion Site Intelligence - Full Pipeline Runner
Manual run: PYTHONPATH=. python3 pipelines/full_run.py
"""

import sys
import os
import json
import datetime
import subprocess
from pathlib import Path

# Add intelligence directory to path
INTELLIGENCE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(INTELLIGENCE_DIR))

try:
    from core.models import (
        JevResult, QuestionTheme, Severity, Ownership, QualityVector, QualityDimension,
        IntelligenceRun, KnowledgeNode, KnowledgeEdge, PageState, PageType
    )
    from core.ingestion import PageIngestion
    from jeev.client import JevClient
except ImportError as e:
    print(f"[ERROR] Import failed: {e}")
    sys.exit(1)


class IntelligencePipeline:
    """Full site intelligence pipeline"""

    def __init__(self, site_root: Path, api_key: str | None = None):
        self.site_root = Path(site_root)
        self.ingestion = PageIngestion(self.site_root)
        self.jev = JevClient(api_key)
        self.results = None

    def get_git_commit(self) -> str:
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                cwd=self.site_root,
                capture_output=True, text=True, timeout=10
            )
            return result.stdout.strip()[:8]
        except:
            return "unknown"

    def run(self) -> IntelligenceRun:
        """Execute the full intelligence pipeline"""
        commit = self.get_git_commit()
        run_id = f"run_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print("\n" + "=" * 60)
        print("INFLEXION SITE INTELLIGENCE")
        print(f"Run: {run_id}")
        print(f"Commit: {commit}")
        print("=" * 60 + "\n")

        # STAGE 1: Ingest all pages
        print("[1/11] INGESTING SITE...")
        page_states = self.ingestion.ingest_all()
        print(f"  ✓ {len(page_states)} pages ingested\n")

        # STAGE 2: Build page state vectors
        print("[2/11] BUILDING PAGE STATE...")
        # Page state is already built during ingestion
        
        # STAGE 3: Extract arguments and claims
        print("[3/11] EXTRACTING ARGUMENTS...")
        # Arguments extracted during ingestion
        
        # STAGE 4: Run Jev evaluation on each page
        print("[4/11] RUNNING JEV EVALUATION...")
        jev_results = {}
        for page_id, state in page_states.items():
            try:
                results = self.jev.evaluate_text(state.body_text[:32000], "", state.title)
                jev_results[page_id] = results
                print(f"  ✓ {page_id}: {len(results)} judgements")
            except Exception as e:
                print(f"  ✗ {page_id}: {e}")
                jev_results[page_id] = []

        # STAGE 5: Build quality vectors
        print("\n[5/11] CALCULATING QUALITY VECTORS...")
        quality_vectors = {}
        for page_id, results in jev_results.items():
            qv = self._build_quality_vector(results)
            quality_vectors[page_id] = qv
            # Also check page state has it
            if page_id in page_states:
                page_states[page_id].quality_vector = qv
            print(f"  ✓ {page_id}: {qv.intellectual_distinctiveness.score:.0f}/100")

        # STAGE 6: Detect relationships
        print("\n[6/11] DETECTING RELATIONSHIPS...")
        nodes, edges = self._build_knowledge_graph(page_states, jev_results)
        print(f"  ✓ {len(nodes)} nodes, {len(edges)} edges")

        # STAGE 7: Run LLM interpretation
        print("\n[7/11] RUNNING LLM INTERPRETATION...")
        interpretations = self._run_llm_interpretation(page_states, jev_results, quality_vectors)
        
        # STAGE 8: Site-wide synthesis
        print("[8/11] SITE-WIDE SYNTHESIS...")
        site_interpretation = self._site_synthesis(page_states, jev_results, quality_vectors, nodes, edges)

        # STAGE 9: Create issues
        print("[9/11] CREATING ISSUES...")
        issues = self._generate_issues(page_states, jev_results, quality_vectors, nodes, edges)

        # STAGE 10: Generate recommendations
        print("[10/11] GENERATING RECOMMENDATIONS AND TICKETS...")
        recommendations, tickets = self._generate_tickets(issues, page_states)

        # STAGE 11: Persist
        print("[11/11] SAVING RUN...")
        run = IntelligenceRun(
            run_id=run_id,
            timestamp=datetime.datetime.now(),
            git_commit=commit,
            pages_analyzed=list(page_states.keys()),
            page_states=page_states,
            jev_results=jev_results,
            quality_vectors=quality_vectors,
            knowledge_nodes=nodes,
            knowledge_edges=edges,
            llm_interpretations=interpretations,
            site_interpretation=site_interpretation,
            issues=issues,
            recommendations=recommendations,
            tickets=tickets,
        )
        
        # Save to data directory
        data_dir = INTELLIGENCE_DIR / "data"
        data_dir.mkdir(exist_ok=True)
        run_path = data_dir / f"{run_id}.json"
        with open(run_path, "w") as f:
            f.write(run.to_json())
        
        print(f"\n  ✓ Saved to: {run_path}")
        
        # Print summary
        self._print_summary(run)
        
        return run

    def _build_quality_vector(self, results: list[JevResult]) -> QualityVector:
        """Build a quality vector from Jev results"""
        themes = {
            "purpose": [r for r in results if r.theme == QuestionTheme.PAGE_PURPOSE],
            "distinctiveness": [r for r in results if r.theme == QuestionTheme.DISTINCTIVENESS],
            "writing": [r for r in results if r.theme == QuestionTheme.HUMAN_WRITING],
            "technical": [r for r in results if r.theme == QuestionTheme.TECHNICAL_PRECISION],
            "evidence": [r for r in results if r.theme == QuestionTheme.EVIDENCE],
            "differentiation": [r for r in results if r.theme == QuestionTheme.SITE_DIFFERENTIATION],
            "writers_eye": [r for r in results if r.theme == QuestionTheme.WRITERS_EYE],
        }
        
        def score_from_results(theme_results: list[JevResult], name: str, positive: list[str]) -> QualityDimension:
            if not theme_results:
                return QualityDimension(name=name, score=50, confidence=0.2, supporting_questions=[], failed_questions=[], issues=[])
            
            positives = 0
            negatives = 0
            supporting = []
            failed = []
            total_conf = 0
            
            for r in theme_results:
                total_conf += r.confidence
                if r.question_id in positive or r.result == "YES":
                    positives += r.confidence
                    supporting.append(r.question_id)
                elif r.result == "NO":
                    negatives += r.confidence
                    failed.append(r.question_id)
            
            total = positives + negatives
            score = (positives / total * 100) if total > 0 else 50
            confidence = total_conf / max(len(theme_results), 1)
            
            issues = []
            if score < 40:
                issues.append(f"Low {name}: key questions failed")
            elif score < 60:
                issues.append(f"Mixed {name}: some indicators weak")
            
            return QualityDimension(name=name, score=round(score, 1), confidence=round(confidence, 2),
                                   supporting_questions=supporting, failed_questions=failed, issues=issues)
        
        return QualityVector(
            intellectual_distinctiveness=score_from_results(themes["distinctiveness"], "Intellectual Distinctiveness", ["has_specific_observation", "uses_specific_mechanics"]),
            evidence_quality=score_from_results(themes["evidence"], "Evidence Quality", ["claims_supported"]),
            subject_specificity=score_from_results(themes["purpose"], "Subject Specificity", ["page_has_purpose", "purpose_statable"]),
            human_writing=score_from_results(themes["writing"], "Human Writing", []),
            structural_quality=QualityDimension(name="Structural Quality", score=60, confidence=0.4, supporting_questions=[], failed_questions=[], issues=[]),
            site_differentiation=score_from_results(themes["differentiation"], "Site Differentiation", []),
            technical_accuracy=score_from_results(themes["technical"], "Technical Accuracy", ["names_technology_correctly", "distinguishes_platforms"]),
            commercial_usefulness=QualityDimension(name="Commercial Usefulness", score=50, confidence=0.3, supporting_questions=[], failed_questions=[], issues=[]),
            editorial_quality=score_from_results(themes["writers_eye"], "Editorial Quality", ["writer_noticed_something", "has_concrete_detail"]),
        )

    def _build_knowledge_graph(self, states: dict, jev_results: dict[str, list[JevResult]]) -> tuple[list, list]:
        """Build a knowledge graph from page states"""
        nodes = []
        edges = []
        
        # Add pages as nodes
        for page_id, state in states.items():
            nodes.append(KnowledgeNode(
                id=f"page:{page_id}",
                node_type="PAGE",
                label=page_id,
                properties={
                    "page_type": state.page_type.value,
                    "url": state.url,
                    "title": state.title[:80],
                }
            ))
            
            # Add arguments as nodes
            for arg in state.arguments:
                arg_id = f"arg:{page_id}:{arg.id}"
                nodes.append(KnowledgeNode(
                    id=arg_id,
                    node_type="ARGUMENT",
                    label=arg.text[:80],
                    properties={"strength": arg.strength}
                ))
                edges.append(KnowledgeEdge(
                    id=f"edge:page_arg:{page_id}:{arg.id}",
                    source=f"page:{page_id}",
                    target=arg_id,
                    relationship="OWNS"
                ))
            
            # Add statistics as nodes
            for stat in state.statistics:
                stat_id = f"stat:{page_id}:{stat.label[:30]}"
                nodes.append(KnowledgeNode(
                    id=stat_id,
                    node_type="STATISTIC",
                    label=f"{stat.value} - {stat.label[:60]}",
                    properties={"source": stat.source}
                ))
                edges.append(KnowledgeEdge(
                    id=f"edge:page_stat:{page_id}:{stat.label[:30]}",
                    source=f"page:{page_id}",
                    target=stat_id,
                    relationship="CITES"
                ))
        
        return nodes, edges

    def _run_llm_interpretation(self, states: dict, jev_results: dict, quality_vectors: dict) -> dict[str, str]:
        """Generate LLM-style interpretations for key pages"""
        interpretations = {}
        
        key_pages = ["aeo", "ai-discovery", "ai-visibility-analytics", "technical-geo", "digital-pr",
                     "retail-media", "amazon", "ai-media", "media", "consultancy", "measurement",
                     "beauty-media-strategy", "ecommerce-whitepaper"]
        
        for page_id in key_pages:
            if page_id not in states:
                continue
            
            state = states[page_id]
            qv = quality_vectors.get(page_id)
            results = jev_results.get(page_id, [])
            
            # Build a concise interpretation
            parts = []
            parts.append(f"PAGE: {page_id} ({state.page_type.value})")
            parts.append(f"TITLE: {state.title[:80]}")
            
            if qv:
                parts.append(f"OVERALL: {qv.overall_score:.0f}/100 weighted quality")
                strong = []
                weak = []
                for dim in [qv.intellectual_distinctiveness, qv.evidence_quality, qv.human_writing, 
                           qv.technical_accuracy, qv.site_differentiation, qv.editorial_quality]:
                    if dim.score >= 60:
                        strong.append(dim.name)
                    elif dim.score < 40:
                        weak.append(dim.name)
                if strong:
                    parts.append(f"STRONG: {', '.join(strong)}")
                if weak:
                    parts.append(f"WEAK: {', '.join(weak)}")
            
            # Evidence patterns
            body_text = state.body_text
            has_overgeneralization = any(p in body_text.lower() for p in ["the algorithm", "ai says", "the model"])
            
            if has_overgeneralization:
                parts.append("POTENTIAL ISSUE: Overgeneralization, 'the algorithm' used as universal mechanism")
            
            # Human writing flags
            not_x_but_y = len([r for r in results if r.question_id == "uses_not_x_but_y" and r.result == "YES"])
            rhetorical = len([r for r in results if r.question_id == "uses_rhetorical_questions" and r.result == "YES"])
            slogans = len([r for r in results if r.question_id == "contains_slogans" and r.result == "YES"])
            
            if not_x_but_y > 0 or rhetorical > 0 or slogans > 0:
                parts.append("WRITING PATTERNS: Some formulaic constructions detected")
            
            interpretations[page_id] = "\n".join(parts)
        
        return interpretations

    def _site_synthesis(self, states: dict, jev_results: dict, quality_vectors: dict, nodes: list, edges: list) -> str:
        """Generate site-wide synthesis"""
        parts = []
        
        parts.append("INFLEXION SITE INTELLIGENCE - SITE SYNTHESIS")
        parts.append("")
        parts.append(f"PAGES: {len(states)}")
        parts.append(f"KNOWLEDGE NODES: {len(nodes)}")
        parts.append(f"KNOWLEDGE EDGES: {len(edges)}")
        parts.append("")
        
        # Topic clusters
        clusters = {
            "AI/DISCOVERY": [],
            "RETAIL/COMMERCE": [],
            "MEDIA": [],
            "STRATEGY": [],
            "RESEARCH": [],
            "OTHER": [],
        }
        
        for page_id, state in states.items():
            pt = state.page_type
            if pt in [PageType.SERVICE]:
                if page_id in ["aeo", "ai-discovery", "ai-visibility-analytics", "technical-geo", "digital-pr"]:
                    clusters["AI/DISCOVERY"].append(page_id)
                elif page_id in ["retail-media", "amazon"]:
                    clusters["RETAIL/COMMERCE"].append(page_id)
                elif page_id in ["ai-media", "media"]:
                    clusters["MEDIA"].append(page_id)
                elif page_id in ["consultancy", "measurement"]:
                    clusters["STRATEGY"].append(page_id)
                else:
                    clusters["OTHER"].append(page_id)
            elif pt == PageType.WHITEPAPER:
                clusters["RESEARCH"].append(page_id)
            elif pt == PageType.THOUGHT_LEADERSHIP:
                clusters["RETAIL/COMMERCE"].append(page_id)
            elif pt == PageType.ARTICLE:
                if "aeo" in page_id or "search" in page_id:
                    clusters["AI/DISCOVERY"].append(page_id)
                elif "media" in page_id or "agentic" in page_id:
                    clusters["MEDIA"].append(page_id)
                elif "amazon" in page_id or "retail" in page_id or "rufus" in page_id:
                    clusters["RETAIL/COMMERCE"].append(page_id)
                else:
                    clusters["OTHER"].append(page_id)
            else:
                clusters["OTHER"].append(page_id)
        
        parts.append("TOPIC CLUSTERS:")
        for cluster, pages in clusters.items():
            if pages:
                parts.append(f"  {cluster}: {', '.join(pages)}")
        
        parts.append("")
        
        # Quality summary
        avg_scores = {}
        for dim_name in ["intellectual_distinctiveness", "evidence_quality", "human_writing", 
                        "technical_accuracy", "site_differentiation", "editorial_quality"]:
            scores = []
            for page_id, qv in quality_vectors.items():
                dim = getattr(qv, dim_name, None)
                if dim and dim.confidence > 0.2:
                    scores.append(dim.score)
            if scores:
                avg_scores[dim_name] = sum(scores) / len(scores)
        
        parts.append("AVERAGE QUALITY SCORES:")
        for name, score in sorted(avg_scores.items(), key=lambda x: x[1]):
            parts.append(f"  {name}: {score:.0f}/100")
        
        parts.append("")
        
        # Top issues
        parts.append("KEY ISSUES DETECTED:")
        
        return "\n".join(parts)

    def _generate_issues(self, states: dict, jev_results: dict, quality_vectors: dict, nodes: list, edges: list) -> list[dict]:
        """Generate structured issues"""
        issues = []
        
        for page_id, state in states.items():
            qv = quality_vectors.get(page_id)
            if not qv:
                continue
            
            # Check critical dimensions
            for dim in qv.critical_dimensions:
                if dim.score < 40 and dim.confidence > 0.3:
                    issues.append({
                        "page": page_id,
                        "dimension": dim.name,
                        "score": dim.score,
                        "confidence": dim.confidence,
                        "severity": "high",
                        "description": f"Low {dim.name} on {page_id}",
                        "failed_questions": dim.failed_questions
                    })
        
        return issues

    def _generate_tickets(self, issues: list[dict], states: dict) -> tuple[list, list]:
        """Generate Hermes editorial tickets"""
        recommendations = []
        tickets = []
        
        for issue in issues:
            if issue["severity"] == "high":
                tickets.append({
                    "page": issue["page"],
                    "problem": issue["description"],
                    "type": issue["dimension"],
                    "severity": issue["severity"],
                    "confidence": issue["confidence"],
                    "required_action": f"Investigate and improve {issue['dimension'].lower()} on {issue['page']}",
                    "success_conditions": [
                        f"{issue['dimension']} score improves",
                        "No critical dimension declines"
                    ]
                })
        
        return recommendations, tickets

    def _print_summary(self, run: IntelligenceRun):
        """Print a summary of the run"""
        print("\n" + "=" * 60)
        print("RUN COMPLETE")
        print("=" * 60)
        print(f"  Run ID: {run.run_id}")
        print(f"  Timestamp: {run.timestamp}")
        print(f"  Commit: {run.git_commit}")
        print(f"  Pages analyzed: {len(run.pages_analyzed)}")
        print(f"  Knowledge graph: {len(run.knowledge_nodes)} nodes, {len(run.knowledge_edges)} edges")
        print(f"  Issues: {len(run.issues)}")
        print(f"  High-priority issues: {len(run.tickets)}")
        print(f"  Tickets generated: {len(run.tickets)}")
        
        if run.tickets:
            print("\n  --- EDITORIAL TICKETS ---")
            for t in run.tickets:
                print(f"  [{t['severity'].upper()}] {t['page']}: {t['problem'][:80]}")
        
        print()


if __name__ == "__main__":
    site_root = Path("~/Projects/04-inflexion/08-Website").expanduser()
    api_key = os.getenv("TYPESAFE_API_KEY")
    
    pipeline = IntelligencePipeline(site_root, api_key)
    pipeline.run()