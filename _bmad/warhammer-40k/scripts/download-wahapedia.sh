#!/bin/bash
# Download Wahapedia 10th Edition CSV exports

BASE_URL="http://wahapedia.ru/wh40k10ed"
DATA_DIR="_bmad/warhammer-40k/data/wahapedia-10ed"

# Create directory
mkdir -p "$DATA_DIR"

# Download CSVs
echo "Downloading Wahapedia CSV exports..."
curl -s "$BASE_URL/Datasheets.csv" > "$DATA_DIR/Datasheets.csv"
curl -s "$BASE_URL/Factions.csv" > "$DATA_DIR/Factions.csv"
curl -s "$BASE_URL/Abilities.csv" > "$DATA_DIR/Abilities.csv"
curl -s "$BASE_URL/Stratagems.csv" > "$DATA_DIR/Stratagems.csv"
curl -s "$BASE_URL/Datasheets_models.csv" > "$DATA_DIR/Datasheets_models.csv"
curl -s "$BASE_URL/Datasheets_wargear.csv" > "$DATA_DIR/Datasheets_wargear.csv"
curl -s "$BASE_URL/Wargear_list.csv" > "$DATA_DIR/Wargear_list.csv"

# Create timestamp
date +%s > "$DATA_DIR/last_update.csv"

echo "✅ Download complete: $(date)"
