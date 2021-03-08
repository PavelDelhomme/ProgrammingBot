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


class Discute(Cog):
    """
    All command relative to the bot and others...
    """

    def __init__(self, bot):
        self.bot = bot

    @command(name="hello", aliases=["hi"],
             usage="",
             description="Send hello from the bot",
             brief="")
    async def say_hello(self, ctx):
        """Says hello from the bot"""
        await ctx.send(f"{choice(('Hello', 'Hi', 'Hey', 'Hiya'))} {ctx.author.mention}!")

    @commands.is_owner()
    @command(name="slap", aliases=["hit"],
             usage="",
             description="Slap member",
             brief="Send {author} slapped {slapped member} {reason}")
    async def slap_member(self, ctx, member: discord.Member, *, reason: Optional[str] = "for no reason"):
        """ Slap a member """
        await ctx.send(f"{ctx.author.display_name} slapped {member.mention} {reason} !")

    @slap_member.error
    async def slap_member_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send("I can't find that member.")

    @commands.command(name="no")
    async def no(self, ctx, number_no: int):
        no = "NO ! "
        nos = str(number_no * no)
        await ctx.send(f"{nos} !")

    @commands.command(name="ideedemerde")
    async def idee_de_merde(self, ctx, member: discord.Member):
        "Envoie que c'est une idée de merde à un membre"
        idees_de_merde = [f"{member.mention}, je pense que c'est une idée de merde",
                          f"{member.mention}, non c'est de la merde",
                          f"c'est vraiment naze {member.mention}",
                          f"{member.mention} comment tu as pu pondre un truc pareil ??",
                          f"{member.mention}, t'es vraiment aussi nul pour proposer une idée pareil ?!"]
        random_idee = random.choice(idees_de_merde)
        await ctx.send(random_idee)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Discute")


def setup(bot):
    bot.add_cog(Discute(bot))
