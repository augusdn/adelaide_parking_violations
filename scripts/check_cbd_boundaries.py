#!/usr/bin/env python3
"""
Enhanced validation to find streets geocoded to wrong Adelaide suburbs
"""

import json
import os
import requests
import time
from typing import Dict, List

def is_within_adelaide_cbd(lat: float, lng: float) -> bool:
    """Check if coordinates are within Adelaide CBD boundaries (stricter)"""
    # Tighter boundaries for Adelaide CBD specifically
    CBD_BOUNDS = {
        'north': -34.910,   # Tighter north boundary
        'south': -34.950,   # Tighter south boundary  
        'east': 138.625,    # Tighter east boundary
        'west': 138.575     # Tighter west boundary
    }
    
    return (CBD_BOUNDS['south'] <= lat <= CBD_BOUNDS['north'] and 
            CBD_BOUNDS['west'] <= lng <= CBD_BOUNDS['east'])

def is_within_adelaide_metro(lat: float, lng: float) -> bool:
    """Check if coordinates are within broader Adelaide metro area"""
    METRO_BOUNDS = {
        'north': -34.900,
        'south': -34.960,
        'east': 138.630,
        'west': 138.570
    }
    
    return (METRO_BOUNDS['south'] <= lat <= METRO_BOUNDS['north'] and 
            METRO_BOUNDS['west'] <= lng <= METRO_BOUNDS['east'])

def check_street_location_with_reverse_geocoding(street_name: str, lat: float, lng: float) -> Dict:
    """
    Check if street coordinates are in the right location using reverse geocoding
    """
    try:
        url = f"https://nominatim.openstreetmap.org/reverse"
        params = {
            'lat': lat,
            'lon': lng,
            'format': 'json',
            'zoom': 16,
            'addressdetails': 1
        }
        
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 403:
            return {'error': 'Rate limited'}
        
        response.raise_for_status()
        data = response.json()
        
        if 'address' in data:
            result_road = data.get('address', {}).get('road', '')
            result_suburb = data.get('address', {}).get('suburb', '')
            result_city_district = data.get('address', {}).get('city_district', '')
            result_city = data.get('address', {}).get('city', '')
            
            # Extract street name from our input
            input_street = street_name.split(',')[0].strip()
            
            # Check if it's in CBD vs other suburbs
            is_cbd = any(keyword in result_suburb.lower() for keyword in ['adelaide', 'city']) or \
                     'adelaide' in result_city_district.lower() or \
                     result_suburb == ''  # Sometimes CBD has no suburb
            
            return {
                'road': result_road,
                'suburb': result_suburb,
                'city_district': result_city_district,
                'city': result_city,
                'is_cbd': is_cbd,
                'full_address': data.get('display_name', ''),
                'input_street': input_street
            }
        
        time.sleep(1)
        return {'error': 'No address details'}
        
    except Exception as e:
        return {'error': str(e)}

def find_streets_outside_cbd():
    """Find streets that are outside Adelaide CBD"""
    streets_file = "./public/data/streets.json"
    
    if not os.path.exists(streets_file):
        print("❌ No streets.json found.")
        return
    
    print("🔍 Finding streets outside Adelaide CBD...")
    
    with open(streets_file, 'r') as f:
        streets = json.load(f)
    
    outside_cbd = []
    high_value_outside = []
    
    for street in streets:
        lat = street['coordinates']['lat']
        lng = street['coordinates']['lng']
        street_name = street['street']
        total_fines = street['totalFines']
        
        # Check if within metro but outside CBD
        if is_within_adelaide_metro(lat, lng) and not is_within_adelaide_cbd(lat, lng):
            outside_cbd.append({
                'street': street_name,
                'lat': lat,
                'lng': lng,
                'fines': total_fines
            })
            
            # Flag high-value streets (>$10k in fines)
            if total_fines > 10000:
                high_value_outside.append({
                    'street': street_name,
                    'lat': lat,
                    'lng': lng,
                    'fines': total_fines
                })
    
    print(f"\n📊 Streets outside Adelaide CBD but within metro area: {len(outside_cbd)}")
    
    if high_value_outside:
        print(f"\n⚠️  High-value streets outside CBD (>${10000:,}+ fines):")
        
        # Sort by fine amount
        high_value_outside.sort(key=lambda x: x['fines'], reverse=True)
        
        for i, street in enumerate(high_value_outside[:10]):  # Show top 10
            print(f"   {i+1}. {street['street']}")
            print(f"      Coordinates: ({street['lat']:.6f}, {street['lng']:.6f})")
            print(f"      Total fines: ${street['fines']:,.0f}")
            
            # Try reverse geocoding for a few high-value ones
            if i < 5:  # Only for top 5 to avoid rate limiting
                print("      Checking location...", end="")
                location_info = check_street_location_with_reverse_geocoding(
                    street['street'], street['lat'], street['lng']
                )
                if 'error' not in location_info:
                    suburb = location_info.get('suburb', 'Unknown')
                    print(f" → Located in: {suburb}")
                else:
                    print(f" → {location_info['error']}")
                
                time.sleep(2)  # Rate limiting
            else:
                print()
    
    return outside_cbd, high_value_outside

def check_specific_streets():
    """Check specific problematic streets mentioned by user"""
    specific_streets = [
        "Union Street, ADELAIDE"
    ]
    
    streets_file = "./public/data/streets.json"
    
    with open(streets_file, 'r') as f:
        streets = json.load(f)
    
    print(f"\n🔍 Checking specific problematic streets:")
    
    for target_street in specific_streets:
        for street in streets:
            if street['street'] == target_street:
                lat = street['coordinates']['lat']
                lng = street['coordinates']['lng']
                total_fines = street['totalFines']
                
                print(f"\n📍 {target_street}")
                print(f"   Coordinates: ({lat:.6f}, {lng:.6f})")
                print(f"   Total fines: ${total_fines:,.0f}")
                print(f"   In CBD: {is_within_adelaide_cbd(lat, lng)}")
                print(f"   In Metro: {is_within_adelaide_metro(lat, lng)}")
                
                # Check actual location
                print("   Checking actual location...", end="")
                location_info = check_street_location_with_reverse_geocoding(
                    target_street, lat, lng
                )
                if 'error' not in location_info:
                    suburb = location_info.get('suburb', 'Unknown')
                    full_addr = location_info.get('full_address', '')
                    print(f" → {suburb}")
                    print(f"   Full address: {full_addr}")
                else:
                    print(f" → {location_info['error']}")
                
                break

if __name__ == "__main__":
    check_specific_streets()
    outside_cbd, high_value_outside = find_streets_outside_cbd()
    
    if outside_cbd:
        print(f"\n💡 Suggestion: Consider tightening geocoding to focus specifically on Adelaide CBD")
        print(f"   Current boundary: lat(-34.900 to -34.960), lng(138.570 to 138.630)")
        print(f"   Suggested CBD boundary: lat(-34.910 to -34.950), lng(138.575 to 138.625)")