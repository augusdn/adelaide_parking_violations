#!/usr/bin/env python3
"""
Quick validation script to check geocoded coordinates
"""

import json
import os

def is_within_adelaide(lat: float, lng: float) -> bool:
    """Check if coordinates are within Adelaide boundaries"""
    ADELAIDE_BOUNDS = {
        'north': -34.900,
        'south': -34.960,
        'east': 138.630,
        'west': 138.570
    }
    
    return (ADELAIDE_BOUNDS['south'] <= lat <= ADELAIDE_BOUNDS['north'] and 
            ADELAIDE_BOUNDS['west'] <= lng <= ADELAIDE_BOUNDS['east'])

def check_coordinates():
    """Check current coordinates in the processed data"""
    streets_file = "./public/data/streets.json"
    
    if not os.path.exists(streets_file):
        print("❌ No streets.json found. Run data processing first.")
        return
    
    print("🔍 Checking current street coordinates...")
    
    with open(streets_file, 'r') as f:
        streets = json.load(f)
    
    invalid_streets = []
    valid_streets = []
    
    for street in streets:
        lat = street['coordinates']['lat']
        lng = street['coordinates']['lng']
        
        if is_within_adelaide(lat, lng):
            valid_streets.append(street)
        else:
            invalid_streets.append(street)
            print(f"🚨 {street['street']}: ({lat:.4f}, {lng:.4f}) - Outside Adelaide")
    
    print(f"\n📊 Summary:")
    print(f"   ✅ Valid streets (within Adelaide): {len(valid_streets)}")
    print(f"   ❌ Invalid streets (outside Adelaide): {len(invalid_streets)}")
    
    if invalid_streets:
        print(f"\n🔧 Top invalid streets by fine amount:")
        invalid_streets.sort(key=lambda x: x['totalFines'], reverse=True)
        for i, street in enumerate(invalid_streets[:10]):
            print(f"   {i+1}. {street['street']} - ${street['totalFines']:,.0f}")
    
    accuracy = len(valid_streets) / len(streets) * 100
    print(f"\n🎯 Geocoding accuracy: {accuracy:.1f}%")
    
    if accuracy < 95:
        print("⚠️  Recommendation: Re-run data processing with improved geocoding")
    else:
        print("✅ Geocoding accuracy is good!")

if __name__ == "__main__":
    check_coordinates()