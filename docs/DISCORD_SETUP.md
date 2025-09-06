# discord bot setup guide

## 1. create discord application

1. go to [discord developer portal](https://discord.com/developers/applications)
2. click "new application"
3. name it "gutterbot" (or whatever you want)
4. click "create"

## 2. create bot

1. in your application, go to "bot" tab
2. click "add bot"
3. customize username and avatar if you want
4. under "token", click "reset token"
5. copy the token (you'll need this for `DISCORD_BOT_TOKEN`)

## 3. get bot permissions

1. go to "oauth2" → "url generator"
2. under "scopes", select "bot"
3. under "bot permissions", select:
   - send messages
   - embed links
   - read message history
   - use slash commands
4. copy the generated url
5. open the url in your browser
6. select your server and authorize

## 4. get channel and guild ids

1. enable developer mode in discord:
   - user settings → advanced → developer mode
2. right-click on your channel → "copy id" (this is `DISCORD_CHANNEL_ID`)
3. right-click on your server name → "copy id" (this is `DISCORD_GUILD_ID`)

## 5. configure environment

add these to your `.env` file:

```bash
# discord bot configuration
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_CHANNEL_ID=your_channel_id_here
DISCORD_GUILD_ID=your_guild_id_here
```

## 6. run the bot

```bash
# activate conda environment
conda activate gutterbot

# run the discord bot
python run_discord_bot.py
```

## 7. test the bot

once the bot is running, try these commands in your discord channel:

- `!ping` - test if bot is responsive
- `!events` - manually fetch event recommendations
- `!help` - show help information

## 8. automation

the bot will automatically post event recommendations every 24 hours. you can modify the interval in `src/discord/bot.py`:

```python
@tasks.loop(hours=24)  # change this to your preferred interval
async def post_daily_events(self):
```

## troubleshooting

- **bot not responding**: check if bot token is correct
- **channel not found**: verify channel id is correct
- **permission errors**: make sure bot has required permissions
- **rate limits**: bot respects discord rate limits automatically

## features

- **automated posting**: posts event recommendations daily
- **manual commands**: `!events` to fetch fresh recommendations
- **rich embeds**: beautiful formatted messages with event details
- **artist matching**: shows which artists matched and similarity scores
- **ticket links**: direct links to buy tickets when available
