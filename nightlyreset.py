import espnscrape
import espnscrapencaa

def createnewlog():
    games = espnscrape.scrapeESPN(0)
    with open('discordscorebot/gamelog.txt','w') as f:
        for game in games:
            f.write(game['tid1'] + "," + game['tid2'] + "," + '0,0,0,0,0,0\n') #tid1,tid2,10-1h,half,10-2h,5-2h,2-2h,final

def cacheGames():
    for n in range(-7, 8):
        if n == 0: # Don't use a cache for today since the results will most likely be changing
            continue
        espnscrape.scrapeESPN(n)
		
def createnewlogncaa():
    games = espnscrapencaa.scrapeESPN(0)
    with open('discordscorebot/ncaagamelog.txt','w') as f:
        for game in games:
            f.write(game['tid1'] + "," + game['tid2'] + "," + '0,0,0,0,0,0,0\n') #tid1,tid2,10-1h,half,10-2h,5-2h,2-2h,final

def cacheGamesncaa():
    for n in range(-7, 8):
        if n == 0: # Don't use a cache for today since the results will most likely be changing
            continue
        espnscrapencaa.scrapeESPN(n)

createnewlog()
cacheGames()
createnewlogncaa()
cacheGamesncaa()