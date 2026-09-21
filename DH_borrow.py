from playwright.sync_api import sync_playwright
import time
import datetime
import ddddocr  
import re       # 新增：用於強制淨化 AI 產生的中文字或符號
import os                         # 新增：用來讀取系統環境變數
from dotenv import load_dotenv    # 新增：用來載入 .env 檔案

# 載入 .env 檔案
load_dotenv()

# ======================================================
# 🎯 搶場地專用設定區
# ======================================================

# 1. 帳號與密碼
USER_ID = os.getenv("STUDENT_ID")       # 你的學號
PASSWORD = os.getenv("SYSTEM_PASSWORD") # 你的系統密碼

# 2. 場地與時間設定
VENUE_TYPE = "戶外大型球場"         # 類型(kinds)，例如："體育館" 或 "戶外大型球場"
VENUE_NAME = "BSK02高爾夫球場"      # 場地(Fields)，例如："XGMB1壽館場B-羽1"
TARGET_DATE = "2026/09/29"         # 欲借用的日期，格式：YYYY/MM/DD
TARGET_SLOT = "06~08"              # 欲借用的時段，例如："06~08" 或 "21~22"
SLOT_INDEX = 0

# 3. 借用原因
BOOKING_REASON = "1"               # 借用原因，例如："1" 

# 4. 定時開搶設定 (請設定為未來的時間來測試等待效果)
# 格式：datetime.datetime(年, 月, 日, 時, 分, 秒)
OPEN_TIME = datetime.datetime(2026, 9, 20, 00, 00, 0) # <--- 記得改成你現在時間的往後 1~2 分鐘

# ======================================================
# 以下為機器人運作邏輯
# ======================================================

def run():
    print("載入 ddddocr 進階辨識模型...")
    # 使用 beta=True 提高對扭曲字母的辨識率
    ocr = ddddocr.DdddOcr(beta=True, show_ad=False)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("前往學校登入網站...")
        page.goto("https://sys.ndhu.edu.tw/gc/sportcenter/SportsFields/login.aspx")

        print("填寫帳號與密碼...")
        page.locator("#MainContent_TxtUSERNO").fill(USER_ID)
        page.locator("#MainContent_TxtPWD").fill(PASSWORD) 
        
        print("點擊登入...")
        page.locator("#MainContent_Button1").click()

        print("點擊「新增申請」按鈕...")
        page.locator("#MainContent_Button2").click()
        
        print(f"選擇類型為 {VENUE_TYPE}...")
        page.locator("#MainContent_drpkind").select_option(label=VENUE_TYPE)
        time.sleep(1) 
        
        print(f"選擇場地為 {VENUE_NAME}...")
        page.locator("#MainContent_DropDownList1").select_option(label=VENUE_NAME)
        time.sleep(1) 

        print(f"強制填入借用日期為 {TARGET_DATE}...")
        page.evaluate(f"document.getElementById('MainContent_TextBox1').value = '{TARGET_DATE}'")
        
        # ==================== 倒數計時啟動 ====================
        print(f"進入倒數計時，等待時間到達 {OPEN_TIME} ...")
        while datetime.datetime.now() < OPEN_TIME:
            time.sleep(0.05) 
        # ======================================================
            
        print("點擊查詢按鈕...")
        page.locator("#MainContent_Button1").click()
        time.sleep(0.5) 

        print(f"點擊 [{TARGET_SLOT}] 的第 {SLOT_INDEX + 1} 個申請按鈕...") 
        page.locator(f"button:has-text('{TARGET_SLOT}')").nth(SLOT_INDEX).click()

        # ==================== 自動辨識與暴力重試機制 ====================
        print("等待驗證碼視窗彈出...")
        page.locator("#imgCaptcha").wait_for()

        captcha_text = ""
        # 條件：長度必須剛好 5 碼，且不可以包含 '0' 或 'O'
        while len(captcha_text) != 5 or '0' in captcha_text or 'O' in captcha_text:
            
            print("截取驗證碼圖片並交給 AI 辨識...")
            captcha_image_bytes = page.locator("#imgCaptcha").screenshot()
            
            raw_text = ocr.classification(captcha_image_bytes)
            
            # 強制淨化：轉大寫，並把所有「非英文與數字」的字元(含中文)直接刪除
            captcha_text = re.sub(r'[^A-Z0-9]', '', raw_text.upper())
            
            print(f"AI 原始結果：[{raw_text}] ➔ 淨化後：[{captcha_text}]")

            if len(captcha_text) != 5 or '0' in captcha_text or 'O' in captcha_text:
                print("觸發淘汰機制，點擊「換一張」重新挑戰...")
                page.locator("button:has-text('換一張')").click()
                time.sleep(0.5) # 給系統 0.5 秒載入新圖片

        print(f"✅ 成功獲得完美 5 碼 [{captcha_text}]，填入輸入框！")
        page.locator("#txtCaptchaValue").fill(captcha_text)

        print("點擊彈出視窗內的「申請」送出按鈕...")
        page.locator(".modal button:has-text('申請')").click()
        # ==============================================================

        print("等待回到主頁面...")
        time.sleep(0.5) 

        print(f"填寫借用原因為 '{BOOKING_REASON}'...")
        page.locator("#MainContent_ReasonTextBox1").fill(BOOKING_REASON)

        print("準備點擊確定按鈕 (目前為測試模式，已取消實際點擊)...")
        # 實戰時請把下面這行最前面的 # 刪掉
        # page.locator("#MainContent_Button4").click()

        print("自動化操作完成！")
        input("請在終端機按下 Enter 鍵來結束程式並關閉瀏覽器...")

if __name__ == "__main__":
    run()