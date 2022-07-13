

import pandas as pd
import csv
import os
import math
import time
from collections import OrderedDict



import torch
import torch.nn as nn
import torch.nn.functional as F


class GATLayer(nn.Module):
    def __init__(self, g, in_dim, out_dim):
        super(GATLayer, self).__init__()
        self.g = g
        # equation (1)
        self.fc = nn.Linear(in_dim, out_dim, bias=False)
        # equation (2)
        self.attn_fc = nn.Linear(2 * out_dim, 1, bias=False)
        self.reset_parameters()

    def reset_parameters(self):
        """Reinitialize learnable parameters."""
        gain = nn.init.calculate_gain('relu')
        nn.init.xavier_normal_(self.fc.weight, gain=gain)
        nn.init.xavier_normal_(self.attn_fc.weight, gain=gain)

    def edge_attention(self, edges):
        # edge UDF for equation (2)
        z2 = torch.cat([edges.src['z'], edges.dst['z']], dim=1)
        a = self.attn_fc(z2)
        edge_num = list(a.shape)[0]
        #print(edge_num)
        add = torch.reshape(edges.data['weight'] , (edge_num, 1))
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
        return {'h': h}

    def forward(self, h):
        # equation (1)
        z = self.fc(h)
        self.g.ndata['z'] = z
        # equation (2)
        self.g.apply_edges(self.edge_attention)
        # equation (3) & (4)
        self.g.update_all(self.message_func, self.reduce_func)
        return self.g.ndata.pop('h')

##################################################################
# Equation (1)
# ^^^^^^^^^^^^
#
# .. math::
#
#   z_i^{(l)}=W^{(l)}h_i^{(l)},(1)
#
# The first one shows linear transformation. It's common and can be
# easily implemented in Pytorch using ``torch.nn.Linear``.
#
# Equation (2)
# ^^^^^^^^^^^^
#
# .. math::
#
#   e_{ij}^{(l)}=\text{LeakyReLU}(\vec a^{(l)^T}(z_i^{(l)}|z_j^{(l)})),(2)
#
# The un-normalized attention score :math:`e_{ij}` is calculated using the
# embeddings of adjacent nodes :math:`i` and :math:`j`. This suggests that the
# attention scores can be viewed as edge data, which can be calculated by the
# ``apply_edges`` API. The argument to the ``apply_edges`` is an **Edge UDF**,
# which is defined as below:

def edge_attention(self, edges):
    # edge UDF for equation (2)
    z2 = torch.cat([edges.src['z'], edges.dst['z']], dim=1)
    a = self.attn_fc(z2)
    return {'e' : F.leaky_relu(a)}

########################################################################3
# Here, the dot product with the learnable weight vector :math:`\vec{a^{(l)}}`
# is implemented again using PyTorch's linear transformation ``attn_fc``. Note
# that ``apply_edges`` will **batch** all the edge data in one tensor, so the
# ``cat``, ``attn_fc`` here are applied on all the edges in parallel.
#
# Equation (3) & (4)
# ^^^^^^^^^^^^^^^^^^
#
# .. math::
#
#   \begin{align}
#   \alpha_{ij}^{(l)}&=\frac{\exp(e_{ij}^{(l)})}{\sum_{k\in \mathcal{N}(i)}^{}\exp(e_{ik}^{(l)})},&(3)\\
#   h_i^{(l+1)}&=\sigma\left(\sum_{j\in \mathcal{N}(i)} {\alpha^{(l)}_{ij} z^{(l)}_j }\right),&(4)
#   \end{align}
#
# Similar to GCN, ``update_all`` API is used to trigger message passing on all
# the nodes. The message function sends out two tensors: the transformed ``z``
# embedding of the source node and the un-normalized attention score ``e`` on
# each edge. The reduce function then performs two tasks:
#
#
# * Normalize the attention scores using softmax (equation (3)).
# * Aggregate neighbor embeddings weighted by the attention scores (equation(4)).
#
# Both tasks first fetch data from the mailbox and then manipulate it on the
# second dimension (``dim=1``), on which the messages are batched.

def reduce_func(self, nodes):
    # reduce UDF for equation (3) & (4)
    # equation (3)
    alpha = F.softmax(nodes.mailbox['e'], dim=1)
    # equation (4)
    h = torch.sum(alpha * nodes.mailbox['z'], dim=1)
    return {'h' : h}

#####################################################################
# Multi-head attention
# ^^^^^^^^^^^^^^^^^^^^
#
# Analogous to multiple channels in ConvNet, GAT introduces **multi-head
# attention** to enrich the model capacity and to stabilize the learning
# process. Each attention head has its own parameters and their outputs can be
# merged in two ways:
#
# .. math:: \text{concatenation}: h^{(l+1)}_{i} =||_{k=1}^{K}\sigma\left(\sum_{j\in \mathcal{N}(i)}\alpha_{ij}^{k}W^{k}h^{(l)}_{j}\right)
#
# or
#
# .. math:: \text{average}: h_{i}^{(l+1)}=\sigma\left(\frac{1}{K}\sum_{k=1}^{K}\sum_{j\in\mathcal{N}(i)}\alpha_{ij}^{k}W^{k}h^{(l)}_{j}\right)
#
# where :math:`K` is the number of heads. You can use
# concatenation for intermediary layers and average for the final layer.
#
# Use the above defined single-head ``GATLayer`` as the building block
# for the ``MultiHeadGATLayer`` below:

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

###########################################################################
# Put everything together
# ^^^^^^^^^^^^^^^^^^^^^^^
#
# Now, you can define a two-layer GAT model.

class GAT(nn.Module):
    def __init__(self, g, in_dim, hidden_dim, out_dim, num_heads):
        super(GAT, self).__init__()
        self.layer1 = MultiHeadGATLayer(g, in_dim, hidden_dim, num_heads)
        # Be aware that the input dimension is hidden_dim*num_heads since
        # multiple head outputs are concatenated together. Also, only
        # one attention head in the output layer.
        self.layer2 = MultiHeadGATLayer(g, hidden_dim * num_heads, out_dim, 1)

    def forward(self, h):
        h = self.layer1(h)
        h = F.elu(h)
        g.ndata['emb'] = h
        h = self.layer2(h)
        
        return h

#############################################################################
# We then load the Cora dataset using DGL's built-in data module.
import dgl as dgl
from dgl import DGLGraph
from dgl.data import citation_graph as citegrh
import networkx as nx

from gat_preprocess_old import studentDataset
torch.set_printoptions(edgeitems=20, sci_mode=False, precision=6)

def load_student_data():
    data = studentDataset()
    features = torch.FloatTensor(data.features)
    labels = torch.LongTensor(data.labels)
    mask = torch.BoolTensor(data.train_mask)
    g = dgl.graph(data.graph)
    g.ndata['emb'] = np.zeros(g.number_of_nodes())

    #add edge feature
    weight = data.weight
    return g, features, labels, mask, weight




##############################################################################
# The training loop is exactly the same as in the GCN tutorial.

import time
import numpy as np

g, features, labels, mask, weight = load_student_data()

#set edge data
#initialize
g.edata['weight'] = torch.ones(g.number_of_edges(), dtype=torch.float32)
#set weight
for edge in weight.keys():
    usr1 = edge[0]
    usr2 = edge[1]
    g.edges[usr1, usr2].data['weight'] = torch.tensor([weight[edge]], dtype=torch.float32)

#declare tensor 1870 * 8
#means the final node embeddings of all nodes


# create the model, 2 heads, each head has hidden size 8



net = GAT(g,
          in_dim=features.size()[1],
          hidden_dim=8,
          out_dim=2,
          num_heads=2)

# create optimizer
optimizer = torch.optim.Adam(net.parameters(), lr=1e-3)


avg_loop = 10
gat_score_list = {}
for i in range(g.number_of_nodes()):
    gat_score_list[i] = 0.0
score = torch.tensor([0.0])

for _ in range(avg_loop):

    net = GAT(g,
          in_dim=features.size()[1],
          hidden_dim=8,
          out_dim=2,
          num_heads=2)

    # create optimizer
    optimizer = torch.optim.Adam(net.parameters(), lr=1e-3)

    # main loop
    dur = []
    for epoch in range(50):
        if epoch >= 3:
            t0 = time.time()

        logits = net(features)
        #print(logits)
        logp = F.log_softmax(logits, 1)
        #print(logp.size())
        #print(labels.size())
        loss = F.nll_loss(logp[mask], labels[mask])

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if epoch >= 3:
            dur.append(time.time() - t0)

        print("Epoch {:05d} | Loss {:.4f} | Time(s) {:.4f}".format(
            epoch, loss.item(), np.mean(dur)))

    #print(g.ndata['emb'])
    emb_tensor = g.ndata['emb']



    
    #score = torch.tensor([0.0])
    for i in range(g.number_of_nodes()):
        for j in range(g.number_of_nodes()):
            if i != j:
                score += torch.dot(emb_tensor[i], emb_tensor[j]) 
        gat_score_list[i] += float(score) * 1.0 / avg_loop
        score = torch.tensor([0.0])


    print(_)


#offset
gat_score_real_list = list(gat_score_list.values())

for i in range(g.number_of_nodes()):
    gat_score_list[i] -= min(gat_score_real_list) * 1.0


sorted_list = sorted(gat_score_list.items(), key = lambda d : d[1], reverse = True)

line2write =[]


for pair in sorted_list:
    line2write.append((pair[0], pair[1]))


OUTPUT_DIR = 'old_gat_like.csv'
with open(OUTPUT_DIR, 'w') as writefile:
    writer = csv.writer(writefile)
    for line in line2write:
        writer.writerow(line)

#compute influence centrality
#for pair in sorted_list[:20]:
#    print(pair)


        
#########################################################################
# Visualizing and understanding attention learned
# ----------------------------------------------
#
# Cora
# ^^^^
#
# The following table summarizes the model performance on Cora that is reported in
# `the GAT paper <https://arxiv.org/pdf/1710.10903.pdf>`_ and obtained with DGL 
# implementations.
#
# .. list-table::
#    :header-rows: 1
#
#    * - Model
#      - Accuracy
#    * - GCN (paper)
#      - :math:`81.4\pm 0.5%`
#    * - GCN (dgl)
#      - :math:`82.05\pm 0.33%`
#    * - GAT (paper)
#      - :math:`83.0\pm 0.7%`
#    * - GAT (dgl)
#      - :math:`83.69\pm 0.529%`
#
# *What kind of attention distribution has our model learned?*
#
# Because the attention weight :math:`a_{ij}` is associated with edges, you can
# visualize it by coloring edges. Below you can pick a subgraph of Cora and plot the
# attention weights of the last ``GATLayer``. The nodes are colored according
# to their labels, whereas the edges are colored according to the magnitude of
# the attention weights, which can be referred with the colorbar on the right.
#
# .. image:: https://data.dgl.ai/tutorial/gat/cora-attention.png
#   :width: 600px
#   :align: center
#
# You can see that the model seems to learn different attention weights. To
# understand the distribution more thoroughly, measure the `entropy
# <https://en.wikipedia.org/wiki/Entropy_(information_theory>`_) of the
# attention distribution. For any node :math:`i`,
# :math:`\{\alpha_{ij}\}_{j\in\mathcal{N}(i)}` forms a discrete probability
# distribution over all its neighbors with the entropy given by
#
# .. math:: H({\alpha_{ij}}_{j\in\mathcal{N}(i)})=-\sum_{j\in\mathcal{N}(i)} \alpha_{ij}\log\alpha_{ij}
#
# A low entropy means a high degree of concentration, and vice
# versa. An entropy of 0 means all attention is on one source node. The uniform
# distribution has the highest entropy of :math:`\log(\mathcal{N}(i))`.
# Ideally, you want to see the model learns a distribution of lower entropy
# (i.e, one or two neighbors are much more important than the others).
#
# Note that since nodes can have different degrees, the maximum entropy will
# also be different. Therefore, you plot the aggregated histogram of entropy
# values of all nodes in the entire graph. Below are the attention histogram of
# learned by each attention head.
#
# |image2|
#
# As a reference, here is the histogram if all the nodes have uniform attention weight distribution.
#
# .. image:: https://data.dgl.ai/tutorial/gat/cora-attention-uniform-hist.png
#   :width: 250px
#   :align: center
#
# One can see that **the attention values learned is quite similar to uniform distribution**
# (i.e, all neighbors are equally important). This partially
# explains why the performance of GAT is close to that of GCN on Cora
# (according to `author's reported result
# <https://arxiv.org/pdf/1710.10903.pdf>`_, the accuracy difference averaged
# over 100 runs is less than 2 percent). Attention does not matter
# since it does not differentiate much.
#
# *Does that mean the attention mechanism is not useful?* No! A different
# dataset exhibits an entirely different pattern, as you can see next.
#
# Protein-protein interaction (PPI) networks
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
# The PPI dataset used here consists of :math:`24` graphs corresponding to
# different human tissues. Nodes can have up to :math:`121` kinds of labels, so
# the label of node is represented as a binary tensor of size :math:`121`. The
# task is to predict node label.
#
# Use :math:`20` graphs for training, :math:`2` for validation and :math:`2`
# for test. The average number of nodes per graph is :math:`2372`. Each node
# has :math:`50` features that are composed of positional gene sets, motif gene
# sets, and immunological signatures. Critically, test graphs remain completely
# unobserved during training, a setting called "inductive learning".
#
# Compare the performance of GAT and GCN for :math:`10` random runs on this
# task and use hyperparameter search on the validation set to find the best
# model.
#
# .. list-table::
#    :header-rows: 1
#
#    * - Model
#      - F1 Score(micro)
#    * - GAT
#      - :math:`0.975 \pm 0.006`
#    * - GCN
#      - :math:`0.509 \pm 0.025`
#    * - Paper
#      - :math:`0.973 \pm 0.002`
#
# The table above is the result of this experiment, where you use micro `F1
# score <https://en.wikipedia.org/wiki/F1_score>`_ to evaluate the model
# performance.
#
# .. note::
#
#   Below is the calculation process of F1 score:
#  
#   .. math::
#  
#      precision=\frac{\sum_{t=1}^{n}TP_{t}}{\sum_{t=1}^{n}(TP_{t} +FP_{t})}
#  
#      recall=\frac{\sum_{t=1}^{n}TP_{t}}{\sum_{t=1}^{n}(TP_{t} +FN_{t})}
#  
#      F1_{micro}=2\frac{precision*recall}{precision+recall}
#  
#   * :math:`TP_{t}` represents for number of nodes that both have and are predicted to have label :math:`t`
#   * :math:`FP_{t}` represents for number of nodes that do not have but are predicted to have label :math:`t`
#   * :math:`FN_{t}` represents for number of output classes labeled as :math:`t` but predicted as others.
#   * :math:`n` is the number of labels, i.e. :math:`121` in our case.
#
# During training, use ``BCEWithLogitsLoss`` as the loss function. The
# learning curves of GAT and GCN are presented below; what is evident is the
# dramatic performance adavantage of GAT over GCN.
#
# .. image:: https://data.dgl.ai/tutorial/gat/ppi-curve.png
#   :width: 300px
#   :align: center
#
# As before, you can have a statistical understanding of the attentions learned
# by showing the histogram plot for the node-wise attention entropy. Below are
# the attention histograms learned by different attention layers.
#
# *Attention learned in layer 1:*
#
# |image5|
#
# *Attention learned in layer 2:*
#
# |image6|
#
# *Attention learned in final layer:*
#
# |image7|
#
# Again, comparing with uniform distribution: 
#
# .. image:: https://data.dgl.ai/tutorial/gat/ppi-uniform-hist.png
#   :width: 250px
#   :align: center
#
# Clearly, **GAT does learn sharp attention weights**! There is a clear pattern
# over the layers as well: **the attention gets sharper with a higher
# layer**.
#
# Unlike the Cora dataset where GAT's gain is minimal at best, for PPI there
# is a significant performance gap between GAT and other GNN variants compared
# in `the GAT paper <https://arxiv.org/pdf/1710.10903.pdf>`_ (at least 20 percent),
# and the attention distributions between the two clearly differ. While this
# deserves further research, one immediate conclusion is that GAT's advantage
# lies perhaps more in its ability to handle a graph with more complex
# neighborhood structure.
#
# What's next?
# ------------
#
# So far, you have seen how to use DGL to implement GAT. There are some
# missing details such as dropout, skip connections, and hyper-parameter tuning,
# which are practices that do not involve DGL-related concepts. For more information
# check out the full example.
#
# * See the optimized `full example <https://github.com/dmlc/dgl/blob/master/examples/pytorch/gat/gat.py>`_.
# * The next tutorial describes how to speedup GAT models by parallelizing multiple attention heads and SPMV optimization.
#
# .. |image2| image:: https://data.dgl.ai/tutorial/gat/cora-attention-hist.png
# .. |image5| image:: https://data.dgl.ai/tutorial/gat/ppi-first-layer-hist.png
# .. |image6| image:: https://data.dgl.ai/tutorial/gat/ppi-second-layer-hist.png
# .. |image7| image:: https://data.dgl.ai/tutorial/gat/ppi-final-layer-hist.png
