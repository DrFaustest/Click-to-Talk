"""
Speech Handler Module
Handles microphone input and speech-to-text conversion
"""

import speech_recognition as sr
from config import Config
import threading  # [ADDED] use a lock to prevent overlapping mic contexts

class SpeechHandler:
    def __init__(self, config, command_parser, mouse_controller):
        self.config = config
        self.command_parser = command_parser
        self.mouse_controller = mouse_controller
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.listening = False
        self.stop_callback = None
        self._active_lock = threading.Lock()  # [ADDED] ensures only one listen loop uses the mic at a time

        # Adjust for ambient noise
        print("Adjusting for ambient noise... Please wait.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Ready to listen.")

    def set_stop_callback(self, callback):
        """Set callback function for stop commands"""
        self.stop_callback = callback

    def start_listening(self):
        """
        Start continuous speech recognition.

        IMPORTANT:
        - If already listening, do nothing (prevents second thread from re-entering).
        - Only one thread can use the microphone at a time (guarded by _active_lock).
        """
        if self.listening:  # [ADDED] idempotent start guard
            print("Already listening; start request ignored.")  # [ADDED]
            return  # [ADDED]

        self.listening = True  # [ADDED] flip the flag here so GUI 'Start' can't spin up another thread immediately
        print("Speech recognition started. Say commands...")

        # One listen loop owns the mic at a time
        with self._active_lock:  # [ADDED] prevent overlapping mic contexts across threads
            try:
                # Open the mic ONCE for the whole run (prevents nested context manager errors)
                with self.microphone as source:  # [ADDED] moved 'with' outside the while loop
                    while self.listening:
                        try:
                            print("Listening...")
                            audio = self.recognizer.listen(
                                source,
                                timeout=5,  # you already expose this in config.listen_timeout if you want to swap
                                phrase_time_limit=5
                            )

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
            finally:
                # ensure we flip the flag off if we exit due to any reason
                self.listening = False  # [ADDED] make state consistent when loop exits

    def stop_listening(self):
        """Stop speech recognition"""
        # Just flip the flag; the loop will exit and close the mic context cleanly
        self.listening = False  # [ADDED] ensure the loop stops and releases mic
        print("Speech recognition stopped.")
