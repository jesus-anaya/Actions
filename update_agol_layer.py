from arcgis.gis import GIS
import datetime
import os

# --- 1. Connect to ArcGIS Online ---
gis = GIS("https://www.arcgis.com", 
          os.getenv("AGOL_USERNAME"), 
          os.getenv("AGOL_PASSWORD"))

# --- 2. Path to your CSV (download or use a local file) ---
csv_path = "https://geomatica.udemedellin.edu.co/proyectos/viirs_fire_latest.csv"  # Make sure it exists or downloaded before

# --- 3. Create a unique title (e.g. with date) ---
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
csv_title = f"Fire_Detections_{timestamp}"

# --- 4. Add the CSV as a new item in AGOL ---
csv_item = gis.content.add(
    {
        "title": csv_title,
        "type": "CSV",
        "tags": "fires,automation,update",
        "snippet": "Automated upload every 6 hours",
        "description": "CSV file automatically uploaded every 6 hours"
    },
    data=csv_path
)

print(f"✅ CSV uploaded to AGOL as item: {csv_item.title} (ID: {csv_item.id})")

# --- 5. ID of your existing hosted feature layer ---
feature_item_id = "efacb3d3a030466c9a88512069d5f8f2"  #this is the hosted layer id assigned by AGOL

# --- 6. Overwrite the data ---
feature_item = gis.content.get(feature_item_id)
feature_item.update(data=csv_path)

print(f"✅ Updated AGOL layer at {datetime.datetime.now()}")
