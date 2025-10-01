"""
Mouse Controller Module
Handles mouse movement and click simulation using pyautogui
"""

import pyautogui
from config import Config

class MouseController:
    def __init__(self, config):
        self.config = config
        pyautogui.FAILSAFE = True  # Enable failsafe
        pyautogui.PAUSE = self.config.mouse_pause  # Pause between actions

    def move_cursor(self, direction, distance=None):
        """Move cursor in specified direction"""
        if distance is None:
            distance = self.config.default_move_distance

        current_x, current_y = pyautogui.position()

        if direction == "up":
            new_y = max(0, current_y - distance)
            pyautogui.moveTo(current_x, new_y, duration=self.config.move_duration)
        elif direction == "down":
            screen_height = pyautogui.size()[1]
            new_y = min(screen_height, current_y + distance)
            pyautogui.moveTo(current_x, new_y, duration=self.config.move_duration)
        elif direction == "left":
            new_x = max(0, current_x - distance)
            pyautogui.moveTo(new_x, current_y, duration=self.config.move_duration)
        elif direction == "right":
            screen_width = pyautogui.size()[0]
            new_x = min(screen_width, current_x + distance)
            pyautogui.moveTo(new_x, current_y, duration=self.config.move_duration)

        print(f"Moved {direction} by {distance} pixels")

    def click(self, button="left"):
        """Perform mouse click"""
        if button == "left":
            pyautogui.click()
            print("Left click performed")
        elif button == "right":
            pyautogui.rightClick()
            print("Right click performed")
        elif button == "double":
            pyautogui.doubleClick()
            print("Double click performed")

    def scroll(self, direction, clicks=3):
        """Scroll mouse wheel"""
        if direction == "up":
            pyautogui.scroll(clicks)
            print(f"Scrolled up {clicks} clicks")
        elif direction == "down":
            pyautogui.scroll(-clicks)
            print(f"Scrolled down {clicks} clicks")

    def get_position(self):
        """Get current mouse position"""
        return pyautogui.position()

    def show_cursor_position(self):
        """Display current cursor position"""
        x, y = self.get_position()
        print(f"Cursor position: ({x}, {y})")