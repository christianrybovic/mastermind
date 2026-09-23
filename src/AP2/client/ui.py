# Copyright (c) 2026 Team Alpha
# All rights reserved.
#
# Licensed under the MIT License. See LICENSE file for details

from console import centered, clear, colorize, COLOR
from game import Game

TITLE = [
    "",
    "   ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗██████╗",
    "   ████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗",
    "   ██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║██║  ██║",
    "   ██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██║  ██║",
    "   ██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██████╔╝",
    "   ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝"]
TITLE_COLORS = [0, 222, 221, 220, 214, 179, 228]
SUBTITLE = " " * 61 + "\033[38;5;214m═══ BY TEAM ALPHA ═══\033[0m"
NEW_LINE = "\r\n"
CIRCLE = '\u2688'
MAPPING = {
    'r': '1',
    'o': '2',
    'y': '3',
    'g': '4',
    'b': '5',
    'v': '6'
}


def block_start(size: int) -> str:
    """Prints the upper border."""
    return "╔" + "═" * size + "╗"


def block_separate(size: int) -> str:
    """Prints a line to separate a block."""
    return "╟" + "─" * size + "╢"


def block_end(size: int) -> str:
    """Prints the bottom closing border."""
    return "╚" + "═" * size + "╝"


def command(key: str) -> str:
    """Prints a command key within square brackets and colorized."""
    return colorize(f"[{key}]", COLOR.ACCENT)


def format_counter(counter: int, is_endless: bool) -> str:
    """Formats the counter based on the number. Print a smiley if bigger than 1000."""
    if not is_endless and counter >= 8:
        return colorize(f" {counter:>2}  ", COLOR.RED)
    else:
        if counter > 999:
            return colorize(" :D  ", COLOR.ACCENT)
        elif counter > 99:
            return f" {counter:>3} "
        else:
            return f" {counter:>2}  "


def format_title(title: str) -> str:
    """Formats the title in uppercase."""
    return colorize("- ", COLOR.ACCENT) + title.upper() + colorize(" -", COLOR.ACCENT)


def format_duration(duration: int) -> str:
    """Format the time to a user friendly output."""
    if duration < 1000:
        return f"{duration}ms"
    totalSeconds = duration / 1000
    if totalSeconds < 60:
        return f"{totalSeconds:.1f}s"
    minutes = int(totalSeconds // 60)
    seconds = int(totalSeconds % 60)
    return f"{minutes}min {seconds}s"


def print_header():
    """Clears the console and prints the header."""
    clear()
    for char, line in zip(TITLE_COLORS, TITLE):
        print(f"\033[38;5;{char}m{line}\033[0m")
    print(SUBTITLE + NEW_LINE * 2)


def print_menu():
    """Print the main menu of the game."""
    print_header()
    block_size = 37
    centered(block_start(block_size))
    centered("║            " + format_title("Main Menu") + "            ║")
    centered(block_separate(block_size))
    centered("║ Play a new game                 " + command("p") + " ║")
    centered("║ Show how to play                " + command("h") + " ║")
    centered("║ Quit the game                   " + command("q") + " ║")
    centered(block_end(block_size))
    print(NEW_LINE * 2)


def print_help():
    """Print the help for the Mastermind game."""
    print_header()
    block_size = 69
    centered(block_start(block_size))
    centered("║                           " + format_title("How to play") + "                           ║")
    centered(block_separate(block_size))
    centered("║ Mastermind is a code-breaking game where you try to guess a hidden  ║")
    centered("║ sequence of colors.                                                 ║")
    centered(block_separate(block_size))
    centered("║ Goal:                                                               ║")
    centered("║ Find the secret code made of 4 colored pegs chosen from " +
             colorize("Red", COLOR.RED) + ", " + colorize("Blue", COLOR.BLUE) + ",  ║")
    centered("║ " + colorize("Orange", COLOR.ORANGE) + ", " +
             colorize("Yellow", COLOR.YELLOW) + ", " +
             colorize("Green", COLOR.GREEN) + " and " +
             colorize("Violet", COLOR.VIOLET) + ".                                   ║")
    centered(block_separate(block_size))
    centered("║ How it works:                                                       ║")
    centered("║ The server chooses a secret sequence. On each turn, you enter a     ║")
    centered("║ combination of 4 colors. After each guess, you receive clues        ║")
    centered("║ indicating whether a color is in the correct position, whether the  ║")
    centered("║ color is correct but in the wrong position, or whether it is not    ║")
    centered("║ part of the secret sequence at all.                                 ║")
    centered(block_separate(block_size))
    centered("║      ● = Correct color and position     ○ = Correct color only      ║")
    centered(block_end(block_size))
    print(NEW_LINE*2)


def print_configuration(game: Game):
    """Print the configuration options for a game."""
    print_header()
    block_size = 47
    centered(block_start(block_size))
    centered("║               " + format_title("Configuration") + "               ║")
    centered(block_separate(block_size))
    centered("║ Allow duplicate colors?               " +
             ("YES " if game.allow_duplicates else " NO ") + command("d") + " ║")
    centered("║ Endless mode?                         " +
             ("YES " if game.endless else " NO ") + command("e") + " ║")
    centered(block_separate(block_size))
    centered("║ Start the game                            " + command("s") + " ║")
    centered(block_end(block_size))
    print(NEW_LINE*2)


def print_autoplay(games: list[Game], quiet: bool):
    """Print all autoplay results."""
    if quiet:
        for number, game in enumerate(games, start=1):
            print(f"Autoplay #{number}: Guesses = {len(game.get_turns())} | " +
                  f"Duration: {format_duration(game.get_duration())}")
    else:
        print_header()
        for number, game in enumerate(games, start=1):
            centered(f"Autoplay #{number}")
            print_game(game, False, True)


def print_game(game: Game, is_running: bool, append: bool = False):
    """Print the current game state."""
    if not append:
        print_header()
    centered("╔══════════════════════════════════╗")
    circles = "║    "
    keys = "║   "
    for i in range(1, 7):
        circles += colorize(CIRCLE, COLOR(i)) + "    "
        keys += colorize(str(i) + "|" +
                         list(MAPPING.keys())[i-1].upper(), COLOR(i)) + "  "
    circles += "║"
    keys += " ║"
    centered(circles)
    centered(keys)
    centered("╟─────┬────────────────┬───────────╢")
    if game.get_turns():
        for counter, turn in enumerate(game.get_turns(), start=1):
            line = "║" + format_counter(counter, game.endless) + "│   "
            for digit in str(turn.combination):
                line += colorize(CIRCLE, COLOR(int(digit))) + "  "
            line += " │  "
            line += "● " * turn.correct_position
            line += "○ " * turn.correct_color
            line += "  " * (4 - turn.correct_position - turn.correct_color)
            line += " ║"
            centered(line)
    else:
        counter = 0
    if is_running:
        centered("║" + format_counter(counter + 1, game.endless) +
                 "│                │           ║")
        centered("╚═════╧════════════════╧═══════════╝")
    else:
        if game.has_won():
            centered("╟─────┴────────────────┴───────────╢")
            text = "Solved in " + format_duration(game.get_duration())
            centered(f"║ {text:>32} ║")
            centered("╚══════════════════════════════════╝")
        else:
            centered("╚═════╧════════════════╧═══════════╝")
    print(NEW_LINE*2)


def print_game_end(game: Game):
    """Print either a win or loss notification."""
    print_game(game, False)
    if game.has_won():
        centered(colorize(" *   *      *      *          *        *       *         ", COLOR.YELLOW))
        centered(colorize("   \|/          *                    *           \|/     ", COLOR.ACCENT))
        centered(colorize(" -- ◊ --        Congratulations, you won!      -- ◊ --   ", COLOR.YELLOW))
        centered(colorize("   /|\          *        *              *        /|\     ", COLOR.ACCENT))
        centered(colorize("    *      *      *              *      *       *      * ", COLOR.YELLOW))
    else:
        centered(colorize("  .   X    '     .     |     '     .    |     .    X      ", COLOR.RED))
        centered(colorize("      '        |      .      |      '       X          '  ", COLOR.RED))
        centered(colorize("     .     |     '      Game over!                   |    ", COLOR.RED))
        centered(colorize("   |      .      '      |      .      |   .     |         ", COLOR.RED))
        centered(colorize(" '     .     X     '     .     |         '        |     X ", COLOR.RED))
    print(NEW_LINE*2)


def print_bye():
    """Print a message when the game is quit."""
    print_header()
    print(NEW_LINE * 3)
    centered("Thanks for playing! See you next time...")
    print(NEW_LINE * 7)


def print_error():
    """Print an error message."""
    print_header()
    block_size = 62
    centered(colorize(block_start(block_size), COLOR.RED))
    centered(
        colorize("║             WELL... THAT WASN'T PART OF THE GAME             ║",
                 COLOR.RED))
    centered(colorize(block_separate(block_size), COLOR.RED))
    centered(
        colorize("║ Something went wrong. We're really sorry! Please try again.  ║",
                 COLOR.RED))
    centered(colorize(block_end(block_size), COLOR.RED))
    print(NEW_LINE * 2)
