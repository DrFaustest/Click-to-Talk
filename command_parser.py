"""
Command Parser Module
Interprets voice commands and executes corresponding mouse actions
"""

import re
import sys  # NEW: for platform-aware shortcuts
from config import Config

class CommandParser:
    def __init__(self, config):
        self.config = config
        self.mouse_controller = None  # Will be set by main app
        self.window_manager = None    # NEW: injected for browser/site navigation
        self.keyboard_controller = None  # NEW: injected for typing/shortcuts
        self.ui_minimize_callback = None   # for GUI minimize
        self.ui_maximize_callback = None   # for GUI maximize

    def set_mouse_controller(self, mouse_controller):
        """Set the mouse controller instance"""
        self.mouse_controller = mouse_controller

    # NEW: allow main.py to inject WindowManager
    def set_window_manager(self, wm):
        self.window_manager = wm  # NEW

    # NEW: allow main.py to inject KeyboardController
    def set_keyboard_controller(self, kc):
        self.keyboard_controller = kc  # NEW

    def set_ui_callbacks(self, minimize_callback=None, maximize_callback=None):
        """Set callbacks used for GUI minimize/maximize via voice commands."""
        self.ui_minimize_callback = minimize_callback
        self.ui_maximize_callback = maximize_callback


    def _primary_mod(self) -> str:
        """NEW: Return platform's primary modifier for common shortcuts."""
        return "command" if sys.platform == "darwin" else "ctrl"  # NEW

    def _extract_target_after_trigger(self, text: str):
        """NEW: Return the substring after specific voice triggers, trimmed."""
        triggers = ("open ", "go to ", "navigate to ")
        for trig in triggers:
            if text.startswith(trig):
                return text[len(trig):].strip()
        return None

    def parse_command(self, text):
        """Parse voice command and execute action"""
        if not self.mouse_controller:
            return

        text = text.lower().strip()

        # Handle visual locate before generic 'where'
        if self._is_find_command(text):  
            try:  
                self.mouse_controller.highlight_cursor()  
            except Exception as e:  
                print(f"Error highlighting cursor: {e}")  
            return  
        
        # GUI minimize / maximize via voice
        if self._is_minimize_command(text):
            if self.ui_minimize_callback:
                self.ui_minimize_callback()
            else:
                print("Minimize panel requested (no UI callback configured).")
            return

        if self._is_maximize_command(text):
            if self.ui_maximize_callback:
                self.ui_maximize_callback()
            else:
                print("Maximize panel requested (no UI callback configured).")
            return

        # NEW: Browser navigation / open (URLs or aliases)
        if text.startswith(("open ", "go to ", "navigate to ")):  # NEW
            if self.window_manager:  # NEW
                target = self._extract_target_after_trigger(text)  # NEW
                if target:  # NEW
                    self.window_manager.open(target)  # NEW
                else:  # NEW
                    print("No navigation target recognized.")  # NEW
            return  # NEW

        # NEW: Typing / dictation
        if text.startswith(("type ", "dictate ")):  # NEW
            if self.keyboard_controller:  # NEW
                content = text.split(" ", 1)[1]
                self.keyboard_controller.type_text(content)  # NEW
            return  # NEW

        # NEW: Press / shortcuts (handle before click so 'press enter' isn't a click)
        if text.startswith(("press ", "hit ")):  # NEW
            if self.keyboard_controller:  # NEW
                keys_phrase = text.split(" ", 1)[1]
                self.keyboard_controller.press_keys(keys_phrase)  # NEW
            return  # NEW

        # NEW: Convenience phrases mapped to shortcuts
        if self.keyboard_controller:  # NEW
            mod = self._primary_mod()  # NEW
            if text in {"new tab"}:
                self.keyboard_controller.press_keys(f"{mod} t")  # NEW
                return
            if text in {"close tab"}:
                self.keyboard_controller.press_keys(f"{mod} w")  # NEW
                return
            if text in {"next tab"}:
                self.keyboard_controller.press_keys("ctrl tab")  # NEW
                return
            if text in {"previous tab", "prev tab"}:
                self.keyboard_controller.press_keys("ctrl shift tab")  # NEW
                return
            if text in {"address bar", "focus address bar"}:
                self.keyboard_controller.press_keys(f"{mod} l")  # NEW
                return
            if text in {"refresh", "reload"}:
                self.keyboard_controller.press_keys(f"{mod} r")  # NEW
                return

        # Check for click commands first (more specific)
        if self._is_click_command(text):
            self._handle_click(text)
        # Movement commands
        elif self._is_movement_command(text):
            self._handle_movement(text)
        # Scroll commands
        elif self._is_scroll_command(text):
            self._handle_scroll(text)
        # Position commands
        elif "position" in text or "where" in text:
            self.mouse_controller.show_cursor_position()
        else:
            print(f"Unrecognized command: {text}")

    def _is_movement_command(self, text):
        """Check if text contains movement command"""
        movement_keywords = ["move", "go"]
        # Check if text starts with movement keywords or contains directional words without scroll
        if any(text.startswith(keyword) for keyword in movement_keywords):
            return True
        # Check for directional commands that don't contain scroll
        directional_keywords = ["up", "down", "left", "right"]
        has_directional = any(keyword in text for keyword in directional_keywords)
        has_scroll = "scroll" in text
        return has_directional and not has_scroll

    def _handle_movement(self, text):
        """Handle movement commands"""
        # Extract direction and distance
        direction = None
        distance = self.config.default_move_distance

        if "up" in text:
            direction = "up"
        elif "down" in text:
            direction = "down"
        elif "left" in text:
            direction = "left"
        elif "right" in text:
            direction = "right"

        # Try to extract number (distance)
        numbers = re.findall(r'\d+', text)
        if numbers:
            try:
                distance = int(numbers[0])
                # Limit distance to prevent excessive movement
                distance = min(distance, self.config.default_move_distance * 5)
            except ValueError:
                distance = self.config.default_move_distance

        if direction:
            try:
                self.mouse_controller.move_cursor(direction, distance)
            except Exception as e:
                print(f"Error moving cursor: {e}")

    def _is_click_command(self, text):
        """Check if text contains click command"""
        # NEW: removed "press" so 'press enter' is not misread as a click
        click_keywords = ["click", "tap"]  # NEW: was ["click","press","tap"]
        return any(keyword in text for keyword in click_keywords)

    def _handle_click(self, text):
        """Handle click commands"""
        try:
            if "right" in text:
                self.mouse_controller.click("right")
            elif "double" in text:
                self.mouse_controller.click("double")
            else:
                self.mouse_controller.click("left")
        except Exception as e:
            print(f"Error performing click: {e}")

    def _is_scroll_command(self, text):
        """Check if text contains scroll command"""
        scroll_keywords = ["scroll", "wheel"]
        return any(keyword in text for keyword in scroll_keywords)

    def _handle_scroll(self, text):
        """Handle scroll commands"""
        try:
            if "up" in text:
                self.mouse_controller.scroll("up")
            elif "down" in text:
                self.mouse_controller.scroll("down")
            else:
                # Default to down if unclear
                self.mouse_controller.scroll("down")
        except Exception as e:
            print(f"Error scrolling: {e}")

    def _is_find_command(self, text):
        keywords = [
            "find cursor", "find my cursor", "find mouse", "find my mouse"
        ]
        t = text.lower()
        hit = any(k in t for k in keywords)
        print(f"[DEBUG] _is_find_command: text='{t}', hit={hit}")
        return hit
  
    def _is_minimize_command(self, text):
        keywords = [
            "minimize panel",
            "minimize gui",
            "hide panel",
            "hide controls",
        ]
        return any(k in text for k in keywords)

    def _is_maximize_command(self, text):
        keywords = [
            "maximize panel",
            "maximize gui",
            "show panel",
            "show controls",
        ]
        return any(k in text for k in keywords)
