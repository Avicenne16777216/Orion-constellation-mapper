🌌 Orion Constellation Mapper & Coordinate Converter

A Python-based astronomical tool that programmatically retrieves stellar data to map the Orion constellation. This project demonstrates the intersection of API integration, Regular Expressions (RegEx), and Celestial Mechanics.


🎯 Project Overview
This tool automates the collection of stellar data for the Orion constellation. The challenge lies in the fact that astronomical data is often served in non-decimal formats (Sexagesimal). This script parses those strings and projects them onto a 2D Cartesian plane for visualization.

🛠️ Technical Highlights

1. Mathematical Coordinate Conversion
To plot the stars correctly, the script converts Celestial Coordinates into Decimal Degrees:
* Right Ascension (RA): Converted from $H/M/S$ to degrees. 
    * Scientific Logic: Since the Earth rotates 360° in 24 hours, 1 hour of RA = 15°. The formula used is: deg = (h + m/60 + s/3600) * 15$.
* Declination (Dec): Converted from D/M/S to degrees, with specific handling for Unicode minus signs (− vs -) to ensure mathematical accuracy in the Southern celestial hemisphere.

2. Robust Data Extraction
* RegEx Parsing: Utilizes the `re` module to "slice" complex string patterns returned by the API (e.g., `05h 55m 10.3s`).
* API Management: Integrated with API Ninjas - Stars API to fetch real-time stellar magnitudes and positions.

3. Security & Best Practices
* Environment Variables: Uses `python-dotenv` to keep API keys secure and out of the public source code.
* Data Visualization: Implemented with `Matplotlib`, featuring a dark-sky theme, coordinate axis inversion (to match astronomical standards), and selective annotation for primary stars (Betelgeuse, Rigel, etc.).

⚙️ Installation & Setup

1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/orion-constellation-mapper.git](https://github.com/yourusername/orion-constellation-mapper.git)
   cd orion-constellation-mapper