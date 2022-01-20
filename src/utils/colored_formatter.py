import logging

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': MAGENTA,
    'ERROR': RED
}

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"


def format_color(message, color):
    message = f"{COLOR_SEQ % (30 + color)}{message}{RESET_SEQ}" 
    return message

def format_black(message):
    return format(message, BLACK)

def format_red(message):
    return format(message, RED)

def format_green(message):
    return format(message, GREEN)

def format_yellow(message):
    return format(message, YELLOW)

def format_blue(message):
    return format(message, BLUE)

def format_magenta(message):
    return format(message, MAGENTA)

def format_cyan(message):
    return format(message, CYAN)

def format_white(message):
    return format(message, WHITE)

def format_bold(message):
    message = f"{BOLD_SEQ}{message}{RESET_SEQ}"
    return message

class colored_formatter(logging.Formatter):
    def __init__(self, msg, use_color = True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color
        
    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)