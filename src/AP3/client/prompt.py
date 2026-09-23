# Copyright (c) 2026 Team Alpha
# All rights reserved.
#
# Licensed under the MIT License. See LICENSE file for details

import console


def prompt(message: str, validate: list = None):
    """
    Prompt the user for input and optionally validate the response.

    Args:
        message: The prompt displayed to the user.
        validate: A collection of valid input values. If provided, the user
            is repeatedly prompted until a valid value is entered.

    Returns:
        The validated user input.
    """
    while True:
        value = input(message)
        console.erase_line()

        if not validate:
            break
        elif callable(validate):
            if validate(value):
                break
        elif value in validate:
            break

        print(console.colorize("This input is invalid. Please try again.", console.COLOR.RED))
        console.cursor_up()
        console.cursor_up()
        console.erase_line()

    console.cursor_up()
    console.erase_line()
    return value
