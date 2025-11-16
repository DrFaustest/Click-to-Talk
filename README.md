# Click-to-Talk: Voice Controlled Mouse Navigation

## Overview
**Click-to-Talk** is a Python desktop application that enables voice-controlled mouse navigation for computer use.
This adaptive technology is designed to support individuals with fine-motor and dexterity challenges—such as those affected by Parkinson's disease or declining motor coordination—who struggle with traditional mouse or trackpad use.

By translating voice input into precise mouse movements and clicks, the application reduces both the **gulf of execution** and the **gulf of evaluation**, enabling users to navigate any application or website more effectively and independently.

## Installation

### Prerequisites
- Python 3.10 - 3.14
- Microphone (built-in or external)
- Windows, macOS, or Linux

### Installing Python 
For Windows
- Download the latest **Python 3.14.x** installer from the [official downloads page](https://www.python.org/downloads/).
- Right-click → Run as administrator.

- In the first screen:

  - Check “Add Python to PATH”

  - Click Customize installation

  - Keep defaults → Next.

  - In Advanced Options:

    - Add Python to environment variables

    - Install for all users (recommended)

    - Create shortcuts for installed applications

    - (Optional) Associate files with Python

- Click Install (or Repair if already installed).

For Mac/Linux
- macOS: use the universal installer from python.org or 
```bash
brew install python@3.14
```
- Ubuntu/Debian (example using the `deadsnakes` PPA if 3.14 is not yet available in the default repositories):
```bash
sudo apt-get update
sudo apt-get install -y python3.14 python3.14-venv python3.14-distutils
```

### Install from Source
```bash
git clone <repository-url>
cd click-to-talk
#Run these commands in terminal once inside directory to initialize environment
py -3.14 -m venv venv
venv\Scripts\activate
# On macOS/Linux use: python3.14 -m venv venv && source venv/bin/activate
python --version   # should be 3.14.x
pip install -r requirements.txt
```

> The dependency pins now use minimum versions so that pip can resolve builds compatible with Python 3.14 automatically.
> **Note**: This application uses `sounddevice` for microphone input, which is a modern, actively maintained alternative to the deprecated PyAudio library.

### Run the Application
```bash
python main.py
```

## Usage

### Voice Commands
- **Movement**: "move up", "move down", "move left", "move right" [optional distance in pixels]
- **Clicks**: "click", "left click", "right click", "double click"
- **Scroll**: "scroll up", "scroll down"
- **Info**: "show position"
- **Find Cursor**: "find mouse", "find my mouse", "find cursor", "find my cursor"
- **Browser / Navigation**: "open gmail", "go to youtube", "open gmail.com", "open browser"
- **Typing / Shortcuts**: "type hello world", "press enter", "press ctrl c", "press ctrl v", "new tab", "close tab", "next tab", "previous tab", "address bar", "refresh"
- **Stop**: "stop", "quit", "exit" (shuts down the application)

### Examples
- "move up 100" - Move cursor up by 100 pixels
- "click" - Perform left mouse click
- "scroll down" - Scroll down
- "show position" - Display current cursor location

### Safety Features
- Failsafe: Move mouse to screen corner to stop
- Distance limits: Maximum movement distance capped
- Error handling: Graceful handling of recognition failures
- Emergency stop: Voice commands to quit immediately

### Browser Preferences
- Voice navigation commands (e.g., "open gmail", "go to youtube", "open browser") now launch URLs with the **machine's default browser/application**, so your existing OS-level preference is respected automatically.
- To force a specific browser, set `preferred_browser` inside `config.py`.  
  - macOS: use the application name you would pass to `open -a`, e.g., `"Brave Browser"`.  
  - Windows/Linux: provide the executable name or full path (quotes are fine), e.g., `"C:\\Program Files\\Mozilla Firefox\\firefox.exe"` or `"firefox"`.
- `browser_open_target` controls what URL is used when a command just asks to "open browser" (defaults to `about:blank`).

## Technology
The implementation relies on widely available hardware and software:

- **Input Device:** Computer's built-in microphone
- **Voice Recognition:** Google Speech Recognition API via Python speech_recognition library
- **Mouse Control:** PyAutoGUI for cross-platform mouse simulation
- **Platform:** Python 3.10 - 3.14 with cross-platform compatibility

## Team Organization

- **Megan Backman** – Documentation Team Lead  
  *Project management, creativity, and documentation leadership.*  

- **Allison Coates** – Documentation Team  
  *Problem-solving, organization, detail-oriented, Python experience.*  

- **Scott Faust** – Implementation & Video Team Lead  
  *Software engineering, problem solving, technical writing, and communication of complex concepts.*  

- **Luke Mabie** – Implementation Team  
  *End-to-end software development, collaboration, and customer-focused coding.*  

- **Alexander Jimenez** – Implementation Team Lead  
  *Programming, design innovation, and team coordination.*  

- **Hunter Pope** – Implementation Team  
  *Back-end programming and graphic design expertise.*  

---

## Roadmap
1. **Phase 1 – Prototype**  
   - Voice-to-text mapping for simple directional and click commands.  
   - Basic integration with Chrome for mouse control.  

2. **Phase 2 – Browser Control**  
   - Navigation commands (back, reload, forward).  
   - Address bar activation.  

3. **Phase 3 – Enhanced Accessibility**  
   - Highlight/circle cursor with `"find"` command.  
   - Expanded natural language interaction.  

4. **Phase 4 – Full Mouse Replacement**  
   - Comprehensive voice-controlled functionality.  
   - Potential integration with accessibility APIs and third-party tools.  

---

## License
TBD (to be decided by the team).  

---

## Acknowledgments
This project is inspired by the need for **inclusive, accessible technology** that empowers individuals with motor coordination challenges to navigate the web confidently and independently.
