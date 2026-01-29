"""
Enhanced Postprocessing Module with Age-Based Rules & Discrimination Handling
"""

import re

# Keyword sets for context validation
ONLINE_KEYWORDS = ["online", "whatsapp", "instagram", "facebook", "message", "dm", "email", 
                   "twitter", "telegram", "snapchat", "tiktok", "video call", "phone call",
                   "chat", "text", "posted", "shared", "screenshot", "website", "forum",
                   "comment", "post", "profile", "account"]

PHYSICAL_KEYWORDS = ["hit", "beaten", "assault", "injured", "kicked", "slapped", "attacked",
                     "punched", "pushed", "threw", "beat", "strike", "punch", "bleed",
                     "hospital", "bruise", "wound", "fracture", "violence", "physically"]

PERSISTENCE_KEYWORDS = ["follows", "followed", "repeated", "constant", "every day", "everyday",
                        "always", "continuous", "persistent", "keeps", "stalks", "watches",
                        "observes", "tracks", "monitors", "surveillance", "every class",
                        "every time", "whenever", "obsessed"]

COLLEGE_KEYWORDS = ["college", "university", "hostel", "campus", "management", "administration",
                    "principal", "director", "dean", "faculty", "professor", "teacher",
                    "certificate", "tc", "migration", "bond", "undertaking", "admission",
                    "scholarship", "files", "records", "officials", "office", "dorm"]

CASTE_KEYWORDS = ["caste", "jati", "dalit", "obc", "general", "forward", "scheduled",
                  "backward", "bhangi", "chamar", "mali", "iyer", "iyengar", "jat",
                  "brahmin", "scavenging", "untouchable", "casteist", "casteism",
                  "brahminical", "varna", "caste slur"]

RACE_KEYWORDS = ["northeast", "north-east", "assam", "manipur", "nagaland", "mizoram",
                 "arunachal", "meghalaya", "tripura", "sikkim", "race", "racial",
                 "foreigner", "chinese", "african", "skin color", "skin colour",
                 "tribal", "indigenous", "ethnicity", "ethnic", "national origin"]

RELIGION_KEYWORDS = ["hindu", "muslim", "christian", "sikh", "buddhist", "jain",
                     "islam", "christianity", "sikhism", "buddhism", "jainism",
                     "religion", "faith", "belief", "temple", "mosque", "church",
                     "prayer", "ritual", "forced conversion", "communal", "communalism"]

GENDER_KEYWORDS = ["female", "male", "transgender", "trans", "woman", "man", "girl", "boy",
                   "gender", "sexism", "patriarchy", "masculinity", "femininity",
                   "unequal treatment", "sex-based", "sexual orientation"]

THREAT_KEYWORDS = ["threat", "will kill", "kill you", "will hurt", "will beat", "will rape",
                   "threat to life", "will harm", "will damage", "will expose", "suicide",
                   "blackmail", "will tell", "or else", "if you don't"]

AGE_KEYWORDS_MINOR = ["class 10", "class 11", "class 12", "10th", "11th", "12th",
                      "school", "16 years", "17 years", "18 years", "minor", "underage",
                      "below 18", "u-18", "teenager", "kid", "child", "year old"]

AGE_KEYWORDS_ADULT = ["college", "university", "adult", "18", "19", "20", "21", "22",
                      "23", "24", "25", "postgraduate", "pg", "btech", "bca", "mtech"]

AUTHORITY_KEYWORDS = ["teacher", "professor", "faculty", "principal", "director", "dean",
                      "warden", "senior", "administration", "admin", "official", "manager",
                      "incharge", "head of department", "hod", "hod"]


def extract_age_indicator(text):
    """
    Extract age indicator from text.
    Returns: 'minor', 'adult', or None
    """
    text_lower = text.lower()
    
    # Check for explicit age mentions - multiple patterns
    # Pattern 1: "I am 16 years old"
    age_match = re.search(r'(?:am|is|was)\s+(\d+)\s*(?:years?|yr|yrs)?(?:\s+old)?', text_lower)
    if age_match:
        age = int(age_match.group(1))
        if 5 <= age <= 100:  # Sanity check
            if age < 18:
                return 'minor'
            else:
                return 'adult'
    
    # Pattern 2: Just "16" when talking about age
    age_match2 = re.search(r'age[:\s]+(\d+)', text_lower)
    if age_match2:
        age = int(age_match2.group(1))
        if 5 <= age <= 100:
            if age < 18:
                return 'minor'
            else:
                return 'adult'
    
    # Check keyword patterns
    if any(kw in text_lower for kw in AGE_KEYWORDS_MINOR):
        return 'minor'
    
    if any(kw in text_lower for kw in AGE_KEYWORDS_ADULT):
        return 'adult'
    
    return None


def extract_authority(text):
    """
    Extract authority information from text.
    Returns: authority type or None
    """
    text_lower = text.lower()
    
    if any(kw in text_lower for kw in AUTHORITY_KEYWORDS):
        if "teacher" in text_lower or "professor" in text_lower or "faculty" in text_lower:
            return 'faculty'
        elif "principal" in text_lower or "director" in text_lower or "dean" in text_lower:
            return 'administration'
        elif "warden" in text_lower or "hostel" in text_lower:
            return 'hostel_warden'
        elif "senior" in text_lower:
            return 'senior_student'
        else:
            return 'authority_figure'
    
    return None


def extract_medium(text):
    """
    Extract whether incident is online or offline.
    Returns: 'online', 'offline', or 'mixed'
    """
    text_lower = text.lower()
    
    online_count = sum(1 for kw in ONLINE_KEYWORDS if kw in text_lower)
    physical_count = sum(1 for kw in PHYSICAL_KEYWORDS if kw in text_lower)
    
    if online_count > 0 and physical_count == 0:
        return 'online'
    elif physical_count > 0 and online_count == 0:
        return 'offline'
    elif online_count > 0 and physical_count > 0:
        return 'mixed'
    else:
        # If no clear indicators, check for general context
        if any(kw in text_lower for kw in COLLEGE_KEYWORDS):
            return 'offline'  # Assume campus incidents are offline by default
        return None


def extract_discrimination_type(text):
    """
    Detect if discrimination involves specific protected characteristics.
    Returns: list of discrimination types
    """
    text_lower = text.lower()
    discrimination_types = []
    
    if any(kw in text_lower for kw in CASTE_KEYWORDS):
        discrimination_types.append('caste')
    
    if any(kw in text_lower for kw in RACE_KEYWORDS):
        discrimination_types.append('race')
    
    if any(kw in text_lower for kw in RELIGION_KEYWORDS):
        discrimination_types.append('religion')
    
    if any(kw in text_lower for kw in GENDER_KEYWORDS):
        discrimination_types.append('gender')
    
    return discrimination_types


def postprocess_categories(text, raw_cats):
    """
    Apply comprehensive rule-based filtering with context awareness.
    """
    text_lower = text.lower()
    final_cats = {}
    
    # Extract context
    age_indicator = extract_age_indicator(text)
    authority = extract_authority(text)
    medium = extract_medium(text)
    discrimination_types = extract_discrimination_type(text)
    
    context = {
        'age_indicator': age_indicator,
        'authority': authority,
        'medium': medium,
        'discrimination_types': discrimination_types
    }
    
    # ========== RULE: Age-Based Sexual Crime Classification ==========
    # CRITICAL: For ANY minor mentioning sexual content, trigger POCSO immediately
    
    if age_indicator == 'minor':
        # For minors: Always use POCSO framework for ANY sexual content
        if 'sexual_harassment' in raw_cats and raw_cats['sexual_harassment'] >= 0.10:
            final_cats['sexual_harassment'] = raw_cats['sexual_harassment']
            context['legal_framework'] = 'POCSO'
        
        if 'sexual_assault' in raw_cats and raw_cats['sexual_assault'] >= 0.08:
            final_cats['sexual_assault'] = raw_cats['sexual_assault']
            context['legal_framework'] = 'POCSO'
        
        # Also check for other sexual crimes
        if 'cyber_sexual_crime' in raw_cats and raw_cats['cyber_sexual_crime'] >= 0.10:
            final_cats['cyber_sexual_crime'] = raw_cats['cyber_sexual_crime']
            context['legal_framework'] = 'POCSO'
    
    elif age_indicator == 'adult':
        # For adults: Lower threshold for sexual crimes
        if 'sexual_harassment' in raw_cats and raw_cats['sexual_harassment'] >= 0.12:
            final_cats['sexual_harassment'] = raw_cats['sexual_harassment']
        
        if 'sexual_assault' in raw_cats and raw_cats['sexual_assault'] >= 0.09:
            final_cats['sexual_assault'] = raw_cats['sexual_assault']
    
    # ========== RULE: Context Validation (Online/Offline) ==========
    
    if 'cyber_harassment' in raw_cats:
        if medium in ['online', 'mixed'] or any(kw in text_lower for kw in ONLINE_KEYWORDS):
            if raw_cats['cyber_harassment'] >= 0.18:
                final_cats['cyber_harassment'] = raw_cats['cyber_harassment']
        # Remove if purely offline and no online indicators
        elif medium == 'offline' or not any(kw in text_lower for kw in ONLINE_KEYWORDS):
            pass
    
    if 'online_hate_speech' in raw_cats:
        if medium in ['online', 'mixed']:
            if raw_cats['online_hate_speech'] >= 0.16:
                final_cats['online_hate_speech'] = raw_cats['online_hate_speech']
    
    if 'cyber_sexual_crime' in raw_cats:
        if medium in ['online', 'mixed']:
            if raw_cats['cyber_sexual_crime'] >= 0.20:
                final_cats['cyber_sexual_crime'] = raw_cats['cyber_sexual_crime']
    
    if 'impersonation_doxxing' in raw_cats:
        if medium in ['online', 'mixed']:
            if raw_cats['impersonation_doxxing'] >= 0.18:
                final_cats['impersonation_doxxing'] = raw_cats['impersonation_doxxing']
    
    # ========== RULE: Physical Action Validation ==========
    
    if 'physical_assault' in raw_cats:
        if any(kw in text_lower for kw in PHYSICAL_KEYWORDS):
            if raw_cats['physical_assault'] >= 0.20:
                final_cats['physical_assault'] = raw_cats['physical_assault']
        # Remove if no physical action indicators
        else:
            pass
    
    if 'ragging' in raw_cats and raw_cats['ragging'] >= 0.18:
        # Ragging can be physical or non-physical
        final_cats['ragging'] = raw_cats['ragging']
    
    # ========== RULE: Stalking - Requires Persistence ==========
    
    if 'stalking' in raw_cats:
        if any(kw in text_lower for kw in PERSISTENCE_KEYWORDS):
            if raw_cats['stalking'] >= 0.18:
                final_cats['stalking'] = raw_cats['stalking']
    
    # ========== RULE: Threat Validation ==========
    
    if 'threats' in raw_cats:
        if any(kw in text_lower for kw in THREAT_KEYWORDS):
            if raw_cats['threats'] >= 0.20:
                final_cats['threats'] = raw_cats['threats']
    
    # ========== RULE: Discrimination with Authority ==========
    
    discrimination_categories = [
        'caste_discrimination', 'racism', 'religious_discrimination', 
        'gender_discrimination', 'general_discrimination'
    ]
    
    for disc_cat in discrimination_categories:
        if disc_cat in raw_cats and raw_cats[disc_cat] >= 0.15:
            final_cats[disc_cat] = raw_cats[disc_cat]
            
            # If by authority figure: Also flag institutional misconduct
            if authority in ['faculty', 'administration', 'hostel_warden']:
                if 'institutional_misconduct' in raw_cats:
                    final_cats['institutional_misconduct'] = max(
                        raw_cats.get('institutional_misconduct', 0), 
                        raw_cats[disc_cat] - 0.1  # Slightly lower confidence
                    )
    
    # ========== RULE: Institutional Context Upgrade ==========
    
    if any(kw in text_lower for kw in COLLEGE_KEYWORDS):
        # College context → institutional possibilities higher
        if authority in ['faculty', 'administration']:
            if 'institutional_misconduct' in raw_cats and raw_cats['institutional_misconduct'] >= 0.12:
                final_cats['institutional_misconduct'] = raw_cats['institutional_misconduct']
        
        # Threats in college context
        if 'threats' in raw_cats and raw_cats['threats'] >= 0.15:
            final_cats['institutional_misconduct'] = max(
                final_cats.get('institutional_misconduct', 0),
                raw_cats['threats'] - 0.05
            )
    
    # ========== RULE: Standard Thresholds ==========
    
    # Categories not explicitly handled above
    standard_threshold_cats = [
        'blackmail_extortion', 'defamation_privacy_fraud', 'sexual_harassment'
    ]
    
    for cat in standard_threshold_cats:
        if cat not in final_cats and cat in raw_cats:
            if raw_cats[cat] >= 0.10:
                final_cats[cat] = raw_cats[cat]
    
    # ========== RULE: General Categories (Fallback) ==========
    
    for cat, score in raw_cats.items():
        if cat not in final_cats and score >= 0.10:
            final_cats[cat] = score
    
    # Sort by confidence
    final_cats = dict(sorted(final_cats.items(), key=lambda x: x[1], reverse=True))
    
    return final_cats, context


def get_legal_framework(category, context):
    """
    Determine applicable legal framework based on category and context.
    """
    age_indicator = context.get('age_indicator')
    discrimination_types = context.get('discrimination_types', [])
    
    frameworks = []
    
    # POCSO Framework - For ALL minors in sexual crimes
    if age_indicator == 'minor' and category in ['sexual_assault', 'sexual_harassment', 'cyber_sexual_crime']:
        frameworks.append('Protection of Children from Sexual Offences Act, 2012 (POCSO)')
    
    # IPC - Base framework for most crimes
    if category in ['physical_assault', 'threats', 'blackmail_extortion', 'defamation_privacy_fraud', 'verbal_abuse']:
        frameworks.append('Indian Penal Code (IPC)')
    
    # Sexual Crimes - IPC Sections 375-376
    if category in ['sexual_assault', 'sexual_harassment'] and age_indicator != 'minor':
        frameworks.append('Indian Penal Code (IPC) Sections 375-376 (Rape & Sexual Assault)')
    
    # Gender-based Sexual Harassment Act
    if category == 'sexual_harassment':
        frameworks.append('Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013')
    
    # Cyber crimes - IT Act
    if category in ['cyber_harassment', 'cyber_sexual_crime', 'impersonation_doxxing', 'online_hate_speech']:
        frameworks.append('Information Technology (IT) Act, 2000 (Cyber Crime)')
    
    # Caste Discrimination
    if 'caste' in discrimination_types or category == 'caste_discrimination':
        frameworks.append('Scheduled Castes and Scheduled Tribes (Prevention of Atrocities) Act, 1989')
        frameworks.append('Constitution of India - Article 17 (Abolition of Untouchability)')
    
    # Religious Discrimination
    if 'religion' in discrimination_types or category == 'religious_discrimination':
        frameworks.append('Indian Penal Code (IPC) Sections 295-298 (Religious Offences)')
    
    # Racial/Ethnic Discrimination
    if 'race' in discrimination_types or category == 'racism':
        frameworks.append('Indian Penal Code (IPC) Section 153-153A (Promoting Enmity)')
    
    # Gender Discrimination
    if 'gender' in discrimination_types or category == 'gender_discrimination':
        frameworks.append('Equality Code - Constitution Article 14-15')
        frameworks.append('Gender Discrimination in Education & Employment Laws')
    
    # Ragging
    if category == 'ragging':
        frameworks.append('UGC (Promotion of Ragging Prevention) Regulations, 2009')
        frameworks.append('Anti-Ragging Act & National Anti-Ragging Rules')
    
    # Institutional/Administrative violations
    if category in ['institutional_misconduct', 'administrative_violation']:
        frameworks.append('National Council for Teacher Education (NCTE) Regulations')
        frameworks.append('University Grants Commission (UGC) Regulations')
        frameworks.append('Constitution Articles 14, 21, 32 (Right to Equality & Liberty)')
    
    # General Discrimination
    if category == 'general_discrimination':
        frameworks.append('Constitution of India - Articles 14-15')
        frameworks.append('Equal Opportunity Laws')
    
    # Stalking
    if category == 'stalking':
        frameworks.append('Indian Penal Code (IPC) Section 503-506 (Criminal Intimidation)')
        frameworks.append('Information Technology (IT) Act, 2000 (if cyber stalking)')
    
    return list(set(frameworks))  # Remove duplicates
