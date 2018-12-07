# Name: Create Point Feature Class from CSV File
# Description: Create a feature class from a CSV file containing latitude, longitude,
# and attributes for a layer.  Script creates a empty feature class, add fields to
# the feature class, and then loops through a CSV file to add records to the feature class
# Created by: Patrick McKinney, Cumberland County GIS
# Contact: pnmcartography@gmail.com
# "Telling the stories of our world through the power of maps"
# Updated on: 12/7/2018
##############################################################################################

# Import the arcpy module and set the current workspace
import arcpy, sys

try:
    arcpy.env.workspace = r"enter file path within quotes"

    # Create a variable to hold the spatial reference for the feature class
    # Place WKID (well-know ID) within ()
    # Geographic Coordinate System reference: http://resources.arcgis.com/en/help/arcgis-rest-api/index.html#/Geographic_coordinate_systems/02r300000105000000/
    # Projected Coordinate System reference: http://resources.arcgis.com/en/help/arcgis-rest-api/index.html#/Projected_coordinate_systems/02r3000000vt000000/
    sr = arcpy.SpatialReference()

    # Create a new feature class
    # Options for "GEOMETRY TYPE" are "POINT", "MULTIPOINT", "POLYGON", or "POLYLINE"
    # This script is developed to create a Point feature class
    arcpy.CreateFeatureclass_management(arcpy.env.workspace, "Name of Feature Class", "GEOMETRY TYPE", spatial_reference = sr)

    # Add a Field to the feature class
    # Repeat this code block for as many fields are as needed
    # Field types can be "TEXT", "FLOAT", "DOUbLE", "SHORT", "LONG", "DATE", "BLOB", "RASTER", or "GUID"
    arcpy.AddField_management("Name of Feature Class", "Field Name", "Field Type")


    # Create a list holding field names from Feature Class
    iflds = ["SHAPE@XY", "Field Name", "Field Name"]

    # Create an arcpy.da.InsertCursor for Feature Class
    # iflds is the fields to edit through the insert cursor
    iCur = arcpy.da.InsertCursor("Name of Feature Class", iflds)

    # Open CSV file containing information to create feature class from.
    # Loop through each record in CSV file and add information into Feature Class.
    # Loop uses "if count > 1" because it is assumed the first row in the CSV file
    # will contain the field titles
    count = 1

    # Make sure to place the corresponding number for each field from the CSV file within the []
    for ln in open(r"File path to csv file", 'r').readlines():
        lnstrip = ln.strip()
        if count > 1:
            dataList = ln.split(",")
            # Number in array containing Latitude
            lat = dataList[1]
            # Number in array containing longitude
            lon = dataList[2]
            # Create variables for each field in CSV file. Use corresponding array number from CSV file
            var = dataList[0]
            # float() is used to convert string to a numberic field
            # include all variables from above, seperated by commas
            ivals = [(float(lon), float(lat)), var]
            iCur.insertRow(ivals)
        count += 1

    # Delete the cursor to close the cursor and release the exclusive lock
    del iCur

    print "Script completed"
# If an error occurs running geoprocessing tool(s) capture error and write message
# handle error outside of Python system
except EnvironmentError as e:
    tbE = sys.exc_info()[2]
    # Print the line number the error occured
    print("Failed at Line {}\n".format(tbE.tb_lineno))
    # Print the error message
    print("Error: {}".format(str(e)))
# handle exception error
except Exception as e:
    # Store information about the error
    tbE = sys.exc_info()[2]
    # Print the line number the error occured
    print("Failed at Line {}\n".format(tbE.tb_lineno))
    # Print the error message
    print("Error: {}".format(e.message))