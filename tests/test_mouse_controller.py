"""
Tests for mouse_controller.py
"""

import pytest
from unittest.mock import MagicMock, patch
from mouse_controller import MouseController
from config import Config


class TestMouseController:
    def setup_method(self):
        """Setup before each test"""
        self.config = Config()
        self.controller = MouseController(self.config)

    @patch('pyautogui.moveTo')
    @patch('pyautogui.position')
    def test_move_cursor_up(self, mock_position, mock_move):
        """Test moving cursor up"""
        mock_position.return_value = (100, 100)
        self.controller.move_cursor("up", 50)
        mock_move.assert_called_once_with(100, 50, duration=0.2)

    @patch('pyautogui.moveTo')
    @patch('pyautogui.position')
    def test_move_cursor_down(self, mock_position, mock_move):
        """Test moving cursor down"""
        mock_position.return_value = (100, 100)
        self.controller.move_cursor("down", 50)
        mock_move.assert_called_once_with(100, 150, duration=0.2)

    @patch('pyautogui.moveTo')
    @patch('pyautogui.position')
    def test_move_cursor_left(self, mock_position, mock_move):
        """Test moving cursor left"""
        mock_position.return_value = (100, 100)
        self.controller.move_cursor("left", 50)
        mock_move.assert_called_once_with(50, 100, duration=0.2)

    @patch('pyautogui.moveTo')
    @patch('pyautogui.position')
    def test_move_cursor_right(self, mock_position, mock_move):
        """Test moving cursor right"""
        mock_position.return_value = (100, 100)
        self.controller.move_cursor("right", 50)
        mock_move.assert_called_once_with(150, 100, duration=0.2)

    @patch('pyautogui.moveTo')
    @patch('pyautogui.position')
    def test_move_cursor_default_distance(self, mock_position, mock_move):
        """Test moving cursor with default distance"""
        mock_position.return_value = (100, 100)
        self.controller.move_cursor("up")
        mock_move.assert_called_once_with(100, 50, duration=0.2)

    @patch('pyautogui.size')
    @patch('pyautogui.moveTo')
    @patch('pyautogui.position')
    def test_move_cursor_bounds_checking(self, mock_position, mock_move, mock_size):
        """Test cursor stays within screen bounds"""
        mock_position.return_value = (10, 10)
        mock_size.return_value = (1920, 1080)
        self.controller.move_cursor("left", 50)  # Would go to -40, should be 0
        mock_move.assert_called_once_with(0, 10, duration=0.2)

    @patch('pyautogui.click')
    def test_click_left(self, mock_click):
        """Test left click"""
        self.controller.click("left")
        mock_click.assert_called_once()

    @patch('pyautogui.rightClick')
    def test_click_right(self, mock_right_click):
        """Test right click"""
        self.controller.click("right")
        mock_right_click.assert_called_once()

    @patch('pyautogui.doubleClick')
    def test_click_double(self, mock_double_click):
        """Test double click"""
        self.controller.click("double")
        mock_double_click.assert_called_once()

    @patch('pyautogui.scroll')
    def test_scroll_up(self, mock_scroll):
        """Test scrolling up"""
        self.controller.scroll("up", 3)
        mock_scroll.assert_called_once_with(3)

    @patch('pyautogui.scroll')
    def test_scroll_down(self, mock_scroll):
        """Test scrolling down"""
        self.controller.scroll("down", 3)
        mock_scroll.assert_called_once_with(-3)

    @patch('pyautogui.position')
    def test_get_position(self, mock_position):
        """Test getting cursor position"""
        mock_position.return_value = (100, 200)
        pos = self.controller.get_position()
        assert pos == (100, 200)

    @patch('pyautogui.position')
    def test_show_cursor_position(self, mock_position, capsys):
        """Test showing cursor position"""
        mock_position.return_value = (100, 200)
        self.controller.show_cursor_position()
        captured = capsys.readouterr()
        assert "Cursor position: (100, 200)" in captured.out