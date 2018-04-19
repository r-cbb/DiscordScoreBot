# discordscorebot

Install the required depedencies:

    pip install -r requirements.txt
	
Set up a discord channel by going here: https://support.discordapp.com/hc/en-us/articles/204849977-How-do-I-create-a-server-

Create a discord bot token by going here: https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token
Follow those instructions to add the bot to your channel. 

Add the App Bot User Token to credentials_discord.py (rename this from credentials_discord_example.py)

Get the channel id of the channel you wish for it to post live updates to.  An example on how to do that is here: 
https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-

(The bot will need to have access to be able to post here.  If not available, it will not work correctly.)

Add the channel id 

# nightlyreset.py

This runs the reset script.  It needs to run once a day.  Run this program first and it will create discordscorebot/gamelog.txt.   I suggest running this program once a day.  If possible, at 4 am EST. 

# discordscorebot.py

Run discordscorebot.py and let it run.  It will run continously till it breaks or you manually turn it off.  If run on a rasbperry pi, set up a crontab to run on reboot (with a delay) and it will run on reboot.


