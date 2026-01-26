#!/usr/bin/env python3
"""
Build datasheet caches for all 40k factions.

Usage:
    python build-all-caches.py              # Build all factions sequentially
    python build-all-caches.py --parallel 4 # Build 4 factions at a time
    python build-all-caches.py --only chaos # Build only chaos factions
    python build-all-caches.py --skip-cached # Skip factions that already have caches
"""

import os
import sys
import time
import argparse
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRAPER = os.path.join(SCRIPT_DIR, 'scrape-wahapedia.py')
DATA_DIR = os.path.join(SCRIPT_DIR, '..', 'data', 'datasheets')

# All factions by category
FACTIONS = {
    'imperium': [
        'adepta-sororitas',
        'adeptus-custodes',
        'adeptus-mechanicus',
        'astra-militarum',
        'grey-knights',
        'imperial-agents',
        'imperial-knights',
        'space-marines',
        'space-wolves',
    ],
    'chaos': [
        'chaos-daemons',
        'chaos-knights',
        'chaos-space-marines',
        'death-guard',
        'emperors-children',
        'thousand-sons',
        'world-eaters',
    ],
    'xenos': [
        'aeldari',
        'drukhari',
        'genestealer-cults',
        'leagues-of-votann',
        'necrons',
        'orks',
        'tau-empire',
        'tyranids',
    ],
}


def is_cached(faction: str) -> bool:
    """Check if faction already has a cache."""
    cache_file = os.path.join(DATA_DIR, f'{faction}.json')
    return os.path.exists(cache_file)


def build_faction(faction: str, verbose: bool = True) -> tuple[str, bool, str]:
    """Build cache for a single faction. Returns (faction, success, message)."""
    try:
        result = subprocess.run(
            ['python3', SCRAPER, '--discover', faction],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout per faction
        )

        if result.returncode == 0:
            # Extract unit count from output
            lines = result.stdout.strip().split('\n')
            for line in lines[-5:]:
                if 'Completed' in line or 'units' in line:
                    return (faction, True, line.strip())
            return (faction, True, 'Cache built successfully')
        else:
            return (faction, False, result.stderr[:200] if result.stderr else 'Unknown error')

    except subprocess.TimeoutExpired:
        return (faction, False, 'Timeout after 5 minutes')
    except Exception as e:
        return (faction, False, str(e))


def main():
    parser = argparse.ArgumentParser(description='Build caches for all 40k factions')
    parser.add_argument('--parallel', type=int, default=1,
                        help='Number of parallel builds (default: 1)')
    parser.add_argument('--only', choices=['imperium', 'chaos', 'xenos'],
                        help='Only build factions from this category')
    parser.add_argument('--skip-cached', action='store_true',
                        help='Skip factions that already have caches')
    parser.add_argument('--faction', type=str,
                        help='Build only this specific faction')
    args = parser.parse_args()

    # Determine which factions to build
    if args.faction:
        factions = [args.faction]
    elif args.only:
        factions = FACTIONS[args.only]
    else:
        factions = FACTIONS['imperium'] + FACTIONS['chaos'] + FACTIONS['xenos']

    # Filter out cached factions if requested
    if args.skip_cached:
        original_count = len(factions)
        factions = [f for f in factions if not is_cached(f)]
        skipped = original_count - len(factions)
        if skipped > 0:
            print(f"Skipping {skipped} cached factions")

    if not factions:
        print("No factions to build!")
        return

    print("=" * 50)
    print("  WAHAPEDIA DATASHEET CACHE BUILDER")
    print("=" * 50)
    print(f"\nFactions to build: {len(factions)}")
    print(f"Parallel jobs: {args.parallel}")
    print()

    start_time = time.time()
    success = []
    failed = []

    if args.parallel > 1:
        # Parallel execution
        with ThreadPoolExecutor(max_workers=args.parallel) as executor:
            futures = {executor.submit(build_faction, f): f for f in factions}

            for i, future in enumerate(as_completed(futures), 1):
                faction, ok, msg = future.result()
                status = '✓' if ok else '✗'
                color = '\033[92m' if ok else '\033[91m'
                reset = '\033[0m'
                print(f"[{i}/{len(factions)}] {color}{status}{reset} {faction}: {msg}")

                if ok:
                    success.append(faction)
                else:
                    failed.append(faction)

                # Small delay between completions
                time.sleep(0.5)
    else:
        # Sequential execution
        for i, faction in enumerate(factions, 1):
            print(f"\n[{i}/{len(factions)}] Building {faction}...")
            print("-" * 40)

            faction, ok, msg = build_faction(faction)

            if ok:
                print(f"\033[92m✓ {faction}: {msg}\033[0m")
                success.append(faction)
            else:
                print(f"\033[91m✗ {faction}: {msg}\033[0m")
                failed.append(faction)

            # Be nice to Wahapedia
            if i < len(factions):
                time.sleep(2)

    elapsed = time.time() - start_time

    print()
    print("=" * 50)
    print("  BUILD COMPLETE")
    print("=" * 50)
    print(f"\nDuration: {elapsed:.0f}s ({elapsed/60:.1f} minutes)")
    print(f"\033[92mSuccess: {len(success)}\033[0m")
    print(f"\033[91mFailed: {len(failed)}\033[0m")

    if failed:
        print("\nFailed factions:")
        for f in failed:
            print(f"  - {f}")

    print(f"\nRun 'python3 {SCRAPER} --list-factions' to see cache status.")


if __name__ == '__main__':
    main()
