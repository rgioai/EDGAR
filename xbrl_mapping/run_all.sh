#!/usr/bin/env bash

# This scripts you have already created the directory
# /storage/xbrl_mapping
# and copied all code files
# You also need rwx access to /storage and any files created therein

chmod +x /storage/xbrl_mapping/*
mkdir /storage/XBRL_Update
mkdir /storage/XBRL_Update/financial_statement_data
cd /storage/XBRL_Update/financial_statement_data

cp /storage/xbrl_mapping/get_data.py /storage/XBRL_Update/financial_statement_data
./get_data.py 16
rm *.py

cd /storage/xbrl_mapping

./parce_sec_data.py -aw
./kmeans.py -aw
./distance.py -acdist
./distance.py -nbest 1
./report_results.py -a