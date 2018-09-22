#!/usr/bin/env python3
"""The bot program

Runs a bot with the given cogs.
"""
import discord
from cogs import lastfm_cog, permissions_cog, compare_cog, tag_cog
from data import lastfm_data, permissions_data, tag_data
from discord.ext import commands

COMMANDS = ["lastfm", "lastfm set", "lastfm scrobbles", "compare", 
            "compare top12", "tag", "tag edit", "tag display", "tag set",
            "tag list", "tag search", "tag owner", "tag delete", "chart",
            "chart set"]

if __name__ == "__main__":
    lastfm_data.create_user_table()
    permissions_data.create_command_tables(COMMANDS)
    tag_data.create_tag_tables()

    bot = commands.Bot(command_prefix=".")
    lastfm_cog.setup(bot)
    permissions_cog.setup(bot)
    compare_cog.setup(bot)
    tag_cog.setup(bot)
    
    @bot.event
    async def on_message(message):
        if "hot take" in message.content:
            await bot.delete_message(message)
        
        await bot.process_commands(message)

    with open("token.txt", "r") as reader:
        token = reader.read()
        bot.run(token)