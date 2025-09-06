#!/usr/bin/env python3
"""
gutterbot discord bot runner
"""

import os
from dotenv import load_dotenv
from src.discord.bot import run_bot
from src.utils.config import Config

# Load environment variables
load_dotenv()

def main():
    """Main entry point for discord bot"""
    try:
        # Validate configuration
        Config.validate()
        
        # Check discord-specific config
        if not Config.get_discord_bot_token():
            print("❌ DISCORD_BOT_TOKEN environment variable is required")
            return 1
        
        if not Config.get_discord_channel_id():
            print("❌ DISCORD_CHANNEL_ID environment variable is required")
            return 1
        
        print("🚀 Starting gutterbot discord bot...")
        print(f"📊 Tracking users: {', '.join(Config.get_users())}")
        print(f"🏙️  Location: {Config.ATLANTA_CITY}, {Config.ATLANTA_COUNTRY}")
        print(f"🎯 Similarity threshold: {Config.SIMILARITY_THRESHOLD}")
        print()
        
        # Run the bot
        run_bot()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
