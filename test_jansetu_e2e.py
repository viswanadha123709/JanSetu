"""
End-to-End Automated Test for JanSetu Platform
Validates:
1. Scheme & Policy queries
2. AI Eligibility Advisor
3. PDF Layout Analysis & Fine Print Detection
4. Grounded Document Q&A
5. User Authentication & Profile
"""

import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jansetu.settings')
django.setup()

from django.contrib.auth.models import User
from apps.accounts.models import UserProfile
from apps.schemes.models import Scheme, Policy, Category, State
from apps.eligibility.ai_engine import EligibilityAdvisor
from apps.documents.models import UploadedDocument
from apps.documents.analyzer import DocumentAnalyzer, DocumentQAService

def run_tests():
    print("=== STARTING JANSETU END-TO-END VALIDATION ===")

    # Test 1: Schemes and Policies catalog
    scheme_count = Scheme.objects.count()
    policy_count = Policy.objects.count()
    print(f"[TEST 1] Master Data: {scheme_count} schemes, {policy_count} policies in SQLite3.")
    assert scheme_count >= 15, "Insufficient schemes populated"
    assert policy_count >= 3, "Insufficient policies populated"

    # Test 2: AI Eligibility Advisor
    print("[TEST 2] Testing AI Eligibility Advisor...")
    query = "I am a farmer from Andhra Pradesh. My annual income is ₹1,50,000. What benefits can I apply for?"
    response_en = EligibilityAdvisor.evaluate_eligibility(query, language='en')
    assert "YSR Rythu Bharosa" in response_en or "PM-KISAN" in response_en, "Failed to match farmer schemes"
    assert "⚠️" in response_en, "Missing compliance disclaimer"
    print("  -> English Advisor response generated successfully with verified scheme recommendations.")

    response_te = EligibilityAdvisor.evaluate_eligibility(query, language='te')
    assert "రైతు" in response_te or "ఆంధ్రప్రదేశ్" in response_te, "Failed Telugu translation response"
    print("  -> Telugu Advisor response generated successfully.")

    # Test 3: Document Layout Analysis & Fine Print Detection
    print("[TEST 3] Testing PDF Document Analysis & Fine Print Detection...")
    sample_path = 'sample_docs/Sample_Health_Insurance_Policy.pdf'
    doc = UploadedDocument.objects.create(
        file_name='Sample_Health_Insurance_Policy.pdf',
        original_file=sample_path,
        file_size=os.path.getsize(sample_path),
        processing_status='pending'
    )
    analyzer = DocumentAnalyzer(doc.id)
    success = analyzer.analyze()
    doc.refresh_from_db()
    assert success is True, "Document analysis failed"
    assert doc.page_count == 4, f"Expected 4 pages, got {doc.page_count}"
    
    clauses = doc.clauses.all()
    print(f"  -> Successfully analysed {doc.page_count} pages, found {clauses.count()} critical clauses.")
    assert clauses.count() >= 5, "Fewer clauses detected than expected"

    # Verify small font detection
    small_font_clauses = doc.clauses.filter(is_small_font=True)
    print(f"  -> Detected {small_font_clauses.count()} small font / fine print clauses.")
    assert small_font_clauses.count() >= 1, "Small font detection failed"

    # Verify final pages / footnote detection
    late_clauses = doc.clauses.filter(document_position__in=['final_pages', 'footnote'])
    print(f"  -> Detected {late_clauses.count()} clauses placed in final pages / footnotes.")
    assert late_clauses.count() >= 1, "Late page detection failed"

    # Test 4: Grounded Document Q&A
    print("[TEST 4] Testing Grounded Document Q&A (RAG)...")
    qa_res = DocumentQAService.answer_question(doc, "What are the cancellation charges?", language='en')
    print("  -> Q&A Result Citation:", qa_res.get('citations'))
    assert len(qa_res.get('citations', [])) > 0, "Failed to extract citation for cancellation"

    # Test 5: Authentication & Profile
    print("[TEST 5] Testing User Authentication & Profile...")
    test_user, created = User.objects.get_or_create(username='test_citizen_ap')
    if created:
        test_user.set_password('Pass1234')
        test_user.save()
        UserProfile.objects.create(
            user=test_user,
            state='Andhra Pradesh',
            occupation='farmer',
            income_range='1l_to_2.5l',
            preferred_language='te'
        )
    assert test_user.profile.occupation == 'farmer', "Profile mismatch"
    print("  -> User profile verified successfully.")

    print("\n=== ALL 5 E2E TESTS PASSED WITH 100% SUCCESS! ===")

if __name__ == '__main__':
    run_tests()
