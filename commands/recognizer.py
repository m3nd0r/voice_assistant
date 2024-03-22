import logging

from fuzzywuzzy import fuzz

import config

logging.basicConfig(level=logging.INFO)


class CommandRecognizer:
    """
    Class to recognize the command from the user input
    """

    def __init__(self, aliases: dict):
        self.aliases = aliases

    @staticmethod
    def format_aliases(aliases: dict) -> list:
        """
        Format the aliases
        :param aliases: The aliases list
        :return: The formatted aliases list
        """
        return [(cmd_name, alias) for cmd_name, aliases in aliases.items() for alias in aliases]

    @staticmethod
    def clean_voice_input(text_input: str) -> str:
        """
        Clean the user input from the name and the pointers to get the command
        :param text_input: Text input from the user
        :return: User's input cleaned from the name and the pointers
        """
        for x in config.NAME_ALIAS:
            text_input = text_input.replace(x, "").strip()

        for x in config.POINTERS:
            text_input = text_input.replace(x, "").strip()

        return text_input

    def detect_cmd(self, text_input: str) -> dict:
        """
        Recognize the command from the user input
        :param text_input: The user input
        :return: The closet command and the percentage of the match
        """
        best_match = {"cmd_name": "", "score": 0, "arguments": []}
        best_alias = ""
        logging.info(f"Text input: {text_input}")
        for cmd_name, alias in self.aliases:
            current_score = fuzz.partial_ratio(text_input, alias)
            if current_score > best_match["score"]:
                best_match["score"] = current_score
                best_match["cmd_name"] = cmd_name
                best_alias = alias

        if best_match["score"] > config.CMD_RECOGNITION_TRESHHOLD:
            best_match["recognized"] = True
            args_str = text_input.replace(best_alias, "", 1).strip()
            best_match["arguments"] = args_str.split() if args_str else []
        return best_match
