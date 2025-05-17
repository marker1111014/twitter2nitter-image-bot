# Nitter 圖片連結 Telegram Bot

本專案是一個 Telegram 聊天機器人，當使用者傳送 x.com 或 twitter.com 的推文網址時，會自動將其轉為 nitter.net 對應網址，然後自動抓取該推文的所有圖片連結並回傳給用戶。

## 功能特色

- 支援 x.com 與 twitter.com 連結自動轉換為 nitter.net。
- 自動抓取推文內的所有圖片連結。
- 圖片網址自動回覆到 Telegram 聊天視窗。

## 專案結構

```
your-project/
│
├─ bot.py                # Telegram 主程式
├─ get_nitter_images.py  # 負責解析 nitter 頁面、提取圖片
└─ README.md
```

## 安裝與環境

請先安裝必要的 Python 套件：

```bash
pip install python-telegram-bot playwright
```

第一次使用前需下載 Playwright 的瀏覽器引擎：

```bash
playwright install
```

## 使用方式

1. 編輯 `bot.py` 裡的 `token` 變數，換成你自己的 Telegram Bot Token。
2. 執行主程式：

```bash
python bot.py
```

3. 在 Telegram 上搜尋並傳訊息給你的機器人，發送任一 x.com 或 twitter.com 推文網址，機器人會自動回覆圖片連結。

## 主要檔案簡介

### bot.py

- 監聽所有文字訊息
- 自動把收到的推文網址 (x.com / twitter.com) 轉成 nitter.net 網址
- 調用 `get_nitter_images.py` 取得所有圖片網址，逐一回覆

### get_nitter_images.py

- 使用 Playwright 自動瀏覽 nitter 推文頁
- 抓取所有推文圖片的直接連結並返回

## 注意事項

- 若你想回傳圖片本身，請再擴充 bot 回傳 `photo` 而不只是圖片網址。
- 由於使用自動瀏覽器進行爬取，請確認伺服器具有可用的 Chromium 或適當瀏覽器環境。
- Nitter 服務可用性視公開服務或私有部署而定，若遇服務不穩可能導致抓取失敗。

## 授權

MIT License

---

如需擴展功能（如支持發送多媒體或其他推文內容），可進一步修改本專案原始碼。欢迎提出 Issue 或 Pull Request！
