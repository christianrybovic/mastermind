# Copyright (c) 2026 Team Alpha
# All rights reserved.
#
# Licensed under the MIT License. See LICENSE file for details

from enum import Enum


class STATE(Enum):
    PLAYING = "playing"
    LOST    = "lost"
    WON     = "won"


class Turn:
    """Represents a single turn and its outcome."""
    def __init__(self, state: str, combination: int,
                 correct_position: int, correct_color: int,
                 duration: int = 0, guesses: int = 0):
        self.state = STATE(state)
        self.combination = combination
        self.correct_position = correct_position
        self.correct_color = correct_color
        self.duration = duration
        self.guesses = guesses
