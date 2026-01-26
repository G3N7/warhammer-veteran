#!/bin/bash
# Build datasheet caches for all 40k factions
# Usage: ./build-all-caches.sh [--parallel N]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRAPER="$SCRIPT_DIR/scrape-wahapedia.py"

# All factions
IMPERIUM=(
    "adepta-sororitas"
    "adeptus-custodes"
    "adeptus-mechanicus"
    "astra-militarum"
    "grey-knights"
    "imperial-agents"
    "imperial-knights"
    "space-marines"
    "space-wolves"
)

CHAOS=(
    "chaos-daemons"
    "chaos-knights"
    "chaos-space-marines"
    "death-guard"
    "emperors-children"
    "thousand-sons"
    "world-eaters"
)

XENOS=(
    "aeldari"
    "drukhari"
    "genestealer-cults"
    "leagues-of-votann"
    "necrons"
    "orks"
    "tau-empire"
    "tyranids"
)

ALL_FACTIONS=("${IMPERIUM[@]}" "${CHAOS[@]}" "${XENOS[@]}")

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Wahapedia Datasheet Cache Builder${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Total factions: ${#ALL_FACTIONS[@]}"
echo ""

# Track results
SUCCESS=()
FAILED=()

build_faction() {
    local faction=$1
    echo -e "${YELLOW}[$faction]${NC} Building cache..."

    if python3 "$SCRAPER" --discover "$faction" 2>&1 | tail -5; then
        echo -e "${GREEN}[$faction]${NC} ✓ Complete"
        return 0
    else
        echo -e "${RED}[$faction]${NC} ✗ Failed"
        return 1
    fi
}

# Parse args
PARALLEL=1
if [[ "$1" == "--parallel" ]] && [[ -n "$2" ]]; then
    PARALLEL=$2
    echo "Running with $PARALLEL parallel jobs"
fi

# Build each faction
START_TIME=$(date +%s)

if [[ $PARALLEL -gt 1 ]]; then
    # Parallel mode using xargs
    printf '%s\n' "${ALL_FACTIONS[@]}" | xargs -P "$PARALLEL" -I {} bash -c "
        echo \"Building {}...\"
        python3 \"$SCRAPER\" --discover {} > /tmp/cache_{}.log 2>&1
        if [ \$? -eq 0 ]; then
            echo -e \"${GREEN}[{}]${NC} ✓ Complete\"
        else
            echo -e \"${RED}[{}]${NC} ✗ Failed - check /tmp/cache_{}.log\"
        fi
    "
else
    # Sequential mode with progress
    TOTAL=${#ALL_FACTIONS[@]}
    COUNT=0

    for faction in "${ALL_FACTIONS[@]}"; do
        COUNT=$((COUNT + 1))
        echo ""
        echo -e "${BLUE}[$COUNT/$TOTAL]${NC} Processing $faction..."
        echo "----------------------------------------"

        if python3 "$SCRAPER" --discover "$faction"; then
            SUCCESS+=("$faction")
        else
            FAILED+=("$faction")
        fi

        # Brief pause between factions to be nice to Wahapedia
        sleep 2
    done
fi

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  BUILD COMPLETE${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Duration: ${DURATION}s"
echo -e "${GREEN}Success: ${#SUCCESS[@]}${NC}"
echo -e "${RED}Failed: ${#FAILED[@]}${NC}"

if [[ ${#FAILED[@]} -gt 0 ]]; then
    echo ""
    echo "Failed factions:"
    for f in "${FAILED[@]}"; do
        echo "  - $f"
    done
fi

echo ""
echo "Run 'python3 $SCRAPER --list-factions' to see cache status."
