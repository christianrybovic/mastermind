/**
 * Copyright (c) 2026 Team Alpha
 * All rights reserved.
 *
 * Licensed under the MIT License. See LICENSE file for details.
 */

import Game, {STATE_WON, generateCombination} from './game.js'
import Configuration from './configuration.js'

const ACTION_LOBBY = "lobby";
const ACTION_WAIT = "wait";
const ACTION_PLAY = "play";
const ACTION_END = "end";
const MAX_PLAYERS = 4;

const rooms = new Map();

/**
 * Generate a random unique room id.
 *
 * @returns {number} A four-digit room id.
 */
function generateRoomId() {
    let id;
    do {
        id = Math.floor(1000 + Math.random() * 9000);
    } while (rooms.has(id));
    return id;
}

/**
 * Represents a room for multiplayer.
 */
export default class Room {
    /**
     * Create a new room.
     *
     * @param {Express.Request.session} session - The session of the user.
     */
    constructor(session) {
        this.roomId = generateRoomId();
        this.adminId = session.id;
        this.players = new Map();
        this.games = new Map();
        this.players.set(session.id, session.username);
        this.allowDuplicates = true;
        this.action = ACTION_LOBBY;
        this.counter = 0;
        this.hasAnyWon = false;
        rooms.set(this.roomId, this);
        console.log("Created room " + this.roomId + " with admin " + this.adminId);
    }

    /**
     * Joins an existing room.
     *
     * @param {Express.Request.session} session - The session of the user.
     */ 
    join(session) {
        if (this.players.has(session.id) ||
            this.action != ACTION_LOBBY ||
            this.players.size >= MAX_PLAYERS) {
            throw new Error(`Failed to join`); 
        }
        this.players.set(session.id, session.username);
    }

    /**
     * Notify the room when the user made a turn.
     *
     * @param {boolean} won - Pass if the user has found the correct combination.
     */ 
    notify(won) {
        if (won) {
            this.hasAnyWon = true;
        }
        this.counter--;
        if (this.counter == 0) {
            this.counter = this.players.size;
            if (this.hasAnyWon) {
                this.action = ACTION_END;
            } else {
                this.action = ACTION_PLAY
            }
        } else {
            this.action = ACTION_WAIT;
        }
    }

    /**
     * Leave an room and skip the turn of the user.
     *
     * @param {Express.Request.session} session - The session of the user.
     */ 
    leave(session) {
        this.players.delete(session.id);
        this.notify(false);
    }

    /**
     * Updates the configuration settings of the current game room.
     *
     * @param {boolean} allowDuplicates - Whether the combination may contain duplicate digits.
     * @param {boolean} start - Start the game.
     */ 
    setConfig(session, allowDuplicates, start) {
        if (this.adminId != session.id) {
            throw new Error(`User is not admin`); 
        }
        this.allowDuplicates = allowDuplicates;
        if (start) {
            const config = new Configuration(this.allowDuplicates);
            const secret = generateCombination(config.allowDuplicates)
            this.players.forEach((value, key) => {
                this.games.set(key, new Game(config, secret));
            });
            this.counter = this.players.size;
            this.action = ACTION_PLAY;
        }
    }

    /**
     * Returns the current state of the game room from the perspective of the specified session.
     * 
     * The returned state includes the room configuration and a list of all other players currently
     * in the room. For each player, it includes their username and their latest game results.
     *
     * @param {Express.Request.session} session - The session of the user.
     * @returns {{
     *   roomId: number,
     *   action: string,
     *   allowDuplicates: boolean,
     *   players?: {
     *     username: string,
     *     correctPosition: number,
     *     correctColor: number
     *   }
     * }} The current room state.
     */ 
    getState(session) {
        const roomId = this.roomId;
        const action = this.action;
        const allowDuplicates = this.allowDuplicates;
        let players = [];
        this.players.forEach((value, key) => {
            if (key != session.id) {
                const userId = key;
                const userName = value;
                let correctPosition = 0;
                let correctColor = 0;
                if (this.games.has(key)) {
                    const game = this.games.get(key);
                    correctPosition = game.lastCorrectPosition;
                    correctColor = game.lastCorrectColor;
                }
                players.push({userId, userName, correctPosition, correctColor});
            }
            });
        return ({roomId, action, allowDuplicates, players});
    }

    /**
     * Get the game object of the user. Each user has it's own object.
     *
     * @param {Express.Request.session} session - The session of the user.
     * @returns {Game} The game object.
     */ 
    getGame(session) {
        return this.games.get(session.id);
    }

    /**
     * Get an room by id.
     *
     * @param {number} id - The room id.
     * @returns {Room} The room object.
     */ 
    static GetById = (id) => {
        id = Number(id);
        return rooms.get(id);
    };

    /**
     * Check whether a value is a valid room id.
     *
     * A valid combination consists of exactly four digits, each in the range 1–6.
     *
     * @param {string|number} value - The value to validate.
     * @returns {boolean} True if the room id is valid.
     */
    static IsValidRoomId = (value) => {
        let roomId = Number(value);
        return 1000 <= roomId && roomId <= 9999;
    };
}