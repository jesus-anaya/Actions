from arcgis.gis import GIS
import datetime
import os

# --- 1. Connect to ArcGIS Online ---
gis = GIS("https://www.arcgis.com",
          os.getenv("AGOL_USERNAME"),
          os.getenv("AGOL_PASSWORD"))

# --- 2. Path or URL to your CSV file ---
csv_path = "https://geomatica.udemedellin.edu.co/proyectos/viirs_fire_latest.csv"

# --- 3. Create a title with timestamp to avoid duplicates ---
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
csv_title = f"VIIRS_Fire_Latest_{timestamp}"

# --- 4. Add the CSV file to AGOL as an item ---
csv_item = gis.content.add(
    {
        "title": csv_title,
        "type": "CSV",
        "tags": "fires, automation, update",
        "snippet": "Automatically created from CSV",
        "description": "VIIRS Fire Detections hosted layer created automatically from the latest CSV data."
    },
    data=csv_path
)

# --- 5. Publish the CSV as a hosted feature layer ---
flayer_item = csv_item.publish()

# --- 6. Optionally, share it publicly (uncomment if needed) ---
# flayer_item.share(everyone=True)

print(f"✅ Created new hosted feature layer: {flayer_item.title}")
print(f"🌐 Feature layer URL: {flayer_item.url}")
print(f"⏰ Created at: {datetime.datetime.now()}")
