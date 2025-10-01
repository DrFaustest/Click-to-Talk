"""
Speech Handler Module
Handles microphone input and speech-to-text conversion
"""

import speech_recognition as sr
from config import Config

class SpeechHandler:
    def __init__(self, config, command_parser, mouse_controller):
        self.config = config
        self.command_parser = command_parser
        self.mouse_controller = mouse_controller
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.listening = False
        self.stop_callback = None

        # Adjust for ambient noise
        print("Adjusting for ambient noise... Please wait.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Ready to listen.")

    def set_stop_callback(self, callback):
        """Set callback function for stop commands"""
        self.stop_callback = callback

    def start_listening(self):
        """Start continuous speech recognition"""
        self.listening = True
        print("Speech recognition started. Say commands...")

        while self.listening:
            try:
                with self.microphone as source:
                    print("Listening...")
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)

                # Recognize speech using Google Speech Recognition
                text = self.recognizer.recognize_google(audio).lower()
                print(f"Recognized: {text}")

                # Check for stop commands first
                if text in self.config.stop_commands:
                    print("Stop command received. Shutting down...")
                    if self.stop_callback:
                        self.stop_callback()
                    break

                # Parse and execute command
                self.command_parser.parse_command(text)

            except sr.WaitTimeoutError:
                # Timeout, continue listening
                continue
            except sr.UnknownValueError:
                print("Could not understand audio")
                continue
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                continue
            except Exception as e:
                print(f"Error in speech recognition: {e}")
                continue

    def stop_listening(self):
        """Stop speech recognition"""
        self.listening = False
        print("Speech recognition stopped.")