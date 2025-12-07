# Testing Guide

## Overview

Click-to-Talk includes a comprehensive test suite with **67 tests** achieving **95% code coverage**. Tests are designed to work in headless environments (CI/CD) using xvfb for GUI dependencies.

## Running Tests

### Full Suite with Coverage

Run all tests and generate a coverage report:

```bash
xvfb-run -a python -m pytest tests/ --cov=. --cov-report=term
```

### Quick Test Run (No Coverage)

For faster feedback without coverage metrics:

```bash
xvfb-run -a python -m pytest tests/ -q
```

### Run Specific Test File

Test a single module (e.g., command parser):

```bash
xvfb-run -a python -m pytest tests/test_command_parser.py -v
```

### Run with HTML Coverage Report

Generate a detailed HTML coverage report:

```bash
xvfb-run -a python -m pytest tests/ --cov=. --cov-report=html
```

Then open `htmlcov/index.html` in a browser.

## Test Coverage Summary

### Latest Results (Headless)

- **Total:** 67 passed, 0 failed
- **Overall Coverage:** 95% (1268 statements, 69 missed)
- **Execution Time:** ~1.5 seconds

### Module Breakdown

| Module | Lines | Coverage | Status |
|--------|-------|----------|--------|
| `config.py` | 24 | 100% | ✓ Complete |
| `keyboard_controller.py` | 16 | 100% | ✓ Complete |
| `setup.py` | 6 | 100% | ✓ Complete |
| `window_manager.py` | 53 | 98% | ✓ Excellent |
| `speech_handler.py` | 55 | 98% | ✓ Excellent |
| `command_parser.py` | 161 | 98% | ✓ Excellent |
| `mouse_controller.py` | 90 | 93% | ✓ Very Good |
| `main.py` | 218 | 75% | ⚠ Partial (GUI-heavy) |

### Test File Coverage

All test files achieve 95–100% coverage:
- `test_config.py`: 100%
- `test_keyboard_controller.py`: 100%
- `test_mouse_controller.py`: 100%
- `test_speech_handler.py`: 100%
- `test_window_manager.py`: 100%
- `test_setup.py`: 95%
- `test_main.py`: 97%
- `test_command_parser.py`: 100%

## Test Organization

### Core Business Logic (98–100% coverage)

- **Config Tests:** Default values, command mappings, structure validation
- **Command Parser Tests:** 23 tests covering movement, clicks, scroll, keyboard shortcuts, browser commands, panel controls, error handling
- **Keyboard Controller Tests:** 7 tests for typing, key presses, hotkey combinations, modifier aliases
- **Window Manager Tests:** 10 tests for URL resolution, cross-platform browser launching
- **Setup Tests:** Validates setup.py file reads and setuptools invocation

### Voice & Audio (98% coverage)

- **Speech Handler Tests:** 10 tests for initialization, listening flow, stop commands, error branches (timeout/unknown/request errors)

### Mouse & GUI (93% coverage for mouse, 75% for main)

- **Mouse Controller Tests:** 10 tests for movement, boundaries, click types, scrolling, cursor highlighting
- **Main App Tests:** 7 tests for app initialization, controller wiring, stop callbacks, GUI loop (mocked to avoid hangs)

## Blind Spots & Limitations

### What Is NOT Tested

1. **Real GUI Event Loop**
   - The Tkinter event loop in `main.py` is heavily mocked
   - Panel animations, slide dynamics, and drag events are not exercised
   - Auto-hide timer and touch tracking are not validated in live form

2. **Actual Mouse/Keyboard I/O**
   - PyAutoGUI calls to move the mouse or press keys are mocked
   - No verification that mouse actually moves or keys are sent to the OS
   - Only that the correct calls are made to the library

3. **Platform-Specific Behaviors**
   - macOS `open -a` browser launch is simulated via mock
   - Windows `Popen` for Chrome is mocked
   - Linux `webbrowser.open()` is mocked
   - Not tested on actual macOS, Windows, or Linux systems

4. **Live Speech Recognition**
   - Microphone input is mocked
   - Google Speech Recognition API is not actually called
   - Audio capture and processing are simulated

5. **Hardware Dependencies**
   - Actual microphone hardware not required
   - Display/cursor position queries are mocked
   - Threading timing and concurrency are simplified

### Why These Limits Exist

- **Headless Environment:** CI/CD servers typically lack audio devices and displays
- **Determinism:** Mocking ensures tests are repeatable and fast
- **Isolation:** Tests should not depend on external services (Google Speech API)
- **Safety:** Real mouse/keyboard control in automated tests is dangerous
- **Cost:** Live testing would be slow and resource-intensive

### Recommended Integration Testing

For comprehensive validation, consider:

1. **Manual Testing**
   - Run `python main.py` on target OS
   - Verify speech recognition with actual microphone
   - Test mouse movement and click actions visually

2. **Platform Testing**
   - Test on macOS, Windows, and Linux systems
   - Verify browser launching works correctly
   - Confirm GUI panel behavior matches design

3. **Accessibility Testing**
   - User testing with motor-impaired individuals
   - Voice command clarity and responsiveness
   - Panel usability and visibility

## Test Implementation Details

### Mocking Strategy

Tests use `unittest.mock` extensively:

```python
from unittest.mock import patch, MagicMock

# Example: Mock speech recognition
with patch('speech_recognition.Microphone'), \
     patch.object(sr.Recognizer, 'adjust_for_ambient_noise'):
    handler = SpeechHandler(config, parser, mouse)
```

### Headless GUI Testing

GUI tests use dummy widget classes and patched Tk components:

```python
monkeypatch.setattr('main.tk.Tk', lambda: DummyRoot())
monkeypatch.setattr('main.ttk.Frame', lambda *a, **k: DummyWidget())
```

### Platform Simulation

Platform-specific code is tested via `@patch('sys.platform', 'darwin')`:

```python
@patch('sys.platform', 'darwin')
def test_macos_behavior(self):
    # Test macOS-specific code path
    pass

@patch('sys.platform', 'win32')
def test_windows_behavior(self):
    # Test Windows-specific code path
    pass
```

## Continuous Integration

The test suite is designed for CI environments:

- **No GUI Display Required:** Uses xvfb virtual framebuffer
- **No Audio Hardware:** All microphone access is mocked
- **Fast Execution:** ~1.5 seconds total runtime
- **Deterministic:** No flakiness or timing dependencies
- **Portable:** Runs on any Linux/Unix system with xvfb

### GitHub Actions Example

```yaml
- name: Run Tests
  run: |
    xvfb-run -a python -m pytest tests/ --cov=. --cov-report=term
```

## Debugging Tests

### Run with Verbose Output

```bash
xvfb-run -a python -m pytest tests/ -v
```

### Stop at First Failure

```bash
xvfb-run -a python -m pytest tests/ --maxfail=1
```

### Show Print Statements

```bash
xvfb-run -a python -m pytest tests/ -s
```

### Run Single Test

```bash
xvfb-run -a python -m pytest tests/test_command_parser.py::TestCommandParser::test_movement_commands -v
```

## Future Improvements

1. **Increase `main.py` Coverage:** Add more GUI integration tests (currently 75%)
2. **Mock Audio Playback:** Test audio error scenarios more thoroughly
3. **Performance Tests:** Benchmark command parsing and mouse movement latency
4. **Accessibility Audit:** Automated checks for keyboard navigation and screen reader compatibility
5. **E2E Tests:** Spawn actual subprocess and pipe voice commands for true integration testing

---

**Last Updated:** December 7, 2025  
**Test Suite Version:** 67 tests, 95% coverage
