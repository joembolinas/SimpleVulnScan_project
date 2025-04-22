import requests
from urllib.parse import urljoin, urlparse

# Basic user agent to identify our scanner
HEADERS = {'User-Agent': 'SimpleVulnScan/0.1'}
TIMEOUT = 10 # seconds

def check_http_headers(headers):
    """Checks for basic security headers."""
    results = {
        'X-Frame-Options': {'present': False, 'value': None, 'pass': False, 'recommendation': 'Set X-Frame-Options to DENY or SAMEORIGIN.'},
        'Strict-Transport-Security': {'present': False, 'value': None, 'pass': False, 'recommendation': 'Implement HSTS to enforce HTTPS.'},
        'Content-Security-Policy': {'present': False, 'value': None, 'pass': False, 'recommendation': 'Implement a strong Content Security Policy.'},
        'X-Content-Type-Options': {'present': False, 'value': None, 'pass': False, 'recommendation': 'Set X-Content-Type-Options to nosniff.'},
        # Add more header checks as needed
    }
    # Case-insensitive check
    headers_lower = {k.lower(): v for k, v in headers.items()}

    if 'x-frame-options' in headers_lower:
        results['X-Frame-Options']['present'] = True
        results['X-Frame-Options']['value'] = headers_lower['x-frame-options']
        # Basic pass condition (can be refined)
        if 'deny' in headers_lower['x-frame-options'].lower() or 'sameorigin' in headers_lower['x-frame-options'].lower():
             results['X-Frame-Options']['pass'] = True

    if 'strict-transport-security' in headers_lower:
        results['Strict-Transport-Security']['present'] = True
        results['Strict-Transport-Security']['value'] = headers_lower['strict-transport-security']
        results['Strict-Transport-Security']['pass'] = True # Presence is often considered a pass for basic checks

    if 'content-security-policy' in headers_lower:
        results['Content-Security-Policy']['present'] = True
        results['Content-Security-Policy']['value'] = headers_lower['content-security-policy']
        results['Content-Security-Policy']['pass'] = True # Presence is a good start

    if 'x-content-type-options' in headers_lower:
        results['X-Content-Type-Options']['present'] = True
        results['X-Content-Type-Options']['value'] = headers_lower['x-content-type-options']
        if 'nosniff' in headers_lower['x-content-type-options'].lower():
             results['X-Content-Type-Options']['pass'] = True

    return results

def check_server_info(headers):
    """Checks for Server header leakage."""
    server_header = headers.get('Server')
    if server_header:
        return {'present': True, 'value': server_header, 'pass': False, 'recommendation': 'Consider removing or obscuring the Server header.'}
    else:
        return {'present': False, 'value': None, 'pass': True, 'recommendation': 'Server header not found (Good).'}

def check_robots_txt(base_url):
    """Checks if robots.txt exists."""
    robots_url = urljoin(base_url, '/robots.txt')
    try:
        response = requests.get(robots_url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        if response.status_code == 200:
            return {'present': True, 'status_code': response.status_code, 'pass': True, 'recommendation': 'robots.txt found. Review its contents for sensitive disallowed paths.'}
        else:
            return {'present': False, 'status_code': response.status_code, 'pass': True, 'recommendation': 'robots.txt not found or inaccessible.'} # Not necessarily a vulnerability
    except requests.exceptions.RequestException as e:
        print(f"Error checking robots.txt: {e}")
        return {'present': False, 'error': str(e), 'pass': False, 'recommendation': 'Could not check robots.txt.'}

def check_sitemap_xml(base_url):
    """Checks if sitemap.xml exists."""
    sitemap_url = urljoin(base_url, '/sitemap.xml')
    try:
        response = requests.get(sitemap_url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        if response.status_code == 200:
            return {'present': True, 'status_code': response.status_code, 'pass': True, 'recommendation': 'sitemap.xml found. Review its contents for listed pages.'}
        else:
            return {'present': False, 'status_code': response.status_code, 'pass': True, 'recommendation': 'sitemap.xml not found or inaccessible.'}
    except requests.exceptions.RequestException as e:
        print(f"Error checking sitemap.xml: {e}")
        return {'present': False, 'error': str(e), 'pass': False, 'recommendation': 'Could not check sitemap.xml.'}

# --- Placeholder for Phase 3 Vulnerability Checks ---
def check_basic_xss(url, response_text):
     """Very basic check for reflected XSS possibilities (highly naive)."""
     # This is extremely basic and prone to false positives/negatives.
     # A real XSS check needs parsing, context analysis, payloads, etc.
     potential_points = 0
     if "<script>" in response_text.lower(): # Very weak indicator
         potential_points += 1
     # Add more sophisticated checks later

     if potential_points > 0:
         return {'vulnerable': True, 'details': 'Potentially vulnerable to basic XSS (found <script> tag in response). Needs manual verification.', 'pass': False, 'recommendation': 'Sanitize user input and encode output correctly. Use Content Security Policy.'}
     else:
         return {'vulnerable': False, 'details': 'No obvious basic XSS patterns found (very limited check).', 'pass': True, 'recommendation': 'Perform thorough XSS testing with specialized tools.'}

def check_basic_idor(url):
     """Placeholder for basic IDOR checks."""
     # Real IDOR checks require understanding application logic, parameter fuzzing, etc.
     return {'vulnerable': None, 'details': 'IDOR check not implemented yet.', 'pass': None, 'recommendation': 'Implement proper authorization checks for all resources.'}
# --- End Placeholder ---


def perform_scan(target_url):
    """Main function to perform all checks."""
    results = {
        'target_url': target_url,
        'scan_status': 'pending',
        'error': None,
        'checks': {}
    }

    # Validate URL format (basic)
    parsed_url = urlparse(target_url)
    if not all([parsed_url.scheme in ['http', 'https'], parsed_url.netloc]):
        results['scan_status'] = 'error'
        results['error'] = 'Invalid URL format. Please include http:// or https://'
        return results

    try:
        response = requests.get(target_url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        results['scan_status'] = 'completed'
        results['checks']['http_headers'] = check_http_headers(response.headers)
        results['checks']['server_info'] = check_server_info(response.headers)
        results['checks']['robots_txt'] = check_robots_txt(target_url)
        results['checks']['sitemap_xml'] = check_sitemap_xml(target_url)

        # Basic Vuln Checks (Phase 1/3 placeholder) - Add response text if needed
        # For more advanced checks, you might need to parse HTML (e.g., with BeautifulSoup)
        # response_text = response.text
        # results['checks']['basic_xss'] = check_basic_xss(target_url, response_text)
        # results['checks']['basic_idor'] = check_basic_idor(target_url)


    except requests.exceptions.Timeout:
        results['scan_status'] = 'error'
        results['error'] = f"Request timed out after {TIMEOUT} seconds."
    except requests.exceptions.RequestException as e:
        results['scan_status'] = 'error'
        results['error'] = f"An error occurred: {e}"
    except Exception as e:
        results['scan_status'] = 'error'
        results['error'] = f"An unexpected error occurred: {e}"

    return results