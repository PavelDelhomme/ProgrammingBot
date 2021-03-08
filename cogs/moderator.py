import asyncio
from datetime import datetime

from discord.ext import commands
import discord
from discord.ext.commands import MissingRequiredArgument, Cog

from discord.utils import get

import re

from utils.utils import notify_user

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {'h': 3600, 's': 1, 'm': 60, 'd': 86400}


class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for key, value in matches:
            try:
                time += time_dict[value] * float(key)
            except KeyError:
                raise commands.BadArgument(f"{value} is an invalid time key! h|m|s|d are valide arguments")
            except ValueError:
                raise commands.BadArgument(f"{key} is not a number !")
        return time


class Moderator(commands.Cog):
    """
    All command to moderate the server
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="Extentions")
    @commands.is_owner()
    @commands.guild_only()
    async def extentions(self, ctx):
        """
        Group every commands about the extentions moderation
        """

    @extentions.command(name="unload",
                        usage="do unload {name_of_cog}",
                        description="Unload some features",
                        brief="Unload some features")
    @commands.is_owner()
    @commands.guild_only()
    async def unload(self, ctx, cog: str):
        """
        Unload some features
        """
        try:
            self.bot.unload_extension(f"cogs.{cog}")
        except MissingRequiredArgument as e:
            await ctx.send("You must specify an cog to unload")
            try:
                self.bot.unload_extension(f"cogs.{cog}")
            except Exception as e:
                await ctx.send("Could not unload cog")
                return
        await ctx.send("Cog unloaded")

    @extentions.command(name="load",
                        usage="do load {name_of_cog}",
                        brief="Load some features")
    @commands.is_owner()
    @commands.guild_only()
    async def load(self, ctx, cog: str):
        """
        Load some features
        """
        try:
            self.bot.load_extension(f"cogs.{cog}")
        except MissingRequiredArgument as e:
            await ctx.send("You must specify an cog to load")
            try:
                self.bot.load_extension(f"cogs.{cog}")
            except Exception as e:
                await ctx.send("Could not load cog")
                return
        await ctx.send("Cog loaded")

    @extentions.command(name="reload",
                        usage="do reload {name_of_cog}",
                        brief="Reload some features")
    @commands.is_owner()
    async def reload(self, ctx, cog: str):
        """
        Reload some features
        """
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            self.bot.load_extension(f"coogs.{cog}")
        except Exception as e:
            await ctx.send("Could not unload cog")
            return
        await ctx.send("Cog unloaded")

    @commands.group(name="Users")
    @commands.is_owner()
    @commands.guild_only()
    async def users(self, ctx):
        """
        Group every commands about the users moderation
        """
        pass

    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    @commands.is_owner()
    @users.command(name="kick",
                   usage="kick {member_name}")
    async def kick(self, ctx, member: discord.Member = None, reason: str = "Because you were bad. We kicked you."):
        """
        Kick an member
        """
        if member is not None:
            await ctx.guild.kick(member, reason=reason)
            await notify_user(member, reason)
        else:
            await ctx.send("Please specify user to kick")
        await ctx.send(f"The {member} was kicked")

    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    @commands.is_owner()
    @users.command(name="ban", hidden=True,
                   usage="ban {member_name}")
    async def ban(self, ctx, member: discord.Member = None, reason: str = "We've banned you for no reason"):
        """
        Ban an member
        """
        if member != None:
            await ctx.guild.ban(member, reason=reason)
            await notify_user(member, reason)
        else:
            await ctx.send("Please specify user to ban")

    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    @commands.is_owner()
    @users.command(name="unban", hidden=True,
                   usage="unban {member_name}")
    async def unban(self, ctx, member: str = "", reason="You have been unbanned. Time is over. Please behave."):
        """
        Unban an member
        """
        if member == "":
            await ctx.send("Please specify the username as text")
            return
        bans = await ctx.guild.bans()
        for b in bans:
            if b.user.name == member:
                await ctx.guild.unban(member, reason=reason)
                await ctx.send(f"{member} was unbanned")
                await notify_user(member, reason)
                return
        await ctx.send("User was not found un ban list")

    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    @commands.is_owner()
    @users.command(name="infoU",
                   usage="user",
                   aliases=['showuser', 'user'], help="Show an user")
    async def user(self, ctx, *, user: discord.Member = None):
        """
        Return information about an user
        """
        embedUser = discord.Embed(title=f"Informations about {user}", color=discord.Colour.gold())
        if ctx.guild.icon:
            embedUser.set_thumbnail(url=user.icon_url)
        if ctx.guild.banner:
            embedUser.set_image(url=ctx.guild.banner_url_as(format="png"))
        embedUser.description(name="Name", value=user.display_name)
        embedUser.add_field(name="Nickname", value=user.nick)
        embedUser.add_field(name="Roles", value=user.roles.sort())
        embedUser.add_field(name="Status", value=user.status)
        embedUser.add_field(name="Activity", value=user.activity)
        embedUser.description(name="Roles", value=user.roles)
        embedUser.add_field(name="Joined server", value=user.joined_at)
        embedUser.add_field(name="Desktop status", value=user.desktop_status)
        embedUser.add_field(name="Mobile status", value=user.mobile_status)
        embedUser.add_field(name="Is on mobile status", value=user.is_on_mobile())
        embedUser.add_field(name="Raw status", value=user.raw_status)
        embedUser.add_field(name="Web status", value=user.web_status)
        embedUser.add_field(name="User colour", value=user.colour)
        embedUser.add_field(name="User color", value=user.color)
        await ctx.channel.send(embed=embedUser)

    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    @commands.is_owner()
    @users.command(name="allU",
                   help="Show all users")
    async def all_users(self, ctx, *, user: discord.Member = None):
        """
        Return all users presents on this server
        """
        embedUsers = discord.Embed(title="Members infos", color=discord.Colour.gold())
        if ctx.guild.icon:
            embedUsers.set_thumbnail(url=user.icon_url)

        embedUsers.add_field(name="Members", value=ctx.guild.members, inline=True)
        embedUsers.add_field(name="Number of user", value=ctx.guild.member_count, inline=True)
        embedUsers.add_field(name="Rols", value=ctx.guild.roles, inline=True)
        embedUsers.add_field(name="WebHooks", value=ctx.guild.webhooks(), inline=True)
        embedUsers.add_field(name="Curretly invite", value=ctx.guild.invites(), inline=True)
        embedUsers.set_footer(text=str(datetime.now()))
        await ctx.channel.send(embed=embedUsers)

    @commands.group(name="Status")
    @commands.is_owner()
    async def Status(self, ctx):
        """
        Group every commands about the server status
        """

    @Status.command(name="status")
    @commands.is_owner()
    async def status(self, ctx):
        """
        Show status of the bot server
        """
        if ctx.invoked_subcommand is None:
            find_bots = sum(1 for member in ctx.guild.members if member.bot)

            embed = discord.Embed(title="Server Infos", description="This is a small description about this server",
                                  color=discord.Colour.red())

            if ctx.guild.icon:
                embed.set_thumbnail(url=ctx.guild.icon_url)
            if ctx.guild.banner:
                embed.set_image(url=ctx.guild.banner_url_as(format="png"))

            embed.add_field(name="Server Name", value=ctx.guild.name, inline=True)
            embed.add_field(name="Server ID", value=ctx.guild.id, inline=True)
            embed.add_field(name="Members", value=ctx.guild.member_count, inline=True)
            embed.add_field(name="Bots", value=find_bots, inline=True)
            embed.add_field(name="Owner", value=ctx.guild.owner, inline=True)
            embed.add_field(name="Region", value=ctx.guild.region, inline=True)
            embed.add_field(name="Created", value=ctx.guild.created_at, inline=True)
            embed.set_author(name=self.bot.user.name)
            embed.set_footer(text=datetime.now())
            emoji_string = ""
            for e in ctx.guild.emojis:
                if e.is_usable():
                    emoji_string += str(e)
            embed.add_field(name="Python Emoji", value=emoji_string or "No emojis available", inline=False)

            await ctx.send(content=f"ℹ information about **{ctx.guild.name}**", embed=embed)

    @staticmethod
    def get_channel_by_name(guild, channel_name):
        """
        ¨Permit to get all channel by name
        :param guild:
        :param channel_name:
        :return:
        """
        channel = None
        for c in guild.channels:
            if c.name == channel_name.lower():
                channel = c
                break
        return channel

    @staticmethod
    def get_category_by_name(guild, category_name):
        """
        Creates a new channel in the category "category_name"
        """
        category = None
        for c in guild.categories:
            if c.name == category_name:
                category = c
                break
        return category

    @commands.group(name="new",
                    invoke_without_command=True)
    @commands.guild_only()
    @commands.is_owner()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def new(self, ctx):
        await ctx.send("Invalide sub-command passed.")
        embed = discord.Embed()
        await ctx.send("Please check with do help new")

    @new.command(name="new category",
                 usage="new category {role} {category_name}",
                 brief="")
    @commands.guild_only()
    @commands.is_owner()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def ccategory(self, ctx, role: discord.Role, *, name):
        """
        Create a new category,
        Role is facultative
        """
        overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                ctx.guild.me          : discord.PermissionOverwrite(read_messages=True),
                role                  : discord.PermissionOverwrite(read_messages=True)
        }
        category = await ctx.guild.create_category(name=name, overwrites=overwrites)
        await ctx.send(f"Hey dude, I made {category.name} for ya!")

    @new.command(name="new channel",
                 description="command to create a new channel"
                             "role is facultative",
                 usage="new channel {role} {channel_name}",
                 brief="")
    @commands.guild_only()
    @commands.is_owner()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def cchannel(self, ctx, role: discord.Role, *, name):
        """
        Create a new channel,
        Role is facultative
        """
        try:
            overwrites = {
                    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    ctx.guild.me          : discord.PermissionOverwrite(read_messages=True),
                    role                  : discord.PermissionOverwrite(read_messages=True)
            }
            channel = await ctx.guild.create_text_channel(name=name, overwrites=overwrites)
            await ctx.send(f"Hey dude, I made {channel.name} for ya!")
        except MissingRequiredArgument:
            await ctx.send("You must specify the name of the channel")

    @commands.command(name="mute",
                      description="Mutes a given user for x time!",
                      usage='<user> [time]')
    @commands.is_owner()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, time: TimeConverter = None):
        """
        Mute a member
        """
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            await ctx.send("No muted role was found. Please create one called \'Muted\'")
            return

        await member.add_roles(role)
        await ctx.send(f"Muted `{member.display_name}` for {time}s." if time else f"Muted `{member.display_name}`.")

        if time:
            await asyncio.sleep(time)

            if role in member.roles:
                await member.remove_roles(role)
                await ctx.send(f"Unmuted `{member.display_name}`")

    @commands.command(
            name="unmute",
            description="Unmuted a member",
            usage="<user>"
    )
    @commands.is_owner()
    async def unmute(self, ctx, member: discord.Member):
        """
        Unmute a member
        """
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            await ctx.send("No muted role was found! Please create one called `Muted`")
            return

        if role not in member.roles:
            await ctx.send("This member is not muted")

        await member.remove_roles(role)
        await ctx.send(f"Unmuted `{member.display_name}`")

    @commands.command(name="give_roles", hidden=True)
    @commands.is_owner()
    @commands.guild_only()
    async def add_roles(self, ctx, member: discord.Member = None, role: discord.Role = None):
        await self.bot.add_roles(member, role)

    @commands.command(name="show_roles")
    @commands.is_owner()
    @commands.guild_only()
    async def show_roles(self, ctx):
        roles = ctx.guild.Guild.roles
        print(roles)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Moderator")


def setup(bot):
    bot.add_cog(Moderator(bot))
