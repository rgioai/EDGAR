#!/usr/bin/env python

"""
IMPORTANT NOTE: THIS SCRIPT RUNS ON PYTHON 2.7
AS SUCH, IT IS CALLED IN A COMPLEX WAY USING
SUBPROCESS MODULE.

Modified from the GitHub Gist of dougvk
@ https://gist.github.com/dougvk/8499335
"""
import sys
import re
from requests import get


def get_cik(ticker):
    URL = 'http://www.sec.gov/cgi-bin/browse-edgar?CIK={}&Find=Search&owner=exclude&action=getcompany'
    CIK_RE = re.compile(r'.*CIK=(\d{10}).*')
    
    results = CIK_RE.findall(get(URL.format(ticker)).content)
    if len(results):
        return str(results[0])
    else:
        return None


def get_ticker(cik):
    raise NotImplementedError


if __name__ == '__main__':
    # Global variables
    URL = 'http://www.sec.gov/cgi-bin/browse-edgar?CIK={}&Find=Search&owner=exclude&action=getcompany'
    CIK_RE = re.compile(r'.*CIK=(\d{10}).*')

    try:
        mode = sys.argv[1]
        input_value = sys.argv[2]
    except IndexError:
        raise IndexError('Invalid arguments')
    if mode == '-c':
        print get_ticker(input_value)
    elif mode == '-t':
        print get_cik(input_value)
    else:
        raise ValueError('Invalid mode')
