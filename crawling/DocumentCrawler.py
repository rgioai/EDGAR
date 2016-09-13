#!/usr/bin/env python3

from objects.FTP import EdgarFtp
from objects.AVLTree import AVLTree
from objects.ref.ref_functions import update_file_structure
import os
from math import ceil
import datetime
import pickle
import sys


class DocumentCrawler(object):
    """
    Crawls EDGAR database for documents through crawl() method.
    """

    def __init__(self):
        pass

    def crawl(self, start_year=2000, end_year=2016, forms_to_download=None, timeout=None):
        """
        :param start_year: The earliest year for which to collect data; default 2000
        :param end_year: The latest year for which to collect data; default 2016
        :param forms_to_download: Forms types to download; default ['10-K', '10-Q', '10-K/A', '10-Q/A']
        :param timeout: Decimal hours of how long to run before timeout; default None
        :return: None
        """
        # Force parameter types
        start_year = int(start_year)
        end_year = int(end_year)
        timeout = float(timeout)

        # Handle mutable defaults
        if forms_to_download is None:
            forms_to_download = ['10-K', '10-Q', '10-K/A', '10-Q/A']
        assert(isinstance(forms_to_download, list))
        assert(isinstance(forms_to_download[0], str))
        if timeout is not None:
            timeout = datetime.timedelta(hours=timeout)
        start = datetime.datetime.now()

        # Init ftp object
        ftp = EdgarFtp()

        # Init cik_list
        # cik_list = pickle.load(open('objects/ref/CIK_List.pkl', 'rb'))
        cik_tree = pickle.load(open('objects/ref/CIK_Tree.pkl', 'rb'))

        # Open new log file
        log_file = open('crawling/logs/log_DocCrawler_%s.txt' % (str(datetime.datetime.now())), 'w')
        this_log = '####### Doc Crawler Summary #######\nRun' + str(datetime.datetime.now()) + '\n'
        error_log = '####### Doc Crawler Errors #######\nRun' + str(datetime.datetime.now()) + '\n'

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
            # Loop backwards in time to prioritize more recent documents
            year = end_year
            while year >= start_year:
                for qtr in [4, 3, 2, 1]:
                    print('\n%sQTR%s' % (str(year), str(qtr)))

                    # Ignore quarters that haven't finished yet
                    if year >= current_year and qtr > current_qtr:
                        continue

                    # Open and load the index file
                    directory = 'full-index/' + str(year) + '/QTR' + str(qtr) + '/'
                    index_file = open(directory + 'master.idx', 'r')

                    header = True
                    # TODO Figure out what's wrong
                    """UnicodeDecodeError:
                    ‘utf-8’ codec can’t decode byte 0xc3 in position 2313: invalid continuation byte"""
                    try:
                        for line in index_file:
                            line = line.replace('\n', '')
                            if header:
                                # Filter out the header
                                if '------------' in line:
                                    header = False
                            else:
                                # Check if this line is a document we should download
                                line_list = line.split('|')
                                cik = int(line_list[0])
                                form = line_list[2]
                                if cik_tree.find(cik) is not None and form in forms_to_download:

                                    total += 1
                                    edgar_addr = line_list[4]
                                    local_addr = self.local_form_address(cik, form, year, qtr)
                                    if not os.path.exists(local_addr):
                                        try:
                                            ftp.download(edgar_addr, local_addr)
                                            success += 1
                                            status = 'success'
                                        except Exception:
                                            # Log errors
                                            error_log += str(datetime.datetime.now()) \
                                                         + ': Failed to download ' + edgar_addr + '\n'
                                            fail += 1
                                            status = 'fail'
                                    else:
                                        previously_complete += 1
                                        status = 'previously complete'
                                    print('%s for %s: %s' % (form, cik, status))
                            if timeout is not None:
                                if datetime.datetime.now() - start > timeout:
                                    exit_code = 'Timeout'
                                    sys.exit()
                    except UnicodeDecodeError as e:
                        error_log += str(datetime.datetime.now()) + ': Failed to decode ' + str(e) + '\n'
                        continue
                year -= 1
            exit_code = 'Loop complete'
            sys.exit()

        except (KeyboardInterrupt, SystemExit) as e:
            print('\n')
            if isinstance(e, KeyboardInterrupt):
                exit_code = 'Keyboard interrupt'
            if exit_code is None:
                exit_code = 'Unknown'
            this_log += 'Exit: %s at %s\nPreviously Complete: %d\nSuccessful: %d\nFailed: %d\n' \
                        'Unattempted: %d\n' % \
                        (exit_code, str(datetime.datetime.now()), previously_complete, success,
                         fail, total - (previously_complete + success + fail))
            log_file.write(this_log + '\n#####################\n#####################\n')
            log_file.write('\n' + error_log)
            log_file.close()

    def local_form_address(self, cik, form, year, qtr, xbrl=False):
        """
        All parameters must be valid literal for str(),
        except xbrl which is a bool default False.
        :param cik:
        :param form:
        :param year:
        :param qtr:
        :param xbrl: is an xbrl file
        :return: Local path to specified file.
        """

        # Parce cik
        cik = str(cik)
        while len(cik) < 9:
            cik = '0' + cik

        top_dir = cik[-9:-6]
        if not os.path.exists('/storage/cik/%s' % top_dir):
            os.mkdir('/storage/cik/%s' % top_dir)
        mid_dir = cik[-6:-3]
        if not os.path.exists('/storage/cik/%s/%s' % (top_dir, mid_dir)):
            os.mkdir('/storage/cik/%s/%s' % (top_dir, mid_dir))
        low_dir = cik[-3:]
        if not os.path.exists('/storage/cik/%s/%s/%s' % (top_dir, mid_dir, low_dir)):
            os.mkdir('/storage/cik/%s/%s/%s' % (top_dir, mid_dir, low_dir))

        if xbrl:
            path = '/storage/cik/%s/%s/%s/%s_%sQ%s_%s_xbrl.txt' \
                   % (top_dir, mid_dir, low_dir, str(cik), str(year), str(qtr), str(form))
        else:
            path = '/storage/cik/%s/%s/%s/%s_%sQ%s_%s.txt' \
                   % (top_dir, mid_dir, low_dir, str(cik), str(year), str(qtr), str(form))

        if not os.path.exists(path):
            return path
        else:
            i = 0
            while os.path.exists(path):
                i += 1
                if xbrl:
                    path = '/storage/cik/%s/%s/%s/%s_%sQ%s_%s_xbrl(%d).txt' \
                           % (top_dir, mid_dir, low_dir, str(cik), str(year), str(qtr), str(form), i)
                else:
                    path = '/storage/cik/%s/%s/%s/%s_%sQ%s_%s(%d).txt' \
                           % (top_dir, mid_dir, low_dir, str(cik), str(year), str(qtr), str(form), i)
            return path
