from arcgis.gis import GIS
import datetime
import os

# --- 1. Connect to ArcGIS Online ---
gis = GIS("https://www.arcgis.com", 
          os.getenv("AGOL_USERNAME"), 
          os.getenv("AGOL_PASSWORD"))

# --- 2. Path to your CSV (download or use a local file) ---
csv_path = "https://geomatica.udemedellin.edu.co/proyectos/viirs_fire_latest.csv"  # Make sure it exists or downloaded before

# --- 3. ID of your existing hosted feature layer ---
feature_item_id = "efacb3d3a030466c9a88512069d5f8f2"  #this is the hosted layer id assigned by AGOL

# --- 4. Overwrite the data ---
feature_item = gis.content.get(feature_item_id)
feature_item.update(data=csv_path)

print(f"✅ Updated AGOL layer at {datetime.datetime.now()}")
