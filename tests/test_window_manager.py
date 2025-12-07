"""
Tests for WindowManager Module
"""

import pytest
from unittest.mock import patch
from window_manager import WindowManager


class TestWindowManager:
    def setup_method(self):
        self.site_aliases = {
            "gmail": "https://mail.google.com",
            "youtube": "https://www.youtube.com"
        }
        self.manager = WindowManager(
            site_aliases=self.site_aliases,
            preferred_browser="Google Chrome"
        )

    def test_initialization(self):
        assert self.manager.site_aliases == self.site_aliases
        assert self.manager.preferred_browser == "Google Chrome"
        
        manager = WindowManager()
        assert manager.site_aliases == {}
        assert manager.preferred_browser is None

    def test_to_url_resolution(self):
        assert self.manager._to_url("gmail") == "https://mail.google.com"
        assert self.manager._to_url("GMAIL") == "https://mail.google.com"
        assert self.manager._to_url("  gmail  ") == "https://mail.google.com"
        assert self.manager._to_url("example.com") == "https://example.com"
        assert self.manager._to_url("http://example.com") == "http://example.com"
        assert self.manager._to_url("https://example.com") == "https://example.com"
        assert self.manager._to_url("browser") is None
        assert self.manager._to_url("chrome") is None

    @patch('window_manager.WindowManager.open_url')
    @patch('window_manager.WindowManager.open_browser')
    def test_open_method_routing(self, mock_browser, mock_url):
        self.manager.open("gmail")
        mock_url.assert_called_once_with("https://mail.google.com")
        
        mock_url.reset_mock()
        self.manager.open("browser")
        mock_browser.assert_called_once()

    @patch('subprocess.run')
    @patch('sys.platform', 'darwin')
    def test_open_url_macos(self, mock_run):
        self.manager.open_url("https://example.com")
        mock_run.assert_called_once_with(["open", "-a", "Google Chrome", "https://example.com"])
        
        mock_run.reset_mock()
        manager = WindowManager()
        manager.open_url("https://example.com")
        mock_run.assert_called_once_with(["open", "https://example.com"])

    @patch('webbrowser.open')
    @patch('subprocess.Popen')
    @patch('sys.platform', 'win32')
    def test_open_url_windows(self, mock_popen, mock_webbrowser):
        manager = WindowManager(preferred_browser="chrome")
        manager.open_url("https://example.com")
        mock_popen.assert_called_once_with(["chrome", "https://example.com"])
        
        mock_popen.reset_mock()
        mock_popen.side_effect = FileNotFoundError
        manager.open_url("https://example.com")
        mock_webbrowser.assert_called_once_with("https://example.com")

    @patch('webbrowser.open')
    @patch('sys.platform', 'linux')
    def test_open_url_linux(self, mock_webbrowser):
        manager = WindowManager()
        manager.open_url("https://example.com")
        mock_webbrowser.assert_called_once_with("https://example.com")

    @patch('subprocess.run')
    @patch('sys.platform', 'darwin')
    def test_open_browser_macos(self, mock_run):
        self.manager.open_browser()
        mock_run.assert_called_once_with(["open", "-a", "Google Chrome"])
        
        mock_run.reset_mock()
        manager = WindowManager()
        manager.open_browser()
        mock_run.assert_called_once_with(["open", "-a", "Safari"])

    @patch('webbrowser.open')
    @patch('subprocess.Popen')
    @patch('sys.platform', 'win32')
    def test_open_browser_windows(self, mock_popen, mock_webbrowser):
        manager = WindowManager(preferred_browser="chrome")
        manager.open_browser()
        mock_popen.assert_called_once_with(["chrome"])
        
        mock_popen.reset_mock()
        mock_popen.side_effect = FileNotFoundError
        manager.open_browser()
        mock_webbrowser.assert_called_once_with("about:blank")

    @patch('webbrowser.open')
    @patch('sys.platform', 'linux')
    def test_open_browser_linux(self, mock_webbrowser):
        manager = WindowManager()
        manager.open_browser()
        mock_webbrowser.assert_called_once_with("about:blank")
