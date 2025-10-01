"""
Tests for main.py
"""

import pytest
from unittest.mock import MagicMock, patch
from main import ClickToTalkApp
from config import Config


class TestClickToTalkApp:
    def setup_method(self):
        """Setup before each test"""
        self.app = ClickToTalkApp()

    @patch('main.SpeechHandler')
    @patch('main.MouseController')
    @patch('main.CommandParser')
    @patch('main.Config')
    def test_initialization(self, mock_config, mock_parser, mock_mouse, mock_speech):
        """Test app initialization"""
        mock_config_instance = MagicMock()
        mock_config.return_value = mock_config_instance

        mock_mouse_instance = MagicMock()
        mock_mouse.return_value = mock_mouse_instance

        mock_parser_instance = MagicMock()
        mock_parser.return_value = mock_parser_instance

        mock_speech_instance = MagicMock()
        mock_speech.return_value = mock_speech_instance

        app = ClickToTalkApp()

        # Verify all components are created
        mock_config.assert_called_once()
        mock_mouse.assert_called_once_with(mock_config_instance)
        mock_parser.assert_called_once_with(mock_config_instance)
        mock_speech.assert_called_once_with(mock_config_instance, mock_parser_instance, mock_mouse_instance)

        # Verify mouse controller is set on parser
        mock_parser_instance.set_mouse_controller.assert_called_once_with(mock_mouse_instance)

        # Verify stop callback is set on speech handler
        mock_speech_instance.set_stop_callback.assert_called_once_with(app.stop)

    @patch('main.threading.Thread')
    @patch('main.time.sleep')
    @patch('builtins.print')
    def test_start_and_stop(self, mock_print, mock_sleep, mock_thread):
        """Test starting and stopping the app"""
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance

        # Mock the components
        self.app.speech_handler = MagicMock()
        self.app.running = True  # Start with running = True

        # Mock KeyboardInterrupt to be raised after sleep
        mock_sleep.side_effect = KeyboardInterrupt()

        # Start the app
        self.app.start()

        # Verify thread was created and started
        mock_thread.assert_called_once()
        mock_thread_instance.start.assert_called_once()
        mock_thread_instance.daemon = True

        # Verify speech handler stop was called (from finally block after KeyboardInterrupt)
        self.app.speech_handler.stop_listening.assert_called_once()
        assert self.app.running == False

    @patch('main.ClickToTalkApp')
    @patch('builtins.print')
    def test_main_function_success(self, mock_print, mock_app):
        """Test main function with successful execution"""
        mock_app_instance = MagicMock()
        mock_app.return_value = mock_app_instance

        from main import main
        main()

        mock_app.assert_called_once()
        mock_app_instance.start.assert_called_once()

    @patch('main.ClickToTalkApp')
    @patch('builtins.print')
    @patch('sys.exit')
    def test_main_function_error(self, mock_exit, mock_print, mock_app):
        """Test main function with initialization error"""
        mock_app.side_effect = Exception("Init error")

        from main import main
        main()

        mock_exit.assert_called_once_with(1)