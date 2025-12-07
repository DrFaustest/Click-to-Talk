# Architecture & Technical Design

This document describes the technical architecture, design patterns, and system components of Click-to-Talk.

## System Overview

Click-to-Talk is a Python desktop application that converts speech input into mouse and keyboard control. The application follows a modular, event-driven architecture with clear separation of concerns.

```
┌─────────────────────────────────────────────────────────┐
│                    Tkinter GUI                          │
│    (Panel UI, Start/Stop buttons, Sliders)              │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────┴──────────────────────────────────────┐
│              Main Application (main.py)                 │
│         (Event loop, threading, lifecycle)              │
└──────────────────┬──────────────────────────────────────┘
                   │
    ┌──────────────┼──────────────┬──────────────┐
    │              │              │              │
┌───▼────┐   ┌────▼──────┐  ┌───▼───────┐  ┌──▼─────────┐
│  Voice  │   │ Command   │  │  Mouse    │  │  Keyboard  │
│ Input   │   │ Parser    │  │ Controller│  │ Controller │
│         │   │           │  │           │  │            │
│Speech   │───│Recognizer │──│ PyAutoGUI │──│ PyAutoGUI  │
│         │   │           │  │           │  │            │
└────┬────┘   └───────────┘  └───────────┘  └────────────┘
     │
┌────▼────────────────────────────────────────┐
│         Configuration (config.py)           │
│  (Commands, Distances, Settings)            │
└─────────────────────────────────────────────┘
```

## Module Structure

### 1. **main.py** – Application Entry Point

**Responsibility:** Orchestrates the entire application lifecycle, GUI creation, and threading.

**Key Components:**
* `ClickToTalkApp` class – Main application controller
* Tkinter window initialization with always-on-top panel
* Threading model for GUI updates and voice listening
* Event loop integration with voice input

**Key Methods:**
```python
class ClickToTalkApp:
    def __init__(self, root, config):
        """Initialize app with Tkinter root and config"""
        
    def start_listening(self):
        """Begin voice input thread"""
        
    def stop_listening(self):
        """Pause voice input"""
        
    def listen_loop(self):
        """Background thread: listens for speech, parses commands"""
        
    def handle_command(self, command):
        """Process parsed command (mouse/keyboard action)"""
```

**Threading Model:**
* Main thread: GUI event loop (Tkinter)
* Listener thread: Continuous speech recognition and command processing
* GUI updates are queued back to main thread via `after()` to avoid deadlocks

**GUI Features:**
* Sliding dock panel (left/right edge)
* Start/Stop Listening buttons
* Movement distance slider (1–500px)
* Commands Reference dropdown (view-only)
* Auto-hide timer (30 seconds)
* Always-on-top window (platform-dependent)

### 2. **speech_handler.py** – Voice Input Processing

**Responsibility:** Manages microphone access, speech recognition, and error handling.

**Key Components:**
* `SpeechHandler` class – Encapsulates speech recognition
* Google Speech Recognition API integration
* Timeout and error handling
* Ambient noise adjustment

**Key Methods:**
```python
class SpeechHandler:
    def __init__(self, config):
        """Initialize recognizer and microphone"""
        
    def listen(self, timeout=10):
        """Capture audio and return recognized text"""
        # Returns: (text: str, success: bool, error: str|None)
        
    def stop(self):
        """Release microphone resource"""
```

**Error Handling:**
* `UnknownValueError` – Unclear speech (returns empty string)
* `RequestError` – Google API unreachable (returns error message)
* `Timeout` – No speech detected within timeout period
* `Microphone not found` – No audio device detected

**Dependencies:**
* `speech_recognition` library (Google Speech API)
* `pyttsx3` (optional text-to-speech)
* Python's `threading` module

### 3. **command_parser.py** – Speech-to-Action Translation

**Responsibility:** Parses recognized text into executable commands.

**Key Components:**
* `CommandParser` class – Converts speech text to action dictionaries
* Command patterns (movement, clicks, keyboard, browser navigation)
* Natural language variations (synonyms)
* Error detection and validation

**Key Methods:**
```python
class CommandParser:
    def __init__(self, config):
        """Initialize parser with command mappings"""
        
    def parse(self, text):
        """Convert speech text to command dict"""
        # Returns: {
        #     'type': 'movement|click|scroll|keyboard|browser|gui_control|stop',
        #     'direction': 'up|down|left|right|...',
        #     'distance': int,
        #     'key': str,
        #     'action': str,
        #     'url': str,
        #     ...
        # }
```

**Command Types:**
1. **Movement:** `move [direction] [distance]`
2. **Click:** `[left|right|double] click`
3. **Scroll:** `scroll [up|down]`
4. **Keyboard:** `press [key+modifiers]`, `type [text]`
5. **Browser:** `open [url]`, `new tab`, `refresh`
6. **GUI Control:** `minimize panel`, `show panel`
7. **Stop:** `stop`, `quit`, `exit`

**Parsing Strategy:**
* Case-insensitive matching
* Regex patterns for flexible input (e.g., "move up 100" or "move 100 up")
* Synonym support (e.g., "click" = "left click")
* Distance extraction from natural numbers

**Design Pattern:** Strategy pattern for different command types

### 4. **mouse_controller.py** – Mouse Control

**Responsibility:** Encapsulates mouse movement and clicking.

**Key Components:**
* `MouseController` class – Wrapper around PyAutoGUI
* Screen boundary enforcement
* Cursor highlighting utility
* Movement safety limits

**Key Methods:**
```python
class MouseController:
    def __init__(self, config):
        """Initialize with config (movement limits, etc.)"""
        
    def move(self, x, y):
        """Move cursor to absolute position (with boundary checks)"""
        
    def move_relative(self, dx, dy):
        """Move cursor by relative offset"""
        
    def click(self, button='left'):
        """Perform mouse click (left, right, or double)"""
        
    def scroll(self, direction):
        """Scroll up or down"""
        
    def get_position(self):
        """Return current cursor position (x, y)"""
        
    def highlight_cursor(self, duration=2):
        """Draw animated ring around cursor"""
```

**Safety Features:**
* **Boundary checking:** Cursor clamped to screen dimensions
* **Distance limits:** Enforces min/max movement per command
* **Failsafe detection:** Checks for cursor at (0, 0) as emergency stop

**Dependencies:**
* `pyautogui` library (cross-platform mouse/keyboard)

### 5. **keyboard_controller.py** – Keyboard Control

**Responsibility:** Encapsulates keyboard input, text typing, and hotkey presses.

**Key Components:**
* `KeyboardController` class – Wrapper around PyAutoGUI keyboard
* Key name normalization
* Modifier key handling (Ctrl, Shift, Alt, Cmd)
* Text typing with safety checks

**Key Methods:**
```python
class KeyboardController:
    def __init__(self, config):
        """Initialize keyboard controller"""
        
    def type_text(self, text):
        """Type a string of text"""
        
    def press_key(self, key):
        """Press a single key"""
        
    def press_combination(self, keys):
        """Press multiple keys as chord (Ctrl+C, Alt+Tab, etc.)"""
```

**Supported Keys:**
* Letters: a-z, A-Z
* Numbers: 0-9
* Navigation: up, down, left, right, home, end, pageup, pagedown
* Editing: delete, backspace, tab
* Functions: f1-f12
* Special: enter, esc, space
* Modifiers: ctrl, shift, alt, cmd

**Design Pattern:** Adapter pattern (wraps PyAutoGUI)

### 6. **window_manager.py** – Browser & Window Control

**Responsibility:** Opens URLs and manages external applications.

**Key Components:**
* `WindowManager` class – Cross-platform URL handling
* Browser detection and launching
* URL validation and normalization
* Platform-specific launch methods

**Key Methods:**
```python
class WindowManager:
    def __init__(self, config):
        """Initialize window manager"""
        
    def open_url(self, url):
        """Open URL in default browser (platform-aware)"""
        
    def resolve_url(self, text):
        """Convert shorthand (gmail, youtube) to full URL"""
```

**Platform Support:**
* **macOS:** Uses `open -a` command
* **Windows:** Uses `webbrowser` module
* **Linux:** Uses `webbrowser` module (xdg-open)

**URL Resolution:**
```
"gmail" → "https://mail.google.com"
"youtube" → "https://www.youtube.com"
"google.com" → "https://www.google.com"
"https://example.com" → "https://example.com" (unchanged)
```

### 7. **config.py** – Configuration & Constants

**Responsibility:** Centralized configuration, command mappings, and constants.

**Key Components:**
* Command pattern definitions
* Default values (movement distance, timeouts, etc.)
* Platform-specific settings
* Constants (window sizes, colors, etc.)

**Example Structure:**
```python
class Config:
    # Movement
    DEFAULT_DISTANCE = 50
    MAX_DISTANCE = 500
    MIN_DISTANCE = 1
    
    # Voice recognition
    RECOGNITION_TIMEOUT = 10
    SPEECH_LANGUAGE = 'en-US'
    
    # GUI
    PANEL_WIDTH = 200
    PANEL_HEIGHT = 300
    AUTO_HIDE_TIME = 30000  # ms
    
    # Commands (regex patterns and actions)
    COMMANDS = {
        'movement': [...],
        'click': [...],
        'keyboard': [...],
        ...
    }
```

## Data Flow Example

**Scenario:** User says "move up 100, click"

```
1. User speaks into microphone
       ↓
2. SpeechHandler.listen() captures audio
       ↓
3. Google Speech API transcribes: "move up 100 click"
       ↓
4. CommandParser.parse() converts to:
   [
     {'type': 'movement', 'direction': 'up', 'distance': 100},
     {'type': 'click', 'button': 'left'}
   ]
       ↓
5. main.py processes each command:
   - MouseController.move_relative(0, -100)
   - MouseController.click('left')
       ↓
6. PyAutoGUI sends OS-level mouse events
       ↓
7. Operating system executes mouse actions
```

## Design Patterns

### 1. **Model-View-Controller (MVC)**
* **Model:** Config, speech handler, command parser
* **View:** Tkinter GUI (main.py)
* **Controller:** ClickToTalkApp (orchestrates interactions)

### 2. **Strategy Pattern**
* Different parsing strategies for different command types
* Pluggable browser handling (macOS vs. Windows vs. Linux)

### 3. **Adapter Pattern**
* MouseController and KeyboardController wrap PyAutoGUI
* Provides clean, domain-specific interface

### 4. **Observer Pattern**
* GUI callbacks trigger action handlers
* Threading model uses callbacks for cross-thread communication

### 5. **Singleton Pattern**
* Config class is effectively a singleton (shared configuration)

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **GUI** | Tkinter (built-in) | Window management, widgets, layout |
| **Voice Input** | `speech_recognition` | Audio capture, Google Speech API |
| **Mouse Control** | `pyautogui` | Cross-platform mouse operations |
| **Keyboard Control** | `pyautogui` | Cross-platform keyboard operations |
| **Text-to-Speech** | `pyttsx3` (optional) | Accessibility feedback |
| **Testing** | `pytest`, `pytest-cov` | Unit tests, coverage analysis |
| **Language** | Python 3.11+ | Programming language |

## Threading & Concurrency

The application uses a **two-threaded model** to prevent GUI freezing:

### Main Thread (Tkinter)
* Runs the GUI event loop
* Handles button clicks, slider changes
* Updates panel display
* **Never blocks** – all I/O is async via `after()`

### Listener Thread
* Runs continuously in background
* Calls `SpeechHandler.listen()` (blocking)
* Parses commands via `CommandParser.parse()`
* Queues GUI updates back to main thread via `root.after()`

### Communication
```python
# Listener thread needs to update GUI
root.after(0, update_gui_function, arg1, arg2)  # Safe
```

**Rationale:** Tkinter is **not thread-safe** for UI updates. Queue operations via `after()` to maintain safety.

## Error Handling Strategy

### Speech Recognition Errors

| Error Type | Cause | Recovery |
|-----------|-------|----------|
| `UnknownValueError` | Speech too unclear | Silently ignore, continue listening |
| `RequestError` | Network/API down | Log error, retry next command |
| `Timeout` | No speech detected | Resume listening automatically |
| `Microphone error` | No audio device | Show error dialog, suggest fix |

### Command Parsing Errors

| Error | Handling |
|-------|----------|
| Unrecognized command | Ignored (no action) |
| Invalid distance | Clamped to min/max range |
| Out-of-bounds movement | Cursor clamped to screen edges |

### GUI Errors

| Error | Handling |
|-------|----------|
| Browser not found | Attempt fallback (xdg-open, etc.) |
| Window manager not available | Graceful degradation |
| Tkinter issues | Logged, app continues |

## Performance Considerations

### Speech Recognition
* **Bottleneck:** Network latency to Google API (~0.5–2 seconds)
* **Optimization:** Local speech recognition (offline) in future

### Mouse Movement
* **Latency:** ~10–50ms per movement command
* **Optimization:** Hardware-level acceleration via PyAutoGUI

### GUI Rendering
* **Panel sliding:** Hardware-accelerated if supported
* **Auto-hide timer:** Configurable via `AUTO_HIDE_TIME`

### Memory Usage
* **Typical footprint:** ~50–100 MB (Tkinter + libraries)
* **Microphone:** Streaming buffer ~1 MB

## Security & Privacy

### Data Handling
* **Speech audio:** Sent to Google Speech Recognition API
* **Mouse/keyboard:** Local processing only
* **URLs:** Sent to browser (normal browsing)
* **No data logging:** Commands are not stored

### Permissions
* **Microphone access:** Required (user grants at OS level)
* **Mouse/keyboard:** No special permissions needed
* **Network:** Internet access required for Google Speech API

### Failsafes
* **Emergency stop:** Move cursor to (0, 0)
* **Timeout:** Listening pauses after 10 seconds of silence
* **Rate limiting:** Commands processed one-at-a-time (no flooding)

## Extending Click-to-Talk

### Adding a New Command Type

1. **Define command pattern in `config.py`:**
   ```python
   COMMANDS = {
       'my_feature': [
           r'^my\s+command\s+(\w+)$',
       ]
   }
   ```

2. **Handle in `command_parser.py`:**
   ```python
   elif 'my_feature' in patterns:
       return {'type': 'my_feature', 'param': match.group(1)}
   ```

3. **Process in `main.py`:**
   ```python
   elif cmd['type'] == 'my_feature':
       self.handle_my_feature(cmd['param'])
   ```

4. **Add tests in `tests/test_command_parser.py`:**
   ```python
   def test_my_feature(self):
       parser = CommandParser(Config())
       cmd = parser.parse('my command test')
       assert cmd['type'] == 'my_feature'
   ```

### Platform-Specific Code

Use `sys.platform` checks:

```python
import sys

if sys.platform == 'darwin':  # macOS
    # macOS-specific code
elif sys.platform == 'win32':  # Windows
    # Windows-specific code
else:  # Linux
    # Linux-specific code
```

All platform checks are tested via mocking in the test suite.

## Future Architecture Improvements

1. **Plugin System:** Allow third-party commands via plugins
2. **Local Speech Recognition:** Offline speech recognition (no network)
3. **Machine Learning:** Intent classification for ambiguous commands
4. **Voice Profiles:** Custom voice models per user
5. **Accessibility APIs:** Integration with OS accessibility frameworks

---

**Last Updated:** December 7, 2025
