# JanSetu (జనసేతు)
> **Know. Understand. Apply.**
> **AI-Powered All-in-One Schemes, Policies & Fine Print Assistant**

JanSetu is an AI-powered web platform designed to help Indian citizens—especially farmers, students, senior citizens, entrepreneurs, and the general public—discover welfare schemes, scholarships, education loans, and transparently analyze policy fine print and hidden clauses before signing agreements.

---

## 🌟 Key Features

### 1. Scheme & Policy Discovery (Module 2)
- **Centralized Catalogue**: Central Government, State Government (Andhra Pradesh & Telangana), Public-sector, and Private offerings.
- **12 Categories**: Agriculture, Education, Scholarships, Education Loans, Entrepreneurship, Business Development, Insurance, Healthcare, Senior Citizen Benefits, Financial Assistance, Employment, and Welfare Programs.
- **Multidimensional Filters**: Filter by State (Andhra Pradesh, Telangana, Central), Category, Organization Type, and natural keywords.
- **Verified Metadata**: Every listing includes benefits, eligibility criteria, required documents checklist, application procedure, official links, and verified dates.

### 2. AI-Powered Eligibility Advisor (Module 3 & Module 6)
- **Natural Language Understanding**: Understands user occupation, income, state, and age directly from text or user profile.
- **Rule-Based & Semantic Matching**: Evaluates eligibility criteria against real rules stored in SQLite3.
- **Transparent Reasoning**: Explains *why* the citizen appears eligible or ineligible, identifies missing documents, and suggests alternatives.
- **Bilingual Interface**: Full English and Telugu (తెలుగు) support.
- **Speech Synthesis**: Built-in read-aloud button for accessibility.
- **Compliance Disclaimer**: Prominently informs citizens that AI guidance is advisory and official approval rests with government authorities.

### 3. AI Fine Print & Hidden Conditions Detector (Module 4 & Module 5 - Flagship)
- **Full Document PyMuPDF Layout Analysis**: Inspects every page of uploaded PDFs.
- **Small Font Detection**: Automatically calculates standard body font size and flags fine print (< 80% body font size, down to 7pt).
- **Position Detection**: Flags clauses hidden in middle pages, back matter, footnotes, and appendices.
- **15 Condition Categories**:
  1. Additional charges
  2. Processing fees
  3. Hidden / less-obvious costs
  4. Cancellation charges & surrender penalties
  5. Late payment penalties & bounce fees
  6. Lock-in periods & mandatory holding
  7. Automatic renewal conditions
  8. Insurance exclusions & non-covered scenarios
  9. Waiting periods (e.g. 30-day, 24-month, 36-month)
  10. Claim restrictions (room rent capping, co-payment)
  11. Eligibility restrictions
  12. Benefit limitations & aggregate caps
  13. Refund conditions & forfeiture
  14. Agreement termination grounds
  15. Critical intimation deadlines (e.g. 24-hour notice)
- **Clause Breakdown**: Each detected clause displays exact page number, section heading, verbatim quote, review priority (High, Medium, Informational), plain-language explanation (English & Telugu), potential impact, and suggested questions to ask.
- **Grounded Document Q&A (RAG)**: Ask questions specifically about the uploaded document and receive answers with exact page citations.
- **Pre-Loaded Instant Samples**: 1-click test with pre-generated Health Insurance Policy (4 pages) or Personal Loan Agreement (3 pages).

### 4. User Authentication & Profile (Module 1)
- User registration, login, session management.
- Captures state, district, occupation, income range, preferred language, and interests.
- Personalized citizen dashboard with tailored scheme recommendations.

### 5. Administrator Portal (Module 12)
- Built-in Django Admin at `/admin/`.
- Manage schemes, policies, categories, organizations, eligibility rules, and view uploaded document analyses.
- Pre-seeded superuser credentials: `admin` / `admin123`.

---

## 🛠️ Technology Stack

- **Frontend**: React.js (React 18), Tailwind CSS, Lucide icons, HTML5, CSS3, JavaScript.
- **Backend**: Python 3.13, Django 6.1.1, Django REST Framework, Django CORS Headers.
- **Database**: SQLite3 (as requested, managed via Django ORM for seamless future migrations).
- **PDF & Layout Processing**: PyMuPDF (`fitz`), layout dict extraction, font size statistics.
- **AI & NLP**: Hybrid architecture with local deterministic semantic rule engine + optional Groq / Gemini API key integration via `.env`.

---

## 🚀 How to Run JanSetu

### 1. Activate Environment and Navigate to Project
```powershell
cd c:\Users\lenovo\vs_code\jansetu
```

### 2. Run the Django Server
```powershell
& "c:\Users\lenovo\vs_code\environment\Scripts\python.exe" manage.py runserver 127.0.0.1:8000
```

### 3. Open in Browser
Open: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### 4. Admin Credentials
- **URL**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Username**: `admin`
- **Password**: `admin123`

### 5. Instant Test PDF Samples
The repository includes pre-generated realistic sample documents with small-font clauses, footnotes, and fine print for instant testing:
- `sample_docs/Sample_Health_Insurance_Policy.pdf` (Waiting periods, room rent caps, co-pay, cancellation penalty, small footnote)
- `sample_docs/Sample_Loan_Agreement.pdf` (Processing fees, 24% default interest, 12-month lock-in, 3% prepayment penalty)
You can test either with 1 click directly in the "Fine Print Detector" tab!
