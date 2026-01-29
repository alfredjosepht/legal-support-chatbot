#!/usr/bin/env python3
"""Add final targeted examples for remaining edge cases."""

import csv

final_additions = {
    "threats": [
        "I am being threatened online",
        "someone threatens me online",
        "I receive threatening messages",
        "someone threatens my safety",
        "online threats are directed at me",
        "I receive threat messages",
        "someone threatens me",
        "threatening behavior online",
        "online threat messages",
    ],
    
    "impersonation_doxxing": [
        "someone impersonated me and shared harmful content",
        "my identity was misused online",
        "someone created fake account as me",
        "identity theft happened",
        "someone stole my online identity",
        "fake profile impersonating me",
        "my info was shared online without consent",
    ],
    
    "stalking": [
        "someone is stalking me",
        "I am being stalked",
        "stalking behavior is happening",
        "someone follows me constantly",
        "I am continuously followed",
        "persistent following is happening",
        "someone stalks me persistently",
        "stalking threat",
    ],
}

# Read existing
with open('/home/alfredjoseph/legal-support-chatbot/data/dataset.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.reader(f))

header = rows[0]
existing = rows[1:]

new_rows = []
for category, examples in final_additions.items():
    for ex in examples:
        new_rows.append([ex, category])

# Write
with open('/home/alfredjoseph/legal-support-chatbot/data/dataset.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(existing)
    writer.writerows(new_rows)

with open('/home/alfredjoseph/legal-support-chatbot/data/dataset.csv', 'r', encoding='utf-8') as f:
    final = len(f.readlines()) - 1

print(f"✅ Added {len(new_rows)} final examples")
print(f"Dataset now: {final} total examples")
