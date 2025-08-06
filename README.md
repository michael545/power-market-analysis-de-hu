# Power Market Analysis: DE vs. HU (Weeks 29 & 30, 2025)


This project is an ammateur analysis of the spot electricity prices and their fundamental dridvers in Germany and Hungary for weeks 29 and 30 of  2025. It aims to identify the key factors influencing price levels and the spread between the two countries.

## Preliminary

### Germany
*   **Wind:** A European leader with ~70 GW of combined onshore and offshore capacity, contributing bigly (around 30%) to the national power mix. The sector continues to expand rapidly.
*   **Solar:** Robust capacity of nearly 108 GW, generating 14% of the country's electricity. Has targets to do more than double of this by 2030.
*   **Hydropower:** A mature and stable sector with over 11 GW of capacity, playing a consistent role in the energy mix, particularly for grid stability.

### Hungary
*   **Wind:** A smaller sector with a modest capacity of 329 MW. Recent regulatory reforms are expected to encourage future growth, but its current contribution is minimal (~1.5%).
*   **Solar:**  Explosive growth, with capacity surging past 7,550 MW—exceeding 2030 targets well ahead of schedule. Solar now accounts for 25% of electricity generation.
*   **Hydropower:** Geographically limited, with small capacity (~40 MW), playing a minor role in the national energy strategy.


## Goals

1.  **Data Collection:** relevant market data for the specified periods +- 2 weeks.
2.  **Data Analysis:** Review of the collected data with visualizations and statistical summaries.
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
        *   Generation data (Solar, Wind, Oil, Nuclera)
        *   Load (consumption) data
        *   Net export/import balance for CWE, Romania, Bulgaria, Slovenia, and Croatia.

## Repository Structure

```
.
├── data/
│   ├── processed/      # Cleaned and merged for analysis
│   └── raw/            # Raw data downloaded from sources
├── notebooks/
│   ├── 01_data_acquisition.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_exploratory_data_analysis.ipynb
│   └── 04_price_driver_analysis.ipynb
├── reports/
│   └── figures/        # Generated plots and visuals
├── scripts/
│   ├── data_fetcher.py # Scripts to download data from APIs/websites
│   ├── 
│   └── 
└── README.md
```

## Setup

### Option 1: via Conda (Recommended)
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
Free account at [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/) and get the API token via Email request.
