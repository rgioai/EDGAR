#!/usr/bin/env python3

from utils import overwrite_hdf5_dataset

import h5py
from sklearn.cluster import KMeans
from scipy.spatial.distance import euclidean
import numpy as np
import sys
import time


def n_clusters(n, x):
    print(" Making cluster", end='')
    if len(x) < n:
        print('\nWARNING: num_samples(%d) < num_clusters(%d)'
              '\nReconfiguring to 0.5 * num_samples = num_clusters(%d)' % (len(x), n, (0.5*len(x))))
        n = int(0.5 * len(x))
    clf = KMeans(n_clusters=n, n_jobs=-1).fit(x.astype('float64'))
    cluster_centers = clf.cluster_centers_
    labels = clf.labels_
    nrst = np.empty((len(cluster_centers), 2))
    print(' Finding Nearest', end='')
    for cluster_index in range(len(clf.cluster_centers_)):
        best = [-1, float('inf')]
        for i in range(len(x)):
            if cluster_index == labels[i]:
                dist = euclidean(x[i], cluster_centers[cluster_index])
                if dist < best[1]:
                    best = [i, dist]
        nrst[cluster_index] = np.array(best)
    return cluster_centers, nrst


if __name__ == '__main__':
    if '-aw' in sys.argv:
        hdf5 = h5py.File('/storage/XBRL_Update/sc_data.hdf5', 'r+')
        vec_grp = hdf5['vector']
        for len_grp in vec_grp:
            std_grp = vec_grp.require_group('%s/standard' % len_grp)
            for cat_grp in std_grp:
                print('\r%s | %s | ' % (len_grp, cat_grp), end='')
                clusters, nearest = n_clusters(1000, std_grp['%s/all_entries' % cat_grp][:])
                overwrite_hdf5_dataset(std_grp[cat_grp], 'clusters', data=clusters)
                overwrite_hdf5_dataset(std_grp[cat_grp], 'nearest', data=nearest)
                print('')
        hdf5.close()
    elif '-exp' in sys.argv:
        test_sizes = [0.25, 0.20, 0.15, 0.10, 0.05, 0.04, 0.03, 0.02, 0.01, 0.05]
        hdf5 = h5py.File('/storage/XBRL_Update/sc_data.hdf5', 'r+')
        vec_grp = hdf5['vector']
        for len_grp in vec_grp:
            std_grp = vec_grp.require_group('%s/standard' % len_grp)
            for cat_grp in std_grp:
                results_array = np.empty((len(test_sizes), 3), dtype=np.float32)
                if cat_grp == 'monetary_unk_point':
                    continue
                for n_percent in range(len(test_sizes)):
                    start = time.time()
                    data = std_grp['%s/all_entries' % cat_grp][:]
                    n_ = int(test_sizes[n_percent] * len(data))
                    print('\r%s | %s | %d | ' % (len_grp, cat_grp, n_), end='')
                    clf_ = KMeans(n_clusters=n_, n_jobs=-1).fit(data.astype('float64'))
                    results_array[n_percent] = np.array([test_sizes[n_percent], n_, clf_.inertia_], dtype=np.float32)
                    print('%.2f s' % (time.time()-start))
                overwrite_hdf5_dataset(std_grp[cat_grp], 'cluster_size_analysis', data=results_array)
        hdf5.close()
