"""
Faire une FAQ pour lui poser des questions au lieu de la documentation
"""
import discord
from discord.ext import commands
from discord.ext.commands.cog import Cog


class Faq(Cog):
    """
    FAQ Category
    """

    def __init__(self, bot):
        self.bot = bot

    # todo FAQ

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Faq")


def setup(bot):
    bot.add_cog(Faq(bot))
