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
def HI_index(degree_list):
    hi_index_list = []
    for i in range(3):
        a = 1


gender_dict = {}
# 'nofilter', 'receivernosend', 'remove1interaction', 'bothcriteria'
# testcase = 'receivernosend'
# file = '../../../dataset_2015/dataset_{}/task1/1_stat_user2/1_stat_user2_0.csv'
file_profile = '../all/students_labels.csv'
file_relation = '../only_post/students_edges_{}.csv'


# read in profile
with open(file_profile, 'r') as read_file:
        for line in read_file:
            token = line.strip().split(",")
            if True:
                usr = token[0]
                #1 for male and 2 for female
                usr_g = token[-1]
                
                if usr not in gender_dict: 
                    gender_dict[usr] = usr_g
            

#for key, value in gender_dict.items():
 #   print(key,'->', value)
#print(len(gender_dict))

edge_list = {}
degree_list = {}
ratio_dict={}
#compute in-degree(or simply "degree")
types = ['comment', 'like', 'tag']

for i in range(1):
    with open(file_relation.format('comment'), 'r') as read_file:
        for line in read_file:
            token = line.strip().split(",")
            usr1 = token[0]
            usr2 = token[1]
            #print(usr1, usr2)
            if usr1 in gender_dict:
                if usr2 in gender_dict:
                    #store in edge list
                    if usr2 not in edge_list:
                        edge_list[usr2] = [usr1]
                    else:
                        if usr1 not in edge_list[usr2]:
                            edge_list[usr2].append(usr1)
                    #if usr2 not in edge_list:
                        #edge_list[usr2] = [usr1]
                    #else:
                        #if usr1 not in edge_list[usr2]:
                            #edge_list[usr2].append(usr1)

           
                

line2write = []
OUTPUT_DIR = 'fb_degree_comment.csv'
OUTPUT_DIR_1 = 'fb_edge_list_comment.csv'
edge_list_sorted = OrderedDict(sorted(edge_list.items(), key=lambda t: int(t[0])))
sorted_degree_list = sorted(edge_list_sorted.items(), key = lambda d : len(d[1]), reverse = True)
#edge_list_sorted = [(usr , edge_list[usr]) for usr in sorted(edge_list.keys())]

for usr, edge in edge_list_sorted.items():
    line = []
    line.append(usr)
    for edges in edge:
        line.append(edges)
    line_ = tuple(line)
    line2write.append(line_)

with open(OUTPUT_DIR_1, 'w') as writefile:
            writer = csv.writer(writefile)
            for line in line2write:
                writer.writerow(line)

line2write = []


for pair in sorted_degree_list:
    usr = pair[0]
    degree = pair[1]
    line2write.append((usr,gender_dict[usr],len(degree)))


with open(OUTPUT_DIR, 'w') as writefile:
            writer = csv.writer(writefile)
            for line in line2write:
                writer.writerow(line)

OUTPUT_DIR_2 = 'fb_ratio_comment.csv'
line2write=[]
for usr in edge_list:
    total = len(edge_list[usr])
    fe = 0
    for nei in edge_list[usr]:
        if gender_dict[nei] == '2':
            fe += 1
    ratio_dict[usr] = float(fe)* 1.0/total
    line2write.append((usr, ratio_dict[usr]))


with open(OUTPUT_DIR_2, 'w') as writefile:
    writer = csv.writer(writefile)
    for line in line2write:
        writer.writerow(line)
            




