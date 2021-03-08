from asyncio import sleep
from datetime import datetime
from glob import glob

import DiscordUtils
import discord
import os.path as path
from discord import DMChannel, Embed
from discord.ext.commands import Bot as BotBase, Context

from pretty_help import Navigation, PrettyHelp
from discord.ext import commands

from TOKEN import TOKEN

PREFIX = "do "
OWNER_IDS = [664535469622689837]
COGS = [path.split("\\")[-1][:-3] for path in glob("./cogs/*.py")]
print(COGS)
COGS = ["_sub-commands",
        "basics",
        "discute",
        "docs",
        "eval",
        "faq",
        "fun",
        "invites",
        "moderator",
        "nsfw",
        "usage",
        "images"]


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        for cog in COGS:
            setattr(self, cog, True)
            # print(f"{cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.cogs_ready = Ready()
        self.cogs_loaded = 0
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None

        self.welcome_channel = 799704924732653598
        self.goodby_channel = None

        # todo.. refaire le reste...
        self.nav = Navigation("", "👉")
        self.nav = Navigation("👎", "\U0001F44D")
        self.act_time = None
        self.Help_Command = PrettyHelp(active_time=self.act_time, navigation=self.nav,
                                       color=discord.colour.Colour.purple(), index_title="Help - Categories",
                                       show_hidden=True
                                       )

        self.tracker = DiscordUtils.InviteTracker(self)
        try:
            with open("./data/banlist.txt", "r", encoding="utf-8") as f:
                self.banlist = [int(line.strip()) for line in f.readlines()]
        except FileNotFoundError:
            self.banlist = []

        super().__init__(command_prefix=discord.ext.commands.when_mentioned_or(self.PREFIX),
                         owner_ids=OWNER_IDS,
                         intents=discord.Intents.all(),
                         case_insensitive=True,
                         help_command=self.Help_Command
                         )

    def setup(self):
        # print(f"Total numbers of cog : {COGS.__len__()}")
        self.cogs_loaded = 0
        for cog in COGS:
            self.load_extension(f"cogs.{cog}")
            print(f"{cog} loaded")
            self.cogs_loaded += 1
        if self.cogs_loaded == len(COGS):
            print("Every cogs has been loaded")
            print(f"Number of cogs loaded : {self.cogs_loaded}/{len(COGS)}")

    def run(self):
        self.setup()
        self.TOKEN = TOKEN
        print(TOKEN)

        super(Bot, self).run(self.TOKEN, reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            if message.author.id in self.banlist:
                await ctx.send("You are banned from using commands.")

            elif not self.ready:
                await ctx.send("I'm not ready to receive commands. Please wait a few seconds.")

            else:
                await self.invoke(ctx)

    async def on_connect(self):
        print("bot connected")

    async def on_disconnect(self):
        print("bot disconnected")

    async def on_ready(self):

        if not self.ready:
            self.guild = self.get_guild(753650060314804255)
            self.logs_channel = self.get_channel(798851483692302347)

            while not self.cogs_ready.all_ready():
                await sleep(0.5)
            await self.logs_channel.send("Now online !")
            await self.logs_channel.send(f"{self.cogs_loaded}/{COGS.__len__()} cogs has been loaded")
            self.ready = True
            await self.tracker.cache_invites()
            print("bot ready")
        else:
            print("bot reconnected")

    async def on_invite_create(self, ctx, invite):
        await self.tracker.update_invite_cache(invite)

    async def on_member_join(self, member: discord.Member):
        inviter = await self.tracker.fetch_inviter(member)

        if self.welcome_channel is not None:
            await self.welcome_channel.send(f"Welcome ! {member.mention}")
        else:
            joined_embed = Embed(title=f"{member} joined !",
                                 colour=discord.colour.Colour.orange(),
                                 timestamp=datetime.utcnow(),
                                 )
            joined_embed.set_thumbnail(url=member.avatar_url)

            await self.logs_channel.send(f"at {datetime.utcnow()}\n"
                                         f"{member} as joined the server"
                                         f"Welcome channel was not set")

    async def on_member_remove(self, member: discord.Member):
        pass

    async def set_welcome_channel(self, ctx, channel_name=None):
        if channel_name is not None:
            for channel in ctx.guild.channels:
                if channel.name == channel_name:
                    self.welcome_channel = channel
                    await ctx.channel.send(f"Welcome channel has been set to: {channel.name}")
                    await channel.send("This is the new welcome channel !")
        else:
            await ctx.channel.send("You didn't include the name of the welcome channel.")

    async def on_message(self, message):
        if not message.author.bot:
            if isinstance(message.channel, DMChannel):
                if len(message.content) < 50:
                    await message.channel.send("Your message should be at least 50 characters in lenght.")
                else:
                    member = self.guild.get_member(message.author.id)
                    embed = Embed(title="ModMail",
                                  colour=member.colour,
                                  timestamp=datetime.utcnow())

                    embed.set_thumbnail(url=member.avatar_url)

                    fields = [("Member", member.display_name, False),
                              ("Message", message.content, False)]

                    for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)

                    mod = self.get_cog("Mod")
                    await mod.logs_channel.send(embed=embed)
                    await message.channel.send("Message relayed to moderators.")
            else:
                await self.process_commands(message)


bot = Bot()
