import discord
from discord.ext import commands
from discord.ext.commands import Cog

from musicbot.utils.constants import RATE_LIMIT_PER_SECOND, BLACKLIST_URLS
from musicbot.utils.embed_builder import create_error_embed


class ModerationCog(Cog):
    """Cog for moderation features."""

    def __init__(self, bot):
        self.bot = bot
        self.message_rate_limits = {}  # {user_id: last_message_time}

    @Cog.listener()
    async def on_message(self, message):
        """Handles incoming messages, checking for spam or inappropriate content."""
        if message.author == self.bot.user:
            return  # Ignore messages sent by the bot itself

        # Rate limiting
        user_id = message.author.id
        if user_id in self.message_rate_limits:
            last_message_time = self.message_rate_limits[user_id]
            time_since_last_message = message.created_at - last_message_time
            if time_since_last_message.total_seconds() < 1 / RATE_LIMIT_PER_SECOND:
                await message.delete()
                await message.channel.send(embed=create_error_embed(
                    "You are sending messages too quickly. Please slow down."
                ))
                return
        self.message_rate_limits[user_id] = message.created_at

        # Blacklist URLs
        for url in BLACKLIST_URLS:
            if url in message.content:
                await message.delete()
                await message.channel.send(embed=create_error_embed(
                    "This link is not allowed in the server."
                ))
                return

        # Content filtering
        # TODO: Implement content moderation logic using a library or API
        # Example:
        # if check_inappropriate_content(message.content):
        #     await message.delete()
        #     await message.channel.send(embed=create_error_embed(
        #         "This message contains inappropriate content and has been removed."
        #     ))
        #     return

    @commands.command(name="kick", help="Kicks a user from the server.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kicks a member from the server."""
        try:
            await member.kick(reason=reason)
            await ctx.send(f"Successfully kicked {member.mention} from the server.")
        except discord.Forbidden:
            await ctx.send(embed=create_error_embed("I do not have permissions to kick members."))

    @commands.command(name="ban", help="Bans a user from the server.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Bans a member from the server."""
        try:
            await member.ban(reason=reason)
            await ctx.send(f"Successfully banned {member.mention} from the server.")
        except discord.Forbidden:
            await ctx.send(embed=create_error_embed("I do not have permissions to ban members."))

    @commands.command(name="mute", help="Mutes a user in the server.")
    @commands.has_permissions(manage_channels=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        """Mutes a member in the server."""
        try:
            await member.edit(mute=True, reason=reason)
            await ctx.send(f"Successfully muted {member.mention} in the server.")
        except discord.Forbidden:
            await ctx.send(embed=create_error_embed("I do not have permissions to mute members."))

    @commands.command(name="unmute", help="Unmutes a user in the server.")
    @commands.has_permissions(manage_channels=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        """Unmutes a member in the server."""
        try:
            await member.edit(mute=False, reason=reason)
            await ctx.send(f"Successfully unmuted {member.mention} in the server.")
        except discord.Forbidden:
            await ctx.send(embed=create_error_embed("I do not have permissions to unmute members."))