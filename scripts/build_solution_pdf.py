from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "NyayaAI_Solution_Document.pdf"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="DocTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=18,
    leading=21, alignment=TA_LEFT, textColor=colors.HexColor("#18324B"), spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="Subtitle", parent=styles["Normal"], fontName="Helvetica", fontSize=9,
    leading=12, textColor=colors.HexColor("#526579"), spaceAfter=9,
))
styles.add(ParagraphStyle(
    name="Section", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=10.5,
    leading=13, textColor=colors.HexColor("#18324B"), spaceBefore=5, spaceAfter=3,
))
styles.add(ParagraphStyle(
    name="BodySmall", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.1,
    leading=10.7, spaceAfter=4, alignment=TA_LEFT,
))
styles.add(ParagraphStyle(
    name="BulletSmall", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.9,
    leading=10, leftIndent=10, firstLineIndent=-6, spaceAfter=2,
))
styles.add(ParagraphStyle(
    name="TableHead", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=7.5,
    leading=9, textColor=colors.white,
))
styles.add(ParagraphStyle(
    name="TableBody", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.3,
    leading=9, textColor=colors.HexColor("#263746"),
))
styles.add(ParagraphStyle(
    name="SmallNote", parent=styles["BodyText"], fontName="Helvetica-Oblique", fontSize=7.4,
    leading=9.2, textColor=colors.HexColor("#526579"), spaceAfter=3,
))


def P(text: str, style="BodySmall"):
    return Paragraph(text, styles[style])


def bullet(text: str):
    return Paragraph("- " + text, styles["BulletSmall"])


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D7E0E8"))
    canvas.setLineWidth(0.5)
    canvas.line(18 * mm, 14 * mm, 192 * mm, 14 * mm)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(colors.HexColor("#667788"))
    canvas.drawString(18 * mm, 9 * mm, "NyayaAI | Kuku AI Generalist Assignment | Problem 2")
    canvas.drawRightString(192 * mm, 9 * mm, f"Page {doc.page} of 2")
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(OUT), pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm,
    topMargin=15 * mm, bottomMargin=19 * mm,
    title="NyayaAI - Solution Document", author="NyayaAI Project",
)
story = []

# PAGE 1
story.append(P("NyayaAI - AI Legal Action Copilot", "DocTitle"))
story.append(P("Kuku AI Generalist Assignment | Problem 2 | Focus: Indian rental security-deposit disputes", "Subtitle"))

story.append(P("Problem choice and scope", "Section"))
story.append(P(
    "I selected Problem 2 and narrowed it to one everyday problem: a tenant vacates a rented home, "
    "but the landlord withholds the security deposit or disputes deductions for repairs or painting. "
    "A narrow scope makes it possible to build and test a useful workflow without claiming to cover "
    "all Indian law. The prototype accepts free-text in English, Hindi or Hinglish and optional PDF/TXT "
    "documents. Voice input, scanned-PDF OCR, formal legal notices and legal representation are outside "
    "the current scope."
))

story.append(P("How the prototype works", "Section"))
for t in [
    "The user describes the dispute and reports the property's city/state. NyayaAI parses selectable PDF text or TXT, then organises the narrative into a case summary, missing-information questions, an evidence checklist, practical next steps and a neutral refund-request draft.",
    "Gemini is called when an API key is configured; otherwise the app clearly identifies its deterministic DEMO simulation. Basic Python checks flag selected urgent situations, instruction-like text in uploaded documents and possible conflicting tenancy dates.",
    "User narratives are labelled USER_REPORTED; extracted document excerpts are labelled DOCUMENT_SUPPORTED. These labels indicate where text came from, not whether it is authentic or legally conclusive.",
]:
    story.append(bullet(t))

story.append(P("AI, code and human roles", "Section"))
data = [
    [P("Part", "TableHead"), P("Responsibility", "TableHead")],
    [P("Gemini", "TableBody"), P("Language understanding, summarisation, missing-information prompts and draft generation.", "TableBody")],
    [P("Deterministic Python", "TableBody"), P("File parsing, source filtering, provenance labels, selected escalation/date checks, exact-quote citation validation and append-only raw-output capture.", "TableBody")],
    [P("Human / advocate", "TableBody"), P("Review disputed facts and drafts; interpret applicable law; handle court proceedings, urgent lockout/eviction risks, imminent deadlines, threats and complex contracts.", "TableBody")],
]
t = Table(data, colWidths=[32 * mm, 142 * mm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#24445F")),
    ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F4F7FA")),
    ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#D7E0E8")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
]))
story.append(t)

story.append(P("M1 research reference", "Section"))
story.append(P(
    "I reviewed the public <link href='https://github.com/SPIKIE-24/LLM' color='#1A6A9A'>SPIKIE-24/LLM</link> "
    "repository as a technical reference. Its README describes M1 as a 12-layer, 768-hidden-size, "
    "12-head multi-head-attention Transformer using RoPE, pre-RMSNorm and GELU. Its Phase 2 legal NER "
    "task uses character-boundary prediction. The public repository contains a README and model notebooks, "
    "but no deployable checkpoints or separate model package. M1 was not integrated: judgment-oriented "
    "labels are not rental-agreement labels, and adaptation requires matching model/tokenizer assets, "
    "rental-specific annotations and separate evaluation. The large local checkpoint and matching assets "
    "are intentionally not part of this submission."
))

story.append(PageBreak())

# PAGE 2
story.append(P("Reliability, evaluation and limitations", "DocTitle"))
story.append(P("Legal reliability and abstention", "Section"))
story.append(P(
    "The local registry currently contains official discovery-portal links only; it has no curated, "
    "versioned statutory passages. Portal URLs are not treated as legal evidence. NyayaAI therefore "
    "abstains from definitive legal citations. If an exact passage is later added, the validator checks "
    "the retrieved source ID, provision and exact quote. This does not determine whether the rule applies "
    "to a particular tenancy or remains legally operative. Missing jurisdiction/evidence and selected "
    "high-risk situations trigger abstention or lawyer-escalation messages."
))

story.append(P("Quality checks", "Section"))
story.append(P(
    "The code audit passes <b>17 automated unit tests</b>. Eight synthetic cases (TC01-TC08) were run "
    "and captured as raw JSON in <b>DEMO mode</b>. These are deterministic simulations, not genuine AI "
    "results, and remain NOT_YET_REVIEWED in the evaluation tracker. Cases cover: deposit not returned; "
    "no written agreement; disputed repair deductions; missing jurisdiction; a request to fabricate law; "
    "a suspicious uploaded notice; an imminent lockout; and conflicting tenancy dates."
))

story.append(P("Known limitations", "Section"))
for t in [
    "The prototype does not yet provide complete field-level extraction or a chronological evidence timeline. Date checks are simple English-language heuristics and may miss unusual wording.",
    "Hindi/Hinglish quality and all live Gemini outputs require manual review. The tool is not legally certified, hallucination-free or a substitute for an advocate.",
    "Scanned/image-only PDFs are not OCR'd. Voice input is not implemented. The browser launch was not verified in the audit environment because Streamlit was not installed and package installation was blocked by unavailable network access.",
    "The eight DEMO outputs are included only to show the pipeline and capture format. No genuine live-model pass rate or legal-accuracy score is claimed.",
]:
    story.append(bullet(t))

story.append(P("A real implementation mistake found and fixed", "Section"))
story.append(P(
    "The first evaluation runner checked that an API key existed but did not pass it into the pipeline. "
    "A requested --live run could therefore fall back to DEMO. I fixed the argument passing, added a guard "
    "that rejects non-live results in live mode, corrected the documented script import path and added "
    "regression tests. The updated code has 17 passing unit tests."
))

story.append(P("Scale and tools", "Section"))
story.append(P(
    "A production version would need a reviewed, jurisdiction- and date-aware corpus of official tenancy "
    "laws, source versioning, stronger multilingual extraction, rental-specific annotated data, a chronological "
    "evidence ledger and advocate review. The model provider can be swapped through the provider adapter. "
    "Tools used: Antigravity/Gemini for the initial scaffold (as supplied in the project workspace), ChatGPT "
    "for code review and implementation fixes, and Python, Streamlit, Pydantic, pypdf, Google GenAI and pytest "
    "in the project."
))

story.append(Spacer(1, 3))
story.append(P(
    "Submission status: runnable repository and setup instructions included; automated tests pass; eight "
    "synthetic DEMO raw records included; live Gemini runs and browser-level validation remain to be performed "
    "with the applicant's own local API key and environment.",
    "SmallNote"
))

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
