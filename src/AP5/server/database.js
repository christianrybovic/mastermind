/**
 * Copyright (c) 2026 Team Alpha
 * All rights reserved.
 *
 * Licensed under the MIT License. See LICENSE file for details.
 */

import sqlite3 from 'sqlite3'

const database = new sqlite3.Database("mastermind.db", (err) => {
  if (err) {
    console.error("Failed to connect:", err.message);
  } else {
    console.log("Connected to SQLite database.");
  }
});

database.serialize(() => {
  database.run(`
    CREATE TABLE IF NOT EXISTS stats (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT,
      duration INTEGER,
      guesses INTEGER,
      configAllowDuplicates BOOLEAN,
      configEndless BOOLEAN
    )
  `);
});

/**
 * Write a stat into the database
 *
 * @param {string} username - The username of the player.
 * @param {number} duration - The duration of the game.
 * @param {number} guesses - The guesses needed to win the game.
 * @param {boolean} allowDuplicates - Wheter duplicate colors were allowed in the game.
 * @param {boolean} endless - Wheter there was a turn limit or not.
 */
export function addStat(username, duration, guesses, allowDuplicates, endless) {
    return new Promise((resolve, reject) => {
        database.run(
            "INSERT INTO stats (username, duration, guesses, configAllowDuplicates, configEndless) VALUES (?, ?, ?, ?, ?)",
            [username, duration, guesses, allowDuplicates, endless],
            (error) => {
                if (error) reject(error);
                else resolve();
            }
        );
    });
}

/**
 * Gets all stats from the database
 *
 * @returns {{
 *   id: number,
 *   username: string,
 *   duration: number,
 *   guesses: number,
 *   configAllowDuplicates: boolean,
 *   configEndless: boolean
 * }} List of stats.
 */
export function getStats() {
    return new Promise((resolve, reject) => {
        database.all(
            "SELECT * FROM stats", 
            [],
            (error, items) => {
                if (error) reject(error);
                else resolve(items);
        });
    });
}