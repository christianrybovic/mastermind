# Copyright (c) 2026 Team Alpha
# All rights reserved.
#
# Licensed under the MIT License. See LICENSE file for details

from mastermind_solver import Knuth
from validator import Validator
from restapi import Restapi
from prompt import prompt
from game import Game
import threading
import argparse
import sys
import ui


def thread_worker(session: int, rounds: int):
    try:
        restapi = Restapi()
        for _ in range(rounds):
            game = Game(session)
            solver = Knuth()
            games.append(game)
            restapi.game_start(game)
            while game.is_running():
                guess = solver.get_next_guess()
                turn = restapi.game_guess("".join(map(str, guess)))
                solver.update_possible_codes(guess, turn.correct_position, turn.correct_color)
                game.add_turn(turn)
    except:
        error.set()


parser = argparse.ArgumentParser()
parser.add_argument("rounds", type=int, nargs="?", default=None,
                    help="Number of rounds to play automatically")
parser.add_argument("sessions", type=int, nargs="?", default=1,
                    help="Number of parallel sessions (default 1)")
parser.add_argument("--quiet", action="store_true",
                    help="Suppress turn-by-turn output and display only a plain-text summary")
autoplay = parser.parse_args()

if autoplay.rounds is not None:
    try:
        error = threading.Event()
        threads = []
        games: list[Game] = []
        for i in range(autoplay.sessions):
            thread = threading.Thread(target=thread_worker, args=(i+1, autoplay.rounds))
            thread.start()
            threads.append(thread)
        for t in threads:
            t.join()
        if error.is_set():
            raise Exception()
        ui.print_autoplay(games, autoplay.quiet)
    except:
        if autoplay.quiet:
            print("Something went wrong. Please try again...")
        else:
            ui.print_error()
        sys.exit(1)
    sys.exit(0)
else:
    restapi = Restapi()
    while True:
        ui.print_menu()
        try:
            match prompt("Please select an option: ", ["h","H","p","P","q","Q"]):
                case "h" | "H":
                    ui.print_help()
                    prompt("Press enter to return ")
                case "p" | "P":
                    game = Game()
                    while True:
                        ui.print_configuration(game)
                        match prompt("Please select an option: ", ["d","D","e","E","s","S"]):
                            case "d" | "D":
                                game.allow_duplicates = not game.allow_duplicates
                            case "e" | "E":
                                game.endless = not game.endless
                            case "s" | "S":
                                break
                    restapi.game_start(game)
                    while game.is_running():
                        ui.print_game(game, True)
                        combination = prompt("Make a guess or exit with [x]: ", Validator.is_valid_guess)
                        if combination.lower() == 'x':
                            restapi.game_cancel()
                            break
                        if not str(combination).isdigit():
                            combination = "".join(ui.MAPPING[c] for c in combination.lower())
                        turn = restapi.game_guess(combination)
                        game.add_turn(turn)
                    else:
                        ui.print_game_end(game)
                        prompt("Press enter to return ")
                case "q" | "Q":
                    ui.print_bye()
                    break
        except:
            ui.print_error()
            prompt("Press enter to return ")
