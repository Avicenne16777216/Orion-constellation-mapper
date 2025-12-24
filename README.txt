Orion Constellation Visualizer

This project retrieves star data for the constellation "Orion" using the KEY = "ZB6SN0rbSV9U35XYn9QWRA==T3GlIVshXQqMGrHD"(https://api-ninjas.com/api/stars), converts celestial coordinates (Right Ascension and Declination) into decimal degrees, and visualizes the constellation with Matplotlib.

✨ Features
- Fetches star data from an external API.
- Converts RA/Dec strings into decimal degrees.
- Plots Orion’s stars on a black background with annotations for the main stars.
- Handles Unicode formats for astronomical coordinates.

📂 Project Structure
- `convertir_coords_stellaires_en_xy`: Function to parse RA/Dec strings and convert them into decimal degrees.
- API request block: Fetches Orion star data.
- Visualization block: Plots stars with Matplotlib.

⚙️ Requirements
- Python 3.8+
- Libraries:
  - `requests`
  - `re` (built-in)
  - `math` (built-in)
  - `matplotlib`

Install dependencies:
```bash
pip install requests matplotlib
