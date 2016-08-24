#!/usr/bin/env python3
import sys
from crawling.IndexCrawler import IndexCrawler
from crawling.DocumentCrawler import DocumentCrawler

# CLI for EDGAR project
# Current implementations:
# -automated
# -index_crawler
# -document_crawler

fn = sys.argv[1]
arg1 = sys.argv[2]
arg2 = sys.argv[3]
arg3 = sys.argv[4]
arg4 = sys.argv[5]

if fn == '-a' or fn == 'auto':
    settings = {}
    with open('crawling/crawling_settings.txt', 'r') as f:
        for line in f:
            if "EDGAR" in line:
                continue
            else:
                line = line.replace(' ', '').split(':')
                settings[line[0]] = line[1]
    settings['forms'] = settings['forms'].split(',')

    ic = IndexCrawler()
    ic.crawl(settings['start_year'], settings['end_year'], None, settings['index_timeout'])

    dc = DocumentCrawler()
    dc.crawl(settings['start_year'], settings['end_year'], settings['forms'], settings['doc_timeout'])

elif fn == '-i' or fn == 'index_crawler':
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

elif fn == '-d' or fn == 'document_crawler':
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

    dc = DocumentCrawler()
    dc.crawl(start, end, to_download, timeout)

elif fn == '-c' or fn == 'update_cik':
    raise NotImplemented
