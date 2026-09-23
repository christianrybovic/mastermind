# Copyright (c) 2026 Team Alpha
# All rights reserved.
#
# Licensed under the MIT License. See LICENSE file for details

from console import centered, clear, colorize, COLOR, DIAMOND
from game import Game
from room import Room
from stats import Stat, Stats
from veteran import Veteran
import base64

TITLE = [
    "",
    "   ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗██████╗",
    "   ████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗",
    "   ██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║██║  ██║",
    "   ██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██║  ██║",
    "   ██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██████╔╝",
    "   ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝"]
TITLE_COLORS = [0, 222, 221, 220, 214, 179, 228]
PLAYING_AS = ""
USERNAME = ""
SUBTITLE = "\033[38;5;214m═══ BY TEAM ALPHA ═══\033[0m"
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


def set_username(username: str):
    global PLAYING_AS
    global USERNAME
    USERNAME = "anonymous" if username == "" else username
    PLAYING_AS = f"You are playing as: {USERNAME}"


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
    print(f"   \033[38;5;240m{PLAYING_AS:<58}" + SUBTITLE + NEW_LINE * 2)


def print_welcome():
    """Print the welcome screen of the game."""
    print_header()
    centered("Welcome to our game!")
    centered("")
    centered("")
    centered("To begin, please enter a username. Your username must be between 1 and 9 characters ")
    centered("long and may only contain letters, numbers, hyphens (-) and underscores (_).")
    centered("")
    centered(colorize("If you do not wish to enter a username, simply press Enter to continue as anonymous.", COLOR.GRAY))
    print(NEW_LINE * 2)


def print_menu():
    """Print the main menu of the game."""
    print_header()
    block_size = 37
    centered(block_start(block_size))
    centered("║            " + format_title("Main Menu") + "            ║")
    centered(block_separate(block_size))
    centered("║ Play a solo game                " + command("p") + " ║")
    centered(block_separate(block_size))
    centered("║ Create a room                   " + command("c") + " ║")
    centered("║ Join a room                     " + command("j") + " ║")
    centered(block_separate(block_size))
    centered("║ View statistics                 " + command("s") + " ║")
    centered("║ View leaderboard                " + command("l") + " ║")
    centered(block_separate(block_size))
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


def print_room(room: Room, is_admin=False):
    """Print the room overview."""
    print_header()
    block_size = 41
    centered(block_start(block_size))
    centered("║              " + format_title("Room " + str(room.id)) + "              ║")
    centered(block_separate(block_size))
    centered("║ Player's in this room (max 4):          ║")
    centered("║ " + colorize("›", COLOR.ACCENT) + f" {USERNAME:<37} ║")
    if room.players:
        for counter, player in enumerate(room.players.values(), start=1):
            centered("║ " + colorize("›", COLOR.ACCENT) + f" {player.username:<37} ║")
    else:
        counter = 0
    for _ in range(3-counter):
        centered("║                                         ║")
    centered(block_separate(block_size))
    if is_admin:
        centered("║ Allow duplicate colors?         " +
                 ("YES " if room.allow_duplicates else " NO ") + command("d") + " ║")
        centered(block_separate(block_size))
        centered("║ Refresh the player list             " + command("r") + " ║")
        centered("║ Start the game                      " + command("s") + " ║")
        centered(block_end(block_size))
        print(NEW_LINE*2)
    else:
        centered("║ Allow duplicate colors?             " +
                 ("YES" if room.allow_duplicates else " NO") + " ║")
        centered(block_end(block_size))
        print(NEW_LINE*2)
        print("Please wait for the game to start...")


def print_room_join(has_failed: bool):
    """Print the room join menu."""
    print_header()
    block_size = 47
    centered(block_start(block_size))
    centered("║                " + format_title("Join a room") + "                ║")
    centered(block_separate(block_size))
    centered("║ Enter the four-digit ID to join a room...     ║")
    centered(block_end(block_size))
    if has_failed:
        centered(colorize(block_start(block_size), COLOR.RED))
        centered(colorize("║           Failed to join the room!            ║", COLOR.RED))
        centered(colorize(block_end(block_size), COLOR.RED))
    print(NEW_LINE*2)


def print_autoplay(games: list[Game], quiet: bool):
    """Print all autoplay results."""
    if quiet:
        for number, game in enumerate(games, start=1):
            print(f"Autoplay #{number}: Session = {game.session} | " +
                  f"Guesses = {len(game.get_turns())} | " +
                  f"Duration: {format_duration(game.get_duration())}")
    else:
        print_header()
        for number, game in enumerate(games, start=1):
            centered(f"Autoplay #{number} (Solved by session {game.session})")
            print_game(game, False, True)


def print_game(game: Game, is_running: bool, append: bool = False, room: Room = None):
    """Print the current game state."""
    if not append:
        print_header()
    opponents = len(room.players) if room and room.players else 0
    centered("╔══════════════════════════════════╗" + " "*opponents*14)
    circles = "║    "
    keys = "║   "
    for i in range(1, 7):
        circles += colorize(CIRCLE, COLOR(i)) + "    "
        keys += colorize(str(i) + "|" +
                         list(MAPPING.keys())[i-1].upper(), COLOR(i)) + "  "
    circles += "║" + " ┌───────────┐"*opponents
    keys += " ║"
    if room and room.players:
        for player in room.players.values():
            keys += f" │ {player.username:^9} │"
    centered(circles)
    centered(keys)
    centered("╟─────┬────────────────┬───────────╢" + " ├───────────┤"*opponents)
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
            if room and room.players:
                for opponent in room.players:
                    opponent_turn = game.get_history()[counter-1].get(opponent)
                    line += " │  "
                    line += "● " * opponent_turn.correct_position
                    line += "○ " * opponent_turn.correct_color
                    line += "  " * (4 - opponent_turn.correct_position - opponent_turn.correct_color)
                    line += " │"
            centered(line)
    else:
        counter = 0
    if is_running:
        centered("║" + format_counter(counter + 1, game.endless) +
                 "│                │           ║" + " └───────────┘"*opponents)
        centered("╚═════╧════════════════╧═══════════╝" + " "*opponents*14)
    else:
        if game.has_won() and room is None:
            centered("╟─────┴────────────────┴───────────╢")
            text = "Solved in " + format_duration(game.get_duration())
            centered(f"║ {text:>32} ║")
            centered("╚══════════════════════════════════╝")
        else:
            centered("╚═════╧════════════════╧═══════════╝" + " └───────────┘"*opponents)
    print(NEW_LINE*2)


def print_game_end(game: Game, room: Room = None):
    """Print either a win or loss notification."""
    print_game(game, False, False, room)
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


def print_statistics(allow_duplicates: bool, stat_personal: Stats, stat_global: Stats, veteran: Veteran):
    """Print some statistics."""
    print_header()
    block_size = 58
    centered(block_start(block_size))
    centered("║                      " + format_title("Statistics") + "                      ║")
    centered(block_separate(block_size))
    centered("║                                                          ║")

    player_games = "0" if stat_personal is None else str(stat_personal.count)
    global_games = "0" if stat_global is None else str(stat_global.count)

    player_most_guesses = "-" if stat_personal is None else str(stat_personal.most_guesses)
    player_fewest_guesses = "-" if stat_personal is None else str(stat_personal.fewest_guesses)
    player_average_guesses = "-" if stat_personal is None else str(stat_personal.average_guesses)

    global_most_guesses = "-" if stat_global is None else str(stat_global.most_guesses)
    global_fewest_guesses = "-" if stat_global is None else str(stat_global.fewest_guesses)
    global_average_guesses = "-" if stat_global is None else str(stat_global.average_guesses)

    if stat_personal is not None and stat_global is not None:
        if stat_personal.most_guesses < stat_global.most_guesses:
            player_most_guesses += " " + DIAMOND
        else:
            global_most_guesses += " " + DIAMOND
        if stat_personal.fewest_guesses <= stat_global.fewest_guesses:
            player_fewest_guesses += " " + DIAMOND
        else:
            global_fewest_guesses += " " + DIAMOND
        if stat_personal.average_guesses <= stat_global.average_guesses:
            player_average_guesses += " " + DIAMOND
        else:
            global_average_guesses += " " + DIAMOND

    player_longest_duration = "-" if stat_personal is None else format_duration(stat_personal.longest_duration)
    player_average_duration = "-" if stat_personal is None else format_duration(stat_personal.average_duration)
    player_shortest_duration = "-" if stat_personal is None else format_duration(stat_personal.shortest_duration)

    global_longest_duration = "-" if stat_global is None else format_duration(stat_global.longest_duration)
    global_average_duration = "-" if stat_global is None else format_duration(stat_global.average_duration)
    global_shortest_duration = "-" if stat_global is None else format_duration(stat_global.shortest_duration)

    if stat_personal is not None and stat_global is not None:
        if stat_personal.longest_duration < stat_global.longest_duration:
            player_longest_duration += " " + DIAMOND
        else:
            global_longest_duration += " " + DIAMOND
        if stat_personal.shortest_duration <= stat_global.shortest_duration:
            player_shortest_duration += " " + DIAMOND
        else:
            global_shortest_duration += " " + DIAMOND
        if stat_personal.average_duration <= stat_global.average_duration:
            player_average_duration += " " + DIAMOND
        else:
            global_average_duration += " " + DIAMOND

    centered(f"║    Your guesses: {player_fewest_guesses:>11} {player_average_guesses:>11} {player_most_guesses:>11}     ║")
    centered("║                  " + colorize(f"{'FEWEST':>11} {'AVERAGE':>11} {'MOST':>11}", COLOR.GRAY) + "     ║")
    centered(f"║  Global guesses: {global_fewest_guesses:>11} {global_average_guesses:>11} {global_most_guesses:>11}     ║")

    centered("║                                                          ║")
    centered(block_separate(block_size))
    centered("║                                                          ║")

    centered(f"║   Your duration: {player_shortest_duration:>11} {player_average_duration:>11} {player_longest_duration:>11}     ║")
    centered("║                  " + colorize(f"{'FASTEST':>11} {'AVERAGE':>11} {'SLOWEST':>11}", COLOR.GRAY) + "     ║")
    centered(f"║ Global duration: {global_shortest_duration:>11} {global_average_duration:>11} {global_longest_duration:>11}     ║")

    centered("║                                                          ║")
    centered(block_separate(block_size))
    centered(f"║                    Your total games played: {player_games:>8}     ║")
    centered(f"║            Global average games per player: {global_games:>8}     ║")

    if veteran is None:
        centered("║                 (Veteran is not available):        0     ║")
    else:
        centered(f"║     {veteran.username:>16} played the most games: {veteran.count:>8}     ║")

    centered(block_separate(block_size))
    centered("║ Statistics for games with duplicate colors?      " +
             ("YES " if allow_duplicates else " NO ") + command("d") + " ║")
    centered("║ Refresh the statistics                               " + command("r") + " ║")
    centered(block_end(block_size))
    print(NEW_LINE*2)


def print_leaderboard(allow_duplicates: bool, show_anonymous: bool, items: list[Stat]):
    """Print the leaderboard."""
    print_header()
    block_size = 55
    centered(block_start(block_size))
    centered("║                    " + format_title("Leaderboard") + "                    ║")
    centered("╟─────┬────────────────────────┬───────────┬────────────╢")
    centered("║  #  │         Player         │  Guesses  │  Duration  ║")

    if items is None:
        centered("╟─────┴────────────────────────┴───────────┴────────────╢")
        centered("║                                                       ║")
        centered("║                                                       ║")
        centered("║                                                       ║")
        centered("║                                                       ║")
        centered("║                 No data available...                  ║")
        centered("║                                                       ║")
        centered("║                                                       ║")
        centered("║                                                       ║")
        centered("║                                                       ║")
        centered(block_separate(block_size))
    else:
        centered("╟─────┼────────────────────────┼───────────┼────────────╢")
        for counter, item in enumerate(items, start=1):
            if counter < 4:
                centered(f"║ {DIAMOND} {counter} │ {item.username:<22} │ {item.guesses:^9} │ {format_duration(item.duration):>10} ║")
            else:
                centered(f"║   {counter} │ {item.username:<22} │ {item.guesses:^9} │ {format_duration(item.duration):>10} ║")
        for _ in range(9-counter):
            centered("║     │                        │           │            ║")
        centered("╟─────┴────────────────────────┴───────────┴────────────╢")

    centered("║ Leaderboard for games with duplicate colors?  " +
             ("YES " if allow_duplicates else " NO ") + command("d") + " ║")
    centered("║ Show results from anonymous players?          " +
             ("YES " if show_anonymous else " NO ") + command("a") + " ║")
    centered("║ Refresh the leaderboard                           " + command("r") + " ║")
    centered(block_end(block_size))
    print(NEW_LINE*2)


def print_unused():
    """The purpose of this function is unknown."""
    clear()
    print(base64.b64decode("""CgoK4pmgIBtbMzg7NTsyMTRt4pmmG1swbSDimaUg4pmgIOKZpSAbWzM4OzU7Mj
    E0beKZphtbMG0g4pmgIOKZpSDimaAgG1szODs1OzIxNG3imaYbWzBtIOKZpSDimaAg4pmlIBtbMzg7NTsyMTRt4p
    mmG1swbSDimaAg4pmlIOKZoCAbWzM4OzU7MjE0beKZphtbMG0g4pmlIOKZoCDimaUgG1szODs1OzIxNG3imaYbWz
    BtIOKZoCDimaUg4pmgIBtbMzg7NTsyMTRt4pmmG1swbSDimaUg4pmgIOKZpSAbWzM4OzU7MjE0beKZphtbMG0g4p
    mgIOKZpSDimaAgG1szODs1OzIxNG3imaYbWzBtIOKZpSDimaAg4pmlIBtbMzg7NTsyMTRt4pmmG1swbSDimaAg4p
    mlIOKZoCAbWzM4OzU7MjE0beKZphtbMG0g4pmlIOKZoCDimaUgG1szODs1OzIxNG3imaYbWzBtIOKZoAoKChtbMz
    FtWW91IGtub3cgdGhpcyBpcyBub3QgYSB2YWxpZCBpbnB1dCBmb3IgbmF2aWdhdGlvbi4uLiBCdXQgeW91IGZvdW
    5kIG91ciBFQVNURVIgRUdHISEhCgobWzM0bVdoZXRoZXIgeW91IGdvdCBoZXJlIGJ5IGFjY2lkZW50LCBieSBsdW
    NrLCBvciAtIGxldCdzIGJlIGhvbmVzdCAtIGJ5IHJlYWRpbmcgdGhlIGNvZGUuLi4KChtbMzg7NTsyMDhtV2VsbC
    wgY29uZ3JhdHVsYXRpb25zISBZb3UgZm91bmQgdGhlIHRoaW5nIHdlIGhvcGVkIG5vYm9keSB3b3VsZCBmaW5kLg
    oKG1szM21Nb3N0IHBsYXllcnMgd2lsbCBuZXZlciBmaW5kIHRoaXMuIFNvbWUgd2lsbCB3b25kZXIgaWYgdGhpcy
    BldmVuIGV4aXN0cy4KChtbMzJtWW91ciByZXdhcmQ/IE5vIGJvbnVzIHBvaW50cy4gTm8gaGlkZGVuIGFjaGlldm
    VtZW50LiBObyBsZWdlbmRhcnkgc3dvcmQuIEp1c3QgdGhpcyBtZXNzYWdlLgoKG1szNW1Ob3cgY2xvc2UgdGhlIH
    NvdXJjZSBjb2RlLCBzdG9wIGxvb2tpbmcgZm9yIHN1c3BpY2lvdXMgZnVuY3Rpb25zLCBhbmQgZ28gcGxheSBzb2
    1lIGdhbWVzIQoKChtbMG3imaAgG1szODs1OzIxNG3imaYbWzBtIOKZpSDimaAg4pmlIBtbMzg7NTsyMTRt4pmmG1
    swbSDimaAg4pmlIOKZoCAbWzM4OzU7MjE0beKZphtbMG0g4pmlIOKZoCDimaUgG1szODs1OzIxNG3imaYbWzBtIO
    KZoCDimaUg4pmgIBtbMzg7NTsyMTRt4pmmG1swbSDimaUg4pmgIOKZpSAbWzM4OzU7MjE0beKZphtbMG0g4pmgIO
    KZpSDimaAgG1szODs1OzIxNG3imaYbWzBtIOKZpSDimaAg4pmlIBtbMzg7NTsyMTRt4pmmG1swbSDimaAg4pmlIO
    KZoCAbWzM4OzU7MjE0beKZphtbMG0g4pmlIOKZoCDimaUgG1szODs1OzIxNG3imaYbWzBtIOKZoCDimaUg4pmgIB
    tbMzg7NTsyMTRt4pmmG1swbSDimaUg4pmgIOKZpSAbWzM4OzU7MjE0beKZphtbMG0g4pmgCgoK""").decode())


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
