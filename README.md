# PhishGuard — ML Phishing URL Detection

Built by Astha Patel | M.S. Information Technology, Arizona State University

> **The short version:** PhishGuard scores 99.89% AUC-ROC on its test set. Then I tested it on real websites, and it flagged the real FedEx tracking page, the Python docs and this GitHub repo as phishing. This README explains both results, and why the second one taught me more.

---

## Why I Built This

Phishing is one of the most common ways attackers get into an organization, and the link is usually the weapon. I wanted to build a URL classifier from scratch, with features I could explain, instead of wrapping someone else's API. No pre-trained models: just data, feature engineering, and honest evaluation.

---

## What It Does

PhishGuard takes a URL and classifies it as phishing or legitimate, with a confidence score. It extracts 24 structural features from the URL string itself, without visiting the page, and runs them through a Random Forest model.

You can use it three ways:
- `predict.py`: check URLs from the command line
- `app.py`: a Flask web interface with feature breakdowns and history
- `predict.py --real-world`: the sanity check described below

---

## The Data

| Class | Count | Source |
|---|---|---|
| Phishing | 3,250 | Verified phishing URLs from PhishTank's public feed (with a public phishing dataset as backup) |
| Legitimate | 3,250 | Well-known real domains (Microsoft, Booking.com, MIT, etc.) paired with common page paths like `/careers`, `/privacy`, `/help` |

The pipeline: `download_data.py` downloads the raw URLs, `build_dataset.py` extracts features into `data/dataset.csv`, and `train.py` trains the models.

---

## Feature Engineering

24 features, all computed from the URL text (`features.py`):

- **Length:** URL, domain and path length
- **Character counts:** dots, hyphens, underscores, slashes, `@`, `?`, `=`, `&`, `%`, digits
- **Red flags:** IP address instead of a domain, `@` in the URL, `//` inside the path, missing HTTPS
- **Suspicious words:** `login`, `verify`, `account`, `password`, brand names like `paypal`, and others
- **Structure:** number of subdomains, top-level-domain length, high-risk TLDs (`.tk`, `.xyz`, `.top`, …)
- **Randomness:** Shannon entropy of the URL and of the domain

---

## Model Performance (test set)

| Model | AUC-ROC |
|---|---|
| Random Forest | 99.89% |
| XGBoost | 99.82% |
| Logistic Regression | 98.32% |

Random Forest won, with 99% precision and recall on 1,300 held-out URLs. On this dataset, the model separates phishing from legitimate almost perfectly.

---

## Real-World Testing: What 99.89% Didn't Tell Me

For a phishing-awareness experiment I ran in November 2026, I tested PhishGuard on links it had never seen. Run it yourself with `python3 predict.py --real-world`:

| URL | Really | PhishGuard says |
|---|---|---|
| `https://www.google.com` | Legitimate | Safe (60.5%) |
| `https://www.fedex.com/en-us/tracking.html` | Legitimate | **Phishing (98.5%)** |
| `https://github.com/astha2310/phishguard` | Legitimate | **Phishing (100%)** |
| `https://docs.python.org/3/library/urllib.parse.html` | Legitimate | **Phishing (100%)** |
| `http://brightline-it-helpdesk.example/verify` | Phishing-style | Phishing (99.0%) |
| `http://parcelgo-redelivery.example` | Phishing-style | Phishing (98.3%) |

It caught every phishing link, but it also called most real websites phishing, very confidently.

**Why it happens:** I went back to the training data, and the answer was there. Every legitimate URL in the dataset was short and simple:

| Feature | Legitimate URLs | Phishing URLs |
|---|---|---|
| Uses HTTPS | 100% | 86% |
| Average length | 28 characters | 46 characters |
| Exactly 3 slashes | 100% | 66% |

So the model learned a shortcut: *"short, HTTPS, one-level path = safe; anything else = phishing."* Real websites don't follow that rule. FedEx tracking pages, documentation and GitHub repos all have longer, deeper paths. The test set couldn't catch this, because it came from the same biased data.

**Why this matters in a SOC:** a detection tool with an impressive lab score can still flood analysts with false positives on real traffic, which is how alert fatigue starts. Before trusting any model, vendor tools included, test it on your own environment.

---

## Tech Stack

Python 3, scikit-learn, XGBoost, pandas, NumPy, tldextract, Flask, joblib

---

## How to Run It

```bash
git clone https://github.com/astha2310/phishguard.git
cd phishguard

pip3 install -r requirements.txt

python3 train.py                                   # trains the models (about 30 seconds)
python3 predict.py http://paypal-verify-account.tk/login
python3 predict.py --real-world                    # the real-world check above
python3 app.py                                     # web interface
```

Then open `http://127.0.0.1:5001` in your browser (it only works while app.py is running on your computer).

**Mac note:** the app uses port 5001, because macOS reserves port 5000 for AirPlay Receiver.

To rebuild the dataset from scratch: `python3 download_data.py` then `python3 build_dataset.py`.

---

## What I Learned

1. **A great test score can hide a broken model.** The test set shares the training data's blind spots. Real-world validation on fresh, varied data is a separate and necessary step.
2. **The data decides what the model learns.** My legitimate URLs were too clean, so the model learned "messy = phishing." Fixing the data matters more than switching algorithms: all three models scored within 2% of each other.
3. **URL length really is a strong signal,** since attackers often hide the real destination deep in the path. But on its own, it punishes every legitimate site with a long link.

---

## What's Next

- Retrain on realistic legitimate URLs: deep links from real sites (tracking pages, docs, login portals), including some plain-HTTP sites
- Add a fixed real-world validation set, and report its false-positive rate next to the AUC
- Add domain-based features (WHOIS domain age, DNS records) so the model looks beyond the URL's shape
- A browser extension and an API endpoint for integration with other security tools

---

## Disclaimer

Built for educational purposes and security research. Phishing URLs come from PhishTank's public verified feed. Don't visit any URL from the dataset.

---

Astha Patel | github.com/astha2310 | linkedin.com/in/asthap23
