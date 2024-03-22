"""Config file for the assistant"""

import os

import dotenv
import torch

dotenv.load_dotenv()

# Directory with the commands
COMMANDS_DIR = os.path.join(os.path.dirname(__file__), os.getenv("COMMANDS_DIR"))

# TTS (silero) model parameters
LANGUAGE: str = os.getenv("LANGUAGE")
MODEL_ID: str = os.getenv("MODEL_ID")
SPEAKER: str = os.getenv("SPEAKER")
TTS_SAMPLE_RATE = int(os.getenv("TTS_SAMPLE_RATE"))
TTS_DEVICE = torch.device("cpu")

# STT parameters
PICOVOICE_API_KEY: str = os.getenv("PICOVOICE_API_KEY")
PICOVOICE_KEYWORD_PATH: str = os.path.join(
    os.path.dirname(__file__), os.getenv("PICOVOICE_KEYWORD_PATH")
)
STT_SAMPLE_RATE: int = int(os.getenv("STT_SAMPLE_RATE"))
STT_DEVICE: int = int(os.getenv("STT_DEVICE"))
MODEL_PATH: str = os.path.join(os.path.dirname(__file__), os.getenv("MODEL_PATH"))

# Other parameters
KEYWORD_DETECTION_TIMEOUT: int = int(os.getenv("KEYWORD_DETECTION_TIMEOUT"))
INITIAL_DETECTION_DELAY: int = int(os.getenv("INITIAL_DETECTION_DELAY"))
CMD_RECOGNITION_TRESHHOLD: int = int(os.getenv("CMD_RECOGNITION_TRESHHOLD"))
BROWSER_PATH: str = os.getenv("BROWSER_PATH")

OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

# TODO: Currently not used
NAME_ALIAS = []
POINTERS = []
