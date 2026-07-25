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

## 🧠 How FAIRLENS Works

FAIRLENS follows a hybrid analysis approach that combines deterministic logic with contextual AI reasoning.

```text
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
