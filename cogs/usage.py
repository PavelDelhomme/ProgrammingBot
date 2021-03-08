import random

import discord
from discord.ext import commands
from discord.ext.commands import Cog

from utils.utils import Pag


class Usage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        if await self.bot.command_usage.find(ctx.command.qualified_name) is None:
            await self.bot.command_usage.upsert(
                    {"_id": ctx.command.qualified_name, "usage_count": 1}
            )
        else:
            await self.bot.command_usage.increment(
                    ctx.command.qualified_name, 1, "usage_count"
            )

    @commands.command(
            name=
    )
    """

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Usage")


def setup(bot):
    bot.add_cog(Usage(bot))
