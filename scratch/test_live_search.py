import asyncio
import json
from playwright.async_api import async_playwright

async def inspect_vexere_live_search():
    print("Khởi chạy Chrome để thực hiện tra cứu trực tiếp trên Vexere...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=True
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        trips_api_data = []

        async def handle_response(response):
            url = response.url
            # Bắt các endpoint trả lời kết quả tìm kiếm chuyến xe
            if any(k in url.lower() for k in ["trip", "search", "graphql", "booking"]):
                ct = response.headers.get("content-type", "")
                if "application/json" in ct:
                    try:
                        res_json = await response.json()
                        trips_api_data.append({"url": url, "data": res_json})
                        print(f"--> Bắt được API JSON: {url[:80]}...")
                    except Exception:
                        pass

        page.on("response", handle_response)

        # Mở trang tìm kiếm vé Sài Gòn -> Đà Lạt
        search_url = "https://vexere.com/vi-VN/ve-xe-khach-tu-sai-gon-di-da-lat-129t23991.html?date=05-11-2026"
        print(f"Đang truy cập: {search_url}")
        await page.goto(search_url, wait_until="domcontentloaded", timeout=25000)
        await page.wait_for_timeout(4000)

        # Thu thập thông tin các chuyến xe đang hiển thị trên màn hình
        trip_elements = await page.eval_on_selector_all(
            "[class*='TripCard'], [class*='ticket-card'], [class*='OperatorCard'], div[data-testid*='trip']",
            """elements => elements.slice(0, 5).map(el => {
                return {
                    text: el.innerText.split('\\n').filter(s => s.trim().length > 0).slice(0, 8)
                };
            })"""
        )

        print(f"\nKẾT QUẢ THỰC TẾ: Bắt được {len(trip_elements)} chuyến xe trực tiếp!")
        for idx, t in enumerate(trip_elements):
            print(f"Chuyến {idx+1}: {t['text']}")

        await browser.close()
        return trips_api_data

if __name__ == "__main__":
    asyncio.run(inspect_vexere_live_search())
