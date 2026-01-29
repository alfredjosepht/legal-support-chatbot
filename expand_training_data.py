#!/usr/bin/env python3
"""Expand training dataset with more sexual assault and comprehensive crime examples."""

import csv

# New sexual assault examples focusing on "touched" variations
new_sexual_assault_examples = [
    # Family member related
    "My uncle touched me inappropriately",
    "My uncle touched me badly",
    "My uncle has been touching me without permission",
    "My father touched me in a sexual way",
    "My cousin touched me at home",
    "A family member touched me inappropriately",
    "My uncle tried to touch me sexually",
    "Uncle touching me without consent",
    
    # Variations of "touched"
    "Someone touched me in a bad way",
    "I was touched inappropriately by someone",
    "A person touched me without my consent",
    "Someone touched my private parts",
    "I was touched against my will",
    "Someone grabbed and touched me",
    "I was touched intimately without permission",
    "A man touched me inappropriately",
    
    # Non-consensual contact
    "Someone touched me sexually without asking",
    "I didn't want to be touched that way",
    "Someone put their hands on me inappropriately",
    "I was touched while sleeping",
    "Someone groped me",
    "I was unwillingly touched by a stranger",
    "A person touched me in an uncomfortable way",
    "Someone touched me after I said no",
    
    # In different settings
    "A senior in hostel touched me",
    "My roommate touched me without consent",
    "Someone at a party touched me sexually",
    "A person at college touched me inappropriately",
    "In the classroom, someone touched me badly",
    "At work, my boss touched me inappropriately",
    "In a bus, someone touched me sexually",
    "Someone touched me in a public place",
    
    # More descriptive variations
    "I was sexually touched by a family member",
    "My uncle made unwanted sexual contact",
    "Someone I know sexually touched me",
    "I was touched in a sexual manner against my will",
    "Someone made non-consensual sexual contact with me",
    "I experienced unwanted sexual touching",
    "A person touched me sexually when I didn't want it",
    "I was touched inappropriately by my relative",
]

# Comprehensive crime examples for all categories
additional_examples = {
    "physical_assault": [
        "My uncle beat me",
        "My uncle hit me badly",
        "Someone beat me at home",
        "My family member attacked me",
    ],
    "verbal_abuse": [
        "My uncle insults me constantly",
        "My father uses abusive language",
        "I face daily verbal abuse from family",
    ],
    "sexual_harassment": [
        "My uncle makes inappropriate comments",
        "Someone makes sexual jokes to me",
        "I face unwanted sexual comments",
    ],
    "threats": [
        "My uncle threatened to hurt me",
        "Someone threatened to harm me",
        "I received death threats from a relative",
    ],
    "blackmail_extortion": [
        "My uncle is blackmailing me",
        "Someone is extorting money from me",
        "I'm being blackmailed with intimate photos",
    ],
    "cyber_sexual_crime": [
        "Someone sent me sexual messages online",
        "My intimate photos were shared without consent",
        "I'm being sexually harassed online",
    ],
}

# Read existing dataset
with open('/home/alfredjoseph/legal-support-chatbot/data/dataset.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

print(f"Original dataset: {len(rows)-1} rows")

# Prepare new rows
new_rows = []

# Add sexual assault examples
for example in new_sexual_assault_examples:
    new_rows.append([example, 'sexual_assault'])

# Add other category examples
for category, examples in additional_examples.items():
    for example in examples:
        new_rows.append([example, category])

print(f"Adding {len(new_rows)} new examples:")
print(f"  - {len(new_sexual_assault_examples)} sexual_assault examples")
print(f"  - {sum(len(v) for v in additional_examples.values())} other category examples")

# Append to dataset
with open('/home/alfredjoseph/legal-support-chatbot/data/dataset.csv', 'a', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    for row in new_rows:
        writer.writerow(row)

# Verify
with open('/home/alfredjoseph/legal-support-chatbot/data/dataset.csv', 'r', encoding='utf-8') as f:
    final_count = len(f.readlines()) - 1

print(f"\n✅ Updated dataset: {final_count} rows")
print(f"New total examples added: {final_count - (len(rows)-1)}")
