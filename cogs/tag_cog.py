#!/usr/bin/env python3
"""Tags cog

Allows users to display tags.
"""
import discord, discord.utils
from data import permissions_data, tag_data
from discord.ext import commands

class TagCog:
    """Tag class"""

    def __init__(self, bot):
        """Constructor for tag class

        Takes as input a Bot object.
        """
        self.bot = bot

    @commands.group(pass_context=True, aliases=["t"])
    async def tag(self, ctx):
        """Handle tag commands"""
        subcommand = ctx.invoked_subcommand
        if subcommand:
            return

        """Display any tag content from name"""
        channel_id = ctx.message.channel.id

        bad_permissions = "Sorry, you cannot use that command here."
        if channel_id not in permissions_data.get_allowed_channels("tag"):
            await self.bot.say(bad_permissions)
            return

        name = " ".join(ctx.message.content.split(" ")[1:])

        content = tag_data.get_tag_content(name)
        await self.bot.say(content)

    @tag.command(pass_context=True)
    async def edit(self, ctx, *, name):
        """Switch to a tag to edit"""
        if "Regular" not in [x.name for x in ctx.message.author.roles]:
            await self.bot.say("You need to have the Regular role to use that command.")
            return
        channel_id = ctx.message.channel.id

        bad_permissions = "Sorry, you cannot use that command here."
        bad_owner = "Sorry, you are not the owner of that tag."

        if channel_id not in permissions_data.get_allowed_channels("tag edit"):
            await self.bot.say(bad_permissions)
            return

        owner = tag_data.get_tag_owner(name)
        if ctx.message.author.id != owner and owner != None:
            await self.bot.say(bad_owner)
            return

        tag_data.edit_tag(ctx.message.author.id, name)
        await self.bot.say("Editing tag.")

    @tag.command(pass_context=True, aliases=['s'])
    async def set(self, ctx, *, content):
        """Set content of tag owner is currently editing"""
        if "Regular" not in [x.name for x in ctx.message.author.roles]:
            await self.bot.say("You need to have the Regular role to use that command.")
            return
        channel_id = ctx.message.channel.id

        bad_permissions = "Sorry, you cannot use that command here."
        if channel_id not in permissions_data.get_allowed_channels("tag set"):
            await self.bot.say(bad_permissions)
            return

        tag_data.set_tag_content(ctx.message.author.id, content)
        await self.bot.say("Tag successfully set.")

    @tag.command(pass_context=True, aliases=['l'])
    async def list(self, ctx, *, owner):
        """Display tag names belonging to an owner"""
        channel_id = ctx.message.channel.id

        bad_permissions = "Sorry, you cannot use that command here."
        if channel_id not in permissions_data.get_allowed_channels("tag list"):
            await self.bot.say(bad_permissions)
            return

        member = discord.utils.find(lambda m: owner.lower() in
                                    m.name.lower(),
                                    ctx.message.channel.server.members)
        if member is None:
            member = discord.utils.find(lambda m: owner.lower() in 
                                        m.display_name.lower(),
                                        ctx.message.channel.server.members)

        tags = tag_data.list_tags(member.id)

        await self.bot.say("; ".join(tags))

    @tag.command(pass_context=True)
    async def search(self, ctx, *, name):
        """Search tags by name"""
        channel_id = ctx.message.channel.id

        bad_permissions = "Sorry, you cannot use that command here."
        if channel_id not in permissions_data.get_allowed_channels("tag search"):
            await self.bot.say(bad_permissions)
            return

        tags = tag_data.search_tags(name)

        await self.bot.say("; ".join(tags))

    @tag.command(pass_context=True)
    async def owner(self, ctx, *, name):
        """Find owner of a tag"""
        channel_id = ctx.message.channel.id

        bad_permissions = "Sorry, you cannot use that command here."
        if channel_id not in permissions_data.get_allowed_channels("tag owner"):
            await self.bot.say(bad_permissions)
            return

        owner_id = tag_data.find_tag_owner(name)
        owner = ctx.message.server.get_member(owner_id)

        await self.bot.say("Tag belongs to " + owner.name + 
                           "#" + owner.discriminator)

    @tag.command(pass_context=True)
    async def delete(self, ctx, *, name):
        """Delete a tag"""
        channel_id = ctx.message.channel.id

        bad_permissions = "Sorry, you cannot use that command here."
        if channel_id not in permissions_data.get_allowed_channels("tag delete"):
            await self.bot.say(bad_permissions)
            return

        owner_id = tag_data.find_tag_owner(name)
        if owner_id == ctx.message.author.id:
            tag_data.delete_tag(name)
            await self.bot.say("Tag successfully deleted.")
        else:
            await self.bot.say("Sorry, you are not the owner of that tag.")

    @commands.command(pass_context=True)
    async def chart(self, ctx):
        """Display any chart content from owner"""
        channel_id = ctx.message.channel.id

        bad_permissions = "Sorry, you cannot use that command here."
        if channel_id not in permissions_data.get_allowed_channels("chart"):
            await self.bot.say(bad_permissions)
            return
        
        if len(ctx.message.content.split(" ")) == 1:
            member = ctx.message.author
        else:
            owner = ctx.message.content[7:]
            member = discord.utils.find(lambda m: owner.lower() in
                                        m.name.lower(),
                                        ctx.message.channel.server.members)
            if member is None:
                member = discord.utils.find(lambda m: owner.lower() in 
                                            m.display_name.lower(),
                                            ctx.message.channel.server.members)

        content = tag_data.get_chart_content(member.id)
        await self.bot.say(content)

    @commands.command(pass_context=True)
    async def setchart(self, ctx, *, content):
        if "Regular" not in [x.name for x in ctx.message.author.roles]:
            await self.bot.say("You need to have the Regular role to use that command.")
            return
        """Set content of chart"""
        channel_id = ctx.message.channel.id

        bad_permissions = "Sorry, you cannot use that command here."
        if channel_id not in permissions_data.get_allowed_channels("chart set"):
            await self.bot.say(bad_permissions)
            return

        tag_data.set_chart_content(ctx.message.author.id, content)
        await self.bot.say("Chart successfully set.")

    @commands.command(pass_context=True)
    async def rym(self, ctx):
        """Display any rym content from owner"""
        channel_id = ctx.message.channel.id

        bad_permissions = "Sorry, you cannot use that command here."
        if channel_id not in permissions_data.get_allowed_channels("chart"):
            await self.bot.say(bad_permissions)
            return
        
        if len(ctx.message.content.split(" ")) == 1:
            member = ctx.message.author
        else:
            owner = ctx.message.content[7:]
            member = discord.utils.find(lambda m: owner.lower() in
                                        m.name.lower(),
                                        ctx.message.channel.server.members)
            if member is None:
                member = discord.utils.find(lambda m: owner.lower() in 
                                            m.display_name.lower(),
                                            ctx.message.channel.server.members)

        content = tag_data.get_rym_content(member.id)
        await self.bot.say("https://rateyourmusic.com/~" + content)

    @commands.command(pass_context=True)
    async def setrym(self, ctx, *, content):
        if "Regular" not in [x.name for x in ctx.message.author.roles]:
            await self.bot.say("You need to have the Regular role to use that command.")
            return
        """Set content of rym"""
        channel_id = ctx.message.channel.id

        bad_permissions = "Sorry, you cannot use that command here."
        if channel_id not in permissions_data.get_allowed_channels("chart set"):
            await self.bot.say(bad_permissions)
            return

        tag_data.set_rym_content(ctx.message.author.id, content)
        await self.bot.say("RYM successfully set.")


def setup(bot):
    """Attach the lastfm cog to a bot"""
    cog = TagCog(bot)
    bot.add_cog(cog)