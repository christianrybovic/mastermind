# Copyright (c) 2026 Team Alpha
# All rights reserved.
#
# Licensed under the MIT License. See LICENSE file for details

import re


class Validator:
    """Static helper methods for validation."""
    @staticmethod
    def is_valid_guess(value: str) -> bool:
        if value.lower() == 'x':
            return True
        elif (str(value).isdigit() and
              bool(re.fullmatch(r"[1-6]{4}", str(value)))):
            return True
        elif re.fullmatch(r"[rgbvoy]{4}", str(value).lower()):
            return True
        else:
            return False

    @staticmethod
    def is_valid_username(value: str) -> bool:
        if value == "":
            return True
        elif re.fullmatch(r"[A-Za-z0-9_-]{1,9}", value):
            return True
        else:
            return False

    @staticmethod
    def is_valid_room(value: str) -> bool:
        if value.lower() == 'x':
            return True
        if not str(value).isdigit():
            return False
        number = int(value)
        if 1000 <= number and number <= 9999:
            return True
        else:
            return False
