# bot.py
import asyncio
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from get_nitter_images import get_tweet_images  # <-- 這樣就能用你剛寫的函數

import re

def convert_to_nitter(url: str) -> str:
    """
    將 x.com/twitter.com 的鏈結轉為 nitter.net 鏈結
    """
    for pattern in [r'https?://(?:www\.)?x\.com/(.+)', r'https?://(?:www\.)?twitter\.com/(.+)']:
        m = re.match(pattern, url)
        if m:
            return f'https://nitter.net/{m.group(1)}'
    return url

async def reply_img_links(update, context):
    msg = update.message.text
    import re
    m = re.search(r'https?://[^\s]+', msg)
    # if not m:
    #     await update.message.reply_text("請傳送合法的網址")
    #     return
    url = m.group(0)
    nitter_url = convert_to_nitter(url)
    # await update.message.reply_text("正在抓取圖片網址，請稍候...")
    img_links = await get_tweet_images(nitter_url)  # <-- 直接調用
    # if not img_links:
    #     await update.message.reply_text("找不到任何圖片網址，可能被平台擋住了。")
    #     return
    for link in img_links:
        await update.message.reply_text(link)

def main():
    token = 'TOKEN'
    app = Application.builder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_img_links))
    app.run_polling()

if __name__ == '__main__':
    main()