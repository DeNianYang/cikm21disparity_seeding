import dgl
import numpy as np
import torch as torch

from dgl import DGLGraph
from dgl.data import citation_graph as citegrh
import networkx as nx

from gat_preprocess import studentDataset
torch.set_printoptions(edgeitems=20, sci_mode=False, precision=6)

def load_student_data():
    data = studentDataset()
    features = torch.FloatTensor(data.features)
    labels = torch.LongTensor(data.labels)
    mask = torch.BoolTensor(data.train_mask)
    g = dgl.graph(data.graph)
    #g.ndata['emb'] = np.zeros(g.number_of_nodes())
    #g.ndata['emb2'] = np.zeros(g.number_of_nodes())
    #add edge feature
    intensity = data.intensity
    return g, features, labels, mask, intensity



class PositiveSampler(object):
    def __init__(self, g, k):
        #self.weights = g.out_degrees().float() ** 0.75
        self.k = k
        #self.neg_share = neg_share

    def p_samples(self, g, node_num):
        v= np.arange(0,node_num)
        src = torch.from_numpy(v)


        sg = dgl.sampling.sample_neighbors(g, src, self.k, prob=g.edata['intensity'])
        return sg.edges()



class NegativeSampler(object):
    def __init__(self, g, k, neg_share=False):
        self.weights = g.out_degrees().float() ** 0.75
        self.k = k
        self.neg_share = neg_share

    def n_samples(self, g, node_num):
        v= np.arange(0,node_num)
        src = torch.from_numpy(v)
        n = len(src)
        if self.neg_share and n % self.k == 0:
            dst = self.weights.multinomial(n, replacement=True)
            dst = dst.view(-1, 1, self.k).expand(-1, self.k, -1).flatten()
        else:
            dst = self.weights.multinomial(n*self.k, replacement=True)
        src = src.repeat_interleave(self.k)
        return src, dst


'''
src = np.array([1, 2, 2, 3, 3, 3, 4, 5, 6, 6, 6, 7, 7, 7, 7, 8, 8, 9, 10, 10,
        10, 11, 12, 12, 13, 13, 13, 13, 16, 16, 17, 17, 19, 19, 21, 21,
        25, 25, 27, 27, 27, 28, 29, 29, 30, 30, 31, 31, 31, 31, 32, 32,
        32, 32, 32, 32, 32, 32, 32, 32, 32, 33, 33, 33, 33, 33, 33, 33,
        33, 33, 33, 33, 33, 33, 33, 33, 33, 33])
dst = np.array([0, 0, 1, 0, 1, 2, 0, 0, 0, 4, 5, 0, 1, 2, 3, 0, 2, 2, 0, 4,
        5, 0, 0, 3, 0, 1, 2, 3, 5, 6, 0, 1, 0, 1, 0, 1, 23, 24, 2, 23,
        24, 2, 23, 26, 1, 8, 0, 24, 25, 28, 2, 8, 14, 15, 18, 20, 22, 23,
        29, 30, 31, 8, 9, 13, 14, 15, 18, 19, 20, 22, 23, 26, 27, 28, 29, 30,
        31, 32])
'''

'''
g_ = dgl.DGLGraph((src,dst))
pos_sampler_ = PositiveSampler(g_, 2)
n_src, n_dst = pos_sampler_.p_samples(g_,34)

print(n_src, n_dst)

'''

'''
g, features, labels, mask, intensity = load_student_data()
g.edata['intensity'] = torch.ones(g.number_of_edges(), dtype=torch.float32)
for edge in intensity.keys():
    usr1 = edge[0]
    usr2 = edge[1]
    g.edges[usr1, usr2].data['intensity'] = torch.tensor([intensity[edge]], dtype=torch.float32)



pos_sampler_ = PositiveSampler(g, 2)
p_src, p_dst = pos_sampler_.p_samples(g, g.number_of_nodes())
'''

a = torch.tensor([1,2])
b = torch.tensor([2,3])

print(a+b)
print(torch.dot(a,b))





