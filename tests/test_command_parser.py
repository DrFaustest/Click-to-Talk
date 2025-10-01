"""
Tests for command_parser.py
"""

import pytest
from unittest.mock import MagicMock
from command_parser import CommandParser
from config import Config


class TestCommandParser:
    def setup_method(self):
        """Setup before each test"""
        self.config = Config()
        self.parser = CommandParser(self.config)
        self.mock_mouse = MagicMock()
        self.parser.set_mouse_controller(self.mock_mouse)

    def test_parse_movement_command_up(self):
        """Test parsing 'move up' command"""
        self.parser.parse_command("move up")
        self.mock_mouse.move_cursor.assert_called_once_with("up", 50)

    def test_parse_movement_command_with_distance(self):
        """Test parsing movement command with distance"""
        self.parser.parse_command("move up 100")
        self.mock_mouse.move_cursor.assert_called_once_with("up", 100)

    def test_parse_movement_command_down(self):
        """Test parsing 'move down' command"""
        self.parser.parse_command("move down")
        self.mock_mouse.move_cursor.assert_called_once_with("down", 50)

    def test_parse_movement_command_left(self):
        """Test parsing 'move left' command"""
        self.parser.parse_command("move left")
        self.mock_mouse.move_cursor.assert_called_once_with("left", 50)

    def test_parse_movement_command_right(self):
        """Test parsing 'move right' command"""
        self.parser.parse_command("move right")
        self.mock_mouse.move_cursor.assert_called_once_with("right", 50)

    def test_parse_click_command_left(self):
        """Test parsing left click command"""
        self.parser.parse_command("click")
        self.mock_mouse.click.assert_called_once_with("left")

    def test_parse_click_command_right(self):
        """Test parsing right click command"""
        self.parser.parse_command("right click")
        self.mock_mouse.click.assert_called_once_with("right")

    def test_parse_click_command_double(self):
        """Test parsing double click command"""
        self.parser.parse_command("double click")
        self.mock_mouse.click.assert_called_once_with("double")

    def test_parse_scroll_command_up(self):
        """Test parsing scroll up command"""
        self.parser.parse_command("scroll up")
        self.mock_mouse.scroll.assert_called_once_with("up")

    def test_parse_scroll_command_down(self):
        """Test parsing scroll down command"""
        self.parser.parse_command("scroll down")
        self.mock_mouse.scroll.assert_called_once_with("down")

    def test_parse_position_command(self):
        """Test parsing position command"""
        self.parser.parse_command("show position")
        self.mock_mouse.show_cursor_position.assert_called_once()

    def test_parse_unrecognized_command(self, capsys):
        """Test parsing unrecognized command"""
        self.parser.parse_command("invalid command")
        captured = capsys.readouterr()
        assert "Unrecognized command: invalid command" in captured.out

    def test_is_movement_command_true(self):
        """Test identifying movement commands"""
        assert self.parser._is_movement_command("move up") == True
        assert self.parser._is_movement_command("go left") == True

    def test_is_movement_command_false(self):
        """Test non-movement commands"""
        assert self.parser._is_movement_command("click") == False
        assert self.parser._is_movement_command("hello") == False

    def test_is_click_command_true(self):
        """Test identifying click commands"""
        assert self.parser._is_click_command("click") == True
        assert self.parser._is_click_command("press") == True

    def test_is_click_command_false(self):
        """Test non-click commands"""
        assert self.parser._is_click_command("move") == False

    def test_is_scroll_command_true(self):
        """Test identifying scroll commands"""
        assert self.parser._is_scroll_command("scroll") == True
        assert self.parser._is_scroll_command("wheel") == True

    def test_is_scroll_command_false(self):
        """Test non-scroll commands"""
        assert self.parser._is_scroll_command("click") == False

    def test_handle_movement_with_invalid_distance(self):
        """Test handling invalid distance in movement command"""
        self.parser.parse_command("move up abc")
        self.mock_mouse.move_cursor.assert_called_once_with("up", 50)  # Should use default

    def test_handle_movement_distance_limit(self):
        """Test distance limit enforcement"""
        # Max distance should be 50 * 5 = 250
        self.parser.parse_command("move up 300")
        self.mock_mouse.move_cursor.assert_called_once_with("up", 250)

    def test_handle_click_error_handling(self):
        """Test error handling in click commands"""
        self.mock_mouse.click.side_effect = Exception("Test error")
        self.parser.parse_command("click")
        # Should not raise exception, just print error

    def test_handle_scroll_error_handling(self):
        """Test error handling in scroll commands"""
        self.mock_mouse.scroll.side_effect = Exception("Test error")
        self.parser.parse_command("scroll up")
        # Should not raise exception, just print error