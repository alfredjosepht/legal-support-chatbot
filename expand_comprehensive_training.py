#!/usr/bin/env python3
"""Dramatically expand training dataset with comprehensive crime examples."""

import csv

comprehensive_examples = {
    "sexual_assault": [
        # Family members
        "My uncle touched me inappropriately",
        "My uncle touched me badly",
        "My father touched me in a sexual way",
        "My cousin assaulted me",
        "A family member forced sexual contact",
        "My stepfather sexually abused me",
        "My brother touched me without consent",
        "My relative tried to rape me",
        
        # Authority figures
        "My teacher sexually assaulted me",
        "My principal touched me inappropriately",
        "My coach forced me to do sexual acts",
        "My instructor sexually abused me",
        "A senior at college assaulted me",
        
        # Forced/non-consensual
        "Someone forced me into sexual activity",
        "I was sexually assaulted against my will",
        "Someone raped me at a party",
        "I was forced to have sex",
        "Someone penetrated me without consent",
        "I was coerced into sexual contact",
        "Someone forced their body on me sexually",
        
        # Variations
        "I was sexually attacked",
        "Someone sexually violated me",
        "I experienced sexual violence",
        "I was molested",
    ],
    
    "sexual_harassment": [
        "My teacher makes sexual comments about me",
        "My professor makes inappropriate sexual remarks",
        "A senior makes sexual jokes directed at me",
        "Someone keeps making unwanted sexual advances",
        "My colleague makes sexual comments to me",
        "A person at work sexually harasses me",
        "Someone sends me sexual messages at college",
        "I receive unwanted sexual comments online",
        "A senior constantly makes sexual remarks",
        "My classmate makes sexual jokes about my body",
        "Someone whistles and makes sexual comments",
        "I am sexually objectified by someone",
        "A person touches me inappropriately on the shoulder",
        "Someone keeps asking me for sexual favors",
        "I face sexual comments and staring",
    ],
    
    "physical_assault": [
        "My senior punched me in the face",
        "A student hit me with a stick",
        "Someone beat me up",
        "I was physically attacked",
        "My peer pushed me against the wall",
        "Someone threw something at me and hurt me",
        "A group of students beat me",
        "My classmate kicked me",
        "Someone stabbed me with a knife",
        "I was slapped and hit",
        "Someone punched me multiple times",
        "A person attacked me physically",
        "I got into a physical fight and got hurt",
        "Someone threw me down the stairs",
        "My senior violently attacked me",
    ],
    
    "ragging": [
        "Seniors ragged me brutally",
        "I was ragged severely in the hostel",
        "Seniors forced me to do humiliating things",
        "I was subjected to extreme ragging",
        "Seniors made me perform degrading acts",
        "I was verbally and physically ragged",
        "Seniors forced me to drink and party excessively",
        "I was ragged as part of a group",
        "Seniors ragged me relentlessly",
        "I was forced to participate in ragging activities",
        "Seniors humiliated me through ragging",
        "I was ragged despite asking them to stop",
        "Seniors created an intimidating atmosphere",
        "I experienced traumatic ragging",
    ],
    
    "caste_discrimination": [
        "I face discrimination because of my caste",
        "People treat me differently due to my caste",
        "I am discriminated against based on my caste",
        "My caste determines how people treat me",
        "I face casteist remarks and behavior",
        "My classmates exclude me because of my caste",
        "I am denied opportunities due to my caste",
        "Someone made casteist comments to me",
        "I face social discrimination for my caste",
        "My caste background causes discrimination",
        "People use my caste against me",
        "I am isolated because of my caste",
    ],
    
    "gender_discrimination": [
        "I face discrimination because of my gender",
        "I am treated unfairly because I am a girl",
        "I am treated unfairly because I am a boy",
        "My gender is used against me",
        "I face gender-based discrimination",
        "I am denied opportunities due to my gender",
        "People stereotype me based on my gender",
        "I face sexist comments and behavior",
        "My gender affects how people treat me",
        "I face discrimination for being transgender",
    ],
    
    "threats": [
        "Someone threatened to hurt me",
        "I received death threats from a senior",
        "Someone threatened to kill me",
        "I was threatened with violence",
        "Someone threatened my safety",
        "I received threatening messages",
        "Someone threatened to harm my family",
        "I am being threatened online",
        "Someone threatened to expose my secrets",
        "I received threatening calls",
        "Someone threatened to damage my reputation",
        "I am threatened if I report them",
    ],
    
    "cyber_harassment": [
        "Someone is harassing me on social media",
        "I receive harassing messages online",
        "Someone cyberbullies me constantly",
        "I am harassed through online platforms",
        "Someone posts mean comments about me",
        "I receive abusive messages online",
        "Someone creates fake accounts to harass me",
        "I am trolled and harassed online",
        "Someone shares my personal information to harass me",
        "I face cyberbullying on Instagram/Facebook",
    ],
    
    "blackmail_extortion": [
        "Someone is blackmailing me",
        "I am being extorted for money",
        "Someone blackmails me with intimate photos",
        "Someone is demanding money and threatening me",
        "I am blackmailed and threatened",
        "Someone extorts money from me threateningly",
        "I am blackmailed with evidence of something",
        "Someone blackmails me to keep secrets",
        "I am being blackmailed and cannot go to police",
        "Someone threatens to share private photos if I don't pay",
    ],
    
    "impersonation_doxxing": [
        "Someone impersonated me on social media",
        "My identity was stolen online",
        "Someone created a fake account in my name",
        "Someone spread my personal information",
        "My private information was leaked online",
        "Someone shared my address and phone number",
        "I was doxxed on social media",
        "Someone impersonates me to harass others",
        "My personal details were made public without consent",
        "Someone created a fake profile pretending to be me",
    ],
    
    "cyber_sexual_crime": [
        "Someone sent me sexual messages online",
        "My intimate photos were shared without consent",
        "Someone is blackmailing me with intimate photos",
        "I am being sexually exploited online",
        "Someone sent me unwanted sexual content",
        "My naked photos were leaked",
        "Someone solicits sexual content from me online",
        "I am being groomed online",
        "Someone made sexual deepfakes of me",
        "My intimate video was shared without permission",
    ],
    
    "racism": [
        "I face racism based on my ethnicity",
        "People treat me differently due to my race",
        "I am discriminated against because of my race",
        "Racist comments are made about me",
        "I am excluded due to my race",
        "People use racist slurs against me",
        "I face racial discrimination",
        "My race determines how people treat me",
        "I am stereotyped based on my race",
        "Racist behavior is directed at me",
    ],
    
    "religious_discrimination": [
        "I face discrimination because of my religion",
        "People treat me unfairly due to my faith",
        "I am discriminated against for my religious beliefs",
        "Disrespectful comments are made about my religion",
        "I am excluded from activities due to my religion",
        "My religious beliefs are mocked",
        "I face religious discrimination",
        "People target me for my faith",
        "My religion is used against me",
        "I face prejudice based on my religion",
    ],
    
    "verbal_abuse": [
        "My senior insults me constantly",
        "I am verbally abused by a peer",
        "Someone uses abusive language towards me",
        "I receive verbal abuse from family",
        "Someone criticizes me harshly",
        "I am yelled at and verbally attacked",
        "Someone uses derogatory terms for me",
        "I face constant verbal aggression",
        "Someone belittles me verbally",
        "I am insulted and degraded verbally",
    ],
    
    "online_hate_speech": [
        "I receive hate speech online",
        "Hateful comments are directed at me",
        "I am targeted with hate speech",
        "Offensive hate speech is posted about me",
        "I receive messages containing hate speech",
        "Someone uses hateful slurs against me online",
        "I face hate-based comments online",
        "Someone spreads hate speech about my community",
        "I receive threatening hate messages",
    ],
    
    "institutional_misconduct": [
        "The college is denying my basic rights",
        "The institution is acting unfairly towards me",
        "College authorities are abusing their power",
        "Institutional negligence caused me harm",
        "The college failed to protect me",
        "Institutional policies are discriminatory",
        "College management is corrupt",
        "I am unfairly punished by the institution",
        "Institutional authorities are biased against me",
    ],
    
    "defamation_privacy_fraud": [
        "Someone is spreading false rumors about me",
        "My reputation is being damaged with lies",
        "Someone defames me publicly",
        "My private information is being shared",
        "Someone defrauded me",
        "False information about me is spread",
        "My privacy is violated",
        "Someone makes false accusations against me",
        "My personal details are misused",
    ],
    
    "stalking": [
        "Someone is following me everywhere",
        "I am being stalked by a person",
        "Someone is watching me constantly",
        "I feel stalked and unsafe",
        "Someone follows me persistently",
        "I am stalked at college/home",
        "Someone monitors my movements",
        "I am being obsessively followed",
        "Someone stalks me online and offline",
    ],
    
    "administrative_violation": [
        "College violated my rights",
        "Administrative procedures are unfair",
        "I faced unfair administrative action",
        "Administrative negligence occurred",
        "I was unfairly suspended",
        "Administrative staff discriminated against me",
        "Incorrect administrative action was taken",
        "I was denied my administrative rights",
    ],
    
    "general_discrimination": [
        "I face general discrimination",
        "I am treated unfairly",
        "Discrimination is happening to me",
        "I am discriminated against",
        "I experience prejudicial treatment",
        "I am denied equal treatment",
        "Discrimination affects my opportunities",
    ],
}

# Read existing dataset
with open('/home/alfredjoseph/legal-support-chatbot/data/dataset.csv', 'r', encoding='utf-8') as f:
    existing_rows = list(csv.reader(f))[1:]  # Skip header

print(f"Starting with {len(existing_rows)} examples")

# Count existing examples per category
category_counts = {}
for row in existing_rows:
    if len(row) >= 2:
        category = row[1]
        category_counts[category] = category_counts.get(category, 0) + 1

print("Current distribution:")
for cat in sorted(category_counts.keys()):
    print(f"  {cat}: {category_counts[cat]}")

# Add comprehensive examples
new_rows = []
for category, examples in comprehensive_examples.items():
    for example in examples:
        new_rows.append([example, category])

print(f"\nAdding {len(new_rows)} new examples")

# Write new dataset
with open('/home/alfredjoseph/legal-support-chatbot/data/dataset.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['text', 'label'])
    writer.writerows(existing_rows)
    writer.writerows(new_rows)

# Verify
with open('/home/alfredjoseph/legal-support-chatbot/data/dataset.csv', 'r', encoding='utf-8') as f:
    final_count = len(f.readlines()) - 1

print(f"\n✅ Updated dataset: {final_count} total examples")

# New distribution
new_category_counts = {}
for row in existing_rows + new_rows:
    if len(row) >= 2:
        category = row[1]
        new_category_counts[category] = new_category_counts.get(category, 0) + 1

print("\nNew distribution:")
for cat in sorted(new_category_counts.keys()):
    old = category_counts.get(cat, 0)
    new = new_category_counts[cat]
    print(f"  {cat}: {old} → {new} (+{new-old})")
