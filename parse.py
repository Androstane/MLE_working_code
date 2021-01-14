import pandas as pd
from scipy.spatial.distance import pdist, squareform
import numpy as np

def hamming(a, b): 
    n = a - b
    s = np.count_nonzero(n)
    return s    
    
def parse(path):
    cnp = pd.read_csv(path + '/gt.cnp', sep = '\t')
    cnp.drop(cnp.columns[[0,1,2]], axis = 1, inplace = True) 
    cnp.columns = cnp.columns.str.replace(' ', '')
    M = cnp.values
    M = M.transpose()
    L = len(M)
    dist = np.zeros((L,L))
    for i in range(0, len(M)):
        for j in range(0, len(M)): 
            value = hamming(M[i], M[j])
            dist[i][j] = value
            dist[j][i] = value
    leaf_name = list(cnp.columns.values) 
    d = cnp.to_dict('list')
    return path, dist, leaf_name, d