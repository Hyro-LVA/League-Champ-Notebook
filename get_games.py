# get_games.py
# Downloads my recent League of Legends games from the Riot API
# and saves the champion I played in each game to games.csv
#
# Run it with:  python get_games.py

import time
import getpass
import requests
import pandas as pd

# the key is typed in when the program runs so it never gets saved in a file
api_key = getpass.getpass("Paste your Riot API key (it will not show up): ").strip()
game_name = input("Game name (the part before the #): ").strip()
tag_line = input("Tagline (the part after the #): ").strip()
num_games = 50

headers = {"X-Riot-Token": api_key}
base_url = "https://americas.api.riotgames.com"

# Step 1: turn my Riot ID into a puuid (the id Riot uses for my account)
url = base_url + "/riot/account/v1/accounts/by-riot-id/" + game_name + "/" + tag_line
response = requests.get(url, headers=headers)

if response.status_code == 404:
    print("Could not find that Riot ID. Check the spelling and tagline.")
    quit()
if response.status_code != 200:
    print("Something went wrong (status " + str(response.status_code) + "). Is the API key expired?")
    quit()

puuid = response.json()["puuid"]
print("Found account!")

# Step 2: get the ids of my most recent games
url = base_url + "/lol/match/v5/matches/by-puuid/" + puuid + "/ids"
response = requests.get(url, headers=headers, params={"start": 0, "count": num_games})
match_ids = response.json()
print("Found", len(match_ids), "games")

# Step 3: look up each game and find which champion I played
champions = []
wins = []

for match_id in match_ids:
    url = base_url + "/lol/match/v5/matches/" + match_id
    response = requests.get(url, headers=headers)

    # the dev key only allows 100 requests every 2 minutes so I wait between each one
    time.sleep(1.3)

    if response.status_code != 200:
        print("skipping", match_id)
        continue

    match = response.json()

    # skip remakes (games shorter than 5 minutes)
    if match["info"]["gameDuration"] < 300:
        continue

    for player in match["info"]["participants"]:
        if player["puuid"] == puuid:
            champions.append(player["championName"])
            wins.append(player["win"])

    print("got", len(champions), "games so far")

# Step 4: save to a csv file
games = pd.DataFrame({"champion": champions, "win": wins})
games.to_csv("games.csv", index=False)
print("Saved", len(champions), "games to games.csv")
