# gutterbot

discord bot for gutterball magazine - automated atlanta music event discovery

## features

- scrapes last.fm for atlanta music events
- matches events with user listening history
- modular design for easy feature expansion

## setup

### option 1: conda (recommended)
```bash
# create and activate conda environment
conda env create -f environment.yml
conda activate gutterbot

# or use the setup script
./setup.sh
```

### option 2: pip
```bash
pip install -r requirements.txt
```

### configuration
1. get a last.fm api key from https://www.last.fm/api/account/create

2. create `.env` file:
```bash
cp env.example .env
# edit .env with your api key and usernames
```

3. run the scraper:
```bash
python main.py
```

## usage

### command line scraper
```bash
python main.py
```

the scraper will:
- fetch your top artists from last.fm
- get upcoming atlanta events
- match events to artists you listen to
- display results with similarity scores

### discord bot
```bash
python run_discord_bot.py
```

the discord bot will:
- automatically post event recommendations daily
- respond to manual commands (`!events`, `!ping`, `!help`)
- create beautiful embeds with event details
- show artist matches and similarity scores

see [DISCORD_SETUP.md](DISCORD_SETUP.md) for detailed setup instructions.

## configuration

- `LASTFM_API_KEY`: your last.fm api key
- `LASTFM_USERS`: comma-separated usernames to track
- similarity threshold can be adjusted in `src/utils/config.py`

## structure

```
src/
├── lastfm/          # last.fm api integration
├── discord/         # future discord bot code
└── utils/           # configuration and utilities
```
