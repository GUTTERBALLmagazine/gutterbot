import requests
import time
from typing import List, Optional, Dict, Any
from .models import Artist, Event, UserListeningData
from ..utils.config import Config


class LastFMClient:
    """Client for interacting with the Last.fm API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = Config.LASTFM_API_URL
        self.session = requests.Session()
    
    def _make_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make a request to the Last.fm API"""
        params.update({
            'api_key': self.api_key,
            'format': 'json',
            'method': method
        })
        
        try:
            response = self.session.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'error' in data:
                raise Exception(f"Last.fm API error: {data['message']}")
            
            return data
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")
    
    def get_user_top_artists(self, username: str, period: str = '1month', limit: int = 50) -> UserListeningData:
        """Get a user's top artists for a given period"""
        params = {
            'user': username,
            'period': period,
            'limit': limit
        }
        
        data = self._make_request('user.gettopartists', params)
        artists_data = data.get('topartists', {}).get('artist', [])
        
        # Handle single artist case (API returns dict instead of list)
        if isinstance(artists_data, dict):
            artists_data = [artists_data]
        
        artists = []
        for artist_data in artists_data:
            artist = Artist(
                name=artist_data.get('name', ''),
                mbid=artist_data.get('mbid'),
                url=artist_data.get('url'),
                playcount=int(artist_data.get('playcount', 0))
            )
            artists.append(artist)
        
        return UserListeningData(
            username=username,
            artists=artists,
            total_artists=len(artists),
            period=period
        )
    
    def get_events_by_location(self, city: str, country: str, page: int = 1, limit: int = 50) -> List[Event]:
        """Get events for a specific location"""
        params = {
            'location': f"{city},{country}",
            'page': page,
            'limit': limit
        }
        
        data = self._make_request('geo.getevents', params)
        events_data = data.get('events', {}).get('event', [])
        
        # Handle single event case
        if isinstance(events_data, dict):
            events_data = [events_data]
        
        events = []
        for event_data in events_data:
            # Parse date
            date_str = event_data.get('startDate', '')
            event_date = None
            if date_str:
                try:
                    # Last.fm uses format like "Wed, 15 Nov 2023 20:00:00 +0000"
                    event_date = time.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
                    event_date = time.mktime(event_date)
                    event_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(event_date))
                except ValueError:
                    # Fallback for different date formats
                    pass
            
            # Extract artists
            artists = []
            if 'artists' in event_data:
                artists_data = event_data['artists']
                if isinstance(artists_data, dict):
                    artists_data = [artists_data]
                artists = [artist.get('name', '') for artist in artists_data if artist.get('name')]
            
            event = Event(
                title=event_data.get('title', ''),
                venue=event_data.get('venue', {}).get('name', ''),
                city=event_data.get('venue', {}).get('location', {}).get('city', city),
                country=event_data.get('venue', {}).get('location', {}).get('country', country),
                date=event_date,
                url=event_data.get('url'),
                description=event_data.get('description'),
                artists=artists
            )
            events.append(event)
        
        return events
    
    def search_artist(self, artist_name: str) -> Optional[Artist]:
        """Search for a specific artist"""
        params = {
            'artist': artist_name,
            'limit': 1
        }
        
        data = self._make_request('artist.search', params)
        artists_data = data.get('results', {}).get('artistmatches', {}).get('artist', [])
        
        if not artists_data:
            return None
        
        # Handle single result case
        if isinstance(artists_data, dict):
            artists_data = [artists_data]
        
        artist_data = artists_data[0]
        return Artist(
            name=artist_data.get('name', ''),
            mbid=artist_data.get('mbid'),
            url=artist_data.get('url')
        )
