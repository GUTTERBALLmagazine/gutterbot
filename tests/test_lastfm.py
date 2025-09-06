import unittest
from src.lastfm.client import LastFMClient
from src.lastfm.scraper import EventScraper
from src.lastfm.models import Artist, Event


class TestLastFMIntegration(unittest.TestCase):
    """Basic tests for last.fm integration"""
    
    def setUp(self):
        # You'll need to set LASTFM_API_KEY in your environment for these tests
        self.api_key = "test_key"  # Replace with actual key for real testing
    
    def test_artist_model(self):
        """Test Artist model creation"""
        artist = Artist(name="Test Artist", playcount=100)
        self.assertEqual(artist.name, "Test Artist")
        self.assertEqual(artist.playcount, 100)
    
    def test_event_model(self):
        """Test Event model creation"""
        event = Event(
            title="Test Concert",
            venue="Test Venue",
            city="Atlanta",
            country="United States",
            date="2024-01-01 20:00:00"
        )
        self.assertEqual(event.title, "Test Concert")
        self.assertEqual(event.city, "Atlanta")
    
    def test_similarity_calculation(self):
        """Test string similarity calculation"""
        scraper = EventScraper(self.api_key)
        
        # Test exact match
        similarity = scraper.calculate_similarity("Radiohead", "Radiohead")
        self.assertEqual(similarity, 1.0)
        
        # Test similar names
        similarity = scraper.calculate_similarity("Radiohead", "radiohead")
        self.assertEqual(similarity, 1.0)
        
        # Test different names
        similarity = scraper.calculate_similarity("Radiohead", "Coldplay")
        self.assertLess(similarity, 0.5)


if __name__ == '__main__':
    unittest.main()
