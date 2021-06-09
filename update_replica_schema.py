#------------------------------------------------------------------
# Name:        Update Schema for Child Replication Geodatabases
#
# Purpose:     Exports replication schema from parent enterprise geodatabase,
#              and compares changes with child geodatabases.  Imports changes
#              into child geodatabases.
#
#              Data schemas change from time to time.  Use this script to help
#              automate incorporating those changes into child geodatabases
#              particpating in parent-to-child replication.
#
# Author:      Patrick McKinney, Cumberland County GIS
#
# Created:     5/11/2021
#
# Updated:     5/27/2021
#
# Copyright:   (c) Cumberland County 2021
#
# Disclaimer: CUMBERLAND COUNTY ASSUMES NO LIABILITY ARISING FROM USE OF THESE MAPS OR DATA. THE MAPS AND DATA ARE PROVIDED WITHOUT
# WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE.
# Furthermore, Cumberland County assumes no liability for any errors, omissions, or inaccuracies in the information provided regardless
# of the cause of such, or for any decision made, action taken, or action not taken by the user in reliance upon any maps or data provided
# herein. The user assumes the risk that the information may not be accurate.
#-----------------------------------------------------------------

# note the imported "print_errors" helper module that is located within this "ArcPy" repo
# Import system modules
import arcpy
import os
import sys
import time
import datetime
import print_errors

try:
    # Get the start time of the geoprocessing tool(s)
    start_time = time.clock()

    # Time stamp variables
    date_today = datetime.date.today()
    # Date formatted as month-day-year (1-1-2017)
    # used in creating log file
    formatted_date_today = date_today.strftime("%m-%d-%Y")
    # date formatted as MonthDayYear (01012017)
    # used in creating directory to store schema xml files in
    folder_formatted_date_today = date_today.strftime("%m%d%Y")

    # variable to store messages for log file. Messages written in finally statement at end of script
    log_message = ''
    # Create text file for logging results of script
    log_file = r'\Path\To\Directory\Update Schema Report {}.txt'.format(formatted_date_today)

    # root directory for schema change files
    # each time this script is run, a sub-directory with the current date will be created
    # replication compare xml files will be created in sub-directory
    base_dir = r'\Path\To\Directory'
    # directory to store schema change files
    out_dir = os.path.join(base_dir, folder_formatted_date_today)
    # create directory
    os.mkdir(out_dir)
    # add message
    log_message += 'Created output directory for schema changes at {}\n'.format(out_dir)

    # parent enterprise geodatabase in replication
    sde_ccgis = r"\Path\To\SDE Connection File\geodatabase.sde"

    # list of dictionaries containing data for each replica you want to update schema for
    # name = human friendly name for replica; used in log file messages
    # geodatabase = path to the child geodatabase participating in replica
    # child_output = output xml file generated when comparing parent geodatabase to child geodatabase
    # replica_changes = output xml file that is imported into child geodatabase to bring in schema changes from parent geodatabase
    replication_data = [
        {
            "name": "Planning Department",
            "geodatabase": r"\Path\To\Geodatabase\Geodata.gdb",
            "replica": "SDE.Planning_Replica",
            "child_output": r"{}\planning_schema_export.xml".format(out_dir),
            "replica_changes": r"{}\planning_schema_changes.xml".format(out_dir)
        },
        {
            "name": "Public Works",
            "geodatabase": r"\Path\To\Geodatabase\Geodata.gdb",
            "replica": "SDE.PublicWorks_Replica",
            "child_output": r"{}\public_works_schema_export.xml".format(out_dir),
            "replica_changes": r"{}\public_works_schema_changes.xml".format(out_dir)
        }
    ]

    # loop through list of replications and update schema
    for replica in replication_data:
        try:
            # add message
            log_message += '\nRunning schema update process for {}\n'.format(replica["name"])
            # export schema from parent geodatabase
            arcpy.ExportReplicaSchema_management(sde_ccgis, replica["child_output"], replica["replica"])
            # add message
            log_message += '\n\tExported schema for CCGIS geodatabase\n'
            # create compare file between parent and child
            arcpy.CompareReplicaSchema_management(replica["geodatabase"], replica["child_output"], replica["replica_changes"])
            # add message
            log_message += '\n\tCompared changes to child geodatabase\n'
            # import schema compare file into child geodatabase
            arcpy.ImportReplicaSchema_management(replica["geodatabase"], replica["replica_changes"])
            # add message
            log_message += '\n\tImported changes into child geodatabase\n'
        except EnvironmentError as e:
            log_message += '\nError running {} replication\n'.format(replica["name"])
            log_message += print_errors.print_exception(e)
        except Exception as e:
            log_message += '\nError running {} replication\n'.format(replica["name"])
            log_message += print_errors.print_exception(e)
    # end for loop

    # Get the end time of the geoprocessing tool(s)
    finish_time = time.clock()
    # Get the total time to run the geoprocessing tool(s)
    elapsed_time = finish_time - start_time
    # total time in minutes
    elapsed_time_minutes =  round((elapsed_time / 60), 2)

    # Write message to a log file
    log_message += "\nSuccessfully updated replication schemas for departments in {}-minutes on {}\n".format(elapsed_time_minutes,formatted_date_today)
# If an error occurs running geoprocessing tool(s) capture error and write message
# handle error outside of Python system
except EnvironmentError as e:
    tbE = sys.exc_info()[2]
    # Write the line number the error occured to the log file
    log_message += "\nFailed at Line {}\n".format(tbE.tb_lineno)
    # Write the error message to the log file
    log_message += "Error: {}".format(str(e))
except Exception as e:
    # If an error occurred, write line number and error message to log
    tb = sys.exc_info()[2]
    log_message += "\nFailed at Line {}\n".format(tb.tb_lineno)
    log_message += "Error: {}".format(e)
finally:
    # write message to log file
    try:
        with open(log_file, 'w') as f:
            f.write(str(log_message))
    except:
        pass