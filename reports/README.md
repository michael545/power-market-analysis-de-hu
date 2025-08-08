# Power Market Analysis: Germany (DE) vs. Hungary (HU)

## A Comparative Study of Weeks 29 & 30, 2025

This report provides an analysis of the German (DE) and Hungarian (HU) electricity markets for weeks 29 and 30 of  2025. It focuses on the fundamental drivers of the price spread between the two countries and explains the dramatic increase in volatility in Hungary observed in week 30, driven by a regional high temps and structural market inefficiencies.

---

### Weekly Comparison: Market Fundamentals

An analysis of the generation, load, and net positions (export - import) for both countries reveals their fundamentally different operational profiles.
![DE HU Prices](figures/DE_HU_prices.png)
(Day ahead market prices week on week comparison for weeks 29 and 30 of 2025 for Germany and Hungary)


#### Germany (DE): A Renewables-Driven Importer

![DE Load, Generation, and Net Position for Week 29](figures/DE_LU_wk29_load_gen_delta_price.png)
*(See also: figures/DE_LU_wk30_load_gen_delta_price.png)*

![DE total generation by source](figures/DE_generation_mix.png)
- **Germany's Generation Profile**: Germany's generation is highly dynamic, driven by a massive fleet of variable renewables. Solar power and wind dictate the daily profile, causing generation to peak significantly during daytime hours. This creates a "merit order effect" where cheap solar and wind power suppress daytime prices, often pushing them below those of neighboring countries. However, this also creates a "solar cliff" in the evening: as solar generation collapses, Germany must rely on imports and its own flexible power plants to meet sustained demand. This evening ramp is a key vulnerability, especially during heatwaves when demand remains high after sunset.

#### Hungary (HU): A Baseload-Driven Importer

![HU Load, Generation, and Net Position for Week 29](figures/HU_wk29_load_gen_delta_price.png)
*(See also: figures/HU_wk30_load_gen_delta_price.png)*
![HU total generation by source](figures/HU_generation_mix.png)

- **Hungary's 'Perfect Storm'**: Hungary's market design flaws create a "perfect storm" during high-demand periods. Its generation is dominated by inflexible baseload power (like nuclear), which cannot ramp up quickly to meet peak demand. This creates a structural dependency on imports. During a regional heatwave, neighboring countries are also desperate for power, leading to a "load squeeze" where Hungary is forced to pay exorbitant prices for imports. This is exacerbated by physical constraints on cross-border transmission lines, which can become congested, further limiting supply and amplifying price spikes. The result is extreme price volatility, as seen in Week 30, where prices decoupled entirely from the more stable German market.

#### Generation Mix at a Glance

![DE vs HU Generation Mix for Weeks 29 & 30](figures/DE_HU_GEN_CONSUMPTION_weeks_29_30.png)

This visual starkly contrasts Germany's massive, solar-dominated (yellow) and wind-influenced (light blue) generation mix with Hungary's much smaller and flatter profile. This difference in generation philosophy is the root cause of the diverging market dynamics and price spreads.

---

### HU-DE Spread Analysis: From Stability to Extreme Volatility

The structural differences between the two markets materialize in the price spread `(HU Price - DE Price)`. While Week 29 showed a manageable spread, Week 30 saw an explosion in volatility driven almost entirely by the Hungarian market and temperatures often reaching over 30 degrees celsisus.

#### Price & Spread Evolution (Week 29 vs. Week 30)
![Spread across 4 weeks  of july](figures/HU_DE_LUspread_linear_scale.png)
![Comparison of DE and HU Prices for Weeks 29 & 30](figures/DE_HU_prices.png)
![Comparison of HU-DE Spread for Weeks 29 & 30](figures/weeks_29_30_comparions_spread.png)

* **Week 29**: Hungarian prices were consistently higher than German prices, but the two markets remained broadly coupled (nothing too out of usual happened). The spread was positive but mostly contained below €80/MWh.
* **Week 30**: The markets decoupled dramatically. While German prices remained relatively stable, Hungarian prices experienced extreme spikes approaching €400/MWh. This caused the HU-DE spread to surge, spiking to over €200/MWh on July 24th and peaking at over €250/MWh on July 25th.

#### Drivers of the Price Spikes: A Perfect Storm in Hungary

The extreme price spikes originate from Hungary's structural vulnerabilities, which were exacerbated by a regional heatwave that created a "perfect storm" of afternoon load and supply pressures.

1.  **Structural Import Dependency & Inflexible Generation**: The primary driver is Hungary's inability to meet its own peak demand. The `figures/HU_wk30_load_gen_delta_price.png` chart shows a direct correlation: the highest price spikes occur precisely when Hungary's net position is most negative. This is a direct result of its inflexible baseload generation being unable to meet the evening peak demand, which is intensified by the heatwave-driven need for AC. Hungary becomes a "price taker," forced to import power at any cost.

2.  **Regional "Load Squeeze"**: Hungary's geographical position is a critical vulnerability. During a regional heatwave, its neighbors face the same crisis. As documented in the provided reports, countries like Croatia (HR) and Romania (RO) also experience huge demand spikes. This creates a regional "load squeeze" where multiple countries are competing for scarce power. This regional scarcity and supply inelesticity is a key reason why prices in Hungary can spike to levels far beyond those in Western Europe.

3.  **Complex Cross-Border Flows**: The `figures/graph-flow_visuzlizer-app.jpg` hints at the complex flow dynamics. While Hungary is importing heavily from the north and west (e.g., Slovakia, Austria, Slovenia, where prices are lower), it may simultaneously be exporting or see reduced import capacity from the south and east due to the regional squeeze. During peak demand, flows from Slovakia (SK) alone can reach more than 2 GW to help meet the deficit. This makes Hungary a critical but vulnerable transit hub. In contrast, Germany can leverage more diverse and resilient partners like France (nuclear) and the Nordic countries (hydro), giving it more options to manage price volatility.

---
![spread vs temp graph week 30 and 29](figures/spread_vs_temp.png)

### Conclusion

The analysis clearly demonstrates that the HU-DE price spread is fundamentally driven by **Hungary's structural dependency on imports** to meet its peak electricity demand. This vulnerability, rooted in its inflexible generation mix and its geographical position within a fragile region, is severely exposed during periods of regional stress, such as a heatwave. Week 30 serves as a textbook example of this risk materializing, where manageable price differences escalated into extreme and costly volatility for the Hungarian market, a direct consequence of the massive delta between its generation capabilities and its peak, weather-driven demand.