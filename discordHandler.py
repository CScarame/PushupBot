###################
# discordHandler.py
# Author: Sc4ry
# Function:
# adds discordHandler class, which we will use to run operate
#   all of the discord stuff
#
# The config file must include the following variables in JSON form
#   COMMAND_PREFIX - Prefix that must be in front of all commands
#   DISCORD_TOKEN - Private token that is used to log in to discord
#
#
###################
import discord
from discord.ext import commands

import os, sys, json, asyncio

class discordHandler:
    def __init__(self,token_filename, config_filename, cog_foldername):
        self.import_token(token_filename) # Read in discord token
        self.import_config(config_filename) # Read in important variables
        bot = commands.Bot(command_prefix=self.prefix) # Create bot and set prefix
        @bot.event
        async def on_ready():
            print("Logging in as {0.name} : {0.id}".format(bot.user))
            for file in os.listdir(cog_foldername):
                if file[-3:] == ".py":
                    print("Loading {}".format(file))
                    file_name = file[:-3]
                    cog_name = ".".join(["Cogs",file_name])
                    bot.load_extension(cog_name)
        @bot.event
        async def on_command(ctx):
            print("Received |{0.command.name}| command from |{0.message.author.name}|".format(ctx))
        self.bot = bot
    def run(self):
        self.bot.run(self.token)
    def import_token(self,token_filename):
        with open(token_filename, 'r') as token_file:
            config = json.load(token_file)
        self.token = config['token']
    def import_config(self,config_filename):
        with open(config_filename, 'r') as config_file:
            config = json.load(config_file)
        self.prefix = config['prefix']

if __name__ == "__main__":
    D = discordHandler("config/discord-token.json", "config/discord.json","Cogs")
    D.run()



