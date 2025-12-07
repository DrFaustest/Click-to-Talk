"""
Tests for main.py
"""

import pytest
from unittest.mock import MagicMock, patch
from main import ClickToTalkApp, main


class TestClickToTalkApp:
    def setup_method(self):
        with patch('main.SpeechHandler') as mock_speech:
            mock_speech_inst = MagicMock()
            mock_speech.return_value = mock_speech_inst
            mock_speech_inst.listening = False
            self.app = ClickToTalkApp()
            self.app.speech_handler = mock_speech_inst

    def test_initialization(self):
        assert self.app.config is not None
        assert self.app.mouse_controller is not None
        assert self.app.command_parser is not None
        assert self.app.keyboard_controller is not None
        assert self.app.window_manager is not None
        assert self.app.speech_handler is not None
        assert self.app.running == False
        assert self.app.root is None

    def test_controllers_wired_correctly(self):
        assert self.app.command_parser.mouse_controller == self.app.mouse_controller
        assert self.app.command_parser.keyboard_controller == self.app.keyboard_controller
        assert self.app.command_parser.window_manager == self.app.window_manager

    def test_stop(self):
        self.app.running = True
        self.app.stop()
        assert self.app.running == False
        self.app.speech_handler.stop_listening.assert_called()

    def test_start_runs_minimal_loop(self, monkeypatch):
        # Dummy root to avoid real Tk loop
        class DummyRoot:
            def __init__(self):
                self._geom = "320x420+0+0"
            def overrideredirect(self, *_):
                return None
            def attributes(self, *_):
                return None
            def winfo_screenwidth(self):
                return 1920
            def winfo_screenheight(self):
                return 1080
            def geometry(self, g=None):
                if g:
                    self._geom = g
                return self._geom
            def winfo_pointerx(self):
                return 0
            def winfo_pointery(self):
                return 0
            def update_idletasks(self):
                return None
            def update(self):
                return None
            def bind(self, *_, **__):
                return None
            def destroy(self):
                return None

        class DummyWidget:
            def __init__(self, *_, **__):
                pass
            def pack(self, *_, **__):
                return None
            def place(self, *_, **__):
                return None
            def bind(self, *_, **__):
                return None
            def set(self, *_, **__):
                return None

        dummy_root = DummyRoot()

        # Patch tk/ttk pieces to avoid GUI
        monkeypatch.setattr('main.tk.Tk', lambda: dummy_root)
        monkeypatch.setattr('main.tk.StringVar', lambda value=None: MagicMock(set=lambda v: None))
        monkeypatch.setattr('main.ttk.Frame', lambda *a, **k: DummyWidget())
        monkeypatch.setattr('main.ttk.Label', lambda *a, **k: DummyWidget())
        monkeypatch.setattr('main.ttk.Button', lambda *a, **k: DummyWidget())
        monkeypatch.setattr('main.ttk.Scale', lambda *a, **k: DummyWidget())
        monkeypatch.setattr('main.ttk.Combobox', lambda *a, **k: DummyWidget())

        # Prevent speech thread from starting and force loop exit via sleep
        monkeypatch.setattr('main.threading.Thread', lambda *a, **k: MagicMock(start=lambda: None))

        # Mock SpeechHandler to avoid microphone
        with patch('main.SpeechHandler') as mock_speech:
            handler = MagicMock()
            handler.listening = False
            mock_speech.return_value = handler

            app = ClickToTalkApp()

            def sleep_stop(*_):
                app.running = False
                return None

            monkeypatch.setattr('main.time.sleep', sleep_stop)

            app.start()

            handler.set_stop_callback.assert_called_once()
            handler.stop_listening.assert_called_once()


class TestMainFunction:
    @patch('main.ClickToTalkApp')
    def test_main_success(self, mock_app_class):
        mock_app = MagicMock()
        mock_app_class.return_value = mock_app
        main()
        mock_app_class.assert_called_once()
        mock_app.start.assert_called_once()

    @patch('main.ClickToTalkApp')
    @patch('sys.exit')
    def test_main_exception(self, mock_exit, mock_app_class):
        mock_app_class.side_effect = Exception("Test error")
        main()
        mock_exit.assert_called_once_with(1)

    @patch('main.ClickToTalkApp')
    def test_main_keyboard_interrupt(self, mock_app_class):
        mock_app = MagicMock()
        mock_app_class.return_value = mock_app
        mock_app.start.side_effect = KeyboardInterrupt()
        with pytest.raises(KeyboardInterrupt):
            main()
