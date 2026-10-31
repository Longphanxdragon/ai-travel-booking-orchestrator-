import asyncio
from playwright.async_api import async_playwright

async def dump_clean_text():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=True
        )
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        url = "https://vexere.com/vi-VN/ve-xe-khach-tu-sai-gon-di-da-lat-129t23991.html"
        await page.goto(url, wait_until="domcontentloaded", timeout=20000)
        await page.wait_for_timeout(3000)

        # Lấy các thẻ chứa từ khóa "Limousine" hoặc "giường nằm" hoặc "khởi hành"
        paragraphs = await page.eval_on_selector_all(
            "p, div, li",
            """nodes => nodes
                .map(n => n.innerText ? n.innerText.trim() : '')
                .filter(t => t.includes('khởi hành') || t.includes('Limousine') || t.includes('giường nằm') || t.includes('chuyến'))
                .slice(0, 15)
            """
        )
        print(f"Bắt được {len(paragraphs)} đoạn thông tin xe thực tế:")
        for idx, p_text in enumerate(set(paragraphs)):
            print(f"--- [Dữ liệu {idx+1}] ---")
            print(p_text[:200])

        await browser.close()

if __name__ == "__main__":
    asyncio.run(dump_clean_text())
