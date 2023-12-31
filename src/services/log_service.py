from datetime import datetime


def log(service, message):
    # Log provided message to a file and add a timestamp
    with open("log.txt", "a", encoding="utf-8") as log_file:
        message = message.replace("\n", "\n\t")
        log_file.write(f"{datetime.now()} - {service}: \n\t{message}\n")
