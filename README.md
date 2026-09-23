# Mastermind by Team Alpha

A client-server implementation of the classic logic game **Mastermind**, built as part of a school project (Team Alpha). The Python client provides an interactive console game, while a Node.js server manages games, validates input, and exposes everything through a versioned REST API. Features include autoplay/automated clients, statistics, a leaderboard, SQLite persistence, and multiplayer support.

<img width="676" height="420" alt="animation" src="https://github.com/user-attachments/assets/bdd32c8a-10ab-48b2-9ea7-eb1a52884870" />

## Work Packages (AP)

The project was built incrementally across six work packages (Arbeitspakete), each one building on top of the previous one.

| Package | Content |
|----|---------|
| **AP1** | Single-game server (one active game on the server) and an interactive Python client script for manual play via the console. |
| **AP2** | Simple statistics (number of guesses & game duration) and client automation (autoplay with a configurable number of rounds). |
| **AP3** | Multi-game server (multiple clients/sessions at the same time) and parallel, automated clients using threading. |
| **AP4** | Extended statistics: the server stores game duration and number of guesses per game and exposes average, minimum, and maximum values via the REST API. |
| **AP5** | Persistent storage of game data in a SQLite database, player recognition via usernames, and leaderboard/veteran statistics. |
| **AP6** | Multiplayer mode: create/join rooms, matchmaking, and a round-based game between multiple players including win/loss logic. |

> **Note:** Since every AP builds on the previous one, **AP6** contains the complete, final version of the project (all earlier APs included) - it's likely the most interesting part to look at if you just want to see the result.

## Requirements

**Server**
- Node.js & npm
- Packages: `express`, `express-session`, `sqlite3`

**Client**
- Python 3
- Package: `requests`

**Other**
- Terminal with ANSI support (colors & cursor control)

## Getting Started

### Start the server
```bash
cd server
npm install
npm run
```
The server listens on port `8090`. On first start, `mastermind.db` is created automatically if it doesn't exist yet.

### Start the client
```bash
cd client
pip install requests
python main.py
```
Running without arguments starts the interactive game mode. After entering a username, you can play, view statistics/leaderboard, or join a multiplayer match.

> **Tip:** For the best visual experience (colors, block layout), run the client in the **VS Code integrated terminal**.

> **Easter Egg:** AP6 includes a hidden easter egg - see if you can find it! :gift:

### (Optional) Build the API documentation
```bash
cd doc
npm run build
```
This generates a HTML file from `index.apib` using Aglio.

## License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2026 Team Alpha

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
