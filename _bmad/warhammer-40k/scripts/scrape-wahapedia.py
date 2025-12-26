#!/usr/bin/env python3
"""
Wahapedia Datasheet Scraper
Extracts unit data from Wahapedia pages into structured JSON.

Usage:
    python scrape-wahapedia.py <url> [output.json]
    python scrape-wahapedia.py --faction <faction-slug> [output-dir]
"""

import sys
import re
import json
import urllib.request
import urllib.error
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional


def fetch_page(url: str) -> str:
    """Fetch HTML content from URL."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode('utf-8')


def parse_stat_value(text: str) -> str:
    """Clean up stat values."""
    return text.strip().replace('"', '').replace("'", '')


def extract_unit_stats(soup: BeautifulSoup) -> Dict[str, str]:
    """Extract M/T/Sv/W/Ld/OC from the stat boxes."""
    stats = {}

    # Look for the dsCharacteristics table or stat boxes
    # Stats are typically in elements with specific classes
    stat_names = ['M', 'T', 'Sv', 'W', 'Ld', 'OC']

    # Method 1: Look for dsStatBig or similar stat elements
    for stat in stat_names:
        # Try various patterns Wahapedia uses
        stat_elem = soup.find(text=re.compile(f'^{stat}$', re.I))
        if stat_elem:
            parent = stat_elem.find_parent()
            if parent:
                # Value is usually in next sibling or nearby element
                value_elem = parent.find_next_sibling()
                if value_elem:
                    stats[stat] = parse_stat_value(value_elem.get_text())

    # Method 2: Look for the characteristics row in dsStatGrid
    char_table = soup.find('table', class_=re.compile('dsCharacteristics|dsStatGrid'))
    if char_table:
        rows = char_table.find_all('tr')
        if len(rows) >= 2:
            headers = [th.get_text().strip() for th in rows[0].find_all(['th', 'td'])]
            values = [td.get_text().strip() for td in rows[1].find_all('td')]
            for h, v in zip(headers, values):
                if h in stat_names:
                    stats[h] = v

    # Method 3: Look for dsStatBig divs (common pattern)
    stat_boxes = soup.find_all('div', class_='dsStatBig')
    for box in stat_boxes:
        text = box.get_text().strip()
        # Usually format is "M\n10"" or similar
        lines = text.split('\n')
        if len(lines) >= 2 and lines[0].strip() in stat_names:
            stats[lines[0].strip()] = lines[1].strip()

    return stats


def extract_weapons(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract weapon profiles from weapons tables."""
    weapons = []

    # Find weapon tables - usually have headers: RANGE, A, WS/BS, S, AP, D
    weapon_tables = soup.find_all('table')

    for table in weapon_tables:
        # Check if this looks like a weapon table
        header_row = table.find('tr')
        if not header_row:
            continue

        headers = [th.get_text().strip().upper() for th in header_row.find_all(['th', 'td'])]

        # Must have RANGE and either WS or BS to be a weapon table
        if 'RANGE' not in headers:
            continue
        if 'WS' not in headers and 'BS' not in headers:
            continue

        # Parse weapon rows
        rows = table.find_all('tr')[1:]  # Skip header
        for row in rows:
            cells = row.find_all('td')
            if len(cells) < 6:
                continue

            weapon = {}
            for i, header in enumerate(headers):
                if i < len(cells):
                    value = cells[i].get_text().strip()
                    # First column is usually weapon name
                    if i == 0:
                        weapon['name'] = value
                    else:
                        weapon[header.lower()] = value

            if weapon.get('name'):
                weapons.append(weapon)

    return weapons


def extract_points(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    """Extract points costs from PriceTag elements."""
    points = []

    price_tags = soup.find_all('div', class_='PriceTag')

    for tag in price_tags:
        pts = tag.get_text().strip()
        if not pts.isdigit():
            continue

        pts = int(pts)

        # Find associated model count - usually in sibling td or parent context
        tr = tag.find_parent('tr')
        if tr:
            tds = tr.find_all('td')
            model_info = ""
            for td in tds:
                if td.find('div', class_='PriceTag') is None:
                    model_info = td.get_text().strip()

            if model_info:
                # Parse model count from text like "5 models" or "10 models"
                match = re.search(r'(\d+)\s*model', model_info.lower())
                if match:
                    points.append({
                        'models': int(match.group(1)),
                        'points': pts,
                        'description': model_info
                    })
                else:
                    points.append({
                        'description': model_info,
                        'points': pts
                    })

    return points


def extract_abilities(soup: BeautifulSoup) -> List[Dict[str, str]]:
    """Extract unit abilities."""
    abilities = []

    # Look for dsAbility divs or ability sections
    ability_sections = soup.find_all('div', class_='dsAbility')

    for section in ability_sections:
        text = section.get_text().strip()

        # Look for ability name in bold
        bold = section.find('b')
        if bold:
            name = bold.get_text().strip().rstrip(':')
            # Get description after the bold name
            desc = text.replace(bold.get_text(), '').strip()
            if name and not name.startswith('Every model'):
                abilities.append({
                    'name': name,
                    'description': desc[:500]  # Truncate long descriptions
                })

    return abilities


def extract_keywords(soup: BeautifulSoup) -> Dict[str, List[str]]:
    """Extract unit and faction keywords."""
    keywords = {
        'unit': [],
        'faction': []
    }

    # Look for KEYWORDS section
    keyword_text = soup.find(text=re.compile('KEYWORDS:', re.I))
    if keyword_text:
        parent = keyword_text.find_parent()
        if parent:
            full_text = parent.get_text()
            # Split by FACTION KEYWORDS if present
            if 'FACTION KEYWORDS' in full_text.upper():
                parts = re.split(r'FACTION\s*KEYWORDS', full_text, flags=re.I)
                if len(parts) >= 1:
                    # Unit keywords
                    unit_part = parts[0].replace('KEYWORDS:', '').strip()
                    keywords['unit'] = [k.strip() for k in unit_part.split(',') if k.strip()]
                if len(parts) >= 2:
                    # Faction keywords
                    faction_part = parts[1].strip().lstrip(':').strip()
                    keywords['faction'] = [k.strip() for k in faction_part.split(',') if k.strip()]

    return keywords


def extract_unit_composition(soup: BeautifulSoup) -> Dict[str, Any]:
    """Extract unit composition info."""
    composition = {
        'description': '',
        'models': [],
        'equipment': ''
    }

    # Look for UNIT COMPOSITION section
    comp_header = soup.find(text=re.compile('UNIT COMPOSITION', re.I))
    if comp_header:
        parent = comp_header.find_parent()
        if parent:
            # Find the next dsAbility div
            next_div = parent.find_next('div', class_='dsAbility')
            if next_div:
                text = next_div.get_text().strip()
                composition['description'] = text

                # Parse model range (e.g., "5-10 Fenrisian Wolves")
                match = re.search(r'(\d+)-(\d+)\s+(.+)', text)
                if match:
                    composition['min_models'] = int(match.group(1))
                    composition['max_models'] = int(match.group(2))

                # Find equipment line
                equip_match = re.search(r'Every model is equipped with:\s*(.+)', text, re.I)
                if equip_match:
                    composition['equipment'] = equip_match.group(1).strip()

    return composition


def extract_datasheet(html: str) -> Dict[str, Any]:
    """Extract all datasheet information from HTML."""
    soup = BeautifulSoup(html, 'html.parser')

    # Get unit name from title
    title = soup.find('title')
    unit_name = title.get_text().split('|')[0].strip() if title else 'Unknown'

    # Build datasheet object
    datasheet = {
        'name': unit_name,
        'stats': extract_unit_stats(soup),
        'weapons': extract_weapons(soup),
        'points': extract_points(soup),
        'abilities': extract_abilities(soup),
        'keywords': extract_keywords(soup),
        'composition': extract_unit_composition(soup)
    }

    return datasheet


def main():
    if len(sys.argv) < 2:
        print("Usage: python scrape-wahapedia.py <url> [output.json]")
        print("       python scrape-wahapedia.py --test")
        sys.exit(1)

    if sys.argv[1] == '--test':
        # Test with local file if available
        try:
            with open('/tmp/fenrisian-wolves.html', 'r') as f:
                html = f.read()
            datasheet = extract_datasheet(html)
            print(json.dumps(datasheet, indent=2))
        except FileNotFoundError:
            print("Test file not found. Run with a URL instead.")
        sys.exit(0)

    url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"Fetching: {url}")
    html = fetch_page(url)

    datasheet = extract_datasheet(html)

    if output_file:
        with open(output_file, 'w') as f:
            json.dump(datasheet, f, indent=2)
        print(f"Saved to: {output_file}")
    else:
        print(json.dumps(datasheet, indent=2))


if __name__ == '__main__':
    main()
