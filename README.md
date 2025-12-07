# Click-to-Talk: Voice Controlled Mouse Navigation

## Overview

**Click-to-Talk** is a Python desktop application that enables voice-controlled mouse navigation for computer use.
This adaptive technology is designed to support individuals with fine-motor and dexterity challenges—such as those affected by Parkinson's disease or declining motor coordination—who struggle with traditional mouse or trackpad use.

By translating voice input into precise mouse movements and clicks, the application reduces both the **gulf of execution** and the **gulf of evaluation**, enabling users to navigate any application or website more effectively and independently.

Click-to-Talk is a human-computer interaction project that demonstrates voice-controlled mouse functionality. Built in Python, it translates spoken commands into real-time cursor movements and clicks using speech recognition and PyAutoGUI. This implementation showcases an accessibility-focused design, modular architecture, and potential for hands-free computing.

## Demo Video

Watch the initial demonstration of Click-to-Talk in action:

[![Click-to-Talk Demo Video](https://img.youtube.com/vi/ZgICXJpQtHA/maxresdefault.jpg)](https://www.youtube.com/watch?v=ZgICXJpQtHA)

**See voice-controlled mouse navigation, command parsing, and accessibility features in real-time.**

---

## Documentation Hub

Complete documentation is organized into dedicated guides:

| Document | Purpose |
|----------|---------|
| **[Installation Guide](docs/INSTALLATION.md)** | Setup instructions for Windows, macOS, and Linux |
| **[Usage Guide](docs/USAGE.md)** | Complete voice commands reference and examples |
| **[Architecture](docs/ARCHITECTURE.md)** | Technical design, module structure, and system overview |
| **[Project Roadmap](docs/ROADMAP.md)** | Development phases, future features, and vision |
| **[Testing Guide](TESTING.md)** | Test suite, coverage details, and CI/CD setup |

## Quick Start

### 1. Install the Application

See the full [**Installation Guide**](docs/INSTALLATION.md) for detailed setup instructions.

**Quick install:**

```bash
git clone https://github.com/DrFaustest/Click-to-Talk.git
cd Click-to-Talk
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
```

### 2. Learn Voice Commands

See the [**Usage Guide**](docs/USAGE.md) for a complete reference of all voice commands.

**Common commands:**
* `"move up 100"` – Move cursor up by 100 pixels
* `"click"` – Left-click at cursor position
* `"scroll down"` – Scroll downward
* `"open gmail"` – Open Gmail in browser
* `"type hello"` – Type the text "hello"
* `"press ctrl c"` – Copy to clipboard

### 3. Understand the System

Curious about how it works? See [**Architecture**](docs/ARCHITECTURE.md) for:
* System design and module structure
* Data flow and threading model
* How to extend with custom commands

## Features

### Voice Control
* **Movement:** Precise cursor control with configurable distance (1–500px)
* **Clicking:** Left, right, and double-click support
* **Scrolling:** Scroll any document or web page
* **Typing:** Dictate text directly into any text field
* **Keyboard:** Press keys, combinations, and shortcuts (Ctrl+C, Alt+Tab, etc.)
* **Browser:** Open websites, manage tabs, navigate pages
* **GUI Control:** Show/hide the control panel with voice

### Accessibility Features
* **Sliding Dock Panel:** Non-intrusive panel that auto-hides after 30 seconds
* **Distance Slider:** Adjust default movement distance (1–500px) for different tasks
* **Cursor Highlighting:** Find your cursor with the "find cursor" command
* **Position Display:** Know exactly where your cursor is ("show position")
* **Safety Limits:** Failsafe detection, screen boundary checking

### Safety & Reliability
* **Failsafe Detection:** Emergency stop by moving cursor to screen corner (0,0)
* **Movement Limits:** Enforces min/max distance to prevent runaway mouse
* **Error Handling:** Graceful recovery from speech recognition timeouts
* **Platform Support:** Works on Windows, macOS, and Linux

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **GUI** | Tkinter | Window management and UI |
| **Voice Input** | `speech_recognition` | Google Speech Recognition API |
| **Mouse Control** | PyAutoGUI | Cross-platform mouse automation |
| **Keyboard Control** | PyAutoGUI | Cross-platform keyboard automation |
| **Testing** | pytest, pytest-cov | Unit tests and code coverage |
| **Language** | Python 3.11+ | Programming language |

See [**Architecture Guide**](docs/ARCHITECTURE.md) for technical details.

## Testing

The project includes a comprehensive test suite with **95% code coverage** and **67 tests**.

**Run all tests with coverage:**

```bash
xvfb-run -a python -m pytest tests/ --cov=. --cov-report=term
```

**Quick test run (no coverage):**

```bash
xvfb-run -a python -m pytest tests/ -q
```

See [**Testing Guide**](TESTING.md) for:
* Detailed coverage breakdown by module
* How to run specific tests
* Known limitations and blind spots
* CI/CD integration examples

## Project Roadmap

Click-to-Talk is actively developed with a clear vision. See [**Project Roadmap**](docs/ROADMAP.md) for:

* **Completed Phases:** Prototype, browser control, accessibility enhancements
* **Current Work:** Full mouse replacement capability
* **Future Plans:** Offline speech recognition, ML-based intent parsing, plugin system
* **Long-term Vision:** Cross-platform, multi-modal control interface

### Development Phases

| Phase | Status | Focus |
|-------|--------|-------|
| Phase 1: Prototype | Complete | Basic voice control |
| Phase 2: Browser | Complete | Web navigation |
| Phase 3: Accessibility | Complete | Full test suite, comprehensive docs |
| Phase 4: Full Mouse | In Progress | Advanced gestures, drag-and-drop |

See [**Roadmap**](docs/ROADMAP.md) for detailed planning, research areas, and contribution opportunities.

## Team

* **Megan Backman** – Documentation Team Lead
* **Allison Coates** – Documentation Team
* **Scott Faust** – Implementation & Video Team Lead
* **Luke Mabie** – Implementation Team
* **Alexander Jimenez** – Implementation Team Lead
* **Hunter Pope** – Implementation Team

## Contributing

We welcome contributions! See [**Project Roadmap**](docs/ROADMAP.md#contributing-to-the-roadmap) for:
* How to report bugs
* How to request features
* How to contribute code
* Development setup instructions

## License

TBD (to be decided by the team).

## Acknowledgments

This project is inspired by the need for **inclusive, accessible technology** that empowers individuals with motor coordination challenges to navigate computers confidently and independently.

We acknowledge the importance of accessibility in computing and are committed to creating tools that eliminate barriers for all users.

---

**Last Updated:** December 7, 2025  
**Version:** 1.0.0-alpha

For more information, visit the [**documentation hub**](#-documentation-hub) or open an issue on [GitHub](https://github.com/DrFaustest/Click-to-Talk/issues).
