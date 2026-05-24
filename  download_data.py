import pandas as pd
import requests
import os

print("Downloading phishing URLs from PhishTank...")

# PhishTank public CSV - no account needed
url = "http://data.phishtank.com/data/online-valid.csv"
headers = {"User-Agent": "phishing-detector-research"}

try:
    r = requests.get(url, headers=headers, timeout=60)
    with open("data/phishing_raw.csv", "wb") as f:
        f.write(r.content)
    print("Phishing data downloaded!")
except Exception as e:
    print(f"PhishTank failed: {e}")
    print("Using backup dataset...")

# Backup - University of New Brunswick phishing dataset
backup_url = "https://raw.githubusercontent.com/GregaVrbancic/Phishing-Dataset/master/dataset_small.csv"
try:
    r2 = requests.get(backup_url, timeout=30)
    with open("data/backup_phishing.csv", "wb") as f:
        f.write(r2.content)
    print("Backup dataset downloaded!")
except Exception as e:
    print(f"Backup also failed: {e}")

# Download legitimate URLs from Tranco list
print("Downloading legitimate URLs from Tranco...")
tranco_url = "https://tranco-list.eu/download/KZQYX/1000000"
try:
    r3 = requests.get(tranco_url, timeout=60)
    with open("data/legitimate_raw.csv", "wb") as f:
        f.write(r3.content)
    print("Legitimate URLs downloaded!")
except Exception as e:
    print(f"Tranco failed: {e}")
    # Create sample legitimate URLs as fallback
    legit_domains = [
        "https://www.google.com", "https://www.amazon.com",
        "https://www.microsoft.com", "https://www.apple.com",
        "https://www.github.com", "https://www.linkedin.com",
        "https://www.youtube.com", "https://www.wikipedia.org",
        "https://www.reddit.com", "https://www.stackoverflow.com",
        "https://www.netflix.com", "https://www.spotify.com",
        "https://www.dropbox.com", "https://www.salesforce.com",
        "https://www.adobe.com", "https://www.oracle.com",
        "https://www.ibm.com", "https://www.cisco.com",
        "https://www.intel.com", "https://www.nvidia.com"
    ]
    df = pd.DataFrame({"url": legit_domains * 500, "label": [0] * 10000})
    df.to_csv("data/legitimate_raw.csv", index=False)
    print("Created sample legitimate URLs as fallback")

print("\nAll downloads complete! Check the data/ folder.")