##### About
# Author: Regan Whitesell
# Date Created: 10/04/2024
# Last Updated: 10/05/2024


##### Import Libraries and Data
#Import libraries
import pandas as pd
import re
import requests
import time
import geopandas as gpd
from shapely.geometry import shape
from shapely.ops import unary_union

# Childcare Data
file_path_1 = INSERT_YOUR_FILE_PATH_HERE
MasonCO_File1 = pd.read_csv(file_path_1)

file_path_2 = INSERT_YOUR_FILE_PATH_HERE
TazewellCO_File1 = pd.read_csv(file_path_2)

file_path_3 = INSERT_YOUR_FILE_PATH_HERE
WoodfordCO_File1 = pd.read_csv(file_path_4)



##### Prep Data for Geocoding
# Concat df's
Counties_cc = pd.concat([MasonCO_File1, TazewellCO_File1, WoodfordCO_File1])

# Split ages
def split_age_ranges(age_range_str):
    if not isinstance(age_range_str, str):
        age_range_str = str(age_range_str)
    
    pattern = re.compile(r'(\d+\s*[A-Za-z]*)\s*TO\s*(\d+\s*[A-Za-z]*)')
    matches = pattern.findall(age_range_str)
    if matches:
        return matches[0]
    else:
        return (None, None)
Counties_cc[['Start_Age_Day', 'End_Age_Day']] = Counties_cc['DayAgeRange'].apply(lambda x: pd.Series(split_age_ranges(x)))
Counties_cc[['Start_Age_Night', 'End_Age_Night']] = Counties_cc['NightAgeRange'].apply(lambda x: pd.Series(split_age_ranges(x)))

# Prep addresses for geocoding
Counties_cc['State'] = "Illinois"
ChildcareData_v1 = Counties_cc[['ProviderID', 'Street', 'City', 'State', 'Zip']]
ChildcareData_v1['Addresses'] = ChildcareData_v1.apply(lambda row: f"{row['Street']}, {row['City']}, {row['State']}, {row['Zip']}", axis=1)
Childcare_ToGeocode = ChildcareData_v1[['Addresses']]



##### Geocode Addresses
geocoded_data = []
failed_addresses = []
api_key = 'INSERT_YOUR_CENSUS_API_KEY_HERE'
for address in Childcare_ToGeocode['Addresses']:
   url = f'https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address={address}&benchmark=Public_AR_Current&format=json&key={api_key}'
   try:
       response = requests.get(url)
       response.raise_for_status()
       data = response.json()
       if 'result' in data and 'addressMatches' in data['result'] and data['result']['addressMatches']:
           lat = data['result']['addressMatches'][0]['coordinates']['y']
           lon = data['result']['addressMatches'][0]['coordinates']['x']
           geocoded_data.append({'Input Address': address, 'Latitude': lat, 'Longitude': lon})
       else:
           failed_addresses.append(address)
   except Exception as e:
       print(f"Error for address: {address}, Exception: {e}")
       failed_addresses.append(address)

# Failed addresses
Failed_Geocode = pd.DataFrame(failed_addresses, columns=['Input Address'])

# Lookup addresses manually through another service to find latitude and longitude coordinates
Manual_Entry = {'Latitude': [INSERT_MANUAL_LATITUDE_VALUES_HERE],
                'Longitude': [INSERT_MANUAL_LONGITUDE_VALUES_HERE]}
Failed_Geocode_Coded = Failed_Geocode.assign(**Manual_Entry)

# Successful addresses
Successful_Geocode = pd.DataFrame(geocoded_data, columns=['Input Address', 'Latitude', 'Longitude'])

# concat geocoded addresses
geocoded_addr_complete = pd.concat([Successful_Geocode, Failed_Geocode_Coded])

# Add lat/long back to df
ChildcareLocations_G1 = pd.merge(ChildcareData_v1, geocoded_addr_complete, how='left', left_on='Addresses', right_on='Input Address')

# Location ref
ChildcareLocations_G1_ref = ChildcareLocations_G1[['ProviderID', 'Latitude', 'Longitude']]

# Add back
ChildcareLocations_PostGC = Counties_cc.merge(ChildcareLocations_G1_ref, how='left', on='ProviderID')



##### Create drive time isochrones
# Fetch isochrone data from OpenRouteService
def fetch_isochrones(api_key, locations, profile='driving-car', range_time=900, batch_size=20):
    isochrones = []
    url = f'https://api.openrouteservice.org/v2/isochrones/{profile}'
    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': api_key,
        'Content-Type': 'application/json; charset=utf-8'
    }

    for i, location in enumerate(locations):
        lon, lat = location
        body = {
            'locations': [[lon, lat]],  
            'range': [range_time] 
        }
        
        response = requests.post(url, json=body, headers=headers)
        
        if response.status_code == 200:
            isochrones.append(response.json())  # Collect the isochrone data
        else:
            print(f"Error fetching isochrone for location {location}: {response.status_code} - {response.reason}")
        
        # Batch size!! API limit is 20 per minute if using free service
        if (i + 1) % batch_size == 0:
            print(f"Processed {i + 1} requests, pausing for 60 seconds to comply with the rate limit...")
            time.sleep(60) 
    
    return isochrones

# Merge isochrones
def merge_isochrones(isochrones):
    polygons = []
    for isochrone in isochrones:
        for feature in isochrone['features']:
            polygons.append(shape(feature['geometry']))
    merged_polygon = unary_union(polygons)  # Merge the polygons into one
    return merged_polygon

api_key = 'INSERT_YOUR_OPENROUTE_API_KEY_HERE'
locations = ChildcareLocations_G1_ref[['Longitude', 'Latitude']].values.tolist()
isochrones = fetch_isochrones(api_key, locations)
merged_isochrone = merge_isochrones(isochrones)

# Create gdf
gdf = gpd.GeoDataFrame(geometry=[merged_isochrone], crs='EPSG:4326')

# Save as a GeoJSON for QGIS!
gdf.to_file('INSERT_YOUR_FILE_PATH_HERE.geojson', driver='GeoJSON')
