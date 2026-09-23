/**
 * Copyright (c) 2026 Team Alpha
 * All rights reserved.
 *
 * Licensed under the MIT License. See LICENSE file for details.
 */

import Game from './game.js'
import Room from './room.js'

const INVALID_DATA_TEXT = 'Invalid data';

/**
 * Static helper methods for request validation.
 */
export default class Validator {
    static GameCreate = (req, res, next) => {
        if (!req.body ||
            !Object.prototype.hasOwnProperty.call(req.body, 'allowDuplicates') ||
            !Object.prototype.hasOwnProperty.call(req.body, 'endless') ||
            typeof req.body.allowDuplicates !== 'boolean' ||
            typeof req.body.endless !== 'boolean' ||
            !req.session || 
            !req.session.username) {
            return res.status(400).send(INVALID_DATA_TEXT);
        }
        next();
    };

    static GameGuess = (req, res, next) => {
        if (!req.body ||
            (!req.session.gameId && !req.session.roomId) ||
            !Object.prototype.hasOwnProperty.call(req.body, 'combination') ||
            Number.isNaN(req.body.combination) ||
            !Game.IsValidCombination(req.body.combination) ||
            !req.session || 
            !req.session.username) {
            return res.status(400).send(INVALID_DATA_TEXT);
        }
        next();
    };

    static GameCancel = (req, res, next) => {
        if (!req.session ||
            (!req.session.gameId && !req.session.roomId) ||
            !req.session.username) {
            return res.status(400).send(INVALID_DATA_TEXT);
        }
        next();
    };

    static RoomCreate = (req, res, next) => {
        if (!req.session || 
            !req.session.username) {
            return res.status(400).send(INVALID_DATA_TEXT);
        }
        next();
    };

    static RoomConfig = (req, res, next) => {
        if (!req.body ||
            !Object.prototype.hasOwnProperty.call(req.body, 'allowDuplicates') ||
            !Object.prototype.hasOwnProperty.call(req.body, 'start') ||
            typeof req.body.allowDuplicates !== 'boolean' ||
            typeof req.body.start !== 'boolean' ||
            !req.session || 
            !req.session.username) {
            return res.status(400).send(INVALID_DATA_TEXT);
        }
        next();
    };

    static RoomJoin = (req, res, next) => {
        if (!req.body ||
            !Object.prototype.hasOwnProperty.call(req.body, 'roomId') ||
            Number.isNaN(req.body.roomId) ||
            !Room.IsValidRoomId(req.body.roomId) ||
            !req.session || 
            !req.session.username) {
            return res.status(400).send(INVALID_DATA_TEXT);
        }
        next();
    };

    static RoomState = (req, res, next) => {
        if (!req.session || 
            !req.session.roomId ||
            !req.session.username) {
            return res.status(400).send(INVALID_DATA_TEXT);
        }
        next();
    };

    static StatGlobal = (req, res, next) => {
        if (!Object.prototype.hasOwnProperty.call(req.query, 'allowDuplicates') ||
            !['true', 'false'].includes(String(req.query.allowDuplicates).toLowerCase()) ||
            !req.session || 
            !req.session.username) {
            return res.status(400).send(INVALID_DATA_TEXT);
        }
        next();
    };

    static StatPersonal = (req, res, next) => {
        if (!Object.prototype.hasOwnProperty.call(req.query, 'allowDuplicates') ||
            !['true', 'false'].includes(String(req.query.allowDuplicates).toLowerCase()) ||
            !req.session || 
            !req.session.username) {
            return res.status(400).send(INVALID_DATA_TEXT);
        }
        next();
    };

    static StatVeteran = (req, res, next) => {
        if (!Object.prototype.hasOwnProperty.call(req.query, 'allowDuplicates') ||
            !['true', 'false'].includes(String(req.query.allowDuplicates).toLowerCase()) ||
            !req.session || 
            !req.session.username) {
            return res.status(400).send(INVALID_DATA_TEXT);
        }
        next();
    };

    static StatLeaderboard = (req, res, next) => {
        if (!Object.prototype.hasOwnProperty.call(req.query, 'allowDuplicates') ||
            !Object.prototype.hasOwnProperty.call(req.query, 'showAnonymous') ||
            !['true', 'false'].includes(String(req.query.allowDuplicates).toLowerCase()) ||
            !['true', 'false'].includes(String(req.query.showAnonymous).toLowerCase()) ||
            !req.session || 
            !req.session.username) {
            return res.status(400).send(INVALID_DATA_TEXT);
        }
        next();
    };

    static UserRegister = (req, res, next) => {
        if (!req.body ||
            !Object.prototype.hasOwnProperty.call(req.body, 'username') ||
            typeof req.body.username !== 'string' ||
            !/^[A-Za-z0-9_-]{1,9}$/.test(req.body.username)) {
            return res.status(400).send(INVALID_DATA_TEXT);
        }
        next();
    };
}