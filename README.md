# 🌍 The Methane Truth

> *We analyzed 304,611 real satellite methane observations over America. Here is what we found.*

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Snowflake](https://img.shields.io/badge/Snowflake-Data%20Warehouse-29B5E8)
![ESA](https://img.shields.io/badge/ESA-Sentinel%205P-003247)
![License](https://img.shields.io/badge/License-MIT-green)

---

## What Is This

Most discussions about satellite methane monitoring assume the satellite sees everything. I wanted to test that assumption with real data.

So I built a pipeline.

Using the ESA Copernicus API I downloaded every available Sentinel 5P TROPOMI methane observation over the continental United States for January 2023 and June through August 2023. I processed 304,611 quality filtered satellite pixels, compared them against NOAA verified atmospheric background levels, and cross referenced the results against official UNFCCC government inventory submissions.

What I found was not what I expected.

---

## Key Findings

**Finding One: Most satellite pixels see clean air.**

Only 21.5 percent of winter pixels and 11.7 percent of summer pixels exceeded the NOAA verified global methane background. The bulk of satellite observations over one of the world's largest methane emitters were measuring air cleaner than the global average. This is not a satellite failure. It is atmospheric physics. Methane plumes disperse rapidly across 5.5 kilometer pixels.

**Finding Two: The pixels that matter tell a precise story.**

| Region | Season | Peak ppb | Enhancement | Likely Source |
|--------|--------|----------|-------------|---------------|
| Northern Plains MN-ND border | Winter | 1976.2 | +56.3 ppb | Agricultural wetlands oil and gas |
| Gulf Coast TX-LA offshore | Summer | 1990.7 | +75.9 ppb | Petrochemical offshore oil and gas |
| California Central Valley | Summer | 1985.2 | +70.3 ppb | Dairy agriculture |

**Finding Three: Satellite monitoring is a geographic tool not a totals tool.**

National scale satellite data cannot reliably verify whether a country's total emission inventory is correct. But it can locate where emissions are coming from with precision no ground based system can match.

---

## Data Sources

| Source | Dataset | Access |
|--------|---------|--------|
| ESA Copernicus Data Space | Sentinel 5P TROPOMI L2 CH4 | Free at dataspace.copernicus.eu |
| NOAA Global Monitoring Laboratory | Monthly global mean methane | Free at gml.noaa.gov |
| Climate Watch API | UNFCCC national GHG inventories | Free at climatewatchdata.org |

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Ingestion | Python requests xarray netCDF4 | Download and parse satellite files |
| Warehouse | Snowflake | Store 300k plus observations |
| Transformation | dbt | Data quality tests and models |
| Orchestration | Apache Airflow | Pipeline scheduling |
| Visualization | Plotly Streamlit | Interactive dashboard |
| Environment | Google Colab | Cloud notebook zero local storage |

---

## Project Structure

```
methane-truth/
├── methane_truth_main.ipynb     
├── app.py                       
├── data/
│   └── processed/
│       ├── satellite_usa_winter.csv      
│       ├── satellite_usa_summer.csv      
│       ├── unfccc_usa_totals.csv         
│       ├── winter_hotspots.csv           
│       ├── summer_hotspots.csv           
│       └── corrected_gap_analysis.csv    
└── README.md
```

---

## How to Reproduce

**Step 1:** Create free account at dataspace.copernicus.eu

**Step 2:** Create free Snowflake trial at snowflake.com

**Step 3:** Open methane_truth_main.ipynb in Google Colab

**Step 4:** Run Cell 1 setup cell

**Step 5:** Run Cell 2 functions cell

**Step 6:** Follow cells sequentially. Each cell is documented.

---

## Methodology Notes

Quality filtering uses qa_value greater than 0.5 per ESA TROPOMI documentation. Background values use NOAA GML monthly means for exact study periods. January 2023 background is 1919.93 ppb. Summer 2023 average is 1914.89 ppb.

**Limitations:** Four months of data covering winter and summer only. Spring and autumn data would complete the annual picture. Orbital coverage is not uniform across all regions.

---

## What Comes Next

- Russia China India and Brazil as comparison countries
- Spring and autumn seasonal data
- Sector attribution against EPA facility level GHGRP data
- Automated monthly updates
- Statistical uncertainty quantification

---

## Live Dashboard

Coming soon at Streamlit Community Cloud

---

## Read the Full Analysis

Coming soon on Medium

---

## About the Author

**Likitha Yarabarla** is a Climate Data Engineer building open source analytics infrastructure for carbon markets and environmental accountability.

Currently at Worldview Development USA tracking 21.5 million tonnes of CO2e across mangrove conservation projects in 26 countries. Previously at 211 LA building disaster relief data pipelines during the LA wildfire response. MS Business Analytics Kent State University.

[LinkedIn](https://linkedin.com/in/likitha-sree) | [Blue Carbon Analysis](https://medium.com/the-quantastic-journal/the-blue-carbon-market-promised-to-save-the-worlds-coastlines-the-data-tells-a-different-story-6b4f4ec774bd)

---

## License

MIT License. Use freely with attribution.

*Built with real satellite data. Zero proprietary sources. Full reproducibility.*
