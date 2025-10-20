#!/usr/bin/env python3
"""
Clear cache for problematic ADELAIDE streets that are in wrong suburbs
"""

import json
import os

def clear_problematic_streets_cache():
    """Clear cache for streets that are in wrong suburbs"""
    cache_file = "./scripts/cache/geocode_cache.json"
    
    if not os.path.exists(cache_file):
        print("No cache file found")
        return
    
    # List of problematic streets to clear from cache
    problematic_streets = [
        "Flinders Street, ADELAIDE",
        "Angas Street, ADELAIDE", 
        "Grenfell Street, ADELAIDE",
        "Union Street, ADELAIDE",
        "Beaumont Road, ADELAIDE",
        "Flinders Street E, ADELAIDE",
        "Victoria Street, ADELAIDE",
        "Unley Road, ADELAIDE",
        "Queen Street, ADELAIDE",
        "Eliza Street, ADELAIDE",
        "Frew Street, ADELAIDE",
        "North Street, ADELAIDE",
        "Charles Street, ADELAIDE",
        "Thomas Street, ADELAIDE",
        "Glen Osmond Road, ADELAIDE",
        "John Street, ADELAIDE",
        "Fisher Place, ADELAIDE",
        "King William Road, ADELAIDE"
    ]
    
    with open(cache_file, 'r') as f:
        cache = json.load(f)
    
    cleared_count = 0
    
    print("🧹 Clearing cache for problematic streets:")
    
    # Check all cache keys and remove those matching problematic streets
    keys_to_remove = []
    for cache_key in cache.keys():
        for problematic_street in problematic_streets:
            if problematic_street in cache_key:
                keys_to_remove.append(cache_key)
                print(f"  - {cache_key}")
                cleared_count += 1
                break
    
    # Remove the keys
    for key in keys_to_remove:
        del cache[key]
    
    # Save updated cache
    with open(cache_file, 'w') as f:
        json.dump(cache, f, indent=2)
    
    print(f"✅ Cleared {cleared_count} problematic street cache entries")

if __name__ == "__main__":
    clear_problematic_streets_cache()