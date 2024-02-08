"""Module Description: This module contains a function for logging messages to a file with timestamps.

Functions:
    log(service: str, message: str) -> None: Logs the provided message to a file with a timestamp.
"""

from datetime import datetime

def log(service: str, message: str) -> None:
    """Logs the provided message to a file with a timestamp.

    Args:
        service (str): The name of the service.
        message (str): The message to be logged.
    """
    # Log provided message to a file and add a timestamp
    with open("log.txt", "a", encoding="utf-8") as log_file:
        message = message.replace("\n", "\n\t")
        log_file.write(f"{datetime.now()} - {service}: \n\t{message}\n")
