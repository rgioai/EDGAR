#!/usr/bin/env python3

import h5py
import numpy as np


if __name__ == '__main__':
    hdf5 = h5py.File('/storage/XBRL_Update/sc_data.hdf5', 'r+')
    vec_grp = hdf5['vector']
    for len_grp in vec_grp:
        std_grp = vec_grp.require_group('%s/standard' % len_grp)
        for cat_grp in std_grp:
            print('\r%s | %s | ' % (len_grp, cat_grp), end='')
            nearest_data = std_grp['%s/all_entries/nearest' % cat_grp][:]
            name_dset = std_grp[cat_grp].create_dataset('cluster_names')

    hdf5.close()