import discord
from discord.ext import commands
import asyncio
import json


class Workout(commands.Cog):
    def __init__(self, client):
        self.client = client = client

    @commands.command(aliases=["bench"])
    async def benchpress(self, client, weight):
        user = self.client.user.id
        print(user)




async def setup(client):
    await client.add_cog(Workout(client))


