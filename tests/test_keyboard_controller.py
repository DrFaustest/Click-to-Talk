"""
Tests for KeyboardController Module
"""

import pytest
from unittest.mock import patch
from keyboard_controller import KeyboardController


class TestKeyboardController:
    def setup_method(self):
        self.controller = KeyboardController(pause=0.05)

    @patch('pyautogui.PAUSE', 0.05)
    def test_initialization(self):
        controller = KeyboardController(pause=0.1)
        assert controller is not None

    @patch('pyautogui.typewrite')
    def test_type_text(self, mock_typewrite):
        self.controller.type_text("hello world")
        mock_typewrite.assert_called_once_with("hello world", interval=0.01)

    @patch('pyautogui.press')
    def test_press_single_key(self, mock_press):
        self.controller.press_keys("enter")
        mock_press.assert_called_once_with("enter")

    @patch('pyautogui.press')
    def test_press_key_aliases(self, mock_press):
        self.controller.press_keys("escape")
        mock_press.assert_called_once_with("esc")
        mock_press.reset_mock()
        self.controller.press_keys("return")
        mock_press.assert_called_once_with("enter")

    @patch('pyautogui.hotkey')
    def test_press_hotkey_combinations(self, mock_hotkey):
        self.controller.press_keys("ctrl c")
        mock_hotkey.assert_called_with("ctrl", "c")
        mock_hotkey.reset_mock()
        self.controller.press_keys("ctrl shift tab")
        mock_hotkey.assert_called_with("ctrl", "shift", "tab")

    @patch('pyautogui.hotkey')
    def test_press_modifier_aliases(self, mock_hotkey):
        self.controller.press_keys("control c")
        mock_hotkey.assert_called_with("ctrl", "c")
        mock_hotkey.reset_mock()
        self.controller.press_keys("cmd l")
        mock_hotkey.assert_called_with("command", "l")
        mock_hotkey.reset_mock()
        self.controller.press_keys("windows tab")
        mock_hotkey.assert_called_with("win", "tab")

    @patch('pyautogui.hotkey')
    def test_press_keys_normalization(self, mock_hotkey):
        self.controller.press_keys("CTRL   SHIFT   T")
        mock_hotkey.assert_called_once_with("ctrl", "shift", "t")
