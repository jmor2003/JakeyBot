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

with open("cogs/api_key.json", "r") as f:
    api_key = json.load(f)


class Weather(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def fahr(self, ctx, left: int):
        ''' * Will
        put
        a
        temp in Fahrenheit
        into
        Celsius * '''

        await ctx.send(f"{(left - 32) * 5 / 9} ° Celsius")


    @commands.command()
    async def cel(self, ctx, left: int):


        await ctx.send(f"{(left * 9 / 5) + 32} ° Fahrenheit")

    @commands.command(aliases=["temp"])
    async def weather(self, ctx, city: str, country: str = None):
        '''

        :param
        city:
        or
        :param
        country:
        :return: the
        weather
        '''

        req = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&units=imperial&appid={api_key['api_key']}")
        json_data = req.json()
        weather = json_data["weather"][0]["main"]
        description = json_data["weather"][0]["description"]
        temp = json_data["main"]["temp"]
        feels_like = json_data["main"]["feels_like"]
        humidity = json_data["main"]["humidity"]
        wind = json_data["wind"]["speed"]

        embed = discord.Embed(title="Weather", description=f"Here's the weather for {city.upper()}",
                              colour=discord.Colour.dark_blue())
        embed.set_thumbnail(url="https://weather.thefuntimesguide.com/files/funny-weatherman.jpg")
        embed.add_field(name="Weather", value=f"`{weather}`", inline=True)
        embed.add_field(name="Description", value=f"`{description}`", inline=True)
        embed.add_field(name="Temperature", value=f"`{temp}°f`", inline=True)
        embed.add_field(name="Real Feel", value=f"`{feels_like}°f`", inline=True)
        embed.add_field(name="Humidity", value=f"`{humidity}`", inline=True)
        embed.add_field(name="Wind", value=f"`{wind} knots`", inline=True)

        await(ctx.send(embed=embed))

    @weather.error
    async def weather_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"{error} That is not a valid city, or country code.")



async def setup(client):
    await client.add_cog(Weather(client))