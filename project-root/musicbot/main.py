import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from musicbot.cogs import MusicCog, ErrorHandlerCog, ModerationCog
from musicbot.utils.constants import PREFIX, LOG_LEVEL

load_dotenv()

# Create a new Discord bot instance
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Load cogs
bot.add_cog(MusicCog(bot))
bot.add_cog(ErrorHandlerCog(bot))
bot.add_cog(ModerationCog(bot))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))