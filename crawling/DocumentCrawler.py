#!/usr/bin/env python3

from objects.FTP import EdgarFtp
from objects.ref.ref_functions import update_file_structure
import os
import datetime
import pickle
import sys


class DocumentCrawler(object):
    def __init__(self):
        pass

    def crawl(self, start_year=2000, end_year=2016, forms_to_download=None, timeout=None):

        # Handle mutable defaults
        if forms_to_download is None:
            forms_to_download = ['10-K', '10-Q']
        if timeout is not None:
            timeout = datetime.timedelta(hours=timeout)
        start = datetime.datetime.now()

        # Init ftp object
        ftp = EdgarFtp()

        # Init cik_list
        #cik_list = pickle.load(open('EDGAR/objects/ref/CIK_List.pkl', 'rb'))
        # TODO Change back to full cik_list
        cik_list = ['0000320193', '1652044']


        # Update directory structure
        update_file_structure()

        # Open new log file
        log_file = open('EDGAR/crawling/log_DocCrawler_%s.txt' % (str(datetime.datetime.now())), 'w')
        this_log = '####### Doc Crawler Summary #######\nRun' + str(datetime.datetime.now()) + '\n'
        error_log = '####### Doc Crawler Errors #######\nRun' + str(datetime.datetime.now()) + '\n'

        # Change to the large storage directory
        os.chdir('/storage/')

        # Init counters
        total = 0
        success = 0
        fail = 0
        previously_complete = 0
        dont_exist = 0
        exit_code = None

        # Know the current quarter
        current_year = datetime.date.today().year
        if 1 <= datetime.date.today().month <= 3:
            current_qtr = 1
        elif 4 <= datetime.date.today().month <= 6:
            current_qtr = 2
        elif 7 <= datetime.date.today().month <= 9:
            current_qtr = 3
        else:
            current_qtr = 4

        # Crawler Loop
        try:
            # Loop backwards in time
            # Prioritize downloading more recent documents
            year = end_year
            while year >= start_year:
                for qtr in [4, 3, 2, 1]:

                    # Ignore quarters that haven't finished yet
                    # FUTURE Add current quarter updating
                    if year == current_year and qtr >= current_qtr:
                        continue

                    for index in ['master.idx', 'xbrl.idx']:
                        # Open and load the index file
                        directory = 'full-index/' + str(year) + '/QTR' + str(qtr) + '/'
                        index_file = open(directory + index, 'r')

                        for cik in cik_list:
                            for form in forms_to_download:
                                local_addr = self.local_form_address(cik, form, year, qtr)
                                # TODO print('\rCurrent File: %s' % local_addr, end='')
                                if not os.path.exists(local_addr):
                                    print('CIK %s; Form %s' % (cik, form))
                                    edgar_addr = self.find_form_address(cik, form, index_file)
                                    if edgar_addr is None:
                                        dont_exist += 1
                                        error_log += str(datetime.datetime.now()) \
                                                     + ': Failed to locate form %s: %sQTR%s CIK %s\n' \
                                                       % (form, str(year), str(qtr), cik)
                                    else:
                                        try:
                                            ftp.download(edgar_addr, local_addr)
                                            success += 1
                                        except Exception:
                                            # Log errors
                                            error_log += str(datetime.datetime.now()) \
                                                         + ': Failed to download ' + local_addr + '\n'
                                            fail += 1
                                else:
                                    previously_complete += 1
                                if timeout is not None:
                                    if datetime.datetime.now() - start > timeout:
                                        exit_code = 'Timeout'
                                        sys.exit()
                year -= 1
            exit_code = 'Loop complete'
            sys.exit()

        except (KeyboardInterrupt, SystemExit) as e:
            print('\n')
            if isinstance(e, KeyboardInterrupt):
                exit_code = 'Keyboard interrupt'
            if exit_code is None:
                exit_code = 'Unknown'
            this_log += 'Exit: %s\nPreviously Complete: %d\nSuccessful: %d\nFailed: %d\n' \
                        'Unattempted: %d\nNot Found: %d\n' % \
                        (exit_code, previously_complete, success,
                         fail, total - (previously_complete + success + fail), dont_exist)
            log_file.write(this_log + '\n#####################\n#####################\n')
            log_file.write('\n' + error_log)
            log_file.close()

    def find_form_address(self, cik, form, index_file):
        header = True
        for line in index_file:
            line = line.replace('\n', '')
            if header:
                if '------------' in line:
                    header = False
            else:
                line_list = line.split('|')
                if int(cik) == int(line_list[0]) and form == line_list[2]:
                    return line_list[4]
        return None

    def local_form_address(self, cik, form, year, qtr):
        return '/storage/cik/%s/%s_%sQ%s_%s.txt' % (str(cik), str(cik), str(year), str(qtr), str(form))
