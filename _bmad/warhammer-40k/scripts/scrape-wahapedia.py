#!/usr/bin/env python3
"""
Wahapedia Datasheet Scraper
Extracts unit datasheets from Wahapedia into per-faction JSON cache files.
Generates TWO formats:
  1. COMPACT (.compact.json) - List-building validation only (~50-100 lines per faction)
  2. FULL (.json) - Complete datasheets for tactical deep-dives (~2000+ lines)

Usage:
    python scrape-wahapedia.py --faction space-wolves    # Refresh one faction (both formats)
    python scrape-wahapedia.py --refresh-all             # Refresh all user factions
    python scrape-wahapedia.py --check space-wolves      # Check if cache is stale
    python scrape-wahapedia.py --validate space-wolves   # Validate cache against live data
    python scrape-wahapedia.py --unit space-wolves "Arjac Rockfist"  # Show one unit (full)
    python scrape-wahapedia.py --compact space-wolves    # Show compact format for faction
    python scrape-wahapedia.py --discover space-wolves   # Discover ALL units from faction index
    python scrape-wahapedia.py --add-unit space-wolves "Unit Name" "url-slug"  # Add single unit to cache
"""

import sys
import os
import re
import json
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional, Tuple

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, '..', 'data', 'datasheets')
METADATA_FILE = os.path.join(DATA_DIR, 'metadata.json')

# User's factions (from memories.md) - priority refresh
USER_FACTIONS = [
    'space-wolves',
    'space-marines',  # Ultramarines use base SM
    'orks',
    'astra-militarum',
    'tyranids',
    'tau-empire',
    'thousand-sons',
]

# ALL available 40k factions
ALL_FACTIONS = [
    # Imperium
    'adepta-sororitas',
    'adeptus-custodes',
    'adeptus-mechanicus',
    'astra-militarum',
    'grey-knights',
    'imperial-agents',
    'imperial-knights',
    'space-marines',
    'space-wolves',  # SM subfaction
    # Chaos
    'chaos-daemons',
    'chaos-knights',
    'chaos-space-marines',
    'death-guard',
    'emperors-children',
    'thousand-sons',
    'world-eaters',
    # Xenos
    'aeldari',
    'drukhari',
    'genestealer-cults',
    'leagues-of-votann',
    'necrons',
    'orks',
    'tau-empire',
    'tyranids',
]

# Wahapedia faction URL mappings
FACTION_URLS = {
    'space-wolves': {
        'base_url': 'https://wahapedia.ru/wh40k10ed/factions/space-marines/',
        'index_url': 'https://wahapedia.ru/wh40k10ed/factions/space-marines/space-wolves',
        'units': [
            ('Arjac-Rockfist', 'Arjac Rockfist'),
            ('Logan-Grimnar', 'Logan Grimnar'),
            ('Bjorn-The-Fell-handed', 'Bjorn the Fell-Handed'),
            ('Ragnar-Blackmane', 'Ragnar Blackmane'),
            ('Njal-Stormcaller', 'Njal Stormcaller'),
            ('Ulrik-The-Slayer', 'Ulrik the Slayer'),
            ('Wolf-Guard-Terminators', 'Wolf Guard Terminators'),
            ('Blood-Claws', 'Blood Claws'),
            ('Grey-Hunters', 'Grey Hunters'),
            ('Fenrisian-Wolves', 'Fenrisian Wolves'),
            ('Thunderwolf-Cavalry', 'Thunderwolf Cavalry'),
            ('Wulfen', 'Wulfen'),
            ('Wolf-Guard-Battle-Leader', 'Wolf Guard Battle Leader'),
            ('Wolf-Priest', 'Wolf Priest'),
            ('Iron-Priest', 'Iron Priest'),
            ('Venerable-Dreadnought-1', 'Venerable Dreadnought'),
            ('Murderfang', 'Murderfang'),
            ('Wulfen-Dreadnought-1', 'Wulfen Dreadnought'),
            ('Wolf-Scouts', 'Wolf Scouts'),
            ('Wolf-Guard-Headtakers', 'Wolf Guard Headtakers'),
        ]
    },
    'space-marines': {
        'base_url': 'https://wahapedia.ru/wh40k10ed/factions/space-marines/',
        'index_url': 'https://wahapedia.ru/wh40k10ed/factions/space-marines/',
        'units': [
            ('Roboute-Guilliman', 'Roboute Guilliman'),
            ('Marneus-Calgar', 'Marneus Calgar'),
            ('Captain-in-Gravis-Armour', 'Captain in Gravis Armour'),
            ('Lieutenant', 'Lieutenant'),
            ('Ballistus-Dreadnought', 'Ballistus Dreadnought'),
            ('Redemptor-Dreadnought', 'Redemptor Dreadnought'),
            ('Brutalis-Dreadnought', 'Brutalis Dreadnought'),
            ('Intercessor-Squad', 'Intercessor Squad'),
            ('Assault-Intercessor-Squad', 'Assault Intercessor Squad'),
            ('Infernus-Squad', 'Infernus Squad'),
            ('Vindicator', 'Vindicator'),
            ('Gladiator-Lancer', 'Gladiator Lancer'),
            ('Terminator-Squad', 'Terminator Squad'),
            ('Stormraven-Gunship', 'Stormraven Gunship'),
            ('Scout-Squad', 'Scout Squad'),
        ]
    },
    'tau-empire': {
        'base_url': 'https://wahapedia.ru/wh40k10ed/factions/t-au-empire/',
        'index_url': 'https://wahapedia.ru/wh40k10ed/factions/t-au-empire/',
        'units': [
            ('Commander-Shadowsun', 'Commander Shadowsun'),
            ('Commander-Farsight', 'Commander Farsight'),
            ('Longstrike', 'Longstrike'),
            ('Cadre-Fireblade', 'Cadre Fireblade'),
            ('Commander-In-Coldstar-Battlesuit', 'Commander in Coldstar Battlesuit'),
            ('Commander-In-Enforcer-Battlesuit', 'Commander in Enforcer Battlesuit'),
            ('Crisis-Battlesuits', 'Crisis Battlesuits'),
            ('Riptide-Battlesuit', 'Riptide Battlesuit'),
            ('Broadside-Battlesuits', 'Broadside Battlesuits'),
            ('Ghostkeel-Battlesuit', 'Ghostkeel Battlesuit'),
            ('Stealth-Battlesuits', 'Stealth Battlesuits'),
            ('Strike-Team', 'Strike Team'),
            ('Breacher-Team', 'Breacher Team'),
            ('Pathfinder-Team', 'Pathfinder Team'),
            ('Hammerhead-Gunship', 'Hammerhead Gunship'),
            ('Sky-Ray-Gunship', 'Sky Ray Gunship'),
            ('Devilfish', 'Devilfish'),
            ('Piranhas', 'Piranhas'),
            ('Kroot-Carnivores', 'Kroot Carnivores'),
            ('Kroot-Farstalkers', 'Kroot Farstalkers'),
        ]
    },
    'astra-militarum': {
        'base_url': 'https://wahapedia.ru/wh40k10ed/factions/astra-militarum/',
        'index_url': 'https://wahapedia.ru/wh40k10ed/factions/astra-militarum/',
        'units': [
            ('Lord-Solar-Leontus', 'Lord Solar Leontus'),
            ('Cadian-Castellan', 'Cadian Castellan'),
            ('Cadian-Command-Squad', 'Cadian Command Squad'),
            ('Leman-Russ-Commander', 'Leman Russ Commander'),  # Was Tank-Commander
            ('Commissar', 'Commissar'),
            ('Catachan-Command-Squad', 'Catachan Command Squad'),  # Was Platoon-Command-Squad
            ('Catachan-Jungle-Fighters', 'Catachan Jungle Fighters'),
            ('Cadian-Shock-Troops', 'Cadian Shock Troops'),
            ('Kasrkin', 'Kasrkin'),
            ('Tempestus-Scions', 'Tempestus Scions'),
            ('Leman-Russ-Battle-Tank', 'Leman Russ Battle Tank'),
            ('Rogal-Dorn-Battle-Tank', 'Rogal Dorn Battle Tank'),
            ('Baneblade', 'Baneblade'),
            ('Basilisk', 'Basilisk'),
            ('Manticore', 'Manticore'),
            ('Chimera', 'Chimera'),
            ('Armoured-Sentinels', 'Armoured Sentinels'),
            ('Scout-Sentinels', 'Scout Sentinels'),
            ('Bullgryn-Squad', 'Bullgryn Squad'),  # Was Bullgryns
            ('Ogryn-Bodyguard', 'Ogryn Bodyguard'),
            # Missing units added
            ('Ratlings', 'Ratlings'),
            ('Gaunt-s-Ghosts', "Gaunt's Ghosts"),
        ]
    },
    'tyranids': {
        'base_url': 'https://wahapedia.ru/wh40k10ed/factions/tyranids/',
        'index_url': 'https://wahapedia.ru/wh40k10ed/factions/tyranids/',
        'units': [
            ('Hive-Tyrant', 'Hive Tyrant'),
            ('Winged-Hive-Tyrant', 'Winged Hive Tyrant'),
            ('The-Swarmlord', 'The Swarmlord'),
            ('Tervigon', 'Tervigon'),
            ('Tyrannofex', 'Tyrannofex'),
            ('Exocrine', 'Exocrine'),
            ('Carnifexes', 'Carnifexes'),
            ('Screamer-Killers', 'Screamer-Killers'),
            ('Haruspex', 'Haruspex'),
            ('Maleceptor', 'Maleceptor'),
            ('Zoanthropes', 'Zoanthropes'),
            ('Neurotyrant', 'Neurotyrant'),
            ('Termagants', 'Termagants'),
            ('Hormagaunts', 'Hormagaunts'),
            ('Barbgaunts', 'Barbgaunts'),
            ('Tyranid-Warriors-with-Melee-Bio-weapons', 'Tyranid Warriors'),
            ('Genestealers', 'Genestealers'),
            ('Biovores', 'Biovores'),
            ('Pyrovores', 'Pyrovores'),
            ('Hive-Guard', 'Hive Guard'),
        ]
    },
    'orks': {
        'base_url': 'https://wahapedia.ru/wh40k10ed/factions/orks/',
        'index_url': 'https://wahapedia.ru/wh40k10ed/factions/orks/',
        'units': [
            ('Ghazghkull-Thraka', 'Ghazghkull Thraka'),
            ('Warboss', 'Warboss'),
            ('Warboss-In-Mega-Armour', 'Warboss in Mega Armour'),
            ('Big-Mek-With-Shokk-Attack-Gun', 'Big Mek with Shokk Attack Gun'),
            ('Big-Mek-In-Mega-Armour', 'Big Mek in Mega Armour'),
            ('Painboy', 'Painboy'),
            ('Weirdboy', 'Weirdboy'),
            ('Boyz', 'Boyz'),
            ('Gretchin', 'Gretchin'),
            ('Nobz', 'Nobz'),
            ('Meganobz', 'Meganobz'),
            ('Lootas', 'Lootas'),
            ('Burna-Boyz', 'Burna Boyz'),
            ('Tankbustas', 'Tankbustas'),
            ('Deff-Dread', 'Deff Dread'),
            ('Killa-Kans', 'Killa Kans'),
            ('Gorkanaut', 'Gorkanaut'),
            ('Morkanaut', 'Morkanaut'),
            ('Mek-Gunz', 'Mek Gunz'),
            ('Battlewagon', 'Battlewagon'),
        ]
    },
    'thousand-sons': {
        'base_url': 'https://wahapedia.ru/wh40k10ed/factions/thousand-sons/',
        'index_url': 'https://wahapedia.ru/wh40k10ed/factions/thousand-sons/',
        'units': [
            # Epic Heroes
            ('Magnus-The-Red', 'Magnus the Red'),
            ('Ahriman', 'Ahriman'),
            # Characters
            ('Exalted-Sorcerer', 'Exalted Sorcerer'),
            ('Infernal-Master', 'Infernal Master'),
            ('Thousand-Sons-Sorcerer', 'Thousand Sons Sorcerer'),
            ('Thousand-Sons-Daemon-Prince', 'Thousand Sons Daemon Prince'),
            # Battleline
            ('Rubric-Marines', 'Rubric Marines'),
            ('Tzaangors', 'Tzaangors'),
            # Elite
            ('Scarab-Occult-Terminators', 'Scarab Occult Terminators'),
            ('Tzaangor-Enlightened', 'Tzaangor Enlightened'),
            ('Tzaangor-Shaman', 'Tzaangor Shaman'),
            # Heavy Support / Monsters
            ('Mutalith-Vortex-Beast', 'Mutalith Vortex Beast'),
            ('Forgefiend', 'Forgefiend'),
            ('Maulerfiend', 'Maulerfiend'),
            ('Helbrute', 'Helbrute'),
            ('Defiler', 'Defiler'),
            # Vehicles
            ('Chaos-Rhino', 'Chaos Rhino'),
            ('Chaos-Land-Raider', 'Chaos Land Raider'),
            ('Chaos-Predator-Annihilator', 'Chaos Predator Annihilator'),
            ('Chaos-Predator-Destructor', 'Chaos Predator Destructor'),
            ('Chaos-Vindicator', 'Chaos Vindicator'),
            # Spawn
            ('Chaos-Spawn', 'Chaos Spawn'),
        ]
    },
}

# Base URLs for faction discovery (supports ALL factions via --discover)
FACTION_BASE_URLS = {
    # Imperium
    'adepta-sororitas': 'https://wahapedia.ru/wh40k10ed/factions/adepta-sororitas/',
    'adeptus-custodes': 'https://wahapedia.ru/wh40k10ed/factions/adeptus-custodes/',
    'adeptus-mechanicus': 'https://wahapedia.ru/wh40k10ed/factions/adeptus-mechanicus/',
    'astra-militarum': 'https://wahapedia.ru/wh40k10ed/factions/astra-militarum/',
    'grey-knights': 'https://wahapedia.ru/wh40k10ed/factions/grey-knights/',
    'imperial-agents': 'https://wahapedia.ru/wh40k10ed/factions/imperial-agents/',
    'imperial-knights': 'https://wahapedia.ru/wh40k10ed/factions/imperial-knights/',
    'space-marines': 'https://wahapedia.ru/wh40k10ed/factions/space-marines/',
    'space-wolves': 'https://wahapedia.ru/wh40k10ed/factions/space-marines/',  # SM subfaction
    # Chaos
    'chaos-daemons': 'https://wahapedia.ru/wh40k10ed/factions/chaos-daemons/',
    'chaos-knights': 'https://wahapedia.ru/wh40k10ed/factions/chaos-knights/',
    'chaos-space-marines': 'https://wahapedia.ru/wh40k10ed/factions/chaos-space-marines/',
    'death-guard': 'https://wahapedia.ru/wh40k10ed/factions/death-guard/',
    'emperors-children': 'https://wahapedia.ru/wh40k10ed/factions/emperor-s-children/',
    'thousand-sons': 'https://wahapedia.ru/wh40k10ed/factions/thousand-sons/',
    'world-eaters': 'https://wahapedia.ru/wh40k10ed/factions/world-eaters/',
    # Xenos
    'aeldari': 'https://wahapedia.ru/wh40k10ed/factions/aeldari/',
    'drukhari': 'https://wahapedia.ru/wh40k10ed/factions/drukhari/',
    'genestealer-cults': 'https://wahapedia.ru/wh40k10ed/factions/genestealer-cults/',
    'leagues-of-votann': 'https://wahapedia.ru/wh40k10ed/factions/leagues-of-votann/',
    'necrons': 'https://wahapedia.ru/wh40k10ed/factions/necrons/',
    'orks': 'https://wahapedia.ru/wh40k10ed/factions/orks/',
    'tau-empire': 'https://wahapedia.ru/wh40k10ed/factions/t-au-empire/',
    'tyranids': 'https://wahapedia.ru/wh40k10ed/factions/tyranids/',
}


def discover_faction_units(faction: str, verbose: bool = True) -> List[Tuple[str, str]]:
    """
    Auto-discover ALL units for a faction by scraping the faction index page.
    Returns list of (url_slug, display_name) tuples.
    """
    if faction not in FACTION_BASE_URLS:
        print(f"ERROR: Unknown faction '{faction}'")
        return []

    base_url = FACTION_BASE_URLS[faction]

    if verbose:
        print(f"Discovering units for {faction} from {base_url}...")

    try:
        html = fetch_page(base_url)
        soup = BeautifulSoup(html, 'html.parser')

        units = []
        seen_slugs = set()

        # Find all links that look like unit datasheets
        # Wahapedia format: /wh40k10ed/factions/faction-name/Unit-Name
        for link in soup.find_all('a', href=True):
            href = link['href']

            # Match unit datasheet links
            # Examples: /wh40k10ed/factions/astra-militarum/Cadian-Shock-Troops
            pattern = rf'/wh40k10ed/factions/[^/]+/([A-Z][a-zA-Z0-9\-\']+)$'
            match = re.search(pattern, href)

            if match:
                slug = match.group(1)

                # Skip non-unit pages
                skip_patterns = [
                    'Legends', 'Index', 'Detachment', 'Enhancement', 'Stratagem',
                    'Army-Rule', 'Faction-Rule', 'Crusade', 'Matched-Play',
                    'Combat-Patrol', 'Wargear', 'Datasheet'
                ]
                if any(skip in slug for skip in skip_patterns):
                    continue

                # Skip if we've already seen this slug
                if slug.lower() in seen_slugs:
                    continue
                seen_slugs.add(slug.lower())

                # Get display name from link text or convert from slug
                display_name = link.get_text(strip=True)
                if not display_name or len(display_name) < 3:
                    # Convert slug to display name: "Cadian-Shock-Troops" -> "Cadian Shock Troops"
                    display_name = slug.replace('-', ' ').replace('1', '').replace('2', '').strip()

                units.append((slug, display_name))

        if verbose:
            print(f"Found {len(units)} units for {faction}")

        return units

    except Exception as e:
        print(f"ERROR discovering units: {e}")
        return []


def add_unit_to_cache(faction: str, unit_name: str, url_slug: str = None, verbose: bool = True) -> bool:
    """
    Add a single unit to an existing faction cache.
    Use this when Tacticus finds a missing unit via web search.

    Args:
        faction: The faction name (e.g., 'astra-militarum')
        unit_name: Display name of the unit (e.g., 'Ursula Creed')
        url_slug: Optional URL slug (e.g., 'Ursula-Creed'). If not provided, will be derived from unit_name.

    Returns:
        True if unit was added successfully, False otherwise.
    """
    if faction not in FACTION_BASE_URLS:
        print(f"ERROR: Unknown faction '{faction}'")
        return False

    base_url = FACTION_BASE_URLS[faction]

    # Derive URL slug from unit name if not provided
    if not url_slug:
        url_slug = unit_name.replace(' ', '-').replace("'", '-')

    # Load existing cache
    cache_file = os.path.join(DATA_DIR, f'{faction}.json')
    compact_file = os.path.join(DATA_DIR, f'{faction}.compact.json')

    if not os.path.exists(cache_file):
        if verbose:
            print(f"No cache for {faction}. Run --faction {faction} first.")
        return False

    with open(cache_file, 'r') as f:
        faction_data = json.load(f)

    # Check if unit already exists
    if unit_name in faction_data.get('units', {}):
        if verbose:
            print(f"Unit '{unit_name}' already in cache")
        return True

    # Fetch the unit
    url = base_url + url_slug
    if verbose:
        print(f"Fetching {unit_name} from {url}...")

    try:
        html = fetch_page(url)
        data = extract_full_datasheet(html, unit_name, url_slug)

        # Add to faction data
        faction_data['units'][unit_name] = data
        faction_data['unit_count'] = len(faction_data['units'])
        faction_data['last_updated'] = datetime.now(timezone.utc).isoformat()

        # Save updated full cache
        with open(cache_file, 'w') as f:
            json.dump(faction_data, f, indent=2)

        # Regenerate and save compact cache
        compact_data = generate_compact_faction(faction_data)
        with open(compact_file, 'w') as f:
            json.dump(compact_data, f, indent=2)

        if verbose:
            pts_str = '/'.join([str(p['points']) for p in data.get('points', [])]) + 'pts' if data.get('points') else '?pts'
            print(f"Added {unit_name} ({pts_str}) to {faction} cache")

        return True

    except urllib.error.HTTPError as e:
        if e.code == 404:
            if verbose:
                print(f"Unit not found at {url}")
                print(f"Try checking Wahapedia for the correct URL slug")
        else:
            if verbose:
                print(f"HTTP error {e.code}: {e.reason}")
        return False

    except Exception as e:
        if verbose:
            print(f"ERROR adding unit: {e}")
        return False


def refresh_faction_autodiscover(faction: str, verbose: bool = True) -> Dict[str, Any]:
    """
    Refresh faction cache by auto-discovering ALL units from the faction index.
    This replaces the hardcoded unit lists.
    """
    units = discover_faction_units(faction, verbose)

    if not units:
        print(f"No units discovered for {faction}")
        return None

    base_url = FACTION_BASE_URLS.get(faction)
    if not base_url:
        print(f"ERROR: No base URL for faction '{faction}'")
        return None

    faction_data = {
        'faction': faction,
        'last_updated': datetime.now(timezone.utc).isoformat(),
        'source': 'wahapedia-autodiscover',
        'schema_version': '2.0',
        'unit_count': len(units),
        'units': {}
    }

    if verbose:
        print(f"Refreshing {faction} ({len(units)} auto-discovered units)...")

    success_count = 0
    error_count = 0

    for slug, name in units:
        url = base_url + slug
        if verbose:
            print(f"  {name}...", end=' ', flush=True)

        try:
            html = fetch_page(url)
            data = extract_full_datasheet(html, name, slug)
            faction_data['units'][name] = data

            if verbose:
                pts_str = '/'.join([str(p['points']) for p in data.get('points', [])]) + 'pts' if data.get('points') else '?pts'
                stats = data.get('stats', {})
                stat_str = f"M{stats.get('M', '?')} T{stats.get('T', '?')} W{stats.get('W', '?')}"
                print(f"OK ({pts_str}, {stat_str})")

            success_count += 1
            time.sleep(0.3)  # Be nice to server

        except Exception as e:
            if verbose:
                print(f"ERROR: {e}")
            faction_data['units'][name] = {
                'name': name,
                'url_slug': slug,
                'error': str(e)
            }
            error_count += 1

    # Save FULL faction cache
    cache_file = os.path.join(DATA_DIR, f'{faction}.json')
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(cache_file, 'w') as f:
        json.dump(faction_data, f, indent=2)

    # Generate and save COMPACT version
    compact_data = generate_compact_faction(faction_data)
    compact_file = os.path.join(DATA_DIR, f'{faction}.compact.json')
    with open(compact_file, 'w') as f:
        json.dump(compact_data, f, indent=2)

    if verbose:
        full_size = os.path.getsize(cache_file)
        compact_size = os.path.getsize(compact_file)
        reduction = (1 - compact_size / full_size) * 100
        print(f"\nCompleted: {success_count} success, {error_count} errors")
        print(f"Generated compact format: {compact_size:,} bytes ({reduction:.0f}% smaller)")

    # Update metadata
    metadata = load_metadata()
    if faction not in metadata.get('factions_cached', []):
        metadata.setdefault('factions_cached', []).append(faction)
    metadata['cache_invalid'] = False
    metadata['invalidation_reason'] = None
    metadata['last_global_refresh'] = datetime.now(timezone.utc).isoformat()
    metadata['schema_version'] = '2.0'
    save_metadata(metadata)

    if verbose:
        print(f"Saved to {cache_file}")

    return faction_data


def load_metadata() -> Dict:
    """Load cache metadata."""
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r') as f:
            return json.load(f)
    return {
        'schema_version': '2.0',  # Full datasheets
        'last_global_refresh': None,
        'cache_invalid': True,
        'stale_after_days': 30,
        'factions_cached': []
    }


def save_metadata(metadata: Dict):
    """Save cache metadata."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=2)


def is_cache_stale(metadata: Dict, faction: str = None) -> Tuple[bool, str]:
    """Check if cache is stale. Returns (is_stale, reason)."""
    if metadata.get('cache_invalid', False):
        return True, metadata.get('invalidation_reason', 'Cache marked invalid')

    if faction:
        cache_file = os.path.join(DATA_DIR, f'{faction}.json')
        if not os.path.exists(cache_file):
            return True, f'No cache file for {faction}'

        with open(cache_file, 'r') as f:
            faction_data = json.load(f)

        last_updated = faction_data.get('last_updated')
        if not last_updated:
            return True, 'No timestamp in cache'

        last_dt = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
        stale_days = metadata.get('stale_after_days', 30)

        if datetime.now(timezone.utc) - last_dt > timedelta(days=stale_days):
            return True, f'Cache older than {stale_days} days'

    return False, 'Cache is fresh'


def invalidate_cache(reason: str):
    """Mark entire cache as invalid."""
    metadata = load_metadata()
    metadata['cache_invalid'] = True
    metadata['invalidation_reason'] = reason
    save_metadata(metadata)
    print(f"Cache invalidated: {reason}")


def fetch_page(url: str) -> str:
    """Fetch HTML content from URL."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode('utf-8')


def search_unit_on_wahapedia(faction: str, unit_name: str, verbose: bool = True) -> Optional[str]:
    """
    Search for a unit's correct URL slug on Wahapedia by scraping the faction index page.
    Returns the correct URL slug if found, None otherwise.
    """
    base_url = FACTION_BASE_URLS.get(faction)
    if not base_url:
        return None

    try:
        html = fetch_page(base_url)
        soup = BeautifulSoup(html, 'html.parser')

        # Normalize the search term for comparison - strip everything to lowercase alphanumeric
        def normalize(s: str) -> str:
            return re.sub(r'[^a-z0-9]', '', s.lower())

        search_normalized = normalize(unit_name)

        best_match = None
        best_score = 0

        # Find all links that look like unit datasheets
        for link in soup.find_all('a', href=True):
            href = link['href']

            # Match unit datasheet links
            pattern = rf'/wh40k10ed/factions/[^/]+/([A-Za-z0-9\-\']+)$'
            match = re.search(pattern, href)

            if match:
                slug = match.group(1)
                link_text = link.get_text(strip=True)

                # Normalize link text and slug for comparison
                link_normalized = normalize(link_text)
                slug_normalized = normalize(slug)

                # Check for exact match (case-insensitive, ignoring punctuation)
                if search_normalized == link_normalized or search_normalized == slug_normalized:
                    if verbose:
                        print(f"    Found exact match: {slug}")
                    return slug

                # Check if search term starts with slug (e.g., "tyranidwarriors" in "tyranidwarriorswithmeleebiowpns")
                if slug_normalized.startswith(search_normalized) or link_normalized.startswith(search_normalized):
                    score = len(search_normalized) / max(len(link_normalized), len(slug_normalized))
                    # Boost score if it's a prefix match
                    score = min(score + 0.3, 1.0)
                    if score > best_score:
                        best_score = score
                        best_match = slug

                # Check for partial match (unit name contained in link text)
                # Score based on how much of the search term matches
                if search_normalized in link_normalized or search_normalized in slug_normalized:
                    score = len(search_normalized) / max(len(link_normalized), len(slug_normalized))
                    if score > best_score:
                        best_score = score
                        best_match = slug

                # Also check if link text is contained in search term (handles cases like
                # "Screamer-Killers" searching for "Screamer-killer")
                if link_normalized in search_normalized and len(link_normalized) > 5:
                    score = len(link_normalized) / len(search_normalized)
                    if score > best_score:
                        best_score = score
                        best_match = slug

        if best_match and best_score > 0.5:  # Lowered threshold for better fuzzy matching
            if verbose:
                print(f"    Found fuzzy match: {best_match} (score: {best_score:.2f})")
            return best_match

        return None

    except Exception as e:
        if verbose:
            print(f"    Search error: {e}")
        return None


def extract_full_datasheet(html: str, unit_name: str, url_slug: str) -> Dict[str, Any]:
    """Extract COMPLETE datasheet from a Wahapedia unit page."""
    soup = BeautifulSoup(html, 'html.parser')

    datasheet = {
        'name': unit_name,
        'url_slug': url_slug,
        'stats': {},
        'invuln': None,
        'weapons': {'ranged': [], 'melee': []},
        'abilities': {'core': [], 'faction': [], 'unit': []},
        'points': [],
        'unit_sizes': [],
        'keywords': [],
        'faction_keywords': [],
        'leader_info': None,
        'led_by': [],
        'can_lead': [],
        'unit_composition': None,
        'default_wargear': [],
        'wargear_options': [],
        'is_epic_hero': False,
        'transport_capacity': None,
        'damaged_profile': None,
        'role': None,
    }

    # 1. Extract stats from dsProfileWrap
    for wrap in soup.find_all('div', class_='dsProfileWrap'):
        text = wrap.get_text(' ', strip=True)
        patterns = [
            (r'M\s*["\']?(\d+)["\']?"?', 'M'),
            (r'T\s+(\d+)', 'T'),
            (r'Sv\s+(\d+\+?)', 'Sv'),
            (r'W\s+(\d+)', 'W'),
            (r'Ld\s+(\d+\+?)', 'Ld'),
            (r'OC\s+(\d+)', 'OC'),
        ]
        for pattern, key in patterns:
            match = re.search(pattern, text)
            if match:
                datasheet['stats'][key] = match.group(1)

    # 2. Extract invulnerable save (look in stats area)
    for div in soup.find_all('div'):
        text = div.get_text(' ', strip=True)
        # Look for "INVULNERABLE SAVE 4+" pattern
        inv_match = re.search(r'INVULNERABLE\s+SAVE\s+(\d+)\+', text, re.IGNORECASE)
        if inv_match:
            datasheet['invuln'] = inv_match.group(1) + '++'
            break

    # 3. Extract weapons from wTable
    # Table structure: first cell often empty, weapon name in cells[1], stats in cells[2-7]
    weapon_type = None
    for table in soup.find_all('table', class_='wTable'):
        rows = table.find_all('tr')
        for row in rows:
            text = row.get_text(' ', strip=True)
            if 'RANGED WEAPONS' in text:
                weapon_type = 'ranged'
                continue
            elif 'MELEE WEAPONS' in text:
                weapon_type = 'melee'
                continue

            cells = [td.get_text(' ', strip=True) for td in row.find_all('td')]

            # Need at least 8 cells for a data row (empty + name + range + A + skill + S + AP + D)
            if len(cells) >= 8:
                # Check if this is a data row (cells[2] should be range like "6"" or "Melee")
                if re.match(r'^(\d+"|Melee)', cells[2]):
                    # Weapon name is in cells[1], stats start at cells[2]
                    raw_name = cells[1]
                    weapon_name = raw_name.split(' anti-')[0].split(' lethal')[0].split(' precision')[0].split(' devastating')[0].strip()
                    if not weapon_name:
                        continue

                    weapon = {
                        'name': weapon_name,
                        'range': cells[2],
                        'A': cells[3],
                        'skill': cells[4],
                        'S': cells[5],
                        'AP': cells[6],
                        'D': cells[7] if len(cells) > 7 else '',
                        'keywords': []
                    }

                    # Extract keywords from the raw weapon name cell
                    raw = raw_name.lower()
                    kw_patterns = [
                        r'anti-\w+\s+\d+\+',
                        r'assault', r'heavy', r'rapid fire \d+',
                        r'precision', r'devastating wounds', r'lethal hits',
                        r'sustained hits \d+', r'torrent', r'melta \d+',
                        r'blast', r'indirect fire', r'one shot',
                        r'twin-linked', r'ignores cover', r'hazardous',
                        r'pistol', r'lance', r'extra attacks',
                    ]
                    for kw_pat in kw_patterns:
                        matches = re.findall(kw_pat, raw)
                        weapon['keywords'].extend(matches)

                    if weapon_type and weapon['name']:
                        datasheet['weapons'][weapon_type].append(weapon)

    # 4. Extract abilities
    for div in soup.find_all('div', class_='dsAbility'):
        text = div.get_text(' ', strip=True)

        if text.startswith('CORE:'):
            abilities = text.replace('CORE:', '').strip().split(',')
            datasheet['abilities']['core'] = [a.strip() for a in abilities if a.strip()]

        elif text.startswith('FACTION:'):
            datasheet['abilities']['faction'] = [text.replace('FACTION:', '').strip()]

        elif ':' in text and not any(text.startswith(x) for x in ['1 ', '2 ', '3 ', '4 ', '5 ', 'This model', 'KEYWORDS', 'FACTION KEYWORDS']):
            # Unit ability - keep full description, don't truncate
            parts = text.split(':', 1)
            if len(parts) == 2 and len(parts[0]) < 50:  # Reasonable ability name length
                # Skip if it looks like wargear option or keywords
                if not any(skip in parts[0].lower() for skip in ['can replace', 'can be equipped', 'keywords']):
                    datasheet['abilities']['unit'].append({
                        'name': parts[0].strip(),
                        'description': parts[1].strip()  # Full description
                    })

    # 5. Extract points (model count + points) - search multiple patterns
    # Wahapedia uses various formats across different pages:
    #   "5 models 170" / "5 MODELS 170 PTS" / "3 models: 110 pts"
    #   Also look for dsPointsCost CSS class used on some pages
    points_patterns = [
        # Standard: "5 models 170" or "5 MODEL 170 PTS"
        r'(\d+)\s+model[s]?\s*[:\-–]?\s*(\d+)\s*(?:pts|points)?',
        # Reversed: "170 pts 5 models" (some pages)
        r'(\d+)\s*(?:pts|points)\s+(\d+)\s+model[s]?',
        # Compact: "5 models170" (no space before number)
        r'(\d+)\s+model[s]?(\d{2,})',
    ]

    # First try: look for dedicated points containers (most reliable)
    for pts_el in soup.find_all(class_=re.compile(r'dsPointsCost|Points|pointsCont', re.IGNORECASE)):
        text = pts_el.get_text(' ', strip=True)
        for pattern in points_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                models = int(match[0])
                pts = int(match[1])
                # For reversed pattern, swap
                if 'pts' in pattern and models > pts:
                    models, pts = pts, models
                if pts > 0 and models > 0 and pts < 2000:  # Sanity check
                    datasheet['points'].append({'models': models, 'points': pts})
                    datasheet['unit_sizes'].append(models)

    # Second try: broad search across all elements (fallback)
    if not datasheet['points']:
        for div in soup.find_all(['div', 'td', 'span']):
            text = div.get_text(' ', strip=True)
            for pattern in points_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    models = int(match[0])
                    pts = int(match[1])
                    if 'pts' in pattern and models > pts:
                        models, pts = pts, models
                    if pts > 0 and models > 0 and pts < 2000:
                        datasheet['points'].append({'models': models, 'points': pts})
                        datasheet['unit_sizes'].append(models)

    # Deduplicate points
    seen = set()
    unique_points = []
    for p in datasheet['points']:
        key = (p['models'], p['points'])
        if key not in seen:
            seen.add(key)
            unique_points.append(p)
    datasheet['points'] = sorted(unique_points, key=lambda x: x['models'])
    datasheet['unit_sizes'] = sorted(list(set(datasheet['unit_sizes'])))

    # 6. Extract leader info
    for div in soup.find_all('div', class_='dsAbility'):
        text = div.get_text(' ', strip=True)
        if 'can be attached to' in text.lower():
            datasheet['leader_info'] = text
            # Extract unit names
            match = re.search(r'attached to.*?:\s*(.+)', text, re.IGNORECASE)
            if match:
                units = [u.strip() for u in match.group(1).split(',')]
                datasheet['led_by'] = units

    # 7. Check for Epic Hero
    for div in soup.find_all('div', class_='dsAbility'):
        text = div.get_text(' ', strip=True)
        if 'EPIC HERO' in text.upper():
            datasheet['is_epic_hero'] = True
            break

    # 8. Extract keywords - look for specific keyword containers first
    # Wahapedia uses specific CSS classes for keywords (dsKw, Keyword, etc.)
    # IMPORTANT: Individual keywords must be short (< 40 chars). Anything longer is garbage data.

    # First, try to find keyword spans/divs with dedicated classes
    # These are more reliable than text parsing
    for kw_element in soup.find_all(class_=re.compile(r'^dsKw|^Keyword', re.IGNORECASE)):
        text = kw_element.get_text(' ', strip=True)
        # Keywords are short identifiers, not sentences or rules text
        if text and 2 < len(text) < 40 and text.upper() not in ['KEYWORDS:', 'KEYWORDS', 'FACTION KEYWORDS:', 'FACTION KEYWORDS']:
            # Skip if it looks like rules text (contains common rules words)
            if not any(x in text.lower() for x in ['attack', 'phase', 'roll', 'wound', 'damage', 'target', 'enemy', 'model', 'unit ', 'stratagem', 'detachment', 'enhancement', 'ability']):
                if text.upper() not in [k.upper() for k in datasheet['keywords']]:
                    datasheet['keywords'].append(text)

    # Also look for keywords in tooltip-enabled spans (Wahapedia pattern)
    for tooltip_span in soup.find_all('span', class_=re.compile(r'tooltip\d+')):
        text = tooltip_span.get_text(' ', strip=True)
        # Check if this looks like a keyword (UPPERCASE, short, no spaces or few spaces)
        if text and text.isupper() and 2 < len(text) < 40 and text.count(' ') <= 3:
            # Filter out common non-keywords
            skip_words = ['WHEN:', 'TARGET:', 'EFFECT:', 'RESTRICTIONS:', 'STRATAGEM', 'WARGEAR', 'ABILITY', 'DETACHMENT', 'ENHANCEMENTS']
            if text not in skip_words and not any(x in text for x in skip_words):
                if text not in [k.upper() for k in datasheet['keywords']]:
                    datasheet['keywords'].append(text)

    # Fallback: Parse text-based KEYWORDS: sections if we didn't find any keywords yet
    if not datasheet['keywords']:
        for div in soup.find_all(['div', 'td', 'span', 'p']):
            text = div.get_text(' ', strip=True)
            # Look for KEYWORDS: but NOT FACTION KEYWORDS:
            if 'KEYWORDS:' in text.upper() and 'FACTION KEYWORDS:' not in text.upper():
                # Extract keywords after KEYWORDS: up to FACTION or end of reasonable text
                # Use a more conservative pattern that stops at common boundaries
                match = re.search(r'KEYWORDS:\s*([A-Z][A-Z\s,\-\'\d]+?)(?=\s*(?:FACTION|LED BY|WARGEAR|UNIT COMPOSITION|ABILITIES|This unit|This model|$))', text, re.IGNORECASE)
                if match:
                    kw_text = match.group(1).strip()
                    # Split by comma and/or newline, filter reasonable keywords
                    keywords = []
                    for k in re.split(r'[,\n■]', kw_text):
                        k = k.strip()
                        # Valid keywords are short and don't contain sentence-like text
                        if k and 2 < len(k) < 50 and ' the ' not in k.lower() and ' is ' not in k.lower():
                            keywords.append(k)
                    if keywords:
                        datasheet['keywords'] = keywords
                        break

    # 8b. Extract FACTION KEYWORDS separately - these should be very short lists
    # Common faction keywords: ADEPTUS ASTARTES, SPACE WOLVES, IMPERIUM, etc.
    for div in soup.find_all(['div', 'td', 'span', 'p']):
        text = div.get_text(' ', strip=True)
        if 'FACTION KEYWORDS:' in text.upper():
            # Faction keywords are typically short - stop at next section or after ~100 chars
            # Look for pattern: FACTION KEYWORDS: KEYWORD1, KEYWORD2
            match = re.search(r'FACTION KEYWORDS:\s*([A-Z][A-Z\s,\-\']+?)(?=\s*(?:STRATAGEMS|DETACHMENT|ENHANCEMENTS|LED BY|WARGEAR|This unit|This model|Oath of Moment|In battle|$))', text, re.IGNORECASE)
            if match:
                fkw_text = match.group(1).strip()
                # Split and validate - faction keywords are usually 1-3 words each
                fkeywords = []
                for fk in re.split(r'[,\n■]', fkw_text):
                    fk = fk.strip()
                    # Faction keywords are short names, not sentences
                    if fk and 2 < len(fk) < 40 and fk.count(' ') <= 3:
                        fkeywords.append(fk)
                if fkeywords and not datasheet['faction_keywords']:
                    datasheet['faction_keywords'] = fkeywords
                    break
            else:
                # If regex fails, try a simpler approach: take first few comma-separated items
                # IMPORTANT: Limit to 200 chars to prevent grabbing entire page text
                simple_match = re.search(r'FACTION KEYWORDS:\s*(.{1,200}?)(?:\.|STRATAGEM|LED BY|DETACHMENT|ENHANCEMENT|This unit|This model|$)', text, re.IGNORECASE)
                if simple_match:
                    raw = simple_match.group(1).strip()
                    # Take only reasonable-looking keywords (stop at first long item)
                    fkeywords = []
                    for item in raw.split(',')[:5]:  # Max 5 faction keywords
                        item = item.strip()
                        # Individual faction keywords must be short (e.g., "IMPERIUM", "ADEPTUS ASTARTES")
                        if item and 2 < len(item) < 40 and ' ' not in item or item.count(' ') <= 2:
                            fkeywords.append(item)
                        else:
                            break  # Stop if we hit garbage
                    if fkeywords and not datasheet['faction_keywords']:
                        datasheet['faction_keywords'] = fkeywords
                        break

    # 9. Extract wargear options (full text, not truncated)
    for div in soup.find_all('div', class_='dsAbility'):
        text = div.get_text(' ', strip=True)
        if any(x in text.lower() for x in ['can be equipped with', 'may replace', 'can replace', 'can have its']):
            datasheet['wargear_options'].append(text)

    # 10. Extract unit composition (e.g., "This unit contains 1 Wolf Guard Terminator Pack Leader...")
    for div in soup.find_all('div', class_='dsAbility'):
        text = div.get_text(' ', strip=True)
        if text.lower().startswith('this unit contains') or text.lower().startswith('this model is equipped'):
            datasheet['unit_composition'] = text

    # 11. Extract default wargear (from unit composition or dedicated section)
    for div in soup.find_all('div', class_='dsAbility'):
        text = div.get_text(' ', strip=True)
        if 'is equipped with' in text.lower() and 'can be equipped' not in text.lower():
            datasheet['default_wargear'].append(text)

    # 12. Extract transport capacity
    for div in soup.find_all('div', class_='dsAbility'):
        text = div.get_text(' ', strip=True)
        if 'transport' in text.lower() and 'capacity' in text.lower():
            datasheet['transport_capacity'] = text

    # 13. Extract damaged profile (for vehicles)
    for div in soup.find_all('div', class_='dsAbility'):
        text = div.get_text(' ', strip=True)
        if 'damaged' in text.lower() and 'wounds remaining' in text.lower():
            datasheet['damaged_profile'] = text

    # 14. Extract what this unit can lead (for leader units)
    # This is CRITICAL for list-building validation - determines legal character attachments
    # Wahapedia formats: "This model can be attached to the following units: UNIT1 ■ UNIT2"
    # or "This model can be attached to the following unit: UNIT1"
    for div in soup.find_all('div', class_='dsAbility'):
        text = div.get_text(' ', strip=True)
        if 'this model can be attached to' in text.lower():
            datasheet['leader_info'] = text
            # Extract unit names - look for the colon then capture everything after
            # Handle both "following unit:" and "following units:"
            match = re.search(r'attached to the following units?[:\s]+(.+?)(?:This model|LEADER|$)', text, re.IGNORECASE | re.DOTALL)
            if match:
                units_text = match.group(1).strip()
                # Wahapedia uses ■ as delimiter between units, also handle commas and 'or'
                # First split by ■ (black square delimiter)
                if '■' in units_text:
                    units = [u.strip() for u in units_text.split('■')]
                else:
                    # Fallback to comma/and/or splitting
                    units = re.split(r'[,]|\band\b|\bor\b', units_text)

                # Clean up unit names - remove trailing periods, extra whitespace
                cleaned_units = []
                for u in units:
                    u = u.strip().rstrip('.').strip()
                    # Filter out empty strings and non-unit text
                    if u and len(u) > 2 and not u.lower().startswith('this '):
                        # Remove any parenthetical notes like "(see above)"
                        u = re.sub(r'\s*\([^)]*\)\s*', '', u).strip()
                        if u:
                            cleaned_units.append(u)

                datasheet['can_lead'] = cleaned_units

    # 15. Extract role (battlefield role)
    for div in soup.find_all('div', class_='dsRole'):
        text = div.get_text(' ', strip=True)
        if text:
            datasheet['role'] = text

    # Alternative: look for role in other locations
    if not datasheet['role']:
        for span in soup.find_all('span', class_='bfRole'):
            text = span.get_text(' ', strip=True)
            if text:
                datasheet['role'] = text
                break

    # 16. Post-process and sanitize keywords
    # Remove duplicates, clean up garbage, validate format
    datasheet['keywords'] = _sanitize_keywords(datasheet['keywords'])
    datasheet['faction_keywords'] = _sanitize_faction_keywords(datasheet['faction_keywords'])

    return datasheet


def _sanitize_keywords(keywords: List[str]) -> List[str]:
    """Clean and validate unit keywords."""
    # Known valid keywords for validation
    VALID_KEYWORD_PATTERNS = [
        # Unit types
        'INFANTRY', 'VEHICLE', 'MONSTER', 'CAVALRY', 'MOUNTED', 'BEAST', 'BEASTS',
        'WALKER', 'FLY', 'SWARM', 'BIKER', 'ARTILLERY',
        # Armor types
        'TERMINATOR', 'GRAVIS', 'PHOBOS', 'TACTICUS', 'JUMP PACK', 'PRIMARIS',
        # Role keywords
        'CHARACTER', 'EPIC HERO', 'BATTLELINE', 'TRANSPORT', 'DEDICATED TRANSPORT',
        'FORTIFICATION', 'TITANIC', 'TOWERING',
        # Stratagem-enabling keywords
        'GRENADES', 'SMOKE', 'PSYKER', 'STEALTH',
        # Faction identifiers (partial)
        'IMPERIUM', 'CHAOS', 'ADEPTUS', 'SPACE WOLVES', 'BLOOD ANGELS',
    ]

    seen = set()
    cleaned = []

    for kw in keywords:
        if not kw or not isinstance(kw, str):
            continue

        kw = kw.strip()

        # Skip if too short or too long (garbage)
        if len(kw) < 2 or len(kw) > 50:
            continue

        # Skip if it looks like rules text or garbage
        garbage_indicators = [
            ' is ', ' are ', ' the ', ' when ', ' each time ', ' if ', ' can ',
            ' you ', ' your ', ' this ', 'phase', 'roll', 'attack', 'wound',
            'damage', 'target', 'enemy', 'model ', 'unit ', 'ability',
            'stratagem', 'weapon', 'profile', 'effect', 'restriction',
            '1cp', '2cp', 'cp ', 'battle tactic', 'strategic ploy',
        ]
        kw_lower = kw.lower()
        if any(x in kw_lower for x in garbage_indicators):
            continue

        # Skip if already seen (case-insensitive)
        kw_upper = kw.upper()
        if kw_upper in seen:
            continue
        seen.add(kw_upper)

        # Normalize to uppercase for consistency
        cleaned.append(kw_upper if kw.isupper() else kw)

    return cleaned


def _sanitize_faction_keywords(faction_keywords: List[str]) -> List[str]:
    """Clean and validate faction keywords - should be very short list."""
    # Known valid faction keywords
    VALID_FACTION_KEYWORDS = {
        # Imperium factions
        'ADEPTUS ASTARTES', 'SPACE WOLVES', 'BLOOD ANGELS', 'DARK ANGELS',
        'BLACK TEMPLARS', 'DEATHWATCH', 'ULTRAMARINES', 'IMPERIAL FISTS',
        'IRON HANDS', 'RAVEN GUARD', 'SALAMANDERS', 'WHITE SCARS',
        'ASTRA MILITARUM', 'ADEPTUS MECHANICUS', 'ADEPTUS CUSTODES',
        'ADEPTA SORORITAS', 'GREY KNIGHTS', 'IMPERIAL KNIGHTS',
        'IMPERIAL AGENTS', 'INQUISITION', 'OFFICIO ASSASSINORUM',
        'IMPERIUM',
        # Chaos factions
        'CHAOS', 'CHAOS SPACE MARINES', 'DEATH GUARD', 'THOUSAND SONS',
        'WORLD EATERS', 'CHAOS DAEMONS', 'CHAOS KNIGHTS', 'HERETIC ASTARTES',
        # Xenos factions
        'AELDARI', 'DRUKHARI', 'HARLEQUINS', 'YNNARI',
        'ORKS', 'TYRANIDS', 'GENESTEALER CULTS', 'NECRONS', 'T\'AU EMPIRE',
        'LEAGUES OF VOTANN', 'KROOT',
    }

    seen = set()
    cleaned = []

    for fkw in faction_keywords:
        if not fkw or not isinstance(fkw, str):
            continue

        fkw = fkw.strip().upper()

        # Skip if too short or too long
        if len(fkw) < 3 or len(fkw) > 30:
            continue

        # Skip if it looks like garbage
        garbage_indicators = [
            'STRATAGEM', '1CP', '2CP', 'BATTLE TACTIC', 'STRATEGIC PLOY',
            'WARGEAR', 'ENHANCEMENT', 'DETACHMENT', 'ABILITY', 'RULE',
            'THIS ', 'WHEN ', 'THE ', 'PHASE', 'DESTROYED',
        ]
        if any(x in fkw for x in garbage_indicators):
            continue

        # Skip if already seen
        if fkw in seen:
            continue
        seen.add(fkw)

        # Only include if it looks like a valid faction keyword
        # Check if it matches known faction or looks reasonable
        if fkw in VALID_FACTION_KEYWORDS:
            cleaned.append(fkw)
        elif fkw.count(' ') <= 2 and len(fkw) <= 25:
            # Allow unknown faction keywords if they're short and clean
            cleaned.append(fkw)

    return cleaned


def clean_leader_list(leader_list: List[str]) -> List[str]:
    """Clean up leader unit names - split multi-unit strings properly."""
    # Known unit names to help with parsing concatenated unit lists
    # IMPORTANT: Longer names first to avoid partial matches (e.g., "Blood Claws" before "Claws")
    KNOWN_UNITS = [
        # Space Wolves - specific units first
        'Wolf Guard Terminators', 'Wolf Guard Headtakers', 'Wolf Guard Battle Leader',
        'Thunderwolf Cavalry', 'Fenrisian Wolves', 'Blood Claws', 'Grey Hunters', 'Wulfen',
        'Long Fangs', 'Skyclaws', 'Hounds of Morkai', 'Wolf Scouts',
        # Space Marines - longer names first
        'Assault Intercessor Squad', 'Heavy Intercessor Squad', 'Intercessor Squad',
        'Terminator Assault Squad', 'Terminator Squad', 'Tactical Squad',
        'Sternguard Veteran Squad', 'Vanguard Veteran Squad', 'Bladeguard Veteran Squad',
        'Hellblaster Squad', 'Infiltrator Squad', 'Incursor Squad', 'Eradicator Squad',
        'Aggressor Squad', 'Inceptor Squad', 'Eliminator Squad', 'Suppressor Squad',
        'Desolation Squad', 'Infernus Squad', 'Scout Squad', 'Company Heroes',
        # T'au
        'Crisis Battlesuits', 'Stealth Battlesuits', 'Broadside Battlesuits',
        'Strike Team', 'Breacher Team', 'Pathfinder Team', 'Kroot Carnivores',
        # Orks
        'Burna Boyz', 'Flash Gitz', 'Tankbustas', 'Meganobz', 'Nobz', 'Boyz',
        'Gretchin', 'Lootas', 'Kommandos', 'Stormboyz', 'Beast Snagga Boyz',
        # Astra Militarum
        'Cadian Shock Troops', 'Catachan Jungle Fighters', 'Infantry Squad',
        'Kasrkin', 'Tempestus Scions', 'Bullgryns', 'Ogryn Bodyguard', 'Ratlings',
        # Tyranids
        'Tyranid Warriors', 'Termagants', 'Hormagaunts', 'Genestealers', 'Zoanthropes',
        'Neurogaunts', 'Barbgaunts', 'Gargoyles', 'Ripper Swarms',
    ]

    cleaned = []
    for item in leader_list:
        clean = item
        # Remove common prefixes
        for prefix in ['the following unit:', 'the following units:', 'following unit:', 'following units:']:
            if clean.lower().startswith(prefix):
                clean = clean[len(prefix):].strip()

        # First, try splitting on ■ delimiter (Wahapedia standard)
        if '■' in clean:
            for part in clean.split('■'):
                part = part.strip()
                if part and len(part) > 2:
                    cleaned.append(part)
            continue

        # Try splitting on comma
        if ',' in clean:
            for part in clean.split(','):
                part = part.strip()
                if part and len(part) > 2:
                    cleaned.append(part)
            continue

        # Split on ' or '
        if ' or ' in clean.lower():
            parts = re.split(r'\s+or\s+', clean, flags=re.IGNORECASE)
            for part in parts:
                if part.strip():
                    cleaned.append(part.strip())
            continue

        # No delimiters found - try to match known unit names from concatenated string
        # This handles cases like "Blood Claws Wolf Guard Headtakers" (no delimiter)
        remaining = clean
        found = []
        for unit in sorted(KNOWN_UNITS, key=len, reverse=True):  # Longest first
            if unit.lower() in remaining.lower():
                found.append(unit)
                # Remove the matched unit from remaining (case insensitive)
                remaining = re.sub(re.escape(unit), '', remaining, flags=re.IGNORECASE).strip()

        if found:
            cleaned.extend(found)
        elif remaining.strip() and len(remaining.strip()) > 2:
            # If no known units matched but we have content, keep original
            cleaned.append(clean)

    # Deduplicate while preserving order
    seen = set()
    result = []
    for item in cleaned:
        item_clean = item.strip()
        if item_clean and item_clean.lower() not in seen:
            seen.add(item_clean.lower())
            result.append(item_clean)

    return result


def generate_compact_datasheet(full_datasheet: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate COMPACT format from full datasheet.
    Contains ONLY what's needed for list-building validation:
    - Points (with model counts)
    - Unit sizes
    - Epic Hero status
    - Key keywords (for Rule of Three, leader validation)
    - Leader attachments
    - Wargear that affects points (if any)
    """
    compact = {
        'name': full_datasheet['name'],
        'pts': None,  # Will be set below
        'sizes': full_datasheet.get('unit_sizes', []),
        'epic_hero': full_datasheet.get('is_epic_hero', False),
    }

    # Extract points - simplify to per-model or flat cost
    points = full_datasheet.get('points', [])
    if points:
        if len(points) == 1:
            # Single size unit - just show the cost
            compact['pts'] = points[0]['points']
            compact['models'] = points[0]['models']
        else:
            # Variable size - show per-model cost if consistent
            pts_per_model = []
            for p in points:
                if p['models'] > 0:
                    pts_per_model.append(p['points'] / p['models'])

            if pts_per_model and len(set(pts_per_model)) == 1:
                # Consistent per-model pricing
                compact['pts_per_model'] = int(pts_per_model[0])
            else:
                # Variable pricing - keep full breakdown
                compact['pts_table'] = {str(p['models']): p['points'] for p in points}

    # Key keywords for validation - ALWAYS include if present
    # These keywords affect gameplay mechanics, stratagems, and list-building rules
    # SAFETY: Skip any keyword longer than 40 chars — those are garbage from HTML parsing
    key_keywords = []
    keywords = [kw for kw in full_datasheet.get('keywords', []) if len(kw) < 40]
    for kw in keywords:
        kw_upper = kw.upper()
        # Keywords that affect list-building rules and stratagem eligibility
        # IMPORTANT: Many stratagems key off these keywords (e.g., GRENADES for Grenade stratagem)
        if any(x in kw_upper for x in [
            # List-building keywords
            'BATTLELINE', 'CHARACTER', 'EPIC HERO', 'TRANSPORT', 'DEDICATED TRANSPORT',
            # Unit type keywords (affects many rules)
            'INFANTRY', 'MONSTER', 'VEHICLE', 'MOUNTED', 'FLY', 'CAVALRY',
            'TERMINATOR', 'PSYKER', 'SYNAPSE', 'BEAST', 'BEASTS', 'SWARM',
            'WALKER', 'BIKER', 'JUMP PACK', 'GRAVIS', 'PHOBOS', 'PRIMARIS',
            # Stratagem-enabling keywords (CRITICAL for gameplay)
            'GRENADES', 'SMOKE', 'STEALTH',
            # Faction-specific keywords that unlock abilities
            'IMPERIUM', 'CHAOS', 'AELDARI', 'TYRANIDS', 'ORKS', 'NECRONS',
            'ADEPTUS ASTARTES', 'SPACE WOLVES', 'BLOOD ANGELS', 'DARK ANGELS',
        ]):
            key_keywords.append(kw)

    # Always include ALL keywords for comprehensive gameplay reference
    # The full keyword list is important for stratagem/ability interactions
    if keywords:
        # Deduplicate while preserving order
        seen = set()
        all_keywords = []
        # Add filtered keywords first (most important)
        for kw in key_keywords:
            kw_upper = kw.upper()
            if kw_upper not in seen:
                seen.add(kw_upper)
                all_keywords.append(kw)
        # Then add remaining keywords
        for kw in keywords:
            kw_upper = kw.upper()
            if kw_upper not in seen:
                seen.add(kw_upper)
                all_keywords.append(kw)
        compact['keywords'] = all_keywords

    # Leader info (who can this lead / who can lead this) - CRITICAL for list validation
    # This data is essential for blocking gate 7 (leader attachment validation)
    if full_datasheet.get('can_lead'):
        leads = clean_leader_list(full_datasheet['can_lead'])
        if leads:
            compact['leads'] = leads
            compact['is_leader'] = True  # Flag for quick identification
    if full_datasheet.get('led_by'):
        led_by = clean_leader_list(full_datasheet['led_by'])
        if led_by:
            compact['led_by'] = led_by

    # Core abilities that affect list-building (Deep Strike for reserves planning)
    core = full_datasheet.get('abilities', {}).get('core', [])
    if core:
        compact['core'] = core

    return compact


def generate_compact_faction(full_faction_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate compact faction file from full faction data."""
    compact = {
        'faction': full_faction_data['faction'],
        'last_updated': full_faction_data['last_updated'],
        'schema': 'compact-v1',
        'unit_count': full_faction_data['unit_count'],
        'units': {}
    }

    for name, full_unit in full_faction_data.get('units', {}).items():
        if 'error' not in full_unit:
            compact['units'][name] = generate_compact_datasheet(full_unit)

    return compact


def refresh_faction(faction: str, verbose: bool = True) -> Dict[str, Any]:
    """Refresh full datasheet cache for a faction."""
    # If faction has hardcoded units, use those; otherwise auto-discover
    if faction not in FACTION_URLS:
        if faction in FACTION_BASE_URLS:
            # No hardcoded units - use auto-discover
            if verbose:
                print(f"No hardcoded units for '{faction}', using auto-discover...")
            return refresh_faction_autodiscover(faction, verbose)
        else:
            print(f"ERROR: Unknown faction '{faction}'")
            print(f"Available factions: {list(FACTION_BASE_URLS.keys())}")
            return None

    config = FACTION_URLS[faction]
    base_url = config['base_url']
    units = config['units']

    faction_data = {
        'faction': faction,
        'last_updated': datetime.now(timezone.utc).isoformat(),
        'source': 'wahapedia',
        'schema_version': '2.0',
        'unit_count': len(units),
        'units': {}
    }

    if verbose:
        print(f"Refreshing {faction} ({len(units)} units - full datasheets)...")

    for slug, name in units:
        url = base_url + slug
        if verbose:
            print(f"  {name}...", end=' ', flush=True)

        try:
            html = fetch_page(url)
            data = extract_full_datasheet(html, name, slug)
            faction_data['units'][name] = data

            if verbose:
                pts_str = '/'.join([str(p['points']) for p in data['points']]) + 'pts'
                stats = data.get('stats', {})
                stat_str = f"M{stats.get('M', '?')} T{stats.get('T', '?')} W{stats.get('W', '?')}"
                print(f"OK ({pts_str}, {stat_str})")

            time.sleep(0.3)  # Be nice to server

        except urllib.error.HTTPError as e:
            if e.code == 404:
                # URL not found - search for correct slug on Wahapedia
                if verbose:
                    print(f"404 - searching...", end=' ', flush=True)

                correct_slug = search_unit_on_wahapedia(faction, name, verbose=False)
                if correct_slug and correct_slug != slug:
                    # Found a different slug - try fetching with it
                    new_url = base_url + correct_slug
                    try:
                        html = fetch_page(new_url)
                        data = extract_full_datasheet(html, name, correct_slug)
                        faction_data['units'][name] = data

                        if verbose:
                            pts_str = '/'.join([str(p['points']) for p in data['points']]) + 'pts'
                            stats = data.get('stats', {})
                            stat_str = f"M{stats.get('M', '?')} T{stats.get('T', '?')} W{stats.get('W', '?')}"
                            print(f"FIXED -> {correct_slug} ({pts_str}, {stat_str})")

                        time.sleep(0.3)
                        continue
                    except Exception as retry_e:
                        if verbose:
                            print(f"RETRY FAILED: {retry_e}")

                # Search failed or retry failed
                if verbose:
                    print(f"ERROR: HTTP Error 404: Not Found")
                faction_data['units'][name] = {
                    'name': name,
                    'url_slug': slug,
                    'error': str(e)
                }
            else:
                if verbose:
                    print(f"ERROR: {e}")
                faction_data['units'][name] = {
                    'name': name,
                    'url_slug': slug,
                    'error': str(e)
                }

        except Exception as e:
            if verbose:
                print(f"ERROR: {e}")
            faction_data['units'][name] = {
                'name': name,
                'url_slug': slug,
                'error': str(e)
            }

    # Save FULL faction cache
    cache_file = os.path.join(DATA_DIR, f'{faction}.json')
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(cache_file, 'w') as f:
        json.dump(faction_data, f, indent=2)

    # Generate and save COMPACT version
    compact_data = generate_compact_faction(faction_data)
    compact_file = os.path.join(DATA_DIR, f'{faction}.compact.json')
    with open(compact_file, 'w') as f:
        json.dump(compact_data, f, indent=2)

    if verbose:
        full_size = os.path.getsize(cache_file)
        compact_size = os.path.getsize(compact_file)
        reduction = (1 - compact_size / full_size) * 100
        print(f"Generated compact format: {compact_size:,} bytes ({reduction:.0f}% smaller)")

    # Update metadata
    metadata = load_metadata()
    if faction not in metadata.get('factions_cached', []):
        metadata.setdefault('factions_cached', []).append(faction)
    metadata['cache_invalid'] = False
    metadata['invalidation_reason'] = None
    metadata['last_global_refresh'] = datetime.now(timezone.utc).isoformat()
    metadata['schema_version'] = '2.0'
    save_metadata(metadata)

    if verbose:
        print(f"Saved to {cache_file}")

    return faction_data


def refresh_all_factions(verbose: bool = True):
    """Refresh all user factions."""
    print("Refreshing all user factions (full datasheets)...")
    for faction in USER_FACTIONS:
        if faction in FACTION_URLS:
            refresh_faction(faction, verbose)
        else:
            print(f"  Skipping {faction} (no URL config)")


def get_unit(faction: str, unit_name: str) -> Optional[Dict]:
    """Get full datasheet for a unit, refreshing cache if needed."""
    metadata = load_metadata()

    is_stale, reason = is_cache_stale(metadata, faction)
    if is_stale:
        print(f"Cache stale ({reason}), refreshing {faction}...")
        refresh_faction(faction)

    cache_file = os.path.join(DATA_DIR, f'{faction}.json')
    if not os.path.exists(cache_file):
        return None

    with open(cache_file, 'r') as f:
        data = json.load(f)

    return data.get('units', {}).get(unit_name)


def validate_faction(faction: str) -> bool:
    """Validate cached data against live Wahapedia."""
    if faction not in FACTION_URLS:
        print(f"ERROR: Unknown faction '{faction}'")
        return False

    cache_file = os.path.join(DATA_DIR, f'{faction}.json')
    if not os.path.exists(cache_file):
        print(f"No cache for {faction}, cannot validate")
        return False

    with open(cache_file, 'r') as f:
        cached = json.load(f)

    config = FACTION_URLS[faction]
    base_url = config['base_url']

    # Pick 3 random units to validate
    import random
    units = list(cached.get('units', {}).items())
    sample = random.sample(units, min(3, len(units)))

    print(f"Validating {faction} (spot-checking {len(sample)} units)...")

    mismatches = []
    for name, cached_data in sample:
        slug = cached_data.get('url_slug')
        if not slug:
            continue

        url = base_url + slug
        print(f"  Checking {name}...", end=' ')

        try:
            html = fetch_page(url)
            live_data = extract_full_datasheet(html, name, slug)

            # Compare points
            cached_pts = {(p['models'], p['points']) for p in cached_data.get('points', [])}
            live_pts = {(p['models'], p['points']) for p in live_data.get('points', [])}

            # Compare stats
            cached_stats = cached_data.get('stats', {})
            live_stats = live_data.get('stats', {})

            if cached_pts != live_pts:
                print(f"MISMATCH (points)!")
                print(f"    Cached: {cached_pts}")
                print(f"    Live:   {live_pts}")
                mismatches.append(f"{name} (points)")
            elif cached_stats != live_stats:
                print(f"MISMATCH (stats)!")
                print(f"    Cached: {cached_stats}")
                print(f"    Live:   {live_stats}")
                mismatches.append(f"{name} (stats)")
            else:
                print("OK")

            time.sleep(0.3)

        except Exception as e:
            print(f"ERROR: {e}")

    if mismatches:
        print(f"\nMISMATCHES FOUND: {mismatches}")
        print("Cache is INVALID - run --faction to refresh")
        invalidate_cache(f"Validation failed: {', '.join(mismatches)}")
        return False

    print("\nValidation PASSED")
    return True


def show_unit(faction: str, unit_name: str):
    """Display a unit's full datasheet."""
    unit = get_unit(faction, unit_name)
    if not unit:
        print(f"Unit '{unit_name}' not found in {faction}")
        return

    print(f"\n{'='*60}")
    print(f"  {unit['name']}")
    print(f"{'='*60}")

    # Stats
    stats = unit.get('stats', {})
    invuln = unit.get('invuln', '')
    inv_str = f"/{invuln}" if invuln else ""
    print(f"\nSTATS: M{stats.get('M', '?')}\" | T{stats.get('T', '?')} | "
          f"Sv{stats.get('Sv', '?')}{inv_str} | W{stats.get('W', '?')} | "
          f"Ld{stats.get('Ld', '?')} | OC{stats.get('OC', '?')}")

    # Points
    pts = unit.get('points', [])
    if pts:
        pts_str = ', '.join([f"{p['models']} model{'s' if p['models']>1 else ''} = {p['points']}pts" for p in pts])
        print(f"POINTS: {pts_str}")

    # Epic Hero
    if unit.get('is_epic_hero'):
        print("TYPE: EPIC HERO (unique)")

    # Weapons
    for wtype in ['ranged', 'melee']:
        weapons = unit.get('weapons', {}).get(wtype, [])
        if weapons:
            print(f"\n{wtype.upper()} WEAPONS:")
            for w in weapons:
                kw = ', '.join(w.get('keywords', []))
                kw_str = f" [{kw}]" if kw else ""
                print(f"  {w['name']}: {w['range']} A{w['A']} {w['skill']} S{w['S']} AP{w['AP']} D{w['D']}{kw_str}")

    # Abilities
    abilities = unit.get('abilities', {})
    if abilities.get('core'):
        print(f"\nCORE: {', '.join(abilities['core'])}")
    if abilities.get('faction'):
        print(f"FACTION: {', '.join(abilities['faction'])}")
    if abilities.get('unit'):
        print("\nABILITIES:")
        for a in abilities['unit']:
            print(f"  {a['name']}: {a['description'][:100]}...")

    # Leader
    if unit.get('leader_info'):
        print(f"\nLEADER: {unit['leader_info']}")

    # Keywords
    if unit.get('keywords'):
        print(f"\nKEYWORDS: {', '.join(unit['keywords'])}")

    print()


def show_compact(faction: str):
    """Display compact format for a faction."""
    compact_file = os.path.join(DATA_DIR, f'{faction}.compact.json')

    if not os.path.exists(compact_file):
        # Try to generate from full cache
        full_file = os.path.join(DATA_DIR, f'{faction}.json')
        if os.path.exists(full_file):
            print(f"Generating compact format from existing full cache...")
            with open(full_file, 'r') as f:
                full_data = json.load(f)
            compact_data = generate_compact_faction(full_data)
            with open(compact_file, 'w') as f:
                json.dump(compact_data, f, indent=2)
        else:
            print(f"No cache for {faction}. Run --faction {faction} first.")
            return

    with open(compact_file, 'r') as f:
        compact = json.load(f)

    print(f"\n{'='*60}")
    print(f"  {faction.upper()} - COMPACT FORMAT")
    print(f"  Schema: {compact.get('schema', 'unknown')}")
    print(f"  Units: {compact.get('unit_count', 0)}")
    print(f"  Updated: {compact.get('last_updated', 'unknown')[:10]}")
    print(f"{'='*60}\n")

    for name, unit in compact.get('units', {}).items():
        # Build points string
        if unit.get('pts'):
            pts_str = f"{unit['pts']}pts"
            if unit.get('models', 1) > 1:
                pts_str += f" ({unit['models']} models)"
        elif unit.get('pts_per_model'):
            pts_str = f"{unit['pts_per_model']}pts/model"
        elif unit.get('pts_table'):
            pts_str = str(unit['pts_table'])
        else:
            pts_str = "?pts"

        # Flags
        flags = []
        if unit.get('epic_hero'):
            flags.append('EPIC HERO')
        if unit.get('core'):
            flags.extend(unit['core'])

        flags_str = f" [{', '.join(flags)}]" if flags else ""

        print(f"  {name}: {pts_str}{flags_str}")

    print()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == '--compact' and len(sys.argv) >= 3:
        faction = sys.argv[2]
        show_compact(faction)

    elif cmd == '--faction' and len(sys.argv) >= 3:
        faction = sys.argv[2]
        refresh_faction(faction)

    elif cmd == '--discover' and len(sys.argv) >= 3:
        # Auto-discover ALL units from faction index
        faction = sys.argv[2]
        refresh_faction_autodiscover(faction)

    elif cmd == '--add-unit' and len(sys.argv) >= 4:
        # Add a single unit to cache: --add-unit faction "Unit Name" [url-slug]
        faction = sys.argv[2]
        unit_name = sys.argv[3]
        url_slug = sys.argv[4] if len(sys.argv) >= 5 else None
        success = add_unit_to_cache(faction, unit_name, url_slug)
        sys.exit(0 if success else 1)

    elif cmd == '--list-discovered' and len(sys.argv) >= 3:
        # Just list discovered units without fetching
        faction = sys.argv[2]
        units = discover_faction_units(faction, verbose=False)
        print(f"\n{faction.upper()} - {len(units)} units discovered:\n")
        for slug, name in sorted(units, key=lambda x: x[1]):
            print(f"  {name} ({slug})")
        print()

    elif cmd == '--refresh-all':
        refresh_all_factions()

    elif cmd == '--check' and len(sys.argv) >= 3:
        faction = sys.argv[2]
        metadata = load_metadata()
        is_stale, reason = is_cache_stale(metadata, faction)
        if is_stale:
            print(f"STALE: {reason}")
            sys.exit(1)
        else:
            print(f"FRESH: {reason}")
            sys.exit(0)

    elif cmd == '--validate' and len(sys.argv) >= 3:
        faction = sys.argv[2]
        success = validate_faction(faction)
        sys.exit(0 if success else 1)

    elif cmd == '--invalidate':
        reason = sys.argv[2] if len(sys.argv) >= 3 else "Manual invalidation"
        invalidate_cache(reason)

    elif cmd == '--status':
        metadata = load_metadata()
        print(json.dumps(metadata, indent=2))

    elif cmd == '--unit' and len(sys.argv) >= 4:
        faction = sys.argv[2]
        unit_name = sys.argv[3]
        show_unit(faction, unit_name)

    elif cmd == '--list-factions':
        print("\n=== AVAILABLE FACTIONS ===\n")
        print("IMPERIUM:")
        for f in ['adepta-sororitas', 'adeptus-custodes', 'adeptus-mechanicus',
                  'astra-militarum', 'grey-knights', 'imperial-agents',
                  'imperial-knights', 'space-marines', 'space-wolves']:
            cached = '✓' if os.path.exists(os.path.join(DATA_DIR, f'{f}.json')) else ' '
            print(f"  [{cached}] {f}")
        print("\nCHAOS:")
        for f in ['chaos-daemons', 'chaos-knights', 'chaos-space-marines',
                  'death-guard', 'emperors-children', 'thousand-sons', 'world-eaters']:
            cached = '✓' if os.path.exists(os.path.join(DATA_DIR, f'{f}.json')) else ' '
            print(f"  [{cached}] {f}")
        print("\nXENOS:")
        for f in ['aeldari', 'drukhari', 'genestealer-cults', 'leagues-of-votann',
                  'necrons', 'orks', 'tau-empire', 'tyranids']:
            cached = '✓' if os.path.exists(os.path.join(DATA_DIR, f'{f}.json')) else ' '
            print(f"  [{cached}] {f}")
        print("\nUse --discover {faction} to build cache for any faction.")
        print()

    else:
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
