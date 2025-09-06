from datetime import datetime, timedelta
from typing import List
from .models import Event


def get_mock_atlanta_events() -> List[Event]:
    """Generate mock atlanta events for testing"""
    
    # Get current date for relative dates
    now = datetime.now()
    
    mock_events = [
        Event(
            title="Radiohead Tribute Night",
            venue="529",
            city="Atlanta",
            country="United States",
            date=(now + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S"),
            url="https://example.com/radiohead-tribute",
            description="A night of Radiohead covers by local bands",
            artists=["Radiohead", "Local Cover Band"]
        ),
        Event(
            title="Indie Rock Showcase",
            venue="Masquerade",
            city="Atlanta", 
            country="United States",
            date=(now + timedelta(days=14)).strftime("%Y-%m-%d %H:%M:%S"),
            url="https://example.com/indie-showcase",
            description="Featuring up-and-coming indie artists",
            artists=["Arctic Monkeys", "The Strokes", "Local Indie Band"]
        ),
        Event(
            title="Electronic Music Night",
            venue="Terminal West",
            city="Atlanta",
            country="United States", 
            date=(now + timedelta(days=21)).strftime("%Y-%m-%d %H:%M:%S"),
            url="https://example.com/electronic-night",
            description="Electronic and ambient music showcase",
            artists=["Aphex Twin", "Boards of Canada", "Local Electronic Artist"]
        ),
        Event(
            title="Jazz & Blues Evening",
            venue="Variety Playhouse",
            city="Atlanta",
            country="United States",
            date=(now + timedelta(days=28)).strftime("%Y-%m-%d %H:%M:%S"),
            url="https://example.com/jazz-blues",
            description="Traditional jazz and blues performances",
            artists=["Miles Davis Tribute", "Local Jazz Ensemble"]
        ),
        Event(
            title="Hip Hop Showcase",
            venue="Center Stage",
            city="Atlanta",
            country="United States",
            date=(now + timedelta(days=35)).strftime("%Y-%m-%d %H:%M:%S"),
            url="https://example.com/hip-hop-showcase",
            description="Atlanta hip hop artists and emerging talent",
            artists=["Outkast Tribute", "Local Hip Hop Artists"]
        ),
        Event(
            title="Alternative Rock Night",
            venue="The Earl",
            city="Atlanta",
            country="United States",
            date=(now + timedelta(days=42)).strftime("%Y-%m-%d %H:%M:%S"),
            url="https://example.com/alt-rock-night",
            description="Alternative and grunge music showcase",
            artists=["Nirvana Tribute", "Pearl Jam Covers", "Local Alt Band"]
        ),
        Event(
            title="Folk & Americana",
            venue="Eddie's Attic",
            city="Atlanta",
            country="United States",
            date=(now + timedelta(days=49)).strftime("%Y-%m-%d %H:%M:%S"),
            url="https://example.com/folk-americana",
            description="Traditional folk and americana music",
            artists=["Bob Dylan Tribute", "Local Folk Artists"]
        ),
        Event(
            title="Metal & Hardcore",
            venue="The Masquerade - Hell",
            city="Atlanta",
            country="United States",
            date=(now + timedelta(days=56)).strftime("%Y-%m-%d %H:%M:%S"),
            url="https://example.com/metal-hardcore",
            description="Heavy metal and hardcore punk showcase",
            artists=["Metallica Tribute", "Local Metal Bands"]
        )
    ]
    
    return mock_events
