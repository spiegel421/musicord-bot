#!/usr/bin/env python3
"""The bot program

Runs a bot with the given cogs.
"""
import discord
from cogs import lastfm_cog, permissions_cog, compare_cog
from data import lastfm_data, permissions_data
from discord.ext import commands

COMMANDS = ["lastfm", "lastfm set", "lastfm scrobbles", "compare", "compare top12"]

if __name__ == "__main__":
    lastfm_data.create_user_table()
    permissions_data.create_command_tables(COMMANDS)

    bot = commands.Bot(command_prefix=".")
    lastfm_cog.setup(bot)
    permissions_cog.setup(bot)
    compare_cog.setup(bot)

    with open("token.txt", "r") as reader:
        token = reader.read()
        bot.run(token)