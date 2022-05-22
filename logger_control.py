import os

LOG_FILE = os.path.join(".", "logs_file.log")


def debug(mesg):
    print(mesg)
    with open(LOG_FILE, 'a') as f:
        f.write(f"{mesg}\n")
