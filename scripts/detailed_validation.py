#!/usr/bin/env python3
"""
Detailed validation script to identify specific geocoding issues
"""

import json
import os
import pandas as pd
import requests
import time
from typing import Dict, List, Tuple

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

def verify_street_location(street_name: str, lat: float, lng: float) -> Dict:
    """
    Verify if a street's coordinates actually correspond to the correct street
    using reverse geocoding
    """
    try:
        # Reverse geocode the coordinates
        url = f"https://nominatim.openstreetmap.org/reverse"
        params = {
            'lat': lat,
            'lon': lng,
            'format': 'json',
            'zoom': 18,
            'addressdetails': 1
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if 'address' in data:
            result_road = data.get('address', {}).get('road', '')
            result_suburb = data.get('address', {}).get('suburb', '')
            result_city = data.get('address', {}).get('city', '')
            
            # Extract street name from our input (remove ", ADELAIDE" etc.)
            input_street = street_name.split(',')[0].strip()
            
            # Check if the reverse geocoded road matches our street
            is_correct_street = (result_road.lower() in input_street.lower() or 
                               input_street.lower() in result_road.lower())
            
            is_in_adelaide = ('adelaide' in result_city.lower() or 
                            'adelaide' in result_suburb.lower() or
                            'north adelaide' in result_suburb.lower())
            
            return {
                'is_correct_street': is_correct_street,
                'is_in_adelaide': is_in_adelaide,
                'reverse_geocoded_road': result_road,
                'reverse_geocoded_suburb': result_suburb,
                'reverse_geocoded_city': result_city,
                'full_address': data.get('display_name', '')
            }
        
        time.sleep(1)  # Rate limiting
        return {
            'is_correct_street': False,
            'is_in_adelaide': False,
            'error': 'No address details in response'
        }
        
    except Exception as e:
        return {
            'is_correct_street': False,
            'is_in_adelaide': False,
            'error': str(e)
        }

def find_major_streets_with_issues(streets_data: List[Dict]) -> List[Dict]:
    """Find streets with high fine amounts that might have incorrect coordinates"""
    
    # Sort by total fines to focus on high-value streets
    sorted_streets = sorted(streets_data, key=lambda x: x['totalFines'], reverse=True)
    
    problematic_streets = []
    
    print("🔍 Checking top 20 highest-value streets for location accuracy...")
    
    for i, street in enumerate(sorted_streets[:20]):
        street_name = street['street']
        lat = street['coordinates']['lat']
        lng = street['coordinates']['lng']
        total_fines = street['totalFines']
        
        print(f"   Checking {i+1}/20: {street_name} (${total_fines:,.0f})")
        
        # Verify location
        verification = verify_street_location(street_name, lat, lng)
        
        if not verification.get('is_correct_street', False):
            problematic_streets.append({
                'street': street_name,
                'coordinates': {'lat': lat, 'lng': lng},
                'total_fines': total_fines,
                'verification': verification
            })
            print(f"      ⚠️  Potential issue: {verification}")
    
    return problematic_streets

def check_duplicate_coordinates(streets_data: List[Dict]) -> List[Tuple]:
    """Find streets that share the same coordinates (suspicious)"""
    coord_map = {}
    
    for street in streets_data:
        lat = round(street['coordinates']['lat'], 6)
        lng = round(street['coordinates']['lng'], 6)
        coord_key = (lat, lng)
        
        if coord_key not in coord_map:
            coord_map[coord_key] = []
        coord_map[coord_key].append(street['street'])
    
    # Find coordinates used by multiple streets
    duplicates = [(coords, streets) for coords, streets in coord_map.items() if len(streets) > 1]
    
    return duplicates

def check_default_coordinates(streets_data: List[Dict]) -> List[Dict]:
    """Find streets using default coordinates (CBD center)"""
    # Default coordinates used when geocoding fails
    DEFAULT_LAT = -34.9285
    DEFAULT_LNG = 138.6007
    
    default_streets = []
    
    for street in streets_data:
        lat = street['coordinates']['lat']
        lng = street['coordinates']['lng']
        
        # Check if coordinates are very close to default (within 0.001 degrees)
        if (abs(lat - DEFAULT_LAT) < 0.001 and abs(lng - DEFAULT_LNG) < 0.001):
            default_streets.append(street)
    
    return default_streets

def detailed_validation():
    """Run comprehensive validation on street data"""
    streets_file = "./public/data/streets.json"
    
    if not os.path.exists(streets_file):
        print("❌ No streets.json found. Run data processing first.")
        return
    
    print("🔍 Running detailed validation on street coordinates...")
    
    with open(streets_file, 'r') as f:
        streets = json.load(f)
    
    print(f"📊 Analyzing {len(streets)} streets...")
    
    # 1. Basic coordinate validation
    invalid_streets = []
    for street in streets:
        lat = street['coordinates']['lat']
        lng = street['coordinates']['lng']
        
        if not is_within_adelaide(lat, lng):
            invalid_streets.append(street)
    
    print(f"\n1️⃣ Basic Coordinate Validation:")
    print(f"   ✅ Valid streets (within Adelaide): {len(streets) - len(invalid_streets)}")
    print(f"   ❌ Invalid streets (outside Adelaide): {len(invalid_streets)}")
    
    # 2. Check for duplicate coordinates
    print(f"\n2️⃣ Duplicate Coordinate Check:")
    duplicates = check_duplicate_coordinates(streets)
    if duplicates:
        print(f"   ⚠️  Found {len(duplicates)} coordinate sets used by multiple streets:")
        for coords, street_list in duplicates[:5]:  # Show first 5
            print(f"      {coords}: {', '.join(street_list[:3])}" + 
                  (f" and {len(street_list)-3} more" if len(street_list) > 3 else ""))
    else:
        print("   ✅ No duplicate coordinates found")
    
    # 3. Check for default coordinates
    print(f"\n3️⃣ Default Coordinate Check:")
    default_streets = check_default_coordinates(streets)
    if default_streets:
        print(f"   ⚠️  Found {len(default_streets)} streets using default coordinates:")
        for street in default_streets[:10]:  # Show first 10
            print(f"      {street['street']} (${street['totalFines']:,.0f})")
    else:
        print("   ✅ No streets using default coordinates")
    
    # 4. Verify major streets (this will take time due to API calls)
    print(f"\n4️⃣ Major Street Verification (this may take a minute):")
    try:
        problematic_streets = find_major_streets_with_issues(streets)
        if problematic_streets:
            print(f"   ⚠️  Found {len(problematic_streets)} potentially problematic high-value streets:")
            for street in problematic_streets:
                print(f"      {street['street']} (${street['total_fines']:,.0f})")
                print(f"         Reverse geocoded: {street['verification'].get('full_address', 'N/A')}")
        else:
            print("   ✅ All major streets appear to be correctly located")
    except Exception as e:
        print(f"   ⚠️  Could not verify major streets: {e}")
    
    # Summary
    print(f"\n📋 Summary:")
    total_issues = len(invalid_streets) + len(duplicates) + len(default_streets)
    if total_issues == 0:
        print("   ✅ No major issues detected with street coordinates")
    else:
        print(f"   ⚠️  Detected {total_issues} potential issues that may need attention")
        
        if invalid_streets:
            print(f"      - {len(invalid_streets)} streets outside Adelaide boundaries")
        if duplicates:
            print(f"      - {len(duplicates)} sets of duplicate coordinates")
        if default_streets:
            print(f"      - {len(default_streets)} streets using default coordinates")

if __name__ == "__main__":
    detailed_validation()