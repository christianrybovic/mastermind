/**
 * Copyright (c) 2026 Team Alpha
 * All rights reserved.
 *
 * Licensed under the MIT License. See LICENSE file for details.
 */

export const STATE_PLAYING = "playing";
export const STATE_LOST = "lost";
export const STATE_WON = "won";
const MAX_GUESSES = 10;

/**
 * Generate a random combination.
 *
 * @param {boolean} allowDuplicates - Whether duplicate digits are allowed or not.
 * @returns {number} A four-digit secret combination.
 */
export function generateCombination(allowDuplicates) {
    let combination;
    do {
        combination = Math.floor(Math.random() * (6666 - 1111 + 1)) + 1111;
    } while (!Game.IsValidCombination(combination) ||
        (!allowDuplicates && new Set(String(combination)).size !== 4));
    return combination;
}

/**
 * Represents a single Mastermind game.
 */
export default class Game {
    /**
     * Create a new game.
     *
     * @param {Configuration} config - The configuration for the current game.
     * @param {Number} secret - Pass the secret to use instead of generating one.
     */
    constructor(config, secret) {
        this.config = config;
        if (secret === undefined) {
            this.secret = generateCombination(config.allowDuplicates);
        } else {
            this.secret = secret;
        }
        this.countGuess = 0;
        this.hasFinished = false;
        this.startTime = new Date();
        this.lastCorrectPosition = 0;
        this.lastCorrectColor = 0;
        console.log("Generated secret: " + this.secret);
    }

    /**
     * Validate a guess against the combination.
     *
     * @param {string} guess - The player's four-digit guess.
     * @returns {{
     *   state: string,
     *   colorAndPosition: number,
     *   colorOnly: number,
     *   duration?: number,
     *   guesses?: number
     * }} The validation result.
     */
    validate(guess) {
        let colorAndPosition = 0;
        let colorOnly = 0;

        let copySecret = [...this.secret.toString()];
        let copyGuess = [...guess];

        for (let i = 0; i < copySecret.length; i++) {
            if (copyGuess[i] === copySecret[i]) {
                colorAndPosition++;
                copySecret[i] = null;
                copyGuess[i] = null;
            }
        }

        for (let i = 0; i < copyGuess.length; i++) {
            if (copyGuess[i] !== null) {
                let index = copySecret.indexOf(copyGuess[i]);

                if (index !== -1) {
                    colorOnly++;
                    copySecret[index] = null;
                }
            }
        }
        
        this.lastCorrectPosition = colorAndPosition;
        this.lastCorrectColor = colorOnly;

        this.countGuess++;
        let state = STATE_PLAYING;
        if (colorAndPosition == 4) {
            state = STATE_WON;
            this.hasFinished = true;
        } else if (this.countGuess == MAX_GUESSES && !this.config.endless) {
            state = STATE_LOST;
            this.hasFinished = true;
        }

        if (this.hasFinished) {
            let duration = new Date() - this.startTime;
            let guesses = this.countGuess;
            return ({state, colorAndPosition, colorOnly, duration, guesses});
        } else{
            return ({state, colorAndPosition, colorOnly});
        }
    }

    /**
     * Check whether a value is a valid Mastermind combination.
     *
     * A valid combination consists of exactly four digits, each in the range 1–6.
     *
     * @param {string|number} value - The value to validate.
     * @returns {boolean} True if the combination is valid.
     */
    static IsValidCombination = (value) => {
        let digits = String(value);
        return digits.length === 4 && [...digits].every(d => "123456".includes(d));
    };
}