# League-Champ-Notebook

How much do I really play my most picked champion?

This project downloads my recent League of Legends games with the Riot API and uses
bootstrapping (from DSC 10 at UCSD) to make a 95% confidence interval for the pick
rate of my most played champion.

## Files

- `get_games.py` - downloads my last 50 games and saves them to `games.csv`
- `champion_picks.ipynb` - the notebook with the bar chart, bootstrap and histogram
- `games.csv` - the data (champion and win/loss for each game)

## How to run it

1. `pip install -r requirements.txt`
2. `python get_games.py` and paste in a Riot API key from https://developer.riotgames.com
3. Open `champion_picks.ipynb` and click Run All

This project isn't endorsed by Riot Games and doesn't reflect the views or opinions
of Riot Games or anyone officially involved in producing or managing Riot Games
properties.
