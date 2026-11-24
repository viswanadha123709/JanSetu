# JanSetu (జనసేతు)

> **Know. Understand. Apply.**  
> **AI-Powered All-in-One Schemes, Policies & Fine Print Assistant**

JanSetu is an AI-powered web platform designed to help Indian citizens—especially farmers, students, senior citizens, entrepreneurs, and the general public—discover welfare schemes, scholarships, education loans, and transparently analyze policy fine print and hidden clauses before signing agreements.

---

## 🌟 Key Features

### 1. Scheme & Policy Discovery
- Centralized catalogue covering Central Government, State Government (Andhra Pradesh & Telangana), Public-sector, and Private offerings.
- 12 categories including Agriculture, Education, Scholarships, Education Loans, Entrepreneurship, Insurance, Healthcare, and Welfare Programs.
- Filters by State, Category, Organization Type, and keywords.
- Verified metadata including benefits, eligibility, required documents, application procedures, official links, and dates.

### 2. AI-Powered Eligibility Advisor
- Understands occupation, income, state, and age through natural-language queries.
- Rule-based and semantic eligibility matching using SQLite3.
- Explains eligibility results, missing documents, and alternative schemes.
- English and Telugu support.
- Speech synthesis for accessibility.
- AI guidance is advisory; final approval rests with the relevant authorities.

### 3. AI Fine Print & Hidden Conditions Detector
- Full-document PDF analysis using PyMuPDF.
- Small-font detection and identification of less-visible clauses.
- Detects conditions in middle pages, footnotes, appendices, and final pages.
- Identifies 15 important condition categories, including additional charges, processing fees, cancellation penalties, lock-in periods, auto-renewals, insurance exclusions, waiting periods, claim restrictions, and refund conditions.
- Displays page numbers, section headings, original text, review priority, simple explanations in English and Telugu, potential impact, and suggested questions.
- Document-specific Q&A using RAG with page references.
- Includes sample health insurance and personal loan PDFs for testing.

### 4. User Authentication & Profile
- Registration, login, and session management.
- User profiles with state, district, occupation, income range, language, and interests.
- Personalized citizen dashboard and scheme recommendations.

### 5. Administrator Portal
- Django Admin dashboard at `/admin/`.
- Manage schemes, policies, categories, organizations, eligibility rules, and document analyses.

---

## 🛠️ Technology Stack

- **Frontend:** React.js (React 18), Tailwind CSS, Lucide Icons, HTML5, CSS3, JavaScript.
- **Backend:** Python 3.13, Django 6.1.1, Django REST Framework, Django CORS Headers.
- **Database:** SQLite3 with Django ORM.
- **PDF Processing:** PyMuPDF (`fitz`), layout extraction, font-size analysis.
- **AI & NLP:** Hybrid architecture using a local rule engine with optional Groq/Gemini API integration through environment variables.

---

## 📄 Sample Documents

The repository includes sample documents for testing the Fine Print Detector:

- `sample_docs/Sample_Health_Insurance_Policy.pdf`
- `sample_docs/Sample_Loan_Agreement.pdf`

These demonstrate the identification of waiting periods, room rent limits, co-payments, processing fees, default interest, lock-in periods, and prepayment penalties.
