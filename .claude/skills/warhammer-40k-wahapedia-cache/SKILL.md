---
name: warhammer-40k-wahapedia-cache
description: Manage Wahapedia datasheet cache — check freshness, refresh faction data, discover units. Use when agents need to verify cache age, refresh stale data, or fetch new faction datasheets from Wahapedia.
---

# Wahapedia Cache Manager

## Purpose

Manage the local cache of Wahapedia faction datasheets. The scraper script generates JSON files that other skills read from. This skill wraps that script for common operations.

## Script Location

`_bmad/warhammer-40k/scripts/scrape-wahapedia.py`

**Requires:** Python 3 with `beautifulsoup4` installed.

## Available Commands

### Check Cache Freshness
```bash
python3 _bmad/warhammer-40k/scripts/scrape-wahapedia.py --check {faction}
```
Returns: cache age, whether stale (>30 days), last update date.

**Use before list building** to ensure data is current.

### Refresh One Faction
```bash
python3 _bmad/warhammer-40k/scripts/scrape-wahapedia.py --faction {faction}
```
Generates BOTH compact and full JSON datasheets for the faction.
Output: `_bmad/warhammer-40k/data/datasheets/{faction}.json` and `{faction}.compact.json`

### Refresh All User Factions
```bash
python3 _bmad/warhammer-40k/scripts/scrape-wahapedia.py --refresh-all
```
Refreshes all factions in the user's collection.

### View Compact Data
```bash
python3 _bmad/warhammer-40k/scripts/scrape-wahapedia.py --compact {faction}
```
Shows compact format summary for quick inspection.

### Look Up Single Unit
```bash
python3 _bmad/warhammer-40k/scripts/scrape-wahapedia.py --unit {faction} "Unit Name"
```
Shows full datasheet for one unit.

### Discover All Units in Faction
```bash
python3 _bmad/warhammer-40k/scripts/scrape-wahapedia.py --discover {faction}
```
Discovers ALL available units from the faction's Wahapedia index page.

### Add Single Unit to Cache
```bash
python3 _bmad/warhammer-40k/scripts/scrape-wahapedia.py --add-unit {faction} "Unit Name" "url-slug"
```

## Faction Slugs

Use these slugs for the `{faction}` parameter:
- `space-wolves`, `space-marines`, `orks`, `astra-militarum`
- `tau-empire`, `tyranids`, `adepta-sororitas`, `imperial-knights`
- `necrons`, `aeldari`, `drukhari`, `thousand-sons`, `world-eaters`
- `death-guard`, `chaos-daemons`, `chaos-knights`, `grey-knights`
- `adeptus-custodes`, `adeptus-mechanicus`, `imperial-agents`
- `leagues-of-votann`, `emperors-children`

## When to Use

| Situation | Command |
|-----------|---------|
| Before building any army list | `--check {faction}` (if stale, `--faction {faction}`) |
| Unit not found in cached data | `--add-unit {faction} "Name" "slug"` |
| New faction requested | `--discover {faction}` then `--faction {faction}` |
| Monthly maintenance | `--refresh-all` |
| Debugging data issues | `--unit {faction} "Name"` to inspect |

## Cache Location

Output files: `_bmad/warhammer-40k/data/datasheets/`
Metadata: `_bmad/warhammer-40k/data/datasheets/metadata.json`

## Stale Cache Policy

- Cache older than 30 days: warn user, offer to refresh
- Cache older than 90 days: strongly recommend refresh before any list building
- No cache: MUST refresh before building lists for that faction
