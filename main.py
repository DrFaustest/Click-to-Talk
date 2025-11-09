#!/usr/bin/env python3
"""
Click-to-Talk: Voice Controlled Mouse Navigation
Main application entry point
"""

import sys
import time
import threading
from speech_handler import SpeechHandler
from mouse_controller import MouseController
from command_parser import CommandParser
from config import Config
import tkinter as tk  
from tkinter import ttk  

# NEW: bring in browser + keyboard controllers
from window_manager import WindowManager  # NEW: browser/site navigation
from keyboard_controller import KeyboardController  # NEW: typing and shortcuts


class ClickToTalkApp:
    def __init__(self):
        self.config = Config()
        self.mouse_controller = MouseController(self.config)
        self.command_parser = CommandParser(self.config)
        self.command_parser.set_mouse_controller(self.mouse_controller)

        # NEW: create browser-first WindowManager using Config aliases
        self.window_manager = WindowManager(
            site_aliases=getattr(self.config, "site_aliases", {}),
            preferred_browser=getattr(self.config, "preferred_browser", None)
        )
        self.command_parser.set_window_manager(self.window_manager)  # NEW

        # NEW: keyboard controller for typing + key combos
        self.keyboard_controller = KeyboardController(
            pause=getattr(self.config, "keyboard_pause", 0.05)
        )
        self.command_parser.set_keyboard_controller(self.keyboard_controller)  # NEW

        self.speech_handler = SpeechHandler(self.config, self.command_parser, self.mouse_controller)
        self.speech_handler.set_stop_callback(self.stop)
        self.running = False

    # Start the application
    def start(self):
        """Start the voice control application"""
        print("=" * 60)
        print("Click-to-Talk: Voice Controlled Mouse Navigation")
        print("=" * 60)
        print("Commands:")
        print("  Movement: 'move up', 'move down', 'move left', 'move right' [distance]")
        print("  Clicks: 'click', 'right click', 'double click'")
        print("  Scroll: 'scroll up', 'scroll down'")
        print("  Info: 'show position'")
        print("  Stop: 'stop' or 'quit'")
        print("-" * 60)
        print("Find Cursor:")
        print("  'find mouse'  |  'find my mouse'  |  'find cursor'  |  'find my cursor'")
        print("-" * 60)
        print("Browser & Navigation:")
        print("  'open gmail'  |  'go to youtube'  |  'open gmail.com'")
        print("  'open browser' (just opens your browser)")
        print("-" * 60)
        print("Typing & Shortcuts:")
        print("  'type hello world'")
        print("  'press enter'  |  'press ctrl c'  |  'press ctrl v'")
        print("  'new tab'  |  'close tab'  |  'next tab'  |  'previous tab'")
        print("  'address bar'  |  'refresh'")
        print("-" * 60)
        print("Starting speech recognition...")

        self.running = True

        # Start speech recognition in a separate thread
        speech_thread = threading.Thread(target=self.speech_handler.start_listening)
        speech_thread.daemon = True
        speech_thread.start()

        # ---- Minimal always-on-top control panel (non-disruptive to your loop) ----
        root = tk.Tk()  
        root.title(self.config.gui_title)  
        root.geometry(f"{self.config.gui_width}x{self.config.gui_height}")  
        if self.config.gui_topmost:  
            root.attributes("-topmost", True)  

        status_var = tk.StringVar(value="Status: stopped")  
        ttk.Label(root, textvariable=status_var, font=("Segoe UI", 11, "bold")).pack(pady=(10, 6))  

        btn_col = ttk.Frame(root)
        btn_col.pack(pady=6, fill="x")

        def _start_listen():
            if not self.speech_handler.listening:
                threading.Thread(target=self.speech_handler.start_listening, daemon=True).start()

        def _stop_listen():
            if self.speech_handler.listening:
                self.speech_handler.stop_listening()

        ttk.Button(btn_col, text="Start Listening", command=_start_listen).pack(fill="x", padx=10)
        ttk.Button(btn_col, text="Stop", command=_stop_listen).pack(fill="x", padx=10, pady=(6, 0))


        ttk.Label(root, text="Movement distance (pixels)").pack(pady=(12, 2))  

        # Create the value var and label FIRST so the callback can safely reference it
        dist_val_var = tk.StringVar(value=f"{self.config.default_move_distance} px")  
        dist_val_lbl = ttk.Label(root, textvariable=dist_val_var)  
        dist_val_lbl.pack(pady=(0, 8))  

        # Callback updates config + StringVar (no direct label reference)
        def _on_scale(val):  
            self.config.default_move_distance = int(float(val))  
            dist_val_var.set(f"{self.config.default_move_distance} px")  

        dist_scale = ttk.Scale(  
            root,
            from_=10,
            to=self.config.default_move_distance * 5,
            orient="horizontal",
            length=self.config.gui_width - 40,
            command=_on_scale
        )
        dist_scale.set(self.config.default_move_distance)  
        dist_scale.pack()  

        # Commands reference dropdown (non-interactive)
        ttk.Label(root, text="Commands (reference)").pack(pady=(12, 4))

        commands_reference = [
            "— Select a command —",
            # Movement
            "move up [distance]",
            "move down [distance]",
            "move left [distance]",
            "move right [distance]",
            # Clicks
            "click",
            "right click",
            "double click",
            # Scroll
            "scroll up",
            "scroll down",
            # Info
            "show position",
            # Stop
            "stop",
            "quit",
            # Find Cursor
            "find mouse",
            "find my mouse",
            "find cursor",
            "find my cursor",
            # Browser & Navigation
            "open gmail",
            "go to youtube",
            "open gmail.com",
            "open browser",
            # Typing & Shortcuts
            "press enter",
            "press ctrl c",
            "press ctrl v",
            "new tab",
            "close tab",
            "next tab",
            "previous tab",
            "address bar",
            "refresh",
        ]

        cmd_var = tk.StringVar(value=commands_reference[0])
        cmd_combo = ttk.Combobox(
            root,
            textvariable=cmd_var,
            values=commands_reference,
            state="readonly",
            width=38,   # tweak if you narrow the window further
        )
        cmd_combo.pack(padx=10, pady=(0, 8))


        def _on_close():  
            try:  
                self.speech_handler.stop_listening()  
            except Exception:  
                pass  
            self.stop()  
            root.destroy()  
        root.protocol("WM_DELETE_WINDOW", _on_close)  
        # ---------------------------------------------------------------------------

        try:
            while self.running:
                root.update_idletasks()  
                root.update()            
                status = "listening" if self.speech_handler.listening else "stopped"  
                status_var.set(f"Status: {status}")  
                time.sleep(0.1)  # Keep main thread alive
        except KeyboardInterrupt:
            print("\nInterrupted by user...")
        finally:
            self.stop()

    def stop(self):
        """Stop the application"""
        self.running = False
        self.speech_handler.stop_listening()
        print("Application stopped.")

def main():
    """Main entry point"""
    try:
        app = ClickToTalkApp()
        app.start()
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
