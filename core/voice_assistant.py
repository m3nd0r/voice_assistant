import config
from commands.processor import CommandProcessor
from core.speech_to_text import STT


class VoiceAssistant:
    """
    The voice assistant class
    """

    def __init__(self) -> None:
        self.stt = STT()
        self.cmd_processor = CommandProcessor()
        self.microphone = config.STT_DEVICE

    @property
    def aliases(self):
        return self.cmd_processor.aliases

    @property
    def commands(self):
        return self.cmd_processor.commands

    def listen(self):
        """
        Listen to the user input
        :return:
        """
        self.stt.va_listen(self.cmd_processor.respond)

    def run(self):
        self.listen()
