#!/usr/bin/env python3
import os
import pickle
import sys
import subprocess


def update_file_structure():
    """
    Opens the hardcoded file containing CIKs to collect data on,
    and ensures they have the associated directory.
    :return: None
    """
    # FUTURE Adapt to CIK_List.pkl
    f = open('objects/ref/Current_SP500_CIK.txt', 'r')
    if not os.path.exists('/storage/cik'):
        os.mkdir('/storage/cik')

    # FUTURE Adapt to a limited child number directory structure
    for line in f:
        directory = '/storage/cik/' + line.replace('\n', '')
        if not os.path.exists(directory):
            os.mkdir(directory)
    f.close()


def init_cik_list():
    """
    Creates the CIK_List.pkl serialized object for DocumentCrawler
    from a hardcoded file.
    :return: None
    """
    # FUTURE Adapt to variable inputs/a standardized file.
    f = open('objects/ref/Current_SP500_CIK.txt', 'r')
    cik_list = []
    for line in f:
        cik_list.append(line.replace('\n', ''))
    pickle.dump(cik_list, open('objects/ref/CIK_List.pkl', 'wb'))
    f.close()

if __name__ == '__main__':
    try:
        os.chdir()
        init_cik_list()
        update_file_structure()
    except IndexError:
        pass
    except FileNotFoundError:
        raise DeprecationWarning('File paths not accurate/in flux')