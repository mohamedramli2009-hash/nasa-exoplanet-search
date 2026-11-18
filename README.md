# NASA Exoplanet Advanced Search Engine 🪐

A professional Python and SQLite application designed to analyze, filter, and process NASA Exoplanet Archive data with high precision.

## Features 🌟
- **Diagnostic Report:** Automatically scans the dataset to check available temperature and diameter records.
- **Habitable Zone Preset:** Quick filter option to target planets within 0°C to 100°C.
- **Advanced Custom Search:** Filter by Temperature and Diameter with a smart `na` (Not Available) bypass option to skip criteria seamlessly.
- **Smart Priority Sorting:** Intelligently prioritizes records containing complete data when criteria are skipped.
- **Data Conversion:** Converts Kelvin to Celsius and Earth-radii to kilometers automatically.

## How to Run 💻
1. Clone or download this repository.
2. Download the official `planets_data.csv` dataset from the [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/).
3. Place `planets_data.csv` in the same directory as `planets_founder.py`.
4. Run the script using Python or Thonny:
   ```bash
   python planets_founder.py
