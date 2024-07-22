import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import Cog
from discord.utils import get

from musicbot.utils.constants import ALLOWED_SOURCES, DEFAULT_VOLUME, MAX_QUEUE_LENGTH
from musicbot.utils.embed_builder import create_song_embed, create_queue_embed, create_error_embed
from musicbot.utils.music_source import (
    get_youtube_info,
    get_spotify_info,
    get_soundcloud_info,
)
from musicbot.utils.queue import Queue

class MusicCog(Cog):
    """Cog for music-related commands and functionality."""

    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None
        self.queue = Queue()
        self.current_song = None
        self.loop_mode = False

    @commands.command(name="play", help="Plays a song from YouTube, Spotify, or SoundCloud.")
    async def play(self, ctx, *, query):
        """Plays a song from YouTube, Spotify, or SoundCloud."""
        try:
            if "youtube.com" in query:
                song_info = await get_youtube_info(query)
            elif "spotify.com" in query:
                song_info = await get_spotify_info(query)
            elif "soundcloud.com" in query:
                song_info = await get_soundcloud_info(query)
            else:
                await ctx.send(
                    embed=create_error_embed(
                        f"Invalid URL or query. Supported sources: {ALLOWED_SOURCES}"
                    )
                )
                return

            if not self.voice_client:
                channel = ctx.author.voice.channel
                if not channel:
                    await ctx.send(
                        embed=create_error_embed(
                            "You need to be in a voice channel to play music."
                        )
                    )
                    return
                self.voice_client = await channel.connect()

            song = Song(
                title=song_info["title"],
                artist=song_info.get("artist", "Unknown Artist"),
                url=song_info["url"],
                duration=song_info.get("duration", "Unknown"),
            )
            await self.queue.add(song)

            if self.current_song is None:
                await self.play_next_song(ctx)

            await ctx.send(
                embed=create_song_embed(
                    song.title, song.artist, song.url, song.duration
                )
            )

        except Exception as e:
            await ctx.send(embed=create_error_embed(f"Error playing song: {e}"))
            print(f"Error playing song: {e}")

    @commands.command(name="skip", help="Skips the current song.")
    async def skip(self, ctx):
        """Skips the current song."""
        if self.voice_client and self.queue:
            self.voice_client.stop()
            await self.play_next_song(ctx)
            await ctx.send(embed=create_song_embed("Skipped", ""))

    @commands.command(name="stop", help="Stops the music and clears the queue.")
    async def stop(self, ctx):
        """Stops the music and clears the queue."""
        if self.voice_client:
            self.voice_client.stop()
            await self.voice_client.disconnect()
            self.voice_client = None
            self.queue.clear()
            self.current_song = None
            await ctx.send(embed=create_error_embed("Stopped and cleared the queue."))

    @commands.command(name="pause", help="Pauses the current song.")
    async def pause(self, ctx):
        """Pauses the current song."""
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.pause()
            await ctx.send(embed=create_error_embed("Paused."))

    @commands.command(name="resume", help="Resumes the paused song.")
    async def resume(self, ctx):
        """Resumes the paused song."""
        if self.voice_client and self.voice_client.is_paused():
            self.voice_client.resume()
            await ctx.send(embed=create_error_embed("Resumed."))

    @commands.command(name="volume", help="Sets the playback volume.")
    async def volume(self, ctx, volume: float):
        """Sets the playback volume."""
        if self.voice_client:
            if 0 <= volume <= 1:
                self.voice_client.source.volume = volume
                await ctx.send(embed=create_error_embed(f"Volume set to {volume:.2f}."))
            else:
                await ctx.send(
                    embed=create_error_embed(
                        "Volume must be between 0 and 1 (inclusive)."
                    )
                )

    @commands.command(name="queue", help="Displays the current queue.")
    async def queue(self, ctx):
        """Displays the current queue."""
        if self.queue.is_empty():
            await ctx.send(embed=create_error_embed("The queue is empty."))
        else:
            await ctx.send(embed=create_queue_embed(self.queue))

    @commands.command(name="nowplaying", help="Shows information about the current song.")
    async def nowplaying(self, ctx):
        """Shows information about the current song."""
        if self.current_song:
            await ctx.send(
                embed=create_song_embed(
                    self.current_song.title,
                    self.current_song.artist,
                    self.current_song.url,
                    self.current_song.duration,
                )
            )
        else:
            await ctx.send(embed=create_error_embed("No song is currently playing."))

    @commands.command(name="loop", help="Enables or disables song looping.")
    async def loop(self, ctx):
        """Enables or disables song looping."""
        self.loop_mode = not self.loop_mode
        if self.loop_mode:
            await ctx.send(embed=create_error_embed("Looping enabled."))
        else:
            await ctx.send(embed=create_error_embed("Looping disabled."))

    @commands.command(name="shuffle", help="Shuffles the queue.")
    async def shuffle(self, ctx):
        """Shuffles the queue."""
        if self.queue:
            self.queue.shuffle()
            await ctx.send(embed=create_error_embed("Queue shuffled."))
        else:
            await ctx.send(embed=create_error_embed("The queue is empty."))

    @commands.command(name="remove", help="Removes a specific song from the queue.")
    async def remove(self, ctx, index: int):
        """Removes a specific song from the queue."""
        if self.queue:
            try:
                song = self.queue.remove(index - 1)
                await ctx.send(
                    embed=create_error_embed(
                        f"Removed '{song.title}' from the queue."
                    )
                )
            except IndexError:
                await ctx.send(
                    embed=create_error_embed(
                        f"Invalid song index. Please enter a valid number between 1 and {len(self.queue)}."
                    )
                )
        else:
            await ctx.send(embed=create_error_embed("The queue is empty."))

    @commands.command(name="clear", help="Clears the entire queue.")
    async def clear(self, ctx):
        """Clears the entire queue."""
        if self.queue:
            self.queue.clear()
            await ctx.send(embed=create_error_embed("Queue cleared."))
        else:
            await ctx.send(embed=create_error_embed("The queue is empty."))

    async def play_next_song(self, ctx):
        """Plays the next song in the queue."""
        if self.voice_client:
            if self.queue.is_empty():
                await self.voice_client.disconnect()
                self.voice_client = None
                self.current_song = None
                await ctx.send(embed=create_error_embed("Queue is empty."))
                return

            self.current_song = self.queue.next()
            if self.loop_mode:
                await self.queue.add(self.current_song)

            try:
                self.voice_client.play(
                    discord.FFmpegOpusAudio(self.current_song.url),
                    after=lambda e: asyncio.run_coroutine_threadsafe(
                        self.play_next_song(ctx), self.bot.loop
                    ).result(),
                )
            except discord.errors.ClientException:
                await ctx.send(
                    embed=create_error_embed(
                        f"Error playing song: {self.current_song.title}"
                    )
                )
                self.current_song = None
                self.queue.next()  # Move to the next song
            else:
                await ctx.send(
                    embed=create_song_embed(
                        self.current_song.title,
                        self.current_song.artist,
                        self.current_song.url,
                        self.current_song.duration,
                    )
                )
                await self.voice_client.source.volume = DEFAULT_VOLUME

    async def cog_check(self, ctx):
        """Checks if the user is in a voice channel before executing commands."""
        if ctx.author.voice is None:
            await ctx.send(
                embed=create_error_embed("You must be in a voice channel to use this command.")
            )
            return False
        return True

class Song:
    """Represents a song object."""

    def __init__(self, title, artist, url, duration):
        self.title = title
        self.artist = artist
        self.url = url
        self.duration = duration

    def __str__(self):
        return f"{self.title} by {self.artist}"