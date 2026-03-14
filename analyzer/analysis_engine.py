# analyzer/analysis_engine.py

import re
from textblob import TextBlob
from .risk_keywords import RISK_KEYWORDS

def analyze_policy(text: str) -> dict:
    """
    Analyzes privacy policy text using NLP sentiment analysis and weighted keyword 
    matching to return comprehensive risk and safety scores, along with context snippets.
    """
    if not text:
        return {
            "sentiment": 0.0,
            "consent_risk_score": 0,
            "safety_score": 5.0,
            "categories": {}
        }

    text_lower = text.lower()

    # 1. Sentiment Analysis (-1.0 to 1.0)
    # Most legal texts are neutral, but negative polarity can indicate aggressive data practices
    sentiment = round(TextBlob(text).sentiment.polarity, 3)

    # 2. Keyword Detection & Snippet Extraction
    detected_categories = {}
    raw_risk_score = 0
    max_possible_risk = sum(item["score"] for item in RISK_KEYWORDS.values())

    for category, data in RISK_KEYWORDS.items():
        for kw in data["keywords"]:
            # Check if any keyword/phrase for this category exists in the text
            index = text_lower.find(kw)
            if index != -1:
                # 1. Grab a slightly larger raw window
                start = max(0, index - 70)
                end = min(len(text), index + len(kw) + 150)
                raw_snippet = text[start:end]
                
                # 2. Split into a list of words to clean up spaces
                words = raw_snippet.split()
                
                # 3. Drop the first and last items because they are likely cut-in-half words!
                if start > 0 and len(words) > 1:
                    words = words[1:]  # Drop the first word fragment
                if end < len(text) and len(words) > 1:
                    words = words[:-1] # Drop the last word fragment
                    
                # 4. Rejoin into a clean, complete-word sentence
                clean_snippet = " ".join(words)
                
                # 5. Clean up Markdown artifacts (Jina AI leaves links and bold/header tags)
                # Removes Markdown links: [Click Here](https://...) -> Click Here
                clean_snippet = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean_snippet)
                
                # Removes incomplete links that got cut off at the end of the snippet
                clean_snippet = re.sub(r'\[([^\]]+)\]\([^\)]*$', r'\1', clean_snippet)
                
                # NEW: Removes leftover raw URLs or URLs inside parentheses: (https://...)
                clean_snippet = re.sub(r'\(?https?://[^\s\)]+\)?', '', clean_snippet)
                
                # Removes Markdown formatting symbols: *, #, _, `, and hanging brackets [ ]
                clean_snippet = re.sub(r'[*#_`\[\]]', '', clean_snippet)
                
                # Clean up any double spaces created by removing symbols
                clean_snippet = " ".join(clean_snippet.split())
                
                # Save the beautifully formatted text snippet
                detected_categories[category] = clean_snippet
                raw_risk_score += data["score"]
                break  # Move to the next category once a match is found

    # 3. Calculate Consent Risk Score (0-100 Scale)
    # Scaled based on the total possible risk weight
    consent_risk_score = 0
    if max_possible_risk > 0:
        consent_risk_score = round((raw_risk_score / max_possible_risk) * 100)
    
    # Clamp between 0 and 100 just to be safe
    consent_risk_score = max(0, min(consent_risk_score, 100))

    # 4. Calculate Safety Score (1.0 to 5.0 Stars)
    # Base safety is inversely proportional to risk (0 risk = 5 stars, 100 risk = 1 star)
    base_safety = 5.0 - ((consent_risk_score / 100) * 4.0)

    # Adjust slightly based on sentiment (penalize aggressive legal language)
    if sentiment < 0:
        base_safety += (sentiment * 0.5)  # e.g., -0.2 sentiment removes 0.1 stars

    safety_score = round(max(1.0, min(base_safety, 5.0)), 1)

    return {
        "sentiment": sentiment,
        "consent_risk_score": consent_risk_score,
        "safety_score": safety_score,
        "categories": detected_categories
    }