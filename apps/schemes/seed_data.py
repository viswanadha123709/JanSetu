"""
JanSetu Scheme & Policy Seed Data
Comprehensive verified schemes and policies for Central Government, Andhra Pradesh, Telangana, and Private offerings.
"""

from datetime import date
from apps.schemes.models import State, Category, Organization, Scheme, Policy, EligibilityRule

def populate_seed_data():
    print("Populating JanSetu master data...")

    # 1. States
    states_data = [
        {"name": "Andhra Pradesh", "code": "AP"},
        {"name": "Telangana", "code": "TS"},
        {"name": "All India (Central)", "code": "IN"},
    ]
    states = {}
    for item in states_data:
        obj, _ = State.objects.get_or_create(state_name=item["name"], defaults={"state_code": item["code"]})
        states[item["code"]] = obj

    # 2. Categories
    categories_data = [
        ("Agriculture", "Farmer assistance, input subsidies, crop insurance, and irrigation programs", "sprout"),
        ("Education", "Schooling, digital learning, textbooks, and hostel admissions", "graduation-cap"),
        ("Scholarships", "Pre-matric, post-matric, merit, and means-based scholarships", "award"),
        ("Education loans", "Subsidized loans, interest waiver, and overseas study support", "landmark"),
        ("Entrepreneurship", "Seed capital, startup grants, and self-employment funding", "rocket"),
        ("Business development", "Industrial clearances, MSME support, and trade subsidies", "briefcase"),
        ("Insurance", "Life, accident, disability, and asset insurance policies", "shield-check"),
        ("Healthcare", "Free treatment, hospital admission coverage, and diagnostic schemes", "heart-pulse"),
        ("Senior citizen benefits", "Old-age pensions, caregiver allowances, and healthcare cards", "user-check"),
        ("Financial assistance", "Direct bank transfers, livelihood support, and crisis grants", "coins"),
        ("Employment and skill development", "Apprenticeships, vocational courses, and job placement", "hammer"),
        ("Other welfare programmes", "Housing, drinking water, food security, and community welfare", "users"),
    ]
    categories = {}
    for name, desc, icon in categories_data:
        obj, _ = Category.objects.get_or_create(category_name=name, defaults={"description": desc, "icon": icon})
        categories[name] = obj

    # 3. Organizations
    orgs_data = [
        ("Ministry of Agriculture & Farmers Welfare", "central", "https://agricoop.nic.in"),
        ("Ministry of Education, GoI", "central", "https://www.education.gov.in"),
        ("Ministry of Finance, GoI", "central", "https://finmin.gov.in"),
        ("Ministry of MSME, GoI", "central", "https://msme.gov.in"),
        ("National Health Authority (NHA)", "central", "https://nha.gov.in"),
        ("Department of Agriculture, Govt. of Andhra Pradesh", "state", "https://apagrisnet.gov.in"),
        ("Social Welfare Department, Govt. of Andhra Pradesh", "state", "https://jaganannavidyadeevena.ap.gov.in"),
        ("Panchayat Raj & Rural Development, Govt. of AP", "state", "https://sspensions.ap.gov.in"),
        ("Department of Agriculture, Govt. of Telangana", "state", "https://agri.telangana.gov.in"),
        ("Social Welfare Department, Govt. of Telangana", "state", "https://telanganaepass.cgg.gov.in"),
        ("Industries & Commerce, Govt. of Telangana", "state", "https://ipass.telangana.gov.in"),
        ("Rural Development, Govt. of Telangana", "state", "https://aasara.telangana.gov.in"),
        ("Life Insurance Corporation of India (LIC)", "public", "https://licindia.in"),
        ("State Bank of India (SBI)", "public", "https://sbi.co.in"),
        ("Star Health and Allied Insurance", "private", "https://www.starhealth.in"),
        ("HDFC Life Insurance Co.", "private", "https://www.hdfclife.com"),
    ]
    orgs = {}
    for name, org_type, website in orgs_data:
        obj, _ = Organization.objects.get_or_create(organization_name=name, defaults={"organization_type": org_type, "official_website": website})
        orgs[name] = obj

    # 4. Schemes
    schemes_data = [
        {
            "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
            "org": "Ministry of Agriculture & Farmers Welfare",
            "cat": "Agriculture",
            "state": None,
            "type": "Central",
            "benefits": "Financial benefit of ₹6,000 per year directly credited into the bank accounts of farmer families in three equal instalments of ₹2,000 every four months.",
            "eligibility": "Small and marginal farmer families with cultivable landholding in their name. Institutional landholders, serving/retired government officers, and income tax payees are excluded.",
            "docs": "Aadhaar Card, Land ownership papers (Pattadar Passbook / RoR 1B), Active Bank Account linked to Aadhaar, Mobile Number.",
            "procedure": "1. Visit the official PM-KISAN portal (pmkisan.gov.in).\n2. Click on 'New Farmer Registration'.\n3. Enter Aadhaar number and select state/district.\n4. Fill land survey numbers and bank account details.\n5. Submit for verification by local revenue/agriculture officer.",
            "url": "https://pmkisan.gov.in",
            "dates": "Enrolment open year-round; instalments disbursed in April, August, and December.",
            "rules": [
                ("occupation", "Must be a farmer or landholder", "farmer"),
                ("max_income", "Excludes institutional landholders and income tax payees", "tax_exempt_only"),
            ]
        },
        {
            "name": "YSR Rythu Bharosa (Andhra Pradesh)",
            "org": "Department of Agriculture, Govt. of Andhra Pradesh",
            "cat": "Agriculture",
            "state": "AP",
            "type": "State",
            "benefits": "Financial assistance of ₹13,500 per year per eligible farmer family (including ₹6,000 from PM-KISAN and ₹7,500 from the State Government). Also covers tenant farmers belonging to SC, ST, BC, and Minority categories.",
            "eligibility": "Cultivator farmer families residing in Andhra Pradesh with landholdings, or registered tenant farmers cultivating land with valid crop agreements.",
            "docs": "Aadhaar card, Pattadar passbook / CCRC (Crop Cultivator Rights Card for tenant farmers), Aadhaar-seeded bank account passbook, Ration card.",
            "procedure": "1. Verify your name in the Village Secretariat (Grama Sachivalayam) published social audit list.\n2. In case of new application, submit land papers and Aadhaar to Village Agriculture Assistant (VAA).\n3. Tenant farmers apply with agreement card approved by landowner.",
            "url": "https://ysrrythubharosa.ap.gov.in",
            "dates": "Disbursements in May (Kharif), October (Rabi), and January (Sankranti).",
            "rules": [
                ("state", "Must be a resident of Andhra Pradesh", "AP"),
                ("occupation", "Must be an agricultural cultivator or tenant farmer", "farmer"),
            ]
        },
        {
            "name": "Rythu Bandhu & Rythu Bima (Telangana)",
            "org": "Department of Agriculture, Govt. of Telangana",
            "cat": "Agriculture",
            "state": "TS",
            "type": "State",
            "benefits": "Investment support of ₹10,000 per acre per year (₹5,000 per acre per season for Kharif & Rabi) to meet initial input costs such as seeds and fertilizers. Includes ₹5,00,000 Rythu Bima group life insurance for landowning farmers.",
            "eligibility": "All landowning farmers possessing agricultural land in Telangana with updated Dharani passbooks. Age limit for Rythu Bima insurance is 18 to 59 years.",
            "docs": "Dharani digital pattadar passbook, Aadhaar card, Bank account details linked to Aadhaar.",
            "procedure": "1. Ensure land records are digitized and verified on Dharani portal.\n2. Submit bank passbook copy and Aadhaar to Agricultural Extension Officer (AEO) of the cluster.\n3. Direct DBT transfer is processed by the Agriculture Department.",
            "url": "https://rythubandhu.telangana.gov.in",
            "dates": "Kharif disbursement in June/July; Rabi disbursement in December/January.",
            "rules": [
                ("state", "Must be a resident/landowner in Telangana", "TS"),
                ("occupation", "Must hold agricultural land in Telangana", "farmer"),
                ("min_age", "Rythu Bima minimum age is 18 years", ">=18"),
                ("max_age", "Rythu Bima maximum age is 59 years", "<=59"),
            ]
        },
        {
            "name": "PM Fasal Bima Yojana (PMFBY)",
            "org": "Ministry of Agriculture & Farmers Welfare",
            "cat": "Insurance",
            "state": None,
            "type": "Central",
            "benefits": "Comprehensive insurance coverage against non-preventable natural risks (drought, flood, unseasonal rain, pests) with low uniform premium: 2% for Kharif food crops, 1.5% for Rabi crops, and 5% for annual commercial/horticultural crops.",
            "eligibility": "All farmers growing notified crops in notified areas including sharecroppers and tenant farmers.",
            "docs": "Land possession certificate / RoR, sowing certificate issued by local patwari/revenue officer, Aadhaar card, bank account passbook.",
            "procedure": "1. Apply via National Crop Insurance Portal (pmfby.gov.in) or nearest CSC / bank branch.\n2. Loanee farmers are enrolled automatically by their financing bank (opt-out available).\n3. Non-loanee farmers submit crop sowing certificate before cut-off date.",
            "url": "https://pmfby.gov.in",
            "dates": "Cut-off date typically July 31 for Kharif crops and December 31 for Rabi crops.",
            "rules": [
                ("occupation", "Must be a farmer cultivating notified crops", "farmer"),
            ]
        },
        {
            "name": "Jagananna Vidya Deevena (AP Post-Matric Fee Reimbursement)",
            "org": "Social Welfare Department, Govt. of Andhra Pradesh",
            "cat": "Scholarships",
            "state": "AP",
            "type": "State",
            "benefits": "Complete 100% tuition fee reimbursement credited directly to the accounts of eligible mothers of students pursuing ITI, Polytechnic, Degree, Engineering, Medicine, and Post-Graduate courses.",
            "eligibility": "Students enrolled in approved colleges in AP with total family annual income less than ₹2,50,000, family landholding less than 10 acres wetland or 25 acres dryland, and no 4-wheeler ownership.",
            "docs": "Student & Mother Aadhaar cards, Integrated Caste & Income certificate, Rice Card / Ration Card, College admission allotment order and fee receipt.",
            "procedure": "1. Apply through college admission desk during counselling.\n2. College uploads verified enrollment data to Jnanabhumi / Navasakam portal.\n3. Village / Ward Welfare Assistant conducts physical field verification.\n4. Approved funds deposited directly in four quarterly cycles.",
            "url": "https://jaganannavidyadeevena.ap.gov.in",
            "dates": "Annual academic cycle; verification happens September - November.",
            "rules": [
                ("state", "Must reside in Andhra Pradesh", "AP"),
                ("occupation", "Must be an active student in post-matric courses", "student"),
                ("max_income", "Annual family income must be under ₹2,50,000", "<=250000"),
            ]
        },
        {
            "name": "Telangana ePASS Post-Matric Scholarship",
            "org": "Social Welfare Department, Govt. of Telangana",
            "cat": "Scholarships",
            "state": "TS",
            "type": "State",
            "benefits": "Full tuition fee reimbursement (RTF) and maintenance charges/mess fees (MTF) for SC, ST, BC, EBC, Minority, and Physically Challenged post-matric students.",
            "eligibility": "Permanent residents of Telangana pursuing Intermediate, ITI, Polytechnic, Degree, PG, or Professional courses. Annual family income limit: ₹2,00,000 for SC/ST and rural BC; ₹1,50,000 for urban BC/EBC.",
            "docs": "SSC Hall Ticket number, Aadhaar Card, MeeSeva Caste & Income Certificate issued within last 1 year, College Bonafide/Allotment order, Bank Passbook.",
            "procedure": "1. Register on official portal telanganaepass.cgg.gov.in.\n2. Select Post-Matric Fresh / Renewal Registration.\n3. Upload photo, caste, income, and bank credentials.\n4. Submit physical hard copy along with original verification certificates to college principal.",
            "url": "https://telanganaepass.cgg.gov.in",
            "dates": "Fresh registrations usually close October/November of each academic year.",
            "rules": [
                ("state", "Must reside in Telangana", "TS"),
                ("occupation", "Must be a college / post-matric student", "student"),
                ("max_income", "Family income up to ₹2,00,000 for SC/ST/rural", "<=200000"),
            ]
        },
        {
            "name": "Central Sector Interest Subsidy Scheme (CSIS) on Education Loans",
            "org": "Ministry of Education, GoI",
            "cat": "Education loans",
            "state": None,
            "type": "Central",
            "benefits": "Full 100% interest subsidy during the moratorium period (course duration plus 1 year) on educational loans availed from scheduled commercial banks for professional/technical courses in India.",
            "eligibility": "Students from Economically Weaker Sections (EWS) whose total gross annual family parental income does not exceed ₹4,50,000. Admitted to approved higher educational institutions.",
            "docs": "Income certificate issued by designated state revenue authority (Tahsildar/Mandal Revenue Officer), Education loan sanction letter, Admission fee receipt, Aadhaar.",
            "procedure": "1. Apply for education loan through Vidya Lakshmi Portal (vidyalakshmi.co.in).\n2. Submit income certificate indicating annual parental income <= ₹4.5 Lakhs to the lending branch.\n3. The bank enters your account in the Canara Bank subsidy portal for quarterly reimbursement.",
            "url": "https://www.education.gov.in",
            "dates": "Available continuously with education loan sanction.",
            "rules": [
                ("occupation", "Must be a student pursuing professional/technical higher education", "student"),
                ("max_income", "Annual family income must not exceed ₹4,50,000", "<=450000"),
            ]
        },
        {
            "name": "Pradhan Mantri Mudra Yojana (PMMY)",
            "org": "Ministry of Finance, GoI",
            "cat": "Entrepreneurship",
            "state": None,
            "type": "Central",
            "benefits": "Collateral-free business loans up to ₹10 Lakhs for micro and small enterprises in manufacturing, trading, and service sectors. Three categories: Shishu (up to ₹50,000), Kishore (₹50,000 to ₹5 Lakhs), and Tarun (₹5 Lakhs to ₹10 Lakhs).",
            "eligibility": "Any Indian citizen who has a business plan for a non-farm income-generating activity such as manufacturing, processing, trading, or service sector. Age 18+.",
            "docs": "Business proposal, identity proof (Aadhaar/Voter ID), proof of residence, passport photos, quotes for machinery/inventory, bank statement for last 6 months.",
            "procedure": "1. Prepare business plan and quotation for machinery or raw materials.\n2. Apply online via Udyami Mitra portal (udyamimitra.in) or visit any commercial/Gramin bank branch.\n3. Bank processes application within 15 days without requiring collateral security.",
            "url": "https://www.mudra.org.in",
            "dates": "Open year-round at all commercial, regional rural, and cooperative bank branches.",
            "rules": [
                ("min_age", "Applicant must be at least 18 years old", ">=18"),
                ("occupation", "Entrepreneurs, shopkeepers, artisans, and small business owners", "entrepreneur,small_business_owner"),
            ]
        },
        {
            "name": "Stand-Up India Scheme",
            "org": "Ministry of Finance, GoI",
            "cat": "Entrepreneurship",
            "state": None,
            "type": "Central",
            "benefits": "Facilitates bank loans between ₹10 Lakhs and ₹1 Crore to at least one SC/ST borrower and at least one woman borrower per bank branch for setting up a greenfield enterprise.",
            "eligibility": "SC/ST and/or woman entrepreneurs above 18 years of age. For non-individual enterprises, at least 51% of the shareholding and controlling stake must be held by an SC/ST or woman entrepreneur.",
            "docs": "Identity & address proof, Caste certificate (for SC/ST), Project report, balance sheet projections, partnership deed/incorporation certificate if applicable.",
            "procedure": "1. Visit standupmitra.in.\n2. Register as a borrower and fill the online loan application.\n3. Handholding agency guides through DPR preparation, business setup, and connects with target bank.",
            "url": "https://www.standupmitra.in",
            "dates": "Active across all scheduled commercial banks nationwide.",
            "rules": [
                ("min_age", "Applicant must be at least 18 years old", ">=18"),
                ("category", "SC, ST, or Woman Entrepreneur", "sc,st,women"),
            ]
        },
        {
            "name": "TS-iPASS Industrial Approvals & Incentives",
            "org": "Industries & Commerce, Govt. of Telangana",
            "cat": "Business development",
            "state": "TS",
            "type": "State",
            "benefits": "Single-window online approval with right to clearances within 15 to 30 days. Includes state investment subsidies, power cost rebates (₹1.50/unit for 5 years), and stamp duty reimbursement for micro and small units.",
            "eligibility": "Micro, small, medium, and large industrial and service enterprises establishing operations within Telangana.",
            "docs": "Udyam registration certificate, land ownership or lease agreement, DPR (Detailed Project Report), factory layout plan, PAN.",
            "procedure": "1. Register on ipass.telangana.gov.in.\n2. Fill Common Application Form (CAF) with combined utility requirements.\n3. Make single-window payment. Clearances issued automatically under deemed approval clause if not processed within statutory window.",
            "url": "https://ipass.telangana.gov.in",
            "dates": "Available 24x7 online through the Telangana single window portal.",
            "rules": [
                ("state", "Enterprise must be established in Telangana", "TS"),
                ("occupation", "Entrepreneurs and business owners", "entrepreneur,small_business_owner"),
            ]
        },
        {
            "name": "YSR Cheyutha (Andhra Pradesh)",
            "org": "Social Welfare Department, Govt. of Andhra Pradesh",
            "cat": "Financial assistance",
            "state": "AP",
            "type": "State",
            "benefits": "Financial assistance of ₹75,000 in four equal phases (₹18,750 per year) provided directly to eligible women to support sustainable self-employment and livestock/retail livelihood units.",
            "eligibility": "Women belonging to SC, ST, BC, and Minority communities residing in AP, aged between 45 and 60 years. Total family income must be under ₹1,20,000 in rural or ₹1,44,000 in urban areas.",
            "docs": "Aadhaar Card with correct date of birth, Caste certificate, Rice Card, Bank account passbook copy.",
            "procedure": "1. Approach Village or Ward Secretariat (Sachivalayam) in your area.\n2. Complete e-KYC authentication with Village Welfare Assistant.\n3. Verify inclusion in the draft beneficiary list displayed on social audit notice boards.",
            "url": "https://navasakam.ap.gov.in",
            "dates": "Annual disbursement cycle, typically announced in July/August.",
            "rules": [
                ("state", "Must reside in Andhra Pradesh", "AP"),
                ("gender", "Must be a female applicant", "female"),
                ("min_age", "Minimum age is 45 years", ">=45"),
                ("max_age", "Maximum age is 60 years", "<=60"),
                ("max_income", "Family income must be below ₹1,44,000", "<=144000"),
            ]
        },
        {
            "name": "Ayushman Bharat - PM-JAY (Pradhan Mantri Jan Arogya Yojana)",
            "org": "National Health Authority (NHA)",
            "cat": "Healthcare",
            "state": None,
            "type": "Central",
            "benefits": "Cashless health insurance coverage up to ₹5,00,000 per family per year for secondary and tertiary hospitalization across 27,000+ empaneled public and private hospitals across India.",
            "eligibility": "Deprived rural families and identified occupational categories of urban workers based on SECC (Socio-Economic Caste Census) 2011 and expanded state BPL databases. No restriction on family size or age.",
            "docs": "Aadhaar Card, Ration Card / NFSA Food Security Card, PM-JAY Ayushman Golden Card.",
            "procedure": "1. Check your name at beneficiary.nha.gov.in or visit any empaneled hospital Ayushman Mitra desk.\n2. Complete Aadhaar e-KYC.\n3. Download your Ayushman PVC card and present during hospital admission for cashless treatment.",
            "url": "https://pmjay.gov.in",
            "dates": "Available year-round across all participating hospitals.",
            "rules": [
                ("max_income", "Targeted at BPL and economically deprived families", "bpl"),
            ]
        },
        {
            "name": "Dr. YSR Aarogyasri Health Scheme (Andhra Pradesh)",
            "org": "Panchayat Raj & Rural Development, Govt. of AP",
            "cat": "Healthcare",
            "state": "AP",
            "type": "State",
            "benefits": "Cashless medical treatment up to ₹5,00,000 per family per year covering 3,257 surgical and medical procedures, including cancer, heart surgeries, and neurosurgery. Includes post-operative sustenance allowance of ₹225/day (up to ₹5,000/month).",
            "eligibility": "All families in Andhra Pradesh possessing a valid Rice Card or whose annual household income is below ₹5,00,000 with landholding less than 12 acres wetland / 35 acres dryland.",
            "docs": "YSR Aarogyasri Card or Rice Card, Aadhaar Card of all family members.",
            "procedure": "1. Visit any network hospital in AP, Hyderabad, Chennai, or Bengaluru.\n2. Meet Aarogyamithra at the reception help desk.\n3. Instant pre-authorization approved within 2 hours for cashless admission and surgery.",
            "url": "https://aarogyasri.ap.gov.in",
            "dates": "Services available 24x7 across all network hospitals.",
            "rules": [
                ("state", "Must reside in Andhra Pradesh", "AP"),
                ("max_income", "Annual household income must be below ₹5,00,000", "<=500000"),
            ]
        },
        {
            "name": "Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY)",
            "org": "Ministry of Finance, GoI",
            "cat": "Insurance",
            "state": None,
            "type": "Central",
            "benefits": "Life insurance coverage of ₹2,00,000 in case of death of the insured due to any reason at a nominal premium of ₹436 per annum, auto-debited from the subscriber's bank account.",
            "eligibility": "All individual bank account holders aged between 18 and 50 years with a participating commercial, regional, or cooperative bank.",
            "docs": "Aadhaar Card, Active savings bank account, auto-debit consent form.",
            "procedure": "1. Visit your home bank branch or log in to your mobile banking / internet banking app.\n2. Select 'Social Security Schemes' -> PMJJBY.\n3. Provide auto-debit consent. The policy is issued instantly with insurance year running June 1 to May 31.",
            "url": "https://financialservices.gov.in",
            "dates": "Annual auto-debit window occurs between May 25 and May 31.",
            "rules": [
                ("min_age", "Minimum age is 18 years", ">=18"),
                ("max_age", "Maximum entry age is 50 years (cover continues till age 55)", "<=50"),
            ]
        },
        {
            "name": "Atal Pension Yojana (APY)",
            "org": "Ministry of Finance, GoI",
            "cat": "Senior citizen benefits",
            "state": None,
            "type": "Central",
            "benefits": "Guaranteed minimum monthly pension of ₹1,000, ₹2,000, ₹3,000, ₹4,000, or ₹5,000 per month starting at age 60, depending on contributions. Same pension to spouse upon subscriber's death, and return of full pension corpus to nominee.",
            "eligibility": "Any citizen of India aged between 18 and 40 years holding a savings bank account. Income tax payers are not eligible to join fresh APY accounts.",
            "docs": "Aadhaar Card, Bank account passbook, mobile number, nominee details.",
            "procedure": "1. Approach your bank branch or apply via NetBanking.\n2. Choose desired monthly pension amount (₹1,000 to ₹5,000).\n3. Bank calculates monthly contribution based on current age and activates monthly auto-debit.",
            "url": "https://www.pfrda.org.in",
            "dates": "Subscribers can join at any time between ages 18 and 40.",
            "rules": [
                ("min_age", "Minimum entry age is 18 years", ">=18"),
                ("max_age", "Maximum entry age is 40 years", "<=40"),
            ]
        },
        {
            "name": "YSR Pension Kanuka (Andhra Pradesh)",
            "org": "Panchayat Raj & Rural Development, Govt. of AP",
            "cat": "Senior citizen benefits",
            "state": "AP",
            "type": "State",
            "benefits": "Monthly financial pension of ₹3,000 delivered straight to the doorsteps of beneficiaries on the 1st of every month through Village/Ward volunteers with biometric authentication.",
            "eligibility": "Old age pensioners aged 60 years and above belonging to BPL families in AP with family monthly income <= ₹10,000 in rural or ₹12,000 in urban areas, and not receiving any other government pension.",
            "docs": "Aadhaar Card, Rice Card / BPL card, Date of birth certificate or age assessment, active mobile number.",
            "procedure": "1. Submit application at Grama/Ward Sachivalayam with age proof.\n2. Welfare and Education Assistant conducts verification and submits to MPDO.\n3. Approved pension sanction order issued with doorstep cash disbursement.",
            "url": "https://sspensions.ap.gov.in",
            "dates": "Disbursed on the 1st day of every single month.",
            "rules": [
                ("state", "Must reside in Andhra Pradesh", "AP"),
                ("min_age", "Minimum age is 60 years", ">=60"),
                ("occupation", "Elderly citizens or destitute seniors", "senior_citizen"),
                ("max_income", "Monthly family income up to ₹12,000", "<=144000"),
            ]
        },
        {
            "name": "Aasara Pensions (Telangana)",
            "org": "Rural Development, Govt. of Telangana",
            "cat": "Senior citizen benefits",
            "state": "TS",
            "type": "State",
            "benefits": "Monthly social security pension of ₹2,016 per month for old age citizens, widows, weavers, and toddy tappers, and ₹4,016 per month for disabled persons.",
            "eligibility": "Senior citizens aged 57 years and above residing in Telangana belonging to vulnerable and BPL households. One pension per eligible household.",
            "docs": "Aadhaar Card, Food Security Card (White Ration card), age proof (voter ID / birth certificate), bank/post office account details.",
            "procedure": "1. Apply at nearest MeeSeva centre or Mandal Parishad Development Officer (MPDO) office.\n2. Field verification conducted by Panchayat Secretary / Bill Collector.\n3. Direct pension credit to bank/post office savings account.",
            "url": "https://aasara.telangana.gov.in",
            "dates": "Disbursed every month directly to beneficiary accounts.",
            "rules": [
                ("state", "Must reside in Telangana", "TS"),
                ("min_age", "Minimum age is 57 years for Old Age Pension", ">=57"),
                ("occupation", "Senior citizens, widows, and vulnerable groups", "senior_citizen"),
            ]
        },
    ]

    for item in schemes_data:
        state_obj = states.get(item["state"]) if item["state"] else None
        scheme, created = Scheme.objects.get_or_create(
            scheme_name=item["name"],
            defaults={
                "organization": orgs[item["org"]],
                "category": categories[item["cat"]],
                "applicable_state": state_obj,
                "scheme_type": item["type"],
                "benefits": item["benefits"],
                "eligibility_info": item["eligibility"],
                "required_documents": item["docs"],
                "application_procedure": item["procedure"],
                "official_source_url": item["url"],
                "important_dates": item["dates"],
                "last_verified_date": date.today(),
            }
        )
        if created and "rules" in item:
            for cond_type, desc, val in item["rules"]:
                EligibilityRule.objects.create(
                    scheme=scheme,
                    condition_type=cond_type,
                    condition_description=desc,
                    value_criteria=val
                )

    # 5. Policies (Private and Public financial/insurance policies with real fine-print conditions)
    policies_data = [
        {
            "name": "Star Health Comprehensive Insurance Policy",
            "org": "Star Health and Allied Insurance",
            "cat": "Insurance",
            "state": None,
            "type": "insurance",
            "benefits": "Covers in-patient hospitalization expenses, room rent without capping for normal rooms, day-care procedures, organ donor expenses, air ambulance up to ₹5 Lakhs, and maternity coverage after 24 months.",
            "eligibility": "Any individual aged between 18 and 65 years. Dependent children covered from 91 days to 25 years.",
            "terms": "Annual renewal policy with 30 days grace period. Premium increases with age bands. Free-look cancellation period of 15 days from policy receipt.",
            "exclusions": "IMPORTANT FINE PRINT: Initial waiting period of 30 days for any non-accidental illness; Specific disease waiting period of 24 months (cataract, hernia, joint replacement); Pre-existing diseases (PED) covered only after 36 months continuous coverage. Cosmetology, routine health checkups, and unproven treatments are excluded.",
            "url": "https://www.starhealth.in/comprehensive-health-insurance",
            "rules": [
                ("min_age", "Minimum entry age is 18 years", ">=18"),
                ("max_age", "Maximum entry age is 65 years", "<=65"),
            ]
        },
        {
            "name": "HDFC Life Sanchay Plus (Guaranteed Returns Plan)",
            "org": "HDFC Life Insurance Co.",
            "cat": "Financial assistance",
            "state": None,
            "type": "investment",
            "benefits": "Guaranteed tax-free regular income or lump sum payout with life cover throughout the policy term. Flexible premium payment options from 5 to 12 years.",
            "eligibility": "Entry age 5 years to 60 years. Minimum annual premium ₹30,000.",
            "terms": "Mandatory minimum premium paying term. Lock-in period of 5 years. Lapsed policies can be revived within 5 years of first unpaid premium.",
            "exclusions": "IMPORTANT FINE PRINT & SURRENDER CHARGES: High surrender penalty if cancelled during the first 3 years (Guaranteed Surrender Value is only 30% to 50% of total premiums paid). Death benefit excludes suicide within first 12 months. Tax exemption under Sec 10(10D) capped if total annual life insurance premium exceeds ₹5,00,000.",
            "url": "https://www.hdfclife.com/savings-plans/sanchay-plus",
            "rules": [
                ("min_age", "Minimum entry age is 18 years for policyholder", ">=18"),
                ("max_age", "Maximum entry age is 60 years", "<=60"),
            ]
        },
        {
            "name": "SBI Scholar Loan for Higher Education",
            "org": "State Bank of India (SBI)",
            "cat": "Education loans",
            "state": None,
            "type": "loan",
            "benefits": "100% financing for tuition fees, examination fees, hostel, and books up to ₹40 Lakhs for premier institutions (IITs, IIMs, NITs) with zero processing fees and zero collateral security.",
            "eligibility": "Indian national students who have secured admission to selected premier institutions in India through entrance test or merit selection.",
            "terms": "Moratorium period of Course Period + 12 months. Repayment tenure up to 15 years after moratorium. Concession of 0.50% interest rate for female students.",
            "exclusions": "IMPORTANT FINE PRINT: Pre-payment penalties may apply if refinanced through private NBFCs before 3 years. Co-borrower (parent/guardian) is mandatory. Penal interest of 2% per annum charged on overdue EMIs. Processing charges of 1.5% if course is outside specified List-A institutions.",
            "url": "https://sbi.co.in/web/personal-banking/loans/education-loans/scholar-loan",
            "rules": [
                ("occupation", "Must be an enrolled student in approved higher education institution", "student"),
            ]
        }
    ]

    for item in policies_data:
        state_obj = states.get(item["state"]) if item["state"] else None
        pol, created = Policy.objects.get_or_create(
            policy_name=item["name"],
            defaults={
                "organization": orgs[item["org"]],
                "category": categories[item["cat"]],
                "applicable_state": state_obj,
                "policy_type": item["type"],
                "benefits": item["benefits"],
                "eligibility_info": item["eligibility"],
                "terms_conditions_summary": item["terms"],
                "key_exclusions": item["exclusions"],
                "official_source_url": item["url"],
                "last_verified_date": date.today(),
            }
        )
        if created and "rules" in item:
            for cond_type, desc, val in item["rules"]:
                EligibilityRule.objects.create(
                    policy=pol,
                    condition_type=cond_type,
                    condition_description=desc,
                    value_criteria=val
                )

    print(f"Seed data population completed! Total schemes: {Scheme.objects.count()}, Policies: {Policy.objects.count()}")

if __name__ == '__main__':
    populate_seed_data()
