import numpy as np

def common_elements(list1, list2):
    return [element for element in list1 if element in list2]


def circular_array(starting_index, ending_index, N_v1):
    idx = np.arange(1,N_v1)
    idx = np.roll(idx, -starting_index)[:(len(idx)-starting_index+ending_index)%len(idx)]
    return idx

def min_distance(x0, x1, dimensions):
    delta = np.abs(x0 - x1)
    delta = np.where(delta > 0.5 * dimensions, delta - dimensions, delta)
    return np.sqrt((delta ** 2).sum(axis=-1))

def compute_center(W_active, N_v1):
    left_sum = np.zeros((N_v1,1))
    right_sum = np.zeros((N_v1,1))
    center_rf = np.full((N_v1,), np.nan)
    for kk in range(N_v1):
        found = 0
        ii = 0
        while((ii < N_v1) and (found == 0)):
            cell_kk = W_active[kk, :]
            left_sum[ii] = np.sum(cell_kk[circular_array(ii-25, ii, N_v1)])
            right_sum[ii] = np.sum(cell_kk[circular_array(ii, ii + 25, N_v1)])
            if((np.abs(left_sum[ii] - right_sum[ii]) < 2) and (W_active[kk, ii] > 0)):
                    center_rf[kk] = ii
                    found = 1
            ii = ii + 1
    return center_rf

def compute_topography(W_active_v1, W_active_s1, N_v1):
    center_v1 = compute_center(W_active_v1, N_v1)
    center_s1 = compute_center(W_active_s1, N_v1)
    diag_values = range(N_v1)
    worst_rf = np.full((N_v1,1),25)
    error_v1 = np.full((N_v1,1), np.nan)
    error_s1 = np.full((N_v1,1), np.nan)
    error_column = np.full((N_v1,1), np.nan)
    for ii in range(N_v1):
        error_v1[ii] = min_distance(center_v1[ii],diag_values[ii], N_v1)
        error_s1[ii] = min_distance(center_s1[ii],diag_values[ii], N_v1)
        error_column[ii] = min_distance(worst_rf[ii],diag_values[ii], N_v1)
    norm_error_v1 = np.nansum(error_v1**2)/np.nansum(~np.isnan(center_v1))
    norm_error_s1 = np.nansum(error_s1**2)/np.nansum(~np.isnan(center_s1))
    norm_column_error = np.sum(error_column**2)/N_v1
    align_error_v1 = 1 - norm_error_v1/norm_column_error
    align_error_s1 = 1 - norm_error_s1/norm_column_error
    sparseness_v1 = np.sum(np.isnan(center_v1))/N_v1
    sparseness_s1 = np.sum(np.isnan(center_s1))/N_v1
    topo_v1 = align_error_v1*((1 - sparseness_v1)**2)
    topo_s1 = align_error_s1*((1 - sparseness_s1)**2)

    return align_error_v1, align_error_s1, topo_v1, topo_s1, sparseness_v1, sparseness_s1
