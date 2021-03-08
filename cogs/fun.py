import random
from random import choice, randint
from typing import Optional

import discord
from discord import Member
from discord.ext import commands
from discord.ext.commands import cooldown, BadArgument, BucketType
from discord.ext.commands.errors import CommandOnCooldown, CommandInvokeError
from discord.ext.commands import command, Cog


class Fun(commands.Cog):
    """
    Some commands to have fun
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dice",
                      aliases=["roll"],
                      usage="",
                      description="something")
    # @cooldown(1, 10, BucketType.user)
    async def roll_dice(self, ctx, die_string: str):
        """
            Return
        """
        dice, value = (int(term) for term in die_string.split("d"))
        try:
            if dice <= 1000000:
                rolls = [random.randint(1, value) for i in range(dice)]
                await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")

            else:
                await ctx.send("I can't roll that many dice. Please try a lower number.")
        except discord.ext.commands.errors.CommandOnCooldown as e:
            await ctx.send(e)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Fun")


def setup(bot):
    bot.add_cog(Fun(bot))
