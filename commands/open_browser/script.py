import logging
import subprocess

import config

browser_path = config.BROWSER_PATH


def script(*args, **kwargs) -> None:
    """
    Open the browser with the given URL
    :param args: The arguments
    :param kwargs: The keyword arguments
    :return: None
    """
    url = kwargs.get("url", "https://www.google.com")
    try:
        subprocess.run([browser_path, url])
    except Exception as e:
        logging.error(f"An error occurred while opening the browser: {e}", exc_info=True)
    return None
