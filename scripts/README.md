# Helper Scripts

This directory contains utility scripts for dataset generation and maintenance.

## Scripts

### `generate_dataset.py`
Unified dataset generator containing comprehensive training examples for all 20 crime and legal support categories.
Run this script to regenerate `data/dataset.csv`:
```bash
python scripts/generate_dataset.py
```

## Categories Covered
- `physical_assault`
- `sexual_assault`
- `sexual_harassment`
- `ragging`
- `caste_discrimination`
- `religious_discrimination`
- `racial_discrimination`
- `gender_discrimination`
- `stalking`
- `threats`
- `blackmail_extortion`
- `cyber_bullying`
- `cyberstalking`
- `online_harassment`
- `impersonation_doxxing`
- `property_damage_theft`
- `domestic_violence`
- `child_abuse`
- `hate_speech`
- `academic_workplace_harassment`
