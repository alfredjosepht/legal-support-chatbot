def postprocess_categories(text, raw_cats):
    text_lower = text.lower()

    final_cats = {}

    # Keyword groups
    online_keywords = ["online", "whatsapp", "instagram", "facebook", "message", "dm", "email"]
    physical_keywords = ["hit", "beaten", "assault", "injured", "kicked", "slapped", "attacked"]
    college_keywords = ["college", "management", "administration", "files", "certificate", "documents"]

    for label, score in raw_cats.items():

        # --------- HARD FILTERS ---------

        # Remove cyber_harassment if no online context
        if label == "cyber_harassment":
            if not any(word in text_lower for word in online_keywords):
                continue

        # Remove physical_assault if no physical action words
        if label == "physical_assault":
            if not any(word in text_lower for word in physical_keywords):
                continue
            if score < 0.20:
                continue

        # Remove sexual_harassment if no sexual indicators
        if label == "sexual_harassment" and score < 0.15:
            continue

        # Institutional coercion → extortion only
        if any(word in text_lower for word in college_keywords):
            if label == "cyber_harassment":
                continue

        # --------- THRESHOLDS ---------

        if label == "threats" and score < 0.20:
            continue

        if label == "cyber_harassment" and score < 0.18:
            continue

        if score < 0.10:
            continue

        final_cats[label] = score

    return dict(sorted(final_cats.items(), key=lambda x: x[1], reverse=True))

