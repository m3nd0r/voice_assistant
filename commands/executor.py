import logging

from core.text_to_speech import tts


class CommandExecutor:
    def __init__(self, commands: dict) -> None:
        self.commands = commands
        self.tts = tts

    def execute_cmd(self, cmd_name: str, arguments: list) -> bool:
        """
        Execute the command
        :param cmd_name: The name of the command to execute
        :param arguments: The arguments for the command
        :return: True if the command was executed, False otherwise
        """
        command = self.commands.get(cmd_name) or self.commands.get("chat_gpt")
        # TODO: fix the problem with script commands returning None (e.g. open_browser)
        response = command.execute(arguments)
        # If we have a response, speak it
        if response:
            self.tts.speak(response)
            return True

        logging.warning(f"Command {cmd_name} not found in the commands list.")
        return False
