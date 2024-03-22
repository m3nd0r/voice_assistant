import datetime

from num2t4ru import num2text
from num2words import num2words

import config


def script(*args, **kwargs):
    """
    Returns the current time in words. Currently only supports English and Russian.
    """
    now = datetime.datetime.now()
    hours, minutes = now.hour, now.minute
    if config.LANGUAGE != "ru":
        return num2words(hours) + " " + num2words(minutes)
    return num2text(hours) + " " + num2text(minutes)
