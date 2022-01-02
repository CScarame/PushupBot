#############
## PushupTracker.py
## Author: Chris Scaramella
## Date: 1/1/2022
#############
## This cog has all of the main commands for the Pushup Tracking
#############

import discord
from discord.ext import commands

import json
import googleHandler
import datetime


def setup(bot):
    bot.add_cog(PushupTracker(bot))

class PushupTracker(commands.Cog):
    def __init__(self, bot):
        self.G = googleHandler.googleHandler("1K9dj5yqQDW7MjXK1J01U-WiVTSJtIns_YHG_s1Shp_U")
        self.bot = bot

    @commands.command(help="Test Command")
    async def test(self,ctx):
        await ctx.send(ctx.author.id)

    @commands.command(help="Track some pushups")
    async def track(self, ctx, *, number):
        self.G.append("RawData!A:C", [[datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S"), "Pushups", number]])
        total = self.G.read("Daily Totals!B2")
        await ctx.send(f"Added {number} pushups.\nYou have done a total of {total} pushups today.")