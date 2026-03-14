# analyzer/policy_sources.py

# 🔹 Main App Privacy URLs
# Grouped into categories for easier maintenance
APP_PRIVACY_URLS = {
    # Social Media & Communication
    "whatsapp": "https://www.whatsapp.com/legal/privacy-policy",
    "instagram": "https://privacycenter.instagram.com/policy/",
    "facebook": "https://www.facebook.com/policy.php",
    "twitter": "https://twitter.com/en/privacy", 
    "snapchat": "https://snap.com/en-US/privacy/privacy-policy",
    "tiktok": "https://www.tiktok.com/legal/privacy-policy?lang=en",
    "linkedin": "https://www.linkedin.com/legal/privacy-policy",
    "telegram": "https://telegram.org/privacy",
    "discord": "https://discord.com/privacy",
    "reddit": "https://www.redditinc.com/policies/privacy-policy",
    "pinterest": "https://policy.pinterest.com/en/privacy-policy",
    "clubhouse": "https://www.clubhouse.com/privacy",
    "kik": "https://www.kik.com/privacy-policy/",
    "quora": "https://www.quora.com/about/privacy",
    
    # Tech Giants & Search
    "google": "https://policies.google.com/privacy",
    "gmail": "https://policies.google.com/privacy",
    "youtube": "https://policies.google.com/privacy",
    "apple": "https://www.apple.com/legal/privacy/en-ww/",
    "microsoft": "https://privacy.microsoft.com/en-us/privacystatement",

    # Work & Productivity
    "zoom": "https://explore.zoom.us/en/privacy/",
    "microsoft teams": "https://privacy.microsoft.com/en-us/privacystatement",
    "skype": "https://privacy.microsoft.com/en-us/privacystatement",
    "slack": "https://slack.com/trust/privacy/privacy-policy",
    "github": "https://docs.github.com/en/site-policy/privacy-policies/github-privacy-statement",

    # Entertainment & Streaming
    "spotify": "https://www.spotify.com/legal/privacy-policy/",
    "netflix": "https://help.netflix.com/legal/privacy",

    # AI & Emerging Tech
    "chatgpt": "https://openai.com/policies/privacy-policy",

    # E-commerce, Delivery & Utility
    "amazon": "https://www.amazon.com/gp/help/customer/display.html?nodeId=GX7NJQ4ZB8MHFRNJ",
    "uber": "https://www.uber.com/legal/en/document/?name=privacy-notice",
    "zomato": "https://www.zomato.com/privacy",
    "swiggy": "https://www.swiggy.com/privacy-policy",
    "flipkart": "https://www.flipkart.com/pages/privacypolicy"
}

# 🔹 Aliases / Common names
APP_NAME_ALIASES = {
    # TikTok
    "tik tok": "tiktok",
    "tiktok app": "tiktok",
    "tiktok lite": "tiktok",

    # Meta Family
    "insta": "instagram",
    "ig": "instagram",
    "instagram app": "instagram",
    "fb": "facebook",
    "facebook app": "facebook",
    "meta": "facebook",
    "wa": "whatsapp",

    # X / Twitter
    "x": "twitter",
    "twitter x": "twitter",
    "twitter app": "twitter",

    # Google Family
    "gm": "gmail",
    "google mail": "gmail",
    "yt": "youtube",
    "youtube app": "youtube",
    "chrome": "google",
    "google search": "google",

    # Social & Chat
    "snap": "snapchat",
    "snap chat": "snapchat",
    "tg": "telegram",
    "telegram app": "telegram",
    "dc": "discord",
    "discord app": "discord",
    "rd": "reddit",
    "reddit app": "reddit",
    "pin": "pinterest",
    "pinterest app": "pinterest",
    "club house": "clubhouse",
    "clubhouse app": "clubhouse",
    "kik app": "kik",
    "quora app": "quora",

    # Professional
    "linkedin app": "linkedin",
    "teams": "microsoft teams",
    "microsoft teams app": "microsoft teams",
    "skype app": "skype",

    # Entertainment
    "sp": "spotify",
    "spotify app": "spotify",
    "netflix app": "netflix",

    # AI
    "chat gpt": "chatgpt",
    "openai": "chatgpt",

    # Commerce & Utilities
    "amazon shopping": "amazon",
    "amazon prime": "amazon",
    "uber app": "uber",
    "zomato app": "zomato",
    "swiggy app": "swiggy",
    "flipkart app": "flipkart"
}