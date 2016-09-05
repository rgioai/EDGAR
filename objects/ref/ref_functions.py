#!/usr/bin/env python3
import os
import pickle
from objects.AVLTree import AVLTree
import sys
import subprocess


def update_file_structure(limit=999):
    """
    Opens the hardcoded file containing CIKs to collect data on,
    and ensures they have the associated directory.
    :return: None
    """
    # FUTURE Adapt to CIK_List.pkl
    f = open('objects/ref/CIK_List.txt', 'r')
    if not os.path.exists('/storage/cik'):
        os.mkdir('/storage/cik')

    # FUTURE Adapt to a limited child number directory structure
    for line in f:
        directory = '/storage/cik/' + line.replace('\n', '')
        if not os.path.exists(directory):
            os.mkdir(directory)
    f.close()


def init_cik_tree():
    """
    Creates the CIK_Tree.pkl serialized object for DocumentCrawler
    from a hardcoded file.
    :return: None
    """
    # FUTURE Adapt to variable inputs/a standardized file.
    cik_tree = AVLTree()
    f = open('objects/ref/CIK_List.txt', 'r')
    for line in f:
        line = line.replace('\n', '')
        cik_tree.insert(int(line))
    pickle.dump(cik_tree, open('objects/ref/CIK_Tree.pkl', 'wb'))
    f.close()


def init_cik_list():
    """
    Creates the CIK_List.pkl serialized object for DocumentCrawler
    from a hardcoded file.
    :return: None
    """
    # FUTURE Adapt to variable inputs/a standardized file.
    f = open('objects/ref/CIK_List.txt', 'r')
    cik_list = []
    for line in f:
        cik_list.append(line.replace('\n', ''))
    pickle.dump(cik_list, open('objects/ref/CIK_List.pkl', 'wb'))
    f.close()

if __name__ == '__main__':
    try:
        #os.chdir()
        init_cik_tree()
        init_cik_list()
        update_file_structure()
    except IndexError:
        pass
    except FileNotFoundError:
        raise DeprecationWarning('File paths not accurate/in flux')
