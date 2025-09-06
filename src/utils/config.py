import os
from typing import List


class Config:
    """Configuration management for gutterbot"""
    
    # last.fm api configuration
    LASTFM_API_URL = 'http://ws.audioscrobbler.com/2.0/'
    
    # atlanta location settings
    ATLANTA_CITY = 'Atlanta'
    ATLANTA_COUNTRY = 'United States'
    
    # user settings
    DEFAULT_USERS: List[str] = []
    
    # matching settings
    SIMILARITY_THRESHOLD = 0.85  # for fuzzy string matching (increased for stricter matching)
    MAX_ARTISTS_TO_SEARCH = 30  # maximum number of artists to search for events
    ARTIST_SEARCH_DELAY = 0.1  # delay between artist searches (seconds)
    
    @classmethod
    def get_api_key(cls) -> str:
        """Get last.fm api key from environment"""
        return os.getenv('LASTFM_API_KEY', '')
    
    @classmethod
    def get_ticketmaster_api_key(cls) -> str:
        """Get ticketmaster api key from environment"""
        return os.getenv('TICKETMASTER_API_KEY', '')
    
    @classmethod
    def get_bandsintown_app_id(cls) -> str:
        """Get bandsintown app id from environment"""
        # Try both BANDSINTOWN_APP_ID and BANDSINTOWN_API_KEY for compatibility
        return os.getenv('BANDSINTOWN_APP_ID', '') or os.getenv('BANDSINTOWN_API_KEY', '')
    
    @classmethod
    def get_discord_bot_token(cls) -> str:
        """Get discord bot token from environment"""
        return os.getenv('DISCORD_BOT_TOKEN', '')
    
    @classmethod
    def get_discord_channel_id(cls) -> str:
        """Get discord channel id from environment"""
        return os.getenv('DISCORD_CHANNEL_ID', '')
    
    @classmethod
    def get_discord_guild_id(cls) -> str:
        """Get discord guild id from environment"""
        return os.getenv('DISCORD_GUILD_ID', '')
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present"""
        lastfm_key = cls.get_api_key()
        if not lastfm_key:
            raise ValueError("LASTFM_API_KEY environment variable is required")
        
        ticketmaster_key = cls.get_ticketmaster_api_key()
        if not ticketmaster_key:
            raise ValueError("TICKETMASTER_API_KEY environment variable is required")
        
        return True
    
    @classmethod
    def get_users(cls) -> List[str]:
        """Get list of last.fm usernames to track"""
        users_env = os.getenv('LASTFM_USERS', '')
        if users_env:
            return [user.strip() for user in users_env.split(',') if user.strip()]
        return cls.DEFAULT_USERS
