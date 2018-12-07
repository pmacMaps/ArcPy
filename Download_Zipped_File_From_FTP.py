# ---------------------------------------------------------------------------
# Name: Download Zipped File from FTP Site
#
# Author: Patrick McKinney, Cumberland County GIS (pmckinney@ccpa.net or pnmcartography@gmail.com)
#
# Created on: 01/2018
#
# Updated on: 12/7/2018
#
# Description: This is a template script for downloading a file from an FTP site
# to a local or network drive.  Results and error messages are written to a text file.
#
# Disclaimer: CUMBERLAND COUNTY ASSUMES NO LIABILITY ARISING FROM USE OF THESE MAPS OR DATA. THE MAPS AND DATA ARE PROVIDED WITHOUT
# WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE.
# Furthermore, Cumberland County assumes no liability for any errors, omissions, or inaccuracies in the information provided regardless
# of the cause of such, or for any decision made, action taken, or action not taken by the user in reliance upon any maps or data provided
# herein. The user assumes the risk that the information may not be accurate.
# ---------------------------------------------------------------------------

# Import modules
import sys, os, datetime, time, zipfile, ftplib

# Writes messages to a text file
def message(message):
    time_stamp = time.strftime("%b %d %Y %H:%M:%S")
    placeholder = '\n{}  {}\n'.format(time_stamp,message)
    return placeholder
# end message()

try:
    # Get current date and time
    currentTime = datetime.datetime.now()
    # Format date as Year-Month-Day (2017-01-17
    dateToday = currentTime.strftime("%Y-%m-%d")

    # container for messages for log file
    log_text = ''
    # path and name of text file to store log messages
    # sample: r'C:\Scripts\File Transfer\Download Geodatabase Results {}.txt'.format(dateToday)
    log_file = ''

    # Variables
    # ftp server
    ftp_server = ""
    # user name for FTP
    username = ''
    # password for FTP
    password = ''
    # location to save file
    # change this to the directory you want to save the file to
    # sample: r'C:\GIS Data\'
    localDir = ''
    # zipped file on FTP you are downloading
    zippedFileToDownload = 'Name_Of_File.zip'

    # Download file from FTP site
    # open ftp connection
    ftp = ftplib.FTP(ftp_server)
    print 'Established FTP connection'
    log_text += message('Established FTP connection')
    # login to ftp
    ftp.login(username, password)
    print 'Logged into FTP'
    log_text += message('Logged into FTP')
    # change directory to desired directory
    ftp.cwd('SomeDirectory')
    # get current ftp directory
    ftpDir = ftp.pwd()
    print 'Changed directories to {}'.format(ftpDir)
    log_text += message('Changed directories to {}'.format(ftpDir))
    # get list of files in current FTP directory
    filesInFtpDir = ftp.nlst()
    print 'Created list of files in {}'.format(ftpDir)
    log_text += message('Created list of files in {}'.format(ftpDir))
    # check if file is in list
    if zippedFileToDownload in filesInFtpDir:
        # download zipped file on ftp to local directory
        with open(os.path.join(localDir, zippedFileToDownload), 'wb') as local_file:
            ftp.retrbinary('RETR ' + zippedFileToDownload, local_file.write)
            print 'Downloaded file to {}'.format(localDir)
            log_text += message('Downloaded file to {}'.format(localDir))
    else: # if file is not in list
        print 'The file: {}, was not found in {}'.format(zippedFileToDownload, ftpDir)
        log_text += message('The file: {}, was not found in {}'.format(zippedFileToDownload, ftpDir))
    # close ftp connection
    ftp.close()
    print 'Closed FTP connection'
    log_text += message('Closed FTP connection')

    # Unzip zipped file
    # get listing of files in local directory
    filesInLocalDir = os.listdir(localDir)
    # check if regional geodatabase is in directory
    if zippedFileToDownload in filesInLocalDir:
        # file object for zip file
        localZipFile = os.path.join(localDir, zippedFileToDownload)
        # verify file is a zipped file
        if zipfile.is_zipfile(localZipFile):
            # create zip file object
            with zipfile.ZipFile(localZipFile) as z:
                # unzip file to local directory
                z.extractall(localDir)
                print 'Completed unzipping file'
                log_text += message('Completed unzipping file')
        else: # file is not a zip file
            print 'The file: {}, is not a zipped file'.format(zippedFileToDownload)
            log_text += message('The file: {}, is not a zipped file'.format(zippedFileToDownload))
    else: # file was not found on local directory.
        print 'The file: {}, was not found in {}'.format(zippedFileToDownload, localDir)
        log_text += message('The file: {}, was not found in {}'.format(zippedFileToDownload, localDir))
# If an error occurs running geoprocessing tool(s) capture error and write message
# handle error outside of Python system
except EnvironmentError as e:
    tbE = sys.exc_info()[2]
    # add the line number the error occured to the log message
    log_text += "\nFailed at Line {}\n".format(tbE.tb_lineno)
    print 'Failed at Line {}\n'.format(tbE.tb_lineno)
    # add the error message to the log message
    log_text += "\nError: {}\n".format(str(e))
    print 'Error: {}\n'.format(str(e))
# handle exception error
except Exception as e:
    # Store information about the error
    tbE = sys.exc_info()[2]
    # add the line number the error occured to the log message
    log_text += "\nFailed at Line {}\n".format(tbE.tb_lineno)
    print 'Failed at Line {}\n'.format(tbE.tb_lineno)
    # add the error message to the log message
    log_text += "\nError: {}\n".format(e.message)
    print 'Error: {}\n'.format(e.message)
finally:
    # write message to log file
    try:
        with open(log_file, 'w') as f:
            f.write(str(log_text))
    except:
        pass