"""
Tests for config.py
"""

import pytest
from config import Config


class TestConfig:
    def test_config_initialization(self):
        """Test Config class initializes with correct default values"""
        config = Config()

        # Mouse settings
        assert config.default_move_distance == 50
        assert config.move_duration == 0.2
        assert config.mouse_pause == 0.1

        # Speech settings
        assert config.energy_threshold == 300
        assert config.pause_threshold == 0.8
        assert config.phrase_time_limit == 5
        assert config.listen_timeout == 5

        # Command mappings
        assert "up" in config.movement_commands
        assert "down" in config.movement_commands
        assert "left" in config.movement_commands
        assert "right" in config.movement_commands

        assert "left" in config.click_commands
        assert "right" in config.click_commands
        assert "double" in config.click_commands

        assert "up" in config.scroll_commands
        assert "down" in config.scroll_commands

        assert "stop" in config.stop_commands
        assert "quit" in config.stop_commands
        assert "exit" in config.stop_commands

    def test_movement_commands_structure(self):
        """Test movement commands dictionary structure"""
        config = Config()
        assert isinstance(config.movement_commands, dict)
        assert len(config.movement_commands) == 4
        for direction, keywords in config.movement_commands.items():
            assert isinstance(keywords, list)
            assert len(keywords) > 0

    def test_click_commands_structure(self):
        """Test click commands dictionary structure"""
        config = Config()
        assert isinstance(config.click_commands, dict)
        assert len(config.click_commands) == 3

    def test_scroll_commands_structure(self):
        """Test scroll commands dictionary structure"""
        config = Config()
        assert isinstance(config.scroll_commands, dict)
        assert len(config.scroll_commands) == 2

    def test_stop_commands_list(self):
        """Test stop commands list"""
        config = Config()
        assert isinstance(config.stop_commands, list)
        assert len(config.stop_commands) == 4