# Copyright (c) 2026 Team Alpha
# All rights reserved.
#
# Licensed under the MIT License. See LICENSE file for details

class Player:
    """Represents a player in multiplayer."""
    def __init__(self, username: str, correct_position: int, correct_color: int):
        self.username = username
        self.correct_position = correct_position
        self.correct_color = correct_color
