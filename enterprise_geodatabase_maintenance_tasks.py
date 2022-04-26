# Performs 'Analyze Datasets' > 'Rebuild Indexes' > 'Compress'
# > 'Analyze Datasets' > 'Rebuild Indexes' geoprocessing tools
# on an enterprise (sde) geodatabase
# connections to the database are closed, and all users are disconnected
# before running tools.  database connections are opened at the end

# import modules
import arcpy
import os
import sys
import datetime
import time

# capture the date the script is being run
date_today = datetime.date.today()
# convert date format to month-day-year (1-1-2020)
formatted_date_today = date_today.strftime("%m-%d-%Y")
# placeholder for messages for text file
log_message = ''
# text file to write messages to
# TODO: update path
log_file = r'C:\GIS\Results\Database_Maint_Report_{}.txt'.format(date_today)

try:
    # database connection
    # TODO: update path for sde connection
    dbase = r"SDE Connection"
    # set workspace to geodatabase
    arcpy.env.workspace = dbase
    # get list of all:
    # > feature classes
    feature_classes = arcpy.ListFeatureClasses()
    # > tables
    tables = arcpy.ListTables()
    # list of data to run tools on
    data_list = feature_classes + tables
    # Next, for feature datasets get all of the datasets and featureclasses
    # from the list and add them to the master list.
    for dataset in arcpy.ListDatasets("", "Feature"):
        arcpy.env.workspace = os.path.join(dbase, dataset)
        data_list += arcpy.ListFeatureClasses() + arcpy.ListDatasets()
    # add message
    log_message += '{} : Created list of feature classes and tables in geodatabase\n'.format(time.strftime('%I:%M%p'))

    # close database from accepting connections
    arcpy.AcceptConnections(dbase, False)
    # remove existing users
    arcpy.DisconnectUser(dbase, 'ALL')
    # add message
    log_message += '\n{} : Disconnected users and closed connections to the geodatabase\n'.format(time.strftime('%I:%M%p'))

    # run analyze datasets
    arcpy.AnalyzeDatasets_management(dbase, 'SYSTEM', data_list, 'ANALYZE_BASE', 'ANALYZE_DELTA', 'ANALYZE_ARCHIVE')
    # add message
    log_message += '\n{} : Ran "Analyze Datasets" tool\n'.format(time.strftime('%I:%M%p'))

    # run rebuild indexes
    arcpy.RebuildIndexes_management(dbase, 'SYSTEM', data_list, 'ALL')
    # add message
    log_message += '\n{} : Ran "Rebuild Indexes" tool\n'.format(time.strftime('%I:%M%p'))

    # run compress
    arcpy.Compress_management(dbase)
     # add message
    log_message += '\n{} : Ran "Compress" tool\n'.format(time.strftime('%I:%M%p'))

    # run analyze datasets
    arcpy.AnalyzeDatasets_management(dbase, 'SYSTEM', data_list, 'ANALYZE_BASE', 'ANALYZE_DELTA', 'ANALYZE_ARCHIVE')
    # add message
    log_message += '\n{} : Ran "Analyze Datasets" tool\n'.format(time.strftime('%I:%M%p'))

    # run rebuild indexes
    arcpy.RebuildIndexes_management(dbase, 'SYSTEM', data_list, 'ALL')
     # add message
    log_message += '\n{} : Ran "Rebuild Indexes" tool\n'.format(time.strftime('%I:%M%p'))

    # allow database to accept connections
    arcpy.AcceptConnections(dbase, True)
# If an error occurs running geoprocessing tool(s) capture error and write message
except (Exception, EnvironmentError) as e:
    tbE = sys.exc_info()[2]
    # Write the line number the error occured to the log file
    log_message += "\nFailed at Line {}\n".format(tbE.tb_lineno)
    # Write the error message to the log file
    log_message += "Error: {}".format(str(e))
finally:
    # write message to log file
    try:
        # allow database to accept connections
        arcpy.AcceptConnections(dbase, True)
         # add message
        log_message += '\n{} : Opened connections to the geodatabase\n'.format(time.strftime('%I:%M%p'))
        # write messages to text file
        with open(log_file, 'w') as f:
            f.write(str(log_message))
    except:
        pass