"""
Configuration Module
Contains configurable settings for the application
"""

class Config:
    def __init__(self):
        # Mouse settings
        self.default_move_distance = 50  # pixels
        self.move_duration = 0.2  # seconds
        self.mouse_pause = 0.1  # seconds between actions

        # Speech recognition settings
        self.energy_threshold = 300          # mic sensitivity baseline for VAD
        self.dynamic_energy_threshold = True # auto-adjust to ambient noise
        self.energy_adjust_duration = 1.5    # seconds to sample background noise
        self.pause_threshold = 0.8           # seconds of silence to end phrase
        self.non_speaking_duration = 0.3     # filter brief inter-word pauses
        self.phrase_time_limit = 5           # max seconds for a phrase (tests expect 5)
        self.mic_device = None               # set to device name substring or index
        self.recognition_language = "en-US"  # BCP-47 code for Google recognizer

        # Application settings
        self.listen_timeout = 5  # seconds to wait for speech (tests expect 5)

        # Command keywords (can be customized)
        self.movement_commands = {
            "up": ["up", "north", "top"],
            "down": ["down", "south", "bottom"],
            "left": ["left", "west"],
            "right": ["right", "east"]
        }

        self.click_commands = {
            "left": ["click", "left click", "press"],
            "right": ["right click"],
            "double": ["double click", "double"]
        }

        self.scroll_commands = {
            "up": ["scroll up", "wheel up"],
            "down": ["scroll down", "wheel down"]
        }

        self.stop_commands = ["stop", "quit", "exit", "end"]

        # GUI
        self.gui_title = "Click-to-Talk"                 # window title
        self.gui_topmost = True                          # keep panel above other windows
        self.gui_width = 500                             # panel width (px)
        self.gui_height = 700                            # panel height (px)
        self.gui_tab_width = 40                          # collapsed tab width (px)
        self.gui_collapsed = True                        # start collapsed

        # Cursor highlight ("find") 
        self.highlight_size = 140                        # highlight diameter (px)
        self.highlight_border = 6                        # ring thickness (px)
        self.highlight_duration_ms = 900                 # display time (ms)
        self.highlight_color = "#00A3FF"               # ring color (high-contrast cyan)
        self.highlight_bg_alpha = 0.18                   # reserved for future alpha handling

        # GUI control commands
        self.show_gui_commands = ["help", "show help", "show panel"]
        self.hide_gui_commands = ["hide", "hide help", "hide panel"]

        self.site_aliases = {
            "gmail": "https://mail.google.com",
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
        }
        
        # Browser / navigation preferences
        # None means "use the operating system's default browser/application"
        self.preferred_browser = None
        self.browser_open_target = "about:blank"  # fallback target when user says "open browser"
