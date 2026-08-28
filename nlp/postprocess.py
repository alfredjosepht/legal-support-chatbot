"""
Enhanced Postprocessing Module with Age-Based Rules, Discrimination Handling & Framework Mapping
"""

import re

# Keyword sets for context validation
ONLINE_KEYWORDS = [
    "online", "whatsapp", "instagram", "facebook", "message", "dm", "email", 
    "twitter", "telegram", "snapchat", "tiktok", "video call", "phone call",
    "chat", "text", "posted", "shared", "screenshot", "website", "forum",
    "comment", "post", "profile", "account", "cyber", "cyberbully", "social media",
    "app", "application", "discord", "gaming", "game", "hack", "hacked",
    "upload", "uploaded", "internet", "send", "sends", "sending", "sent", "texting", "dms",
    "receive", "received", "receiving", "inbox"
]

CYBER_SEXUAL_KEYWORDS = [
    "nude", "nudes", "dick pic", "dick pics", "naked pic", "naked pics", "naked photo",
    "naked photos", "intimate photo", "intimate photos", "intimate video", "intimate videos",
    "explicit video", "explicit photo", "sextortion", "deepfake", "deepfakes", "morphed photo",
    "morphed pic", "morphed video", "revenge porn", "genitals",
    "private photo", "private photos", "private pic", "private pics", "private video", "private videos",
    "inappropriate photo", "inappropriate photos", "inappropriate pic", "inappropriate pics",
    "inappropriate picture", "inappropriate pictures", "inappropriate image", "inappropriate images",
    "inappropriate video", "inappropriate videos", "inapproriate",
    "unsolicited photo", "unsolicited photos", "unsolicited pic", "unsolicited pics",
    "unsolicited picture", "unsolicited pictures", "unsolicited image", "unsolicited images",
    "unwanted photo", "unwanted photos", "unwanted pic", "unwanted pics",
    "unwanted picture", "unwanted pictures", "vulgar message", "vulgar messages",
    "vulgar pic", "vulgar pics", "vulgar photo", "vulgar photos"
]

PHYSICAL_KEYWORDS = [
    "hit", "beaten", "assault", "injured", "kicked", "kick", "slapped", "slap", "attacked",
    "punched", "punch", "pushed", "push", "shoved", "shove", "threw", "beat", "strike", "bleed",
    "hospital", "bruise", "wound", "fracture", "violence", "physically", "stabbed", "stab", "choked", "choke"
]

PERSISTENCE_KEYWORDS = [
    "follows", "followed", "repeated", "constant", "every day", "everyday",
    "always", "continuous", "persistent", "keeps", "stalks", "watches",
    "observes", "tracks", "monitors", "surveillance", "every class",
    "every time", "whenever", "obsessed"
]

COLLEGE_KEYWORDS = [
    "college", "university", "hostel", "campus", "management", "administration",
    "principal", "director", "dean", "faculty", "professor", "teacher",
    "certificate", "tc", "migration", "bond", "undertaking", "admission",
    "scholarship", "files", "records", "officials", "office", "dorm"
]

CASTE_KEYWORDS = [
    "caste", "jati", "dalit", "obc", "general", "forward", "scheduled",
    "backward", "bhangi", "chamar", "mali", "iyer", "iyengar", "jat",
    "brahmin", "scavenging", "untouchable", "casteist", "casteism",
    "brahminical", "varna", "caste slur"
]

RACE_KEYWORDS = [
    "northeast", "north-east", "assam", "manipur", "nagaland", "mizoram",
    "arunachal", "meghalaya", "tripura", "sikkim", "race", "racial",
    "foreigner", "chinese", "african", "skin color", "skin colour",
    "tribal", "indigenous", "ethnicity", "ethnic", "national origin",
    "color", "colour", "dark skin", "black", "brown", "mixed race"
]

RELIGION_KEYWORDS = [
    "hindu", "muslim", "christian", "sikh", "buddhist", "jain",
    "islam", "christianity", "sikhism", "buddhism", "jainism",
    "religion", "religious", "faith", "belief", "temple", "mosque", "church",
    "prayer", "prayers", "ritual", "rituals", "religious practices", "religious practice",
    "religious attire", "hijab", "turban", "burqa", "cross", "namaz", "puja", "pooja",
    "fasting", "halal", "forced conversion", "communal", "communalism"
]

GENDER_KEYWORDS = [
    "female", "male", "transgender", "trans", "woman", "women", "man", "men",
    "girl", "girls", "boy", "boys", "gender", "sexism", "patriarchy",
    "masculinity", "femininity", "unequal treatment", "sex-based", "sexual orientation"
]

THREAT_KEYWORDS = [
    "threat", "threats", "threatens", "threatening", "threatened", "threaten",
    "will kill", "kill you", "kill me", "will hurt", "hurt me", "will beat", "will rape",
    "threat to life", "threat of violence", "threatened with violence", "death threat", "death threats",
    "threat of harm", "threats of harm", "will harm", "harm me", "will damage", "will expose", "will leak",
    "would harm", "would hurt", "would expose", "would leak", "would post",
    "suicide", "blackmail", "will tell", "or else",
    "if you don't", "if i dont", "if i don't", "threatened to", "threat of self-harm", "threats of self-harm"
]

CYBERBULLYING_KEYWORDS = [
    "bullying", "bully", "bullied", "mock", "mocking", "mocked", "taunt", "taunting",
    "insult", "insulting", "insulted", "humiliate", "humiliation", "humiliating",
    "shame", "shaming", "shamed", "embarrass", "embarrassing", "embarrassed",
    "ridicule", "ridiculing", "ridiculous", "tease", "teasing", "teased",
    "spread rumors", "rumour", "spreading lies", "spread lies", "saying false", "saying false things", "false things",
    "fake account", "fake profile", "mass tagging", "meme", "edited photo", "private messages exposed", "viral",
    "exclude", "excluding", "excluded", "group exclusion", "mean messages", "mean comments",
    "abusive messages", "abusive comments", "cruel", "cruelty", "nasty", "vicious",
    "cyber", "cyberbully", "cyberbullying", "cyberbullied", "harass", "harassment",
    "stalk", "stalking", "threatening", "blackmail", "coerce", "coercion",
    "revenge porn", "intimate images", "leaked photos", "leaked videos", "leaked messages",
    "doxing", "doxx", "personal information", "leak", "leaked", "exposed"
]

VERBAL_ABUSE_KEYWORDS = [
    "bad word", "bad words", "vulgar", "abuse", "abusive language",
    "slang", "swear", "swearing", "curse", "cursing", "profanity",
    "offensive language", "name calling", "slur", "verbal abuse",
    "foul language", "verbal", "verbally", "yells", "yelling", "shouted", "shouting",
    "insult", "insulting", "insulted", "insults",
    "humiliate", "humiliating", "humiliated", "humiliation",
    "derogatory", "degrading", "demean", "demeaning"
]

IMPERSONATION_KEYWORDS = [
    "fake profile", "fake account", "fake id", "using my face", "using my photo",
    "using my photos", "using my name", "using my picture", "using my pictures",
    "using my identity", "impersonat", "impersonating", "impersonation", "impersonate",
    "pretending to be me", "pretend to be me", "catfish", "catfishing", "doxx", "doxxing",
    "leaked my number", "leaked my phone", "leaked my address", "posted my address",
    "shared my contact", "shared my phone", "shared my address", "identity theft",
    "stole my photos", "stole my picture", "cloned my profile", "cloned my account"
]

DEFAMATION_KEYWORDS = [
    "defam", "defamed", "defaming", "defamation", "defamatory", "slander", "slandered",
    "slandering", "libel", "ruin my reputation", "ruining my reputation", "tarnish my reputation",
    "damaged my reputation", "false rumor", "false rumours", "spreading lies", "spread lies",
    "false allegations", "saying false things",
    "telling lies", "told lies", "telling false",
    "ruining my name", "ruin my name", "ruining my image",
    "spreading rumors", "spread rumors", "false rumors", "false rumor"
]

GENERAL_DISCRIMINATION_KEYWORDS = [
    "discriminate", "discrimination", "discriminated", "discriminating", "disability",
    "disabled", "wheelchair", "handicap", "poor family", "financial background", "poverty",
    "language bias", "regional bias", "medical condition", "socio-economic",
    "based on appearance", "appearance", "based on age", "age discrimination", "ageism",
    "due to my beliefs", "based on stereotypes", "economic status", "regional background", "outsider"
]

STALKING_KEYWORDS = [
    "stalk", "stalking", "stalked", "stalker",
    "follows me", "followed me", "following me", "watches me", "watching me",
    "constantly watches", "waits for me", "waited for me", "waiting for me",
    "outside my hostel", "near my class", "near my room", "near my house",
    "sees me everywhere", "seeing the same person", "loiters", "loitering",
    "observes me", "observing me", "obsessively tracks"
]

HATE_SPEECH_KEYWORDS = [
    "hate on", "hating on", "hateful", "hate speech", "hate campaign",
    "hate against", "targeting community", "targeting my community",
    "attack my community", "attacking my community", "hate my community",
    "spread hate", "spreading hate"
]

TRACKING_KEYWORDS = [
    "tracking my location", "track my location", "tracking my phone",
    "monitoring my location", "following my location", "tracking where i",
    "track where i", "location tracking", "tracking my movements"
]

BLACKMAIL_KEYWORDS = [
    "blackmail", "blackmailing", "blackmailed", "extort",
    "extorting", "extortion", "ransom", "demand money", "demanding money",
    "demands money", "pay money", "threatens to expose", "threatens to release",
    "threatens to leak", "threatens to post", "threatening to leak",
    "threatening to post", "threatening to expose", "threatened to post",
    "threatened to leak", "threatened to expose", "would leak my",
    "if i dont pay", "if i don't pay", "if you dont pay", "if you don't pay",
    "leak my chats", "leak my messages", "pay her or", "pay him or",
    "pay or", "or she will leak", "or he will leak", "if i don't", "if i dont"
]

AGE_KEYWORDS_MINOR = [
    "class 10", "class 11", "class 12", "10th", "11th", "12th",
    "school", "16 years", "17 years", "18 years", "minor", "underage",
    "below 18", "u-18", "teenager", "kid", "child", "year old"
]

AGE_KEYWORDS_ADULT = [
    "college", "university", "adult", "18", "19", "20", "21", "22",
    "23", "24", "25", "postgraduate", "pg", "btech", "bca", "mtech"
]

AUTHORITY_KEYWORDS = [
    "teacher", "professor", "faculty", "principal", "director", "dean",
    "warden", "senior", "administration", "admin", "official", "manager",
    "incharge", "head of department", "hod"
]


def extract_age_indicator(text: str) -> str | None:
    """
    Extract age indicator from text.
    Returns: 'minor', 'adult', or None
    """
    text_lower = text.lower()
    
    # Check for explicit age mentions - pattern 1: "I am 16 years old"
    age_match = re.search(r'(?:am|is|was)\s+(\d+)\s*(?:years?|yr|yrs)?(?:\s+old)?', text_lower)
    if age_match:
        age = int(age_match.group(1))
        if 5 <= age <= 100:
            return 'minor' if age < 18 else 'adult'
    
    # Pattern 2: "age: 16"
    age_match2 = re.search(r'age[:\s]+(\d+)', text_lower)
    if age_match2:
        age = int(age_match2.group(1))
        if 5 <= age <= 100:
            return 'minor' if age < 18 else 'adult'
    
    # Check keyword patterns
    if any(kw in text_lower for kw in AGE_KEYWORDS_MINOR):
        return 'minor'
    
    if any(kw in text_lower for kw in AGE_KEYWORDS_ADULT):
        return 'adult'
    
    return None


def extract_authority(text: str) -> str | None:
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


def _has_kw(text: str, kw: str) -> bool:
    """Check if keyword appears as a whole word or exact phrase."""
    if " " in kw:
        return kw in text
    return bool(re.search(r'\b' + re.escape(kw) + r'\b', text))


def extract_medium(text: str) -> str | None:
    """
    Extract whether incident is online or offline.
    Returns: 'online', 'offline', 'mixed', or None
    """
    text_lower = text.lower()
    
    online_count = sum(1 for kw in ONLINE_KEYWORDS if _has_kw(text_lower, kw))
    physical_count = sum(1 for kw in PHYSICAL_KEYWORDS if _has_kw(text_lower, kw))
    
    if online_count > 0 and physical_count == 0:
        return 'online'
    elif physical_count > 0 and online_count == 0:
        return 'offline'
    elif online_count > 0 and physical_count > 0:
        return 'mixed'
    else:
        if any(_has_kw(text_lower, kw) for kw in COLLEGE_KEYWORDS):
            return 'offline'
        return None


def extract_discrimination_type(text: str) -> list[str]:
    """
    Detect if discrimination involves specific protected characteristics.
    Returns: list of discrimination types
    """
    text_lower = text.lower()
    discrimination_types = []
    
    if any(_has_kw(text_lower, kw) for kw in CASTE_KEYWORDS):
        discrimination_types.append('caste')
    
    if any(_has_kw(text_lower, kw) for kw in RACE_KEYWORDS):
        discrimination_types.append('race')
    
    if any(_has_kw(text_lower, kw) for kw in RELIGION_KEYWORDS):
        discrimination_types.append('religion')
    
    if any(_has_kw(text_lower, kw) for kw in GENDER_KEYWORDS):
        discrimination_types.append('gender')
    
    return discrimination_types


def postprocess_categories(text: str, raw_cats: dict[str, float]) -> tuple[dict[str, float], dict]:
    """
    Apply comprehensive rule-based filtering with context awareness.
    """
    text_lower = text.lower()
    final_cats: dict[str, float] = {}
    
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
    # Only apply POCSO boosts when actual sexual keywords are present
    _has_sexual_kw_pocso = any(_has_kw(text_lower, kw) for kw in [
        'rape', 'raped', 'sexual', 'assault', 'harass', 'touch', 'touched',
        'molest', 'groped', 'penetrated', 'stare', 'catcall', 'lewd', 'obscene'
    ])
    if age_indicator == 'minor':
        if _has_sexual_kw_pocso:
            if 'sexual_harassment' in raw_cats and raw_cats['sexual_harassment'] >= 0.10:
                final_cats['sexual_harassment'] = raw_cats['sexual_harassment']
                context['legal_framework'] = 'POCSO'
            
            if 'sexual_assault' in raw_cats and raw_cats['sexual_assault'] >= 0.08:
                final_cats['sexual_assault'] = raw_cats['sexual_assault']
                context['legal_framework'] = 'POCSO'
        
        if 'cyber_sexual_crime' in raw_cats and raw_cats['cyber_sexual_crime'] >= 0.10:
            final_cats['cyber_sexual_crime'] = raw_cats['cyber_sexual_crime']
            context['legal_framework'] = 'POCSO'

    # ========== RULE: Authority / College context favors Ragging ==========
    if authority == 'senior_student' or any(kw in text_lower for kw in COLLEGE_KEYWORDS) or 'ragg' in text_lower:
        has_ragging_keywords = 'ragg' in text_lower or any(kw in text_lower for kw in 
                                                           ['senior', 'juniors', 'initiation', 'ritualistic'])
        has_admin_keywords = any(kw in text_lower for kw in ['certificate', 'documents', 'TC', 'migration', 
                                                              'hold', 'held', 'withhold', 'deny', 'refuse', 'fees', 
                                                              'bond', 'undertaking', 'admin', 'office', 'paper', 'exam', 
                                                              'marks', 'grade', 'assignment', 'degree', 'result'])
        has_sexual_keywords = any(kw in text_lower for kw in ['rape', 'sexual', 'assault', 'harass', 'touch', 'molest'])

        if has_ragging_keywords and 'ragging' in raw_cats:
            boosted = max(raw_cats.get('ragging', 0), 0.22)
            final_cats['ragging'] = boosted

            if not has_sexual_keywords:
                if 'sexual_assault' in raw_cats:
                    raw_cats['sexual_assault'] = 0.0
                if 'sexual_harassment' in raw_cats:
                    raw_cats['sexual_harassment'] = 0.0

        elif has_admin_keywords and 'administrative_violation' in raw_cats:
            boosted = max(raw_cats.get('administrative_violation', 0), 0.20)
            final_cats['administrative_violation'] = boosted
        elif has_admin_keywords and 'institutional_misconduct' in raw_cats:
            boosted = max(raw_cats.get('institutional_misconduct', 0), 0.20)
            final_cats['institutional_misconduct'] = boosted
        elif 'ragging' in raw_cats and not has_sexual_keywords:
            if authority in ['faculty', 'administration']:
                if 'institutional_misconduct' in raw_cats:
                    boosted = max(raw_cats.get('institutional_misconduct', 0), 0.20)
                    final_cats['institutional_misconduct'] = boosted
            else:
                boosted = max(raw_cats.get('ragging', 0), 0.22)
                final_cats['ragging'] = boosted
    
    if age_indicator == 'adult':
        has_sexual_keywords = any(kw in text_lower for kw in ['rape', 'sexual', 'assault', 'harass', 'touch', 'molest'])
        if has_sexual_keywords:
            if 'sexual_harassment' in raw_cats and raw_cats['sexual_harassment'] >= 0.12:
                final_cats['sexual_harassment'] = max(raw_cats['sexual_harassment'], 0.30)
            if 'sexual_assault' in raw_cats and raw_cats['sexual_assault'] >= 0.09:
                final_cats['sexual_assault'] = max(raw_cats['sexual_assault'], 0.30)
    
    # ========== RULE: Sexual Crimes (General - Age Unknown) ==========
    if age_indicator is None:
        has_sexual_keywords = any(kw in text_lower for kw in ['rape', 'raped', 'sexual', 'assault', 'harass', 'touch', 'touched', 'molest'])
        if has_sexual_keywords:
            if 'sexual_assault' in raw_cats and raw_cats['sexual_assault'] >= 0.07:
                final_cats['sexual_assault'] = max(raw_cats['sexual_assault'], 0.30)
            if authority in ['faculty', 'administration'] or any(kw in text_lower for kw in ['touch', 'touched', 'harass', 'comment', 'comments']):
                final_cats['sexual_harassment'] = max(raw_cats.get('sexual_harassment', 0), 0.30)
            elif 'sexual_harassment' in raw_cats and raw_cats['sexual_harassment'] >= 0.10:
                final_cats['sexual_harassment'] = max(raw_cats['sexual_harassment'], 0.30)
    
    # ========== RULE: Context Validation (Online/Offline) ==========
    has_bullying_terms = any(_has_kw(text_lower, term) for term in ['bullying', 'bullied', 'bully', 'cyberbullying', 'cyberbullied', 'cyberbully'])
    has_explicit_cyber = any(_has_kw(text_lower, term) for term in ['cyberbullying', 'cyberbullied', 'cyberbully'])
    has_cyber_sexual = any(_has_kw(text_lower, kw) for kw in CYBER_SEXUAL_KEYWORDS)
    has_online_kws = any(_has_kw(text_lower, kw) for kw in ONLINE_KEYWORDS)
    is_online = (medium in ['online', 'mixed']) or has_online_kws or has_explicit_cyber or has_cyber_sexual

    if not is_online and not has_explicit_cyber and not has_cyber_sexual:
        for cyber_cat in ['cyber_harassment', 'cyber_bullying', 'online_hate_speech', 'cyber_sexual_crime', 'impersonation_doxxing']:
            if cyber_cat in raw_cats:
                raw_cats[cyber_cat] = 0.0
            if cyber_cat in final_cats:
                del final_cats[cyber_cat]
    elif medium == 'offline' and not has_explicit_cyber and not has_cyber_sexual:
        for cyber_cat in ['cyber_harassment', 'cyber_bullying', 'online_hate_speech', 'cyber_sexual_crime', 'impersonation_doxxing']:
            if cyber_cat in raw_cats:
                raw_cats[cyber_cat] = 0.0
            if cyber_cat in final_cats:
                del final_cats[cyber_cat]
                
    if 'cyber_harassment' in raw_cats or is_online:
        if is_online:
            has_harass_signals = (
                raw_cats.get('cyber_harassment', 0) >= 0.05
                or any(kw in text_lower for kw in ['message', 'messages', 'comment', 'comments', 'nasty', 'harass', 'stalking', 'insulting', 'humiliate', 'abusive'])
            )
            if has_harass_signals:
                final_cats['cyber_harassment'] = max(raw_cats.get('cyber_harassment', 0), 0.20)
    
    # Keyword-based hate speech detection (lower threshold when online + hate keywords)
    has_hate_speech_kws = any(kw in text_lower for kw in HATE_SPEECH_KEYWORDS)
    if 'online_hate_speech' in raw_cats:
        if medium in ['online', 'mixed']:
            if raw_cats['online_hate_speech'] >= 0.10 or has_hate_speech_kws:
                final_cats['online_hate_speech'] = max(raw_cats.get('online_hate_speech', 0), 0.20)
        elif has_hate_speech_kws and is_online:
            final_cats['online_hate_speech'] = max(raw_cats.get('online_hate_speech', 0), 0.20)
    elif has_hate_speech_kws and is_online:
        final_cats['online_hate_speech'] = max(raw_cats.get('online_hate_speech', 0), 0.20)
    
    if 'cyber_sexual_crime' in raw_cats or has_cyber_sexual:
        if is_online or has_cyber_sexual:
            if has_cyber_sexual or raw_cats.get('cyber_sexual_crime', 0) >= 0.35:
                final_cats['cyber_sexual_crime'] = max(raw_cats.get('cyber_sexual_crime', 0), 0.25)
    
    if 'impersonation_doxxing' in raw_cats or any(_has_kw(text_lower, kw) for kw in IMPERSONATION_KEYWORDS):
        has_imp_kws = any(_has_kw(text_lower, kw) for kw in IMPERSONATION_KEYWORDS)
        if has_imp_kws:
            final_cats['impersonation_doxxing'] = max(raw_cats.get('impersonation_doxxing', 0), 0.25)
        elif (medium in ['online', 'mixed'] or is_online) and raw_cats.get('impersonation_doxxing', 0) >= 0.35:
            final_cats['impersonation_doxxing'] = raw_cats['impersonation_doxxing']

    # Non-consensual photo / video taking (Privacy violation) & Defamation
    has_unauthorized_photo = (
        any(_has_kw(text_lower, kw) for kw in ['without my permission', 'without permission', 'without consent', 'without my consent'])
        and any(_has_kw(text_lower, kw) for kw in ['photo', 'photos', 'picture', 'pictures', 'pic', 'pics', 'image', 'images', 'video', 'videos'])
    )
    has_defamation = any(_has_kw(text_lower, kw) for kw in DEFAMATION_KEYWORDS)
    if has_unauthorized_photo or has_defamation:
        final_cats['defamation_privacy_fraud'] = max(raw_cats.get('defamation_privacy_fraud', 0), 0.25)
    
    # ========== RULE: Cyberbullying & Bullying Validation ==========
    if 'cyber_bullying' in raw_cats or has_bullying_terms:
        has_online_context = medium in ['online', 'mixed'] or any(_has_kw(text_lower, kw) for kw in ONLINE_KEYWORDS)
        has_bullying_keywords = any(_has_kw(text_lower, kw) for kw in CYBERBULLYING_KEYWORDS)
        has_cyber_keywords = any(_has_kw(text_lower, kw) for kw in ['cyber', 'online', 'social media', 'whatsapp', 'facebook', 'instagram'])

        if has_bullying_terms:
            if is_online or has_explicit_cyber or has_online_context or has_cyber_keywords:
                final_cats['cyber_bullying'] = max(raw_cats.get('cyber_bullying', 0), 0.25)
            else:
                final_cats['ragging'] = max(raw_cats.get('ragging', 0), 0.35)
                if 'cyber_bullying' in final_cats:
                    del final_cats['cyber_bullying']
                if 'cyber_bullying' in raw_cats:
                    raw_cats['cyber_bullying'] = 0.0
                if 'defamation_privacy_fraud' in final_cats and not (has_unauthorized_photo or has_defamation):
                    del final_cats['defamation_privacy_fraud']
                if 'defamation_privacy_fraud' in raw_cats and not (has_unauthorized_photo or has_defamation):
                    raw_cats['defamation_privacy_fraud'] = 0.0
        elif (
            has_explicit_cyber
            or (has_online_context and has_bullying_keywords)
            or (has_cyber_keywords and has_bullying_keywords)
            or (has_bullying_keywords and raw_cats.get('cyber_bullying', 0) >= 0.10)
        ):
            if is_online or has_explicit_cyber or has_online_context or has_cyber_keywords:
                if has_cyber_keywords or has_bullying_keywords:
                    boosted_cyber = max(raw_cats.get('cyber_bullying', 0), 0.20)
                else:
                    boosted_cyber = max(raw_cats.get('cyber_bullying', 0), 0.15)

                if not has_unauthorized_photo or has_bullying_terms:
                    final_cats['cyber_bullying'] = boosted_cyber
            else:
                final_cats['ragging'] = max(raw_cats.get('ragging', 0), 0.25)
                if 'cyber_bullying' in final_cats:
                    del final_cats['cyber_bullying']
                if 'cyber_bullying' in raw_cats:
                    raw_cats['cyber_bullying'] = 0.0

        if 'cyber_bullying' in final_cats:
            if raw_cats.get('sexual_assault', 0) < 0.30:
                raw_cats['sexual_assault'] = 0.0
            if raw_cats.get('sexual_harassment', 0) < 0.30:
                raw_cats['sexual_harassment'] = 0.0
    
    # ========== RULE: Physical Action Validation ==========
    if 'physical_assault' in raw_cats or any(_has_kw(text_lower, kw) for kw in PHYSICAL_KEYWORDS) or 'rape' in text_lower or 'raped' in text_lower:
        if any(_has_kw(text_lower, kw) for kw in PHYSICAL_KEYWORDS) or 'rape' in text_lower or 'raped' in text_lower:
            final_cats['physical_assault'] = max(raw_cats.get('physical_assault', 0), 0.35)
        elif raw_cats.get('physical_assault', 0) >= 0.20:
            final_cats['physical_assault'] = raw_cats['physical_assault']

    # ========== RULE: Sexual Assault priority over Physical Assault ==========
    sexual_assault_score = raw_cats.get('sexual_assault', 0)
    physical_assault_score = raw_cats.get('physical_assault', 0)
    _has_sexual_kw = any(_has_kw(text_lower, kw) for kw in ['rape', 'raped', 'sexual', 'molest', 'molested', 'groped', 'penetrated', 'assault'])
    # Only suppress physical_assault in favor of sexual_assault when there's no ragging context
    # (e.g. "my senior raped me" should keep both ragging and physical_assault)
    _has_ragging_context = 'ragg' in text_lower or any(_has_kw(text_lower, kw) for kw in ['senior', 'juniors', 'initiation'])
    if _has_sexual_kw and sexual_assault_score >= 0.30 and not _has_ragging_context:
        if physical_assault_score > 0 and physical_assault_score <= sexual_assault_score * 1.05:
            if 'physical_assault' in final_cats:
                del final_cats['physical_assault']
    
    has_ragging_kw = 'ragg' in text_lower or any(_has_kw(text_lower, kw) for kw in ['senior', 'juniors', 'initiation', 'ritualistic'])
    has_college_kw = any(_has_kw(text_lower, kw) for kw in COLLEGE_KEYWORDS)
    if 'ragging' in raw_cats and (has_ragging_kw or has_college_kw or has_bullying_terms or raw_cats['ragging'] >= 0.35):
        if raw_cats['ragging'] >= 0.18:
            final_cats['ragging'] = raw_cats['ragging']
    
    # ========== RULE: Stalking - Requires Persistence ==========
    has_stalk_kws = any(kw in text_lower for kw in STALKING_KEYWORDS)
    if has_stalk_kws:
        boosted = max(raw_cats.get('stalking', 0), 0.30)
        final_cats['stalking'] = boosted
        if 'physical_assault' in raw_cats and raw_cats['physical_assault'] < 0.20:
            raw_cats['physical_assault'] = 0.0
        if 'cyber_bullying' in raw_cats and raw_cats['cyber_bullying'] < 0.20:
            raw_cats['cyber_bullying'] = 0.0
    elif 'stalking' in raw_cats and any(kw in text_lower for kw in PERSISTENCE_KEYWORDS):
        if raw_cats['stalking'] >= 0.15:
            final_cats['stalking'] = max(raw_cats['stalking'], 0.25)
    
    # ========== RULE: Threat Validation ==========
    if any(kw in text_lower for kw in THREAT_KEYWORDS):
        # Boost to at least 0.20 when explicit threat keywords are present — remove hard score gate
        boosted = max(raw_cats.get('threats', 0), 0.20)
        final_cats['threats'] = boosted
                
    # ========== RULE: Verbal Abuse Validation ==========
    if any(kw in text_lower for kw in VERBAL_ABUSE_KEYWORDS):
        boosted = max(raw_cats.get('verbal_abuse', 0), 0.20)
        final_cats['verbal_abuse'] = boosted
        
    # ========== RULE: Blackmail & Extortion Validation ==========
    if any(kw in text_lower for kw in BLACKMAIL_KEYWORDS):
        boosted = max(raw_cats.get('blackmail_extortion', 0), 0.20)
        final_cats['blackmail_extortion'] = boosted
        if 'physical_assault' in raw_cats and raw_cats['physical_assault'] < 0.20:
            raw_cats['physical_assault'] = 0.0
    
    # ========== RULE: Explicit Discrimination Keywords ==========
    disc_type_to_cat = {
        'caste': 'caste_discrimination',
        'race': 'racism',
        'religion': 'religious_discrimination',
        'gender': 'gender_discrimination'
    }
    
    explicit_disc_cats = []
    for dt in discrimination_types:
        cat_name = disc_type_to_cat.get(dt)
        if cat_name in raw_cats:
            boosted = max(raw_cats.get(cat_name, 0), 0.20)
            final_cats[cat_name] = boosted
            explicit_disc_cats.append(cat_name)
    
    if explicit_disc_cats:
        for disc_cat in ['caste_discrimination', 'racism', 'religious_discrimination', 'gender_discrimination']:
            if disc_cat not in explicit_disc_cats:
                if disc_cat in raw_cats:
                    raw_cats[disc_cat] = 0.0
                if disc_cat in final_cats:
                    del final_cats[disc_cat]

    # ========== RULE: Discrimination with Authority ==========
    discrimination_categories = [
        'caste_discrimination', 'racism', 'religious_discrimination', 
        'gender_discrimination'
    ]
    
    for disc_cat in discrimination_categories:
        disc_type_needed = disc_cat.replace('_discrimination', '')
        has_explicit = (disc_type_needed in discrimination_types) or (disc_cat == 'racism' and 'race' in discrimination_types)
        if has_explicit and disc_cat in raw_cats:
            final_cats[disc_cat] = max(raw_cats[disc_cat], 0.20)
            if authority in ['faculty', 'administration', 'hostel_warden']:
                if 'institutional_misconduct' in raw_cats:
                    final_cats['institutional_misconduct'] = max(
                        raw_cats.get('institutional_misconduct', 0), 
                        raw_cats[disc_cat] - 0.1
                    )
        elif disc_cat in raw_cats and raw_cats[disc_cat] >= 0.40:
            final_cats[disc_cat] = raw_cats[disc_cat]

    has_gen_disc = any(_has_kw(text_lower, kw) for kw in GENERAL_DISCRIMINATION_KEYWORDS)
    if has_gen_disc and not explicit_disc_cats:
        final_cats['general_discrimination'] = max(raw_cats.get('general_discrimination', 0), 0.30)
    elif 'general_discrimination' in raw_cats and raw_cats['general_discrimination'] >= 0.35:
        final_cats['general_discrimination'] = raw_cats['general_discrimination']
    
    # ========== RULE: Institutional Context Upgrade & Pruning ==========
    has_admin_terms = any(_has_kw(text_lower, kw) for kw in ['certificate', 'tc', 'transfer certificate', 'migration', 'marksheet', 'original documents', 'caution deposit', 'bond', 'hall ticket', 'security deposit', 'undertaking', 'affiliation', 'admission cancelled'])
    has_inst_terms = any(_has_kw(text_lower, kw) for kw in ['inquiry', 'complaint', 'retaliat', 'internal committee', 'icc', 'anti-ragging squad', 'victimization', 'kangaroo court', 'ombudsperson', 'whistleblower', 'biased committee'])
    
    if has_admin_terms:
        if 'administrative_violation' in raw_cats:
            final_cats['administrative_violation'] = max(raw_cats['administrative_violation'], 0.22)
            if raw_cats.get('institutional_misconduct', 0) >= 0.10:
                final_cats['institutional_misconduct'] = max(final_cats.get('institutional_misconduct', 0), raw_cats['institutional_misconduct'], 0.30)
            elif 'institutional_misconduct' in final_cats and not has_inst_terms:
                if raw_cats.get('institutional_misconduct', 0) < 0.10:
                    del final_cats['institutional_misconduct']
        elif 'institutional_misconduct' in raw_cats and raw_cats['institutional_misconduct'] >= 0.10:
            final_cats['institutional_misconduct'] = max(final_cats.get('institutional_misconduct', 0), raw_cats['institutional_misconduct'], 0.25)
    
    if 'institutional_misconduct' in raw_cats:
        if has_inst_terms:
            final_cats['institutional_misconduct'] = max(final_cats.get('institutional_misconduct', 0), raw_cats['institutional_misconduct'], 0.25)
        elif (any(kw in text_lower for kw in COLLEGE_KEYWORDS) or authority in ['faculty', 'administration']) and not has_admin_terms:
            if raw_cats['institutional_misconduct'] >= 0.10:
                final_cats['institutional_misconduct'] = max(final_cats.get('institutional_misconduct', 0), raw_cats['institutional_misconduct'], 0.25)
        elif raw_cats['institutional_misconduct'] >= 0.15:
            final_cats['institutional_misconduct'] = max(final_cats.get('institutional_misconduct', 0), raw_cats['institutional_misconduct'], 0.25)

    if 'administrative_violation' in raw_cats and 'administrative_violation' not in final_cats:
        if raw_cats['administrative_violation'] >= 0.15:
            final_cats['administrative_violation'] = raw_cats['administrative_violation']
    
    # ========== RULE: False Positive Suppression ==========
    has_sexual_keywords = any(_has_kw(text_lower, kw) for kw in [
        'rape', 'raped', 'sexual', 'assault', 'harass', 'harassment', 'touch', 'touched',
        'molest', 'molested', 'groped', 'penetrated', 'stare', 'staring', 'catcall', 'catcalling',
        'sexual comment', 'sexual comments', 'sexual joke', 'sexual jokes', 'sexual advance',
        'sexual advances', 'kiss', 'hug', 'wink', 'lewd', 'obscene'
    ])
    if not has_sexual_keywords:
        if 'sexual_assault' in raw_cats and raw_cats['sexual_assault'] < 0.25:
            raw_cats['sexual_assault'] = 0.0
        # Also remove from final_cats if it was added without sexual context
        if 'sexual_assault' in final_cats and raw_cats.get('sexual_assault', 0) == 0.0:
            del final_cats['sexual_assault']
        if 'sexual_harassment' in raw_cats and raw_cats['sexual_harassment'] < 0.20:
            raw_cats['sexual_harassment'] = 0.0
        if 'sexual_harassment' in final_cats and raw_cats.get('sexual_harassment', 0) == 0.0:
            del final_cats['sexual_harassment']
    
    if not has_cyber_sexual:
        if 'cyber_sexual_crime' in raw_cats and raw_cats['cyber_sexual_crime'] < 0.40:
            raw_cats['cyber_sexual_crime'] = 0.0
            if 'cyber_sexual_crime' in final_cats:
                del final_cats['cyber_sexual_crime']
    else:
        if not is_online and not has_bullying_terms:
            for non_sexual in ['cyber_bullying', 'cyber_harassment', 'online_hate_speech', 'cyber_sexual_crime', 'impersonation_doxxing']:
                if non_sexual in raw_cats:
                    raw_cats[non_sexual] = 0.0
                if non_sexual in final_cats:
                    del final_cats[non_sexual]
            
    has_ragging_keywords = 'ragg' in text_lower or any(_has_kw(text_lower, kw) for kw in ['senior', 'juniors', 'initiation', 'ritualistic'])
    has_college_keywords = any(_has_kw(text_lower, kw) for kw in COLLEGE_KEYWORDS)
    if not has_ragging_keywords and not has_college_keywords:
        if 'ragging' in raw_cats and raw_cats['ragging'] < 0.25:
            raw_cats['ragging'] = 0.0
    
    # ========== RULE: Standard Thresholds ==========
    standard_threshold_cats = [
        'defamation_privacy_fraud', 'sexual_harassment'
    ]
    for cat in standard_threshold_cats:
        if cat not in final_cats and cat in raw_cats:
            if raw_cats[cat] >= 0.15:
                final_cats[cat] = raw_cats[cat]
    
    if 'blackmail_extortion' in raw_cats and 'blackmail_extortion' not in final_cats:
        has_blackmail_terms = any(kw in text_lower for kw in BLACKMAIL_KEYWORDS)
        if (has_blackmail_terms and raw_cats['blackmail_extortion'] >= 0.15) or raw_cats['blackmail_extortion'] >= 0.30:
            final_cats['blackmail_extortion'] = raw_cats['blackmail_extortion']

    # ========== RULE: Tracking Keywords → Stalking / Cyber-Harassment ==========
    has_tracking_kws = any(kw in text_lower for kw in TRACKING_KEYWORDS)
    if has_tracking_kws:
        final_cats['stalking'] = max(raw_cats.get('stalking', 0), 0.20)
        if is_online or medium is None:
            final_cats['cyber_harassment'] = max(raw_cats.get('cyber_harassment', 0), 0.20)

    # ========== RULE: Defamation + Online → also Cyber-Harassment ==========
    if has_defamation and is_online:
        final_cats['defamation_privacy_fraud'] = max(raw_cats.get('defamation_privacy_fraud', 0), 0.25)
        # Online defamation (e.g. lies on facebook) also constitutes cyber_harassment
        if raw_cats.get('cyber_harassment', 0) >= 0.05 or 'cyber_harassment' not in final_cats:
            final_cats['cyber_harassment'] = max(raw_cats.get('cyber_harassment', 0), 0.18)

    # ========== RULE: General Categories (Fallback) ==========
    for cat, score in raw_cats.items():
        if cat not in final_cats and score >= 0.25:
            final_cats[cat] = score
    
    # Filter out weak categories (below 0.18)
    final_cats = {k: v for k, v in final_cats.items() if v >= 0.18}

    final_cats = dict(sorted(final_cats.items(), key=lambda x: x[1], reverse=True))
    return final_cats, context


def get_legal_framework(category: str, context: dict) -> list[str]:
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
    if category in ['cyber_harassment', 'cyber_sexual_crime', 'impersonation_doxxing', 'online_hate_speech', 'cyber_bullying']:
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
    
    return sorted(list(set(frameworks)))
