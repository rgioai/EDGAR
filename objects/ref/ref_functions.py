#!/usr/bin/env python3
import numpy as np
import os


def update_file_structure():
    f = open('Current_SP500_CIK.txt', 'r')
    if not os.path.exists('/storage/cik'):
        os.mkdir('/storage/cik')

    for line in f:
        directory = '/storage/cik/' + line
        if not os.path.exists(directory):
            os.mkdir(directory)
    f.close()


def init_cik_list():
    f = open('Current_SP500_CIK.txt', 'r')
    cik_list = []
    for line in f:
        cik_list.append(line)
    cik_array = np.array(cik_list)
    cik_array.dump('CIK_List.pkl')
    f.close()

if __name__ == '__main__':
    try:
        if sys.argv[1] == 'update_file_structure' or sys.argv[1] == '-u':
            update_file_structure()
        elif sys.argv[1] == 'init_cik_list' or sys.argv[1] == '-i':
            init_cik_list()
        else:
            pass
    except IndexError:
        pass
