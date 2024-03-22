import json
import logging
import os
from pathlib import Path
from typing import List, Optional

from commands import command_types


class CommandCreator:
    """
    Class to create the command classes from the json configs
    """

    def __init__(self):
        self.commands_dir = os.path.join(os.path.dirname(__file__))
        self.commands = {}

    @staticmethod
    def create_command_class(
        name: str,
        action: str,
        aliases: List[str],
        responses: Optional[List[str]] = None,
        script_path: Optional[str] = None,
        depends_on: str = None,
        params: Optional[dict] = None,
    ) -> type:
        """
        Create a new command class and set default attributes
        :param name: Name of the command
        :param action: Action to execute
        :param aliases: List of aliases for the command
        :param responses: List of responses for the command
        :param script_path: Path to the script for the command
        :param depends_on: Name of the command this command depends on
        :param params: Parameters for the command (read from the config)
        :param arguments: Arguments for the command (recognized from the user input)
        :return: New command class
        """
        command = command_types.COMMAND_TYPES.get(action)()
        # Set attributes to the class
        args = locals().copy()
        for attr in args:
            try:
                setattr(command, attr, args[attr])
            except AttributeError as e:
                logging.error(f"Error setting the attribute {attr} to the command class: {e}")
        return command

    def parse_configs(self) -> dict[str, command_types.CommandBase]:
        """
        Parse the all the configs and create the command classes
        :return: Dictionary of the command classes
        """
        command_dir_path = Path(self.commands_dir)
        for config_file in command_dir_path.rglob("config.json"):
            with open(config_file, "r") as f:
                logging.info(f"Reading the command config: {config_file}")
                commands = self.create_commands(f.read())
                self.commands.update(commands)
        self.create_command_dependencies()
        logging.info(f"Commands created: {self.commands}")
        return self.commands

    def create_commands(self, config: str) -> dict[str, command_types.CommandBase]:
        """
        Create commands from the config
        :param config: The command config as a string in JSON format
        :return:
        """
        commands = {}
        try:
            cmd_json = json.loads(config)
        except json.JSONDecodeError as e:
            logging.error(f"Error parsing the command config: {e}", exc_info=True)
            return self.commands

        for command_data in cmd_json["commands"]:
            command_name = command_data.get("name")
            action = command_data.get("action")
            command_aliases = command_data.get("aliases", [])
            responses = command_data.get("responses")
            # Check if the command has a script
            script_path = (
                os.path.join(f"commands/{command_name}/script.py") if action == "script" else None
            )
            depends_on = command_data.get("depends_on")
            params = command_data.get("params", {})

            command = self.create_command_class(
                command_name,
                action,
                command_aliases,
                responses,
                script_path,
                depends_on,
                params,
            )
            commands[command_name] = command

        return commands

    def create_command_dependencies(self) -> None:
        """
        Create the command dependencies after all the commands are created
        When a command depends on another command, set the dependency
        :return:
        """
        for command_name, command in self.commands.items():
            if command.depends_on:
                depends_on = self.commands.get(command.depends_on)
                if depends_on is None:
                    logging.error(
                        f"Command {command_name} depends on {command.depends_on} which does not exist."
                    )
                    continue
                command.depends_on = depends_on
