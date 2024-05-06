import requests
import json
from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from nerdgrid.auth import login_required
from nerdgrid.db import get_db

bp = Blueprint('grid', __name__)

url = "https://api-nba-v1.p.rapidapi.com/players/statistics"
url2 = "https://api-nba-v1.p.rapidapi.com/games"

playerGameStats = {"game":"8133"}
gameStats = {"id":"8133"}

headers = {
	"X-RapidAPI-Key": "6c04748644mshcbbb06b9b2789bep1102b6jsneee9fc830bb9",
	"X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=playerGameStats)
data = response.json()  

response2 = requests.get(url2, headers=headers, params=gameStats)
gameData = response2.json()

date_string = gameData["response"][0]["date"]["start"]
# Parse the date string into a datetime object
date_obj = datetime.fromisoformat(date_string)
# Format the datetime object as a string without the time part
formatted_date = date_obj.strftime("%Y-%m-%d")

homeTeam = gameData["response"][0]["teams"]["home"]["name"]
visitorTeam = gameData["response"][0]["teams"]["visitors"]["name"]
homeTeamLogo = gameData["response"][0]["teams"]["home"]["logo"]
visitTeamLogo = gameData["response"][0]["teams"]["visitors"]["logo"]
num_players = len(data["response"])

minplayed23 = {}
ftm5 = {}
fgpct60 = {}

for i in range(num_players):
    player = data["response"][i]
    firstName = player["player"]["firstname"]
    lastName = player["player"]["lastname"]
    fullName = firstName + " " + lastName
    
    playerTime = 0
    ftm = 0
    fgp = 0

    if player["min"] is not None:
        playerTime = int(player["min"].split(":")[0])
    if  playerTime >= 23:   
        minplayed23[fullName] = player["team"]["nickname"]

    if player["ftm"] is not None:
        ftm = player["ftm"]
    if ftm >= 5:
        ftm5[fullName] = player["team"]["nickname"]

    if player["fgp"] is not None:
        fgp = player["fgp"]
    if float(fgp) >= 60:
        fgpct60[fullName] = player["team"]["nickname"]

@bp.route('/')
def index():
    db = get_db()
    return render_template('grid/grid.html', homeLogo = homeTeamLogo, visitLogo = visitTeamLogo, gameDate = formatted_date)



# for i in range(3):
#     min23guess = input("Name a player that is on the Atlanta Hawks and played 23+ minutes: ")
#     min23guess2 = input("Name a player that is on the Orlando Magic and played 23+ minutes: ")
#     if minplayed23.get(min23guess, "").lower() == "hawks" and minplayed23.get(min23guess2, "").lower() == "magic":
#         print("gj lil nigga")
#         break
#     else:
#         print("no")
# else:
#     print("your idiot")









