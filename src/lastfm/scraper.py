from difflib import SequenceMatcher
from typing import List, Dict, Tuple
from .client import LastFMClient
from .ticketmaster_client import TicketmasterClient
from .bandsintown_client import BandsintownClient
from .models import Artist, Event, UserListeningData
from .mock_events import get_mock_atlanta_events
from ..utils.config import Config
from ..utils.date_utils import DateValidator


class EventScraper:
    """Scrapes and matches events with user listening data"""
    
    def __init__(self, lastfm_api_key: str, ticketmaster_api_key: str, bandsintown_app_id: str = None):
        self.lastfm_client = LastFMClient(lastfm_api_key)
        self.ticketmaster_client = TicketmasterClient(ticketmaster_api_key)
        self.bandsintown_client = BandsintownClient(bandsintown_app_id) if bandsintown_app_id else None
        self.similarity_threshold = Config.SIMILARITY_THRESHOLD
    
    def get_user_artists(self, usernames: List[str], period: str = '1month') -> Dict[str, UserListeningData]:
        """Get listening data for multiple users"""
        user_data = {}
        
        for username in usernames:
            try:
                # Get more artists for better coverage
                user_data[username] = self.lastfm_client.get_user_top_artists(username, period, limit=100)
                print(f"✓ Loaded {len(user_data[username].artists)} artists for {username}")
            except Exception as e:
                print(f"✗ Failed to load data for {username}: {e}")
        
        return user_data
    
    def get_atlanta_events(self, limit: int = 100) -> List[Event]:
        """Get events in Atlanta using Ticketmaster API (fallback method)"""
        try:
            events = self.ticketmaster_client.get_events_by_location(
                city='Atlanta',
                state='GA',
                country='US',
                classification='music',
                size=limit
            )
            print(f"✓ Found {len(events)} real events in Atlanta")
            return events
        except Exception as e:
            print(f"✗ Failed to load Atlanta events from Ticketmaster: {e}")
            print("🔄 Falling back to mock events...")
            try:
                events = get_mock_atlanta_events()
                print(f"✓ Found {len(events)} mock events in Atlanta")
                return events
            except Exception as mock_e:
                print(f"✗ Failed to load mock events: {mock_e}")
                return []
    
    def get_events_for_artists_batch(self, artists: List[str]) -> List[Event]:
        """Get events for a batch of artists with caching"""
        all_events = []
        
        for artist in artists:
            try:
                events = self.ticketmaster_client.search_events(
                    keyword=artist,
                    city='Atlanta',
                    state='GA',
                    country='US',
                    classification='music',
                    size=10
                )
                
                if events:
                    all_events.extend(events)
                    print(f"  ✓ {artist}: {len(events)} events")
                else:
                    print(f"  - {artist}: no events")
                    
            except Exception as e:
                print(f"  ✗ {artist}: error - {e}")
        
        return all_events

    def get_events_for_artists(self, artists: List[str], max_artists: int = 20) -> List[Event]:
        """Get events for specific artists (more efficient than location-based search)"""
        all_events = []
        searched_artists = 0
        
        print(f"🔍 Searching for events for {min(len(artists), max_artists)} artists...")
        
        for artist in artists[:max_artists]:
            try:
                events = self.ticketmaster_client.search_events(
                    keyword=artist,
                    city='Atlanta',
                    state='GA',
                    country='US',
                    classification='music',
                    size=10  # smaller size per artist
                )
                
                if events:
                    all_events.extend(events)
                    print(f"  ✓ {artist}: {len(events)} events")
                else:
                    print(f"  - {artist}: no events")
                
                searched_artists += 1
                
                # small delay to be nice to the API
                import time
                time.sleep(Config.ARTIST_SEARCH_DELAY)
                
            except Exception as e:
                print(f"  ✗ {artist}: error - {e}")
                continue
        
        # Remove duplicates based on event title and date
        unique_events = {}
        for event in all_events:
            key = f"{event.title}_{event.date}"
            if key not in unique_events:
                unique_events[key] = event
        
        final_events = list(unique_events.values())
        print(f"✓ Found {len(final_events)} unique events from {searched_artists} artists")
        
        return final_events
    
    def get_bandsintown_events_batch(self, artists: List[str]) -> List[Event]:
        """Get events from Bandsintown for a batch of artists"""
        if not self.bandsintown_client:
            return []
        
        all_events = []
        
        for artist in artists:
            try:
                events = self.bandsintown_client.get_artist_events(
                    artist_name=artist,
                    location='Atlanta, GA'
                )
                
                if events:
                    all_events.extend(events)
                    print(f"  ✓ {artist}: {len(events)} events")
                else:
                    print(f"  - {artist}: no events")
                    
            except Exception as e:
                print(f"  ✗ {artist}: error - {e}")
        
        return all_events

    def get_bandsintown_events(self, artists: List[str], max_artists: int = 20) -> List[Event]:
        """Get events from Bandsintown for specific artists"""
        if not self.bandsintown_client:
            return []
        
        all_events = []
        searched_artists = 0
        
        print(f"🔍 Searching Bandsintown for events for {min(len(artists), max_artists)} artists...")
        
        for artist in artists[:max_artists]:
            try:
                events = self.bandsintown_client.get_artist_events(artist, "Atlanta, GA")
                
                if events:
                    all_events.extend(events)
                    print(f"  ✓ {artist}: {len(events)} events")
                else:
                    print(f"  - {artist}: no events")
                
                searched_artists += 1
                
                # small delay to be nice to the API
                import time
                time.sleep(Config.ARTIST_SEARCH_DELAY)
                
            except Exception as e:
                print(f"  ✗ {artist}: error - {e}")
                continue
        
        # Remove duplicates based on event title and date
        unique_events = {}
        for event in all_events:
            key = f"{event.title}_{event.date}"
            if key not in unique_events:
                unique_events[key] = event
        
        final_events = list(unique_events.values())
        print(f"✓ Found {len(final_events)} unique events from Bandsintown")
        
        return final_events
    
    
    def calculate_similarity(self, name1: str, name2: str) -> float:
        """Calculate similarity between two strings (0.0 to 1.0)"""
        return SequenceMatcher(None, name1.lower(), name2.lower()).ratio()
    
    def is_valid_match(self, event_artist: str, user_artist: str, similarity: float) -> bool:
        """Determine if a match is valid based on strict criteria"""
        
        # Must meet minimum similarity threshold
        if similarity < self.similarity_threshold:
            return False
        
        # Exact match is always valid
        if similarity >= 0.95:
            return True
        
        # For partial matches, apply additional strict checks
        event_lower = event_artist.lower().strip()
        user_lower = user_artist.lower().strip()
        
        # Check if one name is contained in the other (but not too short)
        if len(event_lower) >= 4 and len(user_lower) >= 4:
            if event_lower in user_lower or user_lower in event_lower:
                return True
        
        # Check for common artist name patterns
        # Remove common suffixes/prefixes that might cause false matches
        event_clean = self._clean_artist_name(event_lower)
        user_clean = self._clean_artist_name(user_lower)
        
        # If cleaned names are very similar, it's likely a valid match
        if len(event_clean) >= 3 and len(user_clean) >= 3:
            clean_similarity = SequenceMatcher(None, event_clean, user_clean).ratio()
            if clean_similarity >= 0.85:
                return True
        
        # Check for word-by-word matching (for multi-word names)
        event_words = set(event_clean.split())
        user_words = set(user_clean.split())
        
        if len(event_words) >= 2 and len(user_words) >= 2:
            # If most words match, it's likely the same artist
            common_words = event_words.intersection(user_words)
            if len(common_words) >= min(len(event_words), len(user_words)) * 0.7:
                return True
        
        # If we get here, it's probably not a valid match
        return False
    
    def _clean_artist_name(self, name: str) -> str:
        """Clean artist name for better matching"""
        # Remove common suffixes and prefixes
        suffixes_to_remove = [
            ' band', ' group', ' ensemble', ' orchestra', ' quartet', ' trio',
            ' feat.', ' featuring', ' ft.', ' ft ', ' &', ' and', ' +',
            ' (live)', ' (acoustic)', ' (remix)', ' (cover)', ' (tribute)',
            ' the', ' a ', ' an ', ' of ', ' in ', ' on ', ' at ', ' for ',
            ' with ', ' without ', ' from ', ' to ', ' by ', ' vs ', ' vs. ',
            ' vs ', ' versus', ' presents', ' presents:', ' presents ',
            ' music', ' songs', ' hits', ' greatest', ' best of',
            ' official', ' original', ' new', ' old', ' classic',
            ' live', ' acoustic', ' electric', ' unplugged',
            ' remix', ' remixes', ' cover', ' covers', ' tribute',
            ' tribute to', ' tribute band', ' tribute show'
        ]
        
        cleaned = name
        for suffix in suffixes_to_remove:
            cleaned = cleaned.replace(suffix, ' ')
        
        # Remove extra spaces and normalize
        cleaned = ' '.join(cleaned.split())
        
        return cleaned
    
    def find_matching_events(self, user_data: Dict[str, UserListeningData], events: List[Event]) -> Dict[str, List[Tuple[Event, str, float]]]:
        """
        Find events that match user's listening history
        
        Returns:
            Dict mapping username to list of (event, matched_artist, similarity_score) tuples
        """
        matches = {}
        
        for username, data in user_data.items():
            user_matches = []
            user_artists = data.get_artist_names()
            
            for event in events:
                for event_artist in event.artists:
                    best_similarity = 0.0
                    best_user_artist = ""
                    
                    # Find best match among user's artists
                    for user_artist in user_artists:
                        similarity = self.calculate_similarity(event_artist, user_artist)
                        if similarity > best_similarity and self.is_valid_match(event_artist, user_artist, similarity):
                            best_similarity = similarity
                            best_user_artist = user_artist
                    
                    # If we found a valid match, add it
                    if best_similarity >= self.similarity_threshold and best_user_artist:
                        user_matches.append((event, best_user_artist, best_similarity))
            
            # Remove duplicates and sort by similarity
            unique_matches = {}
            for event, artist, similarity in user_matches:
                key = f"{event.title}_{event.date}"
                if key not in unique_matches or similarity > unique_matches[key][2]:
                    unique_matches[key] = (event, artist, similarity)
            
            matches[username] = sorted(unique_matches.values(), key=lambda x: x[2], reverse=True)
        
        return matches
    
    def match_events_with_users(self, events: List[Event], user_data: Dict[str, UserListeningData]) -> Dict[str, List[Tuple[Event, str, float]]]:
        """Match a list of events with user listening data"""
        matches = {}
        
        for username, data in user_data.items():
            user_matches = []
            
            for event in events:
                # Check if event is in the future
                if not DateValidator.is_future_event(event.date):
                    continue
                
                # Find best matching artist
                best_match = None
                best_similarity = 0.0
                
                for artist in data.get_artist_names():
                    similarity = self.calculate_similarity(event.title, artist)
                    if similarity > self.similarity_threshold and similarity > best_similarity:
                        best_similarity = similarity
                        best_match = artist
                
                if best_match:
                    user_matches.append((event, best_match, best_similarity))
            
            # Sort by similarity score
            user_matches.sort(key=lambda x: x[2], reverse=True)
            matches[username] = user_matches
        
        return matches
    
    async def scrape_and_match(self, usernames: List[str], period: str = '1month', 
                        use_optimized_search: bool = True, batch_callback=None, exclude_artists: List[str] = None) -> Dict[str, List[Tuple[Event, str, float]]]:
        """Main method: scrape events and match with user data"""
        print(f"🎵 Scraping data for users: {', '.join(usernames)}")
        
        # Get user listening data
        user_data = self.get_user_artists(usernames, period)
        
        if not user_data:
            print("❌ No user data loaded")
            return {}
        
        # Get events from all sources
        if use_optimized_search:
            # Collect all unique artists from all users
            all_artists = set()
            for data in user_data.values():
                all_artists.update(data.get_artist_names())
            
            # Optionally exclude artists that already have scheduled events
            if exclude_artists:
                exclude_set = {a.lower() for a in exclude_artists}
                filtered = []
                for a in all_artists:
                    if a.lower() not in exclude_set:
                        filtered.append(a)
                all_artists = filtered
            all_artists = list(all_artists)
            print(f"🎯 Found {len(all_artists)} unique artists across all users")
            
            # Get events from all sources using batched approach
            all_events = []
            
            # Process artists in batches of 10 with 2-minute delays
            batch_size = 10
            total_batches = (len(all_artists) + batch_size - 1) // batch_size
            
            for batch_num in range(total_batches):
                start_idx = batch_num * batch_size
                end_idx = min(start_idx + batch_size, len(all_artists))
                batch_artists = all_artists[start_idx:end_idx]
                
                print(f"🔍 Processing batch {batch_num + 1}/{total_batches} ({len(batch_artists)} artists)...")
                
                # Get events for this batch
                batch_events = self.get_events_for_artists_batch(batch_artists)
                all_events.extend(batch_events)
                
                print(f"✓ Batch {batch_num + 1} complete: {len(batch_events)} events found")
                
                # Process batch results if callback provided
                if batch_callback and batch_events:
                    try:
                        print(f"🔄 Calling batch callback for {len(batch_events)} events...")
                        await batch_callback(batch_events, batch_num + 1, total_batches)
                        print(f"✅ Batch callback completed")
                    except Exception as e:
                        print(f"❌ Error processing batch {batch_num + 1}: {e}")
                
                # Add delay between batches (except for the last one)
                if batch_num < total_batches - 1:
                    print(f"⏳ Waiting 120 seconds before next batch...")
                    import asyncio
                    await asyncio.sleep(120)
            
            print(f"✓ Found {len(all_events)} total events from all batches")
            
            # Bandsintown events (process in same batches)
            bandsintown_events = []
            for batch_num in range(total_batches):
                start_idx = batch_num * batch_size
                end_idx = min(start_idx + batch_size, len(all_artists))
                batch_artists = all_artists[start_idx:end_idx]
                
                batch_bandsintown = self.get_bandsintown_events_batch(batch_artists)
                bandsintown_events.extend(batch_bandsintown)
                
                # Add delay between batches (except for the last one)
                if batch_num < total_batches - 1:
                    print(f"⏳ Waiting 120 seconds before next bandsintown batch...")
                    import asyncio
                    await asyncio.sleep(120)
            
            all_events.extend(bandsintown_events)
            print(f"✓ Bandsintown: {len(bandsintown_events)} events")
            
            
            # Combine and deduplicate events
            unique_events = {}
            for event in all_events:
                key = f"{event.title}_{event.date}_{event.venue}"
                if key not in unique_events:
                    unique_events[key] = event
            
            events = list(unique_events.values())
            
            # Filter for future events only
            future_events = []
            for event in events:
                if DateValidator.is_future_event(event.date, days_ahead=90):
                    future_events.append(event)
            
            events = future_events
            print(f"✓ Combined: {len(events)} unique future events from all sources")
        else:
            # Fallback to location-based search
            events = self.get_atlanta_events()
        
        if not events:
            print("❌ No events found")
            return {}
        
        # Find matches
        matches = self.find_matching_events(user_data, events)
        
        # Print summary
        total_matches = sum(len(user_matches) for user_matches in matches.values())
        print(f"🎯 Found {total_matches} total matches across all users")
        
        for username, user_matches in matches.items():
            print(f"  {username}: {len(user_matches)} matches")
        
        return matches
