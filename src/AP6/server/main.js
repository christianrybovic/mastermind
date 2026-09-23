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
import Room from './room.js'

const NO_STATISTICS = 'No statistics available';
const ROOM_ERROR = 'Room error occured';
const VERSION = "/v6/"
const PORT = 8090;

const app = express();
const games = new Map();

function logger(req, res, next) {
    console.log({
        method: req.method,
        url:    req.originalUrl,
        body:   req.body,
        gid:    req.session.gameId,
        user:   req.session.username
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
    req.session.roomId = null;
    const gid = crypto.randomUUID();
    const config =  new Configuration(req.body.allowDuplicates, req.body.endless);
    games.set(gid, new Game(config));
    req.session.gameId = gid;
    res.status(201).send();
});

app.post(VERSION + "game/guess", Validator.GameGuess, (req, res) => {
    const gid = req.session.gameId;
    let game;
    if (req.session.roomId) {
        try {
            game = Room.GetById(req.session.roomId).getGame(req.session);
        } catch {}
    } else {
        game = games.get(gid);
    }
    if (game == null || game.hasFinished) {
        res.status(410).send()
    } else {
        const result = game.validate(req.body.combination);
        if (result.state == STATE_WON) {
            Stat.AddStat(req.session.username, result.duration, result.guesses, game.config);
            if (req.session.roomId != null) {
                Room.GetById(req.session.roomId).notify(true);
            }
        } else {
           if (req.session.roomId) {
                Room.GetById(req.session.roomId).notify(false);
            } 
        }
        res.status(200).json(result);
    }
});

app.delete(VERSION + "game/cancel", Validator.GameCancel, (req, res) => {
    const gid = req.session.gameId;
    let game;
    if (req.session.roomId) {
        try {
            Room.GetById(req.session.roomId).leave(req.session);
        } catch {}
    } else {
        if (game) {
            games.delete(gid);
        }
    }
    req.session.gameId = null;
    req.session.roomId = null;
    res.status(200).send();
});

app.post(VERSION + "room/create", Validator.RoomCreate, (req, res) => {
    req.session.gameId == null;
    const room = new Room(req.session);
    req.session.roomId = room.roomId;
    res.status(201).send(room.roomId);
});

app.post(VERSION + "room/join", Validator.RoomJoin, (req, res) => {
    req.session.gameId == null;
    try {
        const room = Room.GetById(req.body.roomId);
        room.join(req.session);
        req.session.roomId = room.roomId;
        res.status(200).send();
    } catch {
        res.status(500).send(ROOM_ERROR);
    }
});

app.get(VERSION + "room/state", Validator.RoomState, (req, res) => {
    try {
        const room = Room.GetById(req.session.roomId);
        const state = room.getState(req.session);
        res.status(200).json(state);
    } catch {
        res.status(500).send(ROOM_ERROR);
    }
});

app.post(VERSION + "room/config", Validator.RoomConfig, (req, res) => {
    try {
        const allowDuplicates = Configuration.ParseBoolean(req.body.allowDuplicates);
        const start = Configuration.ParseBoolean(req.body.start);
        const room = Room.GetById(req.session.roomId);
        room.setConfig(req.session, allowDuplicates, start);
        res.status(200).send();
    } catch {
        res.status(500).send(ROOM_ERROR);
    }
});

app.get(VERSION + "stat/global", Validator.StatGlobal, async (req, res) => {
    try {
        const config = new Configuration(req.query.allowDuplicates);
        const stats = await Stat.GetStats(config);
        res.status(200).json(stats);
    } catch {
        res.status(503).send(NO_STATISTICS);
    }
});

app.get(VERSION + "stat/personal", Validator.StatPersonal, async (req, res) => {
    try {
        const config = new Configuration(req.query.allowDuplicates);
        const stats = await Stat.GetStats(config, req.session.username);
        res.status(200).json(stats);
    } catch {        
        res.status(503).send(NO_STATISTICS);
    }
});

app.get(VERSION + "stat/veteran", Validator.StatVeteran, async (req, res) => {
    try {
        const config = new Configuration(req.query.allowDuplicates);
        const veteran = await Stat.GetVeteran(config);
        res.status(200).json(veteran);
    } catch {        
        res.status(503).send(NO_STATISTICS);
    }
});

app.get(VERSION + "stat/leaderboard", Validator.StatLeaderboard, async (req, res) => {
    try {
        const config = new Configuration(req.query.allowDuplicates);
        const showAnonymous = Configuration.ParseBoolean(req.query.showAnonymous);
        const leaderboard = await Stat.GetLeaderboard(config, showAnonymous);
        console.log(leaderboard)
        res.status(200).json(leaderboard);
    } catch {        
        res.status(503).send(NO_STATISTICS);
    }
});

app.post(VERSION + "user/register", Validator.UserRegister, (req, res) => {
    req.session.username = req.body.username;
    res.status(200).send();
});