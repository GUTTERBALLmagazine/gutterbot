#!/usr/bin/env python3
"""
gutterbot - proof of concept for last.fm event scraping
"""

import os
from dotenv import load_dotenv
from src.lastfm.scraper import EventScraper
from src.utils.config import Config

# Load environment variables
load_dotenv()

def main():
    """Main entry point for testing the scraper"""
    try:
        # Validate configuration
        Config.validate()
        
        # Get usernames to track
        usernames = Config.get_users()
        if not usernames:
            print("❌ No usernames configured. Set LASTFM_USERS in .env file")
            return
        
        print(f"🚀 Starting gutterbot scraper...")
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
        matches = scraper.scrape_and_match(usernames)
        
        # Display results
        print("\n" + "="*60)
        print("🎪 MATCHING EVENTS FOUND")
        print("="*60)
        
        for username, user_matches in matches.items():
            if not user_matches:
                print(f"\n{username}: No matches found")
                continue
                
            print(f"\n{username} ({len(user_matches)} matches):")
            print("-" * 40)
            
            for event, matched_artist, similarity in user_matches:
                print(f"🎵 {event.title}")
                print(f"   📍 {event.venue} - {event.date}")
                print(f"   🎤 Matched: {matched_artist} (similarity: {similarity:.2f})")
                if event.artists:
                    print(f"   🎶 Artists: {', '.join(event.artists)}")
                print()
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
