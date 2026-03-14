# analyzer/risk_keywords.py

# 🔹 Risk Keywords and Scoring for Privacy Analysis
# Scores are based on a 1-5 severity scale:
# 1-2: Standard app permissions (low-medium risk)
# 3: Sensitive personal data (medium-high risk)
# 4-5: Critical privacy invasions & data selling (high-critical risk)

RISK_KEYWORDS = {
    "Location Tracking": {
        "keywords": [
            "location", "gps", "geolocation", "real-time location",
            "background location", "precise location", "coarse location",
            "ip address", "location tracking", "location history"
        ],
        "score": 3
    },
    "Camera & Media": {
        "keywords": [
            "camera", "photos", "videos", "image capture",
            "photo gallery", "camera roll", "media files"
        ],
        "score": 2
    },
    "Microphone & Audio": {
        "keywords": [
            "microphone", "audio recording", "voice data",
            "voice recordings", "listen", "audio capture"
        ],
        "score": 2
    },
    "Contacts & Social Graph": {
        "keywords": [
            "contacts", "address book", "phonebook",
            "connections", "friend list", "social graph",
            "call logs", "sms history"
        ],
        "score": 3
    },
    "Financial Data": {
        "keywords": [
            "credit card", "debit card", "bank account",
            "billing", "payment information", "transaction history",
            "financial info", "payment details", "wallet"
        ],
        "score": 4
    },
    "Biometric & Health Data": {
        "keywords": [
            "biometric", "facial recognition", "fingerprint",
            "voiceprint", "face data", "retina", "health", 
            "medical", "fitness data", "heart rate", "sleep data"
        ],
        "score": 5
    },
    "Private Communications": {
        "keywords": [
            "messages", "chats", "email content",
            "private communications", "direct messages", "inbox",
            "message content", "read emails"
        ],
        "score": 5
    },
    "Browsing & Device Tracking": {
        "keywords": [
            "browsing history", "search history", "web activity",
            "device identifier", "advertising id", "cookies",
            "pixels", "web beacons", "cross-device tracking", 
            "mac address", "imei", "profiling"
        ],
        "score": 3
    },
    "Third Party Sharing & Selling": {
        "keywords": [
            "third party", "share data", "sell data", "sold to",
            "advertising partners", "data brokers", "affiliates",
            "marketing partners", "third-party vendors", "sponsors"
        ],
        "score": 5
    },
    "Indefinite Data Retention": {
        "keywords": [
            "retain indefinitely", "store indefinitely",
            "as long as necessary", "perpetual", "without deletion",
            "no expiration"
        ],
        "score": 3
    },
}