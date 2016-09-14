#!/usr/bin/env python3

from objects.FTP import EdgarFtp
import os
import datetime
from math import ceil
from zipfile import ZipFile
import sys


class IndexCrawler(object):
    """
    Crawls EDGAR database for index files through crawl() method.
    """
    def __init__(self):
        pass

    def crawl(self, start_year=1993, end_year=2016, files_to_download=None, timeout=None):
        """
        :param start_year: The earliest year for which to collect data; default 2000
        :param end_year: The latest year for which to collect data; default 2016
        :param files_to_download: File names to download; default ['master.zip', 'xbrl.zip']
        :param timeout: Decimal hours of how long to run before timeout; default None
        :return: None
        """
        # Force parameter types
        start_year = int(start_year)
        end_year = int(end_year)
        timeout = float(timeout)

        # Handle mutable defaults
        if files_to_download is None:
            files_to_download = ['master.zip', 'xbrl.zip']
        assert(isinstance(files_to_download, list))
        assert(isinstance(files_to_download[0], str))
        if timeout is not None:
            timeout = datetime.timedelta(hours=timeout)
        start = datetime.datetime.now()

        # Init ftp object
        ftp = EdgarFtp()
        ftp.change_dir('edgar')

        # Read past log file
        if os.path.exists('crawling/logs/log_IndexCrawler.txt'):
            log_file = open('crawling/logs/log_IndexCrawler.txt', 'r')
            try:
                past_log = log_file.read().split('#####################\n#####################')[1]
            except IndexError:
                past_log = ''
            log_file.close()
        else:
            past_log = ''

        # Open new log file
        log_file = open('crawling/logs/log_IndexCrawler.txt', 'w')
        this_log = '####### Index Crawler Summary #######\nRun ' + str(datetime.datetime.now()) + '\n'
        error_log = '####### Index Crawler Errors #######\nRun ' + str(datetime.datetime.now()) + '\n'

        # Change to the large storage directory
        os.chdir('/storage/')

        # Init counters
        total = 0
        success = 0
        fail = 0
        previously_complete = 0
        exit_code = None

        # Know the current quarter
        current_year = datetime.date.today().year
        current_qtr = ceil(datetime.date.today().month/3)

        # Crawler Loop
        try:
            for year in range(start_year, end_year+1):
                for qtr in range(1, 4+1):

                    # Ignore quarters that haven't finished yet
                    # FUTURE Add current quarter updating
                    if year >= current_year and qtr > current_qtr:
                        # Coming Quarter
                        continue

                    elif year == current_year and qtr == current_qtr:
                        # Current Quarter
                        # Make the destination directory
                        directory = 'full-index/' + str(year) + '/QTR' + str(qtr) + '/'
                        if not os.path.exists(directory):
                            os.makedirs(directory)

                        for file in files_to_download:
                            total += 1
                            file_to_check = directory + file.replace('.zip', '.idx')
                            if os.path.exists(file_to_check):
                                os.remove(file_to_check)
                            try:
                                # Download file
                                # print('\rDownloading ' + directory + file, end='')
                                ftp.download('full-index/' + file, directory + file)

                                # Unzip file
                                # print('\rUnzipping ' + directory + file, end='')
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

                    else:
                        # Past Quarter
                        # Make the destination directory
                        directory = 'full-index/' + str(year) + '/QTR' + str(qtr) + '/'
                        if not os.path.exists(directory):
                            os.makedirs(directory)

                        for file in files_to_download:
                            total += 1
                            file_to_check = directory + file.replace('.zip', '.idx')
                            if os.path.exists(file_to_check):
                                previously_complete += 1
                            else:
                                try:
                                    # Download file
                                    # print('\rDownloading ' + directory + file, end='')
                                    ftp.download(directory + file)

                                    # Unzip file
                                    # print('\rUnzipping ' + directory + file, end='')
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
                        if datetime.datetime.now() - start > timeout:
                            exit_code = 'Timeout'
                            sys.exit()
            exit_code = 'Loop complete'
            sys.exit()
        except (KeyboardInterrupt, SystemExit) as e:
            if isinstance(e, KeyboardInterrupt):
                exit_code = 'Keyboard interrupt'
            if exit_code is None:
                exit_code = 'Unknown'
            print(exit_code)
            this_log += 'Exit: %s\nPreviously Complete: %d\nSuccessful: %d\nFailed: %d\nUnattempted: %d\n' \
                        % (exit_code, previously_complete, success, fail, total-(previously_complete+success+fail))
            log_file.write(this_log + '\n#####################\n#####################\n')
            log_file.write('\n' + error_log + '\n\n' + past_log)
            log_file.close()
