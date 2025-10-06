# to run from GITHUB, REPOSITORY CALLED "ACTIVE"
#Update portal url and web map id.

from arcgis.gis import GIS
import datetime
import os

# --- 1. Connect to ArcGIS Online ---
gis = GIS("https://umedellin.maps.arcgis.com",
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

print(f"✅ Created new hosted feature layer: {flayer_item.title}")
print(f"🌐 Feature layer URL: {flayer_item.url}")

# --- 6. Share the new layer publicly ---
flayer_item.share(everyone=True)
print("🌍 The hosted feature layer is now PUBLIC.")

# --- 7. Retrieve the layer for popup configuration ---
flayer = flayer_item.layers[0]

# Define a basic popup configuration
popup_info = {
    "title": "{Name}",  # Replace "Name" with a field from your CSV
    "fieldInfos": [
        {"fieldName": f.name, "label": f.alias, "visible": True}
        for f in flayer.properties.fields
    ],
    "description": "VIIRS Fire Detection Information",
    "showAttachments": False,
    "mediaInfos": []
}

# --- 8. Add the new hosted feature layer to an existing web map ---
# Replace this with your actual Web Map item ID from AGOL
webmap_id = "9ba7a6dcd4a743b3b4aa6b0dd4e005a1"

# Retrieve the web map
webmap_item = gis.content.get(webmap_id)
webmap_data = webmap_item.get_data()

# Define the new operational layer entry (with pop-up enabled)
new_layer = {
    "title": flayer_item.title,
    "url": flayer_item.url,
    "layerType": "ArcGISFeatureLayer",
    "visibility": True,
    "opacity": 1,
    "popupInfo": popup_info  # ✅ Enables popups
}

# Add the layer to the map
webmap_data["operationalLayers"].append(new_layer)

# Update the web map composition
webmap_item.update(data=webmap_data)

print(f"🗺️  Added layer '{flayer_item.title}' to web map '{webmap_item.title}' with popups enabled.")
print(f"⏰ Completed at: {datetime.datetime.now()}")
