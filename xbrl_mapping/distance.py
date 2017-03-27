#!/usr/bin/env python3

from utils import dist_fns_list, vec_len_list, categories_list, overwrite_hdf5_dataset
import numpy as np
from seq2vec import HashSeq2Vec
from joblib import Parallel, delayed
import tensorflow as tf
import sys
import h5py
import os
import itertools
from scipy.spatial.distance import cdist
import time


def scipy_dist_matrix(vec_len, category):
    std_grp = hdf5['vector/%s/standard/%s' % (str(vec_len), category)]
    cus_grp = hdf5['vector/%s/custom/%s' % (str(vec_len), category)]
    xa_dset = cus_grp['all_entries']
    if xa_dset.shape[0] > 20000:
        xa = xa_dset[0:20000]
    else:
        xa = xa_dset[:]
    xb = std_grp['clusters'][:]
    for dist_fn in dist_fns_list():
        start = time.time()
        print('%s | %s | %s | %d x %d' %
              (str(vec_len), category, dist_fn.__name__, len(xa), len(xb)), end='')
        overwrite_hdf5_dataset(cus_grp, 'cdist_%s' % dist_fn.__name__,
                               data=cdist(xa, xb, metric=dist_fn))
        print(' | %.2f s' % (time.time() - start))


def n_best(n, vec_len, category):
    grp = hdf5['vector/%s/custom/%s' % (str(vec_len), category)]
    for dist_fn in dist_fns_list():
        start = time.time()
        dist_matrix_dset = grp['cdist_%s' % dist_fn.__name__]
        if dist_matrix_dset.shape[0] > 20000:
            dist_matrix = dist_matrix_dset[0:20000]
        else:
            dist_matrix = dist_matrix_dset[:]
        print('%s | %s | %s | %d x %d' %
              (str(vec_len), category, dist_fn.__name__,
               len(dist_matrix), len(dist_matrix[0])), end='')
        best_dset = overwrite_hdf5_dataset(grp, '%d_best_%s' % (n, dist_fn.__name__),
                                           shape=(len(dist_matrix_dset), n, 2), dtype=np.float32)
        for row_index in range(len(dist_matrix)):
            best = []
            for i in range(n):
                best.append([-1, float('inf')])
            for column_index in range(len(dist_matrix[row_index])):
                for i in range(len(best)):
                    if abs(dist_matrix[row_index][column_index]) < best[i][1]:
                        best.insert(i, abs([column_index, dist_matrix_dset[row_index][column_index]]))
                        best.pop()
                        break
            best_dset[row_index] = np.array(best, dtype=np.float32)
        print(' | %.2f s' % (time.time() - start))


if __name__ == '__main__':
    if '-acdist' in sys.argv:
        hdf5 = h5py.File('/storage/XBRL_Update/sc_data.hdf5', 'r+')
        for i_ in itertools.product(vec_len_list(), categories_list()):
            scipy_dist_matrix(i_[0], i_[1])
        hdf5.close()

    if '-abest' in sys.argv:
        n_ = int(sys.argv[sys.argv.index('-abest') + 1])
        hdf5 = h5py.File('/storage/XBRL_Update/sc_data.hdf5', 'r+')
        print('n best: %d' % n_)
        for i_ in itertools.product(vec_len_list(), categories_list()):
            n_best(n_, i_[0], i_[1])
        hdf5.close()
