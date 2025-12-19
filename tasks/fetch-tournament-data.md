# Fetch Tournament Data Task

## Purpose
Aggregates competitive meta data from multiple tournament tracking sources to provide army list meta analysis, unit popularity rankings, win rates, and competitive trends. Implements intelligent caching with configurable refresh intervals.

## Usage

**From Agents:**
```yaml
- action: Execute task fetch-tournament-data with faction="Space Marines"
```

**From Workflows:**
```yaml
Execute: fetch-tournament-data
Parameters:
  faction: "Necrons"
  time_period: "30" # days
  min_events: 3
```

## Inputs

- `faction` (optional): Filter by specific faction
- `unit` (optional): Get popularity data for specific unit
- `time_period` (optional): Days of data to fetch (default: 30)
- `min_events` (optional): Minimum events for inclusion (default: 3)
- `use_cache` (optional): Use cached data if available (default: true)
- `detail_level` (optional): "minimal", "standard", "detailed" (uses config setting if not specified)

## Outputs

Returns aggregated tournament meta data:
- `success`: Boolean indicating if fetch succeeded
- `faction_stats`: Faction-level statistics
  - `win_rate`: Overall win percentage
  - `appearance_rate`: How often faction appears in events
  - `avg_placement`: Average tournament placement
  - `top_8_rate`: Percentage of top 8 finishes
- `unit_popularity`: Array of units with popularity data
  - `unit_name`: Unit name
  - `inclusion_rate`: % of lists including this unit
  - `avg_count`: Average number taken when included
  - `win_correlation`: Correlation with winning lists
- `trending`: Units gaining/losing popularity
- `meta_summary`: Human-readable meta analysis
- `sources`: List of data sources used
- `cached`: Boolean indicating if data came from cache
- `cache_age`: How old the cached data is

## Data Sources

1. **40k Event Tracker** (https://40k-event-tracker.nuxt.dev/)
   - Primary source for event results
   - Provides army lists and placements

2. **Stat Check** (https://www.stat-check.com/the-meta)
   - Global meta dashboard
   - Win rates and faction distribution

3. **Spikey Bits** (https://spikeybits.com/army-lists/)
   - Weekly top tournament lists
   - Faction tier lists

4. **Blood of Kittens** (https://bloodofkittens.com/)
   - ITC tournament results
   - Army list archives

5. **Warp Friends** (https://warpfriends.wordpress.com/)
   - Manual tournament aggregation
   - 20+ player, 5+ round events

## Implementation

<task>
**Step 1: Check Cache**
- Look for cached data in `{w40k_output_folder}/cache/tournaments/`
- Cache format: JSON files per faction
- Cache validity: Configurable via `tournament_cache_days` (default: 7 days)
- Return cached data if fresh enough

**Step 2: Fetch from Sources** (if cache miss)
- **40k Event Tracker**: WebFetch recent events, parse results
- **Stat Check**: WebFetch meta dashboard, extract win rates
- **Spikey Bits**: WebFetch army lists page, parse top lists
- **Blood of Kittens**: WebFetch ITC results
- **Warp Friends**: WebFetch tournament data posts

**Step 3: Parse and Normalize**
Each source has different formats - normalize to common structure:
```json
{
  "event_name": "string",
  "date": "ISO date",
  "faction": "string",
  "placement": number,
  "list": ["unit array"],
  "player": "string",
  "source": "source name"
}
```

**Step 4: Aggregate Statistics**
- Calculate faction win rates
- Compute unit inclusion rates
- Identify trending units (compare to last period)
- Determine win correlations
- Generate meta summary

**Step 5: Apply Detail Level**
Based on `meta_detail_level` config or parameter:
- **Minimal**: Win rates only
- **Standard**: Win rates + unit popularity
- **Detailed**: Full breakdown with trending, correlations, top lists

**Step 6: Cache Result**
- Save aggregated data to cache folder
- Include metadata: timestamp, sources, data period
- Create cache directory if it doesn't exist
- Respect `tournament_cache_days` setting

**Step 7: Return Structured Data**
- Format according to detail level
- Include source attribution
- Provide cache information
</task>

## Error Handling

- **Source unreachable**: Skip that source, continue with others
- **Parse failure**: Log warning, use other sources
- **No data for faction**: Return empty stats with message
- **Rate limiting**: Implement delays between source fetches
- **Stale cache + fetch failure**: Return stale cache with warning

## Cache Strategy

- **Location**: `{w40k_output_folder}/cache/tournaments/`
- **Format**: JSON files per faction + global meta file
- **Naming**: `{faction_slug}-meta.json`, `global-meta.json`
- **TTL**: Configurable via `tournament_cache_days` (1/7/30 days)
- **Invalidation**: Automatic based on TTL, manual clear option

## Example Queries

**Get Faction Meta:**
```
faction: "Space Marines"
time_period: 30
detail_level: "standard"
```

**Check Unit Popularity:**
```
unit: "Ballistus Dreadnought"
time_period: 60
```

**Global Meta Overview:**
```
# No parameters - returns all factions
detail_level: "minimal"
```

## Output Examples

**Standard Detail:**
```json
{
  "success": true,
  "faction_stats": {
    "faction": "Necrons",
    "win_rate": 52.3,
    "appearance_rate": 8.5,
    "top_8_rate": 15.2
  },
  "unit_popularity": [
    {
      "unit_name": "Lokhust Heavy Destroyers",
      "inclusion_rate": 73.5,
      "avg_count": 1.8,
      "win_correlation": 0.62
    }
  ],
  "cached": true,
  "cache_age": "2 days"
}
```

## Notes

- Tournament sites update at different frequencies - cache accordingly
- Some sources require manual parsing of blog posts/PDFs
- Win correlation ≠ causation - provide context in responses
- Meta shifts occur with FAQ updates and new releases
- Always include disclaimer about competitive vs casual play

## Dependencies

- WebFetch tool (for retrieving tournament data)
- File system access (for caching)
- JSON parsing capabilities
- Date/time handling for cache freshness

## Future Enhancements

- Webhook notifications when meta shifts significantly
- Historical trend tracking (meta over time)
- Regional meta differences (US vs EU vs Asia)
- Automated FAQ impact detection
- Integration with GoonHammer tournament coverage
