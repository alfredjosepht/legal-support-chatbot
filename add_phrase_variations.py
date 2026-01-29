#!/usr/bin/env python3
"""Add more phrase variations to improve classification for all categories."""

import csv

# Additional targeted examples with phrase variations
additional_variations = {
    "blackmail_extortion": [
        "someone is blackmailing me with photos",
        "I'm being blackmailed with photos",
        "someone blackmails me with pictures",
        "they are blackmailing me with images",
        "someone threatens to share photos unless I pay",
        "I'm forced to pay or they'll share my photos",
        "someone is extorting money from me with photos",
    ],
    
    "impersonation_doxxing": [
        "someone impersonated me and shared harmful content",
        "my identity was stolen and misused",
        "someone created a fake account pretending to be me",
        "someone is impersonating me online",
        "my personal information was leaked online",
        "someone doxxed me on social media",
        "my address and phone were shared without permission",
        "someone shared my personal details online",
        "my identity is being used to harm me",
    ],
    
    "gender_discrimination": [
        "I am facing gender discrimination",
        "I am discriminated against for my gender",
        "my gender determines how people treat me",
        "I face gender-based treatment",
        "I am denied opportunities because of my gender",
        "people stereotype me based on gender",
        "I am treated unfairly because of my gender",
        "my gender affects my opportunities",
        "gender discrimination affects me",
    ],
    
    "stalking": [
        "someone is stalking me",
        "I am being stalked",
        "someone follows me everywhere",
        "I feel stalked and unsafe",
        "someone watches me constantly",
        "I am being followed persistently",
        "someone is obsessively following me",
        "I am stalked online and offline",
        "someone monitors my movements",
    ],
    
    "threats": [
        "I am being threatened online",
        "someone threatens me online",
        "I receive threatening messages",
        "someone threatens my safety",
        "I am threatened if I report them",
        "threatening messages are sent to me",
        "I face online threats",
    ],
    
    "online_hate_speech": [
        "I receive hate speech online",
        "hateful comments target me",
        "I am attacked with hate speech",
        "hate messages are sent to me",
        "I face online hate",
        "someone posts hateful content about me",
        "hate-filled comments target me",
    ],
}

# Read existing dataset
with open('/home/alfredjoseph/legal-support-chatbot/data/dataset.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.reader(f))

header = rows[0]
existing_rows = rows[1:]

print(f"Starting with {len(existing_rows)} examples")

# Prepare new rows
new_rows = []
for category, examples in additional_variations.items():
    for example in examples:
        new_rows.append([example, category])

print(f"Adding {len(new_rows)} targeted phrase variations")

# Write updated dataset
with open('/home/alfredjoseph/legal-support-chatbot/data/dataset.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(existing_rows)
    writer.writerows(new_rows)

# Verify
with open('/home/alfredjoseph/legal-support-chatbot/data/dataset.csv', 'r', encoding='utf-8') as f:
    final_count = len(f.readlines()) - 1

print(f"✅ Updated dataset: {final_count} total examples")
print(f"New total: {len(existing_rows) + len(new_rows)} = {final_count}")
