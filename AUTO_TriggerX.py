import pyautogui
import cv2
import numpy as np
from PIL import ImageGrab
import time
import keyboard

def detect_blue_and_click():
    x, y, width, height = 833 , 170 , 360, 500  # กำหนดกรอบตรวจจับ
    running = False

    print("กด F7 เพื่อเริ่ม/หยุด Bot")

    while True:
        # ตรวจสอบการกดปุ่ม F7 เพื่อสลับสถานะ
        if keyboard.is_pressed("F7"):
            running = not running
            if running:
                print("Bot ทำงาน...")
            else:
                print("Bot หยุดแล้ว...")
            time.sleep(0.5) 
        
        if running:
            screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_with_rectangle = frame.copy()
            cv2.rectangle(frame_with_rectangle, (0, 0), (width - 1, height - 1), (0, 0, 255), 2)

         
            target_color = np.array([37, 150, 190])
            color_tolerance = 30  

          
            lower_bound = target_color - color_tolerance
            upper_bound = target_color + color_tolerance
            mask = cv2.inRange(frame, lower_bound, upper_bound)

         
            blue_positions = cv2.findNonZero(mask)
            if blue_positions is not None:
               
                for blue_pixel in blue_positions:
                    pixel_x, pixel_y = blue_pixel[0][0], blue_pixel[0][1]
                    click_x = x + pixel_x 
                    click_y = y + pixel_y  

                 
                    pyautogui.click(click_x, click_y)
                    print(f"ตรวจพบสีฟ้าและคลิกที่ตำแหน่ง ({click_x}, {click_y})")
                    time.sleep(0.1) 
                    break  

            # แสดงภาพหน้ากากสีฟ้าเพื่อ Debug
            cv2.imshow("Blue Detection Mask", mask)
            cv2.imshow("Screen Area with Red Rectangle", frame_with_rectangle)

        # กด 'q' เพื่อหยุดโปรแกรมทั้งหมด
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("โปรแกรมปิดแล้ว...")
            break

    cv2.destroyAllWindows()

# เรียกใช้ฟังก์ชัน
detect_blue_and_click()