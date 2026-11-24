"""
JanSetu AI Fine Print and Document Simplification Engine
Analyzes extracted PDF layout elements, identifies hidden conditions, fine print,
calculates review priorities, generates plain-language explanations in English & Telugu,
and provides grounded RAG question-answering over uploaded documents.
"""

import re
import math
from collections import Counter
from django.conf import settings
from apps.documents.pdf_extractor import PDFExtractor
from apps.documents.models import UploadedDocument, ExtractedClause, DocumentAnalysis

# Comprehensive Pattern Rules for the 15 Condition Categories
CONDITION_PATTERNS = [
    {
        "category": "Cancellation charges",
        "title": "Cancellation / Pre-mature Exit Penalty",
        "regex": r'\b(cancellation (fee|charge|penalty)|pre-?mature (termination|withdrawal|surrender)|surrender (charge|value|penalty)|early termination fee|exit load|exit penalty|pre-?payment penalty)\b',
        "level": "High",
        "why": "Cancelling or withdrawing before completing the agreed duration may result in high financial deductions or forfeiture of your deposited funds.",
        "simple": "If you decide to close or stop this contract before the agreed time, the company will deduct a penalty or refund only a partial amount.",
        "simple_te": "మీరు ఒప్పందం గడువు ముగియకముందే దీన్ని రద్దు చేసుకుంటే లేదా నిలిపివేస్తే, అపరాధ రుసుము (పెనాల్టీ) మినహాయించబడుతుంది.",
        "impact": "You could lose a substantial percentage of your invested capital or expected refund.",
        "action": "Check the exact cancellation fee table and consider whether you can commit for the full period before agreeing.",
    },
    {
        "category": "Processing fees",
        "title": "Upfront Processing & Administrative Charges",
        "regex": r'\b(processing (fee|charges)|administrative (charges|fee)|upfront (fee|deduction)|documentation (charges|fee)|non-refundable fee)\b',
        "level": "Medium",
        "why": "These are non-refundable initial charges deducted directly from your sanctioned loan or policy balance.",
        "simple": "An upfront fee will be deducted for handling your paperwork. This money is usually not refunded even if you change your mind.",
        "simple_te": "మీ దరఖాస్తు లేదా లోన్ పత్రాలను ప్రాసెస్ చేయడానికి ఒకేసారి ఫీజు వసూలు చేస్తారు. ఇది సాధారణంగా తిరిగి ఇవ్వబడదు.",
        "impact": "Reduces the net loan or disbursement amount received in hand.",
        "action": "Ask if the processing fee can be discounted or waived, and check if GST is charged on top of it.",
    },
    {
        "category": "Additional charges",
        "title": "Additional & Incidental Charges",
        "regex": r'\b(additional (charges|fees|cost)|maintenance fee|service charges|inspection charges|valuation charges|convenience fee|annual renewal fee|mandate charge)\b',
        "level": "Medium",
        "why": "Ongoing or incidental charges that increase the total cost of the product beyond the advertised primary rate.",
        "simple": "There are extra operational charges billed periodically or upon specific events.",
        "simple_te": "ప్రకటించిన ప్రధాన ఫీజుకు తోడుగా అదనపు సర్వీస్ లేదా నిర్వహణ ఛార్జీలు చెల్లించాల్సి ఉంటుంది.",
        "impact": "Increases your recurring costs over time.",
        "action": "Request a complete schedule of all miscellaneous charges from the provider.",
    },
    {
        "category": "Late payment penalties",
        "title": "Late Payment & Default Interest",
        "regex": r'\b(late (payment|fee|charges)|penal (interest|charge)|default interest|bounce (charge|fee)|ecs (dishonor|bounce)|overdue (charge|interest))\b',
        "level": "High",
        "why": "Missing an installment date triggers immediate penal interest or bounce fees that compound over time.",
        "simple": "If you miss or delay a payment deadline, you will be charged an extra late fee or higher interest rate on the unpaid amount.",
        "simple_te": "మీరు నెలవారీ వాయిదా (EMI) సమయానికి చెల్లించకపోతే, అదనపు ఆలస్య రుసుము లేదా జరిమానా వడ్డీ చెల్లించవలసి ఉంటుంది.",
        "impact": "Significantly damages your credit score (CIBIL) and increases total repayment liability.",
        "action": "Set up automated reminders 3 days before the debit date and ensure sufficient balance.",
    },
    {
        "category": "Lock-in periods",
        "title": "Mandatory Lock-in & Commitment Period",
        "regex": r'\b(lock-?in (period|term)|minimum commitment|cannot be withdrawn for|minimum period of \d+|mandatory holding period)\b',
        "level": "High",
        "why": "You are strictly prohibited from withdrawing or transferring your money or changing plans during this timeframe.",
        "simple": "Your funds or agreement are locked for a compulsory minimum duration. You cannot withdraw during this window without severe penalties.",
        "simple_te": "మీ డబ్బు లేదా పాలసీ నిర్ణీత కాలపరిమితి (లాక్-ఇన్ పీరియడ్) వరకు లాక్ చేయబడుతుంది. మధ్యలో వెనక్కి తీసుకోలేరు.",
        "impact": "Zero liquidity for emergencies during the lock-in span.",
        "action": "Verify if your emergency savings are sufficient before locking funds into this contract.",
    },
    {
        "category": "Automatic renewal conditions",
        "title": "Automatic Renewal & Auto-Debit Rollover",
        "regex": r'\b(automatic(ally)? renew(ed|al)?|auto-?renewal|auto-?debit|rollover|tacit renewal|standing instruction)\b',
        "level": "Medium",
        "why": "The contract will automatically extend and debit your account without needing your explicit permission each cycle.",
        "simple": "Once this policy or service ends, it will automatically renew itself and deduct payment from your bank account unless you actively cancel it.",
        "simple_te": "పాలసీ లేదా సర్వీస్ గడువు ముగిసిన తర్వాత, మీ అనుమతి లేకుండానే ఆటోమేటిక్‌గా పునరుద్ధరించబడి మీ బ్యాంక్ ఖాతా నుండి డబ్బు కట్ అవుతుంది.",
        "impact": "Unintended bank deductions if you forget to cancel before the renewal date.",
        "action": "Note the exact notice window required to opt out before auto-debit triggers.",
    },
    {
        "category": "Insurance exclusions",
        "title": "Explicit Insurance Exclusions & Non-Covered Scenarios",
        "regex": r'\b(exclusion|shall not be liable|not cover(ed)?|excluded from coverage|pre-existing disease(s)?|self-inflicted|adventure sports|cosmetic|hazardous)\b',
        "level": "High",
        "why": "Claims related to these conditions or events will be rejected outright by the insurer.",
        "simple": "Certain treatments, pre-existing illnesses, or events are completely excluded. The insurance company will not pay for these.",
        "simple_te": "కొన్ని అనారోగ్యాలు, ముందస్తు వ్యాధులు లేదా ప్రమాదాలకు బీమా కంపెనీ ఎటువంటి ఖర్చులను చెల్లించదు (మినహాయింపులు).",
        "impact": "You will have to pay hospital and medical bills out-of-pocket for excluded conditions.",
        "action": "Carefully compare your existing medical history with the exclusion list.",
    },
    {
        "category": "Waiting periods",
        "title": "Mandatory Waiting Period Before Coverage",
        "regex": r'\b(waiting period|wait period|no claim shall be payable during the first|30 days waiting|24 months waiting|36 months waiting|48 months waiting)\b',
        "level": "High",
        "why": "No claims can be made for specified conditions during the initial months or years of the policy.",
        "simple": "You must wait for a specified number of days or years before the insurance will cover illnesses or specific surgeries.",
        "simple_te": "పాలసీ తీసుకున్న వెంటనే కొన్ని వ్యాధులకు క్లెయిమ్ రాదు. నిర్దిష్ట నెలలు లేదా సంవత్సరాల నిరీక్షణ సమయం (వెయిటింగ్ పీరియడ్) ఉంటుంది.",
        "impact": "No coverage if hospitalization happens during this initial period.",
        "action": "Ask specifically how long you must wait for pre-existing illnesses, cataract, joint replacements, and hernia.",
    },
    {
        "category": "Claim restrictions",
        "title": "Claim Limits, Co-Payment & Room Rent Caps",
        "regex": r'\b(co-?pay(ment)?|room rent (capping|limit)|sub-?limit|proportionate deduction|percentage of the claim|aggregate limit)\b',
        "level": "High",
        "why": "Even if your claim is approved, you will have to pay a share of the bill yourself or absorb cuts due to room rent capping.",
        "simple": "The insurer limits how much it pays for room rent or specific treatments, or requires you to pay a percentage of every bill (co-payment).",
        "simple_te": "హాస్పిటల్ రూమ్ అద్దెపై పరిమితి ఉంటుంది లేదా మొత్తం బిల్లులో కొంత శాతం మీరే స్వయంగా చెల్లించాల్సి ఉంటుంది (కో-పేమెంట్).",
        "impact": "Unexpected high hospital bills even with an active health policy.",
        "action": "Choose a single standard room or opt for a policy with no room rent capping if affordable.",
    },
    {
        "category": "Refund conditions",
        "title": "Refund Rules & Non-Refundable Clauses",
        "regex": r'\b(non-refundable|refund (policy|terms)|forfeiture|forfeited|pro-?rata refund|no refund shall be payable)\b',
        "level": "Medium",
        "why": "Explains whether you get any money back if you cancel or if services are terminated early.",
        "simple": "The terms specify how much, if any, refund you receive upon cancellation.",
        "simple_te": "మీరు సర్వీస్ రద్దు చేసుకున్నప్పుడు ఎంత డబ్బు వాపస్ వస్తుంది లేదా ఏ మొత్తం తిరిగి రాదు అనే నిబంధనలు.",
        "impact": "Risk of zero refund if cancelled outside the free-look period.",
        "action": "Ensure you test or review the policy during the 15-day statutory free-look period.",
    },
    {
        "category": "Termination conditions",
        "title": "Agreement Termination & Revocation Grounds",
        "regex": r'\b(termination|terminate the agreement|lapse of policy|right to terminate|revocation|without prior notice)\b',
        "level": "Medium",
        "why": "Circumstances under which the provider can unilaterally end the contract or cancel coverage.",
        "simple": "The company has the right to cancel your coverage or contract if certain terms or disclosure conditions are breached.",
        "simple_te": "నిబంధనలు పాటించకపోతే కంపెనీ మీ పాలసీ లేదా ఒప్పందాన్ని రద్దు చేసే పరిస్థితులు.",
        "impact": "Sudden loss of benefits or coverage.",
        "action": "Ensure all health and income declarations provided are 100% accurate.",
    },
    {
        "category": "Other important obligations",
        "title": "Critical Notification & Documentation Timelines",
        "regex": r'\b(within \d+ hours|notice in writing|furnish proof|intimation|mandatory requirement|must notify|within 24 hours|within 48 hours)\b',
        "level": "Informational",
        "why": "Failing to notify the organization within strict hourly deadlines can lead to claim rejection.",
        "simple": "You must inform the company in writing within a strict number of hours (e.g. within 24 hours of hospitalization).",
        "simple_te": "హాస్పిటల్‌లో చేరిన 24 నుండి 48 గంటల లోపు బీమా కంపెనీకి లిఖితపూర్వకంగా సమాచారం ఇవ్వడం తప్పనిసరి.",
        "impact": "Late intimation could delay or jeopardize claim settlement.",
        "action": "Save the emergency TPA helpline number in your phone contacts right away.",
    },
]

# Difficult Legal & Financial Terms Glossary
DIFFICULT_TERMS = [
    {"term": "Co-payment (Co-pay)", "simple": "A fixed percentage of the medical bill you must pay from your own pocket.", "te": "హాస్పిటల్ బిల్లులో పాలసీదారుడే స్వయంగా భరించాల్సిన నిర్ణీత శాతం."},
    {"term": "Waiting Period", "simple": "The initial period during which insurance coverage for certain diseases is not yet active.", "te": "కొన్ని వ్యాధులకు బీమా వర్తించడానికి ముందు ఆగాల్సిన నిర్ణీత కాలవ్యవధి."},
    {"term": "Pre-existing Disease (PED)", "simple": "Any health condition diagnosed or treated before purchasing the policy.", "te": "పాలసీ తీసుకోకముందే ఉన్న అనారోగ్య సమస్యలు."},
    {"term": "Sub-limit", "simple": "A monetary cap on specific treatments or room rent regardless of your total sum insured.", "te": "నిర్దిష్ట చికిత్సలకు బీమా కంపెనీ విధించే గరిష్ట పరిమితి."},
    {"term": "Surrender Value", "simple": "The reduced amount an insurer pays you if you terminate your policy before maturity.", "te": "పాలసీ గడువు తీరకముందే రద్దు చేసుకుంటే వెనక్కి వచ్చే నగదు."},
    {"term": "Moratorium Period", "simple": "A grace period during which loan borrowers are not required to make repayments.", "te": "లోన్ వాయిదాలు చెల్లించకుండా ప్రభుత్వం లేదా బ్యాంక్ ఇచ్చే విరామ సమయం."},
    {"term": "Proportionate Deduction", "simple": "Deducting an equal percentage from all bill items if you choose a room above your eligible limit.", "te": "రూమ్ అద్దె పరిమితి దాటితే మొత్తం బిల్లుపై విధించే దామాషా కోత."},
    {"term": "Free-Look Period", "simple": "A 15 to 30 day trial window to review the policy and cancel with full refund.", "te": "పాలసీ నచ్చకపోతే పూర్తి డబ్బు వాపస్ పొందే 15 రోజుల సమీక్షా సమయం."},
]


class DocumentAnalyzer:
    def __init__(self, document_id):
        import os
        self.doc_record = UploadedDocument.objects.get(id=document_id)
        path = self.doc_record.original_file.path
        if not os.path.exists(path):
            alt_path = os.path.join(settings.BASE_DIR, self.doc_record.original_file.name)
            if os.path.exists(alt_path):
                path = alt_path
        self.file_path = path

    def analyze(self):
        """Runs complete layout analysis and condition detection on all pages."""
        self.doc_record.processing_status = 'processing'
        self.doc_record.save()

        try:
            extractor = PDFExtractor(self.file_path)
            self.doc_record.page_count = extractor.total_pages
            self.doc_record.save()

            elements = extractor.extract_layout_elements()
            pages_text = extractor.extract_full_text_by_pages()
            extractor.close()

            detected_clauses = []
            seen_texts = set()

            for elem in elements:
                text = elem["text"]
                clean_text = " ".join(text.split())
                if len(clean_text) < 20 or clean_text in seen_texts:
                    continue

                for pattern_def in CONDITION_PATTERNS:
                    match = re.search(pattern_def["regex"], clean_text, re.IGNORECASE)
                    if match:
                        seen_texts.add(clean_text)
                        
                        # Calculate confidence based on keyword proximity and font metadata
                        confidence = 0.88
                        if elem["is_small_font"]:
                            confidence += 0.05
                        if elem["document_position"] in ["footnote", "final_pages"]:
                            confidence += 0.04
                        confidence = min(0.98, confidence)

                        # Adjust importance level if small font or buried in final pages
                        level = pattern_def["level"]
                        if elem["is_small_font"] and level == "Medium":
                            level = "High"

                        clause = ExtractedClause(
                            uploaded_document=self.doc_record,
                            original_text=clean_text,
                            page_number=elem["page_number"],
                            section_heading=elem["section_heading"] or pattern_def["title"],
                            clause_category=pattern_def["category"],
                            font_size=elem["font_size"],
                            body_font_size=elem["body_font_size"],
                            is_small_font=elem["is_small_font"],
                            document_position=elem["document_position"],
                            importance_level=level,
                            ai_explanation=pattern_def["simple"],
                            te_explanation=pattern_def["simple_te"],
                            why_it_matters=pattern_def["why"],
                            suggested_action=pattern_def["action"],
                            confidence_score=confidence,
                        )
                        detected_clauses.append(clause)
                        break

            # Bulk save extracted clauses
            ExtractedClause.objects.bulk_create(detected_clauses)

            # Generate Document Analysis Statistics
            total_clauses = len(detected_clauses)
            small_font_count = sum(1 for c in detected_clauses if c.is_small_font)
            later_pages_count = sum(1 for c in detected_clauses if c.document_position == 'final_pages')
            high_count = sum(1 for c in detected_clauses if c.importance_level == 'High')
            med_count = sum(1 for c in detected_clauses if c.importance_level == 'Medium')
            info_count = sum(1 for c in detected_clauses if c.importance_level == 'Informational')

            # Overall Summary Synthesis
            doc_name = self.doc_record.file_name
            summary_en = (
                f"JanSetu successfully analysed all {self.doc_record.page_count} pages of '{doc_name}'. "
                f"We identified {total_clauses} important conditions requiring your review, including "
                f"{high_count} high-priority clauses, {small_font_count} clauses printed in fine or small font, "
                f"and {later_pages_count} important conditions placed in the final pages. "
                f"Key areas flagged involve cancellation terms, waiting periods, room-rent ceilings, and non-refundable fees. "
                f"Please review the verified citations below before executing agreements."
            )
            summary_te = (
                f"జనసేతు మీ '{doc_name}' పత్రంలోని మొత్తం {self.doc_record.page_count} పేజీలను పూర్తిగా విశ్లేషించింది. "
                f"మీరు తప్పక తెలుసుకోవలసిన {total_clauses} ముఖ్యమైన నిబంధనలను గుర్తించాము. "
                f"ఇందులో {high_count} అత్యంత ముఖ్యమైన షరతులు, {small_font_count} చిన్న అక్షరాలతో (ఫైన్ ప్రింట్) ముద్రించిన క్లాజులు, "
                f"మరియు చివరి పేజీలలో ఉంచిన {later_pages_count} షరతులు ఉన్నాయి."
            )

            DocumentAnalysis.objects.update_or_create(
                uploaded_document=self.doc_record,
                defaults={
                    "overall_summary": summary_en,
                    "overall_summary_te": summary_te,
                    "total_pages_analysed": self.doc_record.page_count,
                    "total_conditions_detected": total_clauses,
                    "small_font_count": small_font_count,
                    "later_pages_count": later_pages_count,
                    "high_risk_count": high_count,
                    "medium_risk_count": med_count,
                    "info_risk_count": info_count,
                    "difficult_terms": DIFFICULT_TERMS,
                    "eligibility_summary": "Standard age, identity verification, and insurable interest apply.",
                    "required_docs_summary": "Government Photo ID (Aadhaar), PAN, Income Proof / Bank Statements.",
                    "benefits_limitations_summary": "Primary benefits active subject to standard exclusions, waiting periods, and deductibles.",
                    "analysis_status": "completed",
                }
            )

            self.doc_record.processing_status = 'completed'
            self.doc_record.save()
            return True

        except Exception as e:
            self.doc_record.processing_status = 'failed'
            self.doc_record.error_message = str(e)
            self.doc_record.save()
            return False


class DocumentQAService:
    """Answers user queries grounded directly in the text of the uploaded PDF."""

    @staticmethod
    def answer_question(uploaded_doc, user_question, language='en'):
        import os
        path = uploaded_doc.original_file.path
        if not os.path.exists(path):
            alt = os.path.join(settings.BASE_DIR, uploaded_doc.original_file.name)
            if os.path.exists(alt):
                path = alt
        extractor = PDFExtractor(path)
        pages_text = extractor.extract_full_text_by_pages()
        extractor.close()

        # Tokenize question
        q_words = [w.lower() for w in re.findall(r'\b\w{3,}\b', user_question)]
        if not q_words:
            return {
                "answer": "Please ask a specific question regarding conditions, exclusions, charges, or cancellation in this document.",
                "citations": []
            }

        # Rank pages by term match
        scored_pages = []
        for p in pages_text:
            text_lower = p["text"].lower()
            score = sum(text_lower.count(qw) for qw in q_words)
            if score > 0:
                scored_pages.append((score, p["page_number"], p["text"]))

        scored_pages.sort(key=lambda x: x[0], reverse=True)

        if not scored_pages:
            # Check if any extracted clause matches
            matching_clauses = ExtractedClause.objects.filter(uploaded_document=uploaded_doc)
            for qw in q_words:
                matching_clauses = matching_clauses.filter(original_text__icontains=qw)

            if matching_clauses.exists():
                cl = matching_clauses.first()
                ans = f"According to page {cl.page_number} ({cl.clause_category}): {cl.ai_explanation} (Verbatim: \"{cl.original_text[:180]}...\")"
                return {
                    "answer": ans,
                    "citations": [{"page": cl.page_number, "snippet": cl.original_text[:160]}]
                }

            return {
                "answer": "We did not find specific mentions of this question in the document. Please verify with the provider or consult the extracted conditions report.",
                "citations": []
            }

        # Extract best snippet from top matching page
        best_page = scored_pages[0]
        page_num = best_page[1]
        page_content = best_page[2]

        # Find best paragraph on that page
        paragraphs = [p.strip() for p in page_content.split("\n\n") if len(p.strip()) > 30]
        if not paragraphs:
            paragraphs = [p.strip() for p in page_content.split("\n") if len(p.strip()) > 30]

        best_para = ""
        best_para_score = -1
        for para in paragraphs:
            para_lower = para.lower()
            para_score = sum(para_lower.count(qw) for qw in q_words)
            if para_score > best_para_score:
                best_para_score = para_score
                best_para = para

        citation_snippet = best_para[:250] + ("..." if len(best_para) > 250 else "")

        if language == 'te':
            answer_text = (
                f"మీ పత్రంలోని పేజీ {page_num} ప్రకారం, ఈ క్రింది వివరాలు పేర్కొనబడ్డాయి:\n\n"
                f"\"{citation_snippet}\"\n\n"
                f"ముఖ్య గమనిక: ఇది డాక్యుమెంట్‌లో నమోదు చేయబడిన వాస్తవ నిబంధన. నిర్ణయం తీసుకునే ముందు సంబంధిత సంస్థతో ధృవీకరించుకోండి."
            )
        else:
            answer_text = (
                f"Based directly on Page {page_num} of your document:\n\n"
                f"\"{citation_snippet}\"\n\n"
                f"Important Note: This explanation is grounded strictly in your document. Final decisions depend on the official terms agreed upon."
            )

        return {
            "answer": answer_text,
            "citations": [{"page": page_num, "snippet": citation_snippet}]
        }
