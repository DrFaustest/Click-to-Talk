# Click-to-Talk: Voice Controlled Mouse Navigation

## Overview

**Click-to-Talk** is a Python desktop application that enables voice-controlled mouse navigation for computer use.
This adaptive technology is designed to support individuals with fine-motor and dexterity challenges—such as those affected by Parkinson's disease or declining motor coordination—who struggle with traditional mouse or trackpad use.

By translating voice input into precise mouse movements and clicks, the application reduces both the **gulf of execution** and the **gulf of evaluation**, enabling users to navigate any application or website more effectively and independently.

## Installation

### Prerequisites

* Python 3.12 or lower
* Microphone (built-in or external)
* Windows, macOS, or Linux

### Installing Python

For Windows

* Download the Windows installer:

[https://www.python.org/downloads/release/python-3117/](https://www.python.org/downloads/release/python-3117/)

* Right-click → Run as administrator.

* In the first screen:

  * Check “Add Python to PATH”
  * Click Customize installation
  * Keep defaults → Next.

* In Advanced Options:

  * Add Python to environment variables
  * Install for all users (recommended)
  * Create shortcuts for installed applications
  * (Optional) Associate files with Python

* Click Install (or Repair if already installed).

For Mac/Linux

* macOS: use the official installer or

```bash
brew install python@3.11
```

* Ubuntu/Debian (example):

```bash
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-venv python3.11-distutils
```

### Install from Source

```bash
git clone <repository-url>
cd click-to-talk

# Initialize virtual environment
py -3.11 -m venv venv
venv\Scripts\activate
# source venv/bin/activate if Mac/Linux

python --version   # should be 3.11.x
pip install -r requirements.txt
```

### Run the Application

```bash
python main.py
```

## Usage

### Voice Commands

* **Movement**:
  "move up", "move down", "move left", "move right" *(optional distance)*

* **Clicks**:
  "click", "left click", "right click", "double click"

* **Scroll**:
  "scroll up", "scroll down"

* **Info**:
  "show position"

* **Find Cursor**:
  "find mouse", "find my mouse",
  "find cursor", "find my cursor"

* **Browser / Navigation**:
  "open gmail", "go to youtube",
  "open gmail.com", "open browser"

* **Typing / Shortcuts**:
  "type hello world",
  "press enter", "press ctrl c", "press ctrl v",
  "new tab", "close tab", "next tab", "previous tab",
  "address bar", "refresh"

* **GUI Controls (NEW)**:

  * *Minimize the panel*:
    "minimize panel", "minimize gui", "hide panel", "hide controls"
  * *Show / maximize the panel*:
    "maximize panel", "maximize gui", "show panel", "show controls"

* **Stop**:
  "stop", "quit", "exit"

### Examples

* "move up 100" – Move cursor up by 100 pixels
* "click" – Perform left-click
* "scroll down" – Scroll downward
* "show position" – Display current cursor coordinates

### Safety Features

* Failsafe corner detection
* Movement distance limits
* Graceful speech recognition error handling
* Emergency quit commands

## Sliding Dock GUI Panel (NEW)

A redesigned accessibility panel improves usability while keeping the screen unobstructed.

### Features

* Slide-out / slide-in docking panel
* Dockable to left or right screen edge
* Smooth sliding animation
* Auto-hide after 30 seconds
* Always-on-top
* Pull-tab (≡) always remains visible when minimized
* Contains:

  * Start / Stop Listening buttons (stacked for narrow layout)
  * Movement distance slider
  * Commands Reference dropdown (informational only)

### Removed GUI Buttons (now voice-only)

* “Show Position”
* “Find Cursor”

### Behavior

* Panel starts fully visible on launch
* Automatically hides after inactivity
* Voice commands can minimize or restore the panel

## Technology

* **Microphone Input:** Built-in or external
* **Voice Recognition:** Google Speech Recognition (via `speech_recognition`)
* **Mouse Control:** PyAutoGUI
* **GUI Framework:** Tkinter
* **Platform:** Python 3.8+ (recommended Python 3.11.x)

## Team Organization

* **Megan Backman** – Documentation Team Lead
* **Allison Coates** – Documentation Team
* **Scott Faust** – Implementation & Video Team Lead
* **Luke Mabie** – Implementation Team
* **Alexander Jimenez** – Implementation Team Lead
* **Hunter Pope** – Implementation Team

---

## Roadmap

1. **Phase 1 – Prototype**

   * Basic movement + clicks
   * Chrome integration

2. **Phase 2 – Browser Control**

   * Navigation commands
   * Address bar control

3. **Phase 3 – Enhanced Accessibility**

   * Cursor highlighting (“find”)
   * Expanded natural language

4. **Phase 4 – Full Mouse Replacement**

   * Voice-driven complete interface
   * Possible integration with OS accessibility APIs

---

## License

TBD (to be decided by the team).

---

## Acknowledgments

This project is inspired by the need for **inclusive, accessible technology** that empowers individuals with motor coordination challenges to navigate computers confidently and independently.

---