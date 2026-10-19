import requests
import socket
import re
import tldextract
import whois
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from difflib import SequenceMatcher
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

KNOWN_BRANDS = [
    'google', 'microsoft', 'apple', 'amazon', 'paypal',
    'facebook', 'twitter', 'instagram', 'netflix', 'ebay',
    'linkedin', 'dropbox', 'github', 'yahoo', 'gmail'
]

SHORTENING_SERVICES = [
    'bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly',
    'buff.ly', 'adf.ly', 'bit.do', 'cutt.ly'
]

SUSPICIOUS_TLDS = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.work']

PHISHING_KEYWORDS = ['login', 'verify', 'secure', 'account', 'update',
                     'banking', 'confirm', 'password', 'signin', 'webscr',
                     'ebayisapi', 'payment']

HEADERS = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

def is_ip_address(hostname):
    try:
        socket.inet_aton(hostname)
        return 1
    except:
        return 0

def brand_similarity_score(domain):
    domain_clean = domain.replace('www', '').split('.')[0].lower()
    max_sim = 0
    for brand in KNOWN_BRANDS:
        if domain_clean == brand:
            return 0.0
        sim = SequenceMatcher(None, domain_clean, brand).ratio()
        max_sim = max(max_sim, sim)
    return round(max_sim, 3)

def extract_lexical_features(url):
    try:
        parsed = urlparse(url)
        ext = tldextract.extract(url)
        hostname = parsed.hostname or ""
        path = parsed.path or ""
        full_url = url.lower()

        return {
            "url_length": len(url),
            "hostname_length": len(hostname),
            "nb_dots": url.count('.'),
            "nb_hyphens": url.count('-'),
            "nb_slash": url.count('/'),
            "nb_at": url.count('@'),
            "nb_qmark": url.count('?'),
            "nb_equal": url.count('='),
            "nb_underscore": url.count('_'),
            "nb_percent": url.count('%'),
            "nb_digits": sum(c.isdigit() for c in url),
            "ratio_digits_url": sum(c.isdigit() for c in url) / max(len(url), 1),
            "ratio_digits_host": sum(c.isdigit() for c in hostname) / max(len(hostname), 1),
            "https_token": 1 if parsed.scheme == 'https' else 0,
            "ip_in_hostname": is_ip_address(hostname),
            "nb_subdomains": len(ext.subdomain.split('.')) if ext.subdomain else 0,
            "prefix_suffix": 1 if '-' in ext.domain else 0,
            "suspicious_tld": 1 if any(url.endswith(tld) or f"{tld}/" in url for tld in SUSPICIOUS_TLDS) else 0,
            "shortening_service": 1 if any(s in hostname for s in SHORTENING_SERVICES) else 0,
            "phishing_hints": 1 if any(kw in full_url for kw in PHISHING_KEYWORDS) else 0,
            "brand_similarity": brand_similarity_score(ext.domain),
            "path_length": len(path),
            "has_port": 1 if parsed.port else 0,
            "double_slash_in_path": 1 if '//' in path else 0,
        }
    except:
        return {}

def extract_whois_features(url):
    return {
        "dns_record": 0
    }

def extract_webpage_features(url):
    default = {
        "nb_hyperlinks": 0, "ratio_internal_links": 0,
        "nb_external_css": 0, "has_login_form": 0,
        "has_iframe": 0, "external_favicon": 0,
        "title_matches_domain": 0
    }
    try:
        response = requests.get(url, timeout=5, headers=HEADERS, allow_redirects=True)
        soup = BeautifulSoup(response.text, "html.parser")
        ext = tldextract.extract(url)
        base_domain = f"{ext.domain}.{ext.suffix}"

        all_links = soup.find_all("a", href=True)
        nb_links = len(all_links)
        internal = sum(1 for a in all_links if base_domain in a["href"] or a["href"].startswith('/'))
        ratio_internal = internal / max(nb_links, 1)

        css_links = soup.find_all("link", rel=lambda r: r and "stylesheet" in r)
        external_css = sum(1 for l in css_links if l.get("href") and base_domain not in l.get("href", ""))

        inputs = soup.find_all("input")
        has_login = 1 if any(i.get("type") == "password" for i in inputs) else 0

        has_iframe = 1 if soup.find("iframe") else 0

        favicon = soup.find("link", rel=lambda r: r and "icon" in r)
        ext_favicon = 0
        if favicon and favicon.get("href"):
            ext_favicon = 1 if (favicon["href"].startswith("http") and base_domain not in favicon["href"]) else 0

        title = soup.title.string if soup.title else ""
        title_match = 1 if (title and ext.domain.lower() in title.lower()) else 0

        return {
            "nb_hyperlinks": nb_links,
            "ratio_internal_links": round(ratio_internal, 3),
            "nb_external_css": external_css,
            "has_login_form": has_login,
            "has_iframe": has_iframe,
            "external_favicon": ext_favicon,
            "title_matches_domain": title_match
        }
    except:
        return default

def extract_all_features(url, label=0):
    features = {"url": url, "label": label}
    features.update(extract_lexical_features(url))
    features.update(extract_whois_features(url))
    features.update(extract_webpage_features(url))
    return features