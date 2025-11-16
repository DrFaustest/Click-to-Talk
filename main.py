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


class GUIController:
    """Manages GUI visibility (minimize/restore) safely across threads"""
    def __init__(self, root, config):
        self.root = root
        self.config = config
        import queue as _q
        self._queue = _q.Queue()

    def show_gui(self):
        """Restore/deiconify the window (safe across threads)."""
        def _do():
            try:
                self.root.deiconify()
                self.root.lift()
            except Exception:
                pass
        self._queue.put(_do)

    def hide_gui(self):
        """Minimize/iconify the window (safe across threads)."""
        def _do():
            try:
                self.root.iconify()
            except Exception:
                pass
        self._queue.put(_do)

    def process_queue(self):
        """Run any pending UI actions posted from other threads."""
        try:
            while True:
                fn = self._queue.get_nowait()
                try:
                    fn()
                except Exception:
                    pass
        except Exception:
            # empty queue or other benign conditions
            pass


class ClickToTalkApp:
    def __init__(self):
        self.config = Config()
        self.mouse_controller = MouseController(self.config)
        self.command_parser = CommandParser(self.config)
        self.command_parser.set_mouse_controller(self.mouse_controller)
        self.gui_controller = None  # Will be set after GUI creation

        # NEW: create browser-first WindowManager using Config aliases
        self.window_manager = WindowManager(
            site_aliases=getattr(self.config, "site_aliases", {}),
            preferred_browser=getattr(self.config, "preferred_browser", None),
            browser_open_target=getattr(self.config, "browser_open_target", "about:blank"),
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

        # Increase default pause to reduce premature cutoff (runtime only)
        try:
            self.config.pause_threshold = 1.5
            setp = getattr(self.speech_handler, "set_recognition_params", None)
            if callable(setp):
                setp(pause_threshold=1.5)
        except Exception:
            pass

        # Start speech recognition in a separate thread
        speech_thread = threading.Thread(target=self.speech_handler.start_listening)
        speech_thread.daemon = True
        speech_thread.start()

        # ---- Minimal always-on-top control panel (non-disruptive to your loop) ----
        root = tk.Tk()  
        root.title(self.config.gui_title)  
        
        # Set initial geometry - always open full size
        root.geometry(f"{self.config.gui_width}x{self.config.gui_height}+0+0")
        root.resizable(False, False)
        
        if self.config.gui_topmost:  
            root.attributes("-topmost", True)  
        
        # Initialize GUI controller
        self.gui_controller = GUIController(root, self.config)
        self.command_parser.set_gui_controller(self.gui_controller)
        
        # Main container frame (full width content)
        main_frame = ttk.Frame(root)
        main_frame.pack(fill="both", expand=True)

        # Content panel
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True)

        status_var = tk.StringVar(value="Status: stopped")  
        ttk.Label(content_frame, textvariable=status_var, font=("Segoe UI", 11, "bold")).pack(pady=(10, 6))  

        btn_col = ttk.Frame(content_frame)
        btn_col.pack(pady=6, fill="x")

        def _start_listen():
            if not self.speech_handler.listening:
                threading.Thread(target=self.speech_handler.start_listening, daemon=True).start()

        def _stop_listen():
            if self.speech_handler.listening:
                self.speech_handler.stop_listening()

        ttk.Button(btn_col, text="Start Listening", command=_start_listen).pack(fill="x", padx=10)
        ttk.Button(btn_col, text="Stop", command=_stop_listen).pack(fill="x", padx=10, pady=(6, 0))

        # Input device selector
        ttk.Label(content_frame, text="Input device").pack(pady=(12, 2))

        device_frame = ttk.Frame(content_frame)
        device_frame.pack(fill="x", padx=10)

        device_var = tk.StringVar(value="")
        devices_map = {}  # display -> index

        def _refresh_devices():
            nonlocal devices_map
            devices_map = {}
            try:
                list_func = getattr(self.speech_handler, "list_input_devices", None)
                devices = list_func() if callable(list_func) else []
            except Exception:
                devices = []
            display_list = []
            for d in devices:
                disp = f"[{d['index']}] {d['name']} (ch: {d['max_input_channels']})"
                devices_map[disp] = d['index']
                display_list.append(disp)
            combo.configure(values=display_list)
            # Select current
            cur_idx, cur_name = (None, None)
            try:
                get_func = getattr(self.speech_handler, "get_current_device", None)
                if callable(get_func):
                    res = get_func()
                    if isinstance(res, (list, tuple)) and len(res) >= 2:
                        cur_idx, cur_name = res[0], res[1]
            except Exception:
                pass
            if cur_idx is not None:
                # Find matching display
                for disp, idx in devices_map.items():
                    if idx == cur_idx:
                        device_var.set(disp)
                        break
            current_label_var.set(f"Current input: {cur_name or 'Default Input'}")

        combo = ttk.Combobox(device_frame, textvariable=device_var, state="readonly", width=45)
        combo.pack(side="left", fill="x", expand=True)

        ttk.Button(device_frame, text="Refresh", command=_refresh_devices).pack(side="left", padx=(6, 0))

        def _apply_device():
            disp = device_var.get()
            if not disp or disp not in devices_map:
                return
            idx = devices_map[disp]
            # Update config for persistence and switch mic live
            self.config.mic_device = idx
            try:
                switch_func = getattr(self.speech_handler, "switch_microphone", None)
                if callable(switch_func):
                    switch_func(idx, restart_if_listening=True)
            except Exception:
                pass
            # Update label
            cur_name = None
            try:
                get_func = getattr(self.speech_handler, "get_current_device", None)
                if callable(get_func):
                    res = get_func()
                    if isinstance(res, (list, tuple)) and len(res) >= 2:
                        cur_name = res[1]
            except Exception:
                pass
            current_label_var.set(f"Current input: {cur_name or 'Default Input'}")

        ttk.Button(device_frame, text="Apply", command=_apply_device).pack(side="left", padx=(6, 0))

        current_label_var = tk.StringVar(value="Current input: …")
        ttk.Label(content_frame, textvariable=current_label_var).pack(pady=(4, 0), padx=10, anchor="w")

        # Populate initial device list
        _refresh_devices()

        # Recognition settings
        ttk.Label(content_frame, text="Recognition settings").pack(pady=(16, 4))

        recog_frame = ttk.Frame(content_frame)
        recog_frame.pack(fill="x", padx=10)

        # Language selector
        ttk.Label(recog_frame, text="Language:").grid(row=0, column=0, sticky="w")
        lang_var = tk.StringVar(value=getattr(self.config, "recognition_language", "en-US"))
        lang_combo = ttk.Combobox(recog_frame, textvariable=lang_var, state="readonly", width=10,
                                  values=["en-US", "en-GB", "es-ES", "fr-FR", "de-DE", "it-IT"]) 
        lang_combo.grid(row=0, column=1, padx=(6, 16), sticky="w")

        # Dynamic energy toggle
        dyn_var = tk.BooleanVar(value=getattr(self.config, "dynamic_energy_threshold", True))
        dyn_chk = ttk.Checkbutton(recog_frame, text="Auto sensitivity", variable=dyn_var)
        dyn_chk.grid(row=0, column=2, sticky="w")

        # Energy threshold entry
        ttk.Label(recog_frame, text="Energy:").grid(row=1, column=0, sticky="w", pady=(8,0))
        energy_var = tk.StringVar(value=str(getattr(self.config, "energy_threshold", 300)))
        energy_entry = ttk.Entry(recog_frame, textvariable=energy_var, width=8)
        energy_entry.grid(row=1, column=1, sticky="w", padx=(6,16), pady=(8,0))

        # Pause threshold
        ttk.Label(recog_frame, text="Pause(s):").grid(row=1, column=2, sticky="w", pady=(8,0))
        pause_var = tk.StringVar(value=str(getattr(self.config, "pause_threshold", 0.8)))
        pause_entry = ttk.Entry(recog_frame, textvariable=pause_var, width=6)
        pause_entry.grid(row=1, column=3, sticky="w", padx=(6,0), pady=(8,0))

        # Non-speaking duration
        ttk.Label(recog_frame, text="Gap(s):").grid(row=1, column=4, sticky="w", pady=(8,0))
        gap_var = tk.StringVar(value=str(getattr(self.config, "non_speaking_duration", 0.3)))
        gap_entry = ttk.Entry(recog_frame, textvariable=gap_var, width=6)
        gap_entry.grid(row=1, column=5, sticky="w", padx=(6,0), pady=(8,0))

        # Calibrate + Apply buttons
        def _apply_recog():
            try:
                setp = getattr(self.speech_handler, "set_recognition_params", None)
                if callable(setp):
                    setp(
                        energy_threshold=float(energy_var.get()),
                        dynamic_energy_threshold=bool(dyn_var.get()),
                        pause_threshold=float(pause_var.get()),
                        non_speaking_duration=float(gap_var.get()),
                        language=str(lang_var.get()),
                    )
            except Exception:
                pass

        def _calibrate():
            try:
                recali = getattr(self.speech_handler, "recalibrate", None)
                if callable(recali):
                    recali(None)
            except Exception:
                pass

        btns = ttk.Frame(content_frame)
        btns.pack(fill="x", padx=10, pady=(8, 0))
        ttk.Button(btns, text="Apply Recognition", command=_apply_recog).pack(side="left")
        ttk.Button(btns, text="Calibrate", command=_calibrate).pack(side="left", padx=(6,0))


        ttk.Label(content_frame, text="Movement distance (pixels)").pack(pady=(12, 2))  

        # Create the value var and label FIRST so the callback can safely reference it
        dist_val_var = tk.StringVar(value=f"{self.config.default_move_distance} px")  
        dist_val_lbl = ttk.Label(content_frame, textvariable=dist_val_var)  
        dist_val_lbl.pack(pady=(0, 8))  

        # Callback updates config + StringVar (no direct label reference)
        def _on_scale(val):  
            self.config.default_move_distance = int(float(val))  
            dist_val_var.set(f"{self.config.default_move_distance} px")  

        dist_scale = ttk.Scale(  
            content_frame,
            from_=10,
            to=self.config.default_move_distance * 5,
            orient="horizontal",
            length=self.config.gui_width - 80,
            command=_on_scale
        )
        dist_scale.set(self.config.default_move_distance)  
        dist_scale.pack()  

        # Commands reference dropdown (non-interactive)
        ttk.Label(content_frame, text="Commands (reference)").pack(pady=(12, 4))

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
            content_frame,
            textvariable=cmd_var,
            values=commands_reference,
            state="readonly",
            width=35,
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
                # Process any pending cross-thread UI actions
                if self.gui_controller:
                    self.gui_controller.process_queue()
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
