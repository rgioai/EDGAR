#!/usr/bin/env python3

from objects.FTP import EdgarFtp
import os
import datetime
from zipfile import ZipFile
import sys
import time


def index_crawler(start_year=1993, end_year=2016, files_to_download=None, timeout=None):
    # Handle mutable defaults
    if files_to_download is None:
        files_to_download = ['master.zip, xbrl.zip']
    if timeout is not None:
        # convert timeout from hours to minutes
        timeout *= 60
        # convert timeout from minutes to seconds
        timeout *= 60
        # start clock
        start = time.time()

    # Init ftp object
    ftp = EdgarFtp()
    ftp.change_dir('edgar')

    # Open log file
    log_file = open('IndexCrawler_Log_' + str(datetime.datetime.now()) + '.txt', 'w')
    past_log = log_file.read().split('#####################\n#####################')[1]
    this_log = '####### Index Crawler Summary #######\nRun' + str(datetime.datetime.now()) + '\n'
    error_log = '####### Index Crawler Errors #######\nRun' + str(datetime.datetime.now()) + '\n'

    # Change to the large storage directory
    os.chdir('/storage/')

    # Init counters
    total = 0
    success = 0
    fail = 0

    # Crawler Loop
    try:
        for year in range(start_year, end_year+1):
            for qtr in range(1, 4+1):

                # Ignore quarters that haven't finished yet
                if year == 2016:
                    if qtr >= 3:
                        continue
                total += 1

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

                            success += 1

                        except Exception:
                            # Log errors
                            error_log += str(datetime.datetime.now()) \
                                         + ': Failed to download ' + directory + file + '\n'
                            fail += 1
                if timeout is not None:
                    if time.time() - start > timeout:
                        exit_code = 'Timeout'
                        sys.exit()
        exit_code = 'Loop complete'
        sys.exit()
    except (KeyboardInterrupt, SystemExit) as e:
        if isinstance(e, KeyboardInterrupt):
            exit_code = 'Keyboard interrupt'

        this_log += 'Exit: %s\nSuccessful: %d\nFailed: %d\nUnattempted: %d\n' % (exit_code, success, fail, total-(success+fail))
        log_file.write(this_log + '\n#####################\n#####################\n')
        log_file.write('\n' + error_log + '\n\n' + past_log)
        log_file.close()
