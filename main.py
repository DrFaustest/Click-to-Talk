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

class ClickToTalkApp:
    def __init__(self):
        self.config = Config()
        self.mouse_controller = MouseController(self.config)
        self.command_parser = CommandParser(self.config)
        self.command_parser.set_mouse_controller(self.mouse_controller)
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
        print("Starting speech recognition...")

        self.running = True

        # Start speech recognition in a separate thread
        speech_thread = threading.Thread(target=self.speech_handler.start_listening)
        speech_thread.daemon = True
        speech_thread.start()

        try:
            while self.running:
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