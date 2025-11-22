
"""
Click-to-Talk: Voice Controlled Mouse Navigation
Main application entry point
"""

import sys
import time
import threading
import tkinter as tk
from tkinter import ttk

from speech_handler import SpeechHandler
from mouse_controller import MouseController
from command_parser import CommandParser
from config import Config
from keyboard_controller import KeyboardController
from window_manager import WindowManager


class ClickToTalkApp:
    def __init__(self):
        self.config = Config()
        self.mouse_controller = MouseController(self.config)
        self.command_parser = CommandParser(self.config)
        self.keyboard_controller = KeyboardController(self.config)
        self.window_manager = WindowManager(self.config)

        # Wire controllers into parser
        self.command_parser.set_mouse_controller(self.mouse_controller)
        if hasattr(self.command_parser, "set_keyboard_controller"):
            self.command_parser.set_keyboard_controller(self.keyboard_controller)
        if hasattr(self.command_parser, "set_window_manager"):
            self.command_parser.set_window_manager(self.window_manager)

        self.speech_handler = SpeechHandler(
            self.config, self.command_parser, self.mouse_controller
        )
        self.speech_handler.set_stop_callback(self.stop)

        self.running = False
        self.root = None

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
        print("Find Cursor (NEW):")
        print("  'find mouse'  |  'find my mouse'  |  'find cursor'  |  'find my cursor'")
        print("-" * 60)
        print("Browser & Navigation (NEW):")
        print("  'open gmail'  |  'go to youtube'  |  'open gmail.com'")
        print("  'open browser' (just opens your browser)")
        print("-" * 60)
        print("Typing & Shortcuts (NEW):")
        print("  'type hello world'")
        print("  'press enter'  |  'press ctrl c'  |  'press ctrl v'")
        print("  'new tab'  |  'close tab'  |  'next tab'  |  'previous tab'")
        print("  'address bar'  |  'refresh'")
        print("-" * 60)
        print("Panel Controls (NEW):")
        print("  Minimize: 'minimize panel'  |  'minimize gui'  |  'hide panel'  |  'hide controls'")
        print("  Show   : 'maximize panel'  |  'maximize gui'  |  'show panel'  |  'show controls'")
        print("-" * 60)
        print("Docking:")
        print("  Ctrl+Left  -> dock panel to left edge")
        print("  Ctrl+Right -> dock panel to right edge")
        print("-" * 60)
        print("Starting speech recognition...")


        self.running = True

        # Start speech recognition in a separate thread
        speech_thread = threading.Thread(target=self.speech_handler.start_listening)
        speech_thread.daemon = True
        speech_thread.start()

        # --- Sliding dock panel setup ---
        root = tk.Tk()
        self.root = root
        root.overrideredirect(True)        # frameless window
        root.attributes("-topmost", True)  # keep above normal windows

        W = self.config.gui_width
        H = self.config.gui_height
        TAB = 28                    # visible pull-tab width
        step_px = 20                # slide step per tick
        autohide_seconds = 30       # auto-hide delay

        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        y_default = max(0, (sh - H) // 3)  # vertical position along edge

        dock_side = "right"         # start docked on the right
        shown_x = sw - W            # fully visible position (right)
        hidden_x = sw - TAB         # only leftmost TAB px of window are on-screen
        current_target_x = shown_x  # start fully visible
        last_interaction = time.time()

        # Start fully visible
        root.geometry(f"{W}x{H}+{shown_x}+{y_default}")

        def geom_tuple():
            """Return (x, w, y) from current geometry safely."""
            g = root.geometry()  # e.g. "320x420+1600+200"
            try:
                size, pos = g.split("+", 1)
                w_str, h_str = size.split("x")
                x_str, y_str = pos.split("+")
                w_val = int(w_str)
                x_val = int(x_str)
                y_val = int(y_str)
            except Exception:
                w_val = W
                x_val = shown_x
                y_val = y_default
            return x_val, w_val, y_val

        def pointer_inside():
            """Check if the mouse pointer is inside the panel bounds."""
            px = root.winfo_pointerx()
            py = root.winfo_pointery()
            x_val, _, y_val = geom_tuple()
            return (x_val <= px <= x_val + W) and (y_val <= py <= y_val + H)

        def touch(event=None):
            """Record user interaction (for auto-hide timer)."""
            nonlocal last_interaction
            last_interaction = time.time()

        def set_side(side):
            """Dock panel to left or right edge."""
            nonlocal dock_side, shown_x, hidden_x, current_target_x
            if side == dock_side:
                return
            dock_side = side
            sw_local = root.winfo_screenwidth()
            if dock_side == "right":
                shown_x = sw_local - W
                hidden_x = sw_local - TAB  # only left chunk shown when hidden
            else:
                shown_x = 0
                hidden_x = -(W - TAB)      # only right chunk shown when hidden
            x_val, _, y_val = geom_tuple()
            root.geometry(f"{W}x{H}+{shown_x}+{y_val}")
            current_target_x = shown_x
            touch()
            place_tab()

        def slide_open(event=None):
            """Slide panel fully into view."""
            nonlocal current_target_x
            touch()
            current_target_x = shown_x

        def slide_close(event=None):
            """Slide panel out, leaving only the tab visible."""
            nonlocal current_target_x
            if not pointer_inside():
                current_target_x = hidden_x

        def minimize_panel(event=None):
            """Explicit minimize: hide the panel regardless of pointer location."""
            nonlocal current_target_x
            touch()
            current_target_x = hidden_x

        def maximize_panel(event=None):
            """Explicit maximize: show the panel fully."""
            nonlocal current_target_x
            touch()
            current_target_x = shown_x


        def toggle_panel(event=None):
            """Toggle between open/closed."""
            nonlocal current_target_x
            touch()
            if current_target_x == shown_x:
                slide_close()
            else:
                slide_open()


        # Main content frame (panel interior)
        content = ttk.Frame(root, padding=10)
        content.place(x=0, y=0, width=W, height=H)

        # Status label
        status_var = tk.StringVar(value="Status: stopped")
        ttk.Label(content, textvariable=status_var, font=("Segoe UI", 11, "bold")).pack(pady=(10, 6))

        # Start / Stop buttons (stacked)
        btn_col = ttk.Frame(content)
        btn_col.pack(pady=6, fill="x")

        def _start_listen():
            touch()
            if not self.speech_handler.listening:
                threading.Thread(target=self.speech_handler.start_listening, daemon=True).start()

        def _stop_listen():
            touch()
            if self.speech_handler.listening:
                self.speech_handler.stop_listening()

        ttk.Button(btn_col, text="Start Listening", command=_start_listen).pack(fill="x", padx=10)
        ttk.Button(btn_col, text="Stop", command=_stop_listen).pack(fill="x", padx=10, pady=(6, 0))

        # Movement distance slider
        ttk.Label(content, text="Movement distance (pixels)").pack(pady=(12, 2))

        dist_val_var = tk.StringVar(value=f"{self.config.default_move_distance} px")
        dist_val_lbl = ttk.Label(content, textvariable=dist_val_var)
        dist_val_lbl.pack(pady=(0, 8))

        def _on_scale(val):
            touch()
            self.config.default_move_distance = int(float(val))
            dist_val_var.set(f"{self.config.default_move_distance} px")

        dist_scale = ttk.Scale(
            content,
            from_=10,
            to=self.config.default_move_distance * 5,
            orient="horizontal",
            length=W - 40,
            command=_on_scale,
        )
        dist_scale.set(self.config.default_move_distance)
        dist_scale.pack()

        # Commands reference dropdown (non-interactive)
        ttk.Label(content, text="Commands (reference)").pack(pady=(12, 4))

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
            "type ...",
            "press enter",
            "press ctrl c",
            "press ctrl v",
            "new tab",
            "close tab",
            "next tab",
            "previous tab",
            "address bar",
            "refresh",

            # Panel Controls (NEW)
            "minimize panel",
            "minimize gui",
            "hide panel",
            "hide controls",
            "maximize panel",
            "maximize gui",
            "show panel",
            "show controls",
        ]

        cmd_var = tk.StringVar(value=commands_reference[0])
        cmd_combo = ttk.Combobox(
            content,
            textvariable=cmd_var,
            values=commands_reference,
            state="readonly",
            width=38,
        )
        cmd_combo.pack(padx=10, pady=(0, 8))

        # Pull tab: thin strip that stays visible when hidden
        tab = ttk.Frame(root, relief="ridge")
        tab_width = TAB
        tab_height = 100

        def place_tab():
            """Place the tab so it's always on the visible edge."""
            if dock_side == "right":
                # When hidden to the right, only the LEFT-most TAB px of the window are visible,
                # so put the tab at x=0 (left edge inside the window).
                tab_x = 0
            else:
                # When hidden to the left, only the RIGHT-most TAB px are visible,
                # so put the tab at x=W - TAB.
                tab_x = W - tab_width
            tab.place(x=tab_x, y=(H // 2) - (tab_height // 2), width=tab_width, height=tab_height)

        ttk.Label(tab, text="≡", anchor="center").pack(expand=True, fill="both")

        tab.bind("<Button-1>", toggle_panel)
        tab.bind("<Enter>", slide_open)
        tab.bind("<Motion>", touch)
        content.bind("<Enter>", touch)
        root.bind("<Motion>", touch)

        place_tab()

        # Allow voice commands to control the panel
        self.command_parser.set_ui_callbacks(minimize_panel, maximize_panel)

        # Dock side hotkeys
        root.bind("<Control-Left>", lambda e: set_side("left"))
        root.bind("<Control-Right>", lambda e: set_side("right"))

        # Escape to quit
        root.bind("<Escape>", lambda e: (self.stop(), root.destroy()))

        try:
            while self.running:
                root.update_idletasks()
                root.update()

                # Slide animation towards target x
                x_val, _, y_val = geom_tuple()
                if x_val != current_target_x:
                    if abs(current_target_x - x_val) <= step_px:
                        x_val = current_target_x
                    else:
                        x_val += step_px if current_target_x > x_val else -step_px
                    root.geometry(f"{W}x{H}+{x_val}+{y_val}")
                    place_tab()

                # Auto-hide after inactivity
                if (
                    time.time() - last_interaction > autohide_seconds
                    and current_target_x != hidden_x
                    and not pointer_inside()
                ):
                    current_target_x = hidden_x

                status = "listening" if self.speech_handler.listening else "stopped"
                status_var.set(f"Status: {status}")
                time.sleep(0.05)
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
