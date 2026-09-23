/**
 * Copyright (c) 2026 Team Alpha
 * All rights reserved.
 *
 * Licensed under the MIT License. See LICENSE file for details.
 */

import crypto from 'crypto'
import express from 'express'
import session from 'express-session'
import Configuration from './configuration.js'
import Validator from './validator.js'
import Game, {STATE_WON} from './game.js'
import Stat from './stat.js'

const NO_STATISTICS = 'No statistics available';
const VERSION = "/v4/"
const PORT = 8090;

const app = express();
const games = new Map();

function logger(req, res, next) {
    console.log({
        method: req.method,
        url:    req.originalUrl,
        body:   req.body,
        gid:    req.session.gameId
    });
    next();
}

app.use(session({
    secret: "4X2x3Jw7iM9QmYvK7zIrN1pT6sZ0cHdBeAqP5uYgWnCvE7rL",
    resave: false,
    saveUninitialized: false
}));
app.listen(PORT, () => console.log(`Server started with port ${PORT}`));
app.use(express.json());
app.use(logger);

app.post(VERSION + "game/create", Validator.GameCreate, (req, res) => {
    const gid = crypto.randomUUID();
    const config = new Configuration(req.body.allowDuplicates, req.body.endless);
    games.set(gid, new Game(config));
    req.session.gameId = gid;
    res.status(201).send();
});

app.post(VERSION + "game/guess", Validator.GameGuess, (req, res) => {
    const gid = req.session.gameId;
    const game = games.get(gid);
    if (game == null || game.hasFinished) {
        res.status(410).send()
    } else {
        const result = game.validate(req.body.combination);
        if (result.state == STATE_WON) {
            Stat.AddStat(req.sessionID, result.duration, result.guesses, game.config);
        }
        res.status(200).json(result);
    }
});

app.delete(VERSION + "game/cancel", Validator.GameCancel, (req, res) => {
    const gid = req.session.gameId;
    const game = games.get(gid);
    if (game) {
        games.delete(gid);
    }
    req.session.gameId = null;
    res.status(200).send();
});

app.get(VERSION + "stat/global", Validator.StatGlobal, (req, res) => {
    try {
        const config = new Configuration(req.query.allowDuplicates);
        const stats = Stat.GetStats(config);
        res.status(200).json(stats);
    } catch {
        res.status(503).send(NO_STATISTICS);
    }
});

app.get(VERSION + "stat/personal", Validator.StatPersonal, (req, res) => {
    try {
        const config = new Configuration(req.query.allowDuplicates);
        const stats = Stat.GetStats(config, req.sessionID);
        res.status(200).json(stats);
    } catch {        
        res.status(503).send(NO_STATISTICS);
    }
});