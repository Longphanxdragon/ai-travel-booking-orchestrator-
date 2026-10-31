import asyncio
import json
from playwright.async_api import async_playwright

async def inspect_vexere_with_installed_chrome():
    print("Launching Local Chrome...")
    async with async_playwright() as p:
        # Dùng trực tiếp Google Chrome có sẵn trên máy của bạn
        browser = await p.chromium.launch(
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=True
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        api_results = []

        async def on_response(response):
            url = response.url
            ct = response.headers.get("content-type", "")
            if "application/json" in ct and ("trip" in url.lower() or "search" in url.lower() or "api" in url.lower()):
                try:
                    data = await response.json()
                    api_results.append({"url": url, "data": data})
                    print(f"\n🎯 [FOUND LIVE API]: {url}")
                except Exception:
                    pass

        page.on("response", on_response)

        target_url = "https://vexere.com/vi-VN/ve-xe-khach-tu-sai-gon-di-da-lat-129t23991.html"
        print(f"Opening {target_url}...")
        try:
            await page.goto(target_url, wait_until="networkidle", timeout=30000)
        except Exception as e:
            print(f"Page load note: {e}")

        # Thử lấy danh sách chuyến xe trực tiếp từ DOM nếu API bị ẩn
        cards = await page.query_selector_all(".ticket-card, [class*='TicketItem'], [class*='trip-card']")
        print(f"\n🚌 Tìm thấy {len(cards)} thẻ vé xe trên giao diện HTML thực tế!")

        await browser.close()
        return api_results

if __name__ == "__main__":
    asyncio.run(inspect_vexere_with_installed_chrome())
