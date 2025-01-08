import os
from threading import Thread
from pystray import Icon, MenuItem, Menu
from PIL import Image
import json
from functools import partial
import pyperclip
import time

def get_icon():
    icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
    icon_image = Image.open(icon_path)
    return icon_image

def on_quit(icon, item):
    icon.stop()

def on_copy(icon, item, text):
    pyperclip.copy(text)

def monitor_clipboard():
    last_text = ""
    
    while True:
        print("Monitoring clipboard...")
        text = pyperclip.paste()
        if text != last_text:
            last_text = text
            truncated_text = text[:50] + '...' if len(text) > 20 else text
            if not any(item.text == text for item in menu_items):
                menu_items.insert(-2, MenuItem(truncated_text, partial(on_copy, text=text)))
            icon.menu = Menu(*menu_items)
            icon.update_menu()
        time.sleep(5)

with open('values.json', 'r') as file:
    data = json.load(file)

menu_items = [Menu.SEPARATOR]

for entry in data:
    menu_items.insert(-2, MenuItem(entry['title'], partial(on_copy, text=entry['text'])))

menu_items.append(Menu.SEPARATOR)
menu_items.append(MenuItem('Quit', on_quit))

menu = Menu(*menu_items)
icon = Icon("CopyPaste", get_icon(), "CopyPaste", menu)

# Start the clipboard monitoring in a separate thread
clipboard_thread = Thread(target=monitor_clipboard, daemon=True)
clipboard_thread.start()
icon.run()
