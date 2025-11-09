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
        self.energy_threshold = 300  # microphone sensitivity
        self.pause_threshold = 0.8  # seconds of silence to end phrase
        self.phrase_time_limit = 5  # max seconds for a phrase

        # Application settings
        self.listen_timeout = 5  # seconds to wait for speech

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

        # Cursor highlight ("find") 
        self.highlight_size = 140                        # highlight diameter (px)
        self.highlight_border = 6                        # ring thickness (px)
        self.highlight_duration_ms = 900                 # display time (ms)
        self.highlight_color = "#00A3FF"               # ring color (high-contrast cyan)
        self.highlight_bg_alpha = 0.18                   # reserved for future alpha handling


        self.site_aliases = {
            "gmail": "https://mail.google.com",
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
        }
        
        self.preferred_browser = "Google Chrome"  # macOS exact name
        # (Windows would be: "chrome")