import networkx as nx
import pandas as pd
import csv
import os
import math
import time
from collections import OrderedDict

import numpy as np
import scipy.sparse as sp
import os, sys


class studentDataset(object):
    """Cora citation network dataset. Nodes mean author and edges mean citation
    relationships.
    """
    def __init__(self):
        self.name = 'student'
        self._load()

    def _load(self):
        idx_features_labels = np.genfromtxt("../only_post/students_labels.csv",
                                            dtype=np.dtype(str),
                                            delimiter=',')
        features = sp.csr_matrix(idx_features_labels[:, 1:-1],
                                 dtype=np.float32)
        labels = _encode_onehot(idx_features_labels[:, -1])
        self.num_labels = labels.shape[1]

        # build graph
        idx = np.asarray(idx_features_labels[:, 0], dtype=np.int32)
        idx_map = {j: i for i, j in enumerate(idx)}
        
        edges_all = np.genfromtxt("../only_post/students_edges_tag.csv",
                                        dtype=np.int32,
                                        delimiter=',')
        edges_unordered = edges_all[: , :-1]
        intensity = edges_all[:,-1]
        edges = np.asarray(list(map(idx_map.get, edges_unordered.flatten())),
                           dtype=np.int32).reshape(edges_unordered.shape)
        adj = sp.coo_matrix((np.ones(edges.shape[0]),
                             (edges[:, 0], edges[:, 1])),
                            shape=(labels.shape[0], labels.shape[0]),
                            dtype=np.float32)

        # build symmetric adjacency matrix
        #adj = adj + adj.T.multiply(adj.T > adj) - adj.multiply(adj.T > adj)
        self.graph = nx.from_scipy_sparse_matrix(adj, create_using=nx.DiGraph())

        
        edge_dict={}
        for i in range(edges_all.shape[0]):
            edge = (edges_all[i][0], edges_all[i][1])
            if edge not in edge_dict:
                edge_dict[edge] = intensity[i]
        self.intensity = edge_dict

        features = _normalize(features)
        self.features = np.asarray(features.todense())
        self.labels = np.where(labels)[1]

        #2700 -> 1800

        self.train_mask = _sample_mask(range(90), labels.shape[0])
        self.val_mask = _sample_mask(range(200, 400), labels.shape[0])
        self.test_mask = _sample_mask(range(500, 1350), labels.shape[0])



    def __getitem__(self, idx):
        assert idx == 0, "This dataset has only one graph"
        g = dgl.graph(self.graph)
        g.ndata['train_mask'] = self.train_mask
        g.ndata['val_mask'] = self.val_mask
        g.ndata['test_mask'] = self.test_mask
        g.ndata['label'] = self.labels
        g.ndata['feat'] = self.features

        return g

    def __len__(self):
        return 1


def _sample_mask(idx, l):
    """Create mask."""
    mask = np.zeros(l)
    mask[idx] = 1
    return mask

def _normalize(mx):
    """Row-normalize sparse matrix"""
    rowsum = np.asarray(mx.sum(1))
    r_inv = np.power(rowsum, -1).flatten()
    r_inv[np.isinf(r_inv)] = 0.
    r_mat_inv = sp.diags(r_inv)
    mx = r_mat_inv.dot(mx)
    return mx

def _encode_onehot(labels):
    classes = list(sorted(set(labels)))
    classes_dict = {c: np.identity(len(classes))[i, :] for i, c in
                    enumerate(classes)}
    labels_onehot = np.asarray(list(map(classes_dict.get, labels)),
                               dtype=np.int32)
    return labels_onehot

def load_student():
    data = studentDataset()
    return data




'''

gender_dict = {}
# 'nofilter', 'receivernosend', 'remove1interaction', 'bothcriteria'
# testcase = 'receivernosend'
# file = '../../../dataset_2015/dataset_{}/task1/1_stat_user2/1_stat_user2_0.csv'
file_node = 'DT_node.csv'
file_edge = 'DT_edge.csv'

#edge type
byType = ["\"post_comment\"" , "\"post_like\"" , "\"post_tag\"" , "\"uploaded_photos_comment\"" , "\"uploaded_photos_likes\"" , "\"uploaded_photos_tags\"" , "\"tagged_photos_comments\"" , "\"tagged_photos_likes\"" , "\"tagged_photos_tags\""]

post_type = ["\"post_comment\"" , "\"post_like\"" , "\"post_tag\""]


# read in profile
with open(file_node, 'r') as read_file:
    next(read_file)
    for line in read_file:
        token = line.strip().split(",")
        if token[2] == '0' or token[2] == '1':
            usr = token[1]
            #1 for female and 0 for male
            usr_g = token[2]
            
            if usr not in gender_dict: 
                gender_dict[usr] = str(int(usr_g) + 1)
            

print("#graph node : ", len(gender_dict))


'''









