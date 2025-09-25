# -*- coding: utf-8 -*-
"""
Script Python นี้จำลองการทำงานของบอท AQW
โดยจะตรวจจับข้อความในเกมและสั่งให้บอทใช้สกิล
"""
import time
import mss
import pytesseract
from PIL import Image

# กำหนดเส้นทางของ Tesseract-OCR
# ถ้าคุณไม่ได้ติดตั้ง Tesseract-OCR หรือติดตั้งไว้คนละที่
# โค้ดส่วนนี้อาจต้องถูกแก้ไขเพื่อให้ทำงานได้
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def use_skill(skill_number):
    """
    ฟังก์ชันนี้จำลองการใช้สกิลในเกม
    ในโปรแกรมจริง จะต้องใช้ไลบรารีหรือ API ที่สามารถ
    สั่งให้เกมใช้สกิลตามหมายเลขที่ระบุ
    """
    print(f"Executing skill {skill_number}.")
    # ตัวอย่างการทำงานในโลกจริง:
    # bot_api.send_command(f"useskill {skill_number}")

def read_screen_text():
    """
    ฟังก์ชันนี้ใช้ mss เพื่อจับภาพหน้าจอ และ pytesseract เพื่อแปลงภาพเป็นข้อความ
    หมายเหตุ: นี่คือโค้ดตัวอย่างที่ใช้ได้จริง แต่ต้องติดตั้งไลบรารีและ Tesseract-OCR ก่อน
    """
    # กำหนดพื้นที่บนหน้าจอที่ต้องการตรวจจับข้อความ
    # คุณต้องปรับค่าเหล่านี้ให้ตรงกับตำแหน่งแชทในหน้าจอเกมของคุณ
    monitor = {"top": 800, "left": 600, "width": 400, "height": 100}

    with mss.mss() as sct:
        # จับภาพหน้าจอในพื้นที่ที่กำหนด
        screenshot = sct.grab(monitor)
        
        # แปลงภาพที่ได้จาก mss ให้เป็นภาพที่สามารถใช้งานกับ pytesseract ได้
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        
        # ใช้ pytesseract เพื่อแปลงภาพเป็นข้อความ
        text = pytesseract.image_to_string(img)
        
        return text.strip()

# --- โปรแกรมหลัก ---
if __name__ == "__main__":
    print("Simulating bot script with screen text detection...")
    print("Bot is now running continuously. To stop the bot, press Ctrl+C.")
    
    # วนลูปไม่สิ้นสุด
    while True:
        try:
            # อ่านข้อความจากหน้าจอ
            latest_message = read_screen_text()
            
            if latest_message:
                print(f"Detected text: '{latest_message}'")
                check_for_message(latest_message)
            
            time.sleep(1) # รอ 1 วินาที เพื่อไม่ให้โปรแกรมใช้ทรัพยากรมากเกินไป
            
        except KeyboardInterrupt:
            # หยุดโปรแกรมเมื่อกด Ctrl+C
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break
            
    print("Simulation finished.")
