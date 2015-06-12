# Name: gpx_to_polyline.py
# Description: Converts GPX file into a polyline feature
# Feature class can be a shapefile or geodatabase feature class
# Created by: Patrick McKinney, Cumberland County GIS
# Contact: pnmcartography@gmail.com
# "Telling the stories of our world through the power of maps"

# Import system models
import arcpy

# Define parameter variables for use in ArcGIS toolbox script
inputGPX = arcpy.GetParameterAsText(0)
outputFeatureClass = arcpy.GetParameterAsText(1)

# Convert the GPX file into in_memory features
arcpy.GPXtoFeatures_conversion(inputGPX, 'in_memory\gpx_layer')

# Add message that GPX file has been succesfully converted to layer in Geoprocessing window
arcpy.AddMessage("GPX file converted to feature class")

# Convert the tracks into lines.
arcpy.PointsToLine_management('in_memory\gpx_layer', outputFeatureClass)

# Add message that Polyline feature has been created in Geoprocessing window
arcpy.AddMessage("GPX file converted to polyline feature class")
