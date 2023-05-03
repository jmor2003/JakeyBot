import discord
import time
import os
from discord.ext import commands
from discord.utils import get
from discord.ext import commands
from discord.ext import tasks
import requests
import bs4
import json
from discord.ext.commands import has_permissions
from itertools import cycle

from discord import TextChannel
from yt_dlp import YoutubeDL
import random

import asyncpraw

class Rocket_League(commands.Cog):

    def __init__(self, client):
        self.client = client





    @commands.command()
    async def price(self, ctx, left: str, right=None):
        '''
        *Put in ;price item and an (optional) color, also use _ to fill spaces in names for example "poly_pop" or "sky_blue*
        '''

        if left.lower() == "fireworks":
            left = "fireworks_goal_explosion"
        elif left.lower() == "shattered":
            left = "shattered_goal_explosion"
        elif left.lower() == "reaper":
            left = "reaper_goal_explosion"
        elif right == "sky_blue":
            right = "sblue"

        if right == None:
            site = requests.get(f"https://rl.insider.gg/en/pc/{left.lower()}")
        else:
            site = requests.get(f"https://rl.insider.gg/en/pc/{left.lower()}/{right}")

        check = requests.get(f"https://rl.insider.gg/en/pc/{left.lower()}")
        soup_check = bs4.BeautifulSoup(check.text, "html.parser")
        dark = soup_check.find(id="graph")
        if left == "dominus":
            soup = bs4.BeautifulSoup(site.text, "html.parser")
            nums = soup.find_all("td")
            nums = list(nums)
            tracker = 0
            pc = nums[6]
            ps4 = nums[7]
            xbox = nums[8]
            switch = nums[9]
            if len(str(pc)) > 50:
                await ctx.send(
                    f"{left} is **not** a valid option, you may have mispelled it or it doesn't have a colored option please try again.")
            else:
                await ctx.send(
                    f"`The price on **PC** is: {pc.text}\n price on **playstation** is: {ps4.text}\n price on **xbox** is: {xbox.text}\n price on **switch** is: {switch.text}")

        elif dark == None:
            soup = bs4.BeautifulSoup(site.text, "html.parser")
            nums = soup.find_all("td")
            nums = list(nums)
            pc = nums[11]
            ps4 = nums[12]
            xbox = nums[13]
            switch = nums[14]
            if len(str(pc)) > 50:
                embed4 = discord.Embed(description=f"{left} is **not** a valid option, you may have mispelled it or it doesn't have a colored option please try again.", colour=discord.Colour.dark_blue())

                await ctx.send(embed=embed4)
            else:
                embed3 = discord.Embed(description=f"The price on **PC** is: {pc.text}\n price on **playstation** is: {ps4.text}\n price on **xbox** is: {xbox.text}\n price on **switch** is: {switch.text}", colour=discord.Colour.dark_blue())
                await ctx.send(embed=embed3)


        else:
            soup = bs4.BeautifulSoup(site.text, "html.parser")
            nums = soup.find_all("td")
            nums = list(nums)
            pc = nums[16]
            ps4 = nums[17]
            xbox = nums[18]
            switch = nums[19]
            if len(str(pc)) > 50:
                embed1 = discord.Embed(description=f"{left} is **not** a valid option, you may have mispelled it or it doesn't have a colored option please try again.", colour=discord.Colour.dark_blue())

                await ctx.send(embed=embed1)
            else:
                embed2 = discord.Embed(description=f"The price on **PC** is: {pc.text}\n price on **playstation** is: {ps4.text}\n price on **xbox** is: {xbox.text}\n price on **switch** is: {switch.text}", colour=discord.Colour.dark_blue())

                await ctx.send(embed=embed2)


async def setup(client):
    await client.add_cog(Rocket_League(client))