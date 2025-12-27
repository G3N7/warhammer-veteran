#!/usr/bin/env python3
"""
Wahapedia Datasheet Scraper
Extracts FULL unit datasheets from Wahapedia into per-faction JSON cache files.
This is the SINGLE SOURCE OF TRUTH for all unit data (stats, weapons, abilities, points).

Usage:
    python scrape-wahapedia.py --faction space-wolves    # Refresh one faction
    python scrape-wahapedia.py --refresh-all             # Refresh all user factions
    python scrape-wahapedia.py --check space-wolves      # Check if cache is stale
    python scrape-wahapedia.py --validate space-wolves   # Validate cache against live data
    python scrape-wahapedia.py --unit space-wolves "Arjac Rockfist"  # Show one unit
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

# User's factions (from memories.md)
USER_FACTIONS = [
    'space-wolves',
    'space-marines',  # Ultramarines use base SM
    'orks',
    'astra-militarum',
    'tyranids',
    'tau-empire'
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
        ]
    },
    # Add more factions as needed
}


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
        'unit_composition': None,
        'wargear_options': [],
        'is_epic_hero': False,
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

        elif ':' in text and not any(text.startswith(x) for x in ['1 ', '2 ', '3 ', '4 ', '5 ', 'This model', 'KEYWORDS']):
            # Unit ability
            parts = text.split(':', 1)
            if len(parts) == 2 and len(parts[0]) < 50:  # Reasonable ability name length
                datasheet['abilities']['unit'].append({
                    'name': parts[0].strip(),
                    'description': parts[1].strip()[:500]  # Truncate long descriptions
                })

    # 5. Extract points (model count + points)
    for div in soup.find_all('div', class_='dsAbility'):
        text = div.get_text(' ', strip=True)
        match = re.match(r'(\d+)\s+model[s]?\s+(\d+)', text)
        if match:
            models = int(match.group(1))
            pts = int(match.group(2))
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

    # 8. Extract keywords
    for div in soup.find_all('div', class_='dsAbility'):
        text = div.get_text(' ', strip=True)
        if text.startswith('KEYWORDS:'):
            kw_text = text.replace('KEYWORDS:', '').strip()
            datasheet['keywords'] = [k.strip() for k in kw_text.split(',') if k.strip()]
        elif text.startswith('FACTION KEYWORDS:'):
            fkw_text = text.replace('FACTION KEYWORDS:', '').strip()
            datasheet['faction_keywords'] = [k.strip() for k in fkw_text.split(',') if k.strip()]

    # 9. Extract wargear options
    for div in soup.find_all('div', class_='dsAbility'):
        text = div.get_text(' ', strip=True)
        if any(x in text.lower() for x in ['can be equipped with', 'may replace', 'can replace']):
            datasheet['wargear_options'].append(text[:300])

    return datasheet


def refresh_faction(faction: str, verbose: bool = True) -> Dict[str, Any]:
    """Refresh full datasheet cache for a faction."""
    if faction not in FACTION_URLS:
        print(f"ERROR: Unknown faction '{faction}'")
        print(f"Available: {list(FACTION_URLS.keys())}")
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

        except Exception as e:
            if verbose:
                print(f"ERROR: {e}")
            faction_data['units'][name] = {
                'name': name,
                'url_slug': slug,
                'error': str(e)
            }

    # Save faction cache
    cache_file = os.path.join(DATA_DIR, f'{faction}.json')
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(cache_file, 'w') as f:
        json.dump(faction_data, f, indent=2)

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


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == '--faction' and len(sys.argv) >= 3:
        faction = sys.argv[2]
        refresh_faction(faction)

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

    else:
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
