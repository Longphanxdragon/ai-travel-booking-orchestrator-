import asyncio
from playwright.async_api import async_playwright

async def test_vexere_dom():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=True
        )
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        captured_apis = []
        page.on("response", lambda r: captured_apis.append(r.url) if "api" in r.url.lower() or "trip" in r.url.lower() else None)

        url = "https://vexere.com/vi-VN/ve-xe-khach-tu-sai-gon-di-da-lat-129t23991.html"
        await page.goto(url, wait_until="domcontentloaded", timeout=20000)
        await page.wait_for_timeout(5000)

        # Print all captured APIs
        print("Captured API count:", len(captured_apis))
        for api in list(set(captured_apis))[:10]:
            print("  API:", api)

        # Extract bus operators
        operators = await page.eval_on_selector_all(
            "[class*='operator-name'], [class*='OperatorName'], [class*='title'], h2, h3",
            "elements => elements.slice(0, 15).map(e => e.innerText.trim()).filter(t => t.length > 0)"
        )
        print("Extracted text elements count:", len(operators))
        for op in operators[:10]:
            print("  Text:", repr(op))

        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_vexere_dom())
