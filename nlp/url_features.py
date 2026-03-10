import re
from urllib.parse import urlparse
import tldextract

def extract_url_features(url):
    features = {}
    
    # URL Length
    features['URLLength'] = len(url)
    
    # Domain features
    extracted = tldextract.extract(url)
    domain = extracted.domain
    features['DomainLength'] = len(domain)
    
    # Presence of IP address in domain
    ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    features['IsDomainIP'] = 1 if re.search(ip_pattern, domain) else 0
    
    # Placeholder for Similarity Index (In a real system, you'd compare with top 1M domains)
    # For now, let's assume legitimate domains are very dissimilar to common phishing patterns
    features['URLSimilarityIndex'] = 100.0 if any(legit in url.lower() for legit in ['google.com', 'facebook.com', 'microsoft.com', 'amazon.com']) else 0.0
    
    # Char Continuation Rate (Simplified: Ratio of longest alphanumeric sequence to total length)
    sequences = re.findall(r'[a-zA-Z0-9]+', url)
    if sequences:
        features['CharContinuationRate'] = len(max(sequences, key=len)) / len(url)
    else:
        features['CharContinuationRate'] = 0.0
        
    # TLD Legitimate Probability
    common_tlds = ['.com', '.org', '.net', '.edu', '.gov', '.io']
    features['TLDLegitimateProb'] = 0.9 if any(url.lower().endswith(tld) or (tld + '/') in url.lower() for tld in common_tlds) else 0.1

    return features
