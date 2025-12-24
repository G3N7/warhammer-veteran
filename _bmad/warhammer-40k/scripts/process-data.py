#!/usr/bin/env python3
"""
Process Wahapedia CSV exports into agent-optimized JSON files.
Trims lore for context efficiency while preserving structure for Lorekeeper.
"""

import csv
import json
import os
from pathlib import Path
from collections import defaultdict

# Paths
DATA_DIR = Path("_bmad/warhammer-40k/data/wahapedia-10ed")
PROCESSED_DIR = Path("_bmad/warhammer-40k/data/processed")


def read_csv(filename):
    """Read CSV file with pipe delimiter."""
    filepath = DATA_DIR / filename
    if not filepath.exists():
        print(f"⚠️  Warning: {filename} not found, skipping...")
        return []

    with open(filepath, 'r', encoding='utf-8-sig') as f:  # utf-8-sig handles BOM
        # Wahapedia uses pipe delimiter
        reader = csv.DictReader(f, delimiter='|')
        return list(reader)


def parse_factions():
    """Build faction index with detachment list."""
    print("📋 Processing Factions...")
    factions_data = read_csv("Factions.csv")

    factions_index = {}
    for faction in factions_data:
        faction_id = faction.get('id', '').strip()
        faction_name = faction.get('name', '').strip()

        if faction_id and faction_name:
            factions_index[faction_id] = {
                "id": faction_id,
                "name": faction_name,
                "link": faction.get('link', '').strip()
            }

    # Save factions index
    output_file = PROCESSED_DIR / "factions-index.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(factions_index, f, indent=2)

    print(f"✅ Factions index created: {len(factions_index)} factions")
    return factions_index


def parse_core_abilities():
    """Extract core game abilities (trimmed, no lore)."""
    print("📋 Processing Core Abilities...")
    abilities_data = read_csv("Abilities.csv")

    core_abilities = []
    for ability in abilities_data:
        # Skip faction-specific abilities (they go in faction files)
        if ability.get('faction_id', '').strip():
            continue

        core_abilities.append({
            "id": ability.get('id', '').strip(),
            "name": ability.get('name', '').strip(),
            "type": ability.get('type', '').strip(),
            "description": ability.get('description', '').strip(),
            # Trim legend (lore) for context efficiency
        })

    print(f"✅ Core abilities: {len(core_abilities)}")
    return core_abilities


def parse_core_rules():
    """Extract core game rules (trimmed for non-Lorekeeper agents)."""
    print("📋 Creating core-rules.json...")

    # Get core abilities (non-faction-specific)
    core_abilities = parse_core_abilities()

    core_rules = {
        "version": "10th Edition",
        "source": "wahapedia.ru",
        "abilities": core_abilities,
        "note": "Lore/legend fields trimmed for context efficiency. See raw CSVs for full text."
    }

    output_file = PROCESSED_DIR / "core-rules.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(core_rules, f, indent=2)

    print(f"✅ Core rules saved")


def parse_faction_datasheets(faction_id, factions_index):
    """Extract all datasheets for a faction."""
    datasheets_data = read_csv("Datasheets.csv")
    datasheets_models = read_csv("Datasheets_models.csv")
    datasheets_wargear = read_csv("Datasheets_wargear.csv")
    wargear_list = read_csv("Wargear_list.csv")

    # Build wargear lookup
    wargear_lookup = {w.get('id'): w for w in wargear_list}

    # Group models by datasheet
    models_by_datasheet = defaultdict(list)
    for model in datasheets_models:
        ds_id = model.get('datasheet_id', '').strip()
        if ds_id:
            models_by_datasheet[ds_id].append(model)

    # Group wargear by datasheet
    wargear_by_datasheet = defaultdict(list)
    for wg in datasheets_wargear:
        ds_id = wg.get('datasheet_id', '').strip()
        wg_id = wg.get('wargear_id', '').strip()
        if ds_id and wg_id in wargear_lookup:
            wg_details = wargear_lookup[wg_id].copy()
            wg_details['cost'] = wg.get('cost', '0').strip()
            wg_details['is_index_wargear'] = wg.get('is_index_wargear', '').strip()
            wargear_by_datasheet[ds_id].append(wg_details)

    faction_datasheets = []
    for datasheet in datasheets_data:
        ds_faction_id = datasheet.get('faction_id', '').strip()

        if ds_faction_id == faction_id:
            ds_id = datasheet.get('id', '').strip()

            faction_datasheets.append({
                "id": ds_id,
                "name": datasheet.get('name', '').strip(),
                "role": datasheet.get('role', '').strip(),
                "loadout": datasheet.get('loadout', '').strip(),
                "transport": datasheet.get('transport', '').strip(),
                "points": datasheet.get('points', '0').strip(),
                "models": models_by_datasheet.get(ds_id, []),
                "wargear": wargear_by_datasheet.get(ds_id, []),
                # Trim legend (lore) for context efficiency
            })

    return faction_datasheets


def parse_faction_abilities(faction_id):
    """Extract faction-specific abilities."""
    abilities_data = read_csv("Abilities.csv")

    faction_abilities = []
    for ability in abilities_data:
        if ability.get('faction_id', '').strip() == faction_id:
            faction_abilities.append({
                "id": ability.get('id', '').strip(),
                "name": ability.get('name', '').strip(),
                "type": ability.get('type', '').strip(),
                "description": ability.get('description', '').strip(),
                # Trim legend for context efficiency
            })

    return faction_abilities


def parse_faction_stratagems(faction_id):
    """Extract faction stratagems grouped by detachment."""
    stratagems_data = read_csv("Stratagems.csv")

    faction_stratagems = []
    for stratagem in stratagems_data:
        if stratagem.get('faction_id', '').strip() == faction_id:
            faction_stratagems.append({
                "id": stratagem.get('id', '').strip(),
                "name": stratagem.get('name', '').strip(),
                "type": stratagem.get('type', '').strip(),
                "cp_cost": stratagem.get('cp_cost', '0').strip(),
                "description": stratagem.get('description', '').strip(),
                "detachment": stratagem.get('detachment', '').strip(),
                # Trim legend for context efficiency
            })

    return faction_stratagems


def process_faction(faction_id, faction_name):
    """Process all data for a single faction."""
    print(f"📋 Processing {faction_name}...")

    # Create faction directory
    faction_dir = PROCESSED_DIR / faction_id
    faction_dir.mkdir(parents=True, exist_ok=True)

    # Parse faction-specific data
    abilities = parse_faction_abilities(faction_id)
    datasheets = parse_faction_datasheets(faction_id, {})
    stratagems = parse_faction_stratagems(faction_id)

    # Save rules.json (abilities, no datasheets/lore)
    rules = {
        "faction_id": faction_id,
        "faction_name": faction_name,
        "abilities": abilities,
        "note": "Datasheets in separate file. Lore trimmed for context efficiency."
    }

    with open(faction_dir / "rules.json", 'w', encoding='utf-8') as f:
        json.dump(rules, f, indent=2)

    # Save datasheets.json
    with open(faction_dir / "datasheets.json", 'w', encoding='utf-8') as f:
        json.dump({"datasheets": datasheets}, f, indent=2)

    # Save stratagems.json
    with open(faction_dir / "stratagems.json", 'w', encoding='utf-8') as f:
        json.dump({"stratagems": stratagems}, f, indent=2)

    print(f"  ✅ {len(abilities)} abilities, {len(datasheets)} datasheets, {len(stratagems)} stratagems")


def main():
    """Main processing pipeline."""
    print("⚔️  Wahapedia CSV → JSON Processing")
    print("=" * 50)

    # Create processed directory
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Step 1: Parse factions index
    factions_index = parse_factions()

    # Step 2: Create core rules (abilities without faction_id)
    parse_core_rules()

    # Step 3: Process each faction
    for faction_id, faction_info in factions_index.items():
        process_faction(faction_id, faction_info['name'])

    print("=" * 50)
    print("✅ Processing complete!")
    print(f"📁 Output directory: {PROCESSED_DIR}")


if __name__ == "__main__":
    main()
