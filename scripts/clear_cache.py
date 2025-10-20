#!/usr/bin/env python3
"""
Clear geocoding cache for problematic streets that are using default coordinates
"""

import json
import os

def clear_default_coordinates():
    """Clear cache entries that resulted in default coordinates"""
    cache_file = "./scripts/cache/geocode_cache.json"
    
    if not os.path.exists(cache_file):
        print("No cache file found")
        return
    
    with open(cache_file, 'r') as f:
        cache = json.load(f)
    
    # Default coordinates used when geocoding fails
    DEFAULT_LAT = -34.9285
    DEFAULT_LNG = 138.6007
    
    streets_to_clear = []
    
    for street_key, coords in cache.items():
        lat = coords['lat']
        lng = coords['lng']
        
        # Check if coordinates are exactly default (within very small tolerance)
        if (abs(lat - DEFAULT_LAT) < 0.0001 and abs(lng - DEFAULT_LNG) < 0.0001):
            streets_to_clear.append(street_key)
    
    if streets_to_clear:
        print(f"Clearing {len(streets_to_clear)} cache entries with default coordinates:")
        for street in streets_to_clear:
            print(f"  - {street}")
            del cache[street]
        
        # Save updated cache
        with open(cache_file, 'w') as f:
            json.dump(cache, f, indent=2)
        
        print(f"✅ Cleared {len(streets_to_clear)} cache entries")
    else:
        print("No cache entries with default coordinates found")

if __name__ == "__main__":
    clear_default_coordinates()