# Copyright (c) 2026 Team Alpha
# All rights reserved.
#
# Licensed under the MIT License. See LICENSE file for details

from validator import Validator
from restapi import Restapi
from prompt import prompt
from game import Game
import threading
import argparse
import time
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
    restapi = None
    while True:
        try:
            if not restapi:
                ui.print_welcome()
                username = prompt("Please enter a username: ", Validator.is_valid_username)
                restapi = Restapi(username)
                ui.set_username(username)
            ui.print_menu()
            match prompt("Please select an option: ", ["c","C","h","H","j","J","l","L","p","P","s","S","q","Q","   |   "]):
                case "c" | "C":
                    restapi.room_create()
                    game = Game()
                    game.endless = True
                    while (room := restapi.room_state()).is_lobby():
                        ui.print_room(room, True)
                        match prompt("Please select an option: ", ["d","D","r","R","s","S"]):
                            case "d" | "D":
                                game.allow_duplicates = not game.allow_duplicates
                                restapi.room_config(game.allow_duplicates)
                            case "r" | "R":
                                continue
                            case "s" | "S":
                                restapi.room_config(game.allow_duplicates, True)
                    while room.is_playing():
                        ui.print_game(game, True, False, room)
                        combination = prompt("Make a guess or exit with [x]: ", Validator.is_valid_guess)
                        if combination.lower() == 'x':
                            restapi.game_cancel()
                            break
                        if not str(combination).isdigit():
                            combination = "".join(ui.MAPPING[c] for c in combination.lower())
                        turn = restapi.game_guess(combination, True)
                        game.add_turn(turn)
                        while (room := restapi.room_state()).is_waiting():
                            time.sleep(1.3)
                        game.add_history(room.players)
                    else:
                        ui.print_game_end(game, room)
                        prompt("Press enter to return ")
                case "j" | "J":
                    is_joining = True
                    has_failed = False
                    while is_joining:
                        ui.print_room_join(has_failed)
                        room_id = prompt("Enter room id or exit with [x]: ", Validator.is_valid_room)
                        if room_id.lower() == 'x':
                            break
                        if restapi.room_join(room_id):
                            is_joining = False
                        else:
                            has_failed = True
                    else:
                        while (room := restapi.room_state()).is_lobby():
                            ui.print_room(room)
                            time.sleep(1.3)
                        game = Game()
                        game.endless = True
                        game.allow_duplicates = room.allow_duplicates
                        while room.is_playing():
                            ui.print_game(game, True, False, room)
                            combination = prompt("Make a guess or exit with [x]: ", Validator.is_valid_guess)
                            if combination.lower() == 'x':
                                restapi.game_cancel()
                                break
                            if not str(combination).isdigit():
                                combination = "".join(ui.MAPPING[c] for c in combination.lower())
                            turn = restapi.game_guess(combination, True)
                            game.add_turn(turn)
                            while (room := restapi.room_state()).is_waiting():
                                time.sleep(1.3)
                            game.add_history(room.players)
                        else:
                            ui.print_game_end(game, room)
                            prompt("Press enter to return ")
                case "h" | "H":
                    ui.print_help()
                    prompt("Press enter to return ")
                case "   |   ":
                    ui.print_unused()
                    prompt("Press enter to return ")
                case "l" | "L":
                    allow_duplicates = True
                    show_anonymous = False
                    while True:
                        stat_leaderboard = restapi.stat_leaderboard(allow_duplicates, show_anonymous)
                        ui.print_leaderboard(allow_duplicates, show_anonymous, stat_leaderboard)
                        match prompt("Please select an option or exit with [x]: ", ["a","A","d","D","r","R","x","X"]):
                            case "a" | "A":
                                show_anonymous = not show_anonymous
                            case "d" | "D":
                                allow_duplicates = not allow_duplicates
                            case "r" | "R":
                                continue
                            case "x" | "X":
                                break
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
                case "s" | "S":
                    allow_duplicates = True
                    while True:
                        stat_personal = restapi.stat_personal(allow_duplicates)
                        stat_global = restapi.stat_global(allow_duplicates)
                        veteran = restapi.stat_veteran(allow_duplicates)
                        ui.print_statistics(allow_duplicates, stat_personal, stat_global, veteran)
                        match prompt("Please select an option or exit with [x]: ", ["d","D","r","R","x","X"]):
                            case "d" | "D":
                                allow_duplicates = not allow_duplicates
                            case "r" | "R":
                                continue
                            case "x" | "X":
                                break
                case "q" | "Q":
                    ui.print_bye()
                    break
        except:
            ui.print_error()
            prompt("Press enter to return ")
