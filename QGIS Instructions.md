## Purpose of Continuing Project in QGIS
Although this project could be continued in python, I prefer to use a mapping tool such as ArcGIS or QGIS for the final product. QGIS is a free, open source platform, so that is what I am using for this project. 

## Steps in QGIS
1. Install QuickMapServices </br>
If you have not installed QuickMapServices to QGIS, install it via Plugins. For my map, I added the ESRI Standard map. 

2. Import Data and Set CRS </br>
For this project, you will need the Illinois Shapefile included in this repository and the two outputs, one csv and one geojson. The shapefile and geojson can be dragged to the layer from the browser. The csv needs to be imported via "add a delimited layer". After all layers are imported, check to make sure that everything is in the same CRS if it is not already. 

3. Dissolve Shapefile </br>
While the shapefile layer is selected, navigate to the tool "Select Features by Area or Single Click" and then select all of the census tracts shown. While those are all selected, navigate to the Dissolve tool in the vector geoprocessing tools. In this tool, you need to check the box "Selected features only" under the input layer. Next, press Run and the layer should show up in the layers panel once the tool has run. 

4. Dissolve Shapefile to County Level </br>
To add the county outlines to the map, repeat the same process with the dissolve tool outlined above but you will need to select the census tracts corresponding to the county. This will have to be repeated three times until you have a layer for each county. 

5. Clip Merged Isochrone (Optional) </br>
If you would only like to see the drive time in the three counties, you can clip the merged isochrone using the dissolved census tract layer. To do this, you will need to navigate to the vector geoprocessing tools and select clip. Next, the input layer would be the merged isochrone and the overlay layer would be the dissolved census tract.

7. Create Map </br>
Before creating the map, make sure that you have the correct layers selected in the correct layer order: Childcare Location, clipped drive time isochrone, all three dissolved counties, and dissolved census tract. Additionally, make all formatting changes here before creating the map. The elements that should be displayed on the map will depend on the goal you have for your final output. For this one, I stuck with a simple map to just display the drive time isochrones. 
