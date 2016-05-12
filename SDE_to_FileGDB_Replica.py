# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# File: SDE_to_FileGDB_Replica.py
# Created on: 05/12/2016
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
#
# Credit: Patrick McKinney, pnmcartography@gmail.com
# ---------------------------------------------------------------------------

# Import system modules
import arcpy
import os, sys, time, datetime, traceback, string

# Time stamp variables
currentTime = datetime.datetime.now()
arg1 = currentTime.strftime("%H-%M")
arg2 = currentTime.strftime("%Y-%m-%d %H:%M")

# Create text file for logging results of script
# Change this to a valid file path
file = r'\\path\to\file\\NameofReport_%s.txt' % arg1

# Open text file and log results of script
report = open(file,'w')

# Try to run Replication
try:
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

    finishtime = time.clock()
    elapsedtime = finishtime - starttime

    # write result messages to log
    while result.status < 4:
        time.sleep(0.2)
    resultValue = result.getMessages()
    report.write ("completed " + str(resultValue) + "\n \n")

    # Write message to log
    report.write("Successfully ran replication from " + sde + " to " + child_gdb + " in " + str(elapsedtime) + " sec on " + arg2)
    # Print message to Python console if running through Python interpreter
    print "Successfully ran replication from " + sde + " to " + child_gdb + " in " + str(elapsedtime) + " sec on " + arg2

except Exception, e:
    # If an error occurred, write line number and error message to log
    tb = sys.exc_info()[2]
    report.write("Failed at step 1 \n" "Line %i" % tb.tb_lineno)
    report.write(e.message)

# close log file
report.close()