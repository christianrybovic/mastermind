# Copyright (c) 2026 Team Alpha
# All rights reserved.
#
# Licensed under the MIT License. See LICENSE file for details

from turn import Turn, STATE
from player import Player


class Game:
    """Represents a single game instance."""
    def __init__(self, session: int = 1):
        self.session: int = session
        self.allow_duplicates: bool = True
        self.endless: bool = False
        self.__duration = 0
        self.__is_running: bool = True
        self.__has_won: bool = False
        self.__turns: list[Turn] = []
        self.__opponent_history: list[dict[str, Player]] = []

    def is_running(self) -> bool:
        """Return whether the game is still in progress."""
        return self.__is_running

    def has_won(self) -> bool:
        """Return whether the game has been won."""
        return self.__has_won

    def add_turn(self, turn: Turn):
        """
        Add a turn to the game and update the game state.

        Args:
            turn: The turn to add.
        """
        self.__turns.append(turn)
        if turn.state != STATE.PLAYING:
            self.__is_running = False
            if len(self.__turns) != turn.guesses:
                raise ValueError("Manipulation detected")
            self.__duration = turn.duration
            if turn.state == STATE.WON:
                self.__has_won = True

    def add_history(self, item: dict[str, Player]):
        """Add history data for the opponents."""
        self.__opponent_history.append(item)

    def get_history(self) -> list[dict[str, Player]]:
        """Get the history data for the opponents."""
        return self.__opponent_history.copy()

    def get_turns(self) -> list[Turn]:
        """Return the list of turns played in the game."""
        return self.__turns.copy()

    def get_duration(self) -> int:
        """Return the time in ms for the game to win."""
        return self.__duration
