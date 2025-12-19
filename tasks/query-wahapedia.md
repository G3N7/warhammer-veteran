# Query Wahapedia Task

## Purpose
Centralized task for querying Wahapedia (https://wahapedia.ru/) for Warhammer 40k rules, unit data, faction information, and lore. Implements caching to minimize repeated requests and provides consistent data retrieval across all agents.

## Usage

**From Agents:**
```yaml
- action: Execute task query-wahapedia with query="Space Marines Intercessors stats"
```

**From Workflows:**
```yaml
Execute: query-wahapedia
Parameters:
  query: "Necrons army rules"
  category: "rules" # or "units", "factions", "lore"
```

## Inputs

- `query` (required): The search query (unit name, rule name, faction, etc.)
- `category` (optional): Filter by category - "units", "rules", "factions", "lore", "weapons"
- `faction` (optional): Limit search to specific faction
- `use_cache` (optional): Use cached data if available (default: true)

## Outputs

Returns structured data from Wahapedia:
- `success`: Boolean indicating if query succeeded
- `data`: Parsed data from Wahapedia (structure varies by category)
- `source_url`: Direct link to Wahapedia page
- `cached`: Boolean indicating if data came from cache
- `cache_age`: How old the cached data is (if cached)

## Implementation

<task>
**Step 1: Parse Query**
- Determine query type (unit, rule, faction, etc.)
- Extract faction if mentioned in query
- Normalize search terms

**Step 2: Check Cache**
- Look for cached data in `{w40k_output_folder}/cache/wahapedia/`
- Cache format: JSON files named by query hash
- Cache validity: 7 days (configurable)

**Step 3: Fetch from Wahapedia**
If cache miss or expired:
- Use WebFetch to retrieve from wahapedia.ru
- Parse HTML content to extract relevant data
- Handle different page structures (units vs rules vs factions)

**Step 4: Parse and Structure**
- Extract key information based on category:
  - **Units**: Name, points, stats, abilities, wargear options
  - **Rules**: Rule name, text, FAQ entries
  - **Factions**: Faction abilities, detachment rules, stratagems
  - **Lore**: Historical context, notable battles, characters
  - **Weapons**: Range, type, strength, AP, damage

**Step 5: Cache Result**
- Save parsed data to cache folder
- Include metadata: timestamp, source URL, query hash
- Create cache directory if it doesn't exist

**Step 6: Return Structured Data**
- Return consistent format regardless of category
- Include source attribution
- Provide cache information
</task>

## Error Handling

- **Wahapedia unreachable**: Return cached data if available, otherwise error
- **Parse failure**: Log warning, return raw HTML for manual inspection
- **No results found**: Return empty data with helpful message
- **Rate limiting**: Implement exponential backoff, use cache aggressively

## Cache Strategy

- **Location**: `{w40k_output_folder}/cache/wahapedia/`
- **Format**: JSON files with metadata
- **Naming**: `{category}-{query_hash}.json`
- **TTL**: 7 days default (rules change infrequently)
- **Invalidation**: Manual clear or cache older than TTL

## Example Queries

**Query Unit Stats:**
```
query: "Space Marines Tactical Squad"
category: "units"
faction: "Space Marines"
```

**Query Rule:**
```
query: "Oath of Moment"
category: "rules"
```

**Query Faction Abilities:**
```
query: "Necrons faction abilities"
category: "factions"
faction: "Necrons"
```

## Notes

- Wahapedia structure may change - implement robust parsing with fallbacks
- Respect Wahapedia's bandwidth - aggressive caching is essential
- Always include source attribution in responses to users
- Consider implementing a "refresh cache" parameter for getting latest data

## Dependencies

- WebFetch tool (for retrieving Wahapedia pages)
- File system access (for caching)
- JSON parsing capabilities

## Future Enhancements

- Batch queries for multiple units
- Diff detection (alert when rules change)
- Offline mode with full cached dataset
- Image extraction for unit photos
