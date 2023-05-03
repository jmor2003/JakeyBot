import asyncio

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







class Help_cmd(commands.Cog):
    def __init__(self, client):
        self.client = client
        client.remove_command("help")


    @commands.command()
    async def help(self, ctx, left=None):

        print("Hello!")
        embed2 = discord.Embed(title="Jakeyy_Bot", description="List of all bot music commands below",colour=discord.Colour.dark_blue())
        embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/815750939679260712/930961948290457660/jakeybot.jpg")
        embed2.add_field(name=";play [name of the song you like] or [link to a youtube playlist]", value="`Will play the song or youtube playlist of your liking.`", inline=False)
        embed2.add_field(name=";pause", value="`Will pause the music.`", inline=False)
        embed2.add_field(name=";queue", value="`Display the queue. You can use the arrow keys to go to diffrent pages.`", inline=False)
        embed2.add_field(name=";resume", value="`Will resume the music.`", inline=False)
        embed2.add_field(name=";stop",value="`Will stop the music and clear the queue, I recommend using this when you're getting weird errors it will reset things.`",inline=True)
        embed2.add_field(name=";skip", value="`Will skip to the next song`", inline=False)
        embed2.add_field(name=";remove [THE NUMBER OF SONG YOU WANT REMOVED]",value="`Will remove the chosen song from your queue, if you'd like to see where in the queue your song you want to remove is just do ;queue and see the numbers on the side.`",inline=False)
        embed2.add_field(name=";move [number of song you want to move] [place you want to move it to]", value="`Will let you move the order of songs around in the queue.`", inline=False)


       
        embed3 = discord.Embed(title="Jakeyy_Bot", description="List of all bot admin commands below",colour=discord.Colour.dark_blue())
        embed3.set_thumbnail(url="https://cdn.discordapp.com/attachments/815750939679260712/930961948290457660/jakeybot.jpg")
        embed3.add_field(name=";kick", value="`Will kick the listed user.`", inline=False)
        embed3.add_field(name=";ban", value="`Will ban the listed user.`", inline=False)
        embed3.add_field(name=";unban", value="`Will unban the listed user.`", inline=False)
        embed3.add_field(name=";clear",value="`Will clear a default of five messages, to clear more just specify a number`",inline=False)
        embed3.add_field(name=";mute [member] [time]",value="`Will allow you to mute a member for any amount of minutes, if you'd like to mute them until further notice don't put an amount of time just put the member`",inline=False)
        embed3.add_field(name=";unmute [member]",value="`Will allow you to unmute a member`",inline=False)
        
        embed4 = discord.Embed(title="Jakeyy_Bot", description="List of all bot fun commands below",colour=discord.Colour.dark_blue())
        embed4.set_thumbnail(url="https://cdn.discordapp.com/attachments/815750939679260712/930961948290457660/jakeybot.jpg")
        embed4.add_field(name=";echo", value="`Will make your message look like Jakey Bot sent it`", inline=False)
        embed4.add_field(name=";ts", value="`Will text to speech any message`", inline=False)
        embed4.add_field(name=";meme", value="`Will send a random top meme from r/meme.`", inline=False)
        embed4.add_field(name=";price [item name]",value="`Will show the price of any rocket league item, you can also put a color after the item name.`",inline=False)
        embed4.add_field(name=";ping", value="`Will return the ping of the bot.`", inline=False)


    
        embed1 = discord.Embed(title="Jakeyy_Bot", description="List of all bot command pages below",colour=discord.Colour.dark_blue())
        embed1.set_thumbnail(url="https://cdn.discordapp.com/attachments/815750939679260712/930961948290457660/jakeybot.jpg")
        embed1.add_field(name="Music Commands", value="`The music commands are on page 1.`",inline=False)
        embed1.add_field(name="Admin Commands", value="`Admin commands are on page 2`",inline=False)
        embed1.add_field(name="Fun Commands", value='`Fun commands are on page 3`', inline=False)
        embed1.add_field(name="Weather Commands", value='`All the weather commands are on page 4.`', inline=False)

        embed5 = discord.Embed(title="Jakeyy_Bot", description="List of all bot weather commands below",colour=discord.Colour.dark_blue())
        embed5.set_thumbnail(url="https://cdn.discordapp.com/attachments/815750939679260712/930961948290457660/jakeybot.jpg")
        embed5.add_field(name=";weather [City]", value="`Will return the weather conditions of the given area.`",inline=False)
        embed5.add_field(name=";fahr", value="`Will convert a temperature from Fahrenheit to Celsius.`", inline=False)
        
        embed5.add_field(name=";cel", value="`Will convert a temperature from Celsius to Fahrenheit.`", inline=False)
        embeds = [embed1, embed2, embed3, embed4, embed5]
        pages = len(embeds)
        

        cur_page = 1
        message = await ctx.send(embed=embeds[cur_page-1])
        
        await message.add_reaction("◀")
        await message.add_reaction("▶")
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀", "▶"]
            # This makes sure nobody except the command sender can interact with the "menu"
        while True:
            try:
                reaction, user = await self.client.wait_for("reaction_add", timeout=30, check=check)
                # waiting for a reaction to be added - times out after x seconds, 60 in this
                # example

                if str(reaction.emoji) == "▶" and cur_page != pages:
                    cur_page += 1
                    await message.edit(embed = embeds[cur_page-1])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀" and cur_page > 1:
                    cur_page -= 1
                    await message.edit(embed=embeds[cur_page - 1])
                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page
            except asyncio.TimeoutError:
                await message.delete()
                break
                # ending the loop if user doesn't react after x seconds




    @commands.Cog.listener()
    async def on_message(self, message):
        print(f"{message.author}: {message.content}")
        with open("general_content.txt", "a") as f:
                f.write(f"{message.author}: {message.content}\n")
        if self.client.user.mentioned_in(message):
            await message.add_reaction("👋")
        elif "uwu" in message.content.lower():
            await message.add_reaction("<:sus:861802630645022741>")
        elif "sus" in message.content.lower():
            await message.add_reaction("<a:RockSus:937020942679408660>")
        elif "jake" in message.content.lower():
            with open("me.txt", "a") as f:
                f.write(f"{message.author}: {message.content}\n")
        
async def setup(client):
    await client.add_cog(Help_cmd(client))