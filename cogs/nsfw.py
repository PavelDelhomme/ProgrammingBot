from discord.ext import commands
import discord
from discord.ext.commands import Cog

from utils.utils import get_momma_jokes


class NSFW(commands.Cog):
    """
    NSFW categorie
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="insult",
                      description="Launch some random insults",
                      brief="This command can launch some insults")
    async def insult(self, ctx, member: discord.Member = None):
        try:
            insults = await get_momma_jokes()
            if member is not None:
                await ctx.send(f"{member.name} eat this: {insults}")
            else:
                await ctx.send(f"{ctx.message.author.name} for yourself: {insults}")
        except IndexError:
            await ctx.send("No insults available, please contact your administrator or retry later")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("NSFW")


def setup(bot):
    bot.add_cog(NSFW(bot))
