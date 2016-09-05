#!/usr/bin/env python3

"""Command line interface for EDGAR project.
When edgar bash function is in ~/.bash_profile, call using:
edgar fn arg1 arg2 arg3 arg4"""

import sys
import os
import subprocess
import datetime
from crawling.IndexCrawler import IndexCrawler
from crawling.DocumentCrawler import DocumentCrawler
from objects.ref.ref_functions import *

"""
Current implementations:
-CLI test: Prints arguments to verify correct edgar bash function, verifies and prints storage directory
    fn: -t or test
    arg1: n/a
    arg2: n/a
    arg3: n/a
    arg4: n/a
-Automated crawl: Runs index and document crawlers based on EDGAR/crawling/crawling_settings.txt
    fn: -a or auto
    arg1: n/a
    arg2: n/a
    arg3: n/a
    arg4: n/a
-Index crawl: Crawls EDGAR for index files
    fn: -idx or index_crawler
    arg1: starting year
    arg2: ending year
    arg3: List of files to download ['form1', form2']; -d to default ['master.zip', 'xbrl.zip']
    arg4: Decimal hours of how long the index crawler should run before timeout
-Document crawl: Crawls EDGAR for documents
    fn: -doc or document_crawler
    arg1: starting year
    arg2: ending year
    arg3: List of files to download ['form1', form2']; -d to default ['10-K', '10-Q', '10-K/A', '10-Q/A']
    arg4: Decimal hours of how long the document crawler should run before timeout
-Update reference: Updates package files (see args)
    fn: -ref or update_ref'
    1: update; 0: do nothing
    arg1: CIK_List.pkl based on objects/ref/ref_functions.py
    arg2: File structure based on objects/ref/ref_functions.py
    arg3: docs via pydoc
    arg4: n/a
"""
pkg_path = os.path.expanduser('~') + '/EDGAR'
os.chdir(pkg_path)

fn = sys.argv[1]
try:
    arg1 = sys.argv[2]
except IndexError:
    arg1 = 0
try:
    arg2 = sys.argv[3]
except IndexError:
    arg2 = 0
try:
    arg3 = sys.argv[4]
except IndexError:
    arg3 = 0
try:
    arg4 = sys.argv[5]
except IndexError:
    arg4 = 0

if fn == '-t' or fn == 'test':
    print("fn: %s arg1: %s arg2: %s arg3: %s arg4: %s" % (str(fn), str(arg1), str(arg2), str(arg3), str(arg4)))
    print("project dir: %s" % os.getcwd())
    os.chdir('/storage/')
    print("storage dir: %s" % os.getcwd())

elif fn == '-a' or fn == 'auto':
    settings = {}
    with open('crawling/crawling_settings.txt', 'r') as f:
        for line in f:
            if "EDGAR" in line:
                continue
            elif "####" in line:
                break
            else:
                line = line.replace(' ', '')
                line = line.replace('\n', '')
                line = line.split(':')
                settings[line[0]] = line[1]
    settings['forms'] = settings['forms'].split(',')

    print('Automated Run beginning %s\n\nIndex Crawler: ' % datetime.datetime.now())
    ic = IndexCrawler()
    ic.crawl(settings['start_year'], settings['end_year'], None, settings['index_timeout'])

    os.chdir(pkg_path)
    print('Document Crawler: ')
    dc = DocumentCrawler()
    dc.crawl(settings['start_year'], settings['end_year'], settings['forms'], settings['doc_timeout'])

elif fn == '-idx' or fn == 'index_crawler':
    # Validate input
    try:
        start = int(arg1)
    except ValueError:
        start = 1993
    try:
        end = int(arg2)
    except ValueError:
        end = 2016
    try:
        if arg3 == '-d':
            to_download = None
        else:
            to_download = arg3.replace('[', '').replace(']', '').replace("'", '').replace(' ', '').split(',')
    except ValueError:
        to_download = None
    try:
        timeout = float(arg4)
    except ValueError:
        timeout = None

    # Run function
    ic = IndexCrawler()
    ic.crawl(start, end, to_download, timeout)

elif fn == '-doc' or fn == 'document_crawler':
    # Validate input
    try:
        start = int(arg1)
    except ValueError:
        start = 1993
    try:
        end = int(arg2)
    except ValueError:
        end = 2016
    try:
        if arg3 == '-d':
            to_download = None
        else:
            to_download = arg3.replace('[', '').replace(']', '').replace("'", '').replace(' ', '').split(',')
    except ValueError:
        to_download = None
    try:
        timeout = float(arg4)
    except ValueError:
        timeout = None

    # Run function
    dc = DocumentCrawler()
    dc.crawl(start, end, to_download, timeout)

elif fn == '-ref' or fn == 'update_ref':
    if arg1 == '1':
        print("Updating CIK_List.pkl")
        init_cik_list()
    if arg2 == '1':
        update_file_structure()
        print("Updating file structure")
    if arg3 == '1':
        # TODO Fix functionality
        os.chdir('EDGAR/docs')
        subprocess.run(['pydoc -w EDGAR/*/*/*'])
        print("Generating docs")
    if arg4 == '1':
        pass
