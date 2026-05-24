import pandas as pd
import numpy as np
from features import extract_features
import warnings
warnings.filterwarnings('ignore')

print("=" * 50)
print("BUILDING DATASET")
print("=" * 50)

# ── Load phishing URLs ──
print("\n[1/4] Loading phishing URLs...")
try:
    phish_df = pd.read_csv("data/phishing_raw.csv")
    print(f"Columns found: {list(phish_df.columns)}")
    
    # PhishTank uses 'url' column
    if 'url' in phish_df.columns:
        phish_urls = phish_df['url'].dropna().tolist()
    elif 'URL' in phish_df.columns:
        phish_urls = phish_df['URL'].dropna().tolist()
    else:
        phish_urls = phish_df.iloc[:, 0].dropna().tolist()
    
    print(f"Loaded {len(phish_urls)} phishing URLs from PhishTank")
except Exception as e:
    print(f"PhishTank load failed: {e}")
    phish_urls = []

# Load backup if needed
if len(phish_urls) < 1000:
    print("Loading backup phishing dataset...")
    try:
        backup_df = pd.read_csv("data/backup_phishing.csv")
        print(f"Backup columns: {list(backup_df.columns)}")
        if 'url' in backup_df.columns:
            backup_urls = backup_df['url'].dropna().tolist()
        elif 'URL' in backup_df.columns:
            backup_urls = backup_df['URL'].dropna().tolist()
        else:
            backup_urls = backup_df.iloc[:, 0].dropna().tolist()
        phish_urls.extend(backup_urls)
        print(f"Total phishing URLs: {len(phish_urls)}")
    except Exception as e:
        print(f"Backup load failed: {e}")

# ── Load legitimate URLs ──
print("\n[2/4] Loading legitimate URLs...")
legit_df = pd.read_csv("data/legitimate_raw.csv")
legit_urls = legit_df['url'].dropna().unique().tolist()
print(f"Loaded {len(legit_urls)} legitimate URLs")

# ── Balance dataset ──
print("\n[3/4] Balancing dataset...")
max_samples = min(len(phish_urls), len(legit_urls), 5000)
phish_sample = phish_urls[:max_samples]
legit_sample = legit_urls[:max_samples]
print(f"Using {max_samples} phishing + {max_samples} legitimate = {max_samples*2} total")

# ── Extract features ──
print("\n[4/4] Extracting features (this takes a few minutes)...")
records = []
errors = 0

all_urls = [(u, 1) for u in phish_sample] + [(u, 0) for u in legit_sample]

for i, (url, label) in enumerate(all_urls):
    if i % 500 == 0:
        print(f"  Progress: {i}/{len(all_urls)} URLs processed...")
    try:
        url = str(url).strip()
        if not url.startswith('http'):
            url = 'http://' + url
        f = extract_features(url)
        if f:
            f['url'] = url
            f['label'] = label
            records.append(f)
    except:
        errors += 1

print(f"\nFeature extraction complete!")
print(f"  Successful: {len(records)}")
print(f"  Errors: {errors}")

# ── Save dataset ──
dataset = pd.DataFrame(records)
dataset.to_csv("data/dataset.csv", index=False)

print(f"\nDataset saved to data/dataset.csv")
print(f"Shape: {dataset.shape}")
print(f"\nLabel distribution:")
print(dataset['label'].value_counts())
print(f"\nFeature columns: {[c for c in dataset.columns if c not in ['url','label']]}")
print("\n✅ Dataset ready for training!")
