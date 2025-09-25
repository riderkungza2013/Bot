from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ตั้งค่า WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# เปิดเว็บไซต์
driver.get('https://www.theconcert.com/concert')

# รอโหลดหน้าเว็บ
driver.implicitly_wait(1)


# รอและคลิกที่ <div> "ไทยประกันชีวิต presents COCKTAIL EVER LIVE"
try:
    # รอให้ <div> โหลดและคลิกได้
    concert_div = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="_main-body"]/div/div[3]/div[3]/div[2]/div/div/div[7]/div/div/div[1]/img')
        )
    )
    # ใช้ ActionChains เพื่อเลื่อนและคลิก
    actions = ActionChains(driver)
    actions.move_to_element(concert_div).click().perform()
    print("คลิก 'ONG SEONG-WU FANMEETING <COMEONG> IN BANGKOK สำเร็จ!")
except Exception as e:
    print("ONG SEONG-WU FANMEETING <COMEONG> IN BANGKOK ได้:", e)

try:
    # ใช้ XPath ที่คุณให้มา
    button_to_click = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="_main-body"]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div/div[2]/div[2]/button/span')
        )
    )
    # เลื่อนหน้าจอลงไปที่ปุ่ม
    actions = ActionChains(driver)
    actions.move_to_element(button_to_click).perform()
    # คลิกปุ่ม
    button_to_click.click()
    print("คลิกปุ่มซื้อสำเร็จ!")
except Exception as e:
    print("ไม่สามารถคลิกปุ่มซื้อได้:", e)
# เบราว์เซอร์ยังเปิดอยู่


