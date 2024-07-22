import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional

from musicbot.utils.constants import SOUNDCLOUD_CLIENT_ID, SOUNDCLOUD_CLIENT_SECRET


def _get_soundcloud_api_url(url: str) -> str:
    """
    Constructs the SoundCloud API URL for retrieving track information.

    Args:
        url: The URL of the SoundCloud track.

    Returns:
        The SoundCloud API URL.
    """
    return f"https://api.soundcloud.com/resolve?url={url}&client_id={SOUNDCLOUD_CLIENT_ID}"


async def get_soundcloud_info(url: str) -> Optional[Dict]:
    """
    Retrieves information about a SoundCloud track from its URL.

    Args:
        url: The URL of the SoundCloud track.

    Returns:
        A dictionary containing track information, or None if the track is not found.
    """
    try:
        response = requests.get(_get_soundcloud_api_url(url))
        response.raise_for_status()  # Raise an exception for bad status codes

        data = response.json()

        if data.get("kind") == "track":
            track_info = {
                "title": data.get("title"),
                "artist": data.get("user", {}).get("username"),
                "url": data.get("permalink_url"),
                "duration": data.get("duration"),
            }
            return track_info
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching SoundCloud track info: {e}")
        return None


async def search_soundcloud(query: str) -> Optional[Dict]:
    """
    Searches for SoundCloud tracks based on a query.

    Args:
        query: The search query.

    Returns:
        A dictionary containing information about the first search result, or None if no results are found.
    """
    try:
        search_url = f"https://soundcloud.com/search/sounds?q={query}"
        response = requests.get(search_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        first_result = soup.find("a", class_="soundTitle__title sc-truncate")

        if first_result:
            track_url = first_result.get("href")
            if track_url:
                return await get_soundcloud_info(f"https://soundcloud.com{track_url}")
            else:
                return None
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error searching SoundCloud: {e}")
        return None