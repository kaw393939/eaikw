import asyncio
from playwright.async_api import async_playwright


async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto('http://localhost:8081/is117_ai_test_practice/')
        print('✅ Connected!')
        await browser.close()

asyncio.run(test())
