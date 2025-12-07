"""
Tests for command_parser.py
"""

import pytest
from unittest.mock import MagicMock, patch
from command_parser import CommandParser
from config import Config


class TestCommandParser:
    def setup_method(self):
        self.config = Config()
        self.parser = CommandParser(self.config)
        self.mock_mouse = MagicMock()
        self.mock_keyboard = MagicMock()
        self.mock_wm = MagicMock()
        self.parser.set_mouse_controller(self.mock_mouse)
        self.parser.set_keyboard_controller(self.mock_keyboard)
        self.parser.set_window_manager(self.mock_wm)

    def test_movement_commands(self):
        self.parser.parse_command("move up")
        self.mock_mouse.move_cursor.assert_called_with("up", 50)
        
        self.mock_mouse.reset_mock()
        self.parser.parse_command("move down 100")
        self.mock_mouse.move_cursor.assert_called_with("down", 100)
        
        self.mock_mouse.reset_mock()
        self.parser.parse_command("move left")
        self.mock_mouse.move_cursor.assert_called_with("left", 50)
        
        self.mock_mouse.reset_mock()
        self.parser.parse_command("move right 75")
        self.mock_mouse.move_cursor.assert_called_with("right", 75)

    def test_movement_distance_limits(self):
        self.parser.parse_command("move up 300")
        self.mock_mouse.move_cursor.assert_called_with("up", 250)
        
        self.mock_mouse.reset_mock()
        self.parser.parse_command("move up abc")
        self.mock_mouse.move_cursor.assert_called_with("up", 50)

    def test_click_commands(self):
        self.parser.parse_command("click")
        self.mock_mouse.click.assert_called_with("left")
        
        self.mock_mouse.reset_mock()
        self.parser.parse_command("right click")
        self.mock_mouse.click.assert_called_with("right")
        
        self.mock_mouse.reset_mock()
        self.parser.parse_command("double click")
        self.mock_mouse.click.assert_called_with("double")

    def test_scroll_commands(self):
        self.parser.parse_command("scroll up")
        self.mock_mouse.scroll.assert_called_with("up")
        
        self.mock_mouse.reset_mock()
        self.parser.parse_command("scroll down")
        self.mock_mouse.scroll.assert_called_with("down")
        
        self.mock_mouse.reset_mock()
        self.parser.parse_command("scroll")
        self.mock_mouse.scroll.assert_called_with("down")

    def test_position_commands(self):
        self.parser.parse_command("show position")
        self.mock_mouse.show_cursor_position.assert_called_once()
        
        self.mock_mouse.reset_mock()
        self.parser.parse_command("where")
        self.mock_mouse.show_cursor_position.assert_called_once()

    def test_find_cursor_command(self):
        self.parser.parse_command("find cursor")
        self.mock_mouse.highlight_cursor.assert_called_once()
        
        self.mock_mouse.reset_mock()
        self.parser.parse_command("find my mouse")
        self.mock_mouse.highlight_cursor.assert_called_once()

    def test_type_commands(self):
        self.parser.parse_command("type hello world")
        self.mock_keyboard.type_text.assert_called_with("hello world")
        
        self.mock_keyboard.reset_mock()
        self.parser.parse_command("dictate testing")
        self.mock_keyboard.type_text.assert_called_with("testing")

    def test_press_commands(self):
        self.parser.parse_command("press enter")
        self.mock_keyboard.press_keys.assert_called_with("enter")
        
        self.mock_keyboard.reset_mock()
        self.parser.parse_command("hit escape")
        self.mock_keyboard.press_keys.assert_called_with("escape")

    @patch('sys.platform', 'darwin')
    def test_browser_shortcuts_macos(self):
        self.parser.parse_command("new tab")
        self.mock_keyboard.press_keys.assert_called_with("command t")
        
        self.mock_keyboard.reset_mock()
        self.parser.parse_command("close tab")
        self.mock_keyboard.press_keys.assert_called_with("command w")
        
        self.mock_keyboard.reset_mock()
        self.parser.parse_command("address bar")
        self.mock_keyboard.press_keys.assert_called_with("command l")
        
        self.mock_keyboard.reset_mock()
        self.parser.parse_command("refresh")
        self.mock_keyboard.press_keys.assert_called_with("command r")

    @patch('sys.platform', 'linux')
    def test_browser_shortcuts_linux(self):
        self.parser.parse_command("new tab")
        self.mock_keyboard.press_keys.assert_called_with("ctrl t")
        
        self.mock_keyboard.reset_mock()
        self.parser.parse_command("close tab")
        self.mock_keyboard.press_keys.assert_called_with("ctrl w")
        
        self.mock_keyboard.reset_mock()
        self.parser.parse_command("refresh")
        self.mock_keyboard.press_keys.assert_called_with("ctrl r")

    def test_tab_navigation(self):
        self.parser.parse_command("next tab")
        self.mock_keyboard.press_keys.assert_called_with("ctrl tab")
        
        self.mock_keyboard.reset_mock()
        self.parser.parse_command("previous tab")
        self.mock_keyboard.press_keys.assert_called_with("ctrl shift tab")

    def test_open_commands(self):
        self.parser.parse_command("open gmail")
        self.mock_wm.open.assert_called_with("gmail")
        
        self.mock_wm.reset_mock()
        self.parser.parse_command("go to youtube")
        self.mock_wm.open.assert_called_with("youtube")
        
        self.mock_wm.reset_mock()
        self.parser.parse_command("navigate to example.com")
        self.mock_wm.open.assert_called_with("example.com")

    def test_panel_commands(self):
        mock_minimize = MagicMock()
        mock_maximize = MagicMock()
        self.parser.set_ui_callbacks(mock_minimize, mock_maximize)
        
        self.parser.parse_command("minimize panel")
        mock_minimize.assert_called_once()
        
        self.parser.parse_command("maximize panel")
        mock_maximize.assert_called_once()

    def test_command_recognition_helpers(self):
        assert self.parser._is_movement_command("move up") == True
        assert self.parser._is_movement_command("click") == False
        
        assert self.parser._is_click_command("click") == True
        assert self.parser._is_click_command("tap") == True
        assert self.parser._is_click_command("move") == False
        
        assert self.parser._is_scroll_command("scroll") == True
        assert self.parser._is_scroll_command("wheel") == True
        assert self.parser._is_scroll_command("click") == False
        
        assert self.parser._is_find_command("find cursor") == True
        assert self.parser._is_find_command("find my mouse") == True
        
        assert self.parser._is_minimize_command("minimize panel") == True
        assert self.parser._is_minimize_command("hide controls") == True
        
        assert self.parser._is_maximize_command("maximize panel") == True
        assert self.parser._is_maximize_command("show controls") == True

    @patch('sys.platform', 'darwin')
    def test_primary_mod_macos(self):
        assert self.parser._primary_mod() == "command"

    @patch('sys.platform', 'linux')
    def test_primary_mod_linux(self):
        assert self.parser._primary_mod() == "ctrl"

    @patch('sys.platform', 'win32')
    def test_primary_mod_windows(self):
        assert self.parser._primary_mod() == "ctrl"

    def test_extract_target_after_trigger(self):
        assert self.parser._extract_target_after_trigger("open gmail") == "gmail"
        assert self.parser._extract_target_after_trigger("go to youtube") == "youtube"
        assert self.parser._extract_target_after_trigger("navigate to google.com") == "google.com"
        assert self.parser._extract_target_after_trigger("click") is None

    def test_error_handling(self):
        self.mock_mouse.click.side_effect = Exception("Test error")
        self.parser.parse_command("click")
        
        self.mock_mouse.scroll.side_effect = Exception("Test error")
        self.parser.parse_command("scroll up")
        
        self.mock_mouse.move_cursor.side_effect = Exception("Test error")
        self.parser.parse_command("move up")
        
        self.mock_mouse.highlight_cursor.side_effect = Exception("Test error")
        self.parser.parse_command("find cursor")

    def test_unrecognized_command(self, capsys):
        self.parser.parse_command("invalid command")
        captured = capsys.readouterr()
        assert "Unrecognized command: invalid command" in captured.out

    def test_controller_setters(self):
        mock_kb = MagicMock()
        mock_wm = MagicMock()
        
        self.parser.set_keyboard_controller(mock_kb)
        assert self.parser.keyboard_controller == mock_kb
        
        self.parser.set_window_manager(mock_wm)
        assert self.parser.window_manager == mock_wm

    def test_commands_without_controllers(self):
        parser = CommandParser(self.config)
        parser.parse_command("move up")
        parser.parse_command("type hello")
        parser.parse_command("open gmail")

    def test_panel_commands_without_callbacks(self, capsys):
        parser = CommandParser(self.config)
        parser.set_mouse_controller(self.mock_mouse)
        
        parser.parse_command("minimize panel")
        captured = capsys.readouterr()
        assert "Minimize panel requested" in captured.out
        
        parser.parse_command("maximize panel")
        captured = capsys.readouterr()
        assert "Maximize panel requested" in captured.out
