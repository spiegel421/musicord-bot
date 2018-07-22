#!/usr/bin/env python3
"""Lastfm cog

Communicate with lastfm API to display now playing, number of artist
scrobbles, top artists, and a number of other features.
"""
import colorific
import discord
import json
import requests
import urllib.request
from data import permissions, lastfm_users
from discord.ext import commands
from PIL import Image

API_KEY, API_SECRET = open("cogs/api.txt", "r").readlines()


def get_user_url(user):
    """Return hypothetical url of a lastfm username"""
    url = (("http://ws.audioscrobbler.com/2.0/" +
            "?method=user.getInfo" +
            "&user={}" +
            "&api_key={}" +
            "&format=json").format(user, API_KEY))

    return url


def get_page_url(method, user, results_per_page=1000, page=1):
    """Return url needed for API request

    Given a user and an API method, return the url of the page displaying
    the method's results for that user. For user-only methods.
    """
    url = (("http://ws.audioscrobbler.com/2.0/" +
            "?method={}" +
            "&user={}" +
            "&api_key={}" +
            "&limit={}" +
            "&page={}" +
            "&format=json").format(method, user, API_KEY,
                                   results_per_page, page))

    return url


def get_page_url_alt(method, user, artist, results_per_page=1000, page=1):
    """Same as above, but for artist-dependent methods"""
    url = (("http://ws.audioscrobbler.com/2.0/" +
            "?method={}" +
            "&user={}" +
            "&artist={}" +
            "&api_key={}" +
            "&limit={}" +
            "&page={}" +
            "&format=json").format(method, user, artist,
                                   API_KEY, results_per_page, page))

    return url


def is_username(user):
    """Return whether a username is valid on lastfm"""
    user_url = get_user_url(user)
    request = requests.get(user_url)

    if request.status_code == 200:
        content = request.text
        parsed_content = json.loads(content)

        try:
            error = parsed_content['error']
            return False
        except KeyError as err:
            return True

    return False


def make_recent_tracks_list(parsed_content):
    """Given a parsed json page, make a list of recent tracks"""
    recent_tracks = parsed_content['recenttracks']['track']
    recent_tracks_list = list()

    for track in recent_tracks:
        name = track['name']
        artist = track['artist']['#text']
        album = track['album']['#text']
        image = track['image'][3]['#text']
        recent_tracks_list.append((name, artist, album, image))

    return recent_tracks_list


def get_last_played(user):
    """Get a user's last played track"""
    method = "user.getRecentTracks"
    page_url = get_page_url(method, user, results_per_page=1)
    request = requests.get(page_url)

    if request.status_code == 200:
        content = request.text
        parsed_content = json.loads(content)

        error = None
        try:
            error = parsed_content['error']
        except KeyError as err:
            pass

        if error is None:
            recent_tracks_list = make_recent_tracks_list(parsed_content)
            last_played_track = recent_tracks_list[0]
            return last_played_track

    return None


def get_num_scrobbles_of_artist(user, artist):
    """Find number of times user has scrobbled an artist"""
    method = "user.getArtistTracks"
    page_url = get_page_url_alt(method, user, artist)
    request = requests.get(page_url)

    if request.status_code == 200:
        content = request.text
        parsed_content = json.loads(content)

        error = None
        try:
            error = parsed_content['error']
        except KeyError as err:
            pass

        if error is None:
            artist_tracks = parsed_json['artisttracks']['track']
            num_scrobbles = len(artist_tracks)
            return num_scrobbles

    return None


def make_top_artist_dict(parsed_content):
    """Given a parsed json page, make a dict of top artists"""
    top_artists = parsed_content['topartists']['artist']
    top_artists_dict = dict()

    for artist in top_artists:
        name = artist['name']
        playcount = int(artist['playcount'])
        top_artists_dict[name] = playcount

    return top_artists_dict


def get_top_artists(user):
    """Find a user's most scrobbled artists"""
    method = "user.getTopArtists"
    page_url = get_page_url(method, user)
    request - requests.get(page_url)

    if request.status_code == 200:
        content = request.txt
        parsed_content = json.loads(content)

        error = None
        try:
            error = parsed_content['error']
        except KeyError as err:
            pass

        if error is None:
            top_artists_dict = make_top_artist_dict(parsed_content)
            return top_artists_dict

    return None


def get_primary_color(image_url):
    """Get the primary color of the currently playing album"""
    urllib.request.urlretrieve(image_url, "album_art.jpg")
    
    palette = colorific.extract_colors("album_art.jpg", min_prominence=0.1)
    primary_color_rgb = palette.colors[0].value
    primary_color = "0x" + colorific.rgb_to_hex(primary_color_rgb)[1:]

    return int(primary_color, 0)


class LastfmCog:
    """Cog class"""

    def __init__(self, bot):
        """Constructor for cog class

        Takes as input a Bot object.
        """
        self.bot = bot

        # Dictionaries to keep track of commands to show top artists, since
        # these commands are sensitive to reactions.
        self.top_artist_msgs = {}

    @commands.group(pass_context=True, aliases=["fm"])
    async def lastfm(self, ctx):
        """Display last played, number of artist scrobbles, and top artists"""
        channel_id = ctx.message.channel.id
        author_id = ctx.message.author.id

        bad_permissions = "Sorry, you cannot use that command here."
        bad_username = "Please set a lastfm username first."
        bad_last_played = "I could not find your last played song."

        # Invokes any subcommand given.
        subcommand = ctx.invoked_subcommand
        if subcommand is not None:
            return

        # Bad channel permissions.
        if channel_id not in permissions.get_allowed_channels("lastfm"):
            await self.bot.say(bad_permissions)
            return

        user = lastfm_users.get_user(author_id)
        if user is None:
            await self.bot.say(bad_username)

        last_played = get_last_played(user)
        if last_played is None:
            await self.bot.say(bad_last_played)

        await commands.Command.invoke(self.embed_last_played, ctx)

    @commands.command(pass_context=True)
    @commands.cooldown(1, 420, commands.BucketType.user)
    async def embed_last_played(self, ctx):
        """Create an embed from last played data"""
        author = ctx.message.author
        author_id = author.id
        avatar_url = author.avatar_url

        user = lastfm_users.get_user(author_id)
        last_played = get_last_played(user)

        name, artist, album, image_url = last_played

        rym_link = ("https://rateyourmusic.com/" +
                    "search?&searchtype=l&searchterm={}")

        rym_link = rym_link.format(album.replace(" ", "%20"))
        album_search_url = ("[{}]({})").format(album, rym_link)
        user_search_url = "https://www.last.fm/user/{}".format(user)

        color = get_primary_color(image_url)

        embed = discord.Embed(colour=color, description=name)
        embed.add_field(name=artist, value=album_search_url)

        embed.set_author(name=user, icon_url=avatar_url, url=user_search_url)
        embed.set_thumbnail(url=image_url)

        await self.bot.say(embed=embed)

    @lastfm.command(pass_context=True)
    async def set(self, ctx, user):
        """Add a user's lastfm username to table"""
        channel_id = ctx.message.channel.id
        author_id = ctx.message.author.id

        bad_permissions = "Sorry, you cannot use that command here."
        bad_username = "That is not a valid lastfm username."

        if channel_id not in permissions.get_allowed_channels("lastfm set"):
            await self.bot.say(bad_permissions)
            return

        if not is_username(user):
            await self.bot.say(bad_username)
            return

        lastfm_users.add_user(author_id, user)
        await self.bot.say("Username successfully set!")


def setup(bot):
    """Attach the lastfm cog to a bot"""
    cog = LastfmCog(bot)
    bot.add_cog(cog)
