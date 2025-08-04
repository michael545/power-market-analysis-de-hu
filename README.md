# Power Market Analysis: DE vs. HU (Weeks 29 & 30, 2025)

This project is an in-depth analysis of the spot electricity prices and their fundamental ridvers in Germany and Hungary for weeks 29 and 30 of  2025. IT aims to identify the key factors influencing price levels and the spread between the two countries.

## Goals

1.  **Data Collection:** relevant market data for the specified periods +- 2weeks.
2.  **Data Analysis:** Comprehensive review of the collected data with visualizations and statistical summaries.
3.  **Price Driver Assessment:** Determine the primary factors affecting:
    *   The week-over-week evolution of DE spot prices.
    *   The price delta between DE and HU.
4.  **Advanced Simulation (Optional):**

## Data Sources

*   **Spot Prices:**
    *   Germany (DE): EPEX Spot
    *   Hungary (HU): HUPX
*   **Fundamental Data:**
    *   ENTSO-E Transparency Platform for:
        *   Generation data (Solar, Wind)
        *   Load (consumption) data
        *   Net export/import balance for CWE, Hungary, Romania, Bulgaria, Slovenia, and Croatia.

## Repository Structure

```
.
├── data/
│   ├── processed/      # Cleaned and merged datasets for analysis
│   └── raw/            # Raw data downloaded from sources
├── notebooks/
│   ├── 01_data_acquisition.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_exploratory_data_analysis.ipynb
│   └── 04_price_driver_analysis.ipynb
├── reports/
│   └── figures/        # Generated plots and visualizations
├── scripts/
│   ├── data_fetcher.py # Scripts to download data from APIs/websites
│   ├── plotting.py     # Reusable plotting functions
│   └── analysis.py     # Core analysis functions
└── README.md
```

## Setup

### Option 1: Using Conda (Recommended)
```bash
# Create environment from file
conda env create -f environment.yml

# Activate environment
conda activate power-market-env


### Option 2: Using pip
To run the analysis, install the required Python libraries:

```bash
pip install -r requirements.txt
```

### ENTSO-E API Setup
Free account at [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/) and get the API token.

## Analysis Workflow

1.  **Data Acquisition (`notebooks/01_data_acquisition.ipynb`):** Fetch all required data using the scripts in `scripts/data_fetcher.py`.
2.  **Data Preprocessing (`notebooks/02_data_preprocessing.ipynb`):** Clean, merge, and structure the raw data into a unified dataset.
3.  **Exploratory Data Analysis (`notebooks/03_exploratory_data_analysis.ipynb`):** Visualize time series data (prices, generation, load) and create summary tables.
4.  **Price Driver Analysis (`notebooks/04_price_driver_analysis.ipynb`):** Perform correlation analysis and build simple models to identify the key drivers identified in the project goals.
