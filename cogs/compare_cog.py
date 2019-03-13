#!/usr/bin/env python3
"""Find user similarities"""
import discord
from data import permissions_data, lastfm_data
from discord.ext import commands
from similarities import *


class CompareCog:
    """Compares two users based on lastfm similarity"""

    def __init__(self, bot):
        """Constructor class"""
        self.bot = bot

    @commands.group(pass_context=True, aliases=["cp"])
    async def compare(self, ctx):
        """Find the similarity of oneself to a target user"""
        channel_id = ctx.message.channel.id
        author_id = ctx.message.author.id

        bad_permissions = "Sorry, you cannot use that command here."
        bad_username = "Please set a lastfm username first."
        bad_mention = ("Either you have not mentioned a user or that user " +
                       "has not set a lastfm username.")

        subcommand = ctx.invoked_subcommand
        if subcommand:
            return

        channels = permissions_data.get_allowed_channels("compare")
        if channel_id not in channels:
            await self.bot.say(bad_permissions)
            return

        try:
            target_id = ctx.message.mentions[0].id
        except:
            await self.bot.say(bad_mention)
            return

        user = lastfm_data.get_user(author_id)
        if not user:
            await self.bot.say(bad_username)
            return

        target = lastfm_data.get_user(target_id)
        if not target:
            await self.bot.say(bad_mention)
            return

        sim = compare_users(user, target)
        if not sim:
            await self.bot.say("Unknown error occurred.")
            return

        await self.bot.say(sim)

    @compare.command(pass_context=True)
    async def top12(self, ctx):
        channel_id = ctx.message.channel.id
        author_id = ctx.message.author.id

        bad_permissions = "Sorry, you cannot use that command here."
        bad_username = "Please set a lastfm username first."
        bad_mention = ("Either you have not mentioned a user or that user " +
                       "has not set a lastfm username.")

        channels = permissions_data.get_allowed_channels("compare top12")
        if channel_id not in channels:
            await self.bot.say(bad_permissions)
            return

        user = lastfm_data.get_user(author_id)
        if not user:
            await self.bot.say(bad_username)
            return

        top12 = most_similar(user)
        description = ""
        count = 0
        for similar_user in top12:
            count += 1
            description += str(count) + ": " + similar_user + "\n"
 
        embed = discord.Embed(color=0xFFFFFF, title=user + "'s similar users",
                              description=description)

        await self.bot.say(embed=embed)


def setup(bot):
    """Attach the compare cog to a bot"""
    cog = CompareCog(bot)
    bot.add_cog(cog)
