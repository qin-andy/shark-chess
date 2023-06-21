# shark-chess

![Tournament Matchup Chart](assets/matchup_chart.PNG?raw=true "Title")

An fullstack automatic chess tournament simulator and visualizer written in Python and TypeScript/React.
 * Implement bots with custom move generation heuristics (compatible with existing UCIs such as Stockfish, Komodo, etc)
 * Arrange round robin tourneys between bots with customizable match lengths, max moves, engine thinking speeds, etc
 * Export tourney settings game PGNs, aggregate match results, bot settings, and bot performance statistics to CSV, JSON, or MongoDB
 * Continue existing tourney results with new bots, appending to existing results and statistics
 * Visualize matchups, performance and inspect individual games with a React frontend

 Inspired by [an incredible series of papers written by Tom Murphy for SIGBOVIK.](http://tom7.org/chess/).

 Check out some excample games on this Lichess study:
 https://lichess.org/study/PadCquFg

## Setting up Local Development
If developing on Windows, run all commands through WSL
### Setting up MongoDB
  1. In terminal, start MongoDB with `mongod`
  2. In a different terminal, Start MongoDB shell with `mongosh`. Run `use shark-chess`

### Setting up Flask server
Uses Python3
  1. From root, run `cd backend`
  2. Set up venv with `python3 -m venv env` and `source venv/bin/activate`
  3. Install dependencies with `pip install -r requirements.txt`
  4. Run flask app with `python -m flask --app src/app.py run`. API runs on `localhost:5000`

### Setting up Frontend
Check node version with `node -v`. Developed on v18.14.2
  1. From root, `cd ui`
  2. Install dependencies with `npm install`
  3. Run `npm start` to run live reload on `localhost:3000`

### Running a Tourney
WIP. Gist is to change function calls in `main.py` to adjust tourney settings, run `python src/main.py`,
Check DB in MongoSh, change API call in `MainPage.tsx`.



