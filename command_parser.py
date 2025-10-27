"""
Command Parser Module
Interprets voice commands and executes corresponding mouse actions
"""

import re
from config import Config

class CommandParser:
    def __init__(self, config):
        self.config = config
        self.mouse_controller = None  # Will be set by main app

    def set_mouse_controller(self, mouse_controller):
        """Set the mouse controller instance"""
        self.mouse_controller = mouse_controller

    def parse_command(self, text):
        """Parse voice command and execute action"""
        if not self.mouse_controller:
            return

        text = text.lower().strip()

                # [ADDED] Handle visual locate before generic 'where'
        if self._is_find_command(text):  # [ADDED]
            try:  # [ADDED]
                self.mouse_controller.highlight_cursor()  # [ADDED]
            except Exception as e:  # [ADDED]
                print(f"Error highlighting cursor: {e}")  # [ADDED]
            return  # [ADDED]


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
        click_keywords = ["click", "press", "tap"]
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

    def _is_find_command(self, text):  # [ADDED]
        keywords = [  # [ADDED]
            "find", "highlight cursor", "show cursor", "locate cursor",  # [ADDED]
            "where is my cursor", "where's my cursor"  # [ADDED]
        ]  # [ADDED]
        return any(k in text for k in keywords)  # [ADDED]