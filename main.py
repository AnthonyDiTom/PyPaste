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
        text = pyperclip.paste()
        if text != last_text:
            last_text = text
            add_menu_item(text)
        time.sleep(3)

def add_menu_item(text):
    truncated_text = text[:50] + '...' if len(text) > 20 else text
    if not any(item.text == text for item in menu_items):
        menu_items.insert(-2, MenuItem(truncated_text, partial(on_copy, text=text)))
    icon.menu = Menu(*menu_items)
    icon.update_menu()

def constuct_menu():
    with open('values.json', 'r') as file:
        data = json.load(file)

    items = [Menu.SEPARATOR]

    for entry in data:
        items.insert(-1, MenuItem(entry['title'], partial(on_copy, text=entry['text'])))

    items.append(Menu.SEPARATOR)
    items.append(MenuItem('Quit', on_quit))

    return items

menu_items = constuct_menu()

icon = Icon("CopyPaste", get_icon(), "CopyPaste", Menu(*menu_items))

clipboard_thread = Thread(target=monitor_clipboard, daemon=True)
clipboard_thread.start()

icon.run()
