import asyncio  # 這行是拿來用「非同步」功能的，想像你同時在等很多事情發生
from playwright.async_api import async_playwright  # 這行是叫 Playwright 這個自動開瀏覽器的工具

# 這段像是在寫一個食譜：如果給我一個網址，我來幫你找出裡面的圖片
async def get_tweet_images(url):
    # 開啟一個自動操控的瀏覽器（Playwright幫你處理，像是叫醒一台自動機械手）
    async with async_playwright() as p:
        # 啟動一個chrome瀏覽器（headless=False是讓你看得到這個瀏覽器，像真的一樣在你螢幕跑）
        browser = await p.chromium.launch(headless=False)
        # 打開一個新的網頁分頁
        page = await browser.new_page()
        # 冒充一個正常的使用者，不要像機器人一樣去逛網站
        await page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/114.0.5735.199 Safari/537.36"
        })
        # 叫分頁去打開你指定的那個網址（等到網頁大致載入完再繼續）
        await page.goto(url, wait_until="networkidle")
        try:
            # 接著等「圖片」出現，最久等20秒（Selector就像你用 Ctrl+F 搜尋那個字，這裡就是找src裡有media的img）
            await page.wait_for_selector('img[src*="media"]', timeout=20000)
        except Exception as e:
            # 如果20秒還找不到圖片，來這裡印出錯誤跟網頁內容給你debug
            print("等待圖片時發生錯誤:", e)
            print(await page.content())
            await browser.close()
            return []
        # 如果順利找到圖片，把網頁裡指定的圖片都「找到」
        imgs = await page.query_selector_all('img[src*="media"]')
        img_links = []  # 開一個袋子，等下把圖片網址一個個丟進去
        for img in imgs:
            # 拿圖片的連結出來
            src = await img.get_attribute("src")
            # 如果這個網址開頭是/，要自己補「主網址」才變成有效的 https 網址
            if src.startswith('/'):
                src = 'https://nitter.net' + src
            img_links.append(src)  # 丟進清單
        await browser.close()  # 順利抓完，都做好就把分頁和瀏覽器關掉
        return img_links  # 回傳「所有抓到的圖片網址」

