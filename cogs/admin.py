import discord
from discord.ext import commands
import asyncio


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True, kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        '''
        *Can be used to kick users by admins*
        '''
        await member.kick(reason=reason)
        embed = discord.Embed(description=f"{member.mention} has been kicked for {reason}",
                              colour=discord.Colour.dark_blue())
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True, ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        '''
        *Can be used to ban users by admins*
        '''
        await member.ban(reason=reason)
        embed = discord.Embed(description=f"{member.mention} has been banned for {reason}",
                              colour=discord.Colour.dark_blue())
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True, ban_members=True)
    async def unban(self, ctx, *, member):
        '''
        *Can be used to unban users by admins,just type their name and discriminator, for example "joemama#9876"*
        '''
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed = discord.Embed(description=f"Unbanned {user.name}#{user.discriminator}",
                                      colour=discord.Colour.dark_blue())
                await ctx.send(embed=embed)
                return

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True, manage_messages=True)
    async def clear(self, ctx, amount=10):
        '''
        *Will clear any amount of messages just specify the number after, the default is 5*
        '''
        await ctx.channel.purge(limit=amount)

    @commands.command(pass_context=True)
    async def broadcast(self, ctx, *, msg):
        if ctx.message.author.id == 800608160124764182:
            for server in self.client.guilds:
                for channel in server.channels:
                    try:
                        if channel.name == "general":
                            embed = discord.Embed(title="Alert From Dev", description=f"{msg}",
                                                  colour=discord.Colour.dark_blue(), author="Jake")
                            await channel.send(embed=embed)

                    except Exception:
                        continue
                else:
                    continue

        else:
            pass

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member, duration=0):
        if duration == 0:
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            guild = ctx.guild
            if role not in guild.roles:
                perms = discord.Permissions(send_messages=False, speak=False)
                await guild.create_role(name="Muted", permissions=perms)
                await member.add_roles(role)
                embed = discord.Embed(description=f"Successfully created Muted role and assigned it to (**{member}**).", colour=discord.Colour.dark_blue())
                await ctx.send(embed=embed)
            else:
                await member.add_roles(role)
                embed = discord.Embed(description=f"Successfully muted (**{member}**)", colour=discord.Colour.dark_blue())
                await ctx.send(embed=embed)
        else:
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            guild = ctx.guild
            if role not in guild.roles:
                perms = discord.Permissions(send_messages=False, speak=False)
                await guild.create_role(name="Muted", permissions=perms)
                await member.add_roles(role)
                embed = discord.Embed(description=f"Successfully created Muted role and assigned it to (**{member}**) for {duration} minutes.",colour=discord.Colour.dark_blue())
                await ctx.send(embed=embed)
            else:
                await member.add_roles(role)
                embed = discord.Embed(description=f"Successfully muted (**{member}**) for {duration} minutes", colour=discord.Colour.dark_blue())
                await ctx.send(embed=embed)
            amount = int(duration) * 60
            try:
                await asyncio.sleep(amount)
                mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
                await member.remove_roles(mutedRole)
                await member.send(f"{member} you have unmuted from: - {ctx.guild.name}")
            except:
                pass

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(mutedRole)
        await member.send(f"{member} you have unmuted from: - {ctx.guild.name}")
        embed = discord.Embed(description=f"{member.mention} has been successfully unmuted", colour=discord.Colour.dark_blue())
        await ctx.send(embed=embed)




    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            print(error)
            await ctx.send("An error has occured please be sure the person is still muted or in the server.")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("You don't have permission to use this command.")
        elif isinstance(error, commands.CommandInvokeError):
            print(error)

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("That is not a valid member")

    @broadcast.error
    async def broadcast_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            print(error)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You don't have permission to use this command.")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You don't have permission to use this command.")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You don't have permission to use this command.")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You don't have permission to use this command.")


async def setup(client):
    await client.add_cog(Admin(client))
