from pytermx import Color

def print_success(message, *argv):
    print(Color.GREEN + "[ OK ] " + Color.RESET + Color.BRIGHT_WHITE, end="")
    print(message, end=" ")
    for arg in argv:
        print(arg, end=" ")
    print("")

def print_error(message, *argv):
    print(Color.RED + "[ ERR ] " + Color.RESET + Color.BRIGHT_WHITE, end="")
    print(message, end=" ")
    for arg in argv:
        print(arg, end=" ")
    print("")

def print_status(message, new_line: bool = True):
    if new_line:
        print(Color.BLUE + "[ * ] " + Color.RESET + Color.BRIGHT_WHITE + message)
    else:
        print(Color.BLUE + "[ * ] " + Color.RESET + Color.BRIGHT_WHITE + message, end="\r")

def ask_question(message, *argv):
    message = Color.BLUE + "[ ? ] " + Color.RESET + Color.BRIGHT_WHITE + message
    for arg in argv:
        message = message + " " + arg
    print(message, end="")
    ret = input("> ")
    return ret