# Copyright (c) 2026 Team Alpha
# All rights reserved.
#
# Licensed under the MIT License. See LICENSE file for details

from enum import Enum
from player import Player


class ACTION(Enum):
    LOBBY = "lobby"
    WAIT  = "wait"
    PLAY  = "play"
    END   = "end"


class Room:
    """Represents a room."""
    def __init__(self, id: int, action: str, allow_duplicates: bool, players: dict[str, Player]):
        self.id = id
        self.action = ACTION(action)
        self.allow_duplicates = allow_duplicates
        self.players = players

    def is_lobby(self) -> bool:
        """Return if the room is currently in the lobby."""
        return self.action == ACTION.LOBBY

    def is_playing(self) -> bool:
        """Return if the room is currently playing."""
        return self.action == ACTION.PLAY

    def is_waiting(self) -> bool:
        """Return if there needs to be waiting."""
        return self.action == ACTION.WAIT
