# PhishGuard - Real-Time Phishing Detection System

A machine learning system that detects phishing URLs in real time using a Random Forest classifier trained on 6,500+ real-world URLs from PhishTank and legitimate sources.

## Results
- **Random Forest AUC-ROC: 99.90%**
- **XGBoost AUC-ROC: 99.82%**
- **Logistic Regression AUC-ROC: 98.85%**
- Trained on 3,250 real phishing URLs from PhishTank + 3,250 legitimate URLs
- 24 behavioral and structural URL features engineered from scratch

## Features Extracted
- URL length, domain length, path length
- Number of hyphens, dots, underscores, digits
- Presence of IP address instead of domain
- HTTPS vs HTTP
- Suspicious keyword count (login, verify, secure, paypal, etc.)
- URL entropy (randomness score)
- Suspicious TLD detection (.tk, .ml, .xyz, etc.)
- Number of subdomains

## Tech Stack
- Python, scikit-learn, XGBoost, pandas, NumPy
- Flask (live web dashboard)
- PhishTank API (real threat intelligence data)

## How to Run

### 1. Install dependencies
### 2. Download data
### 3. Build dataset
### 4. Train models
### 5. Launch dashboard
Open browser at `http://localhost:5000`

## Dashboard Features
- Submit any URL for instant phishing prediction
- Confidence score display
- Feature analysis breakdown
- Live counter of URLs analyzed, phishing detected, safe URLs
- Recent analysis history

## Sample Detections
| URL | Result | Confidence |
|-----|--------|-----------|
| http://paypal-verify-account.tk/login | PHISHING | 99% |
| http://192.168.1.1/secure/banking/login.php | PHISHING | 100% |
| http://amazon-account-suspended.xyz/verify | PHISHING | 100% |
| https://www.google.com | SAFE | 60% |

## Known Limitations
- Model trained primarily on URL structure features, not content
- Some legitimate URLs with complex paths may trigger false positives
- Model should be retrained periodically as phishing patterns evolve

## Author
Astha Patel | M.S. Information Technology, Arizona State University
GitHub: github.com/astha2310
