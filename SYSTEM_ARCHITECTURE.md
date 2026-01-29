# System Architecture & Design Philosophy

## Core Principle
**"The chatbot does not attempt to identify exact legal offences. Instead, it identifies the legal context using NLP and applies rule-based mappings to present relevant legal awareness."**

---

## How the System Works: NLP + Rules

### Layer 1: Raw NLP Classification
- **Input**: Student's problem description
- **Process**: Trained spaCy text classifier produces confidence scores for all 19 categories
- **Output**: Raw doc.cats dictionary with scores (0-1) for each category

Example:
```json
{
  "physical_assault": 0.78,
  "ragging": 0.65,
  "caste_discrimination": 0.82,
  "cyber_harassment": 0.12,
  ...
}
```

**Important**: Raw NLP scores are NOT final classifications. They're starting points.

---

### Layer 2: Context Extraction (Rule-Based)
Before filtering, the system extracts 5 key contexts:

#### 2.1 Age Extraction
- **Rule**: Search text for age mentions or age-related keywords
- **Output**: `'minor'` (< 18), `'adult'` (≥ 18), or `None`
- **Purpose**: Determines legal framework (POCSO vs IPC)

Example patterns:
- "I'm 16" → minor
- "Class 10 student" → minor
- "College student" → adult
- No mention → Flag with warning

#### 2.2 Authority Extraction
- **Rule**: Identify if accused is teacher, admin, senior, or peer
- **Output**: `'faculty'`, `'administration'`, `'hostel_warden'`, `'senior_student'`, or `None`
- **Purpose**: Determines if also institutional misconduct

Example patterns:
- "My professor..." → faculty
- "The principal..." → administration
- "A senior student..." → senior_student

#### 2.3 Medium Extraction
- **Rule**: Detect if incident is online, offline, or both
- **Output**: `'online'`, `'offline'`, `'mixed'`, or `None`
- **Purpose**: Filters cyber vs physical classifications

Example patterns:
- "Sent me WhatsApp messages..." → online
- "Hit me in the hostel..." → offline
- "Followed me online and offline..." → mixed

#### 2.4 Discrimination Type Extraction
- **Rule**: Identify if discrimination involves specific protected characteristics
- **Output**: List of `['caste', 'race', 'religion', 'gender']`
- **Purpose**: Applies specific legal frameworks

Example patterns:
- "Because I'm Dalit..." → contains caste
- "Because I'm from Northeast..." → contains race
- "Because I'm Christian..." → contains religion

#### 2.5 Location/Institutional Context
- **Rule**: Check for college/hostel keywords
- **Output**: Boolean + context type
- **Purpose**: Prioritizes institutional misconduct pathways

---

### Layer 3: Rule-Based Filtering
After context extraction, each category is evaluated against threshold + context rules:

#### Rule 3.1: Age-Based Sexual Crime Classification
```
IF sexual_harassment AND age == 'minor' AND confidence >= 0.15:
    INCLUDE with legal_framework = 'POCSO'
    
IF sexual_harassment AND age == 'adult' AND confidence >= 0.18:
    INCLUDE with legal_framework = 'IPC Section 354'
    
IF age == None AND (sexual keywords detected):
    FLAG WARNING: "Age information required for accurate legal framework"
```

**Why this matters**: Minors automatically get POCSO (more protective), adults get IPC. This is non-negotiable legally.

---

#### Rule 3.2: Context Validation (Cyber/Physical)
```
IF cyber_harassment:
    IF medium NOT IN ['online', 'mixed']:
        SKIP (no cyber without online)
    IF confidence < 0.18:
        SKIP (threshold for cyber)
    ELSE:
        INCLUDE

IF physical_assault:
    IF (no physical action keywords):
        SKIP (no violence without physical indicators)
    IF confidence < 0.20:
        SKIP (high threshold for physical)
    ELSE:
        INCLUDE
```

**Why this matters**: Prevents misclassification like "I'm being cyberbullied" → marked as physical assault.

---

#### Rule 3.3: Discrimination with Authority → Institutional Upgrade
```
IF discrimination_category IN ['caste_discrimination', 'racism', 'religious_discrimination', 'gender_discrimination']:
    AND authority IN ['faculty', 'administration', 'hostel_warden']:
    
    THEN: ALSO INCLUDE 'institutional_misconduct' with slightly lower confidence
    
    PURPOSE: Recognize abuse of authority
```

**Why this matters**: When a teacher discriminates, it's not just personal harassment—it's institutional abuse of power.

---

#### Rule 3.4: College Context Threat Upgrade
```
IF college/hostel keywords DETECTED:
    AND threat_category detected:
    
    THEN: PRIORITIZE 'institutional_misconduct'
    
    PURPOSE: Recognize threats as institutional failures
```

---

### Layer 4: Threshold Application
All remaining categories evaluated against confidence thresholds:

| Category | Threshold |
|----------|-----------|
| sexual_assault (minor) | ≥ 0.12 |
| sexual_harassment (adult) | ≥ 0.18 |
| physical_assault | ≥ 0.20 |
| threats | ≥ 0.22 |
| cyber_sexual_crime | ≥ 0.20 |
| caste/racism/religion discrimination | ≥ 0.15 |
| stalking | ≥ 0.18 |
| institutional_misconduct | ≥ 0.12 |
| **All others** | ≥ 0.10 |

---

### Layer 5: Legal Framework Assignment
Based on category + context, assign applicable legal frameworks:

```
IF 'sexual_assault' AND age == 'minor':
    frameworks += 'POCSO (Protection of Children from Sexual Offences Act, 2012)'

IF 'caste_discrimination':
    frameworks += 'SC/ST (Prevention of Atrocities) Act, 1989'
    frameworks += 'Constitution Article 17 (Abolition of Untouchability)'

IF 'cyber_harassment':
    frameworks += 'IT Act, 2000 (Cyber Crime provisions)'

IF 'institutional_misconduct' AND authority == 'faculty':
    frameworks += 'UGC Regulations on Faculty Misconduct'
    frameworks += 'University Code of Conduct'
```

---

### Layer 6: Response Construction
Final response includes:

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
    "medium": "offline",
    "discrimination_types": ["caste"]
  },
  "legal_frameworks": [
    "SC/ST (Prevention of Atrocities) Act, 1989",
    "Constitution Article 17",
    "UGC Faculty Misconduct Regulations"
  ],
  "warnings": [
    "This involves a faculty member. Institutional procedures should be initiated."
  ]
}
```

---

## What the System Does ✅

1. **Identifies Legal Context** - Not guilt or offence, but the situation type
2. **Extracts Demographics** - Age, authority relationship, medium, identity factors
3. **Applies Rules** - Context-aware filtering prevents misclassifications
4. **Assigns Frameworks** - Provides applicable laws (not interpretations)
5. **Suggests Pathways** - Safe first steps and complaint mechanisms
6. **Flags Warnings** - Age ambiguity, high-risk situations, etc.

---

## What the System DOES NOT Do ❌

1. **Identify exact IPC sections** - That's for lawyers
2. **Declare guilt** - That's for courts
3. **Make severity judgments** - Each situation is unique
4. **Name accused persons** - System-level safety
5. **Diagnose mental conditions** - Not medical
6. **Decide punishments** - Legal role only

---

## Safety Mechanisms Built-In

### Safety 1: Age-Based Override
- Minor + sexual content → ALWAYS use POCSO framework
- No ambiguity, no manual judgment

### Safety 2: Authority Hierarchy
- Teacher threat > peer threat in severity routing
- Automatically flags institutional pathways

### Safety 3: Intersectionality Recognition
- Shows MULTIPLE categories when relevant
- Example: "Caste discrimination by teacher" → Shows both discrimination AND institutional misconduct

### Safety 4: Context Warnings
- "Age not provided" → Flag for manual verification
- "Institutional context detected" → Warn student of chain of command escalation

### Safety 5: Keyword Validation
- Cyber without online keywords → Rejected
- Violence without physical keywords → Rejected
- Prevents random/false classifications

---

## Why This Design is Defensible

✅ **Ethical**: Age-based rules protect minors automatically

✅ **Safe**: Rule-based filtering prevents bias creep

✅ **Transparent**: All rules are explicit, auditable

✅ **Scalable**: Works for intersectional situations

✅ **Legally Grounded**: References Indian law framework

✅ **Honest**: Clear what NLP does and doesn't do

---

## For Examiners/Stakeholders

### Question: "How do you prevent the AI from making wrong decisions?"
**Answer**: "We use a two-layer approach:
1. **NLP** identifies patterns and produces confidence scores
2. **Rules** apply context-aware filtering and human-designed decision logic
   
This means the AI never makes final legal decisions. It presents context + applicable frameworks. Humans (counselors, legal aid) make actual decisions."

### Question: "What about bias in the NLP model?"
**Answer**: "We've implemented:
1. Rule-based overrides for sensitive determinations (age, authority)
2. Keyword validation to prevent false positives
3. Multi-category output to avoid forcing single categorization
4. Transparent warning system for ambiguous cases

Additionally, the system errs on the side of caution—lower thresholds for protection (e.g., POCSO) and higher thresholds for accusations."

### Question: "How do you handle discrimination?"
**Answer**: "Discrimination is explicitly categorized and rule-checked:
- Caste/race/religion/gender keywords trigger specific frameworks
- When perpetrator is authority figure, institutional pathway also activated
- System recognizes intersectionality (multiple discrimination types shown together)
- All discrimination categories show applicable legal protections, not accusations"
