#!/usr/bin/env python3
import sys
import crawling
import objects

# CLI for EDGAR project
# Current implementations:
# -test_ftp
# -index_crawler

fn = sys.argv[1]
arg1 = sys.argv[2]
arg2 = sys.argv[3]
arg3 = sys.argv[4]
arg4 = sys.argv[5]

if fn == '-t':
    print(str(sys.argv))

elif fn == 'test_ftp':
    pass

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
        to_download = arg3.replace('[', '').replace(']', '').replace("'", '').replace(' ', '').split(',')
    except ValueError:
        to_download = None
    try:
        timeout = float(arg4)
    except ValueError:
        timeout = None

    # Run function
    index_crawler(start, end, to_download, timeout)

elif fn == '-d' or fn == 'document_crawler':
    raise NotImplemented

elif fn == '-c' or fn == 'update_cik':
    raise NotImplemented