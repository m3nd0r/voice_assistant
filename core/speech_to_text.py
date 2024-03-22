import json
import logging
import queue
import struct
import sys
import time

import pvporcupine
import vosk
from pvrecorder import PvRecorder

import config


class STT:
    """
    Speech to text class
    """

    def __init__(self):
        self.model = vosk.Model(model_path=config.MODEL_PATH)
        self.sample_rate = config.STT_SAMPLE_RATE
        self.q = queue.Queue()
        self.porcupine = self._init_porcupine()
        self.recorder = self._init_recorder()
        self.vosk = self._init_vosk()
        self.last_detection_time = time.time() - config.INITIAL_DETECTION_DELAY

    def _init_porcupine(self) -> pvporcupine.Porcupine:
        """
        Initialize the Porcupine wake word engine to detect the keyword
        and start the voice recognition
        :return:
        """
        try:
            return pvporcupine.create(
                access_key=config.PICOVOICE_API_KEY,
                keyword_paths=[config.PICOVOICE_KEYWORD_PATH],
                sensitivities=[1],
            )
        except pvporcupine.PorcupineActivationError as e:
            logging.error(f"An error occurred while activating Porcupine: {e}", exc_info=True)
            sys.exit(1)

    def _init_recorder(self) -> PvRecorder:
        """
        Initialize the recorder
        :return:
        """
        try:
            # TODO: refactor to remove hardcoded device index
            return PvRecorder(
                device_index=1,
                frame_length=self.porcupine.frame_length,
            )
        except Exception as e:
            logging.error(f"An error occurred while initializing the recorder: {e}", exc_info=True)
            sys.exit(1)

    def _init_vosk(self) -> vosk.KaldiRecognizer:
        """
        Initialize the Vosk recognizer to recognize the speech and convert it to text
        :return:
        """
        return vosk.KaldiRecognizer(self.model, self.sample_rate)

    def _start_listening(self) -> None:
        """
        Start listening to the user input
        :return:
        """
        self.recorder.start()
        logging.info("Started listening to the user input")
        logging.info(f"Using device: {self.recorder.selected_device}")

    def _detect_keyword(self) -> bool:
        """
        Detect the exact keyword
        :return: True if the keyword was detected, False otherwise
        """
        voice_input = self.recorder.read()
        keyword_index = self.porcupine.process(voice_input)
        if keyword_index >= 0:
            logging.info("Keyword detected")
            self.last_detection_time = time.time()
            return True
        return False

    def _process_voice_input(self, callback: callable) -> bool:
        """
        Process the voice input and call the function to process the recognized text
        :param callback: The callback function to call
        :return: True if the voice input was processed, False otherwise
        """
        # TODO: refactor to remove bool return
        voice_input = self.recorder.read()
        if voice_input:
            data = struct.pack("h" * len(voice_input), *voice_input)
            if self.vosk.AcceptWaveform(data):
                self.recorder.stop()
                recognized = callback(json.loads(self.vosk.Result())["text"])
                self.recorder.start()
                return recognized
        return False

    def va_listen(self, callback: callable) -> None:
        """
        Listen to the user input, recognize the speech and call the callback function
        :param callback:
        :return:
        """
        self._start_listening()

        try:
            while True:
                if self._detect_keyword():
                    logging.info("Listening to the user input")
                    while time.time() - self.last_detection_time <= config.KEYWORD_DETECTION_TIMEOUT:
                        success = self._process_voice_input(callback)
                        if success:
                            self.last_detection_time = time.time()
        except Exception as e:
            logging.error(f"An error occurred while listening to the user input: {e}", exc_info=True)
            self.recorder.stop()
            sys.exit(1)
