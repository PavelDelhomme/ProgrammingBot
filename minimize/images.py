"""import random

import aiohttp
import discord
import praw
import urllib3
from discord.ext import commands
from discord.ext.commands.errors import CommandInvokeError

from settings_files._global import REDDIT_APP_ID, REDDIT_APP_SECRET, REDDIT_ENABLE_MEME_SUBREDDITS


class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = None
        if REDDIT_APP_ID and REDDIT_APP_SECRET:
            self.reddit = praw.Reddit(client_id=REDDIT_APP_SECRET, client_secret=REDDIT_APP_SECRET,
                                      user_agent=f"DevIA:{REDDIT_APP_ID}:1.0")
        print(REDDIT_APP_SECRET, REDDIT_ENABLE_MEME_SUBREDDITS, REDDIT_APP_ID)

    @commands.command(name="random",
                      usage="Write some usages",
                      brief="Show random something but it isn't work for now")
    async def random(self, ctx, subreddit: str = ""):
        async with ctx.channel.typing():
            try:
                if self.reddit:
                    # start working
                    chosen_subreddit = REDDIT_ENABLE_MEME_SUBREDDITS[0]
                    if subreddit:
                        # should take default one
                        if subreddit in REDDIT_ENABLE_MEME_SUBREDDITS:
                            chosen_subreddit = subreddit
                        else:
                            await ctx.send("Please choose a subreddit of the following list: %s" % ", ".join(
                                REDDIT_ENABLE_MEME_SUBREDDITS))
                            return

                    submissions = self.reddit.subreddit(chosen_subreddit).hot()

                    post_to_pick = random.randint(1, 10)
                    for i in range(0, post_to_pick):
                        submissions = next(x for x in submissions if not x.stickied)
                    await ctx.send(submissions.url)

                else:
                    await ctx.send("This is not working. Contact Administrator.")
            except urllib3.util.retry.MaxRetryError or Exception:
                await ctx.send("This is not working.")

    @commands.group(name="Images")
    async def images(self):
        pass
""""""
    @commands.command(name="cat",
                      usage="Write some usages",
                      description="Show random images of cats",
                      brief="Show random images of cats...")
    async def cat(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://aws.random.cat/meow") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Meow")
                    embed.set_image(url=data['file'])
                    embed.set_footer(text="https://random.cat/")

                    await ctx.send(embed=embed)

    @commands.command(name="dog",
                      usage="Write some usages",
                      description="Show random images of dogs",
                      brief="Show random images of dogs...")
    async def dog(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://random.dog/woof.json") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Woof")
                    embed.set_image(url=data['url'])
                    embed.set_footer(text="https://random.dog/")

                    await ctx.send(embed=embed)

    @commands.command(name="fox",
                      usage="Write some usages",
                      description="Show random images of foxs",
                      brief="Show random images of foxs...")
    async def fox(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://randomfox.ca/floof/") as r:
                    data = await r.json()

                    embed = discord.Embed(title="Floof")
                    embed.set_image(url=data['image'])
                    embed.set_footer(text="https://randomfox.ca/")

                    await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Images(bot))
"""