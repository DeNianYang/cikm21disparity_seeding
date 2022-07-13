# input line : gender1 gender2 id1 id2 timestamp
# output line : gender1 gender2 id1 id2 #hop #week

import networkx as nx
import pandas as pd
import csv
import os
import math
import time
from collections import OrderedDict

#input is a degree dictionary


def count_N(neighbor_degree_list, index):
    count = 0
    for num in neighbor_degree_list:
        if num >= index:
            count += 1
    return count


def HI_index(degree_list, edge_list):
    hi_index_list = {}
    for usr , edges in edge_list.items():
        degree = degree_list[usr]
        neighbor_degree_list = []
        for i in range(int(degree)):
            neighbor_degree_list.append(int(degree_list[edges[i]]))
        # from 0 to max_neighbor_degree - 1
        #print(neighbor_degree_list)
        hi_index = 1
        for i in range(int(degree)+1):
            if(i > 0):
                #N is the number of neighbor that has degree larger than i
                N = count_N(neighbor_degree_list, i)
                if N >= i:
                    hi_index = i
                else:
                    break

        hi_index_list[usr] = hi_index
    return hi_index_list





gender_dict={}
# 'nofilter', 'receivernosend', 'remove1interaction', 'bothcriteria'
# testcase = 'receivernosend'
# file = '../../../dataset_2015/dataset_{}/task1/1_stat_user2/1_stat_user2_0.csv'
file_degree = 'fb_degree_tag.csv'
file_edge_list = 'fb_edge_list_tag.csv'


degree_list = {}
with open(file_degree, 'r') as read_file:
        for line in read_file:
            token = line.strip().split(",")
            usr = token[0]
            usr_g = token[1]
            degree = token[2]

            if usr not in degree_list: 
                degree_list[usr] = degree
            if usr not in gender_dict:
                gender_dict[usr] = usr_g
            

#for key, value in gender_dict.items():
 #   print(key,'->', value)
#print(len(gender_dict))

edge_list = {}
#compute in-degree(or simply "degree")


with open(file_edge_list, 'r') as read_file:
        for line in read_file:
            token = line.strip().split(",")
            usr = token[0]
            #list of edges of usr
            edges = token[1:]
            #print(usr1, usr2)
            if usr not in edge_list:
                edge_list[usr] = edges


line2write = []
OUTPUT_DIR = 'tag_hi_index.csv'

hi_index_list = HI_index(degree_list, edge_list)


sorted_degree_list = sorted(hi_index_list.items(), key = lambda d : int(d[1]), reverse = True)


for pair in sorted_degree_list:
    usr = pair[0]
    index = pair[1]
    line2write.append((usr, gender_dict[usr], index))

with open(OUTPUT_DIR, 'w') as writefile:
            writer = csv.writer(writefile)
            for line in line2write:
                writer.writerow(line)






