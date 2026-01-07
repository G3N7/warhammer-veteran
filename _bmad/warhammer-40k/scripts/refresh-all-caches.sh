#!/bin/bash
# Refresh ALL faction caches using auto-discovery
# This replaces the hardcoded unit lists with complete faction data from Wahapedia

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRAPER="$SCRIPT_DIR/scrape-wahapedia.py"

# User's factions (from memories.md)
FACTIONS=(
    "astra-militarum"
    "space-marines"
    "space-wolves"
    "orks"
    "tyranids"
    "tau-empire"
)

echo "================================================"
echo "  WAHAPEDIA CACHE REFRESH - ALL FACTIONS"
echo "================================================"
echo ""
echo "This will discover and cache ALL units for ${#FACTIONS[@]} factions."
echo "Estimated time: 5-10 minutes (rate-limited to be nice to Wahapedia)"
echo ""

for faction in "${FACTIONS[@]}"; do
    echo ""
    echo "========================================"
    echo "  Processing: $faction"
    echo "========================================"
    python3 "$SCRAPER" --discover "$faction"
    
    # Small delay between factions
    sleep 2
done

echo ""
echo "================================================"
echo "  COMPLETE!"
echo "================================================"
echo ""
python3 "$SCRAPER" --status
