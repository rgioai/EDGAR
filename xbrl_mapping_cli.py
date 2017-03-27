


def map_user_term(category, value, suggestions=1, vec_len=100, dist_fn=None):
    if vec_len not in vec_len_list():
        raise ValueError
    if dist_fn is None:
        dist_fn = euclidean
    with HashSeq2Vec(vec_len) as t:
        vector = t.transform([value])
    xa = np.reshape(vector, (1, vec_len))
    xb = h5py.File('sc_data.hdf5', 'r')['vector/%s/%s' % (str(vec_len), category)][:]
    cdist_matrix = cdist(xa, xb, metric=dist_fn)
    # Begin copy from n_best
    best = []
    for i in range(suggestions):
        best.append([-1, float('inf')])
    for column_index in range(len(dist_matrix[0])):
        for i in range(len(best)):
            if dist_matrix[0][column_index] < best[i][1]:
                best.insert(i, [column_index, dist_matrix[0][column_index]])
                best.pop()
    # End copy from n_best
    return best