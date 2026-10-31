import httpx
import re

url = "https://vexere.com/vi-VN/ve-xe-khach-tu-sai-gon-di-da-lat-129t23991.html"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

with httpx.Client(headers=headers, timeout=15.0) as client:
    r = client.get(url)
    scripts = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', r.text)
    print("Found script files count:", len(scripts))
    for s in scripts[:10]:
        print("  -", s)
