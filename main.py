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

def reset_menu(icon, item):
    menu_items = constuct_menu(data)
    icon.menu = Menu(*menu_items)
    icon.update_menu()

def on_copy(icon, item, text):
    pyperclip.copy(text)

def monitor_clipboard():
    last_text = ""
    while True:
        text = pyperclip.paste()
        if text != last_text:
            last_text = text
            add_menu_item(text)
        time.sleep(2)
        
def add_menu_item(text):

    if len(menu_items) == len(data) + 3:
       menu_items.insert(-2, Menu.SEPARATOR)
       menu_items.insert(-2, MenuItem('Delete pastboard history', reset_menu))

    truncated_text = text[:50] + '...' if len(text) > 50 else text
    if not any(item.text == text for item in menu_items):
        menu_items.insert(-4, MenuItem(truncated_text.strip(), partial(on_copy, text=text)))
        
    icon.menu = Menu(*menu_items)
    icon.update_menu()

def constuct_menu(data):
    items = [Menu.SEPARATOR]
    for entry in data:
        items.insert(-1, MenuItem(entry['title'], partial(on_copy, text=entry['text'])))
    items.append(Menu.SEPARATOR)
    items.append(MenuItem('Quit', on_quit))

    return items

with open('values.json', 'r') as file:
    data = json.load(file)
menu_items = constuct_menu(data)

icon = Icon("CopyPaste", get_icon(), "CopyPaste", Menu(*menu_items))

clipboard_thread = Thread(target=monitor_clipboard, daemon=True)
clipboard_thread.start()

icon.run()
