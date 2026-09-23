# Copyright (c) 2026 Team Alpha
# All rights reserved.
#
# Licensed under the MIT License. See LICENSE file for details

class Stat:
    """Represents a single stat."""
    def __init__(self, username: str, guesses: int, duration: int):
        self.username = username
        self.guesses = guesses
        self.duration = duration


class Stats:
    """Represents personal or global stats."""
    def __init__(self, longest_duration: int, shortest_duration: int,
                 average_duration: float, most_guesses: int,
                 fewest_guesses: int, average_guesses: float,
                 count: int):
        self.longest_duration = longest_duration
        self.shortest_duration = shortest_duration
        self.average_duration = average_duration
        self.most_guesses = most_guesses
        self.fewest_guesses = fewest_guesses
        self.average_guesses = average_guesses
        self.count = count
