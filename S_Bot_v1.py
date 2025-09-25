import pyautogui
import keyboard
import time
import threading
import tkinter as tk
from tkinter import filedialog, ttk
import json
import cv2
import pytesseract
import numpy as np
from PIL import ImageGrab

# ติดตั้ง pytesseract ก่อนใช้งาน (ต้องลง Tesseract-OCR ในเครื่องด้วย)
# pip install pytesseract pillow opencv-python

positions = []          # ตำแหน่งที่บันทึก (ลำดับการคลิก)
task_sequence = [       # ลำดับงาน (การทำงาน)
    "ตรวจจับภาพ",
    "ตรวจจับข้อความด้วย OCR",
    "คลิกตำแหน่ง"
]
running = False         # สถานะบอท
bot_thread = None       # Thread ของบอท
target_images = []      # ไฟล์ภาพที่ต้องตรวจจับ
target_texts = []       # ข้อความที่ต้องตรวจจับ (OCR)
interval = 2            # เวลา (วินาที) หน่วงระหว่างรอบงาน

# ======================
# ฟังก์ชันบอท
# ======================
def click_loop():
    global running
    pos_index = 0
    while running:
        # ทำงานตามลำดับงานที่ผู้ใช้ตั้งค่า
        for task in task_sequence:
            if task == "ตรวจจับภาพ":
                for img in target_images:
                    box = pyautogui.locateOnScreen(img, confidence=0.8)
                    if box:
                        center = pyautogui.center(box)
                        pyautogui.doubleClick(center)
                        log(f"[ภาพเจอ] ดับเบิ้ลคลิกที่ {center}")
                        # หากเจอภาพแล้ว ให้ออกจาก loop ภาพเพื่อไม่ให้คลิกซ้ำในรอบเดียว
                        break
            elif task == "ตรวจจับข้อความด้วย OCR":
                screen = ImageGrab.grab()
                img_np = np.array(screen)
                gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
                detected_text = pytesseract.image_to_string(gray, lang="eng+tha")
                for keyword in target_texts:
                    if keyword in detected_text:
                        w, h = pyautogui.size()
                        pyautogui.doubleClick(w//2, h//2)
                        log(f"[OCR เจอ] '{keyword}' → ดับเบิ้ลคลิกที่กลางจอ")
                        break
            elif task == "คลิกตำแหน่ง":
                if positions:
                    x, y = positions[pos_index]
                    pyautogui.doubleClick(x, y)
                    log(f"[ตำแหน่งคลิก] ลำดับ {pos_index+1} → ({x}, {y})")
                    pos_index = (pos_index + 1) % len(positions)
        time.sleep(interval)

def start_bot():
    global running, bot_thread
    if running:
        log("⚠️ บอทกำลังทำงานอยู่แล้ว")
        return
    running = True
    bot_thread = threading.Thread(target=click_loop, daemon=True)
    bot_thread.start()
    log("✅ เริ่มทำงานบอท")

def stop_bot():
    global running
    running = False
    log("⛔ หยุดบอทแล้ว")

# ======================
# ฟังก์ชันจัดการตำแหน่ง/รูป/ข้อความ/งาน
# ======================
def add_position():
    x, y = pyautogui.position()
    positions.append((x, y))
    update_lists()
    log(f"➕ เพิ่มตำแหน่ง: ({x}, {y})")

def remove_last():
    if positions:
        pos = positions.pop()
        update_lists()
        log(f"🗑️ ลบตำแหน่ง: {pos}")
    else:
        log("⚠️ ไม่มีตำแหน่งให้ลบ")

def choose_image():
    file_path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png"), ("All Files", "*.*")])
    if file_path:
        target_images.append(file_path)
        update_lists()
        log(f"🖼️ เพิ่มรูปภาพ: {file_path}")

def add_text():
    text = entry_text.get()
    if text:
        target_texts.append(text)
        update_lists()
        log(f"🔤 เพิ่มข้อความ OCR: {text}")

def remove_task():
    # ลบงานที่เลือกออกจาก task_sequence
    try:
        selected_index = listbox_tasks.curselection()[0]
        removed = task_sequence.pop(selected_index)
        update_lists()
        log(f"🗑️ ลบงาน: {removed}")
    except IndexError:
        log("⚠️ กรุณาเลือกงานที่ต้องการลบ")

def save_config():
    data = {
        "positions": positions,
        "images": target_images,
        "texts": target_texts,
        "tasks": task_sequence,
        "interval": interval
    }
    file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        log(f"💾 บันทึก config: {file_path}")

def load_config():
    global positions, target_images, target_texts, task_sequence, interval
    file_path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        positions = data.get("positions", [])
        target_images = data.get("images", [])
        target_texts = data.get("texts", [])
        task_sequence = data.get("tasks", ["ตรวจจับภาพ", "ตรวจจับข้อความด้วย OCR", "คลิกตำแหน่ง"])
        interval = data.get("interval", 2)
        entry_interval.delete(0, tk.END)
        entry_interval.insert(0, str(interval))
        update_lists()
        log(f"📂 โหลด config: {file_path}")

# ======================
# GUI
# ======================
def update_lists():
    # อัปเดต listbox ในหน้า "ตำแหน่งคลิก"
    listbox_positions.delete(0, tk.END)
    if positions:
        listbox_positions.insert(tk.END, "ตำแหน่ง:")
        for idx, (x, y) in enumerate(positions, start=1):
            listbox_positions.insert(tk.END, f" - {idx}. ({x}, {y})")
    # อัปเดต listbox ในหน้า "ลำดับงาน"
    listbox_tasks.delete(0, tk.END)
    if task_sequence:
        listbox_tasks.insert(tk.END, "ลำดับงาน:")
        for idx, task in enumerate(task_sequence, start=1):
            listbox_tasks.insert(tk.END, f" - {idx}. {task}")

def log(msg):
    text_log.insert(tk.END, msg + "\n")
    text_log.see(tk.END)

def set_interval():
    global interval
    try:
        interval = float(entry_interval.get())
        log(f"⏱️ ตั้งค่า interval: {interval} วินาที")
    except ValueError:
        log("⚠️ ค่า interval ไม่ถูกต้อง")

def on_close():
    stop_bot()
    root.destroy()

root = tk.Tk()
root.title("Bot Auto Click + Image + OCR")
root.geometry("500x650")
root.protocol("WM_DELETE_WINDOW", on_close)

# ปุ่มควบคุมตำแหน่ง/รูป/ข้อความ
frame_buttons = ttk.Frame(root)
frame_buttons.pack(pady=10)

ttk.Button(frame_buttons, text="➕ เพิ่มตำแหน่ง (F7)", command=add_position).grid(row=0, column=0, padx=5)
ttk.Button(frame_buttons, text="🗑️ ลบตำแหน่งล่าสุด", command=remove_last).grid(row=0, column=1, padx=5)
ttk.Button(frame_buttons, text="🖼️ เพิ่มรูปภาพ", command=choose_image).grid(row=1, column=0, padx=5, pady=5)
ttk.Button(frame_buttons, text="🔤 เพิ่มข้อความ", command=add_text).grid(row=1, column=1, padx=5, pady=5)

# ช่องกรอกข้อความ OCR
entry_text = ttk.Entry(root, width=40)
entry_text.pack(pady=5)

# Interval
frame_interval = ttk.Frame(root)
frame_interval.pack(pady=5)
ttk.Label(frame_interval, text="Interval (วินาที):").grid(row=0, column=0, padx=5)
entry_interval = ttk.Entry(frame_interval, width=10)
entry_interval.insert(0, str(interval))
entry_interval.grid(row=0, column=1, padx=5)
ttk.Button(frame_interval, text="Set", command=set_interval).grid(row=0, column=2, padx=5)

# ปุ่มบอท
frame_bot = ttk.Frame(root)
frame_bot.pack(pady=5)
ttk.Button(frame_bot, text="▶️ เริ่มบอท", command=start_bot).grid(row=0, column=0, padx=5)
ttk.Button(frame_bot, text="⏹️ หยุดบอท (F6)", command=stop_bot).grid(row=0, column=1, padx=5)

# ปุ่ม Save/Load
frame_save = ttk.Frame(root)
frame_save.pack(pady=5)
ttk.Button(frame_save, text="💾 Save Config", command=save_config).grid(row=0, column=0, padx=5)
ttk.Button(frame_save, text="📂 Load Config", command=load_config).grid(row=0, column=1, padx=5)

# Notebook สำหรับแยกหน้าจอ
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True, padx=10, pady=10)

# Tab สำหรับตำแหน่งคลิก
tab_positions = ttk.Frame(notebook)
notebook.add(tab_positions, text="ตำแหน่งคลิก")

listbox_positions = tk.Listbox(tab_positions, width=60, height=10)
listbox_positions.pack(pady=10)

# Tab สำหรับลำดับงาน
tab_tasks = ttk.Frame(notebook)
notebook.add(tab_tasks, text="ลำดับงาน")

listbox_tasks = tk.Listbox(tab_tasks, width=60, height=10)
listbox_tasks.pack(pady=10)
ttk.Button(tab_tasks, text="🗑️ ลบงานที่เลือก", command=remove_task).pack(pady=5)

# Log
text_log = tk.Text(root, height=15, width=60)
text_log.pack(pady=5)

# Hotkey
keyboard.add_hotkey("F7", add_position)
keyboard.add_hotkey("F6", stop_bot)

update_lists()
root.mainloop()
