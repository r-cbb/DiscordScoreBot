from urllib.request import urlopen, Request
import json
#import time
from fake_useragent import UserAgent
import html
from datetime import datetime  
from datetime import timedelta

GAME_STATUS_PRE = 0
GAME_STATUS_IN = 1
GAME_STATUS_POST = 2

POS_TEN = 2
POS_HALF = 3
POS_PTEN = 4
POS_PFIVE = 5
POS_PTWO = 6
POS_FINAL = 7

def _returntime(delta):
	#Current Time will always be adjusted backwards 4 hours (4 am eastern will change over the day, allowing games to finish.)
	_currenttime = datetime.now()+timedelta(days=delta)-timedelta(hours=-4)
	
	return _addfrontzero(_currenttime.year)+_addfrontzero(_currenttime.month)+_addfrontzero(_currenttime.day)
		
def _addfrontzero(value):
	if value < 10:
		return "0" + str(value)
	else:
		return str(value)

def scrapeESPN(delta=0):

	#MODE_ACTIVE = 0
	#MODE_INACTIVE = 1
		
	req = Request("http://www.espn.com/nba/scoreboard/_/date/" + _returntime(delta))
	req.headers["User-Agent"] = UserAgent(verify_ssl=False).chrome

	# Load data
	scoreData = urlopen(req).read().decode("utf-8")
	scoreData = scoreData[scoreData.find('window.espn.scoreboardData 	= ')+len('window.espn.scoreboardData 	= '):]
	scoreData = json.loads(scoreData[:scoreData.find('};')+1])

	games = []
	for event in scoreData['events']:
		game = dict()

		game["date"] = event['date']
		status = event['status']['type']['state']
		if status == "pre":
			game['status'] = GAME_STATUS_PRE
		elif status == "in":
			game['status'] = GAME_STATUS_IN
		else:
			game['status'] = GAME_STATUS_POST
		team1 = html.unescape(event['competitions'][0]['competitors'][0]['team']['location'])
		tid1 = event['competitions'][0]['competitors'][0]['id']
		score1 = int(event['competitions'][0]['competitors'][0]['score'])
		team1abv = event['competitions'][0]['competitors'][0]['team']['abbreviation']
		team2 = html.unescape(event['competitions'][0]['competitors'][1]['team']['location'])
		tid2 = event['competitions'][0]['competitors'][1]['id']
		score2 = int(event['competitions'][0]['competitors'][1]['score'])
		team2abv = event['competitions'][0]['competitors'][1]['team']['abbreviation']
        
		# Hawaii workaround (Built for College, not NBA)
		if team1 == "Hawai'i":
			team1 = "Hawaii"
		if team2 == "Hawai'i":
			team2 = "Hawaii"

		homestatus = event['competitions'][0]['competitors'][0]['homeAway']

		if homestatus == 'home':
			game['hometeam'], game['homeid'], game['homeabv'], game['homescore'], game['awayteam'], game['awayid'], game['awayabv'], game['awayscore'] =\
				team1, tid1, team1abv, score1, team2, tid2, team2abv, score2
		else:
			game['hometeam'], game['homeid'], game['homeabv'], game['homescore'], game['awayteam'], game['awayid'], game['awayabv'], game['awayscore'] = \
				team2, tid2, team2abv, score2, team1, tid1, team1abv, score1

		game['time'] = event['status']['type']['shortDetail']

#		gamestring = team1 + " " + str(score1) + " vs. " + team2 + " " + str(score2) + " - " + game['time']
		try:
			game['network'] = event['competitions'][0]['broadcasts'][0]['names'][0]
#			gamestring += " (TV: " + game['network'] + ")"
		except:
			game['network'] = "N/A"
			pass
            
		#print(team1,tid1,team1abv,score1,team2,tid2,team2abv,score2,game['time'],game['date'],game['network'])
		indgame = {'team1':team1,'tid1':tid1,'team1abv':team1abv,'score1':score1,'team2':team2,'tid2':tid2,'team2abv':team2abv,'score2':score2,'time':game['time'],'date':game['date'],'network':game['network'],'status':game['status']}
		games.append(indgame)
#		print(gamestring)
	return games

def returnallgames(time=0):
	gamestrings = ''
	for game in scrapeESPN(time):
		gamestrings = gamestrings + game['team1'] + " " + str(game['score1']) + " vs. " + game['team2'] + " " + str(game['score2']) + " - " + game['time'] + "(TV: " + game['network'] + ")"
	return gamestrings

def readlog():
	with open('discordscorebot/gamelog.txt','r') as f:
		lines = f.readlines()
		
	allgames = []
	for line in lines:
		game = line.replace('\n','').split(',')
		allgames.append(game)
	
	return allgames
	
def writelog(allgames):
	with open('discordscorebot/gamelog.txt','w') as f:
		for game in allgames:
			string = ''
			for item in game[:-1]:
				string = string + item + ','
			string = string+game[-1]+'\n'
			f.write(string)
			
def ScoreTickBuilder():
	games = scrapeESPN()
	livetickerstr = ''
	allgamelog = readlog() 
	for game in games:
		if game['status'] == GAME_STATUS_PRE:
			continue
		elif game['status'] == GAME_STATUS_POST:
			for log in allgamelog:
				if log[0] == game['tid1'] or log[0] == game['tid2']:
					if log[7] == 0:
						log[7] = 1
						livetickerstr = livetickerstr + game['team2'] + " " + str(game['score2']) + " @ " + game['team1'] + " " + str(game['score1']) + " - " + game['time'] + " (TV: " + game['network'] + ")"
						break
					else:
						break
		else:
			livetickerstrret, allgamelog = gameinprocess(game,allgamelog)
			livetickerstr = livetickerstr + livetickerstrret + '\n'
			
	writelog(allgamelog)
	return livetickerstr

def gameinprocess(game,allgamelog):
	if game['time'] == 'Halftime':
		if not ifposted(allgamelog,game,POS_HALF):
			return gamestring(game), updateprelog(allgamelog,game,POS_HALF)
	elif game['time'] == 'End of 1st':
		if not isposted(allgamelog,game,POS_TEN):
			return gamestring(game), updateprelog(allgamelog,game,POS_TEN)
	elif game['time'] == 'End of 3rd':
		if not isposted(allgamelog,game,POS_PTEN):
			return gamestring(game), updateprelog(allgamelog,game,POS_PTEN)
			
def gamestring(game):
	return game['team2'] + " " + str(game['score2']) + " @ " + game['team1'] + " " + str(game['score1']) + " - " + game['time'] + " (TV: " + game['network'] + ")"
			
def updateprelog(allgamelog,gameteam, pos):
	for log in allgamelog:
		if log[0] == gameteam or log[1] == gameteam:
			for i in range(2,pos+1):
				log[i] = '1'
	return allgamelog

def ifposted(allgamelog,gameteam,pos):
	for log in allgamelog:
		if log[0] == gameteam or log[1] == gameteam:
			if log[pos] == 0:
				return False
			else:
				return True