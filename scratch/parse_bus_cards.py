import asyncio
from playwright.async_api import async_playwright

async def parse_vexere_bus_cards():
    print("Truy cập VeXeRe để bóc tách thông tin chuyến xe thực tế...")
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

        # Lấy thông tin các nhà xe được hiển thị
        data = await page.evaluate('''() => {
            const results = [];
            // Tìm tất cả các khối có tên nhà xe và thông tin chuyến
            const elements = document.querySelectorAll("div");
            for (let el of elements) {
                const text = el.innerText || "";
                if (text.includes("Limousine") && text.includes("Đà Lạt") && text.includes("đánh giá") && text.length < 500) {
                    const lines = text.split("\\n").map(s => s.trim()).filter(s => s.length > 0);
                    if (lines.length >= 4) {
                        results.push(lines);
                    }
                }
            }
            return results;
        }''')

        print(f"--> Bóc tách thành công {len(data)} khối dữ liệu xe khách từ VeXeRe!")
        unique_samples = []
        for item in data:
            item_str = " | ".join(item[:6])
            if item_str not in unique_samples:
                unique_samples.append(item_str)

        for idx, s in enumerate(unique_samples[:5]):
            print(f"Nhà xe {idx+1}: {s}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(parse_vexere_bus_cards())
