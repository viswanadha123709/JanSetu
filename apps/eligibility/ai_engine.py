"""
JanSetu AI Eligibility Engine & Conversational Advisor
Understands user profile and queries, evaluates eligibility against database rules,
generates explanations, missing info checklists, alternatives, and official links.
Bilingual: English & Telugu.
"""

import re
from apps.schemes.models import Scheme, Policy, EligibilityRule, State, Category

DISCLAIMER_EN = "\n\n⚠️ **Important Notice**: *JanSetu AI provides guidance based on published guidelines. AI assessments do not guarantee eligibility or official approval. Final approval decisions rest solely with the competent government authority or issuing organization.*"

DISCLAIMER_TE = "\n\n⚠️ **ముఖ్య గమనిక**: *జనసేతు AI అందించే సమాచారం మార్గదర్శకాలపై ఆధారపడిన సూచన మాత్రమే. తుది అర్హత మరియు ఆమోద నిర్ణయాలు సంబంధిత ప్రభుత్వ శాఖ లేదా సంస్థ పరిధిలో ఉంటాయి.*"

class EligibilityAdvisor:
    @staticmethod
    def extract_profile_from_text(query_text, user_profile=None):
        """Extracts profile attributes (occupation, state, income, age) from text or UserProfile."""
        text = query_text.lower()
        extracted = {
            "occupation": None,
            "state_code": None,
            "income": None,
            "age": None,
        }

        # 1. State extraction
        if "andhra" in text or "ap" in text or "ఆంధ్ర" in text:
            extracted["state_code"] = "AP"
        elif "telangana" in text or "ts" in text or "తెలంగాణ" in text:
            extracted["state_code"] = "TS"

        # 2. Occupation extraction
        if re.search(r'\b(farmer|cultivator|rythu|raithu|వ్యవసాయ|రైతు)\b', text):
            extracted["occupation"] = "farmer"
        elif re.search(r'\b(student|scholarship|college|engineering|degree|విద్యార్థి|చదువు)\b', text):
            extracted["occupation"] = "student"
        elif re.search(r'\b(senior|pension|old age|elderly|వృద్ధు|పెన్షన్)\b', text):
            extracted["occupation"] = "senior_citizen"
        elif re.search(r'\b(business|entrepreneur|startup|shop|mudra|వ్యాపార|ఉద్యోగ)\b', text):
            extracted["occupation"] = "entrepreneur"
        elif re.search(r'\b(woman|women|female|మహిళ)\b', text):
            extracted["occupation"] = "women"

        # 3. Income extraction
        inc_match = re.search(r'(?:income|earning|సంవత్సర ఆదాయం|ఆదాయం)[\s:isof₹rs\.]*([\d,]+)', text)
        if inc_match:
            try:
                extracted["income"] = int(inc_match.group(1).replace(',', ''))
            except ValueError:
                pass
        elif "1.5" in text or "1,50,000" in text or "150000" in text:
            extracted["income"] = 150000
        elif "2" in text and "lakh" in text:
            extracted["income"] = 200000

        # 4. Age extraction
        age_match = re.search(r'\b(?:age|వయస్సు)[\s:isof]*(\d{1,2})\b', text)
        if age_match:
            try:
                extracted["age"] = int(age_match.group(1))
            except ValueError:
                pass

        # Fill missing from user_profile if provided
        if user_profile:
            if not extracted["occupation"] and user_profile.occupation != 'general_public':
                extracted["occupation"] = user_profile.occupation
            if not extracted["state_code"]:
                if "Andhra" in user_profile.state:
                    extracted["state_code"] = "AP"
                elif "Telangana" in user_profile.state:
                    extracted["state_code"] = "TS"
            if not extracted["age"] and user_profile.age:
                extracted["age"] = user_profile.age

        return extracted

    @classmethod
    def evaluate_eligibility(cls, query_text, user_profile=None, language='en'):
        """Evaluates database schemes against user criteria and formats a conversational response."""
        profile = cls.extract_profile_from_text(query_text, user_profile)
        occupation = profile["occupation"]
        state_code = profile["state_code"]
        income = profile["income"]
        age = profile["age"]

        # Filter schemes from database
        matched_schemes = []
        schemes_qs = Scheme.objects.filter(is_active=True)

        if state_code:
            schemes_qs = schemes_qs.filter(applicable_state__state_code__in=[state_code, None])

        for s in schemes_qs:
            score = 0
            reasons = []

            # Check category / occupation match
            cat_name = s.category.category_name.lower()
            if occupation == "farmer" and "agriculture" in cat_name:
                score += 3
                reasons.append("Matches your farmer/agriculture profile")
            elif occupation == "student" and ("scholarship" in cat_name or "education" in cat_name):
                score += 3
                reasons.append("Matches your student education profile")
            elif occupation == "senior_citizen" and ("senior" in cat_name or "pension" in s.scheme_name.lower()):
                score += 3
                reasons.append("Matches senior citizen welfare criteria")
            elif occupation in ["entrepreneur", "small_business_owner"] and ("entrepreneurship" in cat_name or "business" in cat_name):
                score += 3
                reasons.append("Matches your business/entrepreneurship goal")

            # Check state applicability
            if s.applicable_state:
                if state_code and s.applicable_state.state_code == state_code:
                    score += 2
                    reasons.append(f"Specifically active in {s.applicable_state.state_name}")
                elif not state_code:
                    reasons.append(f"Requires residency in {s.applicable_state.state_name}")
            else:
                score += 1
                reasons.append("Central All-India coverage")

            # Check income rules if present
            if income is not None:
                max_inc_rule = s.rules.filter(condition_type='max_income').first()
                if max_inc_rule:
                    try:
                        max_limit = int(re.sub(r'[^\d]', '', max_inc_rule.value_criteria))
                        if income <= max_limit:
                            score += 2
                            reasons.append(f"Income ₹{income:,} is within eligible ceiling of ₹{max_limit:,}")
                        else:
                            score -= 3
                            reasons.append(f"Income ₹{income:,} exceeds published ceiling of ₹{max_limit:,}")
                    except (ValueError, TypeError):
                        pass

            if score >= 2:
                matched_schemes.append((score, s, reasons))

        matched_schemes.sort(key=lambda x: x[0], reverse=True)

        # Build follow-up questions if critical information is missing
        follow_ups = []
        if not state_code:
            follow_ups.append("Which state do you reside in (Andhra Pradesh, Telangana, or other)?")
        if not occupation:
            follow_ups.append("What is your primary occupation (e.g., Farmer, Student, Senior Citizen, Entrepreneur)?")
        if income is None:
            follow_ups.append("What is your approximate annual household income?")

        # Format Response
        if language == 'te':
            return cls._format_telugu_response(profile, matched_schemes[:4], follow_ups)
        else:
            return cls._format_english_response(profile, matched_schemes[:4], follow_ups)

    @classmethod
    def _format_english_response(cls, profile, top_schemes, follow_ups):
        lines = []
        occ_display = profile["occupation"].replace('_', ' ').capitalize() if profile["occupation"] else "Citizen"
        state_display = "Andhra Pradesh" if profile["state_code"] == "AP" else ("Telangana" if profile["state_code"] == "TS" else "All India")
        
        lines.append(f"Hello! Based on your query for **{occ_display}** in **{state_display}**" + 
                     (f" with annual income ₹{profile['income']:,}" if profile['income'] else "") + ":\n")

        if top_schemes:
            lines.append("### Recommended Opportunities You Appear Eligible For:\n")
            for score, s, reasons in top_schemes:
                state_label = s.applicable_state.state_name if s.applicable_state else "Central Scheme"
                lines.append(f"#### 1. **{s.scheme_name}** ({state_label})")
                lines.append(f"- **Key Benefits**: {s.benefits}")
                lines.append(f"- **Why You Match**: {', '.join(reasons)}")
                lines.append(f"- **Eligibility Criteria**: {s.eligibility_info}")
                lines.append(f"- **Documents Checklist**: {s.required_documents}")
                lines.append(f"- **Official Application Portal**: [{s.official_source_url}]({s.official_source_url})\n")
        else:
            lines.append("We could not find immediate high-confidence matches with the current keywords. Please review the details below:\n")

        if follow_ups:
            lines.append("### To confirm your full eligibility, please clarify:")
            for q in follow_ups:
                lines.append(f"- {q}")

        lines.append(DISCLAIMER_EN)
        return "\n".join(lines)

    @classmethod
    def _format_telugu_response(cls, profile, top_schemes, follow_ups):
        lines = []
        occ_display = "రైతు" if profile["occupation"] == "farmer" else ("విద్యార్థి" if profile["occupation"] == "student" else ("వృద్ధులు" if profile["occupation"] == "senior_citizen" else "పౌరులు"))
        state_display = "ఆంధ్రప్రదేశ్" if profile["state_code"] == "AP" else ("తెలంగాణ" if profile["state_code"] == "TS" else "భారతదేశం")

        lines.append(f"నమస్కారం! **{state_display}** లోని **{occ_display}** ప్రొఫైల్ ఆధారంగా ఈ క్రింది పథకాలు మీకు వర్తించవచ్చు:\n")

        if top_schemes:
            lines.append("### మీరు దరఖాస్తు చేసుకోగల ముఖ్యమైన పథకాలు:\n")
            for score, s, reasons in top_schemes:
                state_label = s.applicable_state.state_name if s.applicable_state else "కేంద్ర ప్రభుత్వ పథకం"
                lines.append(f"#### **{s.scheme_name}** ({state_label})")
                lines.append(f"- **ప్రయోజనాలు**: {s.benefits}")
                lines.append(f"- **అర్హత నిబంధనలు**: {s.eligibility_info}")
                lines.append(f"- **కావలసిన పత్రాలు**: {s.required_documents}")
                lines.append(f"- **అధికారిక వెబ్‌సైట్ లింక్**: [{s.official_source_url}]({s.official_source_url})\n")

        if follow_ups:
            lines.append("### పూర్తి అర్హతను నిర్ధారించడానికి దయచేసి క్రింది వివరాలు తెలియజేయండి:")
            for q in follow_ups:
                lines.append(f"- {q}")

        lines.append(DISCLAIMER_TE)
        return "\n".join(lines)
