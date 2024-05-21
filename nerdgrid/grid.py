import requests
import flask
from datetime import datetime
from flask import (
    Blueprint, render_template, request, jsonify, g, session, redirect, url_for
)
from werkzeug.exceptions import abort
from nerdgrid.auth import login_required
from nerdgrid.db import get_db

import sqlite3

from nerdgrid.auth import bp as auth_bp
bp = Blueprint('grid', __name__)
bp.register_blueprint(auth_bp)

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
date_obj = datetime.fromisoformat(date_string)
formatted_date = date_obj.strftime("%Y-%m-%d")

homeTeam = gameData["response"][0]["teams"]["home"]["name"]
visitorTeam = gameData["response"][0]["teams"]["visitors"]["name"]
homeTeamLogo = gameData["response"][0]["teams"]["home"]["logo"]
visitTeamLogo = gameData["response"][0]["teams"]["visitors"]["logo"]
num_players = len(data["response"])

minplayed23 = {}
ftm5 = {}
fgpct60 = {}
playerList = []

for i in range(num_players):
    player = data["response"][i]
    firstName = player["player"]["firstname"]
    lastName = player["player"]["lastname"]
    fullName = firstName + " " + lastName
    playerList.append(fullName)
    
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



def checkAnswer(dict, player, team):
    if player in dict and dict[player] == team:
        return True
    else:
        return False


def streak(user_id):
    db = get_db()
    user = db.execute('SELECT streak FROM user WHERE id = ?', (user_id,)).fetchone()
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'streak': user['streak']})


@bp.route('/')
@login_required
def index():
    return render_template('grid/grid.html', homeLogo = homeTeamLogo, visitLogo = visitTeamLogo, gameDate = formatted_date, playersList = playerList, message = "",  user_id=g.user['id'])

@bp.route('/checkPlayer1', methods=['POST'])
def checkPlayer1():
    message = ""
    if request.method == 'POST':
        user_player = request.form['name']
        if checkAnswer(minplayed23, user_player, gameData["response"][0]["teams"]["home"]["nickname"]):
            message = "Correct!"
        else:
            message = "Incorrect!"
    return message


@bp.route('/checkPlayer4', methods=['POST'])
def checkPlayer4():
    message = ""
    if request.method == 'POST':
        user_player = request.form['name3']
        if checkAnswer(minplayed23, user_player, gameData["response"][0]["teams"]["visitors"]["nickname"]):
            message = "Correct!"
        else:
            message = "Incorrect!"
    return message


@bp.route('/checkPlayer2', methods=['POST'])
def checkPlayer2():
    message = ""
    if request.method == 'POST':
        user_player = request.form['name1']
        if checkAnswer(ftm5, user_player, gameData["response"][0]["teams"]["home"]["nickname"]):
            message = "Correct!"
        else:
            message = "Incorrect!"
    return message

@bp.route('/checkPlayer5', methods=['POST'])
def checkPlayer5():
    message = ""
    if request.method == 'POST':
        user_player = request.form['name4']
        if checkAnswer(ftm5, user_player, gameData["response"][0]["teams"]["visitors"]["nickname"]):
            message = "Correct!"
        else:
            message= "Incorrect!"
    return message

@bp.route('/checkPlayer3', methods=['POST'])
def checkPlayer3():
    message = ""
    if request.method == 'POST':
        user_player = request.form['name2']
        if checkAnswer(fgpct60, user_player, gameData["response"][0]["teams"]["home"]["nickname"]):
            message = "Correct!"
        else:
            message = "Incorrect!"
    return message

@bp.route('/checkPlayer6', methods=['POST'])
def checkPlayer6():
    message = ""
    if request.method == 'POST':
        user_player = request.form['name5']
        if checkAnswer(fgpct60, user_player, gameData["response"][0]["teams"]["visitors"]["nickname"]):
            message = "Correct!"
        else:
            message = "Incorrect!"
    return message

@bp.route('/get_streak', methods=['GET'])
def get_streak():
    user_id = request.args.get('id')

    conn = sqlite3.connect('schema.db')
    cursor = conn.cursor()

    cursor.execute("SELECT streak FROM user WHERE id = ?", (user_id,))
    streak = cursor.fetchone()[0]

    conn.close()

    return jsonify({'streak': streak})







