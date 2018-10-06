import random
import asyncio
import requests
from credentials_discord import TOKEN, CHANNEL_ID
import discord
from discord import Game
from discord.ext.commands import Bot
import espnscrape
import pickle

BOT_PREFIX = ("?", "!")

teams_full = {"Toronto","Boston","Philadelphia","Cleveland","Indiana","Miami","Milwaukee","Washington","Detroit","Charlotte","New-York","Brooklyn","Chicago","Orlando","Atlanta","Houston","Golden State","Portland","Utah","New Orleans","San Antonio","Oklahoma City","Minnesota","Denver","LA","Los Angeles","Sacramento","Dallas","Memphis","Phoenix"}
teams_short = {"TOR","BOS","PHI","CLE","IND","MIA","MIL","WSH","DET","CHA","NY","BKN","CHI","ORL","ATL","HOU","GS","POR","UTAH","NO","SA","OKC","MIN","DEN","LAC","LAL","SAC","DAL","MEM","PHX"}
teams = teams_full.union(teams_short)

avaliable_roles = ["Game Night"]
cbbid = "363172066431598595"

client = Bot(command_prefix=BOT_PREFIX)

########################################
# Score Bot Commands
# cinciforthewin
# Last Updated: 10/6/18 by Grubberbeb
########################################

@client.command()
async def allgames():
    try:
        allGamesString = ''
        for game in espnscrape.scrapeESPN(0):
            allGamesString += buildGameString(game) + '\n'
        await client.say(allGamesString)
    except Exception as e:
        print(str(e))
        await client.say("Error Occured")

@client.command()
async def score(*,team:str):
    try:
        if team in teams:
            await client.say(buildScoreString(team))
        else:
            await client.say("Can't Find Team")
            print("Can't Find Team")
    except Exception as e:
        print(str(e))
        await client.say("Error Occured")

@client.command()
async def schedule(*,team:str):
    try:
        if team in teams:
            scheduleString = buildScheduleString(team)
            await client.say('Basketball Schedule for ' + team + ':\n' + scheduleString)
        else:
            await client.say("Can't Find Team")
            print("Can't Find Team")
    except Exception as e:
        print(str(e))
        await client.say("Error Occured")

def gameTeams(game):
    return {game['team1'], game['team2'], game['team1abv'], game['team2abv']}

def buildGameString(game):
    return game['team2'] + " " + str(game['score2']) + " @ " + game['team1'] + " " + str(game['score1']) + " - " + game['time'] + " (TV: " + game['network'] + ")"

def buildScoreString(team):
    allgames = espnscrape.scrapeESPN(0)
    for game in allgames:
        if team in gameTeams(game):
            gamestring = buildGameString(game)
            print(gamestring)
            return gamestring

    scheduleString = buildScheduleString(team, includeToday=False)
    return "There are currently no games scheduled for " + team + " today.\n" + scheduleString

def buildScheduleString(team, includeToday=True):
    scheduleString = '**Past Games:**\n'
    for n in range(-7, 8):
        if n == 0:
            if includeToday:
                scheduleString += "**Today's Game:**\n"
            else:
                continue
        if n == 1:
            scheduleString += '**Future Games:**\n'

        allGamesOnDay = getAllGamesOnDay(n)
        for game in allGamesOnDay:
            if team in gameTeams(game):
                gamestring = buildGameString(game)
                scheduleString += gamestring + '\n'
                print(gamestring)
                break
    return scheduleString

def getAllGamesOnDay(n):
    if n == 0:
        return espnscrape.scrapeESPN(0)
    else:
        with open('discordscorebot/' + str(n) + '.pk1', 'rb') as dayCache:
            return pickle.load(dayCache)

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
    channel = discord.Object(id=CHANNEL_ID)
    while not client.is_closed:
        try:
            await client.send_message(channel,espnscrape.ScoreTickBuilder())
            await asyncio.sleep(30)
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            await asyncio.sleep(30)
            continue

########################################
# Assign Role
# By cinciforthewin
# Last Updated: 4/29/18
########################################

@client.command(pass_context=True)
async def addrole(ctx,*,req_role:str):
    if req_role not in avaliable_roles:
        sendstr = "The Role requested is not available to add or remove.  These roles are currently available:\n"
        for a_role in avaliable_roles:
            sendstr = sendstr + "* " + a_role + "\n"
        await client.say(sendstr)
    else:
        for server in client.servers:
            if server.id == cbbid:
                role = discord.utils.get(server.roles,name=req_role)
                await client.add_roles(ctx.message.author,role)
                await client.say(ctx.message.author.name + " added to the " + req_role + " role.")

@client.command(pass_context=True)
async def removerole(ctx,*,req_role:str):
    if req_role not in avaliable_roles:
        sendstr = "The Role requested is not available to add or remove.  These roles are currently available:\n"
        for a_role in avaliable_roles:
            sendstr = sendstr + "* " + a_role + "\n"
        await client.say(sendstr)
    else:
        for server in client.servers:
            if server.id == cbbid:
                role = discord.utils.get(server.roles,name=req_role)
                await client.remove_roles(ctx.message.author,role)
                await client.say(ctx.message.author.name + " removed from the " + req_role + " role.")

client.loop.create_task(list_servers())
client.loop.create_task(liveticker())
client.run(TOKEN)
