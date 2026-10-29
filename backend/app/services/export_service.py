import io
import re
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from app.schemas.research import ResearchReport

def safe_pdf_text(text: str) -> str:
    """Sanitizes text for standard ReportLab Helvetica font by replacing unsupported non-Latin Unicode."""
    if not text:
        return ""
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    cleaned = []
    for ch in text:
        if ord(ch) < 256:
            cleaned.append(ch)
        else:
            if ch in ["\u2018", "\u2019"]:
                cleaned.append("'")
            elif ch in ["\u201c", "\u201d"]:
                cleaned.append('"')
            elif ch in ["\u2013", "\u2014"]:
                cleaned.append("-")
            elif ch == "\u2022":
                cleaned.append("•")
    return "".join(cleaned).strip()

def export_report_to_markdown(report: ResearchReport) -> str:
    """Formats full ResearchReport into clean, publication-ready GitHub-flavored Markdown in native UTF-8."""
    lines = []
    lines.append(f"# {report.title}")
    mode_str = "Demo Synthesis" if report.is_demo_mode else "Live Web Research"
    lines.append(f"**Generated:** {report.generated_at} | **Mode:** {mode_str}")
    
    lang = getattr(report, "language", None) or getattr(report, "target_language", "en")
    lang_display = "Telugu (తెలుగు)" if lang == "te" else ("Hindi (हिन्दी)" if lang == "hi" else "English")
    skill_lvl = getattr(report, "skill_level", "beginner")
    study_hrs = getattr(report, "study_time_hours_per_week", None) or getattr(report, "weekly_study_commitment", "10-15")
    
    lines.append(f"**Target Language:** {lang_display} | **Level:** {skill_lvl} | **Pace:** {study_hrs} hrs/week")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # 1. Executive Summary
    lines.append("## 1. Executive Summary")
    lines.append("")
    lines.append(report.executive_summary)
    lines.append("")
    
    # 2. Objective and Scope
    lines.append("## 2. Research Objective & Scope")
    lines.append("")
    lines.append(report.objective_and_scope)
    lines.append("")
    
    # 3. Methodology
    lines.append("## 3. Methodology")
    lines.append("")
    lines.append(report.methodology)
    lines.append("")
    
    # 4. Key Findings
    lines.append("## 4. Key Findings")
    lines.append("")
    for idx, f in enumerate(report.key_findings, 1):
        lines.append(f"### 4.{idx} {f.title} (Confidence: {f.confidence_level})")
        lines.append(f.explanation)
        lines.append("")
        lines.append("**Supporting Evidence:**")
        for ev in f.supporting_evidence:
            lines.append(f"- {ev}")
        if f.caveats:
            lines.append("")
            lines.append(f"> **Caveat / Constraint:** {f.caveats}")
        if f.citations:
            lines.append("")
            lines.append(f"*Citations:* {', '.join(f.citations)}")
        lines.append("")
        
    # 5. Evidence Comparison
    lines.append("## 5. Evidence & Source Comparison Matrix")
    lines.append("")
    lines.append("| Topic / Assertion | Consensus Level | Independent vs Repetition | Rationale |")
    lines.append("| :--- | :--- | :--- | :--- |")
    for item in report.evidence_comparisons:
        clean_topic = item.topic_or_claim.replace("|", "/")
        clean_rat = item.evidence_strength_rationale.replace("|", "/")
        lines.append(f"| **{clean_topic}** | {item.consensus_level} | {item.is_repetition_vs_independent} | {clean_rat} |")
    lines.append("")

    # 6. Conflicts & Uncertainties
    lines.append("## 6. Conflicting Information & Uncertainties")
    lines.append("")
    lines.append(report.conflicts_and_uncertainties)
    lines.append("")

    # 7. Strategic Recommendations
    lines.append("## 7. Strategic Recommendations")
    lines.append("")
    for r in report.strategic_recommendations:
        lines.append(f"- {r}")
    lines.append("")

    # 8. Execution Roadmap & Practical Exercises
    lines.append("## 8. Personalized Execution Roadmap & Study Plan")
    lines.append("")
    lines.append(f"**Total Timeline:** {report.roadmap.total_estimated_timeline}")
    lines.append(f"**Study Commitment:** {study_hrs} hours/week")
    if getattr(report.roadmap, "learning_strategy_summary", None):
        lines.append(f"**Strategy Summary:** {report.roadmap.learning_strategy_summary}")
    lines.append(f"**Planning Assumptions:** {report.roadmap.planning_assumptions}")
    lines.append("")
    for phase in report.roadmap.phases:
        lines.append(f"### {phase.phase_title} ({phase.duration})")
        lines.append(f"**Skills:** {', '.join(phase.skills_covered)}")
        lines.append(f"**Milestone:** *{phase.milestone}*")
        if getattr(phase, "phase_project", None):
            lines.append(f"**Phase Project:** {phase.phase_project}")
        if getattr(phase, "weekly_breakdown", None):
            lines.append("")
            lines.append("**Weekly Breakdown:**")
            for wb in phase.weekly_breakdown:
                lines.append(f"- {wb}")
        lines.append("")
        lines.append("#### Actionable Deliverables & Exercises:")
        for task in phase.tasks:
            status = "[x]" if task.is_completed else "[ ]"
            tag = " *(Agent Planning Estimate)*" if task.is_agent_estimate else ""
            lines.append(f"- {status} **{task.title}**{tag}")
            lines.append(f"  - *Details:* {task.description}")
            lines.append(f"  - *Deliverable:* {task.deliverable}")
            lines.append(f"  - *Criteria:* {task.completion_criteria}")
            if getattr(task, "practical_exercise", None):
                lines.append(f"  - *Practical Exercise:* {task.practical_exercise}")
            if getattr(task, "project_idea", None):
                lines.append(f"  - *Project Idea:* {task.project_idea}")
        lines.append("")

    # 9. Recommended Learning Resources (YouTube & Websites)
    learning_res = getattr(report, "learning_resources", [])
    if learning_res:
        lines.append("## 9. Recommended Learning Resources (YouTube Videos & Websites)")
        lines.append("")
        for res in learning_res:
            res_source = getattr(res, "source", None) or getattr(res, "channel_or_platform", "Web")
            res_lang = getattr(res, "language_label", None) or getattr(res, "language", "en")
            lines.append(f"### [{res.title}]({res.url})")
            lines.append(f"- **Source:** {res_source} | **Type:** {res.resource_type} | **Language:** {res_lang} | **Level:** {res.skill_level}")
            if getattr(res, "description", None):
                lines.append(f"- **Description:** {res.description}")
            lines.append(f"- **Why Useful:** {res.why_useful}")
            lines.append("")

    # 10. Sources & Citations
    lines.append("## 10. Sources & Citations")
    lines.append("")
    for s in report.sources_and_citations:
        date_str = f" ({s.publication_date})" if s.publication_date else ""
        lines.append(f"- **[{s.title}]({s.url})**{date_str} — *{s.publisher}* [{s.source_type.upper()}]")
        snippet = s.snippet.replace('"', "'")
        lines.append(f"  > '{snippet}'")
        lines.append("")

    # 11. Limitations & Follow-Up
    lines.append("## 11. Limitations & Suggested Follow-up Research")
    lines.append("")
    lines.append(report.limitations_and_future_work)
    lines.append("")
    
    return "\n".join(lines)

def export_report_to_pdf(report: ResearchReport) -> bytes:
    """Generates a professional PDF document using ReportLab."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=12
    )
    h2_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=14,
        spaceAfter=8
    )
    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#334155"),
        spaceAfter=6
    )
    bullet_style = ParagraphStyle(
        "BulletItem",
        parent=body_style,
        leftIndent=15,
        spaceAfter=4
    )

    story = []

    # Title & Metadata
    title_text = safe_pdf_text(report.title) or "ResearchFlow AI Strategic Report"
    story.append(Paragraph(title_text, title_style))
    mode_str = "Demo Synthesis" if report.is_demo_mode else "Live Web Research"
    lang = getattr(report, "language", None) or getattr(report, "target_language", "en")
    lang_display = "Telugu" if lang == "te" else ("Hindi" if lang == "hi" else "English")
    skill_lvl = getattr(report, "skill_level", "beginner")
    study_hrs = getattr(report, "study_time_hours_per_week", None) or getattr(report, "weekly_study_commitment", "10-15")
    
    meta_text = f"<b>Generated:</b> {report.generated_at} | <b>Mode:</b> {mode_str} | <b>Language:</b> {lang_display} | <b>Level:</b> {skill_lvl}"
    story.append(Paragraph(meta_text, body_style))
    story.append(Spacer(1, 10))

    # Executive Summary
    story.append(Paragraph("1. Executive Summary", h2_style))
    story.append(Paragraph(safe_pdf_text(report.executive_summary), body_style))
    story.append(Spacer(1, 10))

    # Action Roadmap
    story.append(Paragraph("2. Personalized Action Execution Roadmap", h2_style))
    story.append(Paragraph(f"<b>Estimated Timeline:</b> {report.roadmap.total_estimated_timeline} | <b>Study Time:</b> {study_hrs} hrs/week", body_style))
    for phase in report.roadmap.phases:
        p_title = safe_pdf_text(f"{phase.phase_title} ({phase.duration})")
        story.append(Paragraph(f"<b>{p_title}</b>", body_style))
        story.append(Paragraph(f"<i>Milestone:</i> {safe_pdf_text(phase.milestone)}", body_style))
        for task in phase.tasks:
            t_box = "[X] " if task.is_completed else "[ ] "
            t_text = safe_pdf_text(f"{task.title}: {task.deliverable}")
            story.append(Paragraph(f"{t_box}<b>{t_text}</b>", bullet_style))
        story.append(Spacer(1, 6))

    # Recommended Learning Resources
    learning_res = getattr(report, "learning_resources", [])
    if learning_res:
        story.append(Paragraph("3. Recommended Learning Resources (YouTube & Docs)", h2_style))
        for res in learning_res[:8]:
            res_source = safe_pdf_text(getattr(res, "source", None) or getattr(res, "channel_or_platform", "Web"))
            res_title = safe_pdf_text(res.title)
            res_why = safe_pdf_text(res.why_useful)
            story.append(Paragraph(f"• <b>{res_title}</b> ({res_source})<br/>&nbsp;&nbsp;<font color='#2563eb'>{res.url}</font><br/>&nbsp;&nbsp;{res_why}", bullet_style))
            story.append(Spacer(1, 4))

    # Sources
    story.append(Paragraph("4. Primary Citations and References", h2_style))
    for s in report.sources_and_citations:
        s_title = safe_pdf_text(s.title)
        s_pub = safe_pdf_text(s.publisher or "Web")
        story.append(Paragraph(f"• <b>{s_title}</b> ({s_pub}) — <font color='#2563eb'>{s.url}</font>", bullet_style))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
