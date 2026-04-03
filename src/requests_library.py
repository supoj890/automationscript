import requests

def monitor_fleet(endpoints):
    report = {}
    
    for name, url in endpoints.items():
        # 1. Outer try/except to catch network-level failures
        try:
            # 2. Make the request with a strict 5-second timeout
            response = requests.get(url, timeout=5)
            
            # 3. Check the status code first
            if response.status_code != 200:
                report[name] = f"HTTP {response.status_code}"
            else:
                # 4. Inner try/except to handle the data parsing
                try:
                    # Attempt to parse as an API (JSON)
                    data = response.json()
                    # Grab the status key. Using .get() for extra safety!
                    report[name] = data.get("status", "Unknown API Status")
                except ValueError:
                    # If .json() throws a ValueError, it's just a regular webpage returning HTML
                    report[name] = "Online"
                    
        except requests.exceptions.RequestException:
            # Catches ConnectionErrors, Timeouts, MissingSchema, etc.
            report[name] = "Connection Failed"
            
    return report

# --- Test Data ---
target_endpoints = {
    "Google": "https://www.google.com",                  # Standard site -> "Online"
    "GitHub API": "https://api.github.com",              # Real API -> JSON parsing attempt
    "Bad URL": "https://this-site-does-not-exist.com",   # Fake URL -> "Connection Failed"
    "HTTP 404 Test": "https://httpstat.us/404"           # 404 Site -> "HTTP 404"
}

print(monitor_fleet(target_endpoints))