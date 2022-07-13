import networkx as nx
import pandas as pd
import csv
import os
import math
import time
from collections import OrderedDict



gender_dict = {}
# 'nofilter', 'receivernosend', 'remove1interaction', 'bothcriteria'
# testcase = 'receivernosend'
# file = '../../../dataset_2015/dataset_{}/task1/1_stat_user2/1_stat_user2_0.csv'
file = 'only_post/students_edges_all.csv'

#edge type
byType = ["\"post_comment\"" , "\"post_like\"" , "\"post_tag\""]



post_type = ['comment', 'like', 'tag', 'interact']

male_pagerank = [[],[],[],[]]; female_pagerank = [[],[],[],[]]; 
pagerank_centrality = [{},{},{},{}]


file_label = 'students_labels.csv'
#build gender dict
with open(file_label, 'r') as read_file:
    for line in read_file:
        token = line.strip().split(',')
        usr = token[0]
        gender = token[1]
        if usr not in gender_dict: gender_dict[usr] = gender


print('#graph size: ', len(gender_dict))

for byType in range(4):
    
    header = ['src','1','dst','2','comment','like','tag','interact']
    df = pd.read_csv(file, names=header)
    cols2dele = [1,3]
    df.drop(df.columns[cols2dele],axis=1,inplace=True)
    df.iloc[:,2+byType] = pd.to_numeric(df.iloc[:,2+byType])
    Graphtype = nx.DiGraph()
    if byType == 0: weight = 'comment'
    elif byType == 1: weight = 'like'
    elif byType == 2: weight = 'tag'
    else: weight = 'interact'
    G = nx.from_pandas_edgelist(df,'src', 'dst', edge_attr=weight, create_using=Graphtype)
    pagerank_centrality[byType] = nx.pagerank(G, weight=weight)

    for n,c in sorted(pagerank_centrality[byType].items()):
        if gender_dict[str(n)] == '1': male_pagerank[byType].append(c)
        elif gender_dict[str(n)] == '2': female_pagerank[byType].append(c)

    male_pagerank[byType] = sorted(male_pagerank[byType])
    female_pagerank[byType] = sorted(female_pagerank[byType])

    male_list = {}; female_list = {}
    for value in male_pagerank[byType]:
        if value not in male_list: male_list[value] = 1
        else: male_list[value] += 1
    for value in female_pagerank[byType]:
        if value not in female_list: female_list[value] = 1
        else: female_list[value] += 1
    # print(male_list)
    male_list_sorted = [(val , male_list[val]) for val in sorted(male_list.keys())]
    female_list_sorted = [(val , female_list[val]) for val in sorted(female_list.keys())] 
    #print(pagerank_centrality[0])
    s = [0,0]


    #sorted output file
    line2write = []
    for i in range(4):
        pagerank_centrality_sorted = sorted(pagerank_centrality[i].items(), key=lambda x: x[1], reverse=True)  
        for pair in pagerank_centrality_sorted:
            #print(pair)
            usr = pair[0]
            value = pair[1]
            line2write.append((usr, gender_dict[str(usr)], value))

        OUTPUT_DIR = 'pagerank/{}.csv'.format(post_type[i])
        with open(OUTPUT_DIR, 'w') as writefile:
            writer = csv.writer(writefile)
            for line in line2write:
                writer.writerow(line)

        line2write=[]




'''
    
    for i in pagerank_centrality[byType].keys():
        line2write.append((i, gender_dict[str(i)], pagerank_centrality[byType][i]))
    OUTPUT_DIR = 'pagerank/pagerank_{}.csv'.format(post_type[byType])
    with open(OUTPUT_DIR, 'w') as writefile:
        writer = csv.writer(writefile)
        for line in line2write:
            writer.writerow(line)
'''

#print(pagerank_centrality[0])

'''
    line2write = []
    OUTPUT_DIR = 'pagerank/pagerank_{}_{}.csv'.format(gender, byType)
    with open(OUTPUT_DIR, 'w') as writefile:
        writer = csv.writer(writefile)
        for line in line2write:
            writer.writerow(line)
    
    for gender, lst in enumerate([male_list_sorted, female_list_sorted]):
        sum = 0
        tmp_line2write = []
        for k, v in lst:
            sum = sum + v
            tmp_line2write.append([k, sum])
        s[gender] = s[gender] + sum
    
    # CCDF Calculation
    for gender, lst in enumerate([male_list_sorted, female_list_sorted]):
        sum = 0
        line2write = []
        for k, v in lst:
            line2write.append([k, 1 - float(sum+v)/float(s[gender])])
            sum = sum + v
        OUTPUT_DIR = 'pagerank/pagerank_{}_{}.csv'.format(gender, byType)
        with open(OUTPUT_DIR, 'w') as writefile:
            writer = csv.writer(writefile)
            for line in line2write:
                writer.writerow(line)

'''


    







