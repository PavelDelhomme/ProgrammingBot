import textwrap

import discord
from discord.ext import commands
from discord.ext.commands import Cog
import io
import contextlib

from utils.utils import clean_code, Pag


class EvalCode(commands.Cog):
    """
    Evaluate some code #In python...
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="eval", aliases=["exec"])
    @commands.is_owner()
    async def _eval(self, ctx, *, code):
        """Command to evaluate some code... in python"""
        code = clean_code(code)
        self.local_variables = {
                "discord" : discord,
                "commands": commands,
                "bot"     : self.bot,
                "ctx"     : ctx,
                "channel" : ctx.channel,
                "author"  : ctx.author,
                "guild"   : ctx.guild,
                "message" : ctx.message
        }

        stdout = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                        f"async def func():\n{textwrap.indent(code, '    ')}", self.local_variables,
                )

                obj = await self.local_variables["func"]()
                result = f"{stdout.getvalue()}\n-- {obj}\n"
        except Exception as e:
            result = f"{e} {e.__traceback__}"

        pager = Pag(
                timeout=100,
                entries=[result[i: i + 2000] for i in range(0, len(result), 2000)],
                length=1,
                prefix="+++py\n",
                suffix="+++"
        )
        print("title : ", pager.title)
        print("page  : ", pager.page)
        print("format : ", pager.format)
        print("length : ", pager.length)
        print("pager : ", pager)

        await pager.start(ctx)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("EvalCode")


def setup(bot):
    bot.add_cog(EvalCode(bot))
