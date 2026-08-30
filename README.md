# ⚖️ Judi — Legal Support Chatbot for Students

A comprehensive, two-stage AI-powered legal advisory and support system designed to help students, youth, and victims in India identify, understand, and act upon their legal rights when facing crimes, abuse, institutional misconduct, and civil rights violations.

---

## ✨ Features

- **🧠 Two-Stage NLP Intelligence Pipeline**:
  - **Stage 1 (Complaint Gate)**: Logistic Regression with TF-IDF vectorization filters greetings, small talk, and general queries (99.7% accuracy).
  - **Stage 2 (Crime Classifier)**: spaCy multi-class CNN categorizes valid legal incidents into 20+ specialized crime classifications.
- **🛡️ POCSO Auto-Detection**: Automatically applies the *Protection of Children from Sexual Offences (POCSO) Act, 2012* for minors (age < 18) with strict privacy safeguards and specialized resources.
- **📜 50+ Indian Statutory Provisions**: Maps incidents directly to applicable sections of the Indian Penal Code (IPC), IT Act, UGC Anti-Ragging Regulations, POCSO Act, SC/ST Prevention of Atrocities Act, and the Constitution of India.
- **📝 Actionable Step-by-Step Filing Procedures**: Provides 8–22 concrete procedural steps for lodging First Information Reports (FIR), medical documentation, institutional complaints, and legal aid petitions.
- **📍 Location-Aware Resource Directory**: Dynamically filters local police stations, legal aid boards (NALSA/SLSA), cyber crime cells, and 24/7 helplines by state/district (e.g., National, Kerala, Mumbai, Delhi, Bangalore).
- **👤 User Authentication & History Persistence**: Secure account registration and login with salted SHA-256 password hashing. Chat consultations are synced across both browser storage and backend storage.
- **💻 Modern Responsive React Interface**: Dark/Light mode theme switcher, expandable legal provision cards, document attachment previews, and mobile-responsive drawer sidebar.

---

## 🎯 Supported Crime & Violation Categories

### 1. Violence & Physical Crimes
- **Physical Assault** (IPC 323, 324, 325, 336)
- **Sexual Assault** (IPC 375, 376, 354, POCSO Act)
- **Sexual Harassment** (IPC 354A, 354D, POSH Act)
- **Ragging** (Anti-Ragging Act, UGC Regulations 2009)

### 2. Online & Cyber Crimes
- **Cyber Harassment** (IT Act 66E, 67, IPC 354D)
- **Cyber Sexual Crime** (IT Act 67A, 67B, POCSO Act)
- **Impersonation & Doxxing** (IT Act 66C, 66D, IPC 419)
- **Online Hate Speech** (IPC 153A, 295A, 505)

### 3. Discrimination & Harassment
- **Caste Discrimination** (SC/ST Prevention of Atrocities Act, Art. 15)
- **Gender Discrimination** (Articles 14, 15, 16, UGC Guidelines)
- **Racism & Regional Bias** (IPC 153A, Article 15)
- **Religious Discrimination** (Articles 15, 25, IPC 295A)
- **General Discrimination** (Equal Opportunities Act, Rights of Persons with Disabilities)
- **Threats & Criminal Intimidation** (IPC 503, 506)
- **Stalking** (IPC 354D)

### 4. Exploitation & Institutional Violations
- **Blackmail & Extortion** (IPC 383, 384, 506)
- **Defamation & Privacy Violations** (IPC 499, 500, IT Act 66E)
- **Verbal Abuse & Insult** (IPC 504)
- **Institutional Misconduct** (UGC Grievance Redressal Regulations)
- **Administrative Violations** (Unlawful withholding of certificates/TC, illegal bonds)

---

## 🧠 Two-Stage Architecture & Pipeline

```
                       User Input Query
                              │
                              ▼
        ┌───────────────────────────────────────────┐
        │   Stage 1: Binary Complaint Gate         │
        │   (Logistic Regression + TF-IDF)          │
        └─────────────────────┬─────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
       [not_complaint]                   [complaint]
     (Greetings, FAQs,              (Crimes, Violations,
        Small Talk)                      Incidents)
              │                               │
              ▼                               ▼
  ┌───────────────────────┐       ┌───────────────────────────┐
  │ Friendly guidance     │       │ Stage 2: spaCy Multi-     │
  │ message returned      │       │ Class Text Categorizer    │
  │ (Skips legal engine)  │       └─────────────┬─────────────┘
  └───────────────────────┘                     │
                                                ▼
                                  ┌───────────────────────────┐
                                  │ Rule-based Postprocessor  │
                                  │ & Context Extractor       │
                                  │ (POCSO / Age / Authority) │
                                  └─────────────┬─────────────┘
                                                │
                                                ▼
                                  ┌───────────────────────────┐
                                  │ Statutory Knowledge Base  │
                                  │ (50+ Laws, Filing Steps,  │
                                  │ & Localized Contacts)     │
                                  └─────────────┬─────────────┘
                                                │
                                                ▼
                                  ┌───────────────────────────┐
                                  │ Structured Preliminary    │
                                  │ Legal Advisory Report     │
                                  └───────────────────────────┘
```

---

## 📁 Project Structure

```
legal-support-chatbot/
├── README.md                          # Project documentation
├── app.py                             # FastAPI backend application & API routing
├── requirements.txt                   # Python backend dependencies
├── start.ps1                          # PowerShell startup script (Windows)
├── start.bat                          # Batch startup script (Windows)
├── start.sh                           # Shell startup script (Linux / macOS)
│
├── frontend/                          # React web application
│   ├── package.json                   # Node dependencies & scripts
│   ├── public/
│   │   └── index.html                 # HTML entry point
│   └── src/
│       ├── App.js                     # Main chat interface, state & consultation manager
│       ├── App.css                    # Modern theme, animations, and responsive layout
│       └── index.js                   # React DOM root
│
├── nlp/                              # NLP classification engines
│   ├── complaint_detector.py         # Stage 1: Logistic Regression inference helper
│   ├── train_complaint_detector.py   # Stage 1: Logistic Regression training script
│   ├── train_classifier.py           # Stage 2: spaCy CNN model training script
│   └── postprocess.py                # Rule-based context extraction & statutory refinement
│
├── models/                           # Serialized machine learning models
│   ├── complaint_detector/           # Stage 1 artifacts
│   │   ├── logreg_model.joblib       # Trained Logistic Regression classifier
│   │   └── tfidf_vectorizer.joblib   # Fitted TF-IDF feature extractor
│   └── legal_textcat/               # Stage 2 artifacts
│       ├── meta.json
│       ├── textcat/
│       ├── tokenizer
│       └── vocab/
│
├── data/                             # Knowledge base, mappings, and datasets
│   ├── complaint_dataset.csv         # 3,189 binary samples for Stage 1 gate
│   ├── dataset.csv                   # 1,750 multi-class crime samples for Stage 2
│   ├── law_mapping_enhanced.json     # 50+ Indian legal provisions and procedures
│   ├── resources.json                # National emergency helplines and legal aid
│   ├── local_numbers.json            # State- and district-level contact directories
│   ├── case_laws.json                # Landmark case law citations
│   ├── users.json                    # User account database (salted SHA-256)
│   └── consultations/                # Saved user consultation session history
│
├── scripts/                          # Dataset generation utilities
│   ├── create_complaint_dataset.py   # Generates binary complaint dataset
│   └── generate_dataset.py           # Generates 20-category synthetic multi-class data
│
└── tests/                            # Automated test suite
    ├── test_complaint_detector.py    # Unit tests for Stage 1 gate
    ├── test_api.py                   # Integration tests for FastAPI endpoints
    └── test_query.py                 # Multi-class integration tests for Stage 2
```

---

## 🚀 Quick Start

### 1. Prerequisites
- **Python 3.8+** (Python 3.10 or 3.11 recommended)
- **Node.js 16+** and **npm**

---

### 2. Installation

#### A. Clone repository
```bash
git clone https://github.com/yourusername/legal-support-chatbot.git
cd legal-support-chatbot
```

#### B. Install Backend Dependencies
```bash
pip install -r requirements.txt
```
*Dependencies include: `fastapi`, `uvicorn`, `spacy`, `scikit-learn`, `joblib`, `pydantic`, `pandas`, `requests`.*

#### C. Install Frontend Dependencies
```bash
cd frontend
npm install
cd ..
```

---

### 3. Running the System

#### Option 1: Automatic Startup Scripts

- **Windows (PowerShell)**:
  ```powershell
  .\start.ps1
  ```
- **Windows (Command Prompt)**:
  ```cmd
  start.bat
  ```
- **Linux / macOS**:
  ```bash
  chmod +x start.sh
  ./start.sh
  ```

#### Option 2: Manual Terminal Startup

**Terminal 1 — Backend (FastAPI on port 8000)**:
```bash
python -m uvicorn app:app --reload --port 8000
```

**Terminal 2 — Frontend (React on port 3001)**:
```bash
cd frontend
PORT=3001 npm start
```

Open your browser and navigate to:
```
http://localhost:3001
```

---

## 🔧 API Reference

### 1. Main Chat Endpoint: `POST /chat`

Processes the user's message through the two-stage pipeline.

- **Request**:
  ```json
  {
    "message": "my senior punched me in the hostel",
    "location": "Kerala"
  }
  ```

- **Complaint Response (`200 OK`)**:
  ```json
  {
    "category": "physical_assault",
    "confidence": 0.35,
    "reason": "classified",
    "is_complaint": true,
    "matched_categories": [
      { "category": "physical_assault", "confidence": 0.35 },
      { "category": "ragging", "confidence": 0.22 }
    ],
    "context": {
      "age_indicator": null,
      "authority": "senior_student",
      "medium": "offline",
      "discrimination_types": [],
      "legal_framework": null,
      "location": "Kerala"
    },
    "legal_frameworks": [
      "Indian Penal Code (IPC)",
      "Anti-Ragging Act & National Anti-Ragging Rules"
    ],
    "laws": [
      {
        "act": "Indian Penal Code",
        "section": "323",
        "title": "Voluntarily causing hurt",
        "description": "Whoever voluntarily causes hurt shall be punished with imprisonment up to 1 year, or with fine up to 1000 rupees, or both."
      }
    ],
    "steps": [
      "File First Information Report (FIR) at nearest police station",
      "Get medical examination done immediately (within 24 hours ideally)"
    ],
    "resources": [
      {
        "name": "Local Police Station",
        "location": "Nearest police station in your jurisdiction",
        "contact": "112",
        "link": "https://www.keralapolice.gov.in"
      }
    ],
    "case_references": [],
    "warnings": []
  }
  ```

- **Non-Complaint Response (`200 OK`)**:
  ```json
  {
    "category": "not_complaint",
    "confidence": 0.95,
    "reason": "not_complaint",
    "is_complaint": false,
    "status": "not_complaint",
    "message": "Please describe the legal issue or incident you want help with.",
    "matched_categories": [],
    "context": { "location": "National" },
    "legal_frameworks": [],
    "laws": [],
    "steps": [],
    "resources": [],
    "case_references": [],
    "warnings": []
  }
  ```

---

### 2. User Authentication Endpoints

- **`POST /signup`**:
  ```json
  { "username": "student1", "password": "securepassword123" }
  ```
- **`POST /login`**:
  ```json
  { "username": "student1", "password": "securepassword123" }
  ```

---

### 3. Consultation History & Metadata

- **`GET /locations`**: Returns list of supported states and districts for localized contacts.
- **`GET /consultations/{username}`**: Retrieves saved consultation sessions for a user.
- **`POST /consultations/{username}`**: Saves and syncs consultation chat history.

---

## 🧪 Testing

Run the automated test suite from the repository root:

```bash
# 1. Test Stage 1 Complaint Gate
python tests/test_complaint_detector.py

# 2. Test FastAPI Endpoints (Gate, Auth, Locations, History)
python tests/test_api.py

# 3. Test Stage 2 Multi-Class Categorizer & Postprocessor
python tests/test_query.py
```

---

## 🧠 Retraining the AI Models

### Retrain Stage 1 (Complaint Detector Gate)
```bash
# 1. Generate/refresh the binary dataset
python scripts/create_complaint_dataset.py

# 2. Fit TF-IDF & Logistic Regression model
python nlp/train_complaint_detector.py
```
*Artifacts are saved to `models/complaint_detector/`.*

### Retrain Stage 2 (Multi-Class Crime Classifier)
```bash
# 1. (Optional) Rebuild synthetic multi-class training data
python scripts/generate_dataset.py

# 2. Train spaCy Text Categorizer
python nlp/train_classifier.py
```
*Artifacts are saved to `models/legal_textcat/`.*

---

## 🐛 Troubleshooting

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| **Port 8000 already in use** | An existing backend process is running | `netstat -ano \| findstr :8000` (Windows) or `fuser -k 8000/tcp` (Linux) to find and kill the process. |
| **Port 3001 in use** | Another frontend instance is active | Run with `PORT=3002 npm start` in `frontend/`. |
| **Missing joblib / sklearn** | Python dependencies not updated | Run `pip install -r requirements.txt`. |
| **CORS errors in browser** | Frontend cannot reach port 8000 | Ensure backend is active and reachable at `http://localhost:8000`. |
| **Model files missing** | Models have not been trained | Run `python nlp/train_complaint_detector.py` and `python nlp/train_classifier.py`. |

---

## ⚠️ Legal Disclaimer

> **IMPORTANT**: Judi is an automated educational and preliminary legal assistance tool. It does **not** constitute formal legal representation or binding legal advice. Users facing active threats or emergency situations should immediately contact emergency authorities (dial **112**) or consult a licensed advocate / legal aid authority.

---

## 📄 License

This project is open source and distributed under the **MIT License**.
