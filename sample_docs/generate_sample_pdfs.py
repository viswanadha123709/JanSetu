"""
Script to generate realistic test PDF documents with real fine-print conditions,
small fonts, and late-page clauses for testing JanSetu.
"""

import fitz  # PyMuPDF
import os

def create_sample_health_policy(output_path):
    doc = fitz.open()

    # Page 1: General Policy Terms
    page1 = doc.new_page()
    page1.insert_text((50, 60), "JANSETU ASSURE HEALTHCARE POLICY", fontsize=16, fontname="helv", color=(0.1, 0.2, 0.6))
    page1.insert_text((50, 85), "Comprehensive Health Insurance Policy Document", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    
    body_text_p1 = (
        "Section 1: Preamble & Coverage Summary\n\n"
        "This policy is an agreement between JanSetu Assure Insurance Company and the Insured "
        "named in the Policy Schedule. In consideration of the premium paid, the company agrees to "
        "indemnify the insured person for medically necessary expenses incurred for in-patient "
        "hospitalization, day care procedures, and pre and post-hospitalization medical treatment.\n\n"
        "1.1 In-Patient Hospitalization Treatment:\n"
        "The company covers hospitalization expenses for illness or injury occurring during the policy period, "
        "provided hospitalization is for a continuous period of at least 24 hours.\n\n"
        "1.2 Day Care Procedures:\n"
        "Cover includes technologically advanced medical procedures conducted under general or local anesthesia "
        "that require less than 24 hours hospitalization in a recognized hospital.\n\n"
        "1.3 Cashless Facility:\n"
        "Available across 10,000+ empaneled network hospitals nationwide subject to pre-authorization approval."
    )
    page1.insert_textbox(fitz.Rect(50, 110, 550, 700), body_text_p1, fontsize=10.5, fontname="helv")

    # Page 2: Exclusions & Waiting Periods (Critical Conditions)
    page2 = doc.new_page()
    page2.insert_text((50, 60), "Section 2: Exclusions and Waiting Periods", fontsize=14, fontname="helv", color=(0.1, 0.2, 0.6))
    
    body_text_p2 = (
        "2.1 Mandatory Initial Waiting Period:\n"
        "A mandatory initial waiting period of 30 days from the inception date of this policy shall apply. "
        "No claim shall be payable during the first 30 days for any illness or hospitalization, except in cases "
        "arising solely out of accidental injuries.\n\n"
        "2.2 Specific Disease Waiting Period of 24 Months:\n"
        "A waiting period of 24 months of continuous coverage shall apply for the treatment of Cataract, "
        "Benign Prostatic Hypertrophy, Hernia, Hydrocele, Piles, Fissures, Sinusitis, Joint Replacement Surgeries, "
        "and Osteoarthritis. Claims for these specified ailments are excluded from coverage during the first two years.\n\n"
        "2.3 Pre-existing Disease (PED) Exclusion:\n"
        "Pre-existing diseases and any condition diagnosed or treated prior to policy commencement are excluded "
        "from coverage until 36 months of continuous coverage have elapsed without any break."
    )
    page2.insert_textbox(fitz.Rect(50, 90, 550, 650), body_text_p2, fontsize=10.5, fontname="helv")

    # Page 3: Middle Page - Room Rent Caps & Co-Payments
    page3 = doc.new_page()
    page3.insert_text((50, 60), "Section 3: Limits of Cover, Deductibles & Co-Payment", fontsize=14, fontname="helv", color=(0.1, 0.2, 0.6))
    
    body_text_p3 = (
        "3.1 Room Rent Capping & Proportionate Deduction:\n"
        "Daily room rent limit is capped at 1% of the total Sum Insured per day. If the insured person occupies "
        "a hospital room whose rent exceeds this limit, proportionate deduction shall apply on all associated medical, "
        "surgical, doctor consultation, and nursing charges incurred during the admission.\n\n"
        "3.2 Co-Payment Requirement:\n"
        "A mandatory co-payment of 20% shall apply on every admissible claim for all insured persons aged 61 years "
        "and above. The insured person must pay 20% of the total approved hospital claim out of their own pocket."
    )
    page3.insert_textbox(fitz.Rect(50, 90, 550, 650), body_text_p3, fontsize=10.5, fontname="helv")

    # Page 4: Final Page with Fine Print & Footnotes (High Importance)
    page4 = doc.new_page()
    page4.insert_text((50, 60), "Section 4: General Conditions & Cancellation Policy", fontsize=14, fontname="helv", color=(0.1, 0.2, 0.6))
    
    body_text_p4 = (
        "4.1 Mandatory Claim Intimation Deadline:\n"
        "Notice in writing with full particulars must be furnished within 24 hours of emergency hospitalization, "
        "or at least 48 hours prior to planned hospitalization. Failure to notify within 24 hours may lead to claim rejection.\n\n"
        "4.2 Cancellation Charges and Short-Period Scale:\n"
        "The insured may cancel this policy by giving 15 days written notice. A cancellation fee will apply. "
        "The insurer shall retain premium as per short-period scale: 25% retained if cancelled within 1 month, "
        "50% retained within 3 months, 75% within 6 months, and no refund shall be payable after 6 months.\n\n"
        "4.3 Automatic Renewal Conditions:\n"
        "The policy will automatically renew on an annual basis and the renewal premium will be auto-debited "
        "from the registered bank account unless written cancellation is received 30 days prior to expiry."
    )
    page4.insert_textbox(fitz.Rect(50, 90, 550, 500), body_text_p4, fontsize=10.5, fontname="helv")

    # Small Font Footnote at the bottom of Page 4 (< 80% body font: 7.2 pt)
    footnote_text = (
        "* Important Fine Print Note: All non-medical expenses, administrative charges, registration charges, and "
        "attendant convenience fees are excluded from coverage. Investigation fees without active medical treatment are non-refundable."
    )
    page4.insert_textbox(fitz.Rect(50, 710, 550, 770), footnote_text, fontsize=7.2, fontname="helv", color=(0.4, 0.4, 0.4))

    doc.save(output_path)
    doc.close()
    print(f"Created sample health policy at: {output_path}")


def create_sample_loan_agreement(output_path):
    doc = fitz.open()

    # Page 1: Loan Schedule
    page1 = doc.new_page()
    page1.insert_text((50, 60), "JANSETU SAMRUDDHI PERSONAL LOAN AGREEMENT", fontsize=16, fontname="helv", color=(0.1, 0.2, 0.6))
    page1.insert_text((50, 85), "Loan Agreement & Schedule of Charges", fontsize=12, fontname="helv", color=(0.3, 0.3, 0.3))
    
    body_text_p1 = (
        "This Personal Loan Agreement is executed between the Borrower and the Bank.\n\n"
        "1. Loan Facility & Disbursement:\n"
        "The Bank agrees to lend the principal loan amount to the Borrower subject to the terms and conditions herein. "
        "The loan will be disbursed into the borrower's designated bank account upon completion of verification.\n\n"
        "2. Interest Rate & Repayment Tenure:\n"
        "The loan carries an agreed annual interest rate payable in Equated Monthly Instalments (EMIs) over the specified tenure."
    )
    page1.insert_textbox(fitz.Rect(50, 110, 550, 650), body_text_p1, fontsize=10.5, fontname="helv")

    # Page 2: Fees, Processing & Penalties
    page2 = doc.new_page()
    page2.insert_text((50, 60), "Section 2: Processing Fees & Operational Charges", fontsize=14, fontname="helv", color=(0.1, 0.2, 0.6))
    
    body_text_p2 = (
        "2.1 Upfront Processing Fee:\n"
        "A non-refundable processing fee of 2.5% of the gross loan amount plus applicable GST shall be deducted upfront "
        "at the time of disbursement. This fee is non-refundable under all circumstances, even if the loan is cancelled.\n\n"
        "2.2 Late Payment Penalties and Default Interest:\n"
        "In the event of default or delayed payment of any EMI, the borrower shall pay penal interest at the rate of "
        "2% per month (24% per annum) on the overdue EMI from the due date until the actual date of realization. "
        "An ECS bounce charge of Rs. 500 will be levied for each failed auto-debit attempt."
    )
    page2.insert_textbox(fitz.Rect(50, 90, 550, 650), body_text_p2, fontsize=10.5, fontname="helv")

    # Page 3: Final Page - Prepayment Penalty, Lock-in & Fine Print
    page3 = doc.new_page()
    page3.insert_text((50, 60), "Section 3: Pre-Payment, Lock-in & Termination Charges", fontsize=14, fontname="helv", color=(0.1, 0.2, 0.6))
    
    body_text_p3 = (
        "3.1 Mandatory Lock-in Period:\n"
        "The loan facility is subject to a mandatory lock-in period of 12 months. No part-prepayment or full foreclosure "
        "is permitted during the first 12 months from the date of initial disbursement.\n\n"
        "3.2 Pre-payment Penalty & Foreclosure Charges:\n"
        "If the borrower opts for pre-mature foreclosure of the loan after 12 months, an early termination fee and "
        "pre-payment penalty of 3% on the outstanding principal balance shall be payable."
    )
    page3.insert_textbox(fitz.Rect(50, 90, 550, 500), body_text_p3, fontsize=10.5, fontname="helv")

    # Small Font Footnote on Page 3 (7.0 pt font)
    footnote_text = (
        "* Fine Print Note: Annual portfolio maintenance charges of Rs. 1,000 + GST will be billed annually to the borrower. "
        "The Bank reserves the right to terminate the agreement and demand immediate full repayment without prior notice upon any covenant breach."
    )
    page3.insert_textbox(fitz.Rect(50, 690, 550, 770), footnote_text, fontsize=7.0, fontname="helv", color=(0.4, 0.4, 0.4))

    doc.save(output_path)
    doc.close()
    print(f"Created sample loan agreement at: {output_path}")

if __name__ == '__main__':
    os.makedirs('sample_docs', exist_ok=True)
    create_sample_health_policy('sample_docs/Sample_Health_Insurance_Policy.pdf')
    create_sample_loan_agreement('sample_docs/Sample_Loan_Agreement.pdf')
