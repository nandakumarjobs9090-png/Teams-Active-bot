import tkinter as tk
import threading
import time
import ctypes
import random
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw

running = False
interval = 30  # default seconds


# ---------------------- Mouse Move Logic ----------------------
def move_mouse():
    global running, interval
    MOUSEEVENTF_MOVE = 0x0001

    while running:
        dx = random.randint(-25, 25)
        dy = random.randint(-25, 25)
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_MOVE, dx, dy, 0, 0)
        time.sleep(interval)


# ---------------------- GUI Functions -------------------------
def start_bot():
    global running, interval
    if not running:
        running = True
        try:
            interval = int(timer_entry.get())
        except:
            interval = 30
        threading.Thread(target=move_mouse, daemon=True).start()
        status_label.config(text="Status: Running")


def stop_bot():
    global running
    running = False
    status_label.config(text="Status: Stopped")


# ---------------------- Minimize to System Tray ----------------------
def create_tray_icon():
    # Create simple tray icon image
    img = Image.new('RGB', (64, 64), "black")
    draw = ImageDraw.Draw(img)
    draw.ellipse((16, 16, 48, 48), fill="white")

    menu = (
        item('Show', show_window),
        item('Exit', quit_app)
    )
    return pystray.Icon("Teams Bot", img, "Teams Active Bot", menu)


def hide_window():
    window.withdraw()
    tray.run()


def show_window(icon=None, item=None):
    window.after(0, window.deiconify)
    tray.stop()


def quit_app(icon=None, item=None):
    global running
    running = False
    tray.stop()
    window.destroy()


# ---------------------- GUI Layout -------------------------
window = tk.Tk()
window.title("Teams Active Bot")
window.geometry("320x220")

tk.Label(window, text="Mouse Move Interval (seconds)").pack(pady=5)
timer_entry = tk.Entry(window)
timer_entry.insert(0, "30")
timer_entry.pack(pady=5)

start_btn = tk.Button(window, text="Start", width=20, command=start_bot)
start_btn.pack(pady=5)

stop_btn = tk.Button(window, text="Stop", width=20, command=stop_bot)
stop_btn.pack(pady=5)

status_label = tk.Label(window, text="Status: Stopped")
status_label.pack(pady=10)

min_btn = tk.Button(window, text="Run in Background", command=hide_window)
min_btn.pack(pady=10)

# Create tray icon object
tray = create_tray_icon()

window.mainloop()
