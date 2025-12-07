"""
Tests for speech_handler.py
"""

import pytest
from unittest.mock import MagicMock, patch
import speech_recognition as sr
from speech_handler import SpeechHandler
from config import Config


class TestSpeechHandler:
    def setup_method(self):
           self.config = Config()
           self.mock_parser = MagicMock()
           self.mock_mouse = MagicMock()
           with patch('speech_recognition.Microphone'), \
               patch.object(sr.Recognizer, 'adjust_for_ambient_noise'):
              self.handler = SpeechHandler(self.config, self.mock_parser, self.mock_mouse)

    def test_initialization(self):
        assert self.handler.config == self.config
        assert self.handler.command_parser == self.mock_parser
        assert self.handler.mouse_controller == self.mock_mouse
        assert self.handler.listening == False
        assert self.handler.stop_callback is None

    def test_set_stop_callback(self):
        mock_callback = MagicMock()
        self.handler.set_stop_callback(mock_callback)
        assert self.handler.stop_callback == mock_callback

    def test_start_listening_already_listening(self, capsys):
        self.handler.listening = True
        self.handler.start_listening()
        captured = capsys.readouterr()
        assert "Already listening" in captured.out

    def test_stop_listening(self):
        self.handler.listening = True
        self.handler.stop_listening()
        assert self.handler.listening == False

    def test_start_listening_already_listening_noop(self):
        self.handler.listening = True
        with patch.object(self.handler.recognizer, 'listen') as mock_listen:
            self.handler.start_listening()
        mock_listen.assert_not_called()

    @patch('speech_recognition.Microphone')
    @patch.object(sr.Recognizer, 'adjust_for_ambient_noise')
    def test_start_listening_stop_command(self, mock_adjust, mock_mic):
        mock_source = MagicMock()
        mock_mic.return_value.__enter__.return_value = mock_source

        handler = SpeechHandler(self.config, self.mock_parser, self.mock_mouse)
        handler.stop_callback = MagicMock()

        handler.recognizer.listen = MagicMock(return_value="audio")
        handler.recognizer.recognize_google = MagicMock(return_value="stop")

        handler.start_listening()

        handler.stop_callback.assert_called_once()
        assert handler.listening is False

    @patch('speech_recognition.Microphone')
    @patch.object(sr.Recognizer, 'adjust_for_ambient_noise')
    def test_start_listening_error_branches(self, mock_adjust, mock_mic):
        mock_source = MagicMock()
        mock_mic.return_value.__enter__.return_value = mock_source

        handler = SpeechHandler(self.config, self.mock_parser, self.mock_mouse)

        calls = {'count': 0}

        def listen_side_effect(*args, **kwargs):
            calls['count'] += 1
            if calls['count'] == 1:
                raise sr.WaitTimeoutError()
            if calls['count'] >= 4:
                handler.listening = False
            return f"audio{calls['count']}"

        handler.recognizer.listen = MagicMock(side_effect=listen_side_effect)
        handler.recognizer.recognize_google = MagicMock(side_effect=[
            sr.UnknownValueError(),
            sr.RequestError("boom"),
            Exception("other"),
        ])

        handler.start_listening()

        assert handler.recognizer.listen.call_count >= 4
