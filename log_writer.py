import os
from datetime import datetime

first_call_time = None

def get_log_filename():
    global first_call_time

    if first_call_time is None:
        first_call_time = datetime.now()

    log_filename = first_call_time.strftime("logs/%b-%d-%H-%M-%S-%Y")

    return log_filename

def logger(text: str):
    log_filename = get_log_filename()

    timestamp_prefix = datetime.now().strftime("[%H:%M:%S]")

    log_line = f"{timestamp_prefix} {text}\n"

    os.makedirs(os.path.dirname(log_filename), exist_ok=True)

    with open(log_filename + ".log", "a", encoding='utf-8') as log_file:
        log_file.write(log_line)