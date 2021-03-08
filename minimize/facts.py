"""from random import choice, randint
from typing import Optional

from aiohttp import request

import discord
from discord import Member, Embed
from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command, cooldown
from discord.ext.commands.errors import BadArgument
from discord.ext import commands
from discord.ext.commands import cooldown, BadArgument, BucketType
from discord.ext.commands.errors import CommandOnCooldown, CommandInvokeError


class Facts(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="")
    async def nothing(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Facts(bot))
"""