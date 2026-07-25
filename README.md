# 🔍 FAIRLENS

### AI-Powered Privacy & Data Collection Risk Scanner

FAIRLENS is an AI-assisted privacy and data collection risk scanner that helps users understand what personal information a website or digital service requests and identify potential privacy concerns.

Users can describe what a service does and paste text from signup forms, privacy notices, consent requests, permission requests, or data collection statements. FAIRLENS analyzes the information and provides a structured privacy risk assessment.

> FAIRLENS is an educational and analytical tool. It does not determine legal compliance and does not provide legal advice.

---

## ✨ Features

- 🔍 **AI-Powered Privacy Analysis**
  - Uses AI to analyze data collection practices in context.

- 🧠 **Context-Aware Risk Assessment**
  - Considers what the service does before evaluating whether requested data appears necessary.

- 🔐 **Sensitive Data Detection**
  - Identifies potentially sensitive categories of personal information.

- 📊 **Risk Category Analysis**
  - Evaluates six major privacy risk areas:
    - Data Necessity
    - Data Sensitivity
    - Data Minimization
    - Transparency
    - Consent & User Choice
    - Third-Party Data Sharing

- 📋 **Individual Data Request Analysis**
  - Explains why each detected data request may or may not be necessary.

- ⚠️ **Risk Scoring**
  - Provides risk levels from Low to Critical.

- 💡 **Actionable Recommendations**
  - Suggests what users may want to investigate or question.

- 🧩 **Deterministic Data Classification**
  - Combines AI reasoning with a local data classification system.

- 🛡️ **Input Validation & Error Handling**
  - Handles missing, invalid, and oversized inputs gracefully.

---

##  How FAIRLENS Works

FAIRLENS follows a hybrid analysis approach that combines deterministic logic with contextual AI reasoning.

-text
User Input
    │
    ▼
Service Description
    │
    +
    │
Data Collection Text
    │
    ▼
Local Data Classifier
    │
    ├── Detect Data Requests
    ├── Classify Data Types
    └── Identify Potentially Sensitive Data
    │
    ▼
AI Risk Analysis
    │
    ├── Evaluate Data Necessity
    ├── Evaluate Data Sensitivity
    ├── Evaluate Data Minimization
    ├── Evaluate Transparency
    ├── Evaluate Consent
    └── Evaluate Data Sharing
    │
    ▼
Risk Framework
    │
    ▼
Structured Privacy Risk Report
    │
    ├── Overall Risk
    ├── Data Requests
    ├── Risk Categories
    ├── Key Findings
    └── Recommended Actions

The AI does not automatically treat sensitive information as unnecessary or high-risk.
Instead, FAIRLENS considers the context of the service.
For example:
A banking service requesting financial information may be reasonable.
A healthcare service requesting health information may be expected.
A weather application requesting precise location may be context-dependent.
A simple calculator application requesting precise location may be potentially excessive.

Core Modules
| File                 | Purpose                                                       |
| -------------------- | ------------------------------------------------------------- |
| `app.py`             | Gradio-based user interface                                   |
| `risk_analyzer.py`   | Main AI analysis pipeline and result processing               |
| `data_classifier.py` | Detects and classifies requested data                         |
| `risk_framework.py`  | Defines risk levels, categories, and framework logic          |
| `prompts.py`         | Contains AI system and analysis prompts                       |
| `test_analyzer.py`   | Tests analysis functionality and validation                   |
| `requirements.txt`   | Python project dependencies                                   |
| `.env.example`       | Example environment variable configuration                    |
| `.gitignore`         | Prevents sensitive and unnecessary files from being committed |

🖥️ Tech Stack
Python
Gradio — User interface
Groq API — AI-powered analysis
python-dotenv — Environment variable management
JSON — Structured AI responses
Custom Python Risk Framework — Privacy risk categorization
Custom Data Classifier — Deterministic data detection and classification

🧪 Example Use Cases
FAIRLENS can analyze text from:
Website registration forms
Mobile application signup forms
Privacy notices
Consent requests
Cookie notices
Permission requests
Data collection statements
Online services requesting personal information
Example
Service:
An online weather application that provides local weather forecasts.
Data Collection Text:
To provide personalized weather forecasts, we request your precise location. You may also optionally provide your email address to receive weekly weather updates.
FAIRLENS can evaluate:
Whether location data appears necessary
Whether precise location may be more data than required
Whether email collection is optional
Potential sensitivity of the requested information
Transparency of the data collection explanation
Overall privacy risk

🔒 Privacy & Security
FAIRLENS is designed to keep API credentials separate from source code.
Sensitive configuration should be stored in a local .env file and excluded from Git using .gitignore.
The .env.example file provides an example of the required environment variable without containing a real API key.
Never commit real API keys to GitHub.

⚠️ Disclaimer
FAIRLENS provides AI-assisted privacy risk analysis for educational and informational purposes.
The tool:
Does not determine whether a service complies with any specific law or regulation.
Does not provide legal advice.
Does not replace professional privacy, security, or legal assessments.
May produce incomplete or inaccurate results depending on the information provided and the AI model used.
Users should treat FAIRLENS results as a starting point for further investigation and critical review.

🌱 Future Improvements
Potential future improvements include:
📈 Interactive visual risk charts
📊 Privacy risk dashboards
📄 Exportable PDF reports
🌐 Website URL scanning
🔗 Automated privacy policy extraction
🧾 Side-by-side comparison of privacy notices
🧠 More advanced data classification
🌍 Multilingual privacy analysis
🔎 Evidence highlighting from analyzed text

👩‍💻 Project Status
Status: Active prototype
FAIRLENS was created as a practical exploration of AI-assisted privacy analysis, responsible AI, data minimization, and human-centered technology.

📜 License
This project is intended for educational and portfolio purposes.
