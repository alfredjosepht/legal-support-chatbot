# Legal Support Chatbot - Complete System Guide

## Overview

An NLP-based legal awareness system that addresses all major crimes, discrimination, and legal violations affecting students as recognized under Indian law, using context-aware classification and rule-based legal mapping.

**Key Principle**: "The chatbot does not attempt to identify exact legal offences. Instead, it identifies the legal context using NLP and applies rule-based mappings to present relevant legal awareness."

---

## System Components

### 1. NLP Model (`models/legal_textcat/`)
- **Type**: spaCy text classification (multi-label)
- **Categories**: 19 comprehensive categories covering all student legal issues
- **Purpose**: Produces initial confidence scores for categorization

### 2. Rule Engine (`nlp/postprocess_v2.py`)
- **Purpose**: Applies context-aware filtering and safety rules
- **Functions**:
  - Context extraction (age, authority, medium, discrimination type)
  - Threshold-based filtering
  - Rule-based category refinement
  - Legal framework assignment

### 3. Backend API (`app.py`)
- **Framework**: FastAPI
- **Endpoint**: `/chat` (POST)
- **Input**: Student's problem description
- **Output**: Rich context + applicable legal frameworks + resources

### 4. Data Layer (`data/`)
- `law_mapping.json` - Laws per category
- `legal_steps.json` - What to do for each issue
- `resources.json` - Helplines and support services
- `case_laws.json` - Real Indian case law examples

---

## 19 Legal Categories

### Discrimination & Identity-Based Crimes (6)
| Category | Trigger Keywords | Legal Framework |
|----------|------------------|-----------------|
| `caste_discrimination` | Caste, jati, dalit, brahmin, scheduled, casteism | SC/ST Act 1989, Article 17 |
| `racism` | Northeast, Assam, race, ethnic, tribal, foreigner | IPC §153, Constitution |
| `religious_discrimination` | Religion, faith, prayer, forced conversion, communal | IPC §295-298 |
| `gender_discrimination` | Gender, sexism, unequal treatment | SHWW Act, IPC |
| `sexual_harassment` | Unwanted advances, inappropriate comments, touching | IPC §354, POCSO (if minor) |
| `general_discrimination` | Other protected characteristics | Constitution, equal protection |

### Physical & Ragging (4)
| Category | Trigger Keywords | Legal Framework |
|----------|------------------|-----------------|
| `physical_assault` | Hit, beaten, kicked, injured, violence | IPC §336-338 |
| `ragging` | Ritualistic abuse, humiliation, seniors, "fagging" | Anti-Ragging Act 1997 |
| `threats` | Threat to life, will kill, will harm, blackmail | IPC §503-506 |
| `stalking` | Follows, repeated, constant, surveillance, obsessed | IPC §354D |

### Sexual Crimes (2)
| Category | Trigger Keywords | Legal Framework |
|----------|------------------|-----------------|
| `sexual_assault` | Non-consensual contact, coercion, rape attempt | IPC §375-376, POCSO (if minor) |
| `cyber_sexual_crime` | Sextortion, morphing, intimate content, non-consent | IT Act §67, POCSO (if minor) |

### Cyber Crimes (3)
| Category | Trigger Keywords | Legal Framework |
|----------|------------------|-----------------|
| `cyber_harassment` | Online abuse, hate messages, repeated emails | IT Act §67 |
| `impersonation_doxxing` | Identity theft, personal info leaked, fake profile | IT Act §66C-66E |
| `online_hate_speech` | Targeted online discrimination, hate messages | IT Act §67, IPC §295-298 |

### Institutional & Administrative (2)
| Category | Trigger Keywords | Legal Framework |
|----------|------------------|-----------------|
| `institutional_misconduct` | College, bond, certificate, retaliation, abuse of authority | UGC Regulations, University Code |
| `administrative_violation` | Certificate blocking, TC, migration, forced undertaking | Right to Education Act, Consumer Law |

### Other Crimes (2)
| Category | Trigger Keywords | Legal Framework |
|----------|------------------|-----------------|
| `blackmail_extortion` | Demands under threat, extortion, coercion | IPC §383-389 |
| `defamation_privacy_fraud` | False statements, privacy violation, cheating, impersonation | IPC §499-503, IT Act §66 |

---

## Context-Aware Rule System

### Rule 1: Age-Based Classification (Non-Negotiable)

```
IF age < 18 AND sexual content detected:
    → POCSO Framework (Protection of Children from Sexual Offences Act)
    → Lower confidence threshold (≥ 0.15 for sexual harassment)
    
IF age ≥ 18 AND sexual content detected:
    → IPC Framework (Indian Penal Code)
    → Higher confidence threshold (≥ 0.18 for sexual harassment)
    
IF age unknown AND sexual keywords present:
    → FLAG WARNING: "Age information required for accurate legal framework"
```

**Why**: POCSO applies ONLY to minors and provides stronger protection. This must be automatic, never manual.

---

### Rule 2: Context Validation (Cyber/Physical)

```
IF cyber_harassment claimed:
    REQUIRE: Online keywords (whatsapp, email, instagram, etc.)
    REQUIRE: confidence ≥ 0.18
    
IF physical_assault claimed:
    REQUIRE: Physical action keywords (hit, beaten, kicked, etc.)
    REQUIRE: confidence ≥ 0.20
    
IF medium = 'offline' BUT cyber keywords present:
    → Mark as 'mixed' medium
    → Show both cyber AND offline advice
```

---

### Rule 3: Authority-Based Institutional Upgrade

```
IF discrimination detected AND perpetrator is teacher/admin/hostel_warden:
    THEN: ALSO classify as 'institutional_misconduct'
    REASON: Abuse of authority is institutional failure
    
EXAMPLE: Student reports caste discrimination by professor
    OUTPUT includes:
    - caste_discrimination (confidence 0.78)
    - institutional_misconduct (confidence 0.72)
```

---

### Rule 4: Discrimination Intersectionality

```
IF MULTIPLE discrimination types detected (e.g., caste + gender):
    SHOW ALL in matched_categories
    REASON: Real experiences are intersectional
    
EXAMPLE: "As a Dalit woman, I faced discrimination"
    OUTPUT includes:
    - caste_discrimination (confidence 0.75)
    - gender_discrimination (confidence 0.68)
```

---

## API Response Format

### Request
```bash
POST /chat
{
  "message": "My professor has been harassing me sexually for months. I'm a college student."
}
```

### Response
```json
{
  "category": "sexual_harassment",
  "confidence": 0.82,
  "reason": "classified",
  "matched_categories": [
    {"category": "sexual_harassment", "confidence": 0.82},
    {"category": "institutional_misconduct", "confidence": 0.75}
  ],
  "context": {
    "age_indicator": "adult",
    "authority": "faculty",
    "medium": "offline",
    "discrimination_types": [],
    "legal_framework": null
  },
  "legal_frameworks": [
    "IPC Section 354 (Sexual Harassment)",
    "IPC Section 509 (Word, gesture intended to insult modesty)",
    "University Code of Conduct",
    "UGC Regulations on Faculty Misconduct"
  ],
  "laws": [
    {
      "name": "Indian Penal Code Section 354",
      "text": "Assault or criminal force to woman with intent to outrage her modesty"
    },
    ...
  ],
  "steps": [
    "Document all incidents with dates and witnesses",
    "Report to Internal Complaints Committee (ICC)",
    "File written complaint with college administration",
    "If not resolved, file police complaint (FIR)",
    ...
  ],
  "resources": [
    {
      "type": "helpline",
      "name": "ARIVOLI Helpline",
      "number": "1800-425-8525",
      "description": "Women's legal support"
    },
    ...
  ],
  "case_references": [
    {
      "case_name": "Vishaka vs State of Rajasthan (1997)",
      "year": 1997,
      "summary": "Established guidelines for workplace sexual harassment",
      "relevance": "Sets framework for institutional accountability"
    },
    ...
  ],
  "warnings": [
    "This involves a faculty member. Institutional procedures should be initiated immediately."
  ]
}
```

---

## Classification Thresholds

| Scenario | Threshold | Reason |
|----------|-----------|--------|
| Sexual crime (minor) | ≥ 0.15 | POCSO protection is stronger |
| Sexual harassment (adult) | ≥ 0.18 | Adult framework requires higher certainty |
| Physical assault | ≥ 0.20 | High threshold (objective evidence) |
| Threats | ≥ 0.22 | Very high threshold (potential false positives) |
| Discrimination | ≥ 0.15 | Moderate threshold (important protection) |
| Institutional misconduct | ≥ 0.12 | Lower threshold (authority relationships) |
| All others | ≥ 0.10 | Standard baseline |

---

## Safety Mechanisms

✅ **Automatic Age Detection**: Minor + sexual = POCSO framework, no manual override

✅ **Context Validation**: Cyber without online keywords = rejected

✅ **Authority Hierarchy**: Teachers > peers in institutional pathways

✅ **Intersectionality**: Shows multiple categories when relevant

✅ **Warning System**: Flags ambiguous cases for human review

✅ **Conservative Approach**: Errs on side of protection, not accusation

---

## What the System Does ✅

1. **Identifies Legal Context** - What type of situation
2. **Extracts Demographics** - Age, authority, medium
3. **Applies Contextual Rules** - Age-aware, authority-aware filtering
4. **Assigns Legal Frameworks** - Applicable laws
5. **Provides Resources** - Helplines, complaint procedures
6. **Shows Case Examples** - Real Indian case law

---

## What the System DOES NOT Do ❌

1. **Identify exact IPC sections** - That's for lawyers
2. **Declare guilt** - That's for courts
3. **Judge severity** - That's contextual
4. **Name accused** - System-level safety
5. **Diagnose conditions** - Not medical
6. **Advise on punishment** - Legal role only

---

## Deployment Instructions

### Backend Setup
```bash
# Install dependencies
pip install fastapi uvicorn spacy

# Run the server
python -m uvicorn app:app --reload
# Server runs on http://localhost:8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
# Frontend runs on http://localhost:3000
```

### API Documentation
Visit `http://localhost:8000/docs` for interactive API documentation

---

## File Structure

```
legal-support-chatbot/
├── app.py                          # FastAPI backend
├── NLP_HANDOVER_V2.md              # Updated NLP specification
├── SYSTEM_ARCHITECTURE.md          # This document
├── models/
│   └── legal_textcat/              # Trained spaCy model
├── nlp/
│   ├── postprocess_v2.py           # Rule engine with context extraction
│   ├── train_classifier.py         # Training script
│   └── test_classifier.py          # Testing script
├── data/
│   ├── law_mapping.json            # Laws per category
│   ├── legal_steps.json            # Procedural steps
│   ├── resources.json              # Helplines & services
│   └── case_laws.json              # Case law database
└── frontend/
    └── [React app files]
```

---

## Design Philosophy

### 1. NLP as Context Identifier
The neural network identifies patterns and produces confidence scores, but doesn't make legal decisions.

### 2. Rules for Safety
Explicit, auditable rules ensure:
- Minors always get POCSO protection
- Authority relationships recognized
- Multiple victimizations shown together
- Ambiguity flagged for human review

### 3. Transparency
All rules documented, all categories explained, all frameworks cited.

### 4. Conservative Approach
- Lower thresholds for protection (helping someone who may not need it)
- Higher thresholds for accusations (not wrongly accusing)
- Multiple categories shown (not forcing single narrative)

### 5. Legal Grounding
All categories and frameworks based on Indian law:
- IPC (Indian Penal Code)
- POCSO (2012)
- SC/ST Act (1989)
- IT Act (2000)
- Constitution of India
- UGC Regulations

---

## For Examiners/Stakeholders

### Q: "How do you prevent the AI from making wrong decisions?"
**A**: Two-layer approach:
1. **NLP** identifies patterns
2. **Rules** apply human-designed logic

The AI never makes final decisions. It presents context + frameworks. Humans make actual decisions.

### Q: "What about bias?"
**A**: Rule-based overrides for sensitive determinations, keyword validation, multi-category output, explicit warning system.

### Q: "How do you handle discrimination?"
**A**: Explicitly categorized + rule-checked. When perpetrator is authority, institutional pathway activated. Recognizes intersectionality.

### Q: "Is this just matching keywords?"
**A**: No. Keywords are one input. The NLP model uses deep contextual understanding. Rules then refine based on situation-specific logic.

---

## Testing

### Example Queries

#### Test 1: Minor Sexual Assault
```
"I'm a 16-year-old student. An older boy in my class touched me inappropriately last week."

Expected:
- PRIMARY: sexual_assault (POCSO framework)
- CONTEXT: age_indicator = 'minor'
- WARNINGS: "This involves a minor. Immediate safeguarding procedures recommended."
```

#### Test 2: Caste Discrimination by Teacher
```
"My professor keeps making jokes about my caste. My classmates laugh. I'm scared to raise my hand in class."

Expected:
- PRIMARY: caste_discrimination
- SECONDARY: institutional_misconduct (faculty authority)
- FRAMEWORKS: SC/ST Act, UGC Regulations, University Code
```

#### Test 3: Cyber Harassment
```
"Someone created a fake Facebook profile using my photos and posted hateful comments about my religion."

Expected:
- PRIMARY: impersonation_doxxing + online_hate_speech
- CONTEXT: medium = 'online', discrimination_types = ['religion']
- FRAMEWORKS: IT Act §66C-66E, IPC §295-298
```

---

## Continuous Improvement

1. **Model Retraining**: Add new student cases regularly
2. **Rule Updates**: Adjust thresholds based on feedback
3. **Legal Updates**: Monitor new precedents and legislation
4. **Resource Updates**: Keep helpline numbers current

---

## Support & Contact

For questions about:
- **Legal accuracy**: Consult with legal domain experts
- **NLP model**: Refer to [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md)
- **Rule logic**: Check [NLP_HANDOVER_V2.md](NLP_HANDOVER_V2.md)
- **Deployment**: See deployment instructions above
