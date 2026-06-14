# PhishGuard — ML Phishing URL Detection

Built by Astha Patel | M.S. Information Technology, Arizona State University

---

## Why I Built This

Phishing is the entry point for most major breaches. The 2024 Verizon DBIR puts it at over 36% of all incidents. But most phishing detection tools are either black-box commercial products or academic demos that never touch real data.

I wanted to build a classifier from scratch using real phishing URLs, real feature engineering, and a model I could actually explain. No API wrappers. No pre-trained models. Just raw data and honest evaluation.

---

## What It Does

PhishGuard takes a URL as input and classifies it as phishing or legitimate. It extracts 24 behavioral and structural features from the URL itself, then runs them through a trained machine learning model. A Flask web interface lets you paste any URL and get a real-time prediction with a confidence score.

---

## The Data

6,500 plus real URLs sourced from PhishTank for verified phishing and public datasets for legitimate URLs. No synthetic data. Every URL in the training set is real.

---

## Feature Engineering

This is where I spent the most time. The model does not just look at the URL string. It extracts 24 features covering URL length and structure, suspicious character patterns, domain age signals, HTTPS presence, lexical similarity to known legitimate domains for typosquatting detection, presence of IP addresses instead of domain names, and redirect chain indicators.

The hypothesis: phishing URLs behave differently from legitimate ones at a structural level, even before you visit them.

---

## Model Performance

| Model | AUC-ROC |
|---|---|
| Random Forest | 99.90% |
| XGBoost | 99.82% |
| Logistic Regression | 98.85% |

Random Forest won. 99.90% AUC-ROC means the model almost perfectly separates phishing from legitimate URLs across all classification thresholds.

---

## Tech Stack

Python 3, scikit-learn, XGBoost, pandas, NumPy, Flask, matplotlib, seaborn

---

## How to Run It

```bash
git clone https://github.com/astha2310/phishguard.git
cd phishguard

pip3 install scikit-learn xgboost flask pandas numpy matplotlib seaborn

python3 train.py
python3 app.py
```

Then open http://127.0.0.1:5000 in your browser.

---

## What I Learned

The biggest lesson was about class imbalance. Getting to a genuinely useful model required careful attention to precision and recall, not just accuracy. A model that predicts "legitimate" for everything would be 95 percent accurate and completely useless.

I also learned that feature engineering matters more than model choice. The gap between good features and bad ones was larger than the gap between Logistic Regression and Random Forest.

The most interesting finding: URL length alone is surprisingly predictive. Phishing URLs are significantly longer on average than legitimate ones, probably because attackers are hiding the real destination domain deep in the path.

---

## What Could Be Added Next

Real-time URL scanning in a browser extension, live threat feed integration to flag newly registered phishing domains, expanded features including WHOIS and DNS records, and an API endpoint for integration with other security tools.

---

## Disclaimer

Built for educational purposes and security research. All phishing URLs are from PhishTank's public verified feed.

---

Astha Patel | github.com/astha2310 | linkedin.com/in/asthap23
