import discord
from discord.ext import commands
from discord.ext.commands import Cog, CommandNotFound, MissingRequiredArgument
import logging

from musicbot.utils.embed_builder import create_error_embed

logger = logging.getLogger(__name__)


class ErrorHandlerCog(Cog):
    """Cog for handling errors within the bot."""

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        """Handles errors that occur when executing commands."""
        if isinstance(error, CommandNotFound):
            await ctx.send(embed=create_error_embed(f"Command not found: {ctx.invoked_with}"))
            logger.warning(f"Command not found: {ctx.invoked_with}")
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send(embed=create_error_embed(f"Missing required argument: {error.param.name}"))
            logger.warning(f"Missing required argument: {error.param.name}")
        elif isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(embed=create_error_embed(f"This command is on cooldown. Try again in {error.retry_after:.2f} seconds."))
            logger.info(f"Command '{ctx.command}' is on cooldown. Retry after {error.retry_after:.2f} seconds.")
        elif isinstance(error, commands.errors.CheckFailure):
            await ctx.send(embed=create_error_embed("You do not have permission to use this command."))
            logger.warning(f"CheckFailure in command '{ctx.command}'. User lacks permissions.")
        elif isinstance(error, discord.errors.Forbidden):
            await ctx.send(embed=create_error_embed("I do not have permission to perform this action."))
            logger.warning(f"Discord Forbidden error in command '{ctx.command}'. Bot lacks permissions.")
        else:
            await ctx.send(embed=create_error_embed(f"An error occurred: {error}"))
            logger.exception(f"Unhandled error in command '{ctx.command}': {error}")