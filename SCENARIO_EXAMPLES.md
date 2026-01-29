# Quick Reference: Classification Examples

## Scenario 1: Minor Sexual Assault (POCSO Framework)

**Student Input:**
```
"I'm in 10th grade. My coach touched me inappropriately last week. 
I'm scared and don't know what to do."
```

**System Processing:**
1. **Age Extraction**: "10th grade" → age_indicator = 'minor'
2. **Content**: Sexual + minor → POCSO framework automatic
3. **Confidence**: 0.82 (sexual_assault with minor context)
4. **Threshold Applied**: ≥ 0.15 for minors (LOWER than adults)
5. **Legal Framework**: POCSO 2012

**Output:**
```json
{
  "category": "sexual_assault",
  "confidence": 0.82,
  "context": {
    "age_indicator": "minor",
    "legal_framework": "POCSO"
  },
  "legal_frameworks": [
    "POCSO (Protection of Children from Sexual Offences Act, 2012)",
    "IPC Section 376 (Rape/Sexual Assault)",
    "Constitution Article 15 (Child protection)"
  ],
  "warnings": [
    "This is a MINOR protection case. Immediate safeguarding required.",
    "School administration must be notified.",
    "Police complaint essential."
  ]
}
```

---

## Scenario 2: Caste Discrimination by Faculty (Institutional)

**Student Input:**
```
"My chemistry professor keeps making jokes about my caste. 
He says things like 'untouchable chemistry' when I make mistakes. 
Today he gave me a lower grade than my classmates for the same answer."
```

**System Processing:**
1. **Keyword Detection**: "caste" keyword found → discrimination_type = 'caste'
2. **Authority**: "professor" → authority = 'faculty'
3. **Rule Trigger**: Discrimination + Faculty → also institutional_misconduct
4. **Confidence**: 0.78 (caste_discrimination), 0.72 (institutional_misconduct)
5. **Legal Framework**: SC/ST Act + UGC Regulations

**Output:**
```json
{
  "category": "caste_discrimination",
  "confidence": 0.78,
  "matched_categories": [
    {"category": "caste_discrimination", "confidence": 0.78},
    {"category": "institutional_misconduct", "confidence": 0.72}
  ],
  "context": {
    "age_indicator": "adult",
    "authority": "faculty",
    "discrimination_types": ["caste"]
  },
  "legal_frameworks": [
    "SC/ST (Prevention of Atrocities) Act, 1989 Section 3",
    "Constitution Article 17 (Abolition of Untouchability)",
    "UGC Guidelines on Caste-Based Discrimination",
    "IPC Section 153 (Wantonly giving provocation)"
  ],
  "warnings": [
    "This involves a faculty member in position of authority.",
    "College Internal Complaints Committee (ICC) must be notified.",
    "Document all incidents with dates and witnesses.",
    "This also constitutes institutional misconduct."
  ]
}
```

---

## Scenario 3: Cyber Sexual Crime (Online Medium)

**Student Input:**
```
"Someone created deepfake videos of me from my Instagram photos. 
They're sharing them on WhatsApp groups with sexual captions. 
I don't know who did it but everyone in my college has seen them."
```

**System Processing:**
1. **Medium Detection**: "Instagram", "WhatsApp" → medium = 'online'
2. **Content Type**: "deepfake videos", "sexual" → cyber_sexual_crime
3. **Keyword Validation**: Online keywords present ✓
4. **Confidence**: 0.85 (cyber_sexual_crime), 0.72 (impersonation_doxxing)
5. **Legal Framework**: IT Act + POCSO (if minor)

**Output:**
```json
{
  "category": "cyber_sexual_crime",
  "confidence": 0.85,
  "matched_categories": [
    {"category": "cyber_sexual_crime", "confidence": 0.85},
    {"category": "impersonation_doxxing", "confidence": 0.72}
  ],
  "context": {
    "age_indicator": "adult",
    "medium": "online",
    "discrimination_types": []
  },
  "legal_frameworks": [
    "IT Act 2000 Section 67 (Publishing obscene material online)",
    "IT Act 2000 Section 66C (Identity theft)",
    "IT Act 2000 Section 66E (Violation of privacy)",
    "IPC Section 509 (Word/gesture intended to insult modesty)",
    "IPC Section 354 (Assault with intent to outrage modesty)"
  ],
  "warnings": [
    "This is a serious cyber crime affecting reputation and privacy.",
    "Preserve all evidence (screenshots, links, witness information).",
    "File complaint with Cyber Police Complaint Center (CPCC).",
    "If age < 18, POCSO applies with enhanced protection."
  ]
}
```

---

## Scenario 4: Ragging Physical + Cyber (Mixed Medium)

**Student Input:**
```
"Seniors have been ragging me. They hit me during lunch, 
then post videos on Instagram making fun of me. 
They message me on WhatsApp with insults every night. 
I haven't told my parents because I'm scared."
```

**System Processing:**
1. **Medium**: "hit" (offline) + "Instagram", "WhatsApp" (online) → medium = 'mixed'
2. **Keywords**: Physical ("hit") + Online ("Instagram", "WhatsApp")
3. **Category**: ragging + physical_assault + cyber_harassment
4. **Confidence**: 0.88 (ragging), 0.76 (physical_assault), 0.74 (cyber_harassment)
5. **Authority**: "seniors" → authority = 'senior_student'

**Output:**
```json
{
  "category": "ragging",
  "confidence": 0.88,
  "matched_categories": [
    {"category": "ragging", "confidence": 0.88},
    {"category": "physical_assault", "confidence": 0.76},
    {"category": "cyber_harassment", "confidence": 0.74}
  ],
  "context": {
    "age_indicator": null,
    "authority": "senior_student",
    "medium": "mixed",
    "discrimination_types": []
  },
  "legal_frameworks": [
    "Anti-Ragging Act 1997",
    "IPC Section 336-338 (Acts endangering life/health)",
    "IT Act 2000 Section 67 (Online abuse)",
    "IPC Section 503-506 (Criminal intimidation)",
    "UGC Regulations on Ragging"
  ],
  "warnings": [
    "Age information not provided. If age < 18, additional protections apply.",
    "This involves MULTIPLE forms of harassment: physical + cyber + ragging.",
    "Ragging is illegal in India. Immediate college intervention required.",
    "Parents/guardians should be informed immediately.",
    "File complaint with:
      - College Anti-Ragging Committee
      - Local police
      - National Anti-Ragging Helpline 1800-1000"
  ]
}
```

---

## Scenario 5: Ambiguous Case (Age Unknown, Sexual Content)

**Student Input:**
```
"My friend is being harassed by someone who keeps sending 
inappropriate messages and asking for pictures. 
They're scared and don't know what to do."
```

**System Processing:**
1. **Age**: Not mentioned → age_indicator = None
2. **Sexual Content**: "inappropriate messages", "asking for pictures" → sexual concern detected
3. **Threshold Issue**: Can't apply correct framework without age
4. **System Response**: CLASSIFICATION + WARNING

**Output:**
```json
{
  "category": "cyber_harassment",
  "confidence": 0.65,
  "matched_categories": [
    {"category": "cyber_harassment", "confidence": 0.65},
    {"category": "cyber_sexual_crime", "confidence": 0.58}
  ],
  "context": {
    "age_indicator": null,
    "medium": "online",
    "discrimination_types": []
  },
  "legal_frameworks": [
    "IT Act 2000 Section 67 (Obscene material)",
    "IT Act 2000 Section 67A (Child sexual abuse material)",
    "POCSO 2012 (If victim is minor)"
  ],
  "warnings": [
    "⚠️ CRITICAL: Age of victim is unknown.",
    "If age < 18: POCSO applies with STRONGER protection.",
    "If age ≥ 18: Adult sexual harassment frameworks apply.",
    "IMMEDIATE ACTION REQUIRED:",
    "1. Ask victim's age to determine legal framework",
    "2. If minor: Contact school authorities immediately",
    "3. If adult: File cyber crime complaint with police",
    "4. Preserve all evidence (screenshots, chat history)",
    "5. Contact National Cyber Crime Complaint Center"
  ]
}
```

---

## Scenario 6: Gender Discrimination in Academics

**Student Input:**
```
"I'm a girl in engineering. My professor says girls are 
naturally bad at coding and won't assign me good projects. 
Male students with lower grades get better assignments. 
I feel like I'm being treated unfairly because of my gender."
```

**System Processing:**
1. **Discrimination Type**: "girl", "girls are naturally bad" → discrimination_type = 'gender'
2. **Authority**: "professor" → authority = 'faculty'
3. **Context**: Academic + authority → institutional_misconduct flag
4. **Confidence**: 0.74 (gender_discrimination), 0.68 (institutional_misconduct)
5. **Legal Framework**: SHWW Act + UGC Guidelines

**Output:**
```json
{
  "category": "gender_discrimination",
  "confidence": 0.74,
  "matched_categories": [
    {"category": "gender_discrimination", "confidence": 0.74},
    {"category": "institutional_misconduct", "confidence": 0.68}
  ],
  "context": {
    "age_indicator": "adult",
    "authority": "faculty",
    "discrimination_types": ["gender"]
  },
  "legal_frameworks": [
    "Sexual Harassment of Women at Workplace Act, 2013",
    "Constitution Article 14 (Equality before law)",
    "Constitution Article 15 (Prohibition of discrimination)",
    "IPC Section 354 (Sexual harassment)",
    "UGC Guidelines on Gender Equality"
  ],
  "steps": [
    "Document instances with dates, witnesses, and evidence",
    "Report to Internal Complaints Committee (ICC)",
    "File written complaint with college authorities",
    "Request intervention with professor and department",
    "If unresolved: File formal complaint with:
      - District Legal Services Authority
      - Women's Commission
      - Higher education regulator"
  ],
  "warnings": [
    "This constitutes gender-based discrimination and institutional bias.",
    "Faculty member's conduct violates UGC guidelines.",
    "Academic discrimination is actionable and can be formally challenged."
  ]
}
```

---

## Scenario 7: Institutional Abuse (Certificate Blocking)

**Student Input:**
```
"I graduated 6 months ago but my college won't give me my TC 
(transfer certificate) because I wrote a complaint against 
the college on social media about their unfair fee structure. 
The director told me I'd regret speaking up."
```

**System Processing:**
1. **Institutional Keywords**: "TC", "college", "director", "complaint", "regret" → institutional misconduct
2. **Authority**: "director" → authority = 'administration'
3. **Violation**: Certificate withholding + threat → retaliation
4. **Context**: Administrative abuse + threatened
5. **Confidence**: 0.82 (institutional_misconduct), 0.75 (threats)

**Output:**
```json
{
  "category": "institutional_misconduct",
  "confidence": 0.82,
  "matched_categories": [
    {"category": "institutional_misconduct", "confidence": 0.82},
    {"category": "administrative_violation", "confidence": 0.76},
    {"category": "threats", "confidence": 0.65}
  ],
  "context": {
    "age_indicator": "adult",
    "authority": "administration",
    "discrimination_types": []
  },
  "legal_frameworks": [
    "Right to Education Act, 2009",
    "UGC Regulations on Institutional Conduct",
    "Consumer Protection Act, 2019",
    "IPC Section 506 (Criminal intimidation)",
    "IPC Section 384 (Extortion)"
  ],
  "steps": [
    "Send formal written demand to college registrar (via registered mail)",
    "If no response: File complaint with:
      - District Education Officer
      - State Human Rights Commission
      - State Consumer Protection Authority",
    "Escalate to:
      - University administration
      - Ministry of Education (if deemed university)",
      "Seek legal aid from law college/legal services authority"
  ],
  "warnings": [
    "Certificate withholding is ILLEGAL and violates your rights.",
    "Retaliation for complaints is PROHIBITED under law.",
    "This is abuse of institutional power.",
    "Document all communications as evidence."
  ]
}
```

---

## Common Misclassifications the System PREVENTS

### ❌ Mistake 1: "Cyber harassment" for offline bullying
```
Input: "They keep bullying me in the hostel."
Without validation: WRONG classification as cyber_harassment
With validation: System checks for online keywords → REJECTED
Correct classification: physical_assault or threats (depending on context)
```

### ❌ Mistake 2: "Sexual harassment" for gender discrimination
```
Input: "Professors call on boys more than girls in class."
Without nuance: Could be sexual_harassment
With context: System recognizes this is gender_discrimination (different legal framework)
Correct classification: gender_discrimination (structural) vs sexual_harassment (personal)
```

### ❌ Mistake 3: Missing institutional misconduct when teacher involved
```
Input: "Professor said discriminatory things to me."
Without rule: Just caste_discrimination
With rule: When authority+discrimination → ALSO institutional_misconduct
Output: Both categories shown, both frameworks provided
```

### ❌ Mistake 4: Applying adult thresholds to minors
```
Input: Minor reports sexual contact
Without age rule: confidence might not meet 0.18 threshold
With age rule: POCSO framework + 0.15 threshold (lower, more protective)
Result: Correct classification and legal framework
```

---

## Key Takeaway

The system works by:
1. **Extracting Context** (age, authority, medium, discrimination type)
2. **Applying Rules** (not just raw NLP scores)
3. **Validating Keywords** (cyber needs online keywords, etc.)
4. **Assigning Frameworks** (POCSO for minors, SC/ST Act for caste, etc.)
5. **Showing Multiple Categories** (intersectionality + authority effects)
6. **Flagging Ambiguity** (age unknown, etc. → warnings)

This makes it **safe, transparent, and defensible** even in complex situations.
