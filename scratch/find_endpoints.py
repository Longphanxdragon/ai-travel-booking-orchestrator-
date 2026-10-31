import httpx
import re

url = "https://vexere.com/vi-VN/ve-xe-khach-tu-sai-gon-di-da-lat-129t23991.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

with httpx.Client(headers=headers, timeout=15.0) as client:
    r = client.get(url)
    
    # Search for all script tags or API endpoints
    apis = re.findall(r'["\'](https?://[^"\']*/api/[^"\']*)["\']', r.text)
    print("Found absolute APIs:", set(apis))
    
    rel_apis = re.findall(r'["\'](/api/[^"\']*)["\']', r.text)
    print("Found relative APIs:", set(rel_apis))
    
    # Also find GraphQL endpoints
    gql = re.findall(r'["\'](/graphql[^"\']*)["\']', r.text)
    print("Found GraphQL endpoints:", set(gql))
