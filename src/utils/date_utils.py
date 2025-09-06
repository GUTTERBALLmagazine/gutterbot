from datetime import datetime, timezone, timedelta
from typing import Optional


class DateValidator:
    """Utility class for validating and formatting event dates"""
    
    @staticmethod
    def parse_event_date(date_str: str) -> Optional[datetime]:
        """Parse various date formats into datetime object"""
        if not date_str:
            return None
        
        # List of common date formats to try
        formats = [
            "%Y-%m-%dT%H:%M:%S%z",  # ISO with timezone
            "%Y-%m-%dT%H:%M:%SZ",   # ISO with Z
            "%Y-%m-%dT%H:%M:%S",    # ISO without timezone
            "%Y-%m-%d %H:%M:%S",    # Standard format
            "%Y-%m-%d",             # Date only
            "%B %d, %Y at %I:%M %p", # Human readable
            "%a, %d %b %Y %H:%M:%S %z",  # Last.fm format
        ]
        
        for fmt in formats:
            try:
                if fmt.endswith('Z'):
                    # Handle Z timezone
                    date_str_clean = date_str.replace('Z', '+00:00')
                    return datetime.fromisoformat(date_str_clean)
                elif fmt.endswith('%z'):
                    # Handle timezone format
                    return datetime.strptime(date_str, fmt)
                else:
                    # Handle non-timezone formats
                    return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        # Try fromisoformat as last resort
        try:
            if date_str.endswith('Z'):
                date_str = date_str.replace('Z', '+00:00')
            return datetime.fromisoformat(date_str)
        except ValueError:
            pass
        
        return None
    
    @staticmethod
    def is_future_event(event_date: str, days_ahead: int = 90) -> bool:
        """Check if event is in the future within specified days"""
        if not event_date:
            return False
        
        parsed_date = DateValidator.parse_event_date(event_date)
        if not parsed_date:
            return False
        
        now = datetime.now(timezone.utc)
        cutoff = now.replace(hour=23, minute=59, second=59) + timedelta(days=days_ahead)
        
        # Ensure both datetimes are timezone-aware
        if parsed_date.tzinfo is None:
            parsed_date = parsed_date.replace(tzinfo=timezone.utc)
        
        return now <= parsed_date <= cutoff
    
    @staticmethod
    def format_discord_date(event_date: str) -> str:
        """Format date for discord display"""
        if not event_date:
            return "TBD"
        
        parsed_date = DateValidator.parse_event_date(event_date)
        if not parsed_date:
            return event_date
        
        # Ensure timezone-aware
        if parsed_date.tzinfo is None:
            parsed_date = parsed_date.replace(tzinfo=timezone.utc)
        
        # Convert to local time for display
        local_date = parsed_date.astimezone()
        return local_date.strftime("%B %d, %Y at %I:%M %p")
    
    @staticmethod
    def get_days_until_event(event_date: str) -> Optional[int]:
        """Get number of days until event"""
        if not event_date:
            return None
        
        parsed_date = DateValidator.parse_event_date(event_date)
        if not parsed_date:
            return None
        
        # Ensure timezone-aware
        if parsed_date.tzinfo is None:
            parsed_date = parsed_date.replace(tzinfo=timezone.utc)
        
        now = datetime.now(timezone.utc)
        delta = parsed_date - now
        return delta.days
