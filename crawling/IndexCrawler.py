#!/usr/bin/env python3

from objects.FTP import EdgarFtp
import os
import datetime
from zipfile import ZipFile
import sys


def main(start_year=1993, end_year=2016, files_to_download=['master.zip, xbrl.zip']):
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
                            error_log += str(datetime.datetime.now()) + ': Failed to download ' + directory + file + '\n'
                            fail += 1
        sys.exit()
    except (KeyboardInterrupt, SystemExit):
        this_log += 'Successful: %d\nFailed: %d\nUnattempted: %d\n' % (success, fail, total-(success+fail))
        log_file.write(this_log + '\n#####################\n#####################\n')
        log_file.write('\n' + error_log + '\n\n' + past_log)
        log_file.close()

if __name__ == '__main__':
    try:
        start_year = int(sys.argv[1])
    except IndexError:
        start_year = 1993
    except ValueError:
        start_year = 1993
    try:
        end_year = sys.argv[2]
    except IndexError:
        end_year = 2016
    except ValueError:
        end_year = 2016
    try:
        files_to_download = sys.argv[3]
        files_to_download = files_to_download.replace('[', '').replace(']', '').replace("'", '').replace(' ', '').split(',')
        files_to_download = files_to_download.replace(']', '')
        files_to_download = files_to_download.replace("'", '')
        files_to_download = files_to_download.replace(' ', '')
        files_to_download = files_to_download.split(',')
    except IndexError:
        files_to_download = ['master.zip, xbrl.zip']
    except ValueError:
        files_to_download = ['master.zip, xbrl.zip']
