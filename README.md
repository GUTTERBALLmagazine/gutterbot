# 🎵 Gutterbot

**Discord bot for Gutterball Magazine - Automated Atlanta Music Event Discovery**

A sophisticated Discord bot that automatically discovers and creates scheduled events for music concerts based on your Last.fm listening history. Built with intelligent matching, rate limiting, and duplicate prevention.

## ✨ Features

### 🎯 **Smart Event Discovery**
- Scrapes Last.fm for your top artists and listening history
- Searches Ticketmaster and Bandsintown for upcoming Atlanta events
- Intelligent fuzzy matching between artists and events
- Configurable similarity threshold (default: 85%)

### 📅 **Discord Scheduled Events**
- Creates actual Discord scheduled events (not just messages!)
- Beautiful event descriptions with venue, date, and ticket links
- Automatic deduplication to prevent duplicate events
- Checks existing events from previous runs

### ⚡ **Production Ready**
- Batched processing with intelligent rate limiting
- Handles API rate limits gracefully with delays
- Comprehensive error handling and logging
- GitHub Actions integration for automated daily runs
- Single-run execution (perfect for cron jobs)

### 🔧 **Developer Friendly**
- Modular, well-documented codebase
- Multiple deployment options (local, GitHub Actions, cloud)
- Comprehensive setup documentation
- Clean separation of concerns

## 🚀 Quick Start

### Option 1: Local Development
```bash
# Clone and setup
git clone https://github.com/GUTTERBALLmagazine/gutterbot.git
cd gutterbot

# Create conda environment
conda env create -f environment.yml
conda activate gutterbot

# Configure environment
cp env.example .env
# Edit .env with your API keys and Discord info

# Run the bot
python run_discord_bot.py
```

### Option 2: GitHub Actions (Recommended)
1. Fork this repository
2. Add your API keys as GitHub Secrets (see [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md))
3. The bot will run automatically on schedule!

## 📋 Configuration

### Required Environment Variables
```bash
# Last.fm API
LASTFM_API_KEY=your_lastfm_api_key
LASTFM_USERS=lobotonist,maddy_eli

# Event APIs
TICKETMASTER_API_KEY=your_ticketmaster_key
BANDSINTOWN_APP_ID=your_bandsintown_id

# Discord Bot
DISCORD_BOT_TOKEN=your_discord_bot_token
DISCORD_CHANNEL_ID=your_channel_id
DISCORD_GUILD_ID=your_server_id
```

### Optional Configuration
- Similarity threshold: `src/utils/config.py` (default: 0.85)
- Batch size and delays: `src/lastfm/scraper.py`
- Event processing limits: `src/utils/config.py`

## 🎮 Usage

### Discord Bot Commands
- `!help` - Show available commands
- `!ping` - Test bot connectivity
- `!create_events` - Manually trigger event creation

### Automated Operation
The bot automatically:
1. Connects to Discord
2. Loads existing scheduled events (prevents duplicates)
3. Scrapes Last.fm for your top artists
4. Searches for upcoming Atlanta events
5. Matches events to your listening history
6. Creates Discord scheduled events for matches
7. Posts embed messages to your channel
8. Exits cleanly

## 🏗️ Architecture

```
src/
├── discord/          # Discord bot implementation
│   └── bot.py       # Main bot class with event creation
├── lastfm/          # Music data integration
│   ├── scraper.py   # Main event scraping logic
│   ├── client.py    # Last.fm API client
│   ├── ticketmaster_client.py
│   └── bandsintown_client.py
└── utils/           # Configuration and utilities
    ├── config.py    # Environment configuration
    └── date_utils.py # Date parsing and validation
```

## 🚀 Deployment Options

### 1. GitHub Actions (Recommended)
- **File**: `.github/workflows/discord-bot.yml`
- **Schedule**: Daily at 9 AM UTC (customizable)
- **Benefits**: Free, automated, no server maintenance
- **Setup**: See [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md)

### 2. Local Development
- **File**: `run_discord_bot.py`
- **Benefits**: Full control, easy debugging
- **Use case**: Development and testing

### 3. Cloud Hosting
- **Platforms**: Railway, Heroku, DigitalOcean, AWS
- **Benefits**: Persistent bot, real-time commands
- **Use case**: Production with live commands

## 📚 Documentation

- [docs/DISCORD_SETUP.md](docs/DISCORD_SETUP.md) - Discord bot setup guide
- [docs/GITHUB_ACTIONS_SETUP.md](docs/GITHUB_ACTIONS_SETUP.md) - Automated deployment
- [docs/DEV_LOG.md](docs/DEV_LOG.md) - Development history and decisions

## 🛠️ Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Style
- Follows Python PEP 8
- Type hints throughout
- Comprehensive docstrings
- Modular design patterns

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🎯 What Makes This Special

- **Real Discord Events**: Creates actual scheduled events, not just messages
- **Intelligent Matching**: Fuzzy string matching with configurable thresholds
- **Rate Limit Aware**: Handles API limits gracefully with batching and delays
- **Duplicate Prevention**: Checks both current run and previous runs
- **Production Ready**: Comprehensive error handling and logging
- **Multiple APIs**: Integrates Last.fm, Ticketmaster, and Bandsintown
- **Automated**: Perfect for GitHub Actions with single-run execution

## 📄 License

This project is part of Gutterball Magazine's music discovery initiative.

---

**Built with ❤️ for the Atlanta music scene**