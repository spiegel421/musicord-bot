#!/usr/bin/env python3
"""Find user similarities"""
import copy
import discord
import math
import numpy
from collections import defaultdict
from cogs.lastfm_cog import get_top_artists
from data import permissions_data, lastfm_data
from discord.ext import commands
from pandas import DataFrame


def gen_user_artist_dataframe():
    """Create a matrix with users as rows and artists as columns,
       corresponding to each user's playcount of each artist"""
    print("Generating dataframe from lastfm usernames.")
    user_to_id_dict = lastfm_data.get_users_and_ids()
    playcounts = defaultdict(dict)
    users = user_to_id_dict.keys()
    count = 0
    for user in users:
        count += 1
        top_artist_dict = get_top_artists(user)
        top_artists = top_artist_dict.keys()
        for artist in top_artists:
            playcounts[user][artist] = top_artist_dict[artist]
        print(str(count) + "/" + str(len(users)) + " users counted.")

    df = DataFrame(playcounts).T.fillna(0.0)
    return df


def gen_npmi_dataframe(df):
    """Generate an npmi value for each user and artist"""
    print("Finding npmi values.")
    total_playcount = sum(df.sum())
    user_playcounts = df.sum(axis=1)
    artist_playcounts = df.sum(axis=0)
    npmi_df = copy.copy(df)
    count = 0
    for user, user_artist_playcounts in df.iterrows():
        count += 1
        for artist in user_artist_playcounts.index:
            user_artist_playcount = user_artist_playcounts[artist]
            if user_artist_playcount == 0.0:
                npmi = -1.0
            else:
                x = total_playcount * user_artist_playcount
                y = user_playcounts[user] * artist_playcounts[artist]
                npmi = -1 * math.log(x / y, 2) / math.log(x, 2)
            npmi_df.at[user, artist] = npmi
        print(str(count) + "/" + str(len(user_playcounts)) + " users counted.")

    return npmi_df


def find_similarities(npmi_df):
    """Find Pearson correlation coefficients between all users"""
    def dotproduct(vectorA, vectorB):
        return sum([a * b if (a > -1.0 and b > -1.0) else 0
                    for a, b in zip(vectorA, vectorB)])

    def length(vector):
        return math.sqrt(dotproduct(vector, vector))

    print("Finding similarities.")
    users = npmi_df.index
    similarities = defaultdict(dict)
    count = 0
    for userA in users:
        count += 1
        vectorA = npmi_df.loc[userA]
        for userB in users:
            vectorB = npmi_df.loc[userB]
            num = dotproduct(vectorA, vectorB)
            den = length(vectorA) * length(vectorB)
            similarities[userA][userB] = num / den
        print(str(count) + "/" + str(len(users)) + " users counted.")

    return similarities


def record_similarities(similarities):
    """Record user similarities to text file"""
    writer = open("similarities.txt", "w")
    for userA in similarities.keys():
        for userB in similarities[userA].keys():
            writer.write(userA + "\t" + userB + "\t" +
                         str(similarities[userA][userB]) + "\n")
    writer.close()


def find_similarity(userA, userB):
    reader = open("similarities.txt", "r")
    lines = reader.readlines()
    sim_dict = dict()
    for line in lines:
        a, b, sim = line.split("\t")
        if userA == a:
            sim_dict[b] = float(sim)

    if len(sim_dict.keys()) == 0:
        return None

    ranked = sorted(sim_dict.keys(), key=lambda x: sim_dict[x],
                    reverse=True)
    try:
        index = ranked.index(userB)
        percentile = 1.0 - (float(index) / len(sim_dict.keys()))
        return int(100 * percentile)
    except:
        return None


def most_similar(user):
    """Finds 10 most similar users to given user"""
    reader = open("similarities.txt", "r")
    lines = reader.readlines()
    sim_dict = dict()
    for line in lines:
        a, b, sim = line.split("\t")
        if user == a:
            sim_dict[b] = float(sim)

    if len(sim_dict.keys()) == 0:
        return None

    ranked = sorted(sim_dict.keys(), key=lambda x: sim_dict[x],
                    reverse=True)

    return ranked[1:13]


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

        sim = find_similarity(user, target)
        if not sim:
            await self.bot.say("Unknown error occurred.")
            return

        await self.bot.say(user + " and " + target + " are " + str(sim) +
                           " percent compatible.")

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


def main():
    df = gen_user_artist_dataframe()
    npmi_df = gen_npmi_dataframe(df)
    similarities = find_similarities(npmi_df)
    record_similarities(similarities)


if __name__ == "__main__":
    main()
