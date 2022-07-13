import networkx as nx
import pandas as pd
import csv
import os
import math
import time
from collections import OrderedDict
import dgl as dgl
from dgl.nn.pytorch import GATConv
import dgl.function as fn
import torch
import torch.nn as nn
import torch.nn.functional as F


class PositiveSampler(object):
    def __init__(self, g, k):
        #self.weights = g.out_degrees().float() ** 0.75
        self.k = k
        #self.neg_share = neg_share

    def p_samples(self, g, node_num):
        v= np.arange(0,node_num)
        src = torch.from_numpy(v)
        sg = dgl.sampling.sample_neighbors(g, src, self.k, edge_dir='in', prob=g.edata['intensity'],replace=True)
        return sg.edges()



class NegativeSampler(object):
    def __init__(self, g, k, neg_share=False):
        self.weights = g.in_degrees().float() ** 0.75
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


class CrossEntropyLoss(object):
    def __init__(self, g, p_src, p_dst, n_src, n_dst, s_0, weight1, weight2):
        pos_g = dgl.graph((p_src, p_dst))
        pos_g.ndata['emb'] = g.ndata['emb']
        pos_g.ndata['s'] = g.ndata['s']
        self.pos_g = pos_g
        neg_g = dgl.graph((n_src, n_dst))
        neg_g.ndata['emb'] = g.ndata['emb']
        neg_g.ndata['s'] = g.ndata['s']
        self.neg_g = neg_g
        self.p_src = p_src
        self.p_dst = p_dst
        self.n_src = n_src
        self.n_dst = n_dst
        self.weight1 = weight1
        self.weight2 = weight2
        self.s_0 = s_0
        self.g = g




    def get_loss(self):
        '''
        with pos_graph.local_scope():
            pos_graph.ndata['h'] = block_outputs
            pos_graph.apply_edges(fn.u_dot_v('h', 'h', 'score'))
            pos_score = pos_graph.edata['score']
        with neg_graph.local_scope():
            neg_graph.ndata['h'] = block_outputs
            neg_graph.apply_edges(fn.u_dot_v('h', 'h', 'score'))
            neg_score = neg_graph.edata['score']
        '''
        with self.pos_g.local_scope():
            self.pos_g.apply_edges(fn.u_dot_v('emb', 'emb', 'score1'))
            pos_score = self.pos_g.edata['score1']
        with self.neg_g.local_scope():
            self.neg_g.apply_edges(fn.u_dot_v('emb', 'emb', 'score1'))
            neg_score = self.neg_g.edata['score1']

        score = torch.cat([pos_score, neg_score])
        label = torch.cat([torch.ones_like(pos_score), torch.zeros_like(neg_score)]).long()
        loss1 = -1.0 * F.binary_cross_entropy_with_logits(score, label.float())

        with self.pos_g.local_scope():
            self.pos_g.apply_edges(fn.u_sub_v('emb', 'emb', 'score2'))
            pos_score = self.pos_g.edata['score2']
        with self.neg_g.local_scope():
            self.neg_g.apply_edges(fn.u_sub_v('emb', 'emb', 'score2'))
            neg_score = self.neg_g.edata['score2']

        anchor = self.p_dst
        #print(anchor)
        positive = self.pos_g.ndata['s'][self.p_src]
        negative = self.neg_g.ndata['s'][self.n_src]

        #print(positive.size())
        #print(negative.size())

        triplet_loss = nn.TripletMarginLoss(margin=1.0, p=2)
        loss2 = triplet_loss(anchor, positive, negative)
        
        mse_loss = nn.MSELoss()
        loss3 = mse_loss(s_0, self.g.ndata['s'])
        

        return loss1  + loss2 * self.weight1 + loss3 * self.weight2



class GATLayer(nn.Module):
    def __init__(self, g, in_dim, out_dim):
        super(GATLayer, self).__init__()
        self.g = g
        # equation (1)
        self.fc = nn.Linear(in_dim, out_dim, bias=False)
        # equation (2)
        self.attn_fc = nn.Linear(2 * out_dim, 1, bias=False)
        #influence loss
        self.inf_fc = nn.Linear(out_dim,1,bias=False)
        self.reset_parameters()

    def reset_parameters(self):
        """Reinitialize learnable parameters."""
        #fix random initialization
        #torch.manual_seed(1024) 
        gain = nn.init.calculate_gain('relu')
        nn.init.xavier_normal_(self.fc.weight, gain=gain)
        nn.init.xavier_normal_(self.attn_fc.weight, gain=gain)
        nn.init.xavier_normal_(self.inf_fc.weight, gain=gain)

    def edge_attention(self, edges):
        # edge UDF for equation (2)

        z2 = torch.cat([edges.src['z'], edges.dst['z']], dim=1)
        a = self.attn_fc(z2)
        edge_num = list(a.shape)[0]
        #print(edge_num)
        add = torch.reshape(edges.data['intensity'] , (edge_num, 1))
        #print(edges.data['weight'].shape)

        return {'e': torch.mul(F.leaky_relu(a), add)}

    def message_func(self, edges):
        # message UDF for equation (3) & (4)
        return {'z': edges.src['z'], 'e': edges.data['e']}

    def reduce_func(self, nodes):
        # reduce UDF for equation (3) & (4)
        # equation (3)
        alpha = F.softmax(nodes.mailbox['e'], dim=1)
        # equation (4)
        h = torch.sum(alpha * nodes.mailbox['z'], dim=1)

        s = self.inf_fc(h)

        return {'h': h, 's': torch.sigmoid(s)}

    def forward(self, h):
        # equation (1)
        z = self.fc(h)
        self.g.ndata['z'] = z
        # equation (2)
        self.g.apply_edges(self.edge_attention)
        # equation (3) & (4)
        self.g.update_all(self.message_func, self.reduce_func)
        return self.g.ndata.pop('h')



class MultiHeadGATLayer(nn.Module):
    def __init__(self, g, in_dim, out_dim, num_heads, merge='cat'):
        super(MultiHeadGATLayer, self).__init__()
        self.heads = nn.ModuleList()
        for i in range(num_heads):
            self.heads.append(GATLayer(g, in_dim, out_dim))
        self.merge = merge

    def forward(self, h):
        head_outs = [attn_head(h) for attn_head in self.heads]
        if self.merge == 'cat':
            # concat on the output feature dimension (dim=1)
            return torch.cat(head_outs, dim=1)
        else:
            # merge using average
            return torch.mean(torch.stack(head_outs))



class GAT(nn.Module):
    def __init__(self, g, in_dim, hidden_dim, out_dim, num_heads):
        super(GAT, self).__init__()
        self.layer1 = MultiHeadGATLayer(g, in_dim, hidden_dim, num_heads)
        # Be aware that the input dimension is hidden_dim*num_heads since
        # multiple head outputs are concatenated together. Also, only
        # one attention head in the output layer.
        self.layer2 = MultiHeadGATLayer(g, hidden_dim * num_heads, hidden_dim, num_heads)

        self.layer3 = MultiHeadGATLayer(g, hidden_dim * num_heads, out_dim, 1)

    def forward(self, h):
        h = self.layer1(h)
        #record a_0T * hi_0
        s_0 = g.ndata['s']
        h = F.elu(h)
        emb1 = h
        #print(emb1.size())
        h = self.layer2(h)
        h = F.elu(h)
        emb2 = h
        h = self.layer3(h)
        h = F.elu(h)
        emb3 = h
        #print(emb2.size())
        g.ndata['emb'] = torch.cat([emb1, emb2, emb3], dim=1)
        #g.ndata['emb2'] = emb2
        
        return (g.ndata['emb'], g.ndata['s'], s_0)





file_node = '../only_post/students_labels.csv'

post_type = ["\"post_comment\"" , "\"post_like\"" , "\"post_tag\""]

gender_dict={}
# read in profile
with open(file_node, 'r') as read_file:
    #next(read_file)
    for line in read_file:
        token = line.strip().split(",")
        usr = token[0]
        gender = token[-1]

        if usr not in gender_dict:
            gender_dict[usr] = int(gender)

        






#############################################################################
# We then load the Cora dataset using DGL's built-in data module.

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




##############################################################################
# The training loop is exactly the same as in the GCN tutorial.

import time
import numpy as np
g, features, labels, mask, intensity = load_student_data()

#set edge data
#initialize
#g.edata['intensity'] = torch.ones(g.number_of_edges(), dtype=torch.float32)
#set intensity
for edge in intensity.keys():
    usr1 = edge[0]
    usr2 = edge[1]
    g.edges[usr1, usr2].data['intensity'] = torch.tensor([intensity[edge]], dtype=torch.float32)


#declare tensor 1870 * 8
#means the final node embeddings of all nodes


# create the model, 2 heads, each head has hidden size 8
net = GAT(g,
          in_dim=features.size()[1],
          hidden_dim=12,
          out_dim=12,
          num_heads=2)

# create optimizer
optimizer = torch.optim.Adam(net.parameters(), lr=1e-3)


avg_loop = 10
gat_score_list = {}
score = torch.tensor([0.0])

for i in range(g.number_of_nodes()):
    gat_score_list[i] = 0.0


for _ in range(avg_loop):


    net = GAT(g,
          in_dim=features.size()[1],
          hidden_dim=12,
          out_dim=12,
          num_heads=2)

    optimizer = torch.optim.Adam(net.parameters(), lr=1e-3)
    # main loop
    dur = []
    for epoch in range(200):
        if epoch >= 3:
            t0 = time.time()

        h_emb, s_emb, s_0 = net(features)
        #postive sampling and negative sampling
        pos_sample_num = 5
        neg_sample_num = 5
        pos_sampler_ = PositiveSampler(g, pos_sample_num)
        neg_sampler_ = NegativeSampler(g, neg_sample_num)
        p_src, p_dst = pos_sampler_.p_samples(g, g.number_of_nodes())
        n_src, n_dst = neg_sampler_.n_samples(g, g.number_of_nodes())

        loss_obj = CrossEntropyLoss(g, p_src, p_dst,n_src, n_dst, s_0, 1, 1)
        loss = loss_obj.get_loss()

        #loss = F.nll_loss(s_emb[mask], labels[mask])

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if epoch >= 3:
            dur.append(time.time() - t0)

        print("Epoch {:05d} | Loss {:.4f} | Time(s) {:.4f}".format(
            epoch, loss.item(), np.mean(dur)))


    #print(g.ndata['emb'])
    emb_tensor = g.ndata['s']

    '''
    for i in range(g.number_of_nodes()):
        for j in range(g.number_of_nodes()):
            if i != j:
                score = score + torch.dot(emb_tensor[i], emb_tensor[j])
        gat_score_list[i] += float(score) * 1.0 / avg_loop
        score = torch.tensor([0.0])
    '''
    for i in range(g.number_of_nodes()):
        gat_score_list[i] += float(emb_tensor[i]) * 1.0
        #score = torch.tensor([0.0])

    print(_)


    sorted_list = sorted(gat_score_list.items(), key = lambda d : d[1], reverse = True)

    line2write =[]


    for pair in sorted_list:
        usr = pair[0]

        line2write.append((usr, gender_dict[str(usr)], pair[1]))

    for i in range(g.number_of_nodes()):
        gat_score_list[i] = 0.0


    OUTPUT_DIR = 'pre/influence_net_comment_{}.csv'
    with open(OUTPUT_DIR, 'w') as writefile:
        writer = csv.writer(writefile)
        for line in line2write:
            writer.writerow(line)








