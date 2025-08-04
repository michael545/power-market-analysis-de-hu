import pandas as pd
import numpy as np
from pathlib import Path

def process_weather_data():
    """
    Process raw weather data from long format to wide format with timestamps as rows
    and cities as columns for easier analysis.
    """
    project_root = Path(__file__).parent.parent
    raw_data_path = project_root / "data" / "raw"
    processed_data_path = project_root / "data" / "processed"
    
    processed_data_path.mkdir(parents=True, exist_ok=True)
    
    hourly_raw_file = raw_data_path / "hourly_weather_HU_DE_weeks29_30.csv"
    daily_raw_file = raw_data_path / "daily_max_weather_HU_DE_weeks29_30.csv"
    
    hourly_processed_file = processed_data_path / "hourly_weather_wide_weeks29_30.csv"
    daily_processed_file = processed_data_path / "daily_max_weather_wide_weeks29_30.csv"
    
    print("Processing weather data from long to wide format...")
    
    if hourly_raw_file.exists():
        print(f"Processing {hourly_raw_file.name}...")
        
        # Load hourly data
        hourly_df = pd.read_csv(hourly_raw_file)
        hourly_df['datetime'] = pd.to_datetime(hourly_df['datetime'])
        
        print(f"Raw hourly data shape: {hourly_df.shape}")
        print(f"Countries: {hourly_df['country'].unique()}")
        print(f"Cities: {hourly_df['city'].unique()}")
        
        # Create pivot table with timestamp as index, cities as columns
        hourly_wide = hourly_df.pivot_table(
            index='datetime',
            columns=['country', 'city'],
            values='temperature',
            aggfunc='mean'  # In case there are duplicates
        )
        
        hourly_wide.columns = [f"{country}_{city}_temp" for country, city in hourly_wide.columns]
        
        hourly_wide = hourly_wide.reset_index()
        
        hourly_wide = hourly_wide.sort_values('datetime')
        
        hourly_wide.to_csv(hourly_processed_file, index=False)
        
        print(f"Processed hourly data shape: {hourly_wide.shape}")
        print(f"Columns: {list(hourly_wide.columns)}")
        print(f"Date range: {hourly_wide['datetime'].min()} to {hourly_wide['datetime'].max()}")
        print(f"Saved to: {hourly_processed_file}")
        
        print("\head hourly data:")
        print(hourly_wide.head(3))
        
    else:
        print(f"Hourly raw file not found: {hourly_raw_file}")
    
    # Process daily max data
    if daily_raw_file.exists():
        print(f"\nProcessing {daily_raw_file.name}...")
        
        # Load daily data
        daily_df = pd.read_csv(daily_raw_file)
        daily_df['date'] = pd.to_datetime(daily_df['date'])
        
        print(f"Raw daily data shape: {daily_df.shape}")
        
        # Create pivot table with date as index, cities as columns
        daily_wide = daily_df.pivot_table(
            index='date',
            columns=['country', 'city'],
            values='max_temperature',
            aggfunc='mean'  # In case there are duplicates
        )
        
        # Flatten column names to be more readable
        daily_wide.columns = [f"{country}_{city}_max_temp" for country, city in daily_wide.columns]
        
        # Reset index to make date a column
        daily_wide = daily_wide.reset_index()
        
        # Sort by date
        daily_wide = daily_wide.sort_values('date')
        
        # Save processed data
        daily_wide.to_csv(daily_processed_file, index=False)
        
        print(f"Processed daily data shape: {daily_wide.shape}")
        print(f"Columns: {list(daily_wide.columns)}")
        print(f"Date range: {daily_wide['date'].min()} to {daily_wide['date'].max()}")
        print(f"Saved to: {daily_processed_file}")
        
        # Show sample
        print("\nSample daily data:")
        print(daily_wide.head(3))
        
        # Calculate country averages
        print("\n--- Adding Country Averages ---")
        
        # Get DE and HU city columns
        de_cols = [col for col in daily_wide.columns if col.startswith('DE_') and col.endswith('_max_temp')]
        hu_cols = [col for col in daily_wide.columns if col.startswith('HU_') and col.endswith('_max_temp')]
        
        # Calculate country averages
        daily_wide['DE_avg_max_temp'] = daily_wide[de_cols].mean(axis=1)
        daily_wide['HU_avg_max_temp'] = daily_wide[hu_cols].mean(axis=1)
        daily_wide['temp_delta_HU_DE'] = daily_wide['HU_avg_max_temp'] - daily_wide['DE_avg_max_temp']
        
        # Also add country averages to hourly data
        de_hourly_cols = [col for col in hourly_wide.columns if col.startswith('DE_') and col.endswith('_temp')]
        hu_hourly_cols = [col for col in hourly_wide.columns if col.startswith('HU_') and col.endswith('_temp')]
        
        hourly_wide['DE_avg_temp'] = hourly_wide[de_hourly_cols].mean(axis=1)
        hourly_wide['HU_avg_temp'] = hourly_wide[hu_hourly_cols].mean(axis=1)
        hourly_wide['temp_delta_HU_DE'] = hourly_wide['HU_avg_temp'] - hourly_wide['DE_avg_temp']
        
        # Save updated files
        hourly_wide.to_csv(hourly_processed_file, index=False)
        daily_wide.to_csv(daily_processed_file, index=False)
        
        print(f"Added country averages. Updated files saved.")
        print(f"Daily temperature delta range: {daily_wide['temp_delta_HU_DE'].min():.1f}°C to {daily_wide['temp_delta_HU_DE'].max():.1f}°C")
        
    else:
        print(f"Daily raw file not found: {daily_raw_file}")
    
    print("\n=== Weather data processing completed! ===")
    print(f"Processed files saved to: {processed_data_path}")

if __name__ == "__main__":
    process_weather_data()
