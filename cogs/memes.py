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

all_subs = []
holder = []
reddit = asyncpraw.Reddit(client_id='aFq56E4QjpUYNvcR1c8HjQ',
                              client_secret='2BPx-Kx_Di3UEVXfBZvUNhtb_NhCMg',
                              sername='Subject_Tadpole641',
                              password='Trader26!',
                              user_agent='Jakeyy Bot')

status = cycle([";help"])



async def gen_memes():
    '''

    Always
    gens
    new
    memes
    '''

    subreddit = await reddit.subreddit("memes")
    top = subreddit.top(limit=1000)
    async for submission in top:
        all_subs.append(submission)


class Memes(commands.Cog):
    def __init__(self, client):
        self.client = client

    @tasks.loop(seconds=30)
    async def change_status(self):
            '''
            This is a
            silent
            function
            that
            changes
            Jakeyy_bot
            's statuses
            '''

            await self.client.change_presence(activity=discord.Game(next(status)))

    @commands.Cog.listener()
    async def on_ready(self):
        '''
        Turns
        the
        bot
        on
        :return:
        '''

        print("Bot Online")
        self.change_status.start()
        await gen_memes()
        try:
            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    holder.append(file)
                    os.remove(holder[0])
        except:
            pass

    @commands.command(aliases=['memes'])
    async def meme(self, ctx):
        '''
        Sends
        the
        meme
        '''


        random_sub = random.choice(all_subs)
        all_subs.remove(random_sub)
        name = random_sub.title
        url = random_sub.url
        ups = random_sub.score
        link = random_sub.permalink
        comments = random_sub.num_comments
        embed = discord.Embed(title=name, url=f"https://reddit.com{link}", color=ctx.author.color)
        embed.set_image(url=url)
        embed.set_footer(text=f"👍{ups} 💬{comments}")
        await ctx.send(embed=embed)

        if len(all_subs) <= 20:  # meme collection running out owo
            await gen_memes()
    @commands.command()
    async def meme_refresh(self, ctx):
        all_subs.clear()
        subreddit = await reddit.subreddit("memes")
        top = subreddit.top(limit=1000)
        async for submission in top:
            all_subs.append(submission)
        await ctx.send("Memes Refreshed.")





async def setup(client):
    await client.add_cog(Memes(client))