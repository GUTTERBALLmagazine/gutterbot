# GitHub Actions Setup for Gutterbot

## Overview
This guide shows how to run gutterbot in the cloud using GitHub Actions. There are three approaches:

1. **Discord Bot with Scheduled Events** (recommended) - Creates actual Discord scheduled events
2. **Scheduled scraping with Discord webhooks** - Posts messages via webhook
3. **Simple scheduled scraping** - No Discord integration

## Setup Steps

### 1. Create Discord Webhook (for Discord integration)
1. Go to your Discord server settings
2. Navigate to Integrations → Webhooks
3. Create a new webhook for your channel
4. Copy the webhook URL

### 2. Configure GitHub Secrets
Go to your GitHub repo → Settings → Secrets and variables → Actions

Add these secrets:
- `LASTFM_API_KEY` - Your Last.fm API key
- `TICKETMASTER_API_KEY` - Your Ticketmaster API key  
- `BANDSINTOWN_APP_ID` - Your Bandsintown app ID
- `LASTFM_USERS` - Comma-separated list of Last.fm usernames (e.g., "user1,user2,user3")
- `DISCORD_BOT_TOKEN` - Your Discord bot token (for scheduled events)
- `DISCORD_CHANNEL_ID` - Your Discord channel ID (for scheduled events)
- `DISCORD_GUILD_ID` - Your Discord server ID (for scheduled events)
- `DISCORD_WEBHOOK_URL` - Your Discord webhook URL (for webhook integration)

### 3. Choose Your Workflow

#### Option A: Discord Bot with Scheduled Events (Recommended)
- Uses `.github/workflows/discord-bot.yml`
- Runs daily at 9 AM UTC
- Creates actual Discord scheduled events
- Posts embed messages to channel
- Prevents duplicates from previous runs

#### Option B: Discord Webhook Integration
- Uses `.github/workflows/daily-events.yml`
- Runs daily at 9 AM UTC
- Posts results to Discord via webhook
- No persistent bot needed

#### Option C: Simple Scraping
- Uses `.github/workflows/scrape-only.yml` 
- Runs daily at 9 AM UTC
- Just runs the scraper (like `python main.py`)
- Results logged in GitHub Actions

### 4. Customize Schedule
Edit the cron expression in the workflow file:
```yaml
- cron: '0 9 * * *'  # 9 AM UTC daily
```

Common schedules:
- `'0 9 * * *'` - Daily at 9 AM UTC
- `'0 9 * * 1'` - Weekly on Monday at 9 AM UTC
- `'0 9 1 * *'` - Monthly on the 1st at 9 AM UTC

### 5. Manual Trigger
You can manually trigger workflows:
1. Go to Actions tab in your GitHub repo
2. Select the workflow
3. Click "Run workflow"

## Limitations

- GitHub Actions has a 6-hour maximum runtime
- Free tier has limited minutes per month
- No persistent state between runs (except for Discord scheduled events)
- Discord bot approach creates scheduled events but requires bot token

## Alternative: Cloud Hosting

For a persistent bot that creates Discord scheduled events, consider:
- Railway (easy deployment)
- Heroku (free tier available)
- DigitalOcean App Platform
- AWS/GCP with proper Discord bot token

## Troubleshooting

- Check GitHub Actions logs for errors
- Verify all secrets are set correctly
- Test locally first with `python main.py`
- Discord webhook URL must be valid and active
