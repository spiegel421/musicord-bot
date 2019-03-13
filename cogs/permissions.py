#!/usr/bin/env python3
"""The permissions cog

Handles permissions for all bot commands.
"""
import discord
from data import permissions
from discord.ext import commands


class PermissionsCog:
    """Cog class"""

    def __init__(self, bot):
        """Constructor for cog class

        Takes as input a bot object.
        """
        self.bot = bot

    @commands.group(pass_context=True, aliases=["perms"])
    async def permissions(self, ctx):
        """Allow and deny certain commands within specified channels"""
        subcommand = ctx.invoked_subcommand
        if subcommand is not None:
            return

    @permissions.command(pass_context=True)
    async def allow(self, ctx, command):
        """Allow a command to be used within a channel"""
        channel_id = ctx.message.channel

        if permissions.add_allowed_channel(command, channel_id) is not None:
            await self.bot.say("Command enabled.")
        else:
            await self.bot.say("Sorry, that is not a command.")


def setup(bot):
    """Attach the permissions cog to a bot"""
    cog = PermissionsCog(bot)
    bot.add_cog(cog)
