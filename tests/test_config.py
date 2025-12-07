"""
Tests for config.py
"""

import pytest
from config import Config


class TestConfig:
    def test_config_initialization(self):
        config = Config()
        assert config.default_move_distance == 50
        assert config.move_duration == 0.2
        assert config.mouse_pause == 0.1
        assert config.energy_threshold == 300
        assert config.pause_threshold == 0.8
        assert config.phrase_time_limit == 5
        assert config.listen_timeout == 5

    def test_movement_commands_structure(self):
        config = Config()
        assert isinstance(config.movement_commands, dict)
        assert len(config.movement_commands) == 4
        assert all(direction in config.movement_commands for direction in ["up", "down", "left", "right"])
        assert isinstance(config.click_commands, dict)
        assert len(config.click_commands) == 3
        assert all(cmd in config.click_commands for cmd in ["left", "right", "double"])
        assert isinstance(config.scroll_commands, dict)
        assert len(config.scroll_commands) == 2
        assert all(direction in config.scroll_commands for direction in ["up", "down"])

    def test_stop_commands_list(self):
        config = Config()
        assert isinstance(config.stop_commands, list)
        assert len(config.stop_commands) == 4
        assert all(cmd in config.stop_commands for cmd in ["stop", "quit", "exit"])