from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "NyayaAI_Solution_Document.pdf"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="DocTitle2", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=17.5, leading=20, alignment=TA_LEFT, textColor=colors.HexColor("#17324D"), spaceAfter=3))
styles.add(ParagraphStyle(name="Sub2", parent=styles["Normal"], fontName="Helvetica", fontSize=8.5, leading=11, textColor=colors.HexColor("#536579"), spaceAfter=7))
styles.add(ParagraphStyle(name="Head2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=9.6, leading=11.3, textColor=colors.HexColor("#17324D"), spaceBefore=4, spaceAfter=2))
styles.add(ParagraphStyle(name="Body2", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.65, leading=9.5, textColor=colors.HexColor("#263746"), spaceAfter=3))
styles.add(ParagraphStyle(name="Bullet2", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.45, leading=9.1, leftIndent=9, firstLineIndent=-6, textColor=colors.HexColor("#263746"), spaceAfter=1.6))
styles.add(ParagraphStyle(name="TH2", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=7.1, leading=8.4, textColor=colors.white))
styles.add(ParagraphStyle(name="TB2", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.0, leading=8.5, textColor=colors.HexColor("#263746")))
styles.add(ParagraphStyle(name="Note2", parent=styles["BodyText"], fontName="Helvetica-Oblique", fontSize=7.1, leading=8.6, textColor=colors.HexColor("#536579"), spaceBefore=3))

def P(text, style="Body2"):
    return Paragraph(text, styles[style])

def bullet(text):
    return Paragraph("- " + text, styles["Bullet2"])

def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D5DEE7"))
    canvas.setLineWidth(0.45)
    canvas.line(17*mm, 13*mm, 193*mm, 13*mm)
    canvas.setFont("Helvetica", 6.8)
    canvas.setFillColor(colors.HexColor("#667788"))
    canvas.drawString(17*mm, 8.5*mm, "NyayaAI | Kuku AI Generalist Assignment | Problem 2")
    canvas.drawRightString(193*mm, 8.5*mm, f"Page {doc.page} of 2")
    canvas.restoreState()

doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=17*mm, leftMargin=17*mm, topMargin=13*mm, bottomMargin=17*mm, title="NyayaAI - Kuku Problem 2 Solution", author="NyayaAI project")
story = []

# PAGE ONE: product framing and operating model
story.append(P("NyayaAI - AI Legal Action Copilot", "DocTitle2"))
story.append(P("Kuku AI Generalist Assignment | Problem 2 | Narrow focus: Indian rental security-deposit disputes", "Sub2"))

story.append(P("1. Problem choice and framing", "Head2"))
story.append(P("I chose Problem 2 because everyday rental disputes can leave people unsure what happened, which evidence matters and how to ask for a resolution. I narrowed the product to one recurring situation: a tenant has vacated a rented home, but the landlord has not returned the security deposit or disputes deductions for painting or repairs. This scope is small enough to build and test, while still producing something a tenant can use. The intended user is a tenant who may not know legal terminology or how to organise a claim."))
story.append(P("Assumptions where the brief was open", "Head2"))
for x in [
    "Start with one dispute type, not every area of Indian law; ask the user for the property's city and state rather than assuming jurisdiction.",
    "Accept text in English, Hindi or Hinglish and optional selectable-text PDF/TXT evidence. Voice input, scanned-PDF OCR, court filings and formal legal notices are outside this prototype.",
    "Treat the user's account and document text as reported information, not independently authenticated facts. A human must review any draft before sending it.",
]: story.append(bullet(x))

story.append(P("2. How the prototype works", "Head2"))
story.append(P("The user describes the deposit dispute and enters the property city/state. They can upload a rental agreement, notice or supporting PDF/TXT. NyayaAI extracts selectable text, then organises the story into a case summary, missing-information questions, an evidence checklist, practical next steps and a neutral refund-request draft. The interface makes DEMO versus LIVE model status visible. With an API key, a configurable Gemini provider is called; without one, deterministic simulated output is clearly labelled DEMO."))
story.append(P("The intended output is an organised case file the tenant can review and act on, not a prediction of who will win. A useful result should separate what the user reported from what appears in an uploaded file, make unknowns visible, and help the user prepare a clear, neutral request without inventing legal authority."))

story.append(P("3. What AI does, what code does, and where a human stays involved", "Head2"))
data = [
    [P("Part", "TH2"), P("Responsibility", "TH2")],
    [P("Gemini", "TB2"), P("Understand the user's narrative, organise information, summarise and draft plain-language communication. It is not the source of legal authority.", "TB2")],
    [P("Python", "TB2"), P("Parse PDF/TXT, retrieve only active source records containing exact text, label provenance, flag selected risk/date patterns, validate citation quotes and save append-only raw records.", "TB2")],
    [P("Person / advocate", "TB2"), P("Review facts and drafts. A qualified advocate handles legal interpretation, court matters, imminent eviction/lockout, urgent deadlines, threats and complex contract disputes.", "TB2")],
]
t = Table(data, colWidths=[31*mm, 145*mm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#244761")),
    ("BACKGROUND", (0,1), (-1,-1), colors.HexColor("#F3F6F9")),
    ("GRID", (0,0), (-1,-1), 0.4, colors.HexColor("#D6DFE8")),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 5), ("RIGHTPADDING", (0,0), (-1,-1), 5),
    ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4),
]))
story.append(t)

story.append(P("4. Honesty about law and uncertainty", "Head2"))
story.append(P("The current local registry lists official discovery portals but contains no curated, versioned statutory passages. A portal URL is not treated as legal evidence, so NyayaAI abstains from definitive statutory citations. If exact source text is added later, the validator checks whether the source was retrieved and whether its provision label and quotation match. This does not prove that the provision applies to the user's facts or is still in force. The app flags selected high-risk situations for human help, but its rules can miss unusual wording. NyayaAI is not hallucination-free, legally certified or a substitute for an advocate."))

story.append(PageBreak())

# PAGE TWO: evidence, failures, learning, scale and tools
story.append(P("Evaluation, failures and what I learned", "DocTitle2"))
story.append(P("5. Quality checking against the assignment", "Head2"))
story.append(P("I wrote eight synthetic cases because Problem 2 provides no input pack. They cover: TC01 deposit not returned; TC02 no written agreement; TC03 disputed repair deductions; TC04 missing jurisdiction; TC05 a request to invent a legal provision; TC06 suspicious instructions in an uploaded notice; TC07 imminent forced lockout; and TC08 conflicting tenancy dates. The cases and timestamped raw JSON outputs are included in the repository under `data/synthetic_cases.json` and `outputs/raw/`."))
story.append(P("The recorded code audit passed <b>17 automated unit tests</b>. The eight end-to-end records currently included were generated in deterministic <b>DEMO mode</b>, not by Gemini. They demonstrate the safety workflow and output-capture format; they are not live-AI results, legal-accuracy evidence or a human-reviewed pass rate. The evaluation tracker therefore remains unreviewed. Live cases must be run and manually scored before being described as passed."))

story.append(P("6. A real failure and how I handled it", "Head2"))
story.append(P("My first local version opened, but it displayed DEMO MODE because I had not configured a live API key. I initially spent time waiting for an automated coding agent that was not showing visible progress. I changed approach: I narrowed the scope, inspected the project structure, checked the provider and pipeline separately, and used VS Code and Git to make the work reproducible. During review I found that the evaluation runner checked for an API key but did not pass it into the pipeline, so a requested live run could fall back to DEMO. I fixed the key hand-off, added a guard against non-live results in live mode, corrected the documented launch path and added regression tests."))
story.append(P("After deployment, a live Gemini request returned HTTP 503, reporting temporary model unavailability. The Streamlit application itself remained available; the failure was at the model service. I kept the error visible, changed the model selection and retried rather than presenting the failed call as a successful AI answer. This showed me that a working interface, a reachable API and a reliable answer are different things. Model availability and live-answer quality still need repeat testing."))

story.append(P("7. Known limitations and where it fails", "Head2"))
for x in [
    "No verified statutory passage is preloaded, so definitive legal citations are withheld. A citation quote match is not a legal applicability check.",
    "Voice input, scanned-PDF OCR, full field-level extraction and a complete chronological evidence ledger are not implemented. Date and escalation checks are simple heuristics and can miss edge cases.",
    "Hindi/Hinglish quality and all live outputs need manual review. Synthetic cases are not representative of all real disputes; the eight DEMO runs do not establish Gemini accuracy.",
]: story.append(bullet(x))

story.append(P("8. Scale, cost and next validation", "Head2"))
story.append(P("The same workflow could expand to other everyday dispute types only after building and testing separate intake schemas, evidence checklists and reviewed source collections for each area. For rental disputes, the next scale step is a jurisdiction- and date-aware corpus of official state tenancy material, rental-specific annotated examples, stronger multilingual extraction, a structured event/evidence ledger, model/API monitoring and advocate review for high-risk cases. The prototype uses a swappable provider adapter; a paid API may improve throughput or quality, but this MVP is intentionally built to run with a configurable API and a DEMO fallback. API usage still has provider-dependent costs and limits."))

story.append(P("9. Tools used and applicant's role", "Head2"))
story.append(P("Tools used: Antigravity and Gemini during initial prototyping; ChatGPT for code generation, review and debugging; VS Code for local development; Python, Streamlit, Pydantic, pypdf, Google GenAI SDK and pytest for implementation; GitHub for version control; and Streamlit Community Cloud for deployment. I used AI assistance but reviewed the project structure, selected the narrow problem, configured and ran the application, checked the test records, fixed the live-runner issue, pushed the repository and deployed the prototype. ChatGPT-assisted code was not assumed to be correct; the API-key hand-off bug was found during review and fixed."))

story.append(Spacer(1, 2))
story.append(P("Submission evidence: public runnable repository and deployed Streamlit prototype; Windows run instructions; eight synthetic test inputs and raw DEMO outputs; evaluation tracker; and this two-page solution note. Automated tests passed in the recorded audit. Genuine live end-to-end cases and manual scoring remain pending. No deployment, legal certification or accuracy claim is made beyond the evidence above.", "Note2"))

doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
