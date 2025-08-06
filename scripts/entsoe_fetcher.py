import os
import logging
import pandas as pd
from entsoe import EntsoePandasClient
from entsoe.mappings import NEIGHBOURS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EntsoeFetcher:
    """
    Attributes:
        client (EntsoePandasClient): to interact with the ENTSO-E API.
        start_date (pd.Timestamp): start date for data queries.
        end_date (pd.Timestamp): end date for data queries.
        output_dir (str): The directory where fetched data will be saved.
    """
    def __init__(self, api_key: str, start_date: pd.Timestamp, end_date: pd.Timestamp, output_dir: str):
        if not api_key:
            raise ValueError("ENTSO-E API key NEEDED, not found.")
        
        self.client = EntsoePandasClient(api_key=api_key)
        self.start_date = start_date
        self.end_date = end_date
        self.output_dir = output_dir
        
        os.makedirs(self.output_dir, exist_ok=True)
        logging.info(f"EntsoeFetcher initialized for date range {start_date.date()} to {end_date.date()}")

    def fetch_data(self, data_type: str, country_code: str):

        query_methods = {
            'load': self.client.query_load,
            'generation': self.client.query_generation,
            'prices': self.client.query_day_ahead_prices,
            'net_position': self.client.query_net_position
        }

        if data_type not in query_methods:
            logging.error(f" query '{data_type}' not supported.")
            return

        filepath = os.path.join(self.output_dir, f"{data_type}_{country_code}.csv")
        logging.info(f"Fetching {data_type} data for {country_code}...")

        try:
            query_func = query_methods[data_type]
            data = query_func(country_code, start=self.start_date, end=self.end_date)
            
            data.to_csv(filepath)
            logging.info(f"Fetched and saved data to {filepath}")

        except Exception as e:
            logging.error(f"Failed to fetch {data_type} for {country_code}. Error: {e}")

    def fetch_all_crossborder_flows(self, country_code: str):

        if country_code not in NEIGHBOURS:
            logging.warning(f"Country code '{country_code}' not found in the neighbours mapping. Skipping flows.")
            return

        neighbours = NEIGHBOURS[country_code]
        logging.info(f"Fetching cross-border flows for {country_code}. Neighbours: {neighbours}")

        for neighbour in neighbours:
            # do From -> To
            try:
                logging.info(f"Fetching flows from {country_code} to {neighbour}...")
                flows_out = self.client.query_crossborder_flows(country_code, neighbour, start=self.start_date, end=self.end_date)
                filepath_out = os.path.join(self.output_dir, f"flows_{country_code}_{neighbour}.csv")
                flows_out.to_csv(filepath_out)
                logging.info(f"Successfully saved flows to {filepath_out}")
            except Exception as e:
                logging.error(f"Could not fetch flows from {country_code} to {neighbour}. Error: {e}")
            
            # do To -> From
            try:
                logging.info(f"Fetching flows from {neighbour} to {country_code}...")
                flows_in = self.client.query_crossborder_flows(neighbour, country_code, start=self.start_date, end=self.end_date)
                filepath_in = os.path.join(self.output_dir, f"flows_{neighbour}_{country_code}.csv")
                flows_in.to_csv(filepath_in)
                logging.info(f"Successfully saved flows to {filepath_in}")
            except Exception as e:
                logging.error(f"Could not fetch flows from {neighbour} to {country_code}. Error: {e}")


# if __name__ == "__main__":
#     load_dotenv()
#     entsoe_api_key = os.getenv("ENTSOE_API_KEY")

#     start = pd.Timestamp("2025-07-07", tz="Europe/Brussels")
#     end = pd.Timestamp("2025-07-14", tz="Europe/Brussels") # Using a shorter range for demonstration
#     output_dir = os.path.join("..", "data", "processed") # Relative path to the data folder

    
#     fetcher = EntsoeFetcher(api_key=entsoe_api_key, start_date=start, end_date=end, output_dir=output_dir)

#     countries_to_fetch = ["DE_LU", "HU", "PL", "SI", "HR", "AT", "SK"]
#     data_types_to_fetch = ['prices', 'load', 'generation']

#     # 3. Loop and fetch the data
#     for country in countries_to_fetch:
#         for data_type in data_types_to_fetch:
#             # This single line replaces your previous try/except blocks
#             fetcher.fetch_data(data_type, country)

#     # 4. Fetch all cross-border flows for specific countries efficiently
#     for country in ["HU", "SK", "AT"]:
#         fetcher.fetch_all_crossborder_flows(country)
        
#     logging.info("--- Data fetching process complete. ---")