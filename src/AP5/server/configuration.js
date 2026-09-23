/**
 * Copyright (c) 2026 Team Alpha
 * All rights reserved.
 *
 * Licensed under the MIT License. See LICENSE file for details.
 */

/**
 * Represents the configuration of a game.
 */
export default class Configuration {
    /**
     * Create a new configuration.
     *
     * @param {boolean} allowDuplicates - Whether the combination may contain duplicate digits.
     * @param {boolean} endless - Whether the game has no guess limit.
     */
    constructor(allowDuplicates, endless = true) {
        this.allowDuplicates = Configuration.ParseBoolean(allowDuplicates);
        this.endless = Configuration.ParseBoolean(endless);
    }

    /**
     * Parse a string as boolean.
     *
     * @param {string} value - The value to parse.
     * @returns {boolean} The sanitized boolean.
     */
    static ParseBoolean = (value) => {
        if (value === true || String(value).toLowerCase() === 'true' || value == 1) return true;
        if (value === false || String(value).toLowerCase() === 'false' || value == 0) return false;
        throw new Error(`Invalid boolean value: ${value}`);
    };
}