#-------------------------------------------------------------------------------
# Name:        Print Errors Helper Module
#
# Purpose:     Writes error messages that are returned from function.
#              Messages can be written to log file or printed in the console.
#
# Author:      Patrick McKinney, Cumberland County, Pennsylvania
#
# Created:     08/22/2019
# Copyright:   (c) pmckinney 2019
# Disclaimer: CUMBERLAND COUNTY ASSUMES NO LIABILITY ARISING FROM USE OF THESE MAPS OR DATA. THE MAPS AND DATA ARE PROVIDED WITHOUT
# WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE.
# Furthermore, Cumberland County assumes no liability for any errors, omissions, or inaccuracies in the information provided regardless
# of the cause of such, or for any decision made, action taken, or action not taken by the user in reliance upon any maps or data provided
# herein. The user assumes the risk that the information may not be accurate.
#-------------------------------------------------------------------------------

import sys
import linecache

# Function to handle errors
def print_exception(error):
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    # add message
    message = '\nError: {}\nFILE: {}, LINE: {}\n\n\t "{}": {}'.format(error, filename, lineno, line.strip(), exc_obj)
    # return to variable
    return message
# end PrintException