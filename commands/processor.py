"""Class to process commands from the user"""

import logging

from commands.command_types import CommandBase
from commands.creator import CommandCreator
from commands.executor import CommandExecutor
from commands.recognizer import CommandRecognizer

logging.basicConfig(level=logging.INFO)


class CommandProcessor:
    """
    Class to process commands from the user
    """

    def __init__(self) -> None:
        self.commands = self.read_commands_from_configs()
        self.aliases = self.read_commands_aliases()

    @staticmethod
    def read_commands_from_configs() -> dict[str, CommandBase]:
        """
        Read the commands from the configs
        :return: The commands dictionary
        """
        return CommandCreator().parse_configs()

    def read_commands_aliases(self):
        """
        Read the commands aliases from the commands
        :return: The commands aliases dictionary
        """
        return [
            (command.name, alias) for command in self.commands.values() for alias in command.aliases
        ]

    def respond(self, raw_voice: str):
        """
        Respond to the user input.
        First, clean the user input, then recognize the command and execute it.
        :param raw_voice: The raw user input from the microphone
        :return: The response from the command
        """
        logging.info("Recognizing the command")
        recognizer = CommandRecognizer(self.aliases)
        cmd = recognizer.detect_cmd(raw_voice)

        # TODO: refactor this solution
        if cmd["cmd_name"] == "":
            logging.warning("Command not recognized")
            return ""

        logging.info(f"Command recognized: {cmd}")
        logging.info("Executing the command")
        # TODO: refactor to make the executor more readable
        executor = CommandExecutor(self.commands)
        return executor.execute_cmd(
            cmd_name=cmd["cmd_name"],
            arguments=cmd["arguments"],
        )
