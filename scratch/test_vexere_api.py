import httpx

# Vexere public API endpoints for searching trips
url = "https://vexere.com/api/v2/trips"
params = {
    "from": "129",      # Mã Sài Gòn
    "to": "2399",       # Mã Đà Lạt
    "date": "2026-11-05"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://vexere.com/"
}

print("Testing direct API call to Vexere...")
try:
    with httpx.Client(headers=headers, timeout=10.0) as client:
        r = client.get(url, params=params)
        print("Status Code:", r.status_code)
        print("Response sample (first 300 chars):", r.text[:300])
except Exception as e:
    print("Error:", e)
