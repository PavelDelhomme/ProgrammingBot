import discord
from discord.ext import commands
from discord.ext.commands import Cog

from DiscordUtils import InviteTracker


class Invites(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tracker = InviteTracker(bot=self.bot)

    @Cog.listener()
    async def on_invite_create(self, invite):
        await self.tracker.update_invite_cache(invite)

    @Cog.listener()
    async def on_guild_join(self, guild):
        await self.tracker.update_guild_cache(guild)

    @Cog.listener()
    async def on_invite_delete(self, invite):
        await self.tracker.remove_invite_cache(invite)

    @Cog.listener()
    async def on_guild_remove(self, guild):
        await self.tracker.remove_guild_cache(guild)

    @Cog.listener()
    async def on_member_join(self, member):
        invter = await self.tracker.fetch_inviter(member)
        """
        channel = discord.utils.get(member.guild.text_channels, name="recording")
        embed = discord.Embed(title=f"Welcome {member.display_name}",
                              description=self.invite
                              )
        """

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Invites")
            await self.tracker.cache_invites()


def setup(bot):
    bot.add_cog(Invites(bot))
