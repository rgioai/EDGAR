#!/usr/bin/env python3
import os
import pickle
import sys


def update_file_structure():
    f = open('EDGAR/objects/ref/Current_SP500_CIK.txt', 'r')
    if not os.path.exists('/storage/cik'):
        os.mkdir('/storage/cik')

    for line in f:
        directory = '/storage/cik/' + line.replace('\n', '')
        if not os.path.exists(directory):
            os.mkdir(directory)
    f.close()


def init_cik_list():
    f = open('EDGAR/objects/ref/Current_SP500_CIK.txt', 'r')
    cik_list = []
    for line in f:
        cik_list.append(line.replace('\n', ''))
    pickle.dump(cik_list, open('EDGAR/objects/ref/CIK_List.pkl', 'wb'))
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