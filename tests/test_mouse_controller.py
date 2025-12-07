"""
Tests for mouse_controller.py
"""

import pytest
from unittest.mock import patch, MagicMock
from mouse_controller import MouseController
from config import Config


class TestMouseController:
    def setup_method(self):
        self.config = Config()
        self.controller = MouseController(self.config)

    @patch('pyautogui.moveTo')
    @patch('pyautogui.position')
    def test_move_cursor_directions(self, mock_position, mock_move):
        mock_position.return_value = (100, 100)
        
        self.controller.move_cursor("up", 50)
        mock_move.assert_called_with(100, 50, duration=0.2)
        
        mock_move.reset_mock()
        self.controller.move_cursor("down", 50)
        mock_move.assert_called_with(100, 150, duration=0.2)
        
        mock_move.reset_mock()
        self.controller.move_cursor("left", 50)
        mock_move.assert_called_with(50, 100, duration=0.2)
        
        mock_move.reset_mock()
        self.controller.move_cursor("right", 50)
        mock_move.assert_called_with(150, 100, duration=0.2)

    @patch('pyautogui.size')
    @patch('pyautogui.moveTo')
    @patch('pyautogui.position')
    def test_move_cursor_boundaries(self, mock_position, mock_move, mock_size):
        mock_size.return_value = (1920, 1080)
        
        mock_position.return_value = (10, 10)
        self.controller.move_cursor("left", 50)
        mock_move.assert_called_with(0, 10, duration=0.2)
        
        mock_move.reset_mock()
        mock_position.return_value = (100, 10)
        self.controller.move_cursor("up", 50)
        mock_move.assert_called_with(100, 0, duration=0.2)
        
        mock_move.reset_mock()
        mock_position.return_value = (1910, 100)
        self.controller.move_cursor("right", 50)
        mock_move.assert_called_with(1920, 100, duration=0.2)
        
        mock_move.reset_mock()
        mock_position.return_value = (100, 1070)
        self.controller.move_cursor("down", 50)
        mock_move.assert_called_with(100, 1080, duration=0.2)

    @patch('pyautogui.click')
    @patch('pyautogui.rightClick')
    @patch('pyautogui.doubleClick')
    def test_click_types(self, mock_double, mock_right, mock_left):
        self.controller.click("left")
        mock_left.assert_called_once()
        
        self.controller.click("right")
        mock_right.assert_called_once()
        
        self.controller.click("double")
        mock_double.assert_called_once()

    @patch('pyautogui.scroll')
    def test_scroll_directions(self, mock_scroll):
        self.controller.scroll("up", 3)
        mock_scroll.assert_called_with(3)
        
        mock_scroll.reset_mock()
        self.controller.scroll("down", 5)
        mock_scroll.assert_called_with(-5)

    @patch('pyautogui.position')
    def test_get_and_show_position(self, mock_position, capsys):
        mock_position.return_value = (100, 200)
        
        pos = self.controller.get_position()
        assert pos == (100, 200)
        
        self.controller.show_cursor_position()
        captured = capsys.readouterr()
        assert "Cursor position: (100, 200)" in captured.out

    @patch('sys.platform', 'darwin')
    @patch('pyautogui.moveTo')
    @patch('pyautogui.position')
    def test_highlight_cursor_macos(self, mock_position, mock_move):
        mock_position.return_value = (100, 100)
        self.controller.highlight_cursor()
        assert mock_move.call_count == 3

    @patch('sys.platform', 'linux')
    @patch('threading.Thread')
    @patch('pyautogui.position')
    def test_highlight_cursor_linux(self, mock_position, mock_thread):
        mock_position.return_value = (100, 100)
        self.controller.highlight_cursor()
        mock_thread.assert_called_once()

    @patch('pyautogui.position', return_value=(0, 0))
    @patch('pyautogui.moveTo')
    def test_move_cursor_unknown_direction(self, mock_move, mock_pos):
        self.controller.move_cursor("diagonal", 25)
        mock_move.assert_not_called()

    @patch('sys.platform', 'darwin')
    @patch('pyautogui.position', side_effect=Exception("boom"))
    def test_highlight_cursor_macos_exception(self, mock_position):
        # Should swallow exceptions and not raise
        self.controller.highlight_cursor()

    @patch('sys.platform', 'linux')
    @patch('pyautogui.position', return_value=(200, 200))
    @patch('tkinter.Canvas')
    @patch('tkinter.Tk')
    def test_highlight_cursor_linux_draws(self, mock_tk, mock_canvas, mock_position):
        fake_root = MagicMock()
        mock_tk.return_value = fake_root

        fake_canvas = MagicMock()
        mock_canvas.return_value = fake_canvas

        class FakeThread:
            def __init__(self, target=None, daemon=None):
                self.target = target
            def start(self):
                if self.target:
                    self.target()

        with patch('threading.Thread', FakeThread):
            self.controller.highlight_cursor()

        mock_canvas.assert_called()
        fake_canvas.create_oval.assert_called()
