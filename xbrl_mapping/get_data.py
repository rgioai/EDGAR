#!/usr/bin/env python3

import subprocess
import sys
import itertools
import os


def download(year, quarter, overwrite):
    if year < 2000:
        year += 2000
    if not overwrite and os.path.exists('/storage/XBRL_Update/financial_statement_data/%dq%d' % (year, quarter)):
        print('Skipping %dq%d' % (year, quarter))
    else:
        link = 'http://www.sec.gov/data/financial-statements/%dq%d.zip' % (year, quarter)
        subprocess.run(['wget', link])
        subprocess.run(['unzip', '%dq%d.zip' % (year, quarter), '-d', '%dq%d' % (year, quarter)])
        subprocess.run(['rm', '%dq%d.zip' % (year, quarter)])


def download_year(year, overwrite):
    for q in range(1, 4+1):
        download(year, q, overwrite)


def download_all(overwrite):
    for y, q in itertools.product(range(2009, 2016+1), range(1, 4+1)):
        download(y, q, overwrite)


if __name__ == '__main__':
    if '-w' in sys.argv:
        ow = True
    else:
        ow = False
    if '-a' in sys.argv:
        download_all(ow)
    else:
        yr_qtr = sys.argv[-1]
        if '/' in yr_qtr:
            yr = int(yr_qtr.split('/')[0])
            qtr = int(yr_qtr.split('/')[1])
            download(yr, qtr, ow)
        else:
            yr = int(yr_qtr)
            download_year(yr, ow)
