/**
 * Copyright (c) 2026 Team Alpha
 * All rights reserved.
 *
 * Licensed under the MIT License. See LICENSE file for details.
 */

import Configuration from './configuration.js'
import { addStat, getStats } from './database.js'

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
        addStat(id, duration, guesses, config.allowDuplicates, config.endless);
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
    static GetStats = async (config, id) => {
        let data = await getStats();
        let stats = data.map(item => new Stat(item.username, item.duration, item.guesses, 
            new Configuration(item.configAllowDuplicates, item.configEndless)));
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

    /**
     * Get information about the user who played most games (the veteran).
     *
     * Returns the user with the most played games.
     *
     * @param {Configuration} config - The configuration.
     * @returns {{
     *   username: string,
     *   maxCount: int
     * }} The information.
     */
    static GetVeteran = async (config) => {
        let data = await getStats();
        let stats = data.map(item => new Stat(item.username, item.duration, item.guesses, 
            new Configuration(item.configAllowDuplicates, item.configEndless)));
        const counts = new Map();
        const filtered = stats.filter(item =>
                item.config.allowDuplicates == config.allowDuplicates);
        if (filtered.length === 0) {
            throw new Error("No stats found");
        }
        let username = null;
        let maxCount = 0;
        for (const item of filtered) {
            const count = (counts.get(item.id) || 0) + 1;
            counts.set(item.id, count);
            if (count > maxCount) {
                username = item.id;
                maxCount = count;
            }
        }
        return ({username, maxCount});
    };

    /**
     * Get the leaderboard for a configuration.
     *
     * Returns the leaderboard.
     *
     * @param {Configuration} config - The configuration for the leaderboard.
     * @param {boolean} showAnonymous - Show scores from anonymous players.
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
    static GetLeaderboard = async (config, showAnonymous) => {
        let data = await getStats();
        let stats = data.map(item => new Stat(item.username, item.duration, item.guesses, 
            new Configuration(item.configAllowDuplicates, item.configEndless)));
        let filtered = [];
        if (showAnonymous) {
            filtered = stats.filter(item =>
                item.config.allowDuplicates == config.allowDuplicates).sort((a, b) =>
                a.guesses - b.guesses ||
                a.duration - b.duration).slice(0, 9);
        } else {
            filtered = stats.filter(item =>
                item.config.allowDuplicates == config.allowDuplicates &&
                item.id != "anonymous").sort((a, b) =>
                a.guesses - b.guesses ||
                a.duration - b.duration).slice(0, 9);
        }
        if (filtered.length === 0) {
            throw new Error("No stats found");
        }
        return (filtered.map(({ id, guesses, duration }) =>
            ({id, guesses, duration})));
    };
}