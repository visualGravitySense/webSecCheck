import csv
import subprocess
import requests
from urllib.parse import urlparse, urljoin

def check_ssl(domain):
    result = subprocess.run(['sslyze', '--regular', domain], capture_output=True, text=True)
    return result.stdout

def check_security_headers(url):
    try:
        response = requests.get(url, timeout=10)
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
    except requests.RequestException as e:
        print(f"Failed to fetch headers for {url}: {e}")
        return {
            'Content-Security-Policy': 'Error',
            'Strict-Transport-Security': 'Error',
            'X-Content-Type-Options': 'Error',
            'X-Frame-Options': 'Error',
            'X-XSS-Protection': 'Error',
            'Referrer-Policy': 'Error',
            'Permissions-Policy': 'Error',
            'Expect-CT': 'Error'
        }

def process_url(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = urljoin("https://", url)
        parsed_url = urlparse(url)

    domain = parsed_url.netloc

    # Debugging information
    print(f"Parsed URL: {parsed_url.geturl()}")
    print(f"Domain: {domain}")

    if not domain:
        print(f"Invalid URL: {url}")
        return

    # Check SSL
    try:
        ssl_report = check_ssl(domain)
    except subprocess.CalledProcessError as e:
        ssl_report = f"Error running sslyze: {e}"

    # Check Security Headers
    security_headers = check_security_headers(url)

    # Prepare report content
    report_content = f"SSL Report for {domain}:\n{ssl_report}\n\n"
    report_content += f"Security Headers for {url}:\n"
    for header, value in security_headers.items():
        report_content += f"{header}: {value}\n"

    # Save report to file
    report_filename = f"{domain}_report.txt"
    with open(report_filename, 'w') as report_file:
        report_file.write(report_content)

def main():
    csv_filename = 'drive.csv'

    with open(csv_filename, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            url = row[0].strip()
            if url and not url.startswith("#"):
                print(f"Processing URL: {url}")
                process_url(url)

if __name__ == "__main__":
    main()
