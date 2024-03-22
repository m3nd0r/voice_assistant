import re

import sounddevice as sd


def choose_microphone() -> int:
    """
    Choose the microphone to use
    :return: The index of the chosen microphone
    """
    for number, microphone in enumerate(sd.query_devices()):
        print(f"{number}: {microphone['name']}")
    return int(input("Choose the microphone: "))


def to_camel_case(input_string: str) -> str:
    """
    Convert a string to camel case
    :param input_string: The string to convert
    :return: The string in camel case
    """
    if not input_string:
        raise ValueError('The value of "input_string" can not be empty')
    words: str = re.findall(r"[A-Z][a-z]*|[a-z]+|\d+|[-_]+|\s+", input_string)
    words = [word.strip() for word in words if word.strip() != ""]
    if not words:
        return input_string[0].lower() + input_string[1:]
    camel_case_words = [words[0].lower()] + [word.capitalize() for word in words[1:]]
    return "".join(camel_case_words).replace("-", "").replace("_", "")
