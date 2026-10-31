import httpx
import json
import re

url = "https://vexere.com/vi-VN/ve-xe-khach-tu-sai-gon-di-da-lat-129t23991.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7"
}

print(f"Connecting to {url}...")
with httpx.Client(headers=headers, timeout=15.0, follow_redirects=True) as client:
    r = client.get(url)
    print(f"Status Code: {r.status_code}")
    
    match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', r.text)
    if match:
        data = json.loads(match.group(1))
        page_props = data.get("props", {}).get("pageProps", {})
        print("Found pageProps keys:", list(page_props.keys()))
        
        # Look for search results / trips
        initial_state = page_props.get("initialState", {})
        if initial_state:
            print("initialState keys:", list(initial_state.keys()))
            
        # Check seo or schema data
        schema = page_props.get("schemaData") or page_props.get("seoData")
        if schema:
            print("Schema/SEO sample:", str(schema)[:200])
    else:
        print("Could not find __NEXT_DATA__ script tag.")
