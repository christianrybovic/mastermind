# Copyright (c) 2026 Team Alpha
# All rights reserved.
#
# Licensed under the MIT License. See LICENSE file for details

from game import Game
from turn import Turn
import requests

LOADING_TEXT = "Please wait, almost there..."
URL = "http://localhost:8090/v2/"


class ENDPOINT():
    GAME_CREATE = URL + "game/create"
    GAME_GUESS = URL + "game/guess"
    GAME_CANCEL = URL + "game/cancel"


class Restapi:
    """Static helper methods for interacting with the REST API."""
    @staticmethod
    def game_start(game: Game):
        data = {
            "allowDuplicates": game.allow_duplicates,
            "endless": game.endless
        }
        print(LOADING_TEXT)
        response = requests.post(ENDPOINT.GAME_CREATE, json=data)
        response.raise_for_status()

    @staticmethod
    def game_guess(combination: str) -> Turn:
        data = {
            "combination": combination
        }
        print(LOADING_TEXT)
        response = requests.post(ENDPOINT.GAME_GUESS, json=data)
        response.raise_for_status()
        data = response.json()
        if "duration" in data and "guesses" in data:
            return Turn(data["state"], combination, data["colorAndPosition"], data["colorOnly"],
                        data["duration"], data["guesses"])
        else:
            return Turn(data["state"], combination, data["colorAndPosition"], data["colorOnly"])

    @staticmethod
    def game_cancel():
        print(LOADING_TEXT)
        response = requests.delete(ENDPOINT.GAME_CANCEL)
        response.raise_for_status()
