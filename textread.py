from pynput import keyboard
# from winwid import main
from pynput.keyboard import Key, KeyCode, Listener
import subprocess
import sys
import os

# The key combination to check
COMBINATIONS = [
    { Key.cmd,Key.shift, keyboard.KeyCode(char='c')},
    { Key.cmd,Key.shift, keyboard.KeyCode(char='C')}
]

# The currently active modifiers
current = set()

def execute():
    # main()
    subprocess.call("C:/Python36/Python.exe d:/VM/textread/winwid.py", shell=True)

def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute()

def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()




