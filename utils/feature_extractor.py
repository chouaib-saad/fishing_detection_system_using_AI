import re
import urllib.parse
import tldextract

def extract_features(url):
    """
    Extract features from a URL for phishing detection.
    Returns a dictionary of features used by the ML model.
    """
    features = {}
    
    try:
        # Basic URL length
        features['url_length'] = len(url)
        
        # Check if URL contains IP address instead of domain
        ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
        features['has_ip'] = 1 if ip_pattern.search(url) else 0
        
        # Check for @ symbol (often used in phishing)
        features['has_at_symbol'] = 1 if '@' in url else 0
        
        # Check for dashes in domain (suspicious pattern)
        features['has_dash'] = 1 if '-' in url else 0
        
        # Check if HTTPS is used
        features['is_https'] = 1 if url.startswith('https://') else 0
        
        # Count subdomains
        try:
            parsed = tldextract.extract(url)
            subdomains = parsed.subdomain.split('.') if parsed.subdomain else []
            features['subdomain_count'] = len([s for s in subdomains if s])
        except:
            features['subdomain_count'] = 0
        
        # Additional suspicious patterns
        features['has_suspicious_tld'] = 1 if any(tld in url.lower() for tld in ['.tk', '.ml', '.ga', '.cf']) else 0
        features['has_url_shortener'] = 1 if any(shortener in url.lower() for shortener in ['bit.ly', 'tinyurl', 't.co', 'goo.gl']) else 0
        features['has_suspicious_keywords'] = 1 if any(keyword in url.lower() for keyword in ['secure', 'account', 'update', 'confirm', 'login', 'verify']) else 0
        
        # Count dots (indication of complex subdomain structure)
        features['dot_count'] = url.count('.')
        
        # Check for suspicious characters
        features['has_suspicious_chars'] = 1 if any(char in url for char in ['%', '&', '=', '?', '#']) else 0
        
    except Exception as e:
        # If any feature extraction fails, set default values
        print(f"Error extracting features: {e}")
        features = {
            'url_length': len(url) if url else 0,
            'has_ip': 0,
            'has_at_symbol': 0,
            'has_dash': 0,
            'is_https': 0,
            'subdomain_count': 0,
            'has_suspicious_tld': 0,
            'has_url_shortener': 0,
            'has_suspicious_keywords': 0,
            'dot_count': 0,
            'has_suspicious_chars': 0
        }
    
    return features
