# NLP Module Handover – Student Legal Support System (V2)

## Owner
Alfred (NLP & Core Intelligence)

## System Definition
An NLP-based legal awareness system that addresses all major crimes, discrimination, and legal violations affecting students as recognized under Indian law, using context-aware classification and rule-based legal mapping.

## Key Principle
**The chatbot does not attempt to identify exact legal offences. Instead, it identifies the legal context using NLP and applies rule-based mappings to present relevant legal awareness.**

---

## Categories Structure

### Level 1: Broad Domains
1. **Physical Violence** - Assault, ragging, beating
2. **Sexual Offence** - Harassment, assault, coercion
3. **Cyber Offence** - Online harassment, threats, impersonation
4. **Discrimination & Hate** - Caste, race, religion, gender-based
5. **Ragging** - Dedicated category (also overlaps with violence/harassment)
6. **Threats & Intimidation** - Direct or implicit threats
7. **Institutional Misconduct** - Admin abuse, illegal bonds, certificate blocking
8. **Other Criminal/Civil** - Blackmail, extortion, defamation, cheating, stalking, privacy violation

### Level 2: Contextual Subclassification (Applied via Rules)
- **Age-based**: Minor (POCSO framework) vs Adult
- **Authority-based**: Teacher, administrator, senior student, peer
- **Identity-based**: Caste, race, religion, gender
- **Medium-based**: Offline, online (cyber), mixed
- **Location-based**: Campus, hostel, outside campus

---

## Updated Categories (19 Total)

### Discrimination & Identity Crimes (6)
- `caste_discrimination` - Caste-based slurs, exclusion, harassment
- `racism` - Racial slurs, ethnic discrimination, North-East targeting
- `religious_discrimination` - Faith-based harassment, forced practices
- `gender_discrimination` - Gender-based hostility, unequal treatment
- `sexual_harassment` - Unwanted advances, inappropriate comments, contact
- `general_discrimination` - Other protected characteristic discrimination

### Physical & Ragging (4)
- `physical_assault` - Beating, hitting, injury
- `ragging` - Ritualistic abuse, humiliation by seniors
- `threats` - Direct or implicit threats of violence
- `stalking` - Repeated following, surveillance, obsessive behavior

### Sexual Crimes (2)
- `sexual_assault` - Non-consensual contact, coercion
- `cyber_sexual_crime` - Sextortion, morphing, intimate content non-consent

### Cyber Crimes (3)
- `cyber_harassment` - Online abuse, hate messages
- `impersonation_doxxing` - Identity theft, personal info exposure
- `online_hate_speech` - Targeted online discrimination

### Institutional & Administrative (2)
- `institutional_misconduct` - Abuse of authority, illegal bonds, retaliation
- `administrative_violation` - Certificate blocking, forced undertakings

### Other Crimes (2)
- `blackmail_extortion` - Demands under threat
- `defamation_privacy_fraud` - False statements, privacy violation, cheating

---

## Threshold Rules (Category-Specific)

### High-Risk Categories
- `sexual_assault` (minor) ≥ 0.15 + age check
- `sexual_harassment` (adult) ≥ 0.18
- `physical_assault` ≥ 0.20
- `threats` ≥ 0.22
- `cyber_sexual_crime` ≥ 0.20

### Medium-Risk Categories
- `caste_discrimination` ≥ 0.15
- `racism` ≥ 0.15
- `religious_discrimination` ≥ 0.15
- `stalking` ≥ 0.18
- `institutional_misconduct` ≥ 0.12

### Standard Risk
- Others ≥ 0.10

---

## Age-Based Rules (Non-Negotiable)

**Critical Rule:**
```
If age < 18:
  - Any sexual content + contact + coercion → POCSO framework
  - Sexual harassment threshold lowered to ≥0.15
  - Output includes "minor protection" indicator

If age ≥ 18:
  - Adult sexual crime frameworks apply
  - Higher confidence thresholds
```

**How it works:**
1. Extract age from message (if mentioned)
2. If age ambiguous or not mentioned → flag for manual follow-up
3. Apply appropriate legal framework accordingly

---

## Post-Processing Rules

### Rule 1: Context Validation
- `cyber_harassment` REQUIRES online keywords (whatsapp, email, instagram, facebook, dm, message, online, etc.)
- `physical_assault` REQUIRES physical action words (hit, beaten, kicked, slapped, attacked, injured, etc.)
- `stalking` REQUIRES persistence/repetition keywords (follows, repeated, constant, everyday, etc.)

### Rule 2: Discrimination Context
- Discrimination detected + online medium → also flag cyber variant
- Discrimination detected + by teacher/admin → also flag institutional misconduct
- Multiple discriminations → show all (intersectionality)

### Rule 3: Authority-Based Override
- If accused is teacher/admin + violence/threat → upgrade to institutional misconduct
- If accused is senior student + ragging → confirm ragging classification
- If accused is peer → standard classification

### Rule 4: Institutional Checks
- Keywords (college, certificate, bond, hostel, management, administration) + violation → institutional_misconduct
- Threats + college context → institutional misconduct priority

### Rule 5: Dual Classification
- Cyber + Discrimination = Show both
- Physical + Ragging = Show both
- Do NOT oversimplify to single category

---

## Post-Processing Output Format

```json
{
  "primary_category": "caste_discrimination",
  "confidence": 0.78,
  "context": {
    "age_relevant": true,
    "age_indicator": "minor",
    "authority": "senior_student",
    "medium": "offline",
    "location": "hostel",
    "intersectional_flags": []
  },
  "matched_categories": [
    {"category": "caste_discrimination", "confidence": 0.78},
    {"category": "physical_assault", "confidence": 0.65},
    {"category": "institutional_misconduct", "confidence": 0.45}
  ],
  "safe_to_proceed": true,
  "flags": []
}
```

---

## Important Notes

✅ **NLP IDENTIFIES CONTEXT**
- Sexual content → age check required
- Discrimination keywords → identity framework
- Admin involvement → institutional pathway

❌ **NLP DOES NOT:**
- Decide exact IPC sections
- Declare guilt or punishment
- Make definitive accusations
- Judge severity

✅ **System ENSURES:**
- Age-appropriate responses
- Institutional accountability recognized
- Intersectionality considered
- Safe first steps provided

---

## Data Sources & Legal Frameworks

For each category, provide:
1. **Legal Frameworks**: IPC, POCSO, SC/ST Act, Constitution articles
2. **Safe First Steps**: What to do immediately
3. **Complaint Channels**: Police, campus, women's cell, legal aid
4. **Helplines**: Student counseling, legal support, emergency contacts
5. **Case References**: Real Indian case law examples
6. **Rights Information**: Constitutional/statutory protections

---

## Integration Points

1. **Frontend**: Captures age, location, authority info where possible
2. **Backend NLP**: Runs classification + rules
3. **Postprocessing**: Applies all contextual rules
4. **Response**: Multi-layered output for different stakeholder needs
