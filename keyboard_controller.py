# keyboard_controller.py
import pyautogui
import re

class KeyboardController:
    def __init__(self, pause=0.05):
        pyautogui.PAUSE = pause

    def type_text(self, text: str):
        pyautogui.typewrite(text, interval=0.01)
        print(f"Typed: {text}")

    def press_keys(self, keys_phrase: str):
        # Examples: "enter", "escape", "tab", "ctrl c", "ctrl v", "cmd l", "alt tab"
        tokens = re.split(r'\s+', keys_phrase.strip().lower())
        # map spoken aliases
        alias = {"control":"ctrl","cmd":"command","windows":"win","escape":"esc","return":"enter"}
        tokens = [alias.get(t, t) for t in tokens]
        if len(tokens) == 1:
            pyautogui.press(tokens[0])
        else:
            pyautogui.hotkey(*tokens)
        print(f"Pressed: {' + '.join(tokens)}")
