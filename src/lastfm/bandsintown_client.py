import requests
import time
from typing import List, Optional, Dict, Any
from .models import Event
from ..utils.config import Config


class BandsintownClient:
    """Client for interacting with the Bandsintown API"""
    
    def __init__(self, app_id: str):
        self.app_id = app_id
        self.base_url = 'https://rest.bandsintown.com'
        self.session = requests.Session()
    
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make a request to the Bandsintown API"""
        params['app_id'] = self.app_id
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if isinstance(data, dict) and 'error' in data:
                raise Exception(f"Bandsintown API error: {data['error']}")
            
            return data
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")
    
    def get_artist_events(self, artist_name: str, location: str = None) -> List[Event]:
        """Get events for a specific artist"""
        # URL encode the artist name
        import urllib.parse
        encoded_artist = urllib.parse.quote(artist_name)
        
        endpoint = f"artists/{encoded_artist}/events"
        params = {}
        
        if location:
            params['location'] = location
        
        data = self._make_request(endpoint, params)
        
        # Handle single event case
        if isinstance(data, dict):
            data = [data]
        
        events = []
        for event_data in data:
            # Parse date
            event_date = None
            if 'datetime' in event_data:
                try:
                    # Bandsintown uses ISO format like "2024-12-25T20:00:00"
                    event_date = event_data['datetime']
                except:
                    pass
            
            # Extract venue info
            venue_name = 'Unknown Venue'
            venue_city = 'Unknown City'
            venue_country = 'US'
            
            if 'venue' in event_data:
                venue = event_data['venue']
                venue_name = venue.get('name', 'Unknown Venue')
                venue_city = venue.get('city', 'Unknown City')
                venue_country = venue.get('country', 'US')
            
            # Get event name
            event_name = event_data.get('title', 'Unknown Event')
            
            # Get event URL
            event_url = event_data.get('url')
            
            # Get event description
            description = event_data.get('description')
            
            # Get event image
            image_url = None
            if 'artist' in event_data and 'image_url' in event_data['artist']:
                image_url = event_data['artist']['image_url']
            
            # Extract artists (usually just the main artist for Bandsintown)
            artists = [artist_name]
            if 'artist' in event_data and 'name' in event_data['artist']:
                artists = [event_data['artist']['name']]
            
            event = Event(
                title=event_name,
                venue=venue_name,
                city=venue_city,
                country=venue_country,
                date=event_date,
                url=event_url,
                description=description,
                image_url=image_url,
                artists=artists
            )
            events.append(event)
        
        return events
    
    def search_events_by_location(self, location: str, radius: int = 25) -> List[Event]:
        """Search for events by location (this is a workaround since Bandsintown doesn't have direct location search)"""
        # Bandsintown doesn't have a direct location search API
        # This would require searching by known artists, which we'll do in the scraper
        return []
    
    def get_artist_info(self, artist_name: str) -> Optional[Dict[str, Any]]:
        """Get artist information"""
        import urllib.parse
        encoded_artist = urllib.parse.quote(artist_name)
        
        endpoint = f"artists/{encoded_artist}"
        params = {}
        
        try:
            data = self._make_request(endpoint, params)
            return data
        except:
            return None
