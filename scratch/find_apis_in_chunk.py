import httpx
import re

bundle_url = "https://229a2c9fe669f7b.cmccloud.com.vn/_next/static/chunks/8e67749e34e28057d0a9283dd52765d62a52ebc1.87f8c096365014bfbfbf.js"
with httpx.Client(timeout=10.0) as client:
    r = client.get(bundle_url)
    apis = re.findall(r'["\'](https?://[^"\']*/[^"\']*)["\']', r.text)
    candidate_apis = [a for a in apis if "api" in a or "trip" in a]
    print("Found candidate APIs in chunk:", candidate_apis[:10])
