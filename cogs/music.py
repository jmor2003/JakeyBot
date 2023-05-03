import discord
import yt_dlp
import ffmpeg
import asyncio
from youtube_search import YoutubeSearch
from discord import FFmpegPCMAudio
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
import pytube 
from pytube import YouTube, Playlist
import spotify_dl

#This is the specifications used to download the yt vids in play() command
ydl_opts = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(id)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch',
    'source_address': '0.0.0.0',
}

ffmpeg_optins = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

songs = {}
links = {}
q = {}


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["p"])
    async def play(self, ctx, *, song_title):
        '''

        :param ctx:
        :param left: song name
        :return: plays music
        '''

        global songs
        global links
        global q
        global ydl_opts
        try:
            print(q[ctx.guild.id])
        except:
            q[ctx.guild.id] = []
        try:
            print(songs[ctx.guild.id])
        except:
            songs[ctx.guild.id] = []
        try:
            print(links[ctx.guild.id])
        except:
            links[ctx.guild.id] = []
        self.song_title = song_title



        # Stuff for Joining channel
        channel = ctx.author.voice.channel
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice == None:
            await channel.connect()
            print("Connected")
            try:
                os.remove(songs[ctx.guild.id][0])
            except:
                pass
            songs[ctx.guild.id].clear()
            links[ctx.guild.id].clear()
            q[ctx.guild.id].clear()
        else:
            pass

        #fix if link has watch do no playlist
        if len(songs[ctx.guild.id]) > 0:

            if "playlist?list=" in song_title:
                await self.add_to_q_playlist(ctx)






            else:
                await self.add_to_q_song(ctx)


        else:
            if "playlist?list=" in song_title:
                await self.play_playlist(ctx)




            else:
                await self.normal_play(ctx)



    async def add_to_q_song(self, ctx):

        if "youtube.com" and "watch?" in self.song_title:
            links[ctx.guild.id].append(self.song_title)
            video = YouTube(self.song_title, use_oauth=True)
            title = video.title
            vid_id = video.video_id
            long = f"({video.length // 60} mins)"
            songs[ctx.guild.id].append(f"{vid_id}.webm")
            q[ctx.guild.id].append(f"{title} {long}")
            embed = discord.Embed(colour=discord.Colour.dark_green(),description=f'[{title}]({self.song_title}) added to the queue')
        else:
            results = YoutubeSearch(self.song_title, max_results=1).to_dict()  # IMPORTANT
            link = f"https://youtube.com{results[0]['url_suffix']}"
            links[ctx.guild.id].append(link)
            video = YouTube(link, use_oauth=True)
            title = video.title
            long = f"({video.length // 60} mins)"
            vid_id = video.video_id
            songs[ctx.guild.id].append(f"{vid_id}.webm")
            q[ctx.guild.id].append(f"{title} {long}")
            embed = discord.Embed(colour=discord.Colour.dark_green(),description=f'[{title}]({link}) added to the queue')
        await ctx.send(embed=embed)



    async def add_to_q_playlist(self, ctx):
        embed = discord.Embed(colour=discord.Colour.dark_green())
        holder = len(q[ctx.guild.id]) + 1
        play_list = Playlist(self.song_title)
        for i in play_list:
            title = YouTube(i, use_oauth=True).title
            vid_id = YouTube(i).video_id
            links[ctx.guild.id].append(i)
            q[ctx.guild.id].append(f"{title}")
            songs[ctx.guild.id].append(f"{vid_id}.webm")
            embed.add_field(name=f"{holder}.", value=f'[{title}]({i}) added to the queue', inline=False)
            holder += 1
        await ctx.send(embed=embed)




    async def play_playlist(self, ctx):
        
        play_list = Playlist(self.song_title)
        link = YouTube(play_list[0], use_oauth=True).watch_url
        title = YouTube(play_list[0]).title
        vid_id = YouTube(play_list[0]).video_id
        print(link, title, vid_id)
        links[ctx.guild.id].append(link)
        q[ctx.guild.id].append(f"{title}")
        songs[ctx.guild.id].append(f"{vid_id}.webm")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([links[ctx.guild.id][0]])
        server = ctx.message.guild
        voice = server.voice_client

        voice.play(discord.FFmpegPCMAudio(songs[ctx.guild.id][0]), after=lambda e: self.play_next(ctx))
        embed = discord.Embed(colour=discord.Colour.dark_blue(),description=f'Now playing [{q[ctx.guild.id][0]}]({links[ctx.guild.id][0]}),\n the other songs from the playlist were added to the queue.\n ***Just as a reminder the bot will leave after 10 minutes of inactivity***')
        await ctx.send(embed=embed)
        links[ctx.guild.id].pop(0)




        for i in play_list:
            try:
                title = YouTube(i, use_oauth=True).title
                vid_id = YouTube(i).video_id
                links[ctx.guild.id].append(i)
                q[ctx.guild.id].append(f"{title}")
                songs[ctx.guild.id].append(f"{vid_id}.webm")
            except:
                continue

        
        links[ctx.guild.id].pop(0)
        q[ctx.guild.id].pop(1)
        songs[ctx.guild.id].pop(1)
        
        






    async def normal_play(self, ctx):
        if "youtube.com" and "watch?" in self.song_title:
            links[ctx.guild.id].append(self.song_title)
            video = YouTube(self.song_title, use_oauth=True)
            title = video.title
            long = f"({video.length // 60} mins)"
            vid_id = video.video_id
            songs[ctx.guild.id].append(f"{vid_id}.webm")
            q[ctx.guild.id].append(title)
            show = f"{title} {long}"
            embed = discord.Embed(colour=discord.Colour.dark_blue(), description=f'Now playing [{show}]({self.song_title})\n *Just as a reminder the bot will leave after 10 minutes of inactivity*')
        else:
            results = YoutubeSearch(self.song_title, max_results=1).to_dict()  # IMPORTANT
            link = f"https://youtube.com{results[0]['url_suffix']}"
            links[ctx.guild.id].append(link)   
            video = YouTube(link, use_oauth=True)
            title = video.title   
            long = f"({video.length // 60} mins)"
            vid_id = video.video_id
            songs[ctx.guild.id].append(f"{vid_id}.webm")
            q[ctx.guild.id].append(title)
            show = f"{title} {long}"
            embed = discord.Embed(colour=discord.Colour.dark_blue(), description=f'Now playing [{show}]({link})\n *Just as a reminder the bot will leave after 10 minutes of inactivity*')



        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([links[ctx.guild.id][0]])



        server = ctx.message.guild
        voice = server.voice_client

        voice.play(discord.FFmpegPCMAudio(songs[ctx.guild.id][0]), after=lambda e: self.play_next(ctx))
        links[ctx.guild.id].pop(0)
        
        await ctx.send(embed=embed)

    def play_next(self, ctx):
        server = ctx.message.guild
        voice = server.voice_client
        global songs
        if len(links[ctx.guild.id]) == 0:
            q[ctx.guild.id].clear()
            os.remove(songs[ctx.guild.id][0])
            songs[ctx.guild.id].clear()



        else:

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:

                os.remove(songs[ctx.guild.id][0])
                ydl.download([links[ctx.guild.id][0]])

                links[ctx.guild.id].pop(0)
                songs[ctx.guild.id].pop(0)
                q[ctx.guild.id].pop(0)

                voice.play(discord.FFmpegPCMAudio(songs[ctx.guild.id][0]), after=lambda e: self.play_next(ctx))

    @commands.command()
    async def move(self, ctx, left, right):
        try:
            if int(right) == 0:
                right  = 2
            elif int(right) == 1:
                right = 2
            q[ctx.guild.id].insert(int(right)-1, q[ctx.guild.id].pop(int(left)-1))
            songs[ctx.guild.id].insert(int(right) - 1, songs[ctx.guild.id].pop(int(left) - 1))
            print(links[ctx.guild.id][int(left)-2])
            links[ctx.guild.id].insert(int(right) - 2, links[ctx.guild.id].pop(int(left) - 2))
            embed = discord.Embed(colour=discord.Colour.dark_blue(),description=f'Successfully moved **{q[ctx.guild.id][int(right)-1]}** to position **{int(right)}**')
            await ctx.send(embed=embed)

        except:
                await ctx.send("There was an error please make sure both of the positions you're using exist")

    @commands.command()
    async def skip(self, ctx):
        server = ctx.message.guild
        voice = server.voice_client
        voice.stop()
        if q[ctx.guild.id] == 0:
            q[ctx.guild.id].clear()
            os.remove(songs[ctx.guild.id][0])
            songs[ctx.guild.id].pop(0)
        else:
            embed = discord.Embed(name = None, description=f"Skipped **{q[ctx.guild.id][0]}**", colour=discord.Colour.dark_red())
            await ctx.send(embed=embed)
            await asyncio.sleep(3)

    @commands.command()
    async def pause(self, ctx):
        global q
        server = ctx.message.guild
        voice = server.voice_client
        if voice.is_playing():
            voice.pause()
            embed = discord.Embed(description=f"**{q[ctx.guild.id][0]}** is paused", colour=discord.Colour.dark_blue())
            await ctx.send(embed=embed)
        else:
            await ctx.send("The audio is not currently playing.")

    @commands.command()
    async def resume(self, ctx):
        server = ctx.message.guild
        voice = server.voice_client
        if voice.is_paused():
            voice.resume()
            embed = discord.Embed(description=f"Resumed **{q[ctx.guild.id][0]}**", colour=discord.Colour.dark_blue())
            await ctx.send(embed=embed)
        else:
            await ctx.send("The audio is not paused.")

    @commands.command()
    async def stop(self, ctx):
        global songs
        global links
        global q
        server = ctx.message.guild
        voice = server.voice_client
        links[ctx.guild.id].clear()
        q[ctx.guild.id].clear()
        voice.stop()
        await asyncio.sleep(1)

    @commands.command()
    async def leave(self, ctx):
        server = ctx.message.guild
        voice = server.voice_client
        voice.stop()
        links[ctx.guild.id].clear()
        await voice.disconnect()

    @commands.command()
    async def remove(self, ctx, number):
        global links
        global q
        global songs
        if int(number) <= 0:
            await ctx.send("You cannot use **zero or below**, please pick a different number.")
            return
        elif int(number) == 1:
            await ctx.send(
                "You cannot remove the song currently playing, if you don't wanna hear it anymore do **;skip or ;stop**.")
            return

        try:
            number = int(number)
            number -= 1
            q[ctx.guild.id].pop(int(number))
            songs[ctx.guild.id].pop(int(number))
            print(links)
            links[ctx.guild.id].pop(int(number - 1))
            await self.queue(ctx)


        except:
            await ctx.send("Your queue is either **empty** or the number is not a valid song in your queue.")

    @commands.command(aliases=["q"])
    async def queue(self, ctx):
        global q
        if len(q[ctx.guild.id]) == 0:
            await ctx.send("There are no songs in your queue.")
        else:
            too_much = False
            embeds = []
            if len(q[ctx.guild.id])+1 <= 10:
                embed1 = discord.Embed(title="Queue Page 1", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed1)
            elif len(q[ctx.guild.id])+1 <= 20:
                embed1 = discord.Embed(title="Queue Page 1", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed1)
                embed2 = discord.Embed(title="Queue Page 2", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed2)
            elif len(q[ctx.guild.id])+1 <= 30:
                embed1 = discord.Embed(title="Queue Page 1", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed1)
                embed2 = discord.Embed(title="Queue Page 2", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed2)
                embed3 = discord.Embed(title="Queue Page 3", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed3)
            elif len(q[ctx.guild.id])+1 <= 40:
                embed1 = discord.Embed(title="Queue Page 1", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed1)
                embed2 = discord.Embed(title="Queue Page 2", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed2)
                embed3 = discord.Embed(title="Queue Page 3", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed3)
                embed4 = discord.Embed(title="Queue Page 4", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed4)
            elif len(q[ctx.guild.id])+1 <= 50:
                embed1 = discord.Embed(title="Queue Page 1", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed1)
                embed2 = discord.Embed(title="Queue Page 2", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed2)
                embed3 = discord.Embed(title="Queue Page 3", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed3)
                embed4 = discord.Embed(title="Queue Page 4", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed4)
                embed5 = discord.Embed(title="Queue Page 5", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed5)
            elif len(q[ctx.guild.id])+1 <= 60:
                embed1 = discord.Embed(title="Queue Page 1", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed1)
                embed2 = discord.Embed(title="Queue Page 2", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed2)
                embed3 = discord.Embed(title="Queue Page 3", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed3)
                embed4 = discord.Embed(title="Queue Page 4", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed4)
                embed5 = discord.Embed(title="Queue Page 5", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed5)
                embed6 = discord.Embed(title="Queue Page 6", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed6)
            elif len(q[ctx.guild.id])+1 <= 70:
                embed1 = discord.Embed(title="Queue Page 1", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed1)
                embed2 = discord.Embed(title="Queue Page 2", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed2)
                embed3 = discord.Embed(title="Queue Page 3", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed3)
                embed4 = discord.Embed(title="Queue Page 4", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed4)
                embed5 = discord.Embed(title="Queue Page 5", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed5)
                embed6 = discord.Embed(title="Queue Page 6", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed6)
                embed7 = discord.Embed(title="Queue Page 7", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed7)
            elif len(q[ctx.guild.id])+1 <= 80:
                embed1 = discord.Embed(title="Queue Page 1", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed1)
                embed2 = discord.Embed(title="Queue Page 2", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed2)
                embed3 = discord.Embed(title="Queue Page 3", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed3)
                embed4 = discord.Embed(title="Queue Page 4", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed4)
                embed5 = discord.Embed(title="Queue Page 5", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed5)
                embed6 = discord.Embed(title="Queue Page 6", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed6)
                embed7 = discord.Embed(title="Queue Page 7", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed7)
                embed8 = discord.Embed(title="Queue Page 8", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed8)
            elif len(q[ctx.guild.id])+1 <= 90:
                embed1 = discord.Embed(title="Queue Page 1", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed1)
                embed2 = discord.Embed(title="Queue Page 2", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed2)
                embed3 = discord.Embed(title="Queue Page 3", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed3)
                embed4 = discord.Embed(title="Queue Page 4", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed4)
                embed5 = discord.Embed(title="Queue Page 5", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed5)
                embed6 = discord.Embed(title="Queue Page 6", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed6)
                embed7 = discord.Embed(title="Queue Page 7", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed7)
                embed8 = discord.Embed(title="Queue Page 8", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed8)
                embed9 = discord.Embed(title="Queue Page 9", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed9)
            elif len(q[ctx.guild.id])+1 <= 105:
                embed1 = discord.Embed(title="Queue Page 1", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed1)
                embed2 = discord.Embed(title="Queue Page 2", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed2)
                embed3 = discord.Embed(title="Queue Page 3", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed3)
                embed4 = discord.Embed(title="Queue Page 4", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed4)
                embed5 = discord.Embed(title="Queue Page 5", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed5)
                embed6 = discord.Embed(title="Queue Page 6", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed6)
                embed7 = discord.Embed(title="Queue Page 7", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed7)
                embed8 = discord.Embed(title="Queue Page 8", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed8)
                embed9 = discord.Embed(title="Queue Page 9", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed9)
                embed10 = discord.Embed(title="Queue Page 10", description="", colour=discord.Colour.dark_blue())
                embeds.append(embed10)

            holder = 1
            for i in q[ctx.guild.id]:
                if holder <= 10:
                    embed1.description += f"**{holder}.**  {i}\n"
                elif holder <= 20:
                    embed2.description += f"**{holder}.**  {i}\n"
                elif holder <= 30:
                    embed3.description += f"**{holder}.**  {i}\n"
                elif  holder <= 40:
                    embed4.description += f"**{holder}.**  {i}\n"
                elif holder <=50:
                    embed5.description += f"**{holder}.**  {i}\n"
                elif holder <= 60:
                    embed6.description += f"**{holder}.**  {i}\n"
                elif holder <= 70:
                    embed7.description += f"**{holder}.**  {i}\n"
                elif holder <= 80:
                    embed8.description += f"**{holder}.**  {i}\n"
                elif  holder <= 90:
                    embed9.description += f"**{holder}.**  {i}\n"
                elif holder <=100:
                    embed10.description += f"**{holder}.**  {i}\n"
                elif holder > 120:
                    too_much = True

                holder += 1
            if too_much == True:
                await ctx.send("You can not print out your queue if there are over 100 songs on it")
            else:
    
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

                   

    @commands.command()
    async def disconnect(self, ctx):
        server = ctx.message.guild
        voice = server.voice_client
        await voice.disconnect()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.id == self.client.user.id:
            return

        elif before.channel is None:
            voice = after.channel.guild.voice_client
            time = 0
            while True:
                await asyncio.sleep(1)
                time = time + 1
                if voice.is_playing() and not voice.is_paused():
                    time = 0
                if time == 600:
                    await voice.disconnect()
                if not voice.is_connected():
                    break

                    
            
    

    @disconnect.error
    async def disconnect_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("The bot must be in a voice channel to use this command.")
        elif isinstance(error, commands.MissingRole):
            await ctx.send("You do not have permission to use this command.")

    @remove.error
    async def remove_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            print(error)

        elif isinstance(error, commands.MissingRole):
            await ctx.send("You do not have permission to use this command.")

    @queue.error
    async def queue_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            print(error)

    @play.error
    async def play_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            if error == IndexError():
                pass
            else:
                await ctx.send("Error has occured, please be sure you're in a channel, if you used a playlist off youtube that none of the songs on the playlist are unavailable/hidden on the youtube website and that the playlist isn't empty.")
            print(f"{error} play error")
        elif isinstance(error, commands.MissingRole):
            await ctx.send("You do not have permission to use this command.")

    @skip.error
    async def skip_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            if error == IndexError:
                pass
            else:
                print(f"{error} skip error")

    @pause.error
    async def pause_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("The bot must be in a voice channel to use this command.")
            print(error)
        elif isinstance(error, commands.MissingRole):
            await ctx.send("You do not have permission to use this command.")

    @resume.error
    async def resume_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("The bot must be in a voice channel to use this command.")
        elif isinstance(error, commands.MissingRole):
            await ctx.send("You do not have permission to use this command.")

    @stop.error
    async def stop_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            print(f"{error} stop error")
        elif isinstance(error, commands.MissingRole):
            await ctx.send("You do not have permission to use this command.")

    @leave.error
    async def leave_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            print(f"{error} leave error")
        elif isinstance(error, commands.MissingRole):
            await ctx.send("You do not have permission to use this command.")



async def setup(client):
    await client.add_cog(Music(client))