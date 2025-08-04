import requests
import pandas as pd
import logging
import time
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CITIES = {
    "DE": ["Berlin", "Munich", "Frankfurt"],  #  faster processing
    "HU": ["Budapest", "Debrecen", "Szeged"]
}

 # 29 and 30 of 2025
START_DATE = "2025-07-14"
END_DATE = "2025-07-28"

GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
HISTORICAL_API_URL = "https://archive-api.open-meteo.com/v1/archive"

OUTPUT_HOURLY_CSV = "data/raw/hourly_weather_HU_DE_weeks29_30.csv"
OUTPUT_DAILY_CSV = "data/raw/daily_max_weather_HU_DE_weeks29_30.csv"

def get_city_coordinates(city_name: str, country_code: str) -> tuple[float, float] | None:
    """
   get latitude and longitude for a city using  Open-Meteo Geocoding API.
    """
    try:
        params = {'name': city_name, 'count': 1, 'language': 'en', 'format': 'json'}
        response = requests.get(GEOCODING_API_URL, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if 'results' in data:
            for result in data['results']:
                if result.get('country_code', '').upper() == country_code.upper():
                    return result['latitude'], result['longitude']
        
        logging.warning(f"Could not find coordinates for {city_name}, {country_code}.")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Geocoding request failed for {city_name}: {e}")
        return None

def fetch_hourly_weather_data(latitude: float, longitude: float, start_date: str, end_date: str) -> pd.DataFrame | None:
    
    try:
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'start_date': start_date,
            'end_date': end_date,
            'hourly': 'temperature_2m',  
            'timezone': 'Europe/Berlin'  #CET
        }
        response = requests.get(HISTORICAL_API_URL, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()
        if 'hourly' not in data or 'time' not in data['hourly']:
            logging.error(f"No hourly data available for lat:{latitude}, lon:{longitude}")
            return None

        df = pd.DataFrame(data['hourly'])
        df.rename(columns={
            'time': 'datetime',
            'temperature_2m': 'temperature'
        }, inplace=True)
        
        df['datetime'] = pd.to_datetime(df['datetime'])
        
        return df

    except requests.exceptions.RequestException as e:
        logging.error(f"Hourly weather request failed for lat:{latitude}, lon:{longitude}: {e}")
        return None
    except (KeyError, TypeError) as e:
        logging.error(f"Error parsing hourly weather data: {e}")
        return None

def fetch_daily_max_weather_data(latitude: float, longitude: float, start_date: str, end_date: str) -> pd.DataFrame | None:
    """
    Fetches historical daily max temperature for a given location and date range.
    """
    try:
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'start_date': start_date,
            'end_date': end_date,
            'daily': 'temperature_2m_max',  # Daily maximum temperature
            'timezone': 'Europe/Berlin'
        }
        response = requests.get(HISTORICAL_API_URL, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()
        if 'daily' not in data or 'time' not in data['daily']:
            logging.error(f"No daily data available for lat:{latitude}, lon:{longitude}")
            return None

        df = pd.DataFrame(data['daily'])
        df.rename(columns={
            'time': 'date',
            'temperature_2m_max': 'max_temperature'
        }, inplace=True)
        
        df['date'] = pd.to_datetime(df['date'])
        
        return df

    except requests.exceptions.RequestException as e:
        logging.error(f"Daily weather request failed for lat:{latitude}, lon:{longitude}: {e}")
        return None
    except (KeyError, TypeError) as e:
        logging.error(f"Error parsing daily weather data: {e}")
        return None

def main():
    """
     funct to fetch h and d data for weeks 29-30 of 2025.
    """
    logging.info("Starting weather data fetching for weeks 29-30, 2025...")
    hourly_data = []
    daily_data = []

    for country_code, cities in CITIES.items():
        for city in cities:
            logging.info(f"Processing {city}, {country_code}...")
            
            coords = get_city_coordinates(city, country_code)
            if not coords:
                continue
            
            lat, lon = coords
            logging.info(f"Coordinates for {city}: Lat={lat:.4f}, Lon={lon:.4f}")
            
            hourly_df = fetch_hourly_weather_data(lat, lon, START_DATE, END_DATE)
            if hourly_df is not None and not hourly_df.empty:
                hourly_df['city'] = city
                hourly_df['country'] = country_code
                hourly_data.append(hourly_df)
                logging.info(f"Hourly data fetched for {city}: {len(hourly_df)} records")
            
            # Fetch daily max data
            daily_df = fetch_daily_max_weather_data(lat, lon, START_DATE, END_DATE)
            if daily_df is not None and not daily_df.empty:
                daily_df['city'] = city
                daily_df['country'] = country_code
                daily_data.append(daily_df)
                logging.info(f"Daily max data fetched for {city}: {len(daily_df)} records")
            
            time.sleep(1)

    if hourly_data:
        final_hourly_df = pd.concat(hourly_data, ignore_index=True)
        final_hourly_df = final_hourly_df[['country', 'city', 'datetime', 'temperature']]
        final_hourly_df.to_csv(OUTPUT_HOURLY_CSV, index=False)
        
        logging.info(f"Hourly data saved to {OUTPUT_HOURLY_CSV}")
    
    if daily_data:
        final_daily_df = pd.concat(daily_data, ignore_index=True)
        final_daily_df = final_daily_df[['country', 'city', 'date', 'max_temperature']]
        final_daily_df.to_csv(OUTPUT_DAILY_CSV, index=False)
        
        logging.info(f"Daily max data saved to {OUTPUT_DAILY_CSV}")
    
    if not hourly_data and not daily_data:
        logging.warning("No weather data was collected.")

if __name__ == "__main__":
    main()