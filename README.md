# Click-to-Talk: Voice Controlled Mouse Navigation

## Overview
**Click-to-Talk** is a Python desktop application that enables voice-controlled mouse navigation for computer use.
This adaptive technology is designed to support individuals with fine-motor and dexterity challenges—such as those affected by Parkinson's disease or declining motor coordination—who struggle with traditional mouse or trackpad use.

By translating voice input into precise mouse movements and clicks, the application reduces both the **gulf of execution** and the **gulf of evaluation**, enabling users to navigate any application or website more effectively and independently.

## Installation

### Prerequisites
- Python 3.8 or higher
- Microphone (built-in or external)
- Windows, macOS, or Linux

### Install from Source
```bash
git clone <repository-url>
cd click-to-talk
pip install -r requirements.txt
```

### Run the Application
```bash
python main.py
```

## Usage

### Voice Commands
- **Movement**: "move up", "move down", "move left", "move right" [optional distance in pixels]
- **Clicks**: "click", "left click", "right click", "double click"
- **Scroll**: "scroll up", "scroll down"
- **Info**: "show position" (displays current cursor coordinates)
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

## Technology
The implementation relies on widely available hardware and software:

- **Input Device:** Computer's built-in microphone
- **Voice Recognition:** Google Speech Recognition API via Python speech_recognition library
- **Mouse Control:** PyAutoGUI for cross-platform mouse simulation
- **Platform:** Python 3.8+ with cross-platform compatibility

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
