import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from config import *
from sklearn.model_selection import train_test_split


class PCA_Model:
    def __init__(self):
        self.n_components = 0

    def calc_components(self, features):

        X_std = StandardScaler().fit_transform(features.values)
        # Calculating Eigenvectors and eigenvalues of Cov matirx
        cov_mat = np.cov(X_std.T)
        eig_vals, eig_vecs = np.linalg.eig(cov_mat)
        # Create a list of (eigenvalue, eigenvector) tuples
        eig_pairs = [ (np.abs(eig_vals[i]),eig_vecs[:,i]) for i in range(len(eig_vals))]

        # Sort the eigenvalue, eigenvector pair from high to low
        eig_pairs.sort(key = lambda x: x[0], reverse= True)

        # Calculation of Explained Variance from the eigenvalues
        tot = sum(eig_vals)
        var_exp = [(i/tot)*100 for i in sorted(eig_vals, reverse=True)] # Individual explained variance
        cum_var_exp = np.cumsum(var_exp) # Cumulative explained variance
        n_components = [ n for n,i in enumerate(cum_var_exp) if i>90 ][0]
        self.n_components = n_components
        return n_components

    def train(self, features):
        try:
            model = pickle.load(open(ROOT_DIR + "/core_detection/machine_learning/models/pca", "rb"))
            return model
        except:
            pass

        n_components = self.calc_components(features)
        pca = PCA(n_components=n_components)

        # Store PCA
        pickle.dump(pca, open(ROOT_DIR + '/core_detection/machine_learning/models/pca', 'wb'))
        return pca
    
    def converter(self, data):
        test_values = data.values
        test_std = StandardScaler().fit_transform(test_values)
        return self.model.transform(test_std)
