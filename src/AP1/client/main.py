# Copyright (c) 2026 Team Alpha
# All rights reserved.
#
# Licensed under the MIT License. See LICENSE file for details

from validator import Validator
from restapi import Restapi
from prompt import prompt
from game import Game
import ui

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
                Restapi.game_start(game)
                while game.is_running():
                    ui.print_game(game, True)
                    combination = prompt("Make a guess or exit with [x]: ", Validator.is_valid_guess)
                    if combination.lower() == 'x':
                        Restapi.game_cancel()
                        break
                    if not str(combination).isdigit():
                        combination = "".join(ui.MAPPING[c] for c in combination.lower())
                    turn = Restapi.game_guess(combination)
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
