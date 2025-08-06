import pandas as pd
from dotenv import load_dotenv
import os
from entsoe_fetcher import EntsoeFetcher
import logging

load_dotenv()


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


entsoe_api_key = os.getenv("ENTSOE_API_KEY")

start_date = pd.Timestamp('2025-07-07', tz='Europe/Brussels')
end_date = pd.Timestamp('2025-08-04', tz='Europe/Brussels')

country_codes = ['AT', 'BE', 'BG', 'CZ', 'DE_LU', 'FR', 'HR', 'HU', 'NL', 'PL', 'RO', 'SI', 'SK']
#what
output_dir = os.path.join("data", "processed", "net_balances")
os.makedirs(output_dir, exist_ok=True)

logging.info(f"Starting data fetch for {len(country_codes)} countries from {start_date.date()} to {end_date.date()}.")

fetcher = EntsoeFetcher(
    api_key=entsoe_api_key, 
    start_date=start_date, 
    end_date=end_date, 
    output_dir=output_dir
)

logging.info("Fetching net positions...")
for country_code in country_codes:
    fetcher.fetch_data(
        data_type='net_position',
        country_code=country_code
    )

logging.info("Data fetching process completed.")
