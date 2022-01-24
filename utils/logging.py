from utils.colors import bcolors


def warning(msg):
    print(f"[{bcolors.WARNING}WARNING{bcolors.ENDC}] " + str(msg))


def error(msg):
    print(f"[{bcolors.FAIL}ERROR{bcolors.ENDC}] " + str(msg))


def info(msg):
    print(f"[{bcolors.OKBLUE}INFO{bcolors.ENDC}] " + str(msg))


def success(msg):
    print(f"[{bcolors.OKGREEN}SUCCESS{bcolors.ENDC}] " + str(msg))
