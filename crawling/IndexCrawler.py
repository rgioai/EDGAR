#!/usr/bin/env python3

from objects.FTP import EdgarFtp
import os
import datetime
from zipfile import ZipFile

# User defined variables
start_year = 1993
end_year = 2016
files_to_download = ['master.zip, xbrl.zip']

# Init ftp object
ftp = EdgarFtp()
ftp.change_dir('edgar')

# Open log file
log_file = open('IndexCrawler_Log_' + str(datetime.datetime.now()) + '.txt', 'w')
log_file.write('####### Index Crawler Log #######\nRun' + str(datetime.datetime.now()) + '\n')


for year in range(start_year, end_year+1):
    for qtr in range(1, 4+1):

        # Ignore quarters that haven't finished yet
        if year == 2016:
            if qtr >= 3:
                continue

        # Make the destination directory
        directory = 'full-index/' + str(year) + '/QTR' + str(qtr) + '/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        for file in files_to_download:
            file_to_check = directory + file.replace('.zip', '.idx')
            if not os.path.exists(file_to_check):
                try:
                    # Download file
                    print('\rDownloading ' + directory + file)
                    ftp.download(directory + file)

                    # Unzip file
                    print('\rUnzipping ' + directory + file)
                    zipped = ZipFile(directory + file)
                    zipped.extractall(path=directory)
                    zipped.close()

                    # Remove zip file
                    os.remove(directory + file)

                except Exception:
                    # Log errors
                    log_file.write(str(datetime.datetime.now()) + ': Failed to download ' + directory + file)
