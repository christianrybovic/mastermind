/**
 * Copyright (c) 2026 Team Alpha
 * All rights reserved.
 *
 * Licensed under the MIT License. See LICENSE file for details.
 */

import express from 'express'
import Validator from './validator.js'
import Game from './game.js'

const VERSION = "/v2/"
const PORT = 8090;

const app = express();
let game;

function logger(req, res, next) {
    console.log({
        method: req.method,
        url:    req.originalUrl,
        body:   req.body
    });
    next();
}

app.listen(PORT, () => console.log(`Server started with port ${PORT}`));
app.use(express.json());
app.use(logger);

app.post(VERSION + "game/create", Validator.GameCreate, (req, res) => {
    game = new Game(req.body.allowDuplicates, req.body.endless);
    res.status(201).send();
});

app.post(VERSION + "game/guess", Validator.GameGuess, (req, res) => {
    if (game == null || game.hasFinished) {
        res.status(410).send();
    } else {
        const result = game.validate(req.body.combination);
        res.status(200).json(result);
    }
});

app.delete(VERSION + "game/cancel", (req, res) => {
    game = null;
    res.status(200).send();
});