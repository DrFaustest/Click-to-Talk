"""
Speech Handler Module
Handles microphone input and speech-to-text conversion
"""

import speech_recognition as sr
from config import Config
import threading

# Import sounddevice backend for speech_recognition
try:
    import sounddevice as sd
    _has_sounddevice = True
except ImportError:
    _has_sounddevice = False


class SoundDeviceMicrophone(sr.Microphone):
    """
    Custom Microphone class that uses sounddevice instead of PyAudio.
    This is a modern alternative compatible with Python 3.14+
    """
    
    @staticmethod
    def get_pyaudio():
        """
        Override to use sounddevice instead of PyAudio.
        Returns a compatible interface that speech_recognition can use.
        """
        if not _has_sounddevice:
            raise AttributeError("Could not find sounddevice; check installation")
        
        # Create a mock PyAudio-compatible interface using sounddevice
        import struct
        import numpy as np
        
        class SoundDeviceWrapper:
            """Wrapper to make sounddevice compatible with PyAudio interface"""
            paInt16 = np.int16
            
            class PyAudio:
                def __init__(self):
                    pass
                
                def get_device_count(self):
                    return len(sd.query_devices())
                
                def get_device_info_by_index(self, index):
                    device = sd.query_devices(index)
                    return {
                        'name': device['name'],
                        'defaultSampleRate': device['default_samplerate']
                    }
                
                def get_default_input_device_info(self):
                    device = sd.query_devices(kind='input')
                    return {
                        'name': device['name'],
                        'defaultSampleRate': device['default_samplerate']
                    }
                
                def terminate(self):
                    pass
                
                def open(self, **kwargs):
                    return SoundDeviceStream(**kwargs)
            
            @staticmethod
            def get_sample_size(format_type):
                return np.dtype(format_type).itemsize
        
        class SoundDeviceStream:
            """Stream wrapper for sounddevice"""
            def __init__(self, rate, channels, format, input, frames_per_buffer, input_device_index=None):
                self.rate = rate
                self.channels = channels
                self.format = format
                self.frames_per_buffer = frames_per_buffer
                self.device_index = input_device_index
                self.stream = None
                self.buffer = []
                self._is_stopped = True
                self._lock = __import__('threading').Lock()
                
            def start_stream(self):
                def callback(indata, frames, time, status):
                    if status:
                        print(f"Stream status: {status}")
                    with self._lock:
                        self.buffer.append(indata.copy())
                
                self.stream = sd.InputStream(
                    samplerate=self.rate,
                    channels=self.channels,
                    dtype=self.format,
                    blocksize=self.frames_per_buffer,
                    device=self.device_index,
                    callback=callback
                )
                self.stream.start()
                self._is_stopped = False
                return self
            
            def read(self, num_frames, exception_on_overflow=True):
                import time
                
                # Ensure stream is running
                if not self.stream or self._is_stopped:
                    if not self.stream:
                        self.start_stream()
                    elif self._is_stopped:
                        self.stream.start()
                        self._is_stopped = False
                
                # Calculate how much data we need
                bytes_per_sample = np.dtype(self.format).itemsize
                target_frames = num_frames
                
                # Wait for enough data with timeout
                timeout = 10  # 10 second timeout
                start_time = time.time()
                
                while True:
                    with self._lock:
                        if self.buffer:
                            # Concatenate all buffered chunks
                            all_data = np.concatenate(self.buffer)
                            self.buffer = []
                            
                            # If we have enough or more data, return what we need
                            if len(all_data) >= target_frames:
                                result = all_data[:target_frames]
                                # Keep excess for next read
                                if len(all_data) > target_frames:
                                    self.buffer = [all_data[target_frames:]]
                                return result.tobytes()
                            else:
                                # Not enough yet, put it back and continue waiting
                                self.buffer = [all_data]
                    
                    # Check timeout
                    if time.time() - start_time > timeout:
                        # Return whatever we have, padded with silence if needed
                        with self._lock:
                            if self.buffer:
                                data = np.concatenate(self.buffer)
                                self.buffer = []
                                if len(data) < target_frames:
                                    # Pad with zeros
                                    padding = np.zeros(target_frames - len(data), dtype=self.format)
                                    data = np.concatenate([data, padding])
                                return data[:target_frames].tobytes()
                            else:
                                # Return silence
                                return np.zeros(target_frames, dtype=self.format).tobytes()
                    
                    time.sleep(0.01)
            
            def is_stopped(self):
                """Check if stream is stopped"""
                return self._is_stopped
            
            def stop_stream(self):
                if self.stream and not self._is_stopped:
                    self.stream.stop()
                    self._is_stopped = True
                return self
            
            def close(self):
                if self.stream:
                    if not self._is_stopped:
                        self.stream.stop()
                    self.stream.close()
                    self.stream = None
                    self._is_stopped = True
        
        return SoundDeviceWrapper()


class SpeechHandler:
    def __init__(self, config, command_parser, mouse_controller):
        self.config = config
        self.command_parser = command_parser
        self.mouse_controller = mouse_controller
        self.recognizer = sr.Recognizer()
        
        # Apply tuning from config for better pickup
        try:
            self.recognizer.energy_threshold = getattr(self.config, "energy_threshold", 300)
            self.recognizer.dynamic_energy_threshold = getattr(self.config, "dynamic_energy_threshold", True)
            self.recognizer.pause_threshold = getattr(self.config, "pause_threshold", 0.8)
            self.recognizer.non_speaking_duration = getattr(self.config, "non_speaking_duration", 0.3)
        except Exception:
            pass

        # Choose microphone device by index or name (sounddevice-backed)
        device_index = self._resolve_input_device_index(getattr(self.config, "mic_device", None))
        self._device_index = device_index
        if device_index is not None:
            try:
                import sounddevice as _sd
                dev_info = _sd.query_devices(device_index)
                self._device_name = dev_info.get("name", f"Device {device_index}")
            except Exception:
                self._device_name = f"Device {device_index}"
            print(f"Using microphone device index {device_index} ({getattr(self, '_device_name', 'unknown')})")
        else:
            # Default input device
            try:
                import sounddevice as _sd
                dinfo = _sd.query_devices(kind='input')
                self._device_name = dinfo.get("name", "Default Input")
            except Exception:
                self._device_name = "Default Input"
        
        # Use sounddevice-based microphone instead of PyAudio
        self.microphone = SoundDeviceMicrophone(device_index=device_index)
        
        self.listening = False
        self.stop_callback = None
        self._active_lock = threading.Lock()

        # Adjust for ambient noise
        print("Adjusting for ambient noise... Please wait.")
        with self.microphone as source:
            adj_dur = getattr(self.config, "energy_adjust_duration", 1.0)
            self.recognizer.adjust_for_ambient_noise(source, duration=adj_dur)
        print("Ready to listen.")

    def get_current_device(self):
        """Return a tuple (index, name) for the active input device."""
        return (self._device_index, getattr(self, "_device_name", None))

    def list_input_devices(self):
        """Return a list of input-capable devices: [{index, name, max_input_channels}]"""
        try:
            import sounddevice as _sd
            devices = _sd.query_devices()
            result = []
            for i, d in enumerate(devices):
                if d.get("max_input_channels", 0) > 0:
                    result.append({
                        "index": i,
                        "name": d.get("name", f"Device {i}"),
                        "max_input_channels": d.get("max_input_channels", 0),
                    })
            return result
        except Exception:
            return []

    def switch_microphone(self, device_index: int, restart_if_listening: bool = True):
        """Switch to a different input device and recalibrate.
        If currently listening and restart_if_listening is True, restart the listening loop automatically.
        """
        was_listening = self.listening
        # Stop current loop if running
        if was_listening:
            self.stop_listening()

        with self._active_lock:
            try:
                # Update device info
                self._device_index = device_index
                try:
                    import sounddevice as _sd
                    dev_info = _sd.query_devices(device_index)
                    self._device_name = dev_info.get("name", f"Device {device_index}")
                except Exception:
                    self._device_name = f"Device {device_index}"

                # Recreate microphone and recalibrate ambient noise
                self.microphone = SoundDeviceMicrophone(device_index=device_index)
                print("Adjusting for ambient noise on new device... Please wait.")
                with self.microphone as source:
                    adj_dur = getattr(self.config, "energy_adjust_duration", 1.0)
                    self.recognizer.adjust_for_ambient_noise(source, duration=adj_dur)
                print(f"Switched to device {device_index} ({self._device_name}).")
            except Exception as e:
                print(f"Failed to switch microphone: {e}")

        # Optionally restart
        if was_listening and restart_if_listening:
            t = threading.Thread(target=self.start_listening, daemon=True)
            t.start()

    def _resolve_input_device_index(self, pref):
        """Resolve a microphone device index using sounddevice list.
        pref can be an int index or a case-insensitive substring of the device name.
        Returns None if no specific preference is provided or not found.
        """
        try:
            if pref is None:
                return None
            if isinstance(pref, int):
                return pref
            # Find by name substring
            import sounddevice as _sd
            devices = _sd.query_devices()
            target = str(pref).lower()
            # prefer input-capable devices
            for i, dev in enumerate(devices):
                name = str(dev.get('name', '')).lower()
                if target in name and dev.get('max_input_channels', 0) > 0:
                    return i
            # fallback: first name match even if no input advertised
            for i, dev in enumerate(devices):
                name = str(dev.get('name', '')).lower()
                if target in name:
                    return i
        except Exception:
            pass
        return None

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
        if self.listening:  
            print("Already listening; start request ignored.")  
            return  

        self.listening = True  # flip the flag here so GUI 'Start' can't spin up another thread immediately
        print("Speech recognition started. Say commands...")

        # One listen loop owns the mic at a time
        with self._active_lock:  # prevent overlapping mic contexts across threads
            try:
                # Open the mic ONCE for the whole run (prevents nested context manager errors)
                with self.microphone as source: 
                    while self.listening:
                        try:
                            print("Listening...")
                            audio = self.recognizer.listen(
                                source,
                                timeout=getattr(self.config, "listen_timeout", 5),
                                phrase_time_limit=getattr(self.config, "phrase_time_limit", 5)
                            )

                            # Recognize speech using Google Speech Recognition
                            lang = getattr(self.config, "recognition_language", "en-US")
                            text = self.recognizer.recognize_google(audio, language=lang).lower()
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
                self.listening = False  # make state consistent when loop exits

    def stop_listening(self):
        """Stop speech recognition"""
        # Just flip the flag; the loop will exit and close the mic context cleanly
        self.listening = False  # ensure the loop stops and releases mic
        print("Speech recognition stopped.")

    def recalibrate(self, duration: float | None = None):
        """Re-run ambient noise calibration with optional custom duration."""
        dur = duration if duration is not None else getattr(self.config, "energy_adjust_duration", 1.0)
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=dur)
            print("Recalibrated ambient noise.")
        except Exception as e:
            print(f"Calibration error: {e}")

    def set_recognition_params(self, *, energy_threshold=None, dynamic_energy_threshold=None,
                                pause_threshold=None, non_speaking_duration=None, language=None):
        """Update recognizer parameters at runtime."""
        try:
            if energy_threshold is not None:
                self.recognizer.energy_threshold = float(energy_threshold)
                self.config.energy_threshold = float(energy_threshold)
            if dynamic_energy_threshold is not None:
                self.recognizer.dynamic_energy_threshold = bool(dynamic_energy_threshold)
                self.config.dynamic_energy_threshold = bool(dynamic_energy_threshold)
            if pause_threshold is not None:
                self.recognizer.pause_threshold = float(pause_threshold)
                self.config.pause_threshold = float(pause_threshold)
            if non_speaking_duration is not None:
                self.recognizer.non_speaking_duration = float(non_speaking_duration)
                self.config.non_speaking_duration = float(non_speaking_duration)
            if language is not None:
                self.config.recognition_language = str(language)
        except Exception as e:
            print(f"Error updating recognition params: {e}")
