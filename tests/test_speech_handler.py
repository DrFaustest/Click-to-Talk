"""
Tests for speech_handler.py
"""

import pytest
from unittest.mock import MagicMock, patch, call
from speech_handler import SpeechHandler
from config import Config


class TestSpeechHandler:
    def setup_method(self):
        """Setup before each test"""
        self.config = Config()
        self.mock_parser = MagicMock()
        self.mock_mouse = MagicMock()
        self.handler = SpeechHandler(self.config, self.mock_parser, self.mock_mouse)

    @patch('speech_recognition.Recognizer')
    @patch('speech_recognition.Microphone')
    def test_initialization(self, mock_microphone, mock_recognizer):
        """Test SpeechHandler initialization"""
        mock_recognizer_instance = MagicMock()
        mock_recognizer.return_value = mock_recognizer_instance
        mock_microphone_instance = MagicMock()
        mock_microphone.return_value = mock_microphone_instance

        handler = SpeechHandler(self.config, self.mock_parser, self.mock_mouse)

        mock_recognizer.assert_called_once()
        mock_microphone.assert_called_once()
        mock_recognizer_instance.adjust_for_ambient_noise.assert_called_once()

    @patch('speech_recognition.Recognizer')
    @patch('speech_recognition.Microphone')
    @patch('builtins.print')
    def test_start_listening_success(self, mock_print, mock_microphone, mock_recognizer):
        """Test successful speech recognition"""
        # Setup mocks
        mock_recognizer_instance = MagicMock()
        mock_recognizer_instance.recognize_google.return_value = "move up"
        mock_recognizer.return_value = mock_recognizer_instance

        mock_microphone_instance = MagicMock()
        mock_microphone.return_value = mock_microphone_instance

        mock_source = MagicMock()
        mock_microphone_instance.__enter__.return_value = mock_source

        handler = SpeechHandler(self.config, self.mock_parser, self.mock_mouse)
        handler.listening = True

        # Mock the listen method to return after one iteration
        mock_recognizer_instance.listen.return_value = MagicMock()

        # Run start_listening briefly
        import threading
        import time

        def stop_after_delay():
            time.sleep(0.1)
            handler.listening = False

        stop_thread = threading.Thread(target=stop_after_delay)
        stop_thread.start()

        handler.start_listening()

        # Verify command was parsed
        self.mock_parser.parse_command.assert_called_with("move up")

    @patch('speech_recognition.Recognizer')
    @patch('speech_recognition.Microphone')
    def test_start_listening_recognition_error(self, mock_microphone, mock_recognizer):
        """Test handling of recognition errors"""
        mock_recognizer_instance = MagicMock()
        mock_recognizer_instance.listen.return_value = MagicMock()
        mock_recognizer_instance.recognize_google.side_effect = Exception("Recognition failed")
        mock_recognizer.return_value = mock_recognizer_instance

        mock_microphone_instance = MagicMock()
        mock_microphone.return_value = mock_microphone_instance

        handler = SpeechHandler(self.config, self.mock_parser, self.mock_mouse)
        handler.listening = True  # Start with listening = True

        # Mock the microphone context manager
        mock_source = MagicMock()
        mock_microphone_instance.__enter__.return_value = mock_source

        # Use a thread to stop listening after a short delay
        import threading
        import time

        def stop_after_delay():
            time.sleep(0.1)
            handler.listening = False

        stop_thread = threading.Thread(target=stop_after_delay)
        stop_thread.start()

        # Should not raise exception
        handler.start_listening()