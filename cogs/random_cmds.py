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


class Cmds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def echo(self, ctx, *, left):
        message = left
        await ctx.message.delete()
        await ctx.send(message)
    @commands.command()
    async def ts(self, ctx, *, left):
        message = left
        await ctx.message.delete()
        await ctx.send(message, tts=True)


async def setup(client):
    await client.add_cog(Cmds(client))