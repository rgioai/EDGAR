#!/usr/bin/env python3

from utils import dist_fns_list, vec_len_list, categories_list

import numpy as np
from joblib import Parallel, delayed
import h5py
import os
import subprocess
import itertools
import sys


def dset_names_to_report():
    dset_names = []
    for vec_len, category in itertools.product(vec_len_list(), categories_list()):
        for n in ['cluster_size_analysis']:
            dset_names.append('/vector/%d/standard/%s/%s' % (vec_len, category, n))
    return dset_names


def save_as_csv(dataset_name):
    try:
        dset = hdf5[dataset_name]
        print('%s ... exporting' % dataset_name)
        target_name = target_directory + dataset_name.replace('/', '_') + '.csv'
        np.savetxt(target_name, dset[:],
                   fmt='%10.5f', delimiter=',', newline='\n', header=get_header(dataset_name))
    except KeyError:
        print('%s not in hdf5 dataset' % dataset_name)


def get_header(dataset_name):
    if 'standard' in dataset_name:
        if 'cluster_size_analysis' in dataset_name:
            return '%_of_data,num_clusters,inertia'
        elif 'cluster_names' in dataset_name:
            return ''
        else:
            raise ValueError('Dataset naming convention not available')
    else:
        raise ValueError('Dataset naming convention not available')


def summary_stats(vec_len, category):
    grp = hdf5['vector/%s/custom/%s' % (str(vec_len), category)]
    report = 'dist_fn,top_n,n,min,max,mean,std,med\n'
    for dset_name in grp:
        if 'best' in dset_name:
            print('Calculating summary statistics for %s' % dset_name)
            dset = grp[dset_name]
            dist_fn = dset_name.split('_')[2]
            top_n = int(dset_name.split('_')[0])
            num_samples = int(dset.shape[0])
            trials = dset[:]
            trial_array = np.array(Parallel(n_jobs=-1, verbose=0)
                                   (delayed(helper_process_row)(i) for i in trials),
                                   dtype=np.float32)
            trial_array = np.reshape(trial_array, (num_samples * top_n,))
            report += '%s,%d,%d,%.5f,%.5f,%.5f,%.5f,%.5f\n' % (dist_fn, top_n, num_samples,
                                                               np.min(trial_array), np.max(trial_array),
                                                               np.mean(trial_array),
                                                               np.std(trial_array), np.median(trial_array))
        else:
            print('Skipping %s' % dset_name)
    with open(target_directory + 'vector_%s_custom_%s_summary_stats.csv'
            % (str(vec_len), category), 'w') as f:
        f.write(report)


def helper_process_row(row):
    return_vals = []
    for val in row:
        return_vals.append(val[1])
    return return_vals


def head_tail_examples(vec_len, category, dist_fn):
    head_list, tail_list = make_head_and_tail_lists(vec_len, category, dist_fn)
    report = 'HEAD\ncustom_term,dist_from_cluster,standard_term,dist_from_cluster,total_distance\n'
    for h in head_list:
        custom_term = hdf5['text/custom/%s' % category][h[0]]
        custom_dist = h[1][1]
        standard_nrst = hdf5['vector/%d/standard/%s/nearest' % (vec_len, category)][h[1][0]]
        standard_term = hdf5['text/standard/%s' % category][standard_nrst[0]]
        standard_dist = standard_nrst[1]
        total_dist = custom_dist + standard_dist
        report += '%s,%.5f,%s,%.5f,%.5f\n' \
                  % (custom_term, custom_dist, standard_term, standard_dist, total_dist)

    report += '\nTAIL\n'
    for t in tail_list:
        custom_term = hdf5['text/custom/%s' % category][h[0]]
        custom_dist = h[1][1]
        standard_nrst = hdf5['vector/%d/standard/%s/nearest' % (vec_len, category)][h[1][0]]
        standard_term = hdf5['text/standard/%s' % category][standard_nrst[0]]
        standard_dist = standard_nrst[1]
        total_dist = custom_dist + standard_dist
        report += '%s,%.5f,%s,%.5f,%.5f\n' \
                  % (custom_term, custom_dist, standard_term, standard_dist, total_dist)

    with open(target_directory + '%d_%s_%s_head_tail_examples.csv'
            % (vec_len, category, dist_fn), 'w') as f:
        f.write(report)
        print('Success!')


def make_head_and_tail_lists(vec_len, category, dist_fn, n=5):
    dset_array = hdf5['vector/%d/custom/%s/1_best_%s' % (vec_len, category, dist_fn)][:]
    best = []
    worst = []
    for i in range(n):
        best.append([-1, [-1, float('+inf')]])
        worst.append([-1, [-1, float('-inf')]])
    for row_index in range(len(dset_array)):
        for i in range(len(best)):
            if abs(dset_array[row_index][0][1]) < best[i][1][1]:
                best.insert(i, [row_index, [dset_array[row_index][0][0], dset_array[row_index][0][1]]])
                best.pop()
                break
            if abs(dset_array[row_index][0][1]) > worst[i][1][1]:
                worst.insert(i, [row_index, [dset_array[row_index][0][0], dset_array[row_index][0][1]]])
                worst.pop()
                break
    return best, worst


def cluster_names(vec_len, category):
    dset_array = hdf5['vector/%d/standard/%s/nearest' % (vec_len, category)][:]
    with open(target_directory + '%d_%s_cluster_terms.txt'
            % (vec_len, category), 'w') as f:
        for row in dset_array:
            term = hdf5['text/standard/%s' % category][row[0]]
            f.write('%s\n' % term)


if __name__ == '__main__':
    target_directory = '/storage/xbrl_reporting/'
    if not os.path.exists('/storage/xbrl_reporting'):
        os.mkdir('/storage/xbrl_reporting')

    do_all = '-a' in sys.argv

    if '-dsdump' in sys.argv or do_all:
        hdf5 = h5py.File('/storage/XBRL_Update/sc_data.hdf5', 'r+')
        for dset_name in dset_names_to_report():
            save_as_csv(dset_name)
        hdf5.close()

    if '-bstat' in sys.argv or do_all:
        hdf5 = h5py.File('/storage/XBRL_Update/sc_data.hdf5', 'r+')
        for i_ in itertools.product(vec_len_list(), categories_list()):
            summary_stats(i_[0], i_[1])
        hdf5.close()

    if '-htex' in sys.argv or do_all:
        hdf5 = h5py.File('/storage/XBRL_Update/sc_data.hdf5', 'r+')
        for i_ in itertools.product(vec_len_list(), categories_list(), dist_fns_list()):
            try:
                head_tail_examples(i_[0], i_[1], i_[2].__name__)
            except KeyError as e:
                print(e)
        hdf5.close()

    if '-cn' in sys.argv or do_all:
        hdf5 = h5py.File('/storage/XBRL_Update/sc_data.hdf5', 'r+')
        for i_ in itertools.product(vec_len_list(), categories_list()):
            try:
                cluster_names(i_[0], i_[1])
            except KeyError as e:
                print(e)
        hdf5.close()

    if '-c' in sys.argv or do_all:
        subprocess.run(['lrztar', '/storage/xbrl_results/'])
        subprocess.run(['scp', '/storage/xbrl_results.tar.lrz', 'rgio@10.0.1.11:~/Downloads/'])
