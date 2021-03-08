from io import BytesIO
from random import choice
from typing import Optional
import random

import discord
from discord.ext import commands
from discord.ext.commands import command, Cog
from discord.ext.commands.errors import MissingRequiredArgument
from discord.mentions import default
from discord.ext.commands import cooldown, BadArgument, BucketType
from discord import Intents

from utils.utils import text_to_owo, notify_user


class Basic(commands.Cog):
    """
    Group all of the basic commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="del",
                      usage="del {number of messages}",
                      description="Delete some message/s"
                                  " del {number of messages}",
                      brief="Delete mesage with argument the number of message")
    async def delete(self, ctx, number_of_message: int):
        """
        Delete some message/s
        """
        try:
            messages = await ctx.channel.history(limit=number_of_message + 1).flatten()
            for each_message in messages:
                await each_message.delete()
            # if discord.ext.commands.errors.MissingRequiredArgument:
            #    await ctx.channel.send("An argument was missing..."
            #                           "Please type do help del for more informations")
            #    await ctx.channel.history(limit=1).flatten()
        except ValueError as e:
            await ctx.channel.send(f"{e}")
        except BadArgument as e:
            await ctx.channel.send(f"{e}")
        except ConnectionError:
            await ctx.channel.send("An error has been occured, wait few seconds or retry later...")

    @commands.command(name="owo",
                      usage="owo {text_to_transform}",
                      description="Convert text to OwO"
                                  "owo {text to transform}",
                      brief="Convert text in OwO")
    async def owo(self, ctx):
        """
        Convert your text in owo format like that
        do owo hello
        hewwo
        """
        link = await ctx.channel.create_invite(max_age=1)
        await ctx.send(text_to_owo(ctx.message.content[7:]))
        await ctx.send(link)

    # todo faire fonctionner le invite
    @commands.command(name="invite",
                      usage="invite {@user_name}",
                      description="Create an invite to join this server",
                      brief="create invite to join this server")
    @commands.guild_only()
    async def invite(self, ctx, member: discord.Member = None):
        """
        Send an invite in private message of this user
        """
        if member is not None:
            link = await ctx.channel.create_invite(max_age=1)
            message = f"{ctx.author.name} invite your to {discord.Member.display_name}"
            await notify_user(member, message)
        else:
            await ctx.send("Please use @mention to poke someone")

    # todo faire fonctionner le roles
    @commands.command(name="roles",
                      usage="roles",
                      description="Shows every rolls present on this server",
                      brief="Show rolls")
    @commands.guild_only()
    async def roles(self, ctx):
        """ Get all roles in current server """
        allroles = ""

        for num, role in enumerate(sorted(ctx.guild.roles, reverse=True), start=1):
            allroles += f"[{str(num).zfill(2)}] {role.id}\t{role.name}\t[ Users: {len(role.members)} ]\r\n"
        print(allroles)

        data = BytesIO(allroles.encode('utf-8'))
        await ctx.send(allroles)
        # await ctx.send(content=f"Roles in **{ctx.guild.name}**",
        #               file=discord.File(data, filename=f"{default.timetext('Roles')}"))

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Basics")


def setup(bot):
    bot.add_cog(Basic(bot))
