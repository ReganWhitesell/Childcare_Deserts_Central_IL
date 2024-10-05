# Childcare Deserts in Central Illinois README
## What This Project Does
This project geocodes childcare locations and generates drive time isochrones using open source geospatial analytic tools to predict and identify childcare deserts in central Illinois. In this project, a childcare desert is defined as any area that is not within a 15 minute drive to a childcare location. This definition helps to highlight regions where families may lack access to childcare services, potentially impacting their ability to find care for their children. 

## Why The Project Is Useful
This project may be useful for predicting the accessibility of childcare in areas where licensed childcare locations are publicly provided. In this example, I focused on three counties in central Illinois, but it could be replicated with any data as long as there are addresses to geocode. Additionally, this code can be changed to create a shorter or longer drive time isochrones or to switch the mode of transportation. 

## Accessing Data
The Illinois Department of Children and Family Services provides the locations of all childcare facilities licensed with the state: https://sunshine.dcfs.illinois.gov/Content/Licensing/Daycare/ProviderLookup.aspx. For this project, I pulled data separately for the following counties: Mason County, Tazewell County, and Woodford County. Please note, with a larger dataset, there will be more addresses that do not geocode that you will have to manually search and input their latitude and longitude into the dataframe. 

## How to Install and Setup Project
In order to install and run this project, you will need Python and QGIS in addition to API keys from the Census Bureau (https://api.census.gov/data/key_signup.html) and OpenRouteService (https://openrouteservice.org/). For the python script, you will need to install the packages that are in the import statements at the beginning of the script if you do not already have them installed in your environment. Additionally, for QGIS, I installed QuickMapServices for the basemap. 

## Replace in Python Code
The following lines will need to be changed in the python code in order for you to run it. Everything that needs to be replaced includes file paths, API keys, and latitude and longitude coordinates for failed geocoded addresses. 
| Line Number | Replace | Insert |
| --------------- | --------------- | --------------- |
| Line 19 | INSERT_YOUR_FILE_PATH_HERE | Insert your file path for Mason County. |
| Line 22 | INSERT_YOUR_FILE_PATH_HERE | Insert your file path for Tazewell County. |
| Line 25 | INSERT_YOUR_FILE_PATH_HERE | Insert your file path for Woodford County. |
| Line 59 | INSERT_YOUR_CENSUS_API_KEY_HERE | Insert your API key from the census bureau. |
| Line 80 | INSERT_MANUAL_LATITUDE_VALUES_HERE | Insert latitude values for the failed geocoded addresses. |
| Line 81 | INSERT_MANUAL_LONGITUDE_VALUES_HERE | Insert longitude values for the failed geocoded addresses. |
| Line 99 | INSERT_YOUR_FILE_PATH_HERE | Insert your file path to save the childcare location data with latitude and longitude coordinates as a csv. | 
| Line 143 | INSERT_YOUR_OPENROUTE_API_KEY_HERE | Insert your API key from OpenRouteService. |
| Line 152 | INSERT_YOUR_FILE_PATH_HERE | Insert the file path you would like the geojson to save to. |
