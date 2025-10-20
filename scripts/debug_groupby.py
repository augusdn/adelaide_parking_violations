#!/usr/bin/env python3
"""
Debug script to check the pandas groupby structure
"""

import pandas as pd

# Configuration
CSV_PATH = "./data/Parking_Expiations.csv"

def debug_groupby():
    """Debug the groupby structure"""
    print("Loading sample of parking violations data...")
    
    # Read only first 1000 rows for debugging
    df = pd.read_csv(CSV_PATH, encoding='utf-8', low_memory=False, nrows=1000)
    
    print(f"Loaded {len(df):,} records for debugging")
    
    # Clean data
    df['LocationOnStreet'] = df['LocationOnStreet'].apply(lambda x: str(x).strip().strip('"') if pd.notna(x) else "Unknown")
    df = df[df['LocationOnStreet'] != 'Unknown']
    
    print(f"After cleaning: {len(df):,} records")
    print(f"Sample streets: {df['LocationOnStreet'].unique()[:5]}")
    
    # Test the problematic groupby
    print("\nTesting offence types groupby...")
    offence_types = df.groupby('LocationOnStreet')['OffenceType'].apply(lambda x: x.value_counts().to_dict())
    print(f"Type: {type(offence_types)}")
    print(f"Index: {offence_types.index[:3]}")
    print(f"Sample values: {list(offence_types.values)[:2]}")
    
    # Reset index and check columns
    offence_types_reset = offence_types.reset_index()
    print(f"After reset_index - Shape: {offence_types_reset.shape}")
    print(f"Columns: {offence_types_reset.columns.tolist()}")
    print(f"First few rows:")
    print(offence_types_reset.head())

if __name__ == "__main__":
    debug_groupby()