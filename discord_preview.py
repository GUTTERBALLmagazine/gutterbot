#!/usr/bin/env python3
"""
discord bot preview - shows what would be posted to discord
"""

import os
from dotenv import load_dotenv
from src.lastfm.scraper import EventScraper
from src.utils.config import Config
from src.utils.date_utils import DateValidator
from datetime import datetime

# Load environment variables
load_dotenv()

def format_discord_embed(username: str, matches, event_num: int = 1):
    """Format a discord embed for event matches"""
    
    print(f"\n{'='*60}")
    print(f"🎵 DISCORD EMBED PREVIEW - {username.upper()}")
    print(f"{'='*60}")
    
    if not matches:
        print("No matches found for this user.")
        return
    
    print(f"**Title:** 🎵 Event Recommendations for {username}")
    print(f"**Description:** Found {len(matches)} events you might be interested in:")
    print(f"**Color:** #1db954 (Spotify Green)")
    print(f"**Timestamp:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"**Footer:** gutterbot • powered by last.fm & ticketmaster")
    print()
    
    for i, (event, matched_artist, similarity) in enumerate(matches[:5], 1):  # Limit to 5 events
        # Format date using proper validation
        event_date = DateValidator.format_discord_date(event.date)
        
        print(f"**Field {i}: {event.title}**")
        print(f"  **Venue:** {event.venue}")
        print(f"  **Date:** {event_date}")
        print(f"  **Matched Artist:** {matched_artist} ({similarity:.0%} match)")
        
        if event.artists:
            artists_str = ", ".join(event.artists[:3])  # Limit to 3 artists
            if len(event.artists) > 3:
                artists_str += f" +{len(event.artists) - 3} more"
            print(f"  **Artists:** {artists_str}")
        
        if event.url:
            print(f"  **Tickets:** [Get Tickets]({event.url})")
        
        print()

def main():
    """Main function to preview discord output"""
    try:
        # Validate configuration
        Config.validate()
        
        # Get usernames to track
        usernames = Config.get_users()
        if not usernames:
            print("❌ No usernames configured. Set LASTFM_USERS in .env file")
            return
        
        print("🚀 GUTTERBOT DISCORD PREVIEW")
        print("=" * 50)
        print(f"📊 Tracking users: {', '.join(usernames)}")
        print(f"🏙️  Location: {Config.ATLANTA_CITY}, {Config.ATLANTA_COUNTRY}")
        print(f"🎯 Similarity threshold: {Config.SIMILARITY_THRESHOLD}")
        print()
        
        # Initialize scraper
        scraper = EventScraper(
            Config.get_api_key(), 
            Config.get_ticketmaster_api_key(),
            Config.get_bandsintown_app_id()
        )
        
        # Scrape and match
        print("🎵 Fetching event recommendations...")
        matches = scraper.scrape_and_match(usernames)
        
        if not matches:
            print("❌ No matches found")
            return
        
        # Show what would be posted to discord
        print("\n" + "="*60)
        print("📱 WHAT WOULD BE POSTED TO DISCORD")
        print("="*60)
        
        for username, user_matches in matches.items():
            if user_matches:
                format_discord_embed(username, user_matches)
        
        print("\n" + "="*60)
        print("📊 SUMMARY")
        print("="*60)
        total_matches = sum(len(user_matches) for user_matches in matches.values())
        print(f"Total matches: {total_matches}")
        for username, user_matches in matches.items():
            print(f"  {username}: {len(user_matches)} matches")
        
        print(f"\n✅ This would create {len(matches)} embed(s) in discord")
        print("   (one embed per user with matches)")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
