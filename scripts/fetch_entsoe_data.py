import os
import pandas as pd
from entsoe import EntsoePandasClient
from entsoe.mappings import NEIGHBOURS
from dotenv import load_dotenv

def fetch_entsoe_data(api_key, start_date, end_date, output_dir):
    """
    Args:
        api_key (str): Your ENTSO-E API key.
        start_date (pd.Timestamp): Start date for data fetching.
        end_date (pd.Timestamp): End date for data fetching.
        output_dir (str): Directory to save the fetched data.
    """
    client = EntsoePandasClient(api_key=api_key)
    os.makedirs(output_dir, exist_ok=True)

    countries = {"HU", "DE_LU"}
    for country in countries:
        try:
            print(f"Fetching spot prices for {country}...")
            prices = client.query_day_ahead_prices(country, start=start_date, end=end_date)
            prices.to_csv(os.path.join(output_dir, f"{country}_spot_prices.csv"))
            print(f"fetched, saved spot prices for {country}.")
        except Exception as e:
            print(f"Error for {country}: {e}")

    for country in countries:
        try:
            print(f"Fetching generation and load for {country}...")
            generation = client.query_generation(country, start=start_date, end=end_date, psr_type=None)
            load = client.query_load(country, start=start_date, end=end_date)
            
            generation.to_csv(os.path.join(output_dir, f"{country}_generation.csv"))
            load.to_csv(os.path.join(output_dir, f"{country}_load.csv"))
            print(f"Successfully fetched and saved generation and load for {country}.")
        except Exception as e:
            print(f"Error fetching generation and load for {country}: {e}")

    # neto bilance
    cwe_countries = ["AT", "BE", "FR", "DE_LU", "NL", "SK", "CZ", "PL"]# FBMC 13 with LU/DE merged
    other_countries = ["HU", "RO", "SI", "HR"]
    all_countries = cwe_countries + other_countries
    #all_countries = list(NEIGHBOURS.keys())  # 

    for country_from in all_countries:
        for country_to in all_countries:
            if country_from != country_to:
                try:
                    print(f"Fetching cross-border flows from {country_from} to {country_to}...")
                    flows = client.query_crossborder_flows(country_from, country_to, start=start_date, end=end_date)
                    flows.to_csv(os.path.join(output_dir, f"flows_{country_from}_{country_to}.csv"))
                    print(f"Successfully fetched and saved cross-border flows from {country_from} to {country_to}.")
                except Exception as e:
                    print(f"Error fetching cross-border flows from {country_from} to {country_to}: {e}")


if __name__ == "__main__":
    load_dotenv()
    entsoe_api_key = os.getenv("ENTSOE_API_KEY")
    if not entsoe_api_key:
        raise ValueError("ENTSOE_API_KEY wrong")

    
    start = pd.Timestamp("2025-07-07", tz="Europe/Brussels")
    end = pd.Timestamp("2025-08-04", tz="Europe/Brussels")

    # Define output directory
    output_dir = "C:\\Users\\micha\\code\\power-market-analysis-de-hu\\data\\processed"

    fetch_entsoe_data(entsoe_api_key, start, end, output_dir)
