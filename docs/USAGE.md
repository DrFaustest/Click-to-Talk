# Usage Guide

Learn how to use Click-to-Talk's voice commands to control your computer.

## Quick Start

1. Launch the application:
   ```bash
   python main.py
   ```

2. Click **Start Listening** or say **"start"** to begin voice control

3. Speak clearly into your microphone

4. Say **"stop"** or **"quit"** to end the session

## Voice Commands Reference

### Movement Commands

Control cursor position with precise or relative movement.

| Command | Effect | Example |
|---------|--------|---------|
| `move up` | Move cursor up (default 50px) | "move up" |
| `move up [distance]` | Move cursor up by N pixels | "move up 100" |
| `move down` | Move cursor down (default 50px) | "move down" |
| `move down [distance]` | Move cursor down by N pixels | "move down 75" |
| `move left` | Move cursor left (default 50px) | "move left" |
| `move left [distance]` | Move cursor left by N pixels | "move left 200" |
| `move right` | Move cursor right (default 50px) | "move right" |
| `move right [distance]` | Move cursor right by N pixels | "move right 150" |

**Default distance:** 50 pixels (adjustable via the GUI slider)

**Distance limits:** 1–500 pixels per command (safety feature)

**Example workflow:**
```
"move up 100"     → cursor moves up 100px
"move right 50"   → cursor moves right 50px
"click"           → left-click at new position
```

### Click Commands

Perform mouse clicks at the current cursor position.

| Command | Effect |
|---------|--------|
| `click` | Left-click |
| `left click` | Left-click (explicit) |
| `right click` | Right-click (context menu) |
| `double click` | Double-click (open files, etc.) |

**Examples:**
```
"click"          → Single left-click
"right click"    → Right-click for context menu
"double click"   → Open file or activate element
```

### Scroll Commands

Scroll content within windows and web pages.

| Command | Effect |
|---------|--------|
| `scroll up` | Scroll up |
| `scroll down` | Scroll down |

**Examples:**
```
"scroll down"   → Scroll downward in active window
"scroll up"     → Scroll upward in active window
```

### Cursor Information

Display or highlight the cursor position.

| Command | Effect |
|---------|--------|
| `show position` | Display current cursor coordinates (X, Y) in terminal |
| `find cursor` | Highlight cursor with a visual indicator |
| `find mouse` | Highlight cursor (alias) |
| `find my cursor` | Highlight cursor (alias) |
| `find my mouse` | Highlight cursor (alias) |

**Examples:**
```
"show position"  → Prints "Cursor at (1234, 567)" to console
"find cursor"    → Highlights cursor on screen with animated ring
```

### Browser & Navigation Commands

Open websites and control browser navigation.

| Command | Effect |
|---------|--------|
| `open [website]` | Open website in default browser |
| `go to [website]` | Navigate to website |
| `open gmail` | Open Gmail |
| `open youtube` | Open YouTube |
| `open gmail.com` | Open Gmail (explicit URL) |
| `open browser` | Open default browser |

**Examples:**
```
"open google.com"       → Opens Google in default browser
"go to wikipedia.org"   → Navigates to Wikipedia
"open gmail"            → Opens Gmail directly
"open browser"          → Opens default browser (no URL)
```

**Supported formats:**
* Domain names: `google.com`, `youtube.com`
* Common names: `gmail`, `youtube`, `wikipedia`
* Full URLs: `https://example.com`

### Keyboard & Typing Commands

Type text and press keyboard shortcuts.

| Command | Effect |
|---------|--------|
| `type [text]` | Type the specified text |
| `press [key]` | Press a single key |
| `press [key] [key]` | Press multiple keys (chord/shortcut) |

**Examples:**
```
"type hello world"        → Types: hello world
"press enter"             → Presses Enter key
"press ctrl c"            → Presses Ctrl+C (copy)
"press ctrl v"            → Presses Ctrl+V (paste)
"press alt tab"           → Presses Alt+Tab (switch app)
"press shift a"           → Presses Shift+A (capital A)
```

**Supported modifiers:**
* `ctrl` / `control`
* `shift`
* `alt`
* `cmd` / `command` (macOS)

**Supported keys:**
* Navigation: `up`, `down`, `left`, `right`, `home`, `end`, `pageup`, `pagedown`
* Editing: `delete`, `backspace`, `tab`
* Functions: `f1`, `f2`, ..., `f12`
* Special: `enter`, `esc`, `space`

### Browser Control Commands

Control browser tabs and navigation while on web pages.

| Command | Effect |
|---------|--------|
| `new tab` | Open a new browser tab |
| `close tab` | Close current tab |
| `next tab` | Switch to next tab |
| `previous tab` | Switch to previous tab |
| `address bar` | Focus the address/location bar |
| `refresh` | Reload current page |

**Examples:**
```
"new tab"         → Opens new tab
"address bar"     → Focuses address bar for URL entry
"refresh"         → Reloads page
"next tab"        → Switches to next tab
"close tab"       → Closes current tab
```

### GUI Control Commands

Manage the visibility of the application panel.

| Command | Effect |
|---------|--------|
| `minimize panel` | Hide the control panel |
| `minimize gui` | Hide the control panel |
| `hide panel` | Hide the control panel |
| `hide controls` | Hide the control panel |
| `maximize panel` | Show the control panel |
| `maximize gui` | Show the control panel |
| `show panel` | Show the control panel |
| `show controls` | Show the control panel |

**Examples:**
```
"minimize panel"    → Hides the dock panel
"show panel"        → Shows the dock panel (resets auto-hide timer)
```

**Note:** The pull-tab (≡) remains visible even when the panel is minimized, so you can always slide it back.

### Control Commands

Start, stop, and quit the application.

| Command | Effect |
|---------|--------|
| `stop` | Stop listening (pause voice input) |
| `quit` | Exit the application |
| `exit` | Exit the application |

**Examples:**
```
"stop"   → Stops listening (app remains open)
"quit"   → Exits the entire application
"exit"   → Exits the entire application
```

## Command Examples

### Example 1: Click a Button

Goal: Click a button in the middle of the screen

```
"move up 100"      → Move cursor up 100 pixels
"click"            → Click at new position
```

### Example 2: Open a Website

Goal: Open Gmail and type an email address

```
"open gmail"                    → Opens Gmail
[wait for page to load]
"type john.doe@example.com"     → Types email address
"press tab"                     → Move to password field
```

### Example 3: Navigate a Document

Goal: Scroll down and click a link

```
"scroll down"      → Scroll down in page
"scroll down"      → Scroll down more
"move right 50"    → Move cursor to a link
"click"            → Click the link
```

### Example 4: Copy & Paste Text

Goal: Copy selected text and paste it elsewhere

```
"press ctrl c"     → Copy selected text
"move left 200"    → Move cursor to destination
"click"            → Click destination field
"press ctrl v"     → Paste the text
```

### Example 5: Tab Navigation

Goal: Open a new tab and search Google

```
"new tab"          → Opens new browser tab
"address bar"      → Focus address bar
"type google.com"  → Type the domain
"press enter"      → Navigate to Google
"type my search"   → Type search query
"press enter"      → Search
```

## Safety Features

Click-to-Talk includes several built-in safety mechanisms:

### Movement Limits

* **Maximum distance:** 500 pixels per command
* **Minimum distance:** 1 pixel
* **Default distance:** 50 pixels
* **Adjustable:** Use the GUI slider to change default distance

### Screen Boundaries

* Cursor cannot move off-screen
* Commands that exceed screen limits are clamped to edge

### Failsafe Detection

* Moving cursor to screen corners (0,0) activates emergency stop
* Quickly move cursor to top-left corner to force-quit

### Error Handling

* Unrecognized commands are ignored (no action taken)
* Timeouts gracefully pause listening
* Microphone errors don't crash the application

## Tips & Tricks

### 1. Speak Clearly

* Pronounce commands slowly and clearly
* Google Speech Recognition works best with standard accents
* Background noise reduces accuracy

### 2. Use the GUI Slider

* Adjust the movement distance slider for different tasks
* Use **50px** for precise work (small elements)
* Use **100px+** for larger movements

### 3. Combine Commands

* Build workflows by chaining commands:
  ```
  "move right 100" → "move down 50" → "click" → "type my text"
  ```

### 4. Use Keyboard Shortcuts

* Browser shortcuts are faster than mouse navigation:
  ```
  "press ctrl l"    → Focus address bar (Chrome/Firefox)
  "address bar"     → Alternative focus address bar command
  ```

### 5. Find & Highlight Cursor

* Use "find cursor" to locate your mouse when you lose track
* Helpful after moving the cursor many times

### 6. Mobile Phone as Microphone

* If your computer's microphone is poor quality, try:
  * External USB microphone
  * Wireless headset microphone

### 7. Pause Between Commands

* If commands aren't recognized, pause ~1 second between them
* This helps speech recognition separate commands

## Troubleshooting

### Commands Not Recognized

1. **Speak more clearly** – Enunciate each word
2. **Reduce background noise** – Use in a quiet environment
3. **Check microphone** – Ensure microphone is selected in System Settings
4. **Adjust microphone input level** – Too quiet = worse recognition

### Cursor Moves Wrong Direction

* Double-check the spoken direction: "up", "down", "left", "right"
* Try "move up 50" instead of just "move up" to verify recognition

### Speech Recognition Timeout

* The app will automatically resume listening after a timeout
* Say "start" to explicitly resume voice input

### GUI Panel Won't Hide/Show

* Click the pull-tab (≡) to manually slide the panel
* Use "maximize panel" or "minimize panel" voice commands

## Advanced Topics

### Custom Commands

See [ARCHITECTURE.md](ARCHITECTURE.md) for adding custom commands.

### Configuration

See `config.py` for advanced settings like:
* Default movement distance
* Microphone sensitivity
* Speech recognition language
* GUI panel size and position

---

**Last Updated:** December 7, 2025
