#!/usr/bin/env python3
"""
Data processing script for Adelaide Parking Violations
Converts raw CSV data into optimized JSON files for static web app
"""

import pandas as pd
import json
import os
from datetime import datetime
import requests
import time
from typing import Dict, List, Any

# Configuration
CSV_PATH = "./data/Parking_Expiations.csv"
OUTPUT_DIR = "./public/data"
CACHE_DIR = "./scripts/cache"

def ensure_directories():
    """Create necessary directories"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(CACHE_DIR, exist_ok=True)

def clean_street_name(street: str) -> str:
    """Clean and standardize street names"""
    if pd.isna(street):
        return "Unknown"
    
    # Remove quotes and extra spaces
    street = str(street).strip().strip('"')
    
    # Handle common formatting issues
    if street.startswith('.'):
        street = street[1:]
    
    return street.strip()

def is_within_adelaide(lat: float, lng: float) -> bool:
    """Check if coordinates are within Adelaide CBD boundaries (strict)"""
    # Stricter boundaries focused on Adelaide CBD proper
    ADELAIDE_CBD_BOUNDS = {
        'north': -34.915,   # North Terrace area
        'south': -34.940,   # South Terrace area  
        'east': 138.620,    # East Terrace area
        'west': 138.580     # West Terrace area
    }
    
    return (ADELAIDE_CBD_BOUNDS['south'] <= lat <= ADELAIDE_CBD_BOUNDS['north'] and 
            ADELAIDE_CBD_BOUNDS['west'] <= lng <= ADELAIDE_CBD_BOUNDS['east'])

def clean_street_for_geocoding(street: str) -> str:
    """Clean street name for better geocoding results"""
    # Remove common suffixes that confuse geocoding
    street = street.replace(' C/Pk', '').replace(' Car Park', '')
    
    # Handle specific parking areas
    parking_mappings = {
        'Hindley St C/Pk': 'Hindley Street',
        'Bonython Park C/Pk': 'Bonython Park',
        'Light Sq C/Pk': 'Light Square',
        'Pulteney St Karidis C/Pk': 'Pulteney Street',
        'Pulteney St 281-301 C/Pk': 'Pulteney Street',
        'Pulteney St 182 C/Pk': 'Pulteney Street',
        'Park Lands': 'Adelaide Park Lands',
        'War Memorial Dr Par3 C/Pk': 'War Memorial Drive',
        'War Memorial Dr Sth C/Pk': 'War Memorial Drive',
        'Dunn St C/Pk': 'Dunn Street',
        'Victoria Square': 'Victoria Square, Adelaide',
    }
    
    base_street = street.split(',')[0].strip()
    if base_street in parking_mappings:
        return parking_mappings[base_street]
    
    # Remove specific descriptors and numbers
    import re
    cleaned = re.sub(r'\s+\d+-?\d*\s+C/Pk$', '', street)
    cleaned = re.sub(r'\s+C/Pk$', '', cleaned)
    cleaned = re.sub(r'\s+\d+$', '', cleaned)
    
    return cleaned.strip()

def get_specific_coordinates(street: str) -> Dict[str, float]:
    """Get specific coordinates for known landmarks and hard-to-geocode locations"""
    specific_coords = {
        # Major squares and landmarks
        'Victoria Square': {'lat': -34.9289, 'lng': 138.5999},
        'Light Square': {'lat': -34.9253, 'lng': 138.5937},
        'Hindmarsh Square': {'lat': -34.9238, 'lng': 138.6052},
        'Whitmore Square': {'lat': -34.9327, 'lng': 138.5942},
        'Hurtle Square': {'lat': -34.9319, 'lng': 138.6058},
        'Bonython Park': {'lat': -34.9167, 'lng': 138.5833},
        'Elder Park': {'lat': -34.9198, 'lng': 138.5952},
        'Rymill Park': {'lat': -34.9236, 'lng': 138.6140},
        'Adelaide Park Lands': {'lat': -34.9285, 'lng': 138.6007},
        'War Memorial Drive': {'lat': -34.9159, 'lng': 138.6016},
        'Festival Drive': {'lat': -34.9201, 'lng': 138.5978},
        'Rundle Mall': {'lat': -34.9228, 'lng': 138.6026},
        'Topham Mall': {'lat': -34.9248, 'lng': 138.5977},
        
        # Major CBD streets (corrected coordinates)
        'Hindley Street': {'lat': -34.9231, 'lng': 138.5965},
        'Pulteney Street': {'lat': -34.9319, 'lng': 138.6063},
        'Gouger Street': {'lat': -34.9291, 'lng': 138.5919},
        'Flinders Street': {'lat': -34.9240, 'lng': 138.6000},  # CBD location, not Kent Town
        'North Terrace': {'lat': -34.9218, 'lng': 138.5920},
        'Angas Street': {'lat': -34.9257, 'lng': 138.6000},     # CBD location, not Kent Town  
        'Grenfell Street': {'lat': -34.9202, 'lng': 138.6000}, # CBD location, not Kent Town
        'Union Street': {'lat': -34.9240, 'lng': 138.6100},    # CBD location, not Stepney
        'Frome Street': {'lat': -34.9268, 'lng': 138.6082},
        'Halifax Street': {'lat': -34.9327, 'lng': 138.6033},
        'Franklin Street': {'lat': -34.9276, 'lng': 138.5911},
        'Pirie Street': {'lat': -34.9253, 'lng': 138.6088},
        'Currie Street': {'lat': -34.9249, 'lng': 138.5906},
        'Waymouth Street': {'lat': -34.9262, 'lng': 138.5903},
        'Gawler Place': {'lat': -34.9257, 'lng': 138.6021},
        'East Terrace': {'lat': -34.9307, 'lng': 138.6168},
        'West Terrace': {'lat': -34.9356, 'lng': 138.5885},
        'South Terrace': {'lat': -34.9358, 'lng': 138.5973},
        'King William Street': {'lat': -34.9308, 'lng': 138.6000},
        'Morphett Street': {'lat': -34.9218, 'lng': 138.5933},
        'Gilles Street': {'lat': -34.9340, 'lng': 138.6064},
        'Hutt Street': {'lat': -34.9309, 'lng': 138.6123},
        'Sturt Street': {'lat': -34.9329, 'lng': 138.5993},
        'Wright Street': {'lat': -34.9316, 'lng': 138.5976},
        'Carrington Street': {'lat': -34.9313, 'lng': 138.6044},
        'Rundle Street': {'lat': -34.9225, 'lng': 138.6094},
        
        # Problematic streets - CBD coordinates
        'Beaumont Road': {'lat': -34.9300, 'lng': 138.6100},   # Keep in CBD area
        'Eliza Street': {'lat': -34.9250, 'lng': 138.6080},    # CBD location
        'North Street': {'lat': -34.9240, 'lng': 138.6100},    # CBD location
        'Glen Osmond Road': {'lat': -34.9320, 'lng': 138.6150}, # CBD section
        'John Street': {'lat': -34.9280, 'lng': 138.6050},     # CBD section
    }
    
    base_street = street.split(',')[0].strip()
    return specific_coords.get(base_street)

def geocode_street(street: str, city: str = "Adelaide, South Australia, Australia") -> Dict[str, float]:
    """
    Geocode street using free Nominatim service with Adelaide-specific validation
    Returns lat/lng coordinates within Adelaide boundaries
    """
    cache_file = f"{CACHE_DIR}/geocode_cache.json"
    
    # Load existing cache
    cache = {}
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache = json.load(f)
    
    # Check cache first
    cache_key = f"{street}, {city}"
    if cache_key in cache:
        return cache[cache_key]
    
    # Check for specific coordinates first
    specific_coords = get_specific_coordinates(street)
    if specific_coords:
        print(f"✅ Using specific coordinates: {street} -> ({specific_coords['lat']:.4f}, {specific_coords['lng']:.4f})")
        cache[cache_key] = specific_coords
        with open(cache_file, 'w') as f:
            json.dump(cache, f, indent=2)
        return specific_coords
    
    # Clean street name for better geocoding
    cleaned_street = clean_street_for_geocoding(street)
    
    # Multiple search strategies for better Adelaide CBD-specific results
    search_queries = [
        f"{cleaned_street}, Adelaide CBD, Adelaide, South Australia, Australia",
        f"{cleaned_street}, Central Adelaide, South Australia, Australia",
        f"{cleaned_street}, Adelaide City Centre, SA, Australia",
        f"{cleaned_street}, Adelaide CBD, SA, Australia", 
        f"{cleaned_street}, Adelaide, SA, Australia", 
        f"{street.split(',')[0]}, Adelaide CBD, Australia"  # Fallback to original with CBD
    ]
    
    try:
        url = "https://nominatim.openstreetmap.org/search"
        headers = {
            'User-Agent': 'Adelaide-Parking-Map/1.0'
        }
        
        for query in search_queries:
            params = {
                'q': query,
                'format': 'json',
                'limit': 5,  # Get multiple results to filter
                'countrycodes': 'au',  # Limit to Australia
                'bounded': 1,
                'viewbox': '138.580,-34.915,138.620,-34.940'  # Adelaide CBD bounding box (stricter)
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Find the first result within Adelaide boundaries
            for result in data:
                lat = float(result['lat'])
                lng = float(result['lon'])
                
                if is_within_adelaide(lat, lng):
                    coords = {'lat': lat, 'lng': lng}
                    print(f"✅ Geocoded: {street} -> ({lat:.4f}, {lng:.4f})")
                    
                    # Cache result
                    cache[cache_key] = coords
                    with open(cache_file, 'w') as f:
                        json.dump(cache, f, indent=2)
                    
                    # Rate limiting
                    time.sleep(1)
                    return coords
            
            # Small delay between queries
            time.sleep(0.5)
        
        # If no result found within Adelaide, use default CBD coordinates
        print(f"⚠️  No Adelaide match for: {street}, using CBD default")
        result = {'lat': -34.9285, 'lng': 138.6007}
        
        # Cache the default result
        cache[cache_key] = result
        with open(cache_file, 'w') as f:
            json.dump(cache, f, indent=2)
        
        return result
        
    except Exception as e:
        print(f"❌ Geocoding failed for {street}: {e}")
        return {'lat': -34.9285, 'lng': 138.6007}  # Default Adelaide coordinates

def validate_existing_coordinates():
    """
    Validate existing geocoded coordinates and re-geocode if outside Adelaide
    """
    cache_file = f"{CACHE_DIR}/geocode_cache.json"
    
    if not os.path.exists(cache_file):
        return
        
    print("🔍 Validating existing geocoded coordinates...")
    
    with open(cache_file, 'r') as f:
        cache = json.load(f)
    
    invalid_count = 0
    for street_key, coords in cache.items():
        if not is_within_adelaide(coords['lat'], coords['lng']):
            invalid_count += 1
            street_name = street_key.split(',')[0]
            print(f"🚨 Invalid coordinates for {street_name}: ({coords['lat']:.4f}, {coords['lng']:.4f})")
    
    if invalid_count > 0:
        print(f"⚠️  Found {invalid_count} streets with coordinates outside Adelaide")
        response = input("Would you like to re-geocode these streets? (y/n): ")
        
        if response.lower() == 'y':
            print("🔄 Re-geocoding invalid coordinates...")
            # Clear invalid entries from cache
            updated_cache = {}
            for street_key, coords in cache.items():
                if is_within_adelaide(coords['lat'], coords['lng']):
                    updated_cache[street_key] = coords
                else:
                    print(f"   Removing: {street_key}")
            
            with open(cache_file, 'w') as f:
                json.dump(updated_cache, f, indent=2)
            
            print("✅ Invalid coordinates cleared. They will be re-geocoded.")
    else:
        print("✅ All cached coordinates are within Adelaide boundaries")

def process_parking_data():
    """Main data processing function"""
    print("Loading parking violations data...")
    
    # Validate existing coordinates first
    validate_existing_coordinates()
    
    # Read CSV with proper handling
    df = pd.read_csv(CSV_PATH, encoding='utf-8', low_memory=False)
    
    print(f"Loaded {len(df):,} records")
    
    # Clean data
    df['LocationOnStreet'] = df['LocationOnStreet'].apply(clean_street_name)
    df['OffenceDate'] = pd.to_datetime(df['OffenceDate'], format='%d/%m/%Y', errors='coerce')
    df['ExpiationAmount'] = pd.to_numeric(df['ExpiationAmount'], errors='coerce').fillna(0)
    df['OffenceBalance'] = pd.to_numeric(df['OffenceBalance'], errors='coerce').fillna(0)
    df['AmountPaid'] = pd.to_numeric(df['AmountPaid'], errors='coerce').fillna(0)
    
    # Remove invalid records
    df = df.dropna(subset=['OffenceDate', 'LocationOnStreet'])
    df = df[df['LocationOnStreet'] != 'Unknown']
    
    print(f"After cleaning: {len(df):,} records")
    
    # Generate street-level aggregations
    print("Generating street-level aggregations...")
    
    # First, get basic numeric aggregations
    numeric_stats = df.groupby('LocationOnStreet').agg({
        'ExpiationAmount': ['sum', 'count', 'mean'],
        'OffenceBalance': 'sum',
        'AmountPaid': 'sum',
        'OffenceDate': ['min', 'max']
    }).round(2)
    
    # Flatten column names for numeric stats
    numeric_stats.columns = ['_'.join(col).strip() for col in numeric_stats.columns]
    numeric_stats = numeric_stats.reset_index()
    
    # Separately handle categorical aggregations using a different approach
    print("Processing offence type breakdowns...")
    offence_types_dict = {}
    status_breakdown_dict = {}
    
    for street in df['LocationOnStreet'].unique():
        street_data = df[df['LocationOnStreet'] == street]
        
        # Get offence type counts
        offence_counts = street_data['OffenceType'].value_counts().to_dict()
        offence_types_dict[street] = offence_counts
        
        # Get status breakdown
        status_counts = street_data['Status'].value_counts().to_dict()
        status_breakdown_dict[street] = status_counts
    
    # Add dictionaries to the numeric stats dataframe
    numeric_stats['offence_types_dict'] = numeric_stats['LocationOnStreet'].map(offence_types_dict)
    numeric_stats['status_breakdown_dict'] = numeric_stats['LocationOnStreet'].map(status_breakdown_dict)
    
    street_stats = numeric_stats
    
    # Get unique streets for geocoding
    unique_streets = street_stats['LocationOnStreet'].unique()
    print(f"Geocoding {len(unique_streets)} unique streets...")
    
    # Geocode streets (this will take time but only needs to be done once)
    street_coordinates = {}
    for i, street in enumerate(unique_streets):
        if i % 10 == 0:
            print(f"Geocoding progress: {i}/{len(unique_streets)}")
        
        coords = geocode_street(street)
        street_coordinates[street] = coords
    
    # Merge coordinates with street stats
    street_data = []
    for _, row in street_stats.iterrows():
        street = row['LocationOnStreet']
        coords = street_coordinates.get(street, {'lat': -34.9285, 'lng': 138.6007})
        
        street_info = {
            'street': street,
            'coordinates': coords,
            'totalFines': float(row['ExpiationAmount_sum']),
            'totalCount': int(row['ExpiationAmount_count']),
            'averageFine': float(row['ExpiationAmount_mean']),
            'outstandingBalance': float(row['OffenceBalance_sum']),
            'totalPaid': float(row['AmountPaid_sum']),
            'offenceTypes': row['offence_types_dict'],
            'statusBreakdown': row['status_breakdown_dict'],
            'dateRange': {
                'first': row['OffenceDate_min'].strftime('%Y-%m-%d'),
                'last': row['OffenceDate_max'].strftime('%Y-%m-%d')
            }
        }
        street_data.append(street_info)
    
    # Sort by total fines (highest first)
    street_data.sort(key=lambda x: x['totalFines'], reverse=True)
    
    # Generate temporal analysis
    print("Generating temporal analysis...")
    df['Year'] = df['OffenceDate'].dt.year
    df['Month'] = df['OffenceDate'].dt.month
    df['DayOfWeek'] = df['OffenceDate'].dt.dayofweek
    df['Hour'] = df['OffenceHour']
    
    # Monthly trends
    monthly_stats = df.groupby(['Year', 'Month']).agg({
        'ExpiationAmount': ['sum', 'count'],
        'OffenceBalance': 'sum'
    }).round(2)
    monthly_stats.columns = ['_'.join(col) for col in monthly_stats.columns]
    monthly_stats = monthly_stats.reset_index()
    monthly_stats['date'] = pd.to_datetime(monthly_stats[['Year', 'Month']].assign(day=1))
    
    monthly_data = monthly_stats.to_dict('records')
    for record in monthly_data:
        record['date'] = record['date'].strftime('%Y-%m')
    
    # Hourly patterns
    hourly_stats = df.groupby('Hour').agg({
        'ExpiationAmount': ['sum', 'count', 'mean']
    }).round(2)
    hourly_stats.columns = ['_'.join(col) for col in hourly_stats.columns]
    hourly_data = hourly_stats.reset_index().to_dict('records')
    
    # Day of week patterns
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_stats = df.groupby('DayOfWeek').agg({
        'ExpiationAmount': ['sum', 'count', 'mean']
    }).round(2)
    daily_stats.columns = ['_'.join(col) for col in daily_stats.columns]
    daily_stats = daily_stats.reset_index()
    daily_stats['dayName'] = daily_stats['DayOfWeek'].apply(lambda x: day_names[x])
    daily_data = daily_stats.to_dict('records')
    
    # Offence type analysis
    offence_stats = df.groupby('OffenceType').agg({
        'ExpiationAmount': ['sum', 'count', 'mean']
    }).round(2)
    offence_stats.columns = ['_'.join(col) for col in offence_stats.columns]
    offence_data = offence_stats.reset_index().sort_values('ExpiationAmount_sum', ascending=False).to_dict('records')
    
    # Generate summary statistics
    summary_stats = {
        'totalRecords': len(df),
        'totalFines': float(df['ExpiationAmount'].sum()),
        'totalOutstanding': float(df['OffenceBalance'].sum()),
        'totalPaid': float(df['AmountPaid'].sum()),
        'averageFine': float(df['ExpiationAmount'].mean()),
        'dateRange': {
            'first': df['OffenceDate'].min().strftime('%Y-%m-%d'),
            'last': df['OffenceDate'].max().strftime('%Y-%m-%d')
        },
        'uniqueStreets': len(unique_streets),
        'lastUpdated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Save all data files
    print("Saving processed data files...")
    
    # Main street data for map
    with open(f"{OUTPUT_DIR}/streets.json", 'w') as f:
        json.dump(street_data, f, indent=2)
    
    # Temporal analysis
    with open(f"{OUTPUT_DIR}/temporal.json", 'w') as f:
        json.dump({
            'monthly': monthly_data,
            'hourly': hourly_data,
            'daily': daily_data
        }, f, indent=2)
    
    # Offence analysis
    with open(f"{OUTPUT_DIR}/offences.json", 'w') as f:
        json.dump(offence_data, f, indent=2)
    
    # Summary statistics
    with open(f"{OUTPUT_DIR}/summary.json", 'w') as f:
        json.dump(summary_stats, f, indent=2)
    
    print("\n✅ Data processing complete!")
    print(f"📊 Processed {len(df):,} records")
    print(f"🗺️  Generated data for {len(unique_streets)} streets")
    print(f"💰 Total fines: ${summary_stats['totalFines']:,.2f}")
    print(f"📁 Output files saved to {OUTPUT_DIR}/")

if __name__ == "__main__":
    ensure_directories()
    process_parking_data()