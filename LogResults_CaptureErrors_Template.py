# ---------------------------------------------------------------------------
# Name: Template ArcPy Script for Writing Messages to Text File
#
# Author: Patrick McKinney, Cumberland County GIS (pmckinney@ccpa.net or pnmcartography@gmail.com)
#
# Created on: 01/06/2017
#
# Updated on: 12/7/2018
#
# Description: This is a template script for running ArcGIS geoprocessing tool(s).
# It is ideally suited for scripts that run as Windows scheduled tasks.
# The script writes success or error messages in a text file.
# You must update the path and name of the text file.
# The ArcPy geoprocessing code goes in at line 39.
#
# Disclaimer: CUMBERLAND COUNTY ASSUMES NO LIABILITY ARISING FROM USE OF THESE MAPS OR DATA. THE MAPS AND DATA ARE PROVIDED WITHOUT
# WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE.
# Furthermore, Cumberland County assumes no liability for any errors, omissions, or inaccuracies in the information provided regardless
# of the cause of such, or for any decision made, action taken, or action not taken by the user in reliance upon any maps or data provided
# herein. The user assumes the risk that the information may not be accurate.
# ---------------------------------------------------------------------------

# Import system modules
import arcpy, sys, time, datetime

# Run geoprocessing tool.
# If there is an error with the tool, it will break and run the code within the except statement
try:
    # Time stamp variables
    currentTime = datetime.datetime.now()
    # Date formatted as month-day-year (1-1-2017)
    dateToday = currentTime.strftime("%m-%d-%Y")
    # Date formated as month-day-year-hours-minutes-seconds
    dateTodayTime = currentTime.strftime("%m-%d-%Y-%H-%M-%S")

    # Create text file for logging results of script
    # Update file path with your parameters
    # Each time the script runs, it creates a new text file with the date1 variable as part of the file name
    # The example would be GeoprocessingReport_1-1-2017
    logFile = r'C:\GIS\Results\GeoprocessingReport_{}.txt'.format(dateToday)

    # variable to store messages for log file. Messages written in finally statement at end of script
    logMsg = ''

    # Get the start time of the geoprocessing tool(s)
    starttime = time.clock()

    # Put ArcPy geoprocessing code within this section
    result # = arcpy command with appropriate parameters

    # Get the end time of the geoprocessing tool(s)
    finishtime = time.clock()
    # Get the total time to run the geoprocessing tool(s)
    elapsedtime = finishtime - starttime

    # write result messages to log
    # delay writing results until geoprocessing tool gets the completed code
    while result.status < 4:
        time.sleep(0.2)
    # store tool result message in a variable
    resultValue = result.getMessages()
    # add the tool's message to the log file message
    logMsg += "completed {}\n".format(str(resultValue))
    # add a more human readable message to log message
    logMsg += "\nSuccessfully ran the geoprocessing tool in {} seconds on {}\n".format(str(elapsedtime), dateToday)
# If an error occurs running geoprocessing tool(s) capture error and write message
# handle error outside of Python system
except EnvironmentError as e:
    tbE = sys.exc_info()[2]
    # add the line number the error occured to the log message
    logMsg += "\nFailed at Line {}\n".format(tbE.tb_lineno)
    # add the error message to the log message
    logMsg += "\nError: {}\n".format(str(e))
# handle exception error
except Exception as e:
    # Store information about the error
    tbE = sys.exc_info()[2]
    # add the line number the error occured to the log message
    logMsg += "\nFailed at Line {}\n".format(tbE.tb_lineno)
    # add the error message to the log message
    logMsg += "\nError: {}\n".format(e.message)
finally:
    # write message to log file
    try:
        with open(logFile, 'w') as f:
            f.write(str(logMsg))
    except:
        pass