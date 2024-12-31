import os
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw
import json
from functools import partial
import pyperclip

def get_icon():
    icon_path = os.path.join(os.path.dirname(__file__), "icon.png")
    icon_image = Image.open(icon_path)
    return icon_image

def on_quit(icon, item):
    icon.stop()

def on_copy(icon, item, text):
    pyperclip.copy(text)

with open('values.json', 'r') as file:
    data = json.load(file)

menu_items = [MenuItem(entry['title'], partial(on_copy, text=entry['text'])) for entry in data]
menu_items.append(Menu.SEPARATOR)
menu_items.append(MenuItem('Quit', on_quit))

menu = Menu(*menu_items)

icon = Icon("CopyPaste", get_icon(), "CopyPaste", menu)
icon.run()
