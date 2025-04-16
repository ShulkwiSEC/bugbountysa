from urllib.parse import urlparse
import re

def clean_domain(url):
    """Clean and normalize domain/URL"""
    # Remove any whitespace
    url = url.strip()
    
    # If it doesn't start with http/https, add https://
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
        
    # Parse the URL
    parsed = urlparse(url)
    domain = parsed.netloc
    
    # If domain is empty, try using the path (some URLs might be malformed)
    if not domain and parsed.path:
        domain = parsed.path
    
    # Remove www. prefix if present
    domain = re.sub(r'^www\.', '', domain)
    
    # Remove trailing slashes
    domain = domain.rstrip('/')
    
    return domain

def extract_domains(scope):
    """Extract and clean domains from scope"""
    if not scope or 'data' not in scope or 'domains' not in scope['data']:
        return []
        
    domains = []
    seen = set()  # To prevent duplicates
    
    for domain_obj in scope['data']['domains']:
        if 'domain' not in domain_obj:
            continue
            
        domain = domain_obj['domain']
        if domain:
            cleaned = clean_domain(domain)
            if cleaned and cleaned not in seen:
                domains.append(cleaned)
                seen.add(cleaned)
                
    return sorted(domains)  # Sort domains for consistent output