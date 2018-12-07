# -----------------------------------------------------------------------------------------------------------------------------------------------------
# Name: Run Replication from SDE Enterprise Geodatabase to File Geodatabase
#
# Author: Patrick McKinney, Cumberland County GIS (pmckinney@ccpa.net or pnmcartography@gmail.com)
#
# Created on: 05/12/2016
#
# Updated on: 12/7/2018
#
# Description: Synchronizes updates between a parent and child replica geodatabase in favor of the parent.
# The parent geodatabase is a SDE enterprise geodatabase. The child is a file geodatabase
# The script can be added as a windows scheduled task to automate replication updates on a weekly basis, for example.
#
# Note: Originally developed by Cumberland County GIS to replicate data to various departments.
# You must update the following paramaters:
# 1. file path to the log file that reports whether the tool ran successfully or unsuccessfully.
# 2. SDE connection to parent geodatabase
# 3. file path to the child file geodatabase
# 4. name of the replication you are performing synchronize changes on
#
# Disclaimer: CUMBERLAND COUNTY ASSUMES NO LIABILITY ARISING FROM USE OF THESE MAPS OR DATA. THE MAPS AND DATA ARE PROVIDED WITHOUT
# WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE.
# Furthermore, Cumberland County assumes no liability for any errors, omissions, or inaccuracies in the information provided regardless
# of the cause of such, or for any decision made, action taken, or action not taken by the user in reliance upon any maps or data provided
# herein. The user assumes the risk that the information may not be accurate.
# ---------------------------------------------------------------------------------------------------------------------------------------------------

# Import system modules
import arcpy, sys, time, datetime

# Try to run Replication
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

    # get time stamp for start of tool
    starttime = time.clock()

    # SDE is parent geodatabase in replication
    # Change this to your SDE connection
    sde = r"SDE Connection"
    # Child file geodatabase in replication
    # Change this to your file geodatabase
    child_gdb = r"\\path\to\file.gdb"

    # Process: Synchronize Changes
    # Replicates data from parent to child geodatabase
    # update the name of the replication
    result = arcpy.SynchronizeChanges_management(sde, "Name of Replication", child_gdb, "FROM_GEODATABASE1_TO_2", "IN_FAVOR_OF_GDB1", "BY_OBJECT", "DO_NOT_RECONCILE")

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
    # add the tool's message to the log message
    logMsg += "completed {}\n".format(str(resultValue))
    # add a more human readable message to log message
    logMsg += "\nSuccessfully ran replication from {} to {} in {} seconds on {}\n".format(sde, child_gdb, str(elapsedtime), dateToday)
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