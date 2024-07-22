import discord

from musicbot.utils.constants import EMBED_COLOR

def create_song_embed(title, artist, url, duration):
    """Creates a Discord embed message for displaying information about a song.

    Args:
        title: The title of the song.
        artist: The artist of the song.
        url: The URL of the song.
        duration: The duration of the song.

    Returns:
        A Discord embed message object.
    """
    embed = discord.Embed(
        title=title,
        description=f"By {artist}",
        color=EMBED_COLOR
    )
    embed.add_field(name="URL", value=url, inline=False)
    embed.add_field(name="Duration", value=duration, inline=False)
    return embed

def create_queue_embed(queue):
    """Creates a Discord embed message for displaying the current queue.

    Args:
        queue: The queue of songs.

    Returns:
        A Discord embed message object.
    """
    embed = discord.Embed(
        title="Current Queue",
        description="Here's the current queue:",
        color=EMBED_COLOR
    )
    for i, song in enumerate(queue.songs):
        embed.add_field(name=f"{i+1}. {song.title}", value=f"By {song.artist}", inline=False)
    return embed

def create_error_embed(message):
    """Creates a Discord embed message for displaying error messages.

    Args:
        message: The error message.

    Returns:
        A Discord embed message object.
    """
    embed = discord.Embed(
        title="Error",
        description=message,
        color=EMBED_COLOR
    )
    return embed