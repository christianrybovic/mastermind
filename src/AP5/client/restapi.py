# Copyright (c) 2026 Team Alpha
# All rights reserved.
#
# Licensed under the MIT License. See LICENSE file for details

from game import Game
from turn import Turn
from veteran import Veteran
from stats import Stat, Stats
import requests

LOADING_TEXT = "Please wait, almost there..."
URL = "http://localhost:8090/v5/"
DEFAULT_USERNAME = "anonymous"


class ENDPOINT():
    USER_REGISTER = URL + "user/register"
    GAME_CREATE = URL + "game/create"
    GAME_GUESS = URL + "game/guess"
    GAME_CANCEL = URL + "game/cancel"
    STAT_GLOBAL = URL + "stat/global"
    STAT_PERSONAL = URL + "stat/personal"
    STAT_VETERAN = URL + "stat/veteran"
    STAT_LEADERBOARD = URL + "stat/leaderboard"


class Restapi:
    """Client for making REST API calls with session support."""
    def __init__(self, username=DEFAULT_USERNAME):
        self.username = username.strip() if username and username.strip() else DEFAULT_USERNAME
        self.session = requests.Session()
        data = {
            "username": self.username
        }
        print(LOADING_TEXT)
        response = self.session.post(ENDPOINT.USER_REGISTER, json=data)
        response.raise_for_status()

    def game_start(self, game: Game):
        data = {
            "allowDuplicates": game.allow_duplicates,
            "endless": game.endless
        }
        print(LOADING_TEXT)
        response = self.session.post(ENDPOINT.GAME_CREATE, json=data)
        response.raise_for_status()

    def game_guess(self, combination: str) -> Turn:
        data = {
            "combination": combination
        }
        print(LOADING_TEXT)
        response = self.session.post(ENDPOINT.GAME_GUESS, json=data)
        response.raise_for_status()
        data = response.json()
        if "duration" in data and "guesses" in data:
            return Turn(data["state"], combination, data["colorAndPosition"], data["colorOnly"],
                        data["duration"], data["guesses"])
        else:
            return Turn(data["state"], combination, data["colorAndPosition"], data["colorOnly"])

    def game_cancel(self):
        print(LOADING_TEXT)
        response = self.session.delete(ENDPOINT.GAME_CANCEL)
        response.raise_for_status()

    def stat_global(self, get_allow_duplicates: bool) -> Stats | None:
        print(LOADING_TEXT)
        query = f"?allowDuplicates={get_allow_duplicates}"
        response = self.session.get(ENDPOINT.STAT_GLOBAL + query)
        if response.status_code == 503:
            return None
        response.raise_for_status()
        data = response.json()
        return Stats(data["longestDuration"], data["shortestDuration"],
                     data["averageDuration"], data["mostGuesses"],
                     data["fewestGuesses"], data["averageGuesses"],
                     data["count"])

    def stat_personal(self, get_allow_duplicates: bool) -> Stats | None:
        print(LOADING_TEXT)
        query = f"?allowDuplicates={get_allow_duplicates}"
        response = self.session.get(ENDPOINT.STAT_PERSONAL + query)
        if response.status_code == 503:
            return None
        response.raise_for_status()
        data = response.json()
        return Stats(data["longestDuration"], data["shortestDuration"],
                     data["averageDuration"], data["mostGuesses"],
                     data["fewestGuesses"], data["averageGuesses"],
                     data["count"])

    def stat_veteran(self, get_allow_duplicates: bool) -> Veteran | None:
        print(LOADING_TEXT)
        query = f"?allowDuplicates={get_allow_duplicates}"
        response = self.session.get(ENDPOINT.STAT_VETERAN + query)
        if response.status_code == 503:
            return None
        response.raise_for_status()
        data = response.json()
        return Veteran(data["username"], data["maxCount"])

    def stat_leaderboard(self, get_allow_duplicates: bool, get_show_anonymous: bool) -> list[Stat] | None:
        print(LOADING_TEXT)
        query = f"?allowDuplicates={get_allow_duplicates}&showAnonymous={get_show_anonymous}"
        response = self.session.get(ENDPOINT.STAT_LEADERBOARD + query)
        if response.status_code == 503:
            return None
        response.raise_for_status()
        data = response.json()
        items: list[Stat] = []
        for item in data:
            items.append(Stat(item["id"], item["guesses"], item["duration"]))
        return items
