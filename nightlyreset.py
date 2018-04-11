from espnscrape import scrapeESPN

def createnewlog():
	games = scrapeESPN(0)
	with open('discordscorebot/gamelog.txt','w') as f:
		for game in games:
			f.write(game['tid1'] + "," + game['tid2'] + "," + '0,0,0,0,0,0\n') #tid1,tid2,10-1h,half,10-2h,5-2h,2-2h,final