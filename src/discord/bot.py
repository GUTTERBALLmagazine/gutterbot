import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import os

from ..lastfm.scraper import EventScraper
from ..utils.config import Config
from ..utils.date_utils import DateValidator


class GutterBot(commands.Bot):
    """Discord bot for gutterball magazine event recommendations"""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None
        )
        
        # Initialize scraper
        self.scraper = EventScraper(
            Config.get_api_key(),
            Config.get_ticketmaster_api_key(),
            Config.get_bandsintown_app_id()
        )
        
        # Bot configuration
        self.channel_id = int(os.getenv('DISCORD_CHANNEL_ID', '0'))
        self.guild_id = int(os.getenv('DISCORD_GUILD_ID', '0'))
        self.created_events = set()  # Track created events to prevent duplicates
        self.existing_events = set()  # Track existing events from previous runs
        self.mode = os.getenv('GUTTERBOT_MODE', 'default')  # default | cleanup
        
    async def on_ready(self):
        """Called when bot is ready"""
        print(f'🎵 {self.user} is online!')
        print(f'📊 Monitoring channel: {self.channel_id}')
        print(f'🏠 Guild: {self.guild_id}')
        
        # Load existing events to prevent duplicates
        await self.load_existing_events()
        
        # Mode-based single-run behavior
        try:
            if self.mode == 'cleanup':
                print("🧹 Running cleanup mode...")
                deleted = await self.clean_scheduled_events()
                print(f"🧹 Cleanup complete. Removed {deleted} duplicate scheduled event(s).")
            else:
                await self.post_event_recommendations()
                print("✅ Event processing complete. Bot will exit.")
        except Exception as e:
            print(f"❌ Error during bot run: {e}")
        finally:
            await self.close()
    
    def _normalize_event_name(self, title: str) -> str:
        """Apply the same formatting/truncation we use when creating events."""
        event_name = f"🎵 {title}"
        if len(event_name) > 100:
            event_name = event_name[:97] + "..."
        return event_name
    
    def _build_existing_event_key(self, name: str, start_time: datetime, location: str) -> str:
        """Consistent key format for existing scheduled events (as stored by Discord)."""
        return f"{name}|{start_time.isoformat()}|{location or 'Unknown'}"
    
    
    async def post_event_recommendations(self):
        """Post event recommendations to discord channel"""
        channel = self.get_channel(self.channel_id)
        if not channel:
            print(f"❌ Channel {self.channel_id} not found")
            return
        
        print("🎵 Fetching event recommendations...")
        
        # Get usernames to track
        usernames = Config.get_users()
        if not usernames:
            await channel.send("❌ No usernames configured for tracking")
            return
        
        # Scrape and match events with batch callback
        matches = await self.scraper.scrape_and_match(usernames, batch_callback=self.process_batch_results)
        
        if not matches:
            await channel.send("🎵 No event matches found today")
            return
        
        # Create embed for each user's matches and discord events
        for username, user_matches in matches.items():
            if not user_matches:
                continue
                
            # Create discord scheduled events for each match
            created_events = []
            for event, matched_artist, similarity in user_matches:
                discord_event = await self.create_discord_event(event, matched_artist, similarity)
                if discord_event:
                    created_events.append(discord_event)
            
            # Create and send embed
            embed = self.create_event_embed(username, user_matches)
            if created_events:
                embed.add_field(
                    name="📅 Discord Events Created",
                    value=f"Created {len(created_events)} scheduled events! Check the Events tab in your server.",
                    inline=False
                )
            
            await channel.send(embed=embed)
    
    async def process_batch_results(self, batch_events, batch_num, total_batches):
        """Process and post results from a single batch"""
        print(f"🔍 Processing batch {batch_num} results: {len(batch_events)} events")
        
        if not batch_events:
            print(f"❌ No events in batch {batch_num}")
            return
        
        channel = self.get_channel(self.channel_id)
        if not channel:
            print(f"❌ Channel {self.channel_id} not found")
            return
        
        # Get usernames to track
        usernames = Config.get_users()
        if not usernames:
            print("❌ No usernames configured")
            return
        
        # Get user listening data for matching
        user_data = self.scraper.get_user_artists(usernames)
        if not user_data:
            print("❌ No user data available")
            return
        
        # Match events with user data
        matches = self.scraper.match_events_with_users(batch_events, user_data)
        print(f"🎯 Found matches: {matches}")
        
        if not matches:
            print(f"❌ No matches found in batch {batch_num}")
            return
        
        # Process each user's matches
        for username, user_matches in matches.items():
            if not user_matches:
                continue
            
            print(f"🎵 Processing {len(user_matches)} matches for {username}")
            
            # Create discord scheduled events for each match
            created_events = []
            for event, matched_artist, similarity in user_matches:
                print(f"🎫 Creating discord event for: {event.title} (matched: {matched_artist})")
                discord_event = await self.create_discord_event(event, matched_artist, similarity)
                if discord_event:
                    created_events.append(discord_event)
                    print(f"✅ Successfully created discord event: {discord_event.name}")
                else:
                    print(f"❌ Failed to create discord event for: {event.title}")
            
            # Create and send embed
            embed = self.create_event_embed(username, user_matches)
            embed.title = f"🎵 New Events Found (Batch {batch_num}/{total_batches})"
            if created_events:
                embed.add_field(
                    name="📅 Discord Events Created",
                    value=f"Created {len(created_events)} scheduled events! Check the Events tab in your server.",
                    inline=False
                )
            
            await channel.send(embed=embed)
            print(f"📤 Sent embed to discord channel")
    
    def create_event_embed(self, username: str, matches: List[Tuple]) -> discord.Embed:
        """Create a discord embed for event matches"""
        embed = discord.Embed(
            title=f"🎵 Event Recommendations for {username}",
            description=f"Found {len(matches)} events you might be interested in:",
            color=0x1db954,  # Spotify green
            timestamp=datetime.utcnow()
        )
        
        embed.set_footer(text="gutterbot • powered by last.fm & ticketmaster")
        
        for i, (event, matched_artist, similarity) in enumerate(matches[:5], 1):  # Limit to 5 events
            # Format date using proper validation
            event_date = DateValidator.format_discord_date(event.date)
            
            # Create field value
            field_value = f"**Venue:** {event.venue}\n"
            field_value += f"**Date:** {event_date}\n"
            field_value += f"**Matched Artist:** {matched_artist} ({similarity:.0%} match)\n"
            
            if event.artists:
                artists_str = ", ".join(event.artists[:3])  # Limit to 3 artists
                if len(event.artists) > 3:
                    artists_str += f" +{len(event.artists) - 3} more"
                field_value += f"**Artists:** {artists_str}\n"
            
            if event.url:
                field_value += f"**Tickets:** [Get Tickets]({event.url})"
            
            embed.add_field(
                name=f"{i}. {event.title}",
                value=field_value,
                inline=False
            )
        
        return embed
    
    async def load_existing_events(self):
        """Load existing scheduled events to prevent duplicates from previous runs"""
        try:
            guild = self.get_guild(self.guild_id)
            if not guild:
                print(f"❌ Could not find guild {self.guild_id}")
                return
            
            # Fetch all scheduled events
            scheduled_events = await guild.fetch_scheduled_events()
            print(f"📋 Found {len(scheduled_events)} existing scheduled events")
            
            # Add them to our tracking set
            for scheduled_event in scheduled_events:
                # Extract event info from the scheduled event
                # We'll use name, start_time, and location as the key
                location = scheduled_event.entity_metadata.location if scheduled_event.entity_metadata else 'Unknown'
                event_key = self._build_existing_event_key(scheduled_event.name, scheduled_event.start_time, location)
                self.existing_events.add(event_key)
                print(f"📝 Loaded existing event: {scheduled_event.name}")
                
        except Exception as e:
            print(f"❌ Error loading existing events: {e}")
    
    async def create_discord_event(self, event, matched_artist: str, similarity: float) -> Optional[discord.ScheduledEvent]:
        """Create a discord scheduled event for a music event"""
        try:
            # Check for duplicate events (same title + date + venue)
            event_key = f"{event.title}|{event.date}|{event.venue}"
            if event_key in self.created_events:
                print(f"⏭️  Skipping duplicate event (this run): {event.title}")
                return None
            
            # Check against existing events from previous runs
            # We need to format the key to match how we store existing events
            event_date = DateValidator.parse_event_date(event.date)
            if event_date and event_date.tzinfo is None:
                from datetime import timezone
                event_date = event_date.replace(tzinfo=timezone.utc)
            
            if event_date:
                normalized_name = self._normalize_event_name(event.title)
                existing_key = self._build_existing_event_key(normalized_name, event_date, event.venue)
                if existing_key in self.existing_events:
                    print(f"⏭️  Skipping duplicate event (previous run): {event.title}")
                    return None
            
            # Mark as created
            self.created_events.add(event_key)
            # Parse the event date
            event_date = DateValidator.parse_event_date(event.date)
            if not event_date:
                print(f"❌ Could not parse date for event: {event.title}")
                return None
            
            # Ensure timezone-aware
            if event_date.tzinfo is None:
                from datetime import timezone
                event_date = event_date.replace(tzinfo=timezone.utc)
            
            # Calculate end time (assume 3 hours duration for concerts)
            end_time = event_date + timedelta(hours=3)
            
            # Create event name (limit to 100 chars)
            event_name = self._normalize_event_name(event.title)
            
            # Create description (limit to 1000 chars)
            description = f"**Artist:** {matched_artist}\n"
            description += f"**Venue:** {event.venue}\n"
            if event.artists:
                artists_str = ", ".join(event.artists[:5])  # Limit to 5 artists
                if len(event.artists) > 5:
                    artists_str += f" +{len(event.artists) - 5} more"
                description += f"**Artists:** {artists_str}\n"
            if event.url:
                description += f"**Tickets:** {event.url}\n"
            description += f"\n*Found by gutterbot based on your last.fm listening history*"
            
            if len(description) > 1000:
                description = description[:997] + "..."
            
            # Get the guild from the channel
            guild = self.get_guild(self.guild_id)
            if not guild:
                print(f"❌ Could not find guild {self.guild_id}")
                return None
            
            # Create the scheduled event
            scheduled_event = await guild.create_scheduled_event(
                name=event_name,
                description=description,
                start_time=event_date,
                end_time=end_time,
                entity_type=discord.EntityType.external,
                location=event.venue,
                privacy_level=discord.PrivacyLevel.guild_only
            )
            
            print(f"✅ Created discord event: {event_name}")
            # Track the newly created event in existing_events to avoid duplicates later in the same run
            created_key = self._build_existing_event_key(event_name, event_date, event.venue)
            self.existing_events.add(created_key)
            return scheduled_event
            
        except Exception as e:
            print(f"❌ Failed to create discord event for {event.title}: {e}")
            return None
    
    @commands.command(name='events')
    async def manual_events(self, ctx):
        """Manual command to fetch and post events"""
        await ctx.send("🎵 Fetching fresh event recommendations...")
        await self.post_event_recommendations()
    
    @commands.command(name='ping')
    async def ping(self, ctx):
        """Test command to check if bot is responsive"""
        await ctx.send(f"🏓 Pong! Latency: {round(self.latency * 1000)}ms")
    
    @commands.command(name='create_events')
    async def create_events_command(self, ctx):
        """Create discord scheduled events for current recommendations"""
        await ctx.send("🎵 Creating discord scheduled events for current recommendations...")
        await self.post_event_recommendations()
    
    @commands.command(name='clean_events')
    async def clean_events_command(self, ctx):
        """Scan scheduled events and remove duplicates (keeps the earliest entry)."""
        deleted = await self.clean_scheduled_events()
        await ctx.send(f"🧹 removed {deleted} duplicate scheduled event(s)")

    async def clean_scheduled_events(self) -> int:
        """Remove duplicate scheduled events, keeping the oldest per unique key. Returns count deleted."""
        guild = self.get_guild(self.guild_id)
        if not guild:
            print(f"❌ Could not find guild {self.guild_id}")
            return 0
        try:
            scheduled_events = await guild.fetch_scheduled_events()
            print(f"🧹 scanning {len(scheduled_events)} scheduled events for duplicates...")
            groups = {}
            for ev in scheduled_events:
                location = ev.entity_metadata.location if ev.entity_metadata else 'Unknown'
                key = self._build_existing_event_key(ev.name, ev.start_time, location)
                groups.setdefault(key, []).append(ev)
            to_delete = []
            for key, evs in groups.items():
                if len(evs) <= 1:
                    continue
                evs_sorted = sorted(evs, key=lambda e: e.id)
                to_delete.extend(evs_sorted[1:])
            if not to_delete:
                print("✅ no duplicates found")
                return 0
            deleted = 0
            for ev in to_delete:
                try:
                    await ev.delete()
                    deleted += 1
                except Exception as e:
                    print(f"❌ failed to delete duplicate event {ev.name}: {e}")
            print(f"🧹 removed {deleted} duplicate scheduled event(s)")
            return deleted
        except Exception as e:
            print(f"❌ error during cleanup: {e}")
            return 0
    
    @commands.command(name='help')
    async def help_command(self, ctx):
        """Show help information"""
        embed = discord.Embed(
            title="gutterbot help",
            description="automated atlanta music event recommendations with discord scheduled events",
            color=0x1db954
        )
        
        embed.add_field(
            name="Commands",
            value="`!events` - fetch fresh event recommendations\n`!create_events` - create discord scheduled events\n`!clean_events` - remove duplicate scheduled events\n`!ping` - check bot responsiveness\n`!help` - show this help",
            inline=False
        )
        
        embed.add_field(
            name="About",
            value="gutterbot matches your last.fm listening history with upcoming atlanta music events and automatically creates discord scheduled events for easy tracking!",
            inline=False
        )
        
        await ctx.send(embed=embed)


def run_bot():
    """Run the discord bot"""
    bot = GutterBot()
    
    # Get discord token
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("❌ DISCORD_BOT_TOKEN environment variable is required")
        return
    
    try:
        bot.run(token)
    except Exception as e:
        print(f"❌ Error running bot: {e}")


if __name__ == "__main__":
    run_bot()
