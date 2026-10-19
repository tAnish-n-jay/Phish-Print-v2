# PhishPrint V2 🎣🔍
### Real-Time Phishing URL Detection with Live Feature Extraction

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![ML](https://img.shields.io/badge/ML-XGBoost%20%7C%20Random%20Forest%20%7C%20LightGBM-orange)
![Accuracy](https://img.shields.io/badge/Accuracy-97.97%25-brightgreen)
![Backend](https://img.shields.io/badge/Backend-FastAPI-teal)
![Frontend](https://img.shields.io/badge/Frontend-Streamlit-red)

---

## Overview

PhishPrint V2 is a machine learning-based phishing URL detection system that extracts 30+ real features from any raw URL and classifies it as **legitimate** or **phishing** with 97.97% accuracy.

Unlike traditional approaches that rely on pre-extracted datasets, PhishPrint V2 builds its own feature extraction pipeline from scratch — including lexical analysis, WHOIS lookups, and live webpage inspection.

---

## What's New in V2 vs V1

| Feature | V1 | V2 |
|---|---|---|
| Dataset | Pre-extracted features | Raw URLs — extract everything live |
| Dataset Size | 11,430 URLs | 30,000 URLs |
| Typosquatting Detection | ❌ | ✅ Brand similarity score |
| Models | RF + XGBoost | RF + XGBoost + LightGBM + Ensemble |
| Accuracy | 96.28% | **97.97%** |
| Backend | None | FastAPI REST API |
| Explainability | Feature importance | SHAP force plots per prediction |

---

## Tech Stack

```
Language      : Python 3.10+
ML            : Scikit-learn, XGBoost, LightGBM
Data          : Pandas, NumPy
Feature Ext.  : Requests, BeautifulSoup, python-whois, tldextract
Explainability: SHAP
Backend       : FastAPI + Uvicorn
Frontend      : Streamlit
Version Ctrl  : Git + GitHub
```

---

## Dataset

| Source | Type | Count |
|---|---|---|
| OpenPhish + Phishing.Database (GitHub) | Phishing URLs | 15,000 |
| Majestic Million (Top domains by traffic) | Legitimate URLs | 15,000 |
| **Total** | **Balanced** | **30,000** |

---

## Features Extracted (30+)

### Lexical Features (URL string analysis)
- URL length, hostname length, path length
- Count of special characters (dots, hyphens, slashes, @, ?, =)
- Ratio of digits in URL and hostname
- HTTPS token presence
- IP address as hostname
- Number of subdomains
- Suspicious TLD detection (.tk, .ml, .ga, .cf)
- URL shortening service detection
- Phishing keyword hints (login, verify, secure, account)
- **Brand similarity score** (typosquatting detection)

### WHOIS Features
- DNS record existence

### Webpage Features
- Number of hyperlinks
- Ratio of internal vs external links
- Number of external CSS files
- Login form presence
- iFrame presence
- External favicon detection
- Page title matches domain

---

## Model Results

| Model | Accuracy | ROC-AUC |
|---|---|---|
| Random Forest | 97.65% | ~0.992 |
| LightGBM | 97.80% | ~0.994 |
| Ensemble | 97.87% | ~0.996 |
| **XGBoost** ✅ | **97.97%** | **~0.995** |

> XGBoost selected as best model based on test accuracy.

---

## Project Structure

```
PhishPrint-V2/
│
├── data/
│   ├── raw/                         # Raw URLs (gitignored)
│   ├── batches/                     # Extraction batches (gitignored)
│   └── processed/                   # Final dataset (gitignored)
│
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_feature_extraction.ipynb
│   ├── 03_EDA.ipynb
│   ├── 04_preprocessing.ipynb
│   ├── 05_model_training.ipynb
│   └── 06_evaluation.ipynb
│
├── src/
│   └── feature_extractor.py         # All feature extraction functions
│
├── api/
│   └── main.py                      # FastAPI backend
│
├── app/
│   └── streamlit_app.py             # Streamlit frontend
│
├── models/                          # Saved models (gitignored)
├── results/                         # Plots and evaluation outputs
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/tAnish-n-jay/PhishPrint-V2.git
cd PhishPrint-V2
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the notebooks in order
```
01 → 02 → 03 → 04 → 05 → 06
```
> Note: Notebook 02 (feature extraction) runs for several hours. Start it overnight.

### 5. Start the FastAPI backend
```bash
cd api
uvicorn main:app --reload
```

### 6. Start the Streamlit frontend
```bash
cd app
streamlit run streamlit_app.py
```

---

## API Usage

### Endpoint
```
POST /predict
```

### Request
```json
{
  "url": "https://example.com"
}
```

### Response
```json
{
  "url": "https://example.com",
  "verdict": "legitimate",
  "confidence": 97.3,
  "top_features": {
    "hostname_length": 0.423,
    "nb_subdomains": 0.312,
    "ratio_digits_url": 0.289,
    "nb_slash": 0.201,
    "https_token": -0.198
  }
}
```

---

## Explainability

PhishPrint V2 uses **SHAP (SHapley Additive exPlanations)** to explain every prediction:

- **SHAP Summary Plot** — which features matter most across all predictions
- **SHAP Force Plot** — why the model made a specific decision for one URL

---

## Key Findings from EDA

- `hostname_length` is the strongest predictor (correlation: 0.59) — phishing URLs have unusually long hostnames
- `nb_subdomains` (0.53) — phishing sites use multiple subdomains to appear legitimate
- `ratio_digits_url` (0.50) — phishing URLs are packed with digits to obfuscate
- `https_token` is **negatively** correlated — legitimate sites use HTTPS far more consistently
- All top features are **lexical** — meaning fast, real-time detection without fetching the page

---

## Limitations

- Zero-day domains with no suspicious URL patterns may evade detection
- Heavily obfuscated URLs using encoding can bypass lexical features
- WHOIS lookups time out frequently for newly registered domains
- Model trained on a snapshot — requires periodic retraining on fresh phishing feeds

---

## Author

**Tanish**  
BTech Honours CSE (AI/ML) — RV University, Bengaluru  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://www.linkedin.com/in/tanish-n-jay-732a7b383/)
[![GitHub](https://img.shields.io/badge/GitHub-tAnish--n--jay-black)](https://github.com/tAnish-n-jay)

---

*PhishPrint V2 | AIML Internals Project | Built on learnings from V1*