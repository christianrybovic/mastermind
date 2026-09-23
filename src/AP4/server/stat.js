/**
 * Copyright (c) 2026 Team Alpha
 * All rights reserved.
 *
 * Licensed under the MIT License. See LICENSE file for details.
 */

const stats = [];

/**
 * Represents a single statistic for a game.
 */
export default class Stat {
    /**
     * Represents the statistics for a completed game.
     *
     * @param {string} id - The user id.
     * @param {number} duration - Time needed to solve the game.
     * @param {number} guesses - Number of guesses needed to win.
     * @param {Configuration} config - The game configuration.
     */
    constructor(id, duration, guesses, config) {
        this.id = id;
        this.duration = duration;
        this.guesses = guesses;
        this.config = config;
    }

    /**
     * Add the statistics of a completed game.
     *
     * Stores the games duration, number of guesses and configuration.
     *
     * @param {string} id - The user id.
     * @param {number} duration - Time needed to solve the game.
     * @param {number} guesses - Number of guesses needed to win.
     * @param {Configuration} config - The game configuration.
     */
    static AddStat = (id, duration, guesses, config) => {
        stats.push(new Stat(id, duration, guesses, config));
    };

    /**
     * Get statistics for a game configuration.
     *
     * Returns duration, guess and game count statistics.
     *
     * @param {Configuration} config - The configuration for the desired stats.
     * @param {string} id - The id of the desired player.
     * @returns {{
     *   longestDuration: number,
     *   shortestDuration: number,
     *   averageDuration: number,
     *   mostGuesses: number,
     *   fewestGuesses: number,
     *   averageGuesses: number,
     *   count: number
     * }} The statistics.
     */
    static GetStats = (config, id) => {
        let filtered = [];
        let count = 0;
        if (typeof id === 'undefined') {
            filtered = stats.filter(item =>
                item.config.allowDuplicates == config.allowDuplicates);
            count = Number((filtered.length / new Set(filtered.map(s => s.id)).size).toFixed(2));
        } else {
            filtered = stats.filter(item =>
                item.config.allowDuplicates == config.allowDuplicates &&
                item.id == id);
            count = filtered.length;
        }
        if (filtered.length === 0) {
            throw new Error("No stats found");
        }
        const longestDuration = filtered.reduce((result, item) => item.duration > result.duration ? item : result).duration;
        const shortestDuration = filtered.reduce((result, item) => item.duration < result.duration ? item : result).duration;
        const averageDuration = Number((filtered.reduce((result, item) => result + item.duration, 0) / filtered.length).toFixed(0));
        const mostGuesses = filtered.reduce((result, item) => item.guesses > result.guesses ? item : result).guesses;
        const fewestGuesses = filtered.reduce((result, item) => item.guesses < result.guesses ? item : result).guesses;
        const averageGuesses = Number((filtered.reduce((result, item) => result + item.guesses, 0) / filtered.length).toFixed(2));
        return ({longestDuration, shortestDuration, averageDuration, mostGuesses, fewestGuesses, averageGuesses, count});
    };
}