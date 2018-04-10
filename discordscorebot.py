import random
import asyncio
import requests
from credentials_discord import TOKEN
import discord
from discord import Game
from discord.ext.commands import Bot
import espnscrape

BOT_PREFIX = ("?", "!")

teams = ["Toronto","Boston","Philadelphia","Cleveland","Indiana","Miami","Milwaukee Bucks","Washington","Detroit","Charlotte","New-York","Brooklyn","Chicago","Orlando","Atlanta","Houston","Golden State","Portland","Utah","New Orleans","San Antonio","Oklahoma City","Minnesota","Denver","LA","Los Angeles","Sacramento","Dallas","Memphis","Phoenix"]
teams_short = ["TOR","BOS","PHI","CLE","IND","MIA","MIL","WSH","DET","CHA","NY","BKN","CHI","ORL","ATL","HOU","GS","POR","UTAH","NO","SA","OKC","MIN","DEN","LAC","LAL","SAC","DAL","MEM","PHX"]

client = Bot(command_prefix=BOT_PREFIX)

@client.command()
async def allgames():
	try:
		for game in espnscrape.scrapeESPN(0):
			gamestring = game['team1'] + " " + str(game['score1']) + " vs. " + game['team2'] + " " + str(game['score2']) + " - " + game['time'] + "(TV: " + game['network'] + ")"
			await client.say(gamestring)
	except Exception as e:
		print(str(e))
		await client.say("Error Occured")
		
@client.command()
async def score(*,team:str):
	try:
		if team not in teams and team not in teams_short:
			await client.say("Can't Find Team")
			print("Can't Find Team")
		else:
			allgames = espnscrape.scrapeESPN(0)
			if team in (game['team1'] for game in allgames) or team in (game['team2'] for game in allgames) or team in (game['team1abv'] for game in allgames) or team in (game['team2abv'] for game in allgames):
				for game in allgames:
					if team == game['team1'] or team == game['team2'] or team == game['team1abv'] or team == game['team2abv']:
						gamestring = game['team2'] + " " + str(game['score2']) + " @ " + game['team1'] + " " + str(game['score1']) + " - " + game['time'] + " (TV: " + game['network'] + ")"
						await client.say(gamestring)
						print(gamestring)
						break
			else:
				allgameteam = '**Past Games:**\n'
				for n in range(-7,7):
					allgames = espnscrape.scrapeESPN(n)
					if team in (game['team1'] for game in allgames) or team in (game['team2'] for game in allgames) or team in (game['team1abv'] for game in allgames) or team in (game['team2abv'] for game in allgames):
						for game in allgames:
							if team == game['team1'] or team == game['team2'] or team == game['team1abv'] or team == game['team2abv']:
								gamestring = game['team2'] + " " + str(game['score2']) + " @ " + game['team1'] + " " + str(game['score1']) + " - " + game['time'] + " (TV: " + game['network'] + ")"
								# await client.say(gamestring)
								allgameteam = allgameteam + gamestring + "\n"
								print(gamestring)
					if n == 0:
						allgameteam = allgameteam + "**Future Games:**\n"
						
				await client.say("There are currently no games today.\n" + allgameteam)
				#await client.say("No Games")
				#print("No Games")
	except Exception as e:
		print(str(e))
		await client.say("Error Occured")
		
@client.command()
async def schedule(*,team:str):
	try:
		if team not in teams and team not in teams_short:
			await client.say("Can't Find Team")
			print("Can't Find Team")
		else:
			allgames = espnscrape.scrapeESPN(0)
			allgameteam = '**Past Games:**\n'
			for n in range(-7,7):
				gameday = False
				allgames = espnscrape.scrapeESPN(n)
				if team in (game['team1'] for game in allgames) or team in (game['team2'] for game in allgames) or team in (game['team1abv'] for game in allgames) or team in (game['team2abv'] for game in allgames):
					for game in allgames:
						if team == game['team1'] or team == game['team2'] or team == game['team1abv'] or team == game['team2abv']:
							gamestring = game['team2'] + " " + str(game['score2']) + " @ " + game['team1'] + " " + str(game['score1']) + " - " + game['time'] + " (TV: " + game['network'] + ")"
							# await client.say(gamestring)
							gameday = True
							allgameteam = allgameteam + gamestring + "\n"
							print(gamestring)
				if n == -1:
					allgameteam = allgameteam + "**Today's Game:**\n"
				elif n == 0:
					# print("Enter 0 if")
					#print(gameday)
					if not gameday:
						# print("entered if not statement")
						allgameteam = allgameteam.replace("**Today's Game:**\n","")
						
					allgameteam = allgameteam + "**Future Game:**\n"
					
			await client.say("Basketball Schedule for "+team+"\n"+allgameteam)
			#await client.say("No Games")
			#print("No Games")
	except Exception as e:
		print(str(e))
		await client.say("Error Occured")
		
@client.event
async def on_ready():
    await client.change_presence(game=Game(name="Basketball"))
    print("Logged in as " + client.user.name)

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)

async def liveticker():
	await client.wait_until_ready()
	channel = discord.Object(id="433334140868493333")
	while not client.is_closed:
		awaitingmessage = espnscrape.ScoreTickBuilder()
		if awaitingmessage != '':
			await client.send_message(channel,espnscrape.ScoreTickBuilder())
		await asyncio.sleep(30)


client.loop.create_task(list_servers())
client.loop.create_task(liveticker())
client.run(TOKEN)