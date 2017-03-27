#!/usr/bin/env bash

# Anytime you use the Mac file explorer to view a directory, it adds a file '.DS_Store' that saves the view
# preferences of the user.  It's a hidden file, so whatever.  Except it throws off a lot of file operations
# in this project.  Simply run this script to remove all the .DS_Store files in the data directory.

cd /storage
find . -name '.DS_Store' -type f -delete

# Copy relevant programs to deep learning servers
rsync -r ~/PycharmProjects/EDGAR/xbrl_mapping/ rgio@10.0.1.27:/storage/xbrl_mapping/

rsync -r ~/PycharmProjects/EDGAR/xbrl_mapping/ rgio@fireball.cs.uni.edu:/storage/xbrl_mapping/

rsync -r ~/PycharmProjects/EDGAR/xbrl_mapping/ /storage/xbrl_mapping/