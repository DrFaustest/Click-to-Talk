"""
Mouse Controller Module
Handles mouse movement and click simulation using pyautogui
"""

import pyautogui
from config import Config
import threading  
import tkinter as tk  
import time  

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

    def highlight_cursor(self):  
        """Briefly display a ring around the current cursor position."""  
        def _show():  
            try:  
                x, y = pyautogui.position()  
                size = self.config.highlight_size  
                radius = size // 2  
                border = self.config.highlight_border  
                duration = self.config.highlight_duration_ms / 1000.0  

                root = tk.Tk()  
                root.overrideredirect(True)  
                root.attributes("-topmost", True)  

                try:  
                    root.attributes("-transparentcolor", "white")  
                    transparent_supported = True  
                except Exception:  
                    transparent_supported = False  

                root.geometry(f"{size}x{size}+{x - radius}+{y - radius}")  

                canvas = tk.Canvas(  
                    root, width=size, height=size, highlightthickness=0, bd=0,  
                    bg="white" if transparent_supported else ""  
                )  
                canvas.pack()  

                canvas.create_oval(  
                    border, border, size - border, size - border,  
                    outline=self.config.highlight_color, width=border  
                )  

                if not transparent_supported:  
                    canvas.create_oval(  
                        border + 2, border + 2, size - (border + 2), size - (border + 2),  
                        outline="", fill="#E6F6FF"  
                    )  

                root.after(int(self.config.highlight_duration_ms), root.destroy)  
                root.mainloop()  
            except Exception:  
                pass  

        threading.Thread(target=_show, daemon=True).start()  
        print("Cursor highlighted (find)")  