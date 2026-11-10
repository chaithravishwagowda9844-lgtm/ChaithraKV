
import requests
from urllib.parse import urlparse
import ipaddress
import socket

SECURITY_HEADERS = {
    "Strict-Transport-Security": {
        "description": "Enforces secure HTTPS connections."
    },
    "Content-Security-Policy": {
        "description": "Helps prevent cross-site scripting attacks."
    },
    "X-Content-Type-Options": {
        "description": "Prevents MIME type sniffing."
    },
    "X-Frame-Options": {
        "description": "Helps prevent clickjacking attacks."
    },
    "Referrer-Policy": {
        "description": "Controls referrer information."
    },
    "Permissions-Policy": {
        "description": "Controls browser features and permissions."
    }
}


def validate_url(url):
    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    if not parsed.hostname or parsed.scheme not in ("http", "https"):
        raise ValueError("Please enter a valid website URL.")

    if parsed.username or parsed.password:
        raise ValueError("URLs containing login credentials are not allowed.")

    hostname = parsed.hostname

    if hostname.lower() == "localhost":
        raise ValueError("Localhost URLs cannot be scanned.")

    try:
        addresses = socket.getaddrinfo(hostname, None)
        for address in addresses:
            ip = ipaddress.ip_address(address[4][0])
            if not ip.is_global:
                raise ValueError("Private or local IP addresses cannot be scanned.")
    except socket.gaierror:
        raise ValueError("Website address could not be found.")

    return url


def scan_website(url):

    url = validate_url(url)

    response = requests.get(
        url,
        timeout=15,
        allow_redirects=True,
        headers={"User-Agent": "WebsiteSecurityChecker/1.0"}
    )

    headers = response.headers

    results = []

    for header, details in SECURITY_HEADERS.items():

        if header in headers:
            results.append({
                "name": header,
                "status": "Present",
                "value": headers[header],
                "description": details["description"]
            })

        else:
            results.append({
                "name": header,
                "status": "Missing",
                "value": "Not Found",
                "description": details["description"]
            })

    present = sum(
        1 for item in results if item["status"] == "Present"
    )

    total = len(SECURITY_HEADERS)
    score = round((present / total) * 100)

    recommendations = [
        {
            "name": item["name"],
            "message": "Add this security header to improve website protection."
        }
        for item in results if item["status"] == "Missing"
    ]

    if response.url.startswith("https://"):
        https_status = "Secure HTTPS connection"
    else:
        https_status = "Website is not using HTTPS"

    return {
        "url": url,
        "final_url": response.url,
        "status_code": response.status_code,
        "score": score,
        "present": present,
        "missing": total - present,
        "total": total,
        "headers": results,
        "recommendations": recommendations,
        "https_status": https_status
    }
