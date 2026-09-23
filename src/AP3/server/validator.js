/**
 * Copyright (c) 2026 Team Alpha
 * All rights reserved.
 *
 * Licensed under the MIT License. See LICENSE file for details.
 */

import Game from './game.js'

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
            typeof req.body.endless !== 'boolean') {
            return res.status(400).send(INVALID_DATA_TEXT);
        }
        next();
    };

    static GameGuess = (req, res, next) => {
        if (!req.body ||
            !req.session.gameId ||
            !Object.prototype.hasOwnProperty.call(req.body, 'combination') ||
            Number.isNaN(req.body.combination) ||
            !Game.IsValidCombination(req.body.combination)) {
            return res.status(400).send(INVALID_DATA_TEXT);
        }
        next();
    };

    static GameCancel = (req, res, next) => {
        if (!req.session.gameId) {
            return res.status(400).send(INVALID_DATA_TEXT);
        }
        next();
    };
}