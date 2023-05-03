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
import asyncio
from discord import TextChannel
from yt_dlp import YoutubeDL
import random

import asyncpraw


intents = discord.Intents.all()

client = commands.Bot(command_prefix=';', intents=intents)


@client.command()
async def load(ctx, extension):
    if ctx.message.author.id == 800608160124764182:
        try:
            
            await client.load_extension(f"cogs.{extension}")
            await ctx.send(f"{extension} loaded")
        except:
            await ctx.send("That branch either doesn't exist or has already been loaded")
    else:
        pass
    


@client.command()
async def unload(ctx, extension):
    if ctx.message.author.id == 800608160124764182:
        try:
            await client.unload_extension(f"cogs.{extension}")
            await ctx.send(f"{extension} unloaded")
        except:
            await ctx.send("That branch either doesn't exist or has already been unloaded")
    else:
        pass
        
    

'''
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")
        '''

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await client.load_extension(f"cogs.{filename[:-3]}")
            print(f"cogs.{filename[:-3]} loaded")


@client.command(aliases=["speed"])
async def ping(ctx):
    '''
    *Will
    return your
    ping *
    '''
    await ctx.send(f"Pong {client.latency * 1000}ms")





@client.command()
async def servers(ctx):
    counter = 0
    checkk = []
    messages = []
    activeservers = client.guilds
    await ctx.send("This command is for the **bot owner**, the only output is in the console logs.")
    for guild in activeservers:
        print(guild.name)
'''
    for servers in activeservers:
        for channels in servers.channels:
            checkk.append(channels)
    for i in checkk:
        messages = await i.history(limit = 1).flatten() 
        for o in messages:
            print(o)
           '''


            







@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        '''
    This
    activates if a
    command is used
    that
    doesn
    't exist
    '''
        await ctx.send("That is an invalid command, please try again or use ;help for more information.")

async def main():
    async with client:
        await load_extensions()
        await client.start('')

asyncio.run(main())





