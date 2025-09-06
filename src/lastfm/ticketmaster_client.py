import requests
import time
from typing import List, Optional, Dict, Any
from .models import Event
from ..utils.config import Config


class TicketmasterClient:
    """Client for interacting with the Ticketmaster Discovery API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = 'https://app.ticketmaster.com/discovery/v2'
        self.session = requests.Session()
    
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make a request to the Ticketmaster API"""
        params['apikey'] = self.api_key
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'errors' in data:
                raise Exception(f"Ticketmaster API error: {data['errors']}")
            
            return data
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")
    
    def get_events_by_location(self, city: str, state: str = None, country: str = 'US', 
                              classification: str = 'music', size: int = 50) -> List[Event]:
        """Get events for a specific location"""
        params = {
            'city': city,
            'countryCode': country,
            'classificationName': classification,
            'size': size,
            'sort': 'date,asc'  # sort by date ascending (upcoming first)
        }
        
        if state:
            params['stateCode'] = state
        
        data = self._make_request('events.json', params)
        events_data = data.get('_embedded', {}).get('events', [])
        
        events = []
        for event_data in events_data:
            # Parse date
            event_date = None
            if 'dates' in event_data and 'start' in event_data['dates']:
                start_date = event_data['dates']['start']
                if 'dateTime' in start_date:
                    # Parse ISO 8601 datetime
                    try:
                        event_date = start_date['dateTime']
                    except ValueError:
                        pass
                elif 'localDate' in start_date:
                    # Fallback to local date
                    event_date = start_date['localDate']
            
            # Extract venue info
            venue_name = 'Unknown Venue'
            venue_city = city
            venue_country = country
            
            if 'venues' in event_data.get('_embedded', {}):
                venues = event_data['_embedded']['venues']
                if venues:
                    venue = venues[0]
                    venue_name = venue.get('name', 'Unknown Venue')
                    venue_city = venue.get('city', {}).get('name', city)
                    venue_country = venue.get('country', {}).get('name', country)
            elif 'venue' in event_data:
                venue = event_data['venue']
                venue_name = venue.get('name', 'Unknown Venue')
                venue_city = venue.get('city', {}).get('name', city)
                venue_country = venue.get('country', {}).get('name', country)
            
            # Extract artists/attractions
            artists = []
            if 'attractions' in event_data.get('_embedded', {}):
                attractions = event_data['_embedded']['attractions']
                artists = [attraction.get('name', '') for attraction in attractions if attraction.get('name')]
            elif 'attractions' in event_data:
                attractions = event_data['attractions']
                artists = [attraction.get('name', '') for attraction in attractions if attraction.get('name')]
            
            # Get event name
            event_name = event_data.get('name', 'Unknown Event')
            
            # Get event URL
            event_url = None
            if 'url' in event_data:
                event_url = event_data['url']
            
            # Get event description
            description = None
            if 'info' in event_data:
                description = event_data['info']
            
            # Get event image
            image_url = None
            if 'images' in event_data and event_data['images']:
                # Get the largest image
                images = sorted(event_data['images'], key=lambda x: x.get('width', 0), reverse=True)
                if images:
                    image_url = images[0].get('url')
            
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
    
    def search_events(self, keyword: str, city: str = None, state: str = None, 
                     country: str = 'US', classification: str = 'music', 
                     size: int = 50) -> List[Event]:
        """Search for events by keyword"""
        params = {
            'keyword': keyword,
            'countryCode': country,
            'classificationName': classification,
            'size': size,
            'sort': 'date,asc'
        }
        
        if city:
            params['city'] = city
        if state:
            params['stateCode'] = state
        
        data = self._make_request('events.json', params)
        events_data = data.get('_embedded', {}).get('events', [])
        
        # Convert to Event objects (reuse the same logic as get_events_by_location)
        return self._convert_events_data(events_data)
    
    def _convert_events_data(self, events_data: List[Dict[str, Any]]) -> List[Event]:
        """Convert raw events data to Event objects"""
        events = []
        for event_data in events_data:
            # Parse date
            event_date = None
            if 'dates' in event_data and 'start' in event_data['dates']:
                start_date = event_data['dates']['start']
                if 'dateTime' in start_date:
                    event_date = start_date['dateTime']
                elif 'localDate' in start_date:
                    event_date = start_date['localDate']
            
            # Extract venue info
            venue_name = 'Unknown Venue'
            venue_city = 'Unknown City'
            venue_country = 'US'
            
            if 'venues' in event_data.get('_embedded', {}):
                venues = event_data['_embedded']['venues']
                if venues:
                    venue = venues[0]
                    venue_name = venue.get('name', 'Unknown Venue')
                    venue_city = venue.get('city', {}).get('name', 'Unknown City')
                    venue_country = venue.get('country', {}).get('name', 'US')
            
            # Extract artists
            artists = []
            if 'attractions' in event_data.get('_embedded', {}):
                attractions = event_data['_embedded']['attractions']
                artists = [attraction.get('name', '') for attraction in attractions if attraction.get('name')]
            
            event = Event(
                title=event_data.get('name', 'Unknown Event'),
                venue=venue_name,
                city=venue_city,
                country=venue_country,
                date=event_date,
                url=event_data.get('url'),
                description=event_data.get('info'),
                artists=artists
            )
            events.append(event)
        
        return events
