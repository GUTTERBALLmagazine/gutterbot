from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from urllib.parse import urlparse


@dataclass
class Artist:
    """Represents a musical artist"""
    name: str
    mbid: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None
    playcount: Optional[int] = None
    
    def __str__(self) -> str:
        return self.name


@dataclass
class Event:
    """Represents a music event/concert"""
    title: str
    venue: str
    city: str
    country: str
    date: datetime
    url: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    artists: List[str] = None
    
    def __post_init__(self):
        if self.artists is None:
            self.artists = []
    
    def __str__(self) -> str:
        return f"{self.title} at {self.venue} on {self.date.strftime('%Y-%m-%d')}"


@dataclass
class UserListeningData:
    """Represents a user's listening history data"""
    username: str
    artists: List[Artist]
    total_artists: int
    period: str  # e.g., "7day", "1month", "3month", "6month", "12month", "overall"
    
    def get_artist_names(self) -> List[str]:
        """Get list of artist names for easy matching"""
        return [artist.name for artist in self.artists]
