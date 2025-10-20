#!/usr/bin/env python3
"""
Find ADELAIDE-labeled streets that are in wrong suburbs
"""

import json
import os

def analyze_adelaide_labeled_streets():
    """Find streets labeled ADELAIDE that might be in wrong locations"""
    streets_file = "./public/data/streets.json"
    
    with open(streets_file, 'r') as f:
        streets = json.load(f)
    
    # Tight Adelaide CBD boundaries
    CBD_BOUNDS = {
        'north': -34.915,   # North Terrace area
        'south': -34.940,   # South Terrace area
        'east': 138.620,    # East Terrace area  
        'west': 138.580     # West Terrace area
    }
    
    adelaide_streets_outside_cbd = []
    
    for street in streets:
        street_name = street['street']
        lat = street['coordinates']['lat']
        lng = street['coordinates']['lng']
        total_fines = street['totalFines']
        
        # Only check streets labeled as "ADELAIDE" (not "NORTH ADELAIDE")
        if ", ADELAIDE" in street_name and "NORTH ADELAIDE" not in street_name:
            
            # Check if outside tight CBD bounds
            outside_cbd = not (CBD_BOUNDS['south'] <= lat <= CBD_BOUNDS['north'] and 
                             CBD_BOUNDS['west'] <= lng <= CBD_BOUNDS['east'])
            
            if outside_cbd:
                adelaide_streets_outside_cbd.append({
                    'street': street_name,
                    'lat': lat,
                    'lng': lng,
                    'fines': total_fines
                })
    
    # Sort by total fines (highest first)
    adelaide_streets_outside_cbd.sort(key=lambda x: x['fines'], reverse=True)
    
    print(f"🔍 Found {len(adelaide_streets_outside_cbd)} 'ADELAIDE' labeled streets outside tight CBD bounds:")
    print()
    
    high_value_count = 0
    for i, street in enumerate(adelaide_streets_outside_cbd):
        if street['fines'] > 50000:  # High value threshold
            high_value_count += 1
            status = "🚨 HIGH VALUE"
        elif street['fines'] > 10000:
            status = "⚠️  MEDIUM VALUE"
        else:
            status = "ℹ️  LOW VALUE"
            
        print(f"{i+1:2d}. {status} - {street['street']}")
        print(f"    Coordinates: ({street['lat']:.6f}, {street['lng']:.6f})")
        print(f"    Total fines: ${street['fines']:,.0f}")
        
        # Add helpful location context
        if street['lng'] > 138.620:
            print(f"    → Likely in: Eastern suburbs (Kent Town, Stepney area)")
        elif street['lng'] < 138.580:
            print(f"    → Likely in: Western suburbs")
        elif street['lat'] < -34.940:
            print(f"    → Likely in: Southern suburbs")
        elif street['lat'] > -34.915:
            print(f"    → Likely in: Northern suburbs")
        
        print()
        
        # Limit output for readability
        if i >= 19:  # Show top 20
            remaining = len(adelaide_streets_outside_cbd) - 20
            if remaining > 0:
                print(f"... and {remaining} more streets with lower fine amounts")
            break
    
    print(f"\n📊 Summary:")
    print(f"   🚨 High-value problematic streets (>$50k): {high_value_count}")
    print(f"   📍 Total 'ADELAIDE' streets outside CBD: {len(adelaide_streets_outside_cbd)}")
    
    return adelaide_streets_outside_cbd

if __name__ == "__main__":
    problematic_streets = analyze_adelaide_labeled_streets()