import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from typing import Dict, Optional

from musicbot.utils.constants import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

client_credentials_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


async def get_spotify_track(track_id: str) -> Optional[Dict]:
    """
    Retrieves information about a Spotify track by its ID.

    Args:
        track_id: The Spotify track ID.

    Returns:
        A dictionary containing track information, or None if the track is not found.
    """
    try:
        track = sp.track(track_id)
        track_info = {
            "title": track["name"],
            "artist": ", ".join([artist["name"] for artist in track["artists"]]),
            "url": track["external_urls"]["spotify"],
            "duration": track["duration_ms"],
        }
        return track_info
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching Spotify track info: {e}")
        return None


async def get_spotify_playlist(playlist_id: str) -> Optional[Dict]:
    """
    Retrieves information about a Spotify playlist by its ID.

    Args:
        playlist_id: The Spotify playlist ID.

    Returns:
        A dictionary containing playlist information, or None if the playlist is not found.
    """
    try:
        playlist = sp.playlist(playlist_id)
        playlist_info = {
            "title": playlist["name"],
            "description": playlist["description"],
            "url": playlist["external_urls"]["spotify"],
        }
        return playlist_info
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching Spotify playlist info: {e}")
        return None


async def get_spotify_info(query: str) -> Optional[Dict]:
    """
    Retrieves information about a Spotify track or playlist from its URL or ID.

    Args:
        query: The Spotify track URL, playlist URL, or ID.

    Returns:
        A dictionary containing track or playlist information, or None if the item is not found.
    """
    if "spotify.com/track" in query or "open.spotify.com/track" in query:
        # Extract track ID from URL
        track_id = query.split("/")[-1].split("?")[0]
        return await get_spotify_track(track_id)
    elif "spotify.com/playlist" in query or "open.spotify.com/playlist" in query:
        # Extract playlist ID from URL
        playlist_id = query.split("/")[-1].split("?")[0]
        return await get_spotify_playlist(playlist_id)
    else:
        print(f"Invalid Spotify URL or ID: {query}")
        return None