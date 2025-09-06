# gutterbot dev log

## 2024-09-06 - API Research & Analysis

### research objective
find viable APIs for fetching real atlanta music events to replace our current mock data system.

### findings summary

#### 🎯 **top tier options (recommended)**

**1. bandsintown api**
- **status**: ✅ active, public api
- **coverage**: comprehensive music events database
- **auth**: simple `app_id` parameter (no oauth required)
- **format**: json responses
- **atlanta coverage**: excellent
- **cost**: free tier available
- **pros**: 
  - designed for music events specifically
  - good atlanta coverage
  - simple authentication
  - well-documented
- **cons**: 
  - requires written consent for commercial use
  - enterprise-focused (but public endpoints work)
- **integration difficulty**: ⭐⭐☆☆☆ (easy)

**2. ticketmaster discovery api**
- **status**: ✅ active, public api
- **coverage**: 230,000+ events across multiple countries
- **auth**: api key required
- **format**: json responses
- **atlanta coverage**: excellent (major venue partner)
- **cost**: free tier with rate limits
- **pros**:
  - massive database
  - official ticket sales integration
  - comprehensive venue data
  - reliable data source
- **cons**:
  - may include non-music events
  - rate limits on free tier
- **integration difficulty**: ⭐⭐⭐☆☆ (moderate)

#### 🎵 **music-focused options**

**3. songkick api**
- **status**: ⚠️ partnership required
- **coverage**: 6+ million concerts
- **auth**: partnership agreement + licensing fee
- **format**: json/xml
- **atlanta coverage**: excellent
- **cost**: $$$ (partnership/licensing required)
- **pros**:
  - largest music events database
  - excellent data quality
  - comprehensive artist tracking
- **cons**:
  - not accessible for hobbyist projects
  - requires business partnership
- **integration difficulty**: ❌ (not accessible)

**4. jambase api**
- **status**: ✅ re-enabled august 2023
- **coverage**: jam bands, festivals, live music
- **auth**: api key required
- **format**: json responses
- **atlanta coverage**: good (jam band scene)
- **cost**: unknown (need to investigate)
- **pros**:
  - focused on live music
  - 25+ years historical data
  - festival coverage
- **cons**:
  - limited to jam bands primarily
  - may not cover mainstream events
- **integration difficulty**: ⭐⭐⭐☆☆ (moderate)

#### 🎫 **ticket aggregator options**

**5. seatgeek api**
- **status**: ✅ active
- **coverage**: aggregated ticket listings
- **auth**: api key required
- **format**: json responses
- **atlanta coverage**: good
- **cost**: free tier available
- **pros**:
  - real-time ticket availability
  - pricing data included
  - multiple source aggregation
- **cons**:
  - ticket-focused (not event discovery)
  - may have limited free tier
- **integration difficulty**: ⭐⭐⭐☆☆ (moderate)

**6. eventbrite api**
- **status**: ✅ active
- **coverage**: user-generated events
- **auth**: oauth 2.0 + api key
- **format**: json responses
- **atlanta coverage**: good (local events)
- **cost**: free tier available
- **pros**:
  - good for smaller/local events
  - detailed event information
  - user-friendly
- **cons**:
  - more general events (not music-specific)
  - oauth complexity
- **integration difficulty**: ⭐⭐⭐⭐☆ (complex)

#### 🔍 **specialized options**

**7. music gigs & concerts tracker api**
- **status**: ✅ active
- **coverage**: artist-specific + location-based
- **auth**: api key required
- **format**: json responses
- **atlanta coverage**: good
- **cost**: subscription-based plans
- **pros**:
  - user-friendly
  - flexible pricing
  - good documentation
- **cons**:
  - subscription required
  - smaller database
- **integration difficulty**: ⭐⭐⭐☆☆ (moderate)

**8. predicthq api**
- **status**: ✅ active
- **coverage**: global events with impact ranking
- **auth**: api key required
- **format**: json responses
- **atlanta coverage**: good
- **cost**: free tier + paid plans
- **pros**:
  - impact ranking system
  - global coverage
  - real-time updates
- **cons**:
  - not music-specific
  - may be overkill for our needs
- **integration difficulty**: ⭐⭐⭐☆☆ (moderate)

### 🎯 **recommendations**

#### **primary choice: bandsintown api**
- best fit for our use case
- music-focused
- simple integration
- good atlanta coverage
- free tier available

#### **secondary choice: ticketmaster discovery api**
- backup option with broader coverage
- official ticket sales integration
- reliable data source
- good for major venues

#### **implementation strategy**
1. start with bandsintown api
2. implement ticketmaster as fallback
3. add filtering for music events only
4. maintain mock data for testing

### 🔧 **next steps**
1. register for bandsintown api access
2. create bandsintown client module
3. implement atlanta event fetching
4. add fallback to ticketmaster
5. test with real data
6. update scraper to use real events

### 📊 **api comparison matrix**

| api | music focus | atlanta coverage | auth complexity | cost | integration ease |
|-----|-------------|------------------|-----------------|------|------------------|
| bandsintown | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | free | ⭐⭐ |
| ticketmaster | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | free | ⭐⭐⭐ |
| songkick | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ | $$$ | ❌ |
| jambase | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ? | ⭐⭐⭐ |
| seatgeek | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | free | ⭐⭐⭐ |
| eventbrite | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | free | ⭐⭐⭐⭐ |

### 🚀 **implementation timeline**
- **week 1**: bandsintown api integration
- **week 2**: ticketmaster fallback
- **week 3**: testing & optimization
- **week 4**: discord bot integration

## 2024-09-06 - Ticketmaster Integration Complete ✅

### what we implemented
- **ticketmaster discovery api client** - full integration with atlanta music events
- **fallback system** - mock events if ticketmaster fails
- **real data testing** - successfully fetching 100+ real atlanta events
- **fuzzy matching** - finding similar artists (blood orange → mild orange, samia → sampha)

### results
- **100 real events** fetched from ticketmaster
- **5 total matches** found across both users
- **fuzzy matching working** - 73-78% similarity scores for close matches
- **exact matches working** - deftones, michael minelli found perfectly

### next steps
- discord bot integration
- scheduling/automation
- more sophisticated filtering

## 2024-09-06 - Stricter Matching Implemented ✅

### problem
previous fuzzy matching was too loose, creating false positives:
- "mild orange" matched "blood orange" (78% similarity)
- "samia" matched "sampha" (73% similarity)  
- "ivri" matched "duster" (73% similarity)

### solution
implemented multi-layer validation:
- **increased threshold** from 0.7 to 0.85
- **exact match validation** (95%+ similarity)
- **contained name checking** (one name in other, but not too short)
- **cleaned name matching** (85%+ after removing common suffixes)
- **word-by-word validation** (70%+ word overlap for multi-word names)

### results
- **eliminated false positives** - no more incorrect matches
- **maintained true matches** - deftones, michael minelli still found
- **reduced noise** - 2 total matches instead of 5
- **higher confidence** - only high-quality matches returned

## 2024-09-06 - API Optimization Complete ✅

### problem
previous approach was inefficient:
- fetched 100 random atlanta events
- then matched against 50 artists per user
- many irrelevant events, low hit rate

### solution
implemented artist-specific search:
- **search ticketmaster for each user's top artists individually**
- **increased artist limit** from 50 to 100 per user
- **deduplication** - remove duplicate events
- **rate limiting** - small delays between requests
- **configurable limits** - max 30 artists searched by default

### results
- **6 total matches** (up from 2)
- **lobotonist**: 5 matches (che, 2hollis, bladee, earl sweatshirt, they are gutting a body of water)
- **maddy_eli**: 1 match (beach fossils)
- **more efficient** - 30 targeted searches vs 100 random events
- **better coverage** - 100 artists per user vs 50
- **higher hit rate** - 7 events from 29 successful searches

## 2024-09-06 - Discord Bot Integration Complete ✅

### what we built
- **full discord bot** with automated event posting
- **rich embeds** with event details, venue info, and ticket links
- **manual commands** (`!events`, `!ping`, `!help`)
- **daily automation** - posts recommendations every 24 hours
- **artist matching display** - shows which artists matched and similarity scores

### features
- **automated posting** - runs continuously, posts daily
- **manual triggers** - `!events` command for fresh recommendations
- **beautiful formatting** - discord embeds with event details
- **ticket integration** - direct links to buy tickets
- **error handling** - graceful fallbacks and error messages
- **configurable** - easy to adjust posting frequency and settings

### setup
- **discord application** - create bot in discord developer portal
- **permissions** - send messages, embed links, read history
- **environment variables** - bot token, channel id, guild id
- **easy deployment** - `python run_discord_bot.py`

### next steps
- deploy to production server
- set up monitoring and logging
- add more sophisticated filtering options

## 2024-09-06 - Bandsintown API Integration Complete ✅

### what we added
- **bandsintown api client** - additional event data source
- **dual api support** - ticketmaster + bandsintown for comprehensive coverage
- **smart deduplication** - removes duplicate events across apis
- **fallback system** - graceful handling when one api fails
- **compatibility layer** - supports both BANDSINTOWN_APP_ID and BANDSINTOWN_API_KEY

### api coverage
- **ticketmaster**: major venues, festivals, big artists (15 events found)
- **bandsintown**: indie artists, smaller venues, alternative coverage (0 events in test)
- **combined**: comprehensive atlanta music scene coverage

### results
- **15 unique events** found from ticketmaster
- **0 events** from bandsintown (no atlanta shows for test artists)
- **5 total matches** across both users
- **no duplicates** - smart deduplication working
- **error handling** - graceful fallbacks for api failures

### technical details
- **artist-specific searches** - 30 artists searched per api
- **rate limiting** - respects both api limits
- **location filtering** - atlanta, ga for bandsintown
- **deduplication key** - title + date + venue for uniqueness

---

*last updated: 2024-09-06*
*next review: after production deployment*
