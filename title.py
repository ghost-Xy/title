import asyncio
from playwright.async_api import async_playwright
import socket
from urllib.parse import urlparse

async def get_title(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # 无头模式
        page = await browser.new_page()

        try:
            # 访问网页
            await page.goto(url)

            # 获取页面标题
            title = await page.title()

            # 获取网站的 IP 地址
            ip_address = socket.gethostbyname(urlparse(url).hostname)

            return f"{url}--------{title}--------{ip_address}\n"
        
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
        
        finally:
            await browser.close()

async def main():
    with open('urls.txt', 'r') as f:
        urls = f.readlines()

    # 使用 asyncio.gather() 进行并行化处理
    tasks = [get_title(url.strip()) for url in urls]
    results = await asyncio.gather(*tasks)

    # 写入文件
    with open('ok.txt', 'w') as output_file:
        for result in results:
            if result:
                output_file.write(result)

# 执行异步任务
asyncio.run(main())
