import requests
from typing import Dict, Optional

from musicbot.utils.constants import YOUTUBE_API_KEY


def _get_youtube_api_url(query: str) -> str:
    """
    Constructs the YouTube Data API v3 URL for searching videos.

    Args:
        query: The search query.

    Returns:
        The YouTube Data API v3 URL.
    """
    return f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={YOUTUBE_API_KEY}&type=video"


async def search_youtube(query: str) -> Optional[Dict]:
    """
    Searches for YouTube videos based on a query.

    Args:
        query: The search query.

    Returns:
        A dictionary containing information about the first search result, or None if no results are found.
    """
    try:
        response = requests.get(_get_youtube_api_url(query))
        response.raise_for_status()  # Raise an exception for bad status codes

        data = response.json()
        if "items" in data and data["items"]:
            first_result = data["items"][0]
            video_info = {
                "title": first_result["snippet"]["title"],
                "artist": first_result["snippet"].get("channelTitle", "Unknown Artist"),
                "url": f"https://www.youtube.com/watch?v={first_result['id']['videoId']}",
                "duration": first_result["snippet"].get("duration"),
            }
            return video_info
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error searching YouTube: {e}")
        return None


async def get_youtube_video(video_id: str) -> Optional[Dict]:
    """
    Retrieves information about a YouTube video by its ID.

    Args:
        video_id: The YouTube video ID.

    Returns:
        A dictionary containing video information, or None if the video is not found.
    """
    try:
        response = requests.get(
            f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails&id={video_id}&key={YOUTUBE_API_KEY}"
        )
        response.raise_for_status()  # Raise an exception for bad status codes

        data = response.json()
        if "items" in data and data["items"]:
            video_info = {
                "title": data["items"][0]["snippet"]["title"],
                "artist": data["items"][0]["snippet"].get("channelTitle", "Unknown Artist"),
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "duration": data["items"][0]["contentDetails"]["duration"],
            }
            return video_info
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching YouTube video info: {e}")
        return None


async def get_youtube_playlist(playlist_id: str) -> Optional[Dict]:
    """
    Retrieves information about a YouTube playlist by its ID.

    Args:
        playlist_id: The YouTube playlist ID.

    Returns:
        A dictionary containing playlist information, or None if the playlist is not found.
    """
    try:
        response = requests.get(
            f"https://www.googleapis.com/youtube/v3/playlists?part=snippet,contentDetails&id={playlist_id}&key={YOUTUBE_API_KEY}"
        )
        response.raise_for_status()  # Raise an exception for bad status codes

        data = response.json()
        if "items" in data and data["items"]:
            playlist_info = {
                "title": data["items"][0]["snippet"]["title"],
                "description": data["items"][0]["snippet"].get("description"),
                "url": f"https://www.youtube.com/playlist?list={playlist_id}",
            }
            return playlist_info
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching YouTube playlist info: {e}")
        return None