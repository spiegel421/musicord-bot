#!/usr/bin/env python3
"""The permissions cog

Handles permissions for all bot commands.
"""
import discord
from data import permissions_data
from discord.ext import commands


def user_is_me(ctx):
    return ctx.message.author.id == "359613794843885569"


class PermissionsCog:
    """Cog class"""

    def __init__(self, bot):
        """Constructor for cog class

        Takes as input a bot object.
        """
        self.bot = bot

    @commands.group(pass_context=True, aliases=["perms"])
    @commands.check(user_is_me)
    async def permissions(self, ctx):
        """Allow and deny certain commands within specified channels"""
        subcommand = ctx.invoked_subcommand
        if subcommand is not None:
            return

    @permissions.command(pass_context=True)
    async def allow(self, ctx, *args):
        """Allow a command to be used within a channel"""
        channel_id = ctx.message.channel.id

        command = ""
        for arg in args:
            command += arg + " "
        command = command[:-1]

        if permissions_data.add_allowed_channel(command, channel_id):
            await self.bot.say("Command enabled.")
        else:
            await self.bot.say("Sorry, that is not a command.")

    @permissions.command(pass_context=True)
    async def deny(self, ctx, *args):
        """Deny a command from being used within a channel"""
        channel_id = ctx.message.channel.id

        command = ""
        for arg in args:
            command += arg + " "
        command = command[:-1]

        if permissions_data.remove_allowed_channel(command, channel_id):
            await self.bot.say("Command disabled.")
        else:
            await self.bot.say("Sorry, that is not a command.")


def setup(bot):
    """Attach the permissions cog to a bot"""
    cog = PermissionsCog(bot)
    bot.add_cog(cog)
