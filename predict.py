"""
PhishGuard - command-line predictions
Built by Astha Patel

Usage:
  python3 predict.py <url> [<url> ...]     check one or more URLs
  python3 predict.py --real-world          run the real-world sanity check

The real-world check uses links the model never saw in training:
real, legitimate pages with longer paths, plus two phishing-style links.
It exists to show the model's false-positive problem honestly
(see "Real-world testing" in the README).
"""

import sys
import warnings

import joblib
import pandas as pd

from features import extract_features

warnings.filterwarnings("ignore")

model = joblib.load("models/best_model.pkl")
feature_cols = joblib.load("models/feature_cols.pkl")

REAL_WORLD_CHECK = [
    # (url, what it really is)
    ("https://www.google.com", "legitimate"),
    ("https://www.fedex.com/en-us/tracking.html", "legitimate"),
    ("https://github.com/astha2310/phishguard", "legitimate"),
    ("https://docs.python.org/3/library/urllib.parse.html", "legitimate"),
    ("http://brightline-it-helpdesk.example/verify", "phishing"),
    ("http://parcelgo-redelivery.example", "phishing"),
]


def predict(url):
    if not url.startswith("http"):
        url = "http://" + url
    row = pd.DataFrame([extract_features(url)])[feature_cols]
    label = int(model.predict(row)[0])
    confidence = model.predict_proba(row)[0][label] * 100
    return url, ("PHISHING" if label == 1 else "SAFE"), confidence


def main(args):
    if not args:
        print(__doc__)
        return

    if args[0] == "--real-world":
        correct = 0
        print(f"{'URL':<55} {'Really':<11} {'Model says':<11} Confidence")
        for url, truth in REAL_WORLD_CHECK:
            url, verdict, conf = predict(url)
            ok = (verdict == "PHISHING") == (truth == "phishing")
            correct += ok
            print(f"{url:<55} {truth:<11} {verdict:<11} {conf:5.1f}%  {'OK' if ok else 'WRONG'}")
        print(f"\n{correct}/{len(REAL_WORLD_CHECK)} correct on real-world links")
        return

    for url in args:
        url, verdict, conf = predict(url)
        print(f"{url}  ->  {verdict}  ({conf:.1f}% confidence)")


if __name__ == "__main__":
    main(sys.argv[1:])
