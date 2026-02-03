#!/usr/bin/env python3
"""
Enhanced Cyberbullying Dataset & Code Fixer
Adds comprehensive cyberbullying scenarios and improves detection logic
"""

import csv
import json
import re

# Comprehensive cyberbullying scenarios covering various mediums and behaviors
COMPREHENSIVE_CYBERBULLYING_SCENARIOS = [
    # Online social media bullying
    "Someone is harassing me constantly on social media platforms",
    "People spread hateful messages about me on online groups",
    "They created multiple fake accounts to bully me online",
    "A group of strangers are cyberbullying me continuously on messaging apps",
    "Someone hacked my online account and is impersonating me",
    
    # Cyber attacks and content abuse
    "They posted intimate photos of me without consent online",
    "My videos were shared on social media to humiliate me",
    "Someone screenshot my private conversation and posted it publicly",
    "They edited my photos and put them on the internet to mock me",
    "A video of me was uploaded online to shame me in front of everyone",
    
    # Online harassment and threats
    "I'm receiving abusive messages on social platforms every hour",
    "Someone is threatening me through online chat platforms",
    "A group chat was created specifically to target and bully me online",
    "They send me vulgar and threatening messages on messaging apps",
    "People are mass-following and commenting mean things on all my online posts",
    
    # Cyberstalking
    "Someone is tracking my online activities and monitoring my posts",
    "They follow all my social media movements and comment negatively",
    "A person is stalking me online and knows where I am",
    "Someone is constantly checking my online status and messaging me threats",
    "They're watching and recording my online activities without permission",
    
    # Reputation damage online
    "My reputation is being destroyed through online false accusations",
    "Someone started a hate campaign against me on social media",
    "They're spreading rumors about me on all online platforms",
    "A fake profile was created pretending to be me doing embarrassing things",
    "My name is being dragged online with false stories and accusations",
    
    # Online exclusion and targeted campaigns
    "I'm being excluded from all online communities and chat groups",
    "A group organized online to boycott and block me on social media",
    "They started an online petition against me to harm my reputation",
    "Someone created a hashtag to bully me online across all platforms",
    "Thousands of people joined an online hate campaign targeting me",
    
    # Cyber mobbing
    "An entire online community is cyberbullying me at once",
    "Multiple people coordinated online harassment against me",
    "I'm being cyber-mobbed by a group from my school on social platforms",
    "They organized an online attack on my social media profiles",
    "A large group is cyberbullying me in an organized manner online",
    
    # Cyber revenge and leaks
    "My personal information was leaked online by someone I trusted",
    "They posted my home address online to threaten me",
    "Someone shared my private messages online to embarrass me",
    "They leaked my photos online without my permission",
    "My personal details and secrets were exposed online publicly",
    
    # Platform-specific bullying
    "Instagram users are commenting cruel things on every post I make",
    "Facebook bullies created a group specifically to hurt me online",
    "TikTok users are making mean videos targeting me specifically",
    "Twitter is being used to cyberbully me with hateful posts",
    "WhatsApp group members are constantly bullying me in messages",
    
    # Gaming and online community harassment
    "Online gamers are cyberbullying me on gaming platforms",
    "I'm being harassed in online gaming communities",
    "Discord users are targeting and bullying me online",
    "Online forums are being used to mock and bully me",
    "Someone is spreading false rumors about me in online communities",
    
    # Cyber blackmail and coercion
    "Someone is cyber-blackmailing me with my online photos",
    "They threatened to post my private images online if I don't comply",
    "I'm being coerced through online threats and harassment",
    "Someone is using my online data to blackmail me",
    "They're threatening to expose my online activities if I don't do what they want",
    
    # Anonymous cyberbullying
    "I'm being bullied by anonymous accounts online",
    "Someone created anonymous profiles to bully me continuously",
    "Anonymous users are targeting me with hate messages online",
    "An unknown person is cyberbullying me from anonymous accounts",
    "I don't know who is bullying me but they're harassing me online constantly",
    
    # Workplace/professional cyberbullying online
    "My colleagues are cyberbullying me on work online platforms",
    "Someone is spreading workplace rumors about me on social media",
    "I'm being bullied by coworkers through online messaging",
    "My boss is cyberbullying me through email and online messages",
    "Professional peers are mocking me online on industry forums",
    
    # Educational cyberbullying
    "My classmates are cyberbullying me on social media platforms",
    "School friends created a group to bully me online",
    "I'm being bullied online by people from my college",
    "University students are cyberbullying me on online platforms",
    "Peers from school are targeting me with mean messages online",
]

# Keywords that should trigger cyber_bullying categorization
CYBER_RELATED_KEYWORDS = [
    "cyber", "online", "social media", "whatsapp", "facebook", "instagram", "twitter",
    "tiktok", "snapchat", "telegram", "discord", "email", "dm", "direct message",
    "message", "chat", "group chat", "posted", "post", "profile", "account",
    "hack", "hacked", "screenshot", "screenshotted", "screenshot", "video call",
    "video", "uploaded", "upload", "shared", "share", "shared publicly",
    "internet", "website", "forum", "online platform", "digital", "message app",
    "gaming", "game", "app", "application", "cyberbully", "cyberbullying"
]

def read_current_dataset(filepath):
    """Read current dataset and return all rows"""
    data = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        print(f"✓ Read {len(data)} records from dataset")
    except Exception as e:
        print(f"✗ Error reading dataset: {e}")
    return data

def enhance_dataset(data, new_scenarios):
    """Add new cyberbullying scenarios to dataset"""
    # Add new scenarios
    for scenario in new_scenarios:
        data.append({
            'text': scenario,
            'label': 'cyber_bullying'
        })
    
    print(f"✓ Added {len(new_scenarios)} new cyberbullying scenarios")
    print(f"✓ Total records now: {len(data)}")
    return data

def save_dataset(data, filepath):
    """Save enhanced dataset"""
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['text', 'label'])
            writer.writeheader()
            writer.writerows(data)
        print(f"✓ Saved {len(data)} records to {filepath}")
        return True
    except Exception as e:
        print(f"✗ Error saving dataset: {e}")
        return False

def enhance_postprocess_logic():
    """Enhance postprocess_v2.py with improved cyber keyword detection"""
    postprocess_file = '/home/alfredjoseph/legal-support-chatbot/nlp/postprocess_v2.py'
    
    try:
        with open(postprocess_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Expand CYBERBULLYING_KEYWORDS
        old_keywords = 'CYBERBULLYING_KEYWORDS = ["bullying", "bully", "bullied", "mock", "mocking", "mocked", "taunt", "taunting",\n                          "insult", "insulting", "insulted", "humiliate", "humiliation", "humiliating",\n                          "shame", "shaming", "shamed", "embarrass", "embarrassing", "embarrassed",\n                          "ridicule", "ridiculing", "ridiculous", "tease", "teasing", "teased",\n                          "spread rumors", "rumour", "spreading lies", "fake account", "fake profile",\n                          "mass tagging", "meme", "edited photo", "private messages exposed", "viral",\n                          "exclude", "excluding", "excluded", "group exclusion", "mean messages", "mean comments",\n                          "abusive messages", "abusive comments", "cruel", "cruelty", "nasty", "vicious"]'
        
        new_keywords = '''CYBERBULLYING_KEYWORDS = ["bullying", "bully", "bullied", "mock", "mocking", "mocked", "taunt", "taunting",
                          "insult", "insulting", "insulted", "humiliate", "humiliation", "humiliating",
                          "shame", "shaming", "shamed", "embarrass", "embarrassing", "embarrassed",
                          "ridicule", "ridiculing", "ridiculous", "tease", "teasing", "teased",
                          "spread rumors", "rumour", "spreading lies", "fake account", "fake profile",
                          "mass tagging", "meme", "edited photo", "private messages exposed", "viral",
                          "exclude", "excluding", "excluded", "group exclusion", "mean messages", "mean comments",
                          "abusive messages", "abusive comments", "cruel", "cruelty", "nasty", "vicious",
                          "cyber", "cyberbully", "cyberbullying", "cyberbullied", "harass", "harassment",
                          "stalk", "stalking", "threatening", "blackmail", "coerce", "coercion",
                          "revenge porn", "intimate images", "leaked photos", "leaked videos", "leaked messages",
                          "doxing", "doxx", "personal information", "leak", "leaked", "exposed"]'''
        
        if old_keywords in content:
            content = content.replace(old_keywords, new_keywords)
            print("✓ Enhanced CYBERBULLYING_KEYWORDS in postprocess_v2.py")
        else:
            print("⚠ Could not find exact keywords pattern to replace")
        
        # Enhance ONLINE_KEYWORDS to include more cyber indicators
        old_online = 'ONLINE_KEYWORDS = ["online", "whatsapp", "instagram", "facebook", "message", "dm", "email", \n                   "twitter", "telegram", "snapchat", "tiktok", "video call", "phone call",\n                   "chat", "text", "posted", "shared", "screenshot", "website", "forum",\n                   "comment", "post", "profile", "account"]'
        
        new_online = '''ONLINE_KEYWORDS = ["online", "whatsapp", "instagram", "facebook", "message", "dm", "email", 
                   "twitter", "telegram", "snapchat", "tiktok", "video call", "phone call",
                   "chat", "text", "posted", "shared", "screenshot", "website", "forum",
                   "comment", "post", "profile", "account", "cyber", "cyberbully", "social media",
                   "app", "application", "discord", "gaming", "game", "hack", "hacked",
                   "upload", "uploaded", "video", "photo", "image", "internet"]'''
        
        if old_online in content:
            content = content.replace(old_online, new_online)
            print("✓ Enhanced ONLINE_KEYWORDS in postprocess_v2.py")
        else:
            print("⚠ Could not find exact ONLINE_KEYWORDS pattern to replace")
        
        # Update cyberbullying validation logic to be more aggressive
        # Find and replace the cyberbullying validation section
        old_cyber_rule = '''    if 'cyber_bullying' in raw_cats:
        # Explicit cyberbullying term ("cyberbullying", "cyberbullied", "cyberbully")
        # OR online medium + bullying keywords
        has_explicit_cyber = any(term in text_lower for term in ['cyberbullying', 'cyberbullied', 'cyberbully'])
        has_online_context = medium in ['online', 'mixed'] or any(kw in text_lower for kw in ONLINE_KEYWORDS)
        has_bullying_keywords = any(kw in text_lower for kw in CYBERBULLYING_KEYWORDS)
        
        if has_explicit_cyber or (has_online_context and has_bullying_keywords):
            # Boost cyberbullying confidence when keywords are present
            boosted_cyber = max(raw_cats.get('cyber_bullying', 0), 0.15)
            final_cats['cyber_bullying'] = boosted_cyber
            
            # When cyberbullying is clearly detected, suppress sexual crime false positives
            # (low-confidence sexual assault/harassment are often misclassifications)
            if raw_cats.get('sexual_assault', 0) < 0.30:
                raw_cats['sexual_assault'] = 0  # Suppress
            if raw_cats.get('sexual_harassment', 0) < 0.30:
                raw_cats['sexual_harassment'] = 0  # Suppress'''
        
        new_cyber_rule = '''    if 'cyber_bullying' in raw_cats:
        # Explicit cyberbullying term ("cyberbullying", "cyberbullied", "cyberbully")
        # OR online medium + bullying keywords
        # OR any cyber/online keyword present with bullying keywords
        has_explicit_cyber = any(term in text_lower for term in ['cyberbullying', 'cyberbullied', 'cyberbully'])
        has_online_context = medium in ['online', 'mixed'] or any(kw in text_lower for kw in ONLINE_KEYWORDS)
        has_bullying_keywords = any(kw in text_lower for kw in CYBERBULLYING_KEYWORDS)
        has_cyber_keywords = any(kw in text_lower for kw in ['cyber', 'online', 'social media', 'whatsapp', 'facebook', 'instagram'])
        
        # Trigger cyberbullying if:
        # 1. Explicit cyber term OR
        # 2. (Online context AND bullying keywords) OR
        # 3. (Cyber keywords AND bullying keywords)
        if has_explicit_cyber or (has_online_context and has_bullying_keywords) or (has_cyber_keywords and has_bullying_keywords):
            # Boost cyberbullying confidence when keywords are present
            # Higher boost if cyber keywords are explicitly present
            if has_cyber_keywords:
                boosted_cyber = max(raw_cats.get('cyber_bullying', 0), 0.20)  # Higher boost for cyber keywords
            else:
                boosted_cyber = max(raw_cats.get('cyber_bullying', 0), 0.15)
            
            final_cats['cyber_bullying'] = boosted_cyber
            
            # When cyberbullying is clearly detected, suppress sexual crime false positives
            # (low-confidence sexual assault/harassment are often misclassifications)
            if raw_cats.get('sexual_assault', 0) < 0.30:
                raw_cats['sexual_assault'] = 0  # Suppress
            if raw_cats.get('sexual_harassment', 0) < 0.30:
                raw_cats['sexual_harassment'] = 0  # Suppress'''
        
        if old_cyber_rule in content:
            content = content.replace(old_cyber_rule, new_cyber_rule)
            print("✓ Enhanced cyberbullying validation rule in postprocess_v2.py")
        else:
            print("⚠ Could not find exact cyberbullying validation rule to replace")
        
        # Save updated content
        with open(postprocess_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✓ Saved enhanced postprocess_v2.py")
        return True
    
    except Exception as e:
        print(f"✗ Error enhancing postprocess logic: {e}")
        return False

def main():
    print("=" * 60)
    print("ENHANCED CYBERBULLYING DATASET & CODE FIXER")
    print("=" * 60)
    
    dataset_path = '/home/alfredjoseph/legal-support-chatbot/data/dataset.csv'
    
    # Step 1: Read current dataset
    print("\n[1] Reading current dataset...")
    data = read_current_dataset(dataset_path)
    
    if not data:
        print("Error: Could not read dataset")
        return False
    
    # Step 2: Add new cyberbullying scenarios
    print("\n[2] Adding comprehensive cyberbullying scenarios...")
    data = enhance_dataset(data, COMPREHENSIVE_CYBERBULLYING_SCENARIOS)
    
    # Step 3: Save enhanced dataset
    print("\n[3] Saving enhanced dataset...")
    if not save_dataset(data, dataset_path):
        return False
    
    # Step 4: Enhance postprocess logic
    print("\n[4] Enhancing postprocess_v2.py with improved cyber keyword detection...")
    if not enhance_postprocess_logic():
        return False
    
    print("\n" + "=" * 60)
    print("✓ ENHANCEMENT COMPLETE!")
    print("=" * 60)
    print(f"\nSummary:")
    print(f"  • Added {len(COMPREHENSIVE_CYBERBULLYING_SCENARIOS)} new cyberbullying scenarios")
    print(f"  • Enhanced keyword detection for cyber, online, and social media terms")
    print(f"  • Updated validation rules to catch more cyberbullying cases")
    print(f"  • Total dataset size: {len(data)} records")
    print(f"\nNext steps:")
    print(f"  1. Retrain the model: python nlp/train_classifier.py")
    print(f"  2. Test the system: python -c 'from nlp.postprocess_v2 import ...'")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
