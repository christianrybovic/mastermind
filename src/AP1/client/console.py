# Copyright (c) 2026 Team Alpha
# All rights reserved.
#
# Licensed under the MIT License. See LICENSE file for details

from enum import Enum
import subprocess
import sys
import re


class COLOR(Enum):
    RED    = 1
    ORANGE = 2
    YELLOW = 3
    GREEN  = 4
    BLUE   = 5
    VIOLET = 6
    ACCENT = 7


ANSI_ESCAPE   = re.compile(r"\x1b\[[0-9;]*m")
MAX_WIDTH     = 91
DEFAULT_COLOR = '\033[0m'
CURSOR_UP     = '\x1b[1A'
ERASE_LINE    = '\x1b[2K'
COLORS: dict[COLOR, str] = {
    COLOR.RED:       '\033[31m',
    COLOR.ORANGE:    '\033[38;5;208m',
    COLOR.YELLOW:    '\033[33m',
    COLOR.GREEN:     '\033[32m',
    COLOR.BLUE:      '\033[34m',
    COLOR.VIOLET:    '\033[35m',
    COLOR.ACCENT:    '\033[38;5;214m'
}


def colorize(text: str, color: COLOR) -> str:
    """Add color to the text."""
    return COLORS[color] + text + DEFAULT_COLOR


def erase_line():
    """Erase the current line on the console."""
    sys.stdout.write(ERASE_LINE)


def cursor_up():
    """Move the cursor one line up."""
    sys.stdout.write(CURSOR_UP)


def clear():
    """Clear the whole screen."""
    subprocess.run('cmd /c cls')


def centered(text: str):
    """Print the text centered within a width of MAX_WIDTH."""
    padding = (MAX_WIDTH - len(ANSI_ESCAPE.sub("", text))) // 2
    print(" " * padding + text)
