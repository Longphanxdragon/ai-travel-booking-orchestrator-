import asyncio
import json
from playwright.async_api import async_playwright

async def inspect_vexere_network():
    print("Launching Chromium...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        api_calls = []

        # Intercept network requests & responses
        async def on_response(response):
            url = response.url
            if any(keyword in url.lower() for keyword in ["api", "graphql", "trip", "search"]):
                ct = response.headers.get("content-type", "")
                if "application/json" in ct:
                    try:
                        data = await response.json()
                        api_calls.append({"url": url, "sample": str(data)[:300]})
                        print(f"\n[FOUND API] {url}")
                        print(f"Sample data: {str(data)[:200]}")
                    except Exception:
                        pass

        page.on("response", on_response)

        target_url = "https://vexere.com/vi-VN/ve-xe-khach-tu-sai-gon-di-da-lat-129t23991.html"
        print(f"Navigating to {target_url}...")
        try:
            await page.goto(target_url, wait_until="networkidle", timeout=30000)
            print(f"Page loaded. Total JSON APIs captured: {len(api_calls)}")
        except Exception as e:
            print(f"Navigation note: {e}")
            print(f"Captured APIs so far: {len(api_calls)}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(inspect_vexere_network())
