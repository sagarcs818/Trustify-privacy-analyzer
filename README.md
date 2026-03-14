# 🛡️ Trustify – AI-Powered Privacy Analyzer

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Django](https://img.shields.io/badge/Django-Framework-green)
![NLP](https://img.shields.io/badge/NLP-Text%20Analysis-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Trustify** is an AI-powered web platform that helps users understand and evaluate the privacy policies of mobile apps and websites.  
Most users **blindly accept privacy policies** without reading how their personal data is collected, used, stored, or shared.

Trustify retrieves privacy policies of **listed applications** and analyzes potential **data-tracking risks**. If an application is not listed, users can paste the privacy policy manually for analysis. The platform then presents the results in a clear dashboard with a **Consent Risk Score, Safety Rating, and key privacy disclosures with short contextual descriptions** showing where those practices appear in the policy, helping users make informed privacy decisions.

---

# 🚀 Core Features

- AI-based extraction of **data-tracking risks**
- **Single app privacy audit** with Consent Risk Score and Safety Rating
- **Side-by-side comparison** of two applications
- **Multi-engine scraper**
  - Jina AI  
  - BeautifulSoup4  
  - Playwright  
  - Wayback Machine
- **Sentiment analysis** and weighted keyword detection
- **Sentence-level context extraction**
- **Manual paste mode** for custom privacy text
- **Fully responsive modern UI**

---

# 🖼️ Application Screenshots

## 🏠 Home Page
Landing page introducing the platform with navigation to the **Analyze Policy** tool.

![Home Page](https://github.com/user-attachments/assets/3f4918ac-d69c-4e43-8054-562c463c2a34)

---

## 🛡️ Single App Analysis
Displays the **Consent Risk Score, Safety Rating, and contextual evidence** extracted from the policy.

![Single App Analysis](https://github.com/user-attachments/assets/4bbd6529-169c-43ae-b8af-4149977cb178)

---

## ⚖️ App Comparison
Compare two applications with a **visual bar chart** showing which one is safer for user data.

![App Comparison Chart](https://github.com/user-attachments/assets/b2dff5ea-d6bb-4fa8-86d6-3f37c6779921)
![App Comparison Key Disclosures](https://github.com/user-attachments/assets/e18de45f-5fe5-479a-badf-b7dc2c0e1c32)

---

## 🔄 System Workflow
Architecture flow illustrating how the system processes a request.

![Workflow](https://github.com/user-attachments/assets/e9ecdc1c-9fbe-4176-b6bc-30275da38c4c)

---

# 🔄 System Workflow Explanation

### 1️⃣ User Search & Input
User searches for an application name (e.g., **WhatsApp**) or pastes a custom privacy policy.

### 2️⃣ Conditional Policy Retrieval
System checks if the application exists in the internal list.

- **Known App** → Privacy policy fetched using scraping tools  
- **Unknown App** → User pastes the privacy policy manually

### 3️⃣ Text Preprocessing
Raw text is processed using:

- Tokenization  
- Stopword removal  
- Text cleaning  

### 4️⃣ Sentiment Analysis & Keyword Detection
The NLP engine:

- Detects risky or aggressive clauses  
- Extracts sensitive permission keywords (Location, Contacts, Microphone, etc.)

### 5️⃣ Score Calculation & Results
The system generates:

- **Privacy Risk Score**
- **Safety Rating**

Results are displayed with **graphs and visual dashboards**.

---

# 🛠️ Tech Stack

## Backend
- Python
- Django
- SQLite

## AI & NLP
- TextBlob (Sentiment Analysis)
- Python `re` (Regex processing)

## Frontend
- HTML5
- CSS3
- Tailwind CSS
- JavaScript
- Chart.js

## Scraping & Automation
- Playwright
- BeautifulSoup4
- Jina AI API
- Archive.org API

---

# 📂 Project Structure

```text
TRUSTIFY-PRIVACY-ANALYZER/
│
├── analyzer/                   # Main Django App
│   ├── migrations/             # Database migrations
│   ├── __init__.py
│   ├── admin.py
│   ├── analysis_engine.py      # Core NLP & Scoring Logic
│   ├── apps.py
│   ├── models.py               # Database schemas
│   ├── policy_sources.py       # Source mapping
│   ├── risk_keywords.py        # Weighted keyword dictionary
│   ├── tests.py
│   ├── urls.py                 # App-level routing
│   ├── utils.py                # 4-Engine Scraper Logic
│   └── views.py                # Smart Caching & Core Views
│
├── static/                     # Global Static Assets
│   └── images/                 # Image assets
│
├── templates/                  # Global HTML Templates
│   ├── contact.html
│   ├── index.html              # Landing Page
│   ├── privacy.html            # Main Analyze Policy Page
│   ├── privacy_policy.html
│   ├── team.html
│   └── terms_service.html
│
├── trustify/                   # Django Project Config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py                 # Root-level routing
│   └── wsgi.py
│
├── .gitignore                  # Ignores venv, sqlite3, and pycache
├── manage.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/code2Renovate/Trustify-privacy-analyzer.git
cd Trustify-privacy-analyzer
```

---

### 2️⃣ Create Virtual Environment

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Install Playwright Browser

```bash
playwright install chromium
```

---

### 5️⃣ Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 6️⃣ Start Server

```bash
python manage.py runserver
```

---

### 7️⃣ Open in Browser

```
http://127.0.0.1:8000/
```

---

## 🎯 Project Objective
Trustify aims to:
- Identify hidden privacy risks in long legal documents
- Provide AI-based transparency for everyday users
- Compare applications based on data-handling practices
- Simplify privacy policies so users can make informed decisions
  
⭐ If you found this project useful, consider starring the repository.

## 📜 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
