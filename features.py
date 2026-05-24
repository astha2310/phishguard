import re
import tldextract
from urllib.parse import urlparse

def extract_features(url):
    features = {}
    
    try:
        parsed = urlparse(url)
        ext = tldextract.extract(url)
    except:
        return None

    # Length features
    features['url_length'] = len(url)
    features['domain_length'] = len(ext.domain)
    features['path_length'] = len(parsed.path)

    # Count features
    features['num_dots'] = url.count('.')
    features['num_hyphens'] = url.count('-')
    features['num_underscores'] = url.count('_')
    features['num_slashes'] = url.count('/')
    features['num_at'] = url.count('@')
    features['num_question'] = url.count('?')
    features['num_equals'] = url.count('=')
    features['num_ampersand'] = url.count('&')
    features['num_percent'] = url.count('%')
    features['num_digits'] = sum(c.isdigit() for c in url)

    # Boolean features
    features['has_ip'] = 1 if re.match(
        r'http[s]?://\d+\.\d+\.\d+\.\d+', url) else 0
    features['has_https'] = 1 if parsed.scheme == 'https' else 0
    features['has_www'] = 1 if 'www.' in url else 0
    features['has_at_symbol'] = 1 if '@' in url else 0
    features['has_double_slash'] = 1 if '//' in parsed.path else 0

    # Suspicious keywords
    suspicious_words = [
        'login', 'verify', 'secure', 'account', 'update',
        'banking', 'confirm', 'password', 'signin', 'paypal',
        'ebay', 'apple', 'microsoft', 'amazon', 'support',
        'suspend', 'unusual', 'click', 'free', 'winner'
    ]
    url_lower = url.lower()
    features['suspicious_word_count'] = sum(
        1 for word in suspicious_words if word in url_lower)

    # Subdomain features
    features['num_subdomains'] = len(
        ext.subdomain.split('.')) if ext.subdomain else 0

    # Entropy (randomness of URL)
    import math
    def entropy(s):
        if not s:
            return 0
        prob = [float(s.count(c)) / len(s) for c in set(s)]
        return -sum(p * math.log(p, 2) for p in prob)
    features['url_entropy'] = entropy(url)
    features['domain_entropy'] = entropy(ext.domain)

    # TLD features
    features['tld_length'] = len(ext.suffix) if ext.suffix else 0
    suspicious_tlds = [
        'tk', 'ml', 'ga', 'cf', 'gq', 'xyz', 'top',
        'click', 'link', 'work', 'date', 'racing'
    ]
    features['suspicious_tld'] = 1 if ext.suffix in suspicious_tlds else 0

    return features

if __name__ == "__main__":
    test_urls = [
        "https://www.google.com",
        "http://paypal-verify-account.tk/login?user=test",
        "https://192.168.1.1/secure/banking/login.php",
        "https://www.amazon.com/products/item123"
    ]
    
    print("Testing feature extraction:\n")
    for url in test_urls:
        f = extract_features(url)
        print(f"URL: {url}")
        print(f"  Length: {f['url_length']}")
        print(f"  Has IP: {f['has_ip']}")
        print(f"  Has HTTPS: {f['has_https']}")
        print(f"  Suspicious words: {f['suspicious_word_count']}")
        print(f"  Suspicious TLD: {f['suspicious_tld']}")
        print(f"  Entropy: {f['url_entropy']:.2f}")
        print()
