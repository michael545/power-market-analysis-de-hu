import os
import pandas as pd
from entsoe import EntsoePandasClient
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    
    api_key = os.getenv("ENTSOE_API_KEY")
    try:
        start_date = pd.Timestamp("2025-07-07", tz="Europe/Brussels") # [0] week 28, 
        end_date = pd.Timestamp("2025-08-04", tz="Europe/Brussels")   # [end] week 31 

        client = EntsoePandasClient(api_key=api_key)
        de_prices = client.query_day_ahead_prices('DE_LU', start=start_date, end=end_date)

        if de_prices.empty:
            print("query ok, but no data  returned.")
        else:
            script_dir = os.path.dirname(__file__)
            output_dir = os.path.join(script_dir, '..', 'data', 'processed')
            os.makedirs(output_dir, exist_ok=True)
            
            output_file_path = os.path.join(output_dir, 'DE_spot_prices.csv')
            de_prices.to_csv(output_file_path)
            print(f"saved to: {output_file_path}")

            with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                print(de_prices)

    except Exception as e:
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Details: {e}")
        

