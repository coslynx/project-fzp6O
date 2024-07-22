import os

# Bot Configuration
PREFIX = "!"  # Default command prefix
ALLOWED_SOURCES = ["youtube", "spotify", "soundcloud"]  # Allowed music sources
DEFAULT_VOLUME = 0.5  # Default playback volume
MAX_QUEUE_LENGTH = 10  # Maximum number of songs in the queue
LOG_LEVEL = "INFO"  # Logging level

# API Keys
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SOUNDCLOUD_CLIENT_ID = os.getenv("SOUNDCLOUD_CLIENT_ID")
SOUNDCLOUD_CLIENT_SECRET = os.getenv("SOUNDCLOUD_CLIENT_SECRET")
GENIUS_API_KEY = os.getenv("GENIUS_API_KEY")
MUSICMATCH_API_KEY = os.getenv("MUSICMATCH_API_KEY")

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# Check if required environment variables are set
if not all([
    DISCORD_TOKEN,
    YOUTUBE_API_KEY,
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    SOUNDCLOUD_CLIENT_ID,
    SOUNDCLOUD_CLIENT_SECRET,
    GENIUS_API_KEY,
    MUSICMATCH_API_KEY,
]):
    raise ValueError(
        "Missing required environment variables. Please set them in the .env file."
    )