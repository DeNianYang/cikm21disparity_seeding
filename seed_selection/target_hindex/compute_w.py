import networkx as nx
import pandas as pd
import csv
import os
import math
import time

import matplotlib.pyplot as plt
import numpy as np


sort_number = [0,1,2]
types = ['comment.csv', 'like.csv', 'tag.csv']

target_ = ['target_hindexc', 'target_hindexl', 'target_hindext']

seeds = [100]
#,10,20,50,100

OPEN_DIR = 'Diffusion_Model/{}_target_hindex-{}-{}-{}.csv.out'

WRITE_DIR = 'new_weight/weight2_{}_{}.csv'

for seed in seeds:
    for bytype in range(1):
        x = []
        y = []
        z = []

        for ratio in range(21):

            

            with open(OPEN_DIR.format(types[bytype], target_[bytype], seed, ratio/20), 'r') as read_file:
                for line in read_file:
                    token = line.strip().split("\t")
                    spread_m = float(token[0])
                    spread_f = float(token[1])
                    target_ratio = spread_f * 1.0 / (spread_f + spread_m)
                    print(target_ratio)



            x.append(target_ratio)
            y.append(ratio/20)

            #print(x)
            #print(y)

        print(x)
        print(y)
        z_ = np.polyfit(x,y,1)
        z = list(z_)
        line2write=[]
        print(z)

        for t_ratio in range(21):

            s_ratio = z[0] * t_ratio/20 + z[1]  

            line2write.append((t_ratio/20, s_ratio))

        with open (WRITE_DIR.format(seed, target_[bytype]), 'w') as writefile:
            writer = csv.writer(writefile)
            for line in line2write:
                writer.writerow(line)





