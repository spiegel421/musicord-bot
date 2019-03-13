import discord
from datetime import datetime
from discord.ext import commands

TOKEN = open("token_test.txt", "r").read()
SERVERS = dict()

client = discord.Client()


@client.event
async def on_message(message):
    if not message.author.server_permissions.administrator:
        return

    if message.content.startswith("!autoban"):
        enable_or_disable = message.content.split(" ")[1]
        if enable_or_disable == "enable":
            SERVERS[message.server] = True
        elif enable_or_disable == "disable":
            SERVERS[message.server] = False
    

@client.event
async def on_member_join(member):
    try:
        enabled = SERVERS[member.server]
        if not enabled:
            return
    except KeyError:
        return

    join_date = member.created_at
    account_age = (datetime.utcnow() - join_date).total_seconds()
    num_days_old = account_age / 60 / 60 / 24

    if num_days_old < 1:
        await client.ban(member)

client.run(TOKEN)
