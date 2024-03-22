import importlib.util
import logging
import random
from types import ModuleType
from typing import Optional

from openai import OpenAI

import config


class CommandBase:
    def __init__(self, *args, **kwargs):
        self.name = None
        self.action = None
        self.aliases = []
        self.responses = []
        self.script_path = None
        self.depends_on = None
        self.params = {}
        self.arguments = []


class CommandVoice(CommandBase):
    """
    Simple commands that only require a voice response
    """

    def execute(self, *args, **kwargs) -> str:
        return random.choice(self.responses)


class CommandScript(CommandBase):
    """
    Commands that require a script to be executed
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_script_path(self) -> str:
        """
        Get the path to the script file.
        If the command depends on another command, return the path of the dependent command
        :return: The path to the script file
        """
        if self.depends_on:
            return self.depends_on.script_path
        return self.script_path

    def get_result_from_script(self, script_module: ModuleType) -> Optional[str]:
        """
        Get the result from the script module
        :param script_module: The script module
        :return: The result
        """
        try:
            result = script_module.script(*self.arguments, **self.params)
        except Exception as e:
            logging.error(f"Error executing the script: {e}", exc_info=True)
            return None
        return result

    def execute(self, *args, **kwargs) -> Optional[str]:
        """
        Execute the script. The script should be placed in the same directory as the command config
        and has a name "script.py"
        :return:
        """
        spec = importlib.util.spec_from_file_location("script", self.get_script_path())
        script_module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(script_module)
        except FileNotFoundError as e:
            logging.error(f"Script file {self.script_path} not found for command {self.name}: {e}")

        result = self.get_result_from_script(script_module)

        return result


class CommandChatGPT(CommandBase):
    """
    Commands that require a request to the ChatGPT API
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = OpenAI(
            api_key=config.OPENAI_API_KEY,
        )

    def execute(self, *args, **kwargs) -> str:
        """
        Get the voice input and send a request to the ChatGPT API
        :param args: list of words from the user input
        :param kwargs: The keyword arguments
        :return: The response from the ChatGPT API
        """
        self.arguments = " ".join(args[0])
        logging.info(f"Executing ChatGPT command with arguments: {self.arguments}")
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": " ".join(self.arguments)},
            ],
        )
        logging.info(f"ChatGPT response: {response.choices[0].message.content}")
        return str(response.choices[0].message.content)


COMMAND_TYPES = {
    "voice": CommandVoice,
    "script": CommandScript,
    "chat_gpt": CommandChatGPT,
}
