# NLP Module Handover – Student Legal Support System

## Owner
Alfred (NLP & Core Intelligence)

## Purpose
Identify possible legal issue categories from student problem descriptions.
Supports multiple issues in a single incident.

## Categories (13)
ragging  
threats  
cyber_harassment  
physical_assault  
sexual_harassment  
verbal_abuse  
stalking  
blackmail  
extortion  
discrimination  
defamation  
cheating_fraud  
privacy_violation  

## Model
- spaCy text classification (multi-label)
- Model path: backend/models/legal_textcat

## Output
- Uses `doc.cats`
- Multiple categories possible
- Confidence-based

## Threshold Rules
- physical_assault ≥ 0.20
- sexual_harassment ≥ 0.15
- cyber_harassment ≥ 0.18
- threats ≥ 0.20
- others ≥ 0.10

## Post-Processing
- Rule-based filtering in `nlp/postprocess.py`
- Removes logically impossible categories
- Prevents random crime suggestions

## Important Notes
- NLP DOES NOT decide IPC sections
- NLP DOES NOT decide guilt or punishment
- NLP only suggests possible issue types

