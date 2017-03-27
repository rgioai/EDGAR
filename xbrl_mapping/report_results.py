from utils import dist_fns_list, vec_len_list, categories_list

import numpy as np
import h5py
import os
import subprocess
import itertools
import sys


def dset_names_to_report():
    dset_names = []
    for vec_len, category in itertools.product(dist_fns_list(), categories_list):
        for n in ['cluster_size_analysis', 'cluster_names']:
            dset_names.append('/vector/%d/standard/%s/%s' % (vec_len, category, n))
        for n, dist in itertools.product([1, 5], dist_fns_list()):
            dset_names.append('vector/%d/custom/%s/%d_best_%s'
                              % (vec_len, category, n, dist.__name__))
        for n in ['head_examples', 'tail_examples']:
            dset_names.append('/vector/%d/custom/%s/%s' % (vec_len, category, n))
    return dset_names


def save_as_csv(dataset_name):
    try:
        dset = hdf5[dataset_name]
        np.savetxt(target_directory + dataset_name + '.csv', dset[:],
                   fmt='%g', delimiter=',', newline='\n', header=get_header(dataset_name))
    except KeyError:
        print('%s not in hdf5 dataset' % dataset_name)


def get_header(dataset_name):
    if 'standard' in dataset_name:
        if 'cluster_size_analysis' in dataset_name:
            return ''  # Cluster size analysis
        elif 'cluster_names' in dataset_name:
            return ''  # Cluster names
        else:
            raise ValueError('Dataset naming convention not available')
    elif 'custom' in dataset_name:
        if 'best' in dataset_name:
            return ''  # n_best analysis
        elif 'head_examples' in dataset_name:
            return ''  # Head examples
        elif 'tail_examples' in dataset_name:
            return ''  # Tail exampels
        else:
            raise ValueError('Dataset naming convention not available')
    else:
        raise ValueError('Dataset naming convention not available')


if __name__ == '__main__':
    target_directory = '/storage/xbrl_reporting/'
    hdf5 = h5py.File('/storage/XBRL_Update/sc_data.hdf5', 'r+')
    if not os.path.exists('/storage/xbrl_results'):
        os.mkdir('/storage/xbrl_results')
    for dset_name in dsets_to_report():
        save_as_csv(dset_name)
    hdf5.close()

    if '-c' in sys.argv:
        subprocess.run(['lrztar', '/storage/xbrl_results/'])
        subprocess.run(['scp', '/storage/xbrl_results.tar.lrz', 'rgio@10.0.1.11:~/Downloads/'])
