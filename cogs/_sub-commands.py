import discord.ext.commands
import discord
from discord.ext.commands import Cog
from discord.ext import commands


class Sub_Commands(Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Sub_Commands(bot))
