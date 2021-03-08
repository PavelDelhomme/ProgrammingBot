"""
import datetime
import json
import os
import sys
import time

import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="new",
                    description="command to create a new {category / channel}]",
                    usage="",
                    invoke_without_command=True)
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def new(self, ctx):
        await ctx.send("Invalide sub-command passed.")
        embed = discord.Embed()
        await ctx.send("Please check with do new")

    @new.command(name="new category",
                 description="command to create a new category"
                             "role is facultative",
                 usage="new category {role} {category_name}",
                 brief="")
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def ccategory(self, ctx, role: discord.Role, *, name):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True)
        }
        category = await ctx.guild.create_category(name=name, overwrites=overwrites)
        await ctx.send(f"Hey dude, I made {category.name} for ya!")


    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def remove(self, ctx):
        await ctx.send("Invalide sub-command passed.")

    # todo delete category
    @remove.command(name="remove category",
                    description="command to delete a category",
                    usage="remove {category_name}",
                    brief="")
    async def dcategory(self, ctx, *, name):
        pass

    # todo delete channel
    @remove.command(name="remove channel",
                    description="command to delete an channel",
                    usage="remove {channel_name}",
                    brief="")
    async def dchannel(self, ctx, *, name):
        pass

    @commands.is_owner()
    @commands.command(name="reboot",
                      description="reboot the bot",
                      usage="reboot",
                      brief="")
    async def reboot(self, ctx):
        await ctx.send("Rebooting now...")
        time.sleep(1)
        sys.exit(0)

    @commands.guild_only()
    @commands.is_owner()
    @commands.command(name="deleteall",
                      description="Delete All TextChannel adn VoiceChannel...")
    async def deleteall(self, ctx):
        [await channel.delete() for channel in ctx.guild.text_channels]

    @commands.guild_only()
    @commands.is_owner()
    @commands.command(name="reactrole")
    async def reactrole(self, ctx, emoji, role: discord.Role, *, message):
        """
        #reactrole
        #:param ctx:
        #:param emoji:
        #:param role:
        #:param message:
        #:return:
       #
       # embedVar = discord.Embed(description=message)
       # msg = await ctx.channel.send(embed=embedVar)
       # await msg.add_reaction(emoji)
       # REACT_ROLE_FILE = "../data/reactrole.json"
       # if not os.path.exists(REACT_ROLE_FILE):
       #     os.makedirs(REACT_ROLE_FILE)
#
#        with open(REACT_ROLE_FILE) as json_file:
#            data = json.load(json_file)
#
#            new_react_role = {
#                'role_name': role.name,
#                'role_id': role.id,
#                'emoji': emoji,
#                'message_id': message.id
#            }
#
#            data.append(new_react_role)
#
#        with open(REACT_ROLE_FILE, "w") as j:
#            json.dump(data, j, indent=4)
#
#
#def setup(bot):
#    bot.add_cog(Admin(bot))
#"""