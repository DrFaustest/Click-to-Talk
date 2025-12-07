# Installation Guide

Click-to-Talk is a Python desktop application that enables voice-controlled mouse navigation for computer use.

## Prerequisites

* Python 3.12 or lower
* Microphone (built-in or external)
* Windows, macOS, or Linux
* Git (for cloning the repository)

## System Requirements

### Windows

* Windows 10 or later
* Administrator access (recommended for installation)
* Audio input device (microphone)

### macOS

* macOS 10.13 or later
* Intel or Apple Silicon processor
* Audio input device (microphone)

### Linux

* Ubuntu 18.04 or later (or compatible distribution)
* Audio input device (microphone)
* X11 display server (for GUI)

## Installing Python

### Windows

1. Download the Windows installer from:
   [https://www.python.org/downloads/release/python-3117/](https://www.python.org/downloads/release/python-3117/)

2. Right-click the installer → **Run as administrator**

3. **First screen:**
   * Check "Add Python to PATH"
   * Click "Customize installation"
   * Keep defaults → Click "Next"

4. **Advanced Options:**
   * Add Python to environment variables
   * Install for all users (recommended)
   * Create shortcuts for installed applications
   * (Optional) Associate files with Python

5. Click **Install** (or **Repair** if already installed)

6. Verify installation:
   ```bash
   python --version
   ```

### macOS

**Using Homebrew (Recommended):**

```bash
brew install python@3.11
```

**Using Official Installer:**

1. Download from [python.org](https://www.python.org/downloads/)
2. Run the `.pkg` installer
3. Follow the on-screen prompts

**Verify installation:**

```bash
python3 --version
```

### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-venv python3.11-distutils
```

**Verify installation:**

```bash
python3.11 --version
```

## Install from Source

### 1. Clone the Repository

```bash
git clone https://github.com/DrFaustest/Click-to-Talk.git
cd Click-to-Talk
```

### 2. Create a Virtual Environment

**Windows:**

```bash
py -3.11 -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### 3. Verify Python Version

```bash
python --version
# Should output: Python 3.11.x
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

**What gets installed:**
* `pyautogui` – Mouse and keyboard control
* `speech_recognition` – Voice input processing
* `pyttsx3` – Text-to-speech feedback
* `pytest` – Testing framework
* `pytest-cov` – Code coverage reporting

### 5. Run the Application

```bash
python main.py
```

The application window should appear with the sliding dock panel.

## Troubleshooting

### "Python is not recognized"

**Windows:** Make sure "Add Python to PATH" was checked during installation. Restart your terminal after installation.

**macOS/Linux:** Use `python3` instead of `python`, or create an alias:

```bash
alias python=python3.11
```

### Microphone Not Found

* Check System Settings → Sound → Input device is selected
* Try adjusting the input volume
* Restart the application

### "Module not found" errors

Ensure your virtual environment is activated:

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

Then reinstall dependencies:

```bash
pip install -r requirements.txt
```

### GUI Panel Not Appearing (macOS/Linux)

Some window managers don't support "always-on-top" windows. Try:

1. Update your window manager
2. Check if other always-on-top applications work
3. Report the issue with your window manager info

## Next Steps

* See [**USAGE.md**](USAGE.md) for voice commands and examples
* See [**TESTING.md**](../TESTING.md) to run the test suite
* See [**ARCHITECTURE.md**](ARCHITECTURE.md) for technical details

## Getting Help

If you encounter issues:

1. Check this installation guide first
2. Review [Troubleshooting](#troubleshooting) section
3. Open an issue on [GitHub](https://github.com/DrFaustest/Click-to-Talk/issues)

---

**Last Updated:** December 7, 2025
