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
import tkinter as tk  # [ADDED]
from tkinter import ttk  # [ADDED]

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
        # NEW: show minimal browser/nav help
        print("Browser & Navigation (NEW):")
        print("  'open gmail'  |  'go to youtube'  |  'open gmail.com'")
        print("  'open browser' (just opens your browser)")
        print("  'type hello world'  |  'press enter'  |  'press ctrl c'")
        print("-" * 60)
        print("Starting speech recognition...")

        self.running = True

        # Start speech recognition in a separate thread
        speech_thread = threading.Thread(target=self.speech_handler.start_listening)
        speech_thread.daemon = True
        speech_thread.start()

        # [ADDED] ---- Minimal always-on-top control panel (non-disruptive to your loop) ----
        root = tk.Tk()  # [ADDED]
        root.title(self.config.gui_title)  # [ADDED]
        root.geometry(f"{self.config.gui_width}x{self.config.gui_height}")  # [ADDED]
        if self.config.gui_topmost:  # [ADDED]
            root.attributes("-topmost", True)  # [ADDED]

        status_var = tk.StringVar(value="Status: stopped")  # [ADDED]
        ttk.Label(root, textvariable=status_var, font=("Segoe UI", 11, "bold")).pack(pady=(10, 6))  # [ADDED]

        btn_row = ttk.Frame(root)  # [ADDED]
        btn_row.pack(pady=6)  # [ADDED]
        def _start_listen():  # [ADDED]
            if not self.speech_handler.listening:  # [ADDED]
                threading.Thread(target=self.speech_handler.start_listening, daemon=True).start()  # [ADDED]
        def _stop_listen():  # [ADDED]
            if self.speech_handler.listening:  # [ADDED]
                self.speech_handler.stop_listening()  # [ADDED]
        ttk.Button(btn_row, text="Start Listening", command=_start_listen).grid(row=0, column=0, padx=6)  # [ADDED]
        ttk.Button(btn_row, text="Stop", command=_stop_listen).grid(row=0, column=1, padx=6)  # [ADDED]

        ttk.Label(root, text="Movement distance (pixels)").pack(pady=(12, 2))  # [ADDED]

        # [ADDED] Create the value var and label FIRST so the callback can safely reference it
        dist_val_var = tk.StringVar(value=f"{self.config.default_move_distance} px")  # [ADDED]
        dist_val_lbl = ttk.Label(root, textvariable=dist_val_var)  # [ADDED]
        dist_val_lbl.pack(pady=(0, 8))  # [ADDED]

        # [ADDED] Callback updates config + StringVar (no direct label reference)
        def _on_scale(val):  # [ADDED]
            self.config.default_move_distance = int(float(val))  # [ADDED]
            dist_val_var.set(f"{self.config.default_move_distance} px")  # [ADDED]

        dist_scale = ttk.Scale(  # [ADDED]
            root,
            from_=10,
            to=self.config.default_move_distance * 5,
            orient="horizontal",
            length=self.config.gui_width - 40,
            command=_on_scale
        )
        dist_scale.set(self.config.default_move_distance)  # [ADDED]
        dist_scale.pack()  # [ADDED]

        quick = ttk.Frame(root)  # [ADDED]
        quick.pack(pady=6)  # [ADDED]
        ttk.Button(quick, text="Show Position", command=self.mouse_controller.show_cursor_position).grid(row=0, column=0, padx=6)  # [ADDED]
        ttk.Button(quick, text="Find (Highlight)", command=self.mouse_controller.highlight_cursor).grid(row=0, column=1, padx=6)  # [ADDED]

        def _on_close():  # [ADDED]
            try:  # [ADDED]
                self.speech_handler.stop_listening()  # [ADDED]
            except Exception:  # [ADDED]
                pass  # [ADDED]
            self.stop()  # [ADDED]
            root.destroy()  # [ADDED]
        root.protocol("WM_DELETE_WINDOW", _on_close)  # [ADDED]
        # [ADDED] ---------------------------------------------------------------------------

        try:
            while self.running:
                root.update_idletasks()  # [ADDED]
                root.update()            # [ADDED]
                status = "listening" if self.speech_handler.listening else "stopped"  # [ADDED]
                status_var.set(f"Status: {status}")  # [ADDED]
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
