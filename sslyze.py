import subprocess
import requests
from urllib.parse import urlparse

def check_ssl(domain):
    result = subprocess.run(['sslyze', '--regular', domain], capture_output=True, text=True)
    return result.stdout

def check_security_headers(url):
    response = requests.get(url)
    headers = response.headers

    security_headers = {
        'Content-Security-Policy': headers.get('Content-Security-Policy', 'Missing'),
        'Strict-Transport-Security': headers.get('Strict-Transport-Security', 'Missing'),
        'X-Content-Type-Options': headers.get('X-Content-Type-Options', 'Missing'),
        'X-Frame-Options': headers.get('X-Frame-Options', 'Missing'),
        'X-XSS-Protection': headers.get('X-XSS-Protection', 'Missing'),
        'Referrer-Policy': headers.get('Referrer-Policy', 'Missing'),
        'Permissions-Policy': headers.get('Permissions-Policy', 'Missing'),
        'Expect-CT': headers.get('Expect-CT', 'Missing')
    }

    return security_headers

def main():
    url = 'https://aveda.ee'
    domain = urlparse(url).netloc

    # Check SSL
    print("Checking SSL for:", domain)
    ssl_report = check_ssl(domain)
    print(ssl_report)

    # Check Security Headers
    print("Checking Security Headers for:", url)
    security_headers = check_security_headers(url)
    for header, value in security_headers.items():
        print(f"{header}: {value}")

if __name__ == "__main__":
    main()
