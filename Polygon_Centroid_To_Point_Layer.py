# ---------------------------------------------------------------------------
# Name: Create Point Feature Class from Polygon Feature Class
#
# Description: This script allows you to create a point feature class from
#              a polygon feature class using the centroid of the polygon
#               feature class.  This mimics the behavior of the Feature To Point
#               geoprocessing tool (http://pro.arcgis.com/en/pro-app/tool-reference/data-management/feature-to-point.htm).
#               As this tool requires a ArcGIS Desktop Advanced license, this
#               script provides a work around for lower license installs of ArcGIS Desktop.
#
# Author: Patrick McKinney, Cumberland County GIS
#
# Created on: 7/23/2018
#
# Updated on: 12/7/2018
#
# Disclaimer: CUMBERLAND COUNTY ASSUMES NO LIABILITY ARISING FROM USE OF THESE MAPS OR DATA. THE MAPS AND DATA ARE PROVIDED WITHOUT
# WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE.
# Furthermore, Cumberland County assumes no liability for any errors, omissions, or inaccuracies in the information provided regardless
# of the cause of such, or for any decision made, action taken, or action not taken by the user in reliance upon any maps or data provided
# herein. The user assumes the risk that the information may not be accurate.
# ---------------------------------------------------------------------------

# Import system modules
import arcpy, sys, time, datetime, os

# Run geoprocessing tool.
# If there is an error with the tool, it will break and run the code within the except statement
try:
    # Time stamp variables
    current_time = datetime.datetime.now()
    # Date formatted as month-day-year (1-1-2017)
    date_today = current_time.strftime("%m-%d-%Y")
    # Date formated as month-day-year-hours-minutes-seconds
    date_today_time = current_time.strftime("%m-%d-%Y-%H-%M-%S")

    # If you want to overwrite an existing feature class, uncomment this line
    # arcpy.env.overwriteOutput = True

    # Create text file for logging results of script
    # Update file path with your parameters
    # Each time the script runs, it creates a new text file with the date_today variable as part of the file name
    # The example would be Polygon_To_Point_FC_1-1-2017.txt
    log_file = r'C:\GIS\Results\Polygon_To_Point_FC_{}.txt'.format(date_today)
    # variable to store messages for log file. Messages written in finally statement at end of script
    log_msg = ''
    # Get the start time of the geoprocessing tool(s)
    start_time = time.clock()

    # 1. Copy data for features from polygon layer to a list
    # list to contain data for each record
    features_list = []
    # Polygon Layer
    # update to your polygon layer
    polygon_layer = r'C:\GIS\Geodata.gdb\Polygon_Layer'
    # fields from polygon layer
    # include any fields from polygon layer you want within the point layer
    # 'SHAPE@TRUECENTROID' gives us the x,y coordinates to use for the point layer
    polygon_fields = ['SHAPE@TRUECENTROID', 'NAME', 'FACILITY_ID', 'ADDRESS']

    # Create a Search Cursor to loop through the polygon feature class and copy
    # each record to the features_list variable
    with arcpy.da.SearchCursor(polygon_layer,polygon_fields) as cursor:
        for row in cursor:
            # append item to features_list
            featuresList.append([row[0],row[1],row[2],row[3]])
        # end for
    # end with

    # write messages to text file
    # update message as desired
    log_msg += 'Completed copying features from polygon layer to list container\n'

    # 2. Create a shell feature class for point layer
    # name of feature class
    fc_name = 'Point_Layer'
    # location of feature class
    output_location = r'C:\GIS\Geodata.gdb'
    # projected or geographic coordinate system for feature class
    sr = arcpy.SpatialReference(0000)

    # create feature class
    arcpy.CreateFeatureclass_management(output_location,fc_name,'POINT',spatial_reference=sr)
    # add message
     # update message as desired
    log_msg += '\nCreated empty feature class for Points Layer\n'

    # 3. Add fields to Point layer
    # These fields should match the fields from the polygon_fields variable with the
    # exception of the 'SHAPE@TRUECENTROID' field
    # point layer created in step #2
    point_layer = os.path.join(output_location,fc_name)

    # Create PIN field
    arcpy.AddField_management(point_layer,'NAME','TEXT')
    # add message
    log_msg += '\nAdded NAME field\n'

    # Create location field
    arcpy.AddField_management(addPts,'FACILITY_ID','SHORT')
    # add message
    log_msg += '\nAdded FACILITY_ID field\n'

    # create City field
    arcpy.AddField_management(addPts,'ADDRESS','TEXT')
    # add message
    log_msg += '\nAdded ADDRESS field\n'

    # 4. Loop through features_list and add records to Point layer
    # Point layer fields
    # 'SHAPE@XY' defines where the point is located
    # the other fields should match what was created in step #3 and the fields from the polygon layer
    point_fields = ['SHAPE@XY', 'NAME', 'FACILITY_ID', 'ADDRESS']

    # Create an Insert Cursor on the Point layer and add records from features_list
    with arcpy.da.InsertCursor(point_layer,point_fields) as cursor:
        for record in features_list:
            cursor.insertRow(record)
        # end for
    # end with

    # Get the end time of the geoprocessing tool(s)
    finish_time = time.clock()
    # Get the total time to run the geoprocessing tool(s)
    elapsed_time_seconds = finish_time - start_time
    # convert elapsed time to minutes
    elapsed_time_minutes = round((elapsed_time_seconds / 60),2)

    # add message
    log_msg += '\nCompleted adding records to points layer\n'
    log_msg += '\nCompleted script in {} seconds on {}'.format(elapsed_time_seconds,date_today)
    # of if you want minutes, use this line instead
    log_msg += '\nCompleted script in {} minutes on {}'.format(elapsed_time_minutes,date_today)
# If an error occurs running geoprocessing tool(s) capture error and write message
# handle error outside of Python system
except EnvironmentError as e:
    tbE = sys.exc_info()[2]
    # add the line number the error occured to the log message
    log_msg += "\nFailed at Line {}\n".format(tbE.tb_lineno)
    # add the error message to the log message
    log_msg += "\nError: {}\n".format(str(e))
# handle exception error
except Exception as e:
    # Store information about the error
    tbE = sys.exc_info()[2]
    # add the line number the error occured to the log message
    log_msg += "\nFailed at Line {}\n".format(tbE.tb_lineno)
    # add the error message to the log message
    log_msg += "\nError: {}\n".format(e.message)
finally:
    try:
        # delete cursor
        del cursor
    except:
        pass
    # write message to log file
    try:
        with open(log_file, 'w') as f:
            f.write(str(log_msg))
    except:
        print 'an error occured writing results to text file'