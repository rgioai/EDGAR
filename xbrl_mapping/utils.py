from scipy.spatial.distance import cosine, euclidean


def dist_fns_list():
    # return [braycurtis, canberra, chebyshev, cityblock, correlation,
    #       cosine, euclidean, mahalanobis, minkowski, seuclidean]
    return [cosine, euclidean]


def vec_len_list():
    return [50, 100, 150, 200]


def categories_list():
    return ['abstract', 'monetary_credit_duration', 'monetary_credit_point',
            'monetary_debit_duration', 'monetary_debit_point', 'monetary_unk_duration',
            'monetary_unk_point', 'nonmonetary_duration', 'nonmonetary_point']


def overwrite_hdf5_dataset(grp, dset_name, data=None, shape=None, dtype=None):
    try:
        dset = grp[dset_name]
        del grp[dset_name]
    except KeyError:
        pass
    if data is not None:
        grp.create_dataset(dset_name, data=data)
    elif shape is not None:
        return grp.create_dataset(dset_name, shape, dtype=dtype)
    else:
        raise ValueError('No dataset defined')