import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep

import pandas as pd
import csv
import os
import math
import time
from collections import OrderedDict


edge_list = []
g = nx.DiGraph()
with open('../diffusion/comment.csv', 'r') as read_file:
    #next(read_file)
    for line in read_file:
        token = line.strip().split(" ")
        edge_list.append((int(token[0]), int(token[2]), float(token[4])))


g.add_weighted_edges_from(edge_list)


# Network topology
#g = nx.erdos_renyi_graph(10, 0.1)

# Model selection
model = ep.IndependentCascadesModel(g)

# Model Configuration
config = mc.Configuration()
config.add_model_parameter('infected', [1,2,3,4,5,6,7,8,9,10,11,12,13,114,15,16,16])

# Setting the edge parameters

threshold = 0.0
for e in g.edges():
    config.add_edge_configuration("threshold", e, threshold)

model.set_initial_status(config)

# Simulation execution
a = iterations = model.iteration_bunch(200)
#for i in range(10):
#    for j in range(10):
#        print(g[i][j])
#print(g.edges())
print(a[-1]['node_count'])
