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
file_node = 'DT_node.csv'
file_edge = 'DT_edge.csv'

#edge type
byType = ["\"post_comment\"" , "\"post_like\"" , "\"post_tag\"" , "\"uploaded_photos_comment\"" , "\"uploaded_photos_likes\"" , "\"uploaded_photos_tags\"" , "\"tagged_photos_comments\"" , "\"tagged_photos_likes\"" , "\"tagged_photos_tags\""]


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
            
'''
for key, value in gender_dict.items():
    print(key,'->', value)
print(len(gender_dict))
'''

print("#graph node : ", len(gender_dict))



#usr:[in-neighbor1, in-neighbor2,...]
edge_list = [{},{},{}]
intensity_list = [{},{},{}]
in_degree_list = [{},{},{}]
output_list=[{},{},{}]



with open(file_edge, 'r') as read_file:
    next(read_file)
    for line in read_file:
        token = line.strip().split(",")
        edge_type = token[1]
        #usr2 = actor
        #usr1 = person
        usr2 = token[2]
        usr1 = token[4]
        
        #for all byType
        for type_ in range(len(byType)):
            #print(byType[type_], edge_type)
            if byType[type_] == edge_type:

                if usr1 in gender_dict:
                    if usr2 in gender_dict:
                        #if (usr1 != usr2):
                            #print(usr1,usr2)
                        #store in edge list
                        if usr2 not in edge_list[type_]:
                            edge_list[type_][usr2] = [usr1]
                            in_degree_list[type_][usr2] = 1
                        else:
                            if usr1 not in edge_list[type_][usr2]:
                                edge_list[type_][usr2].append(usr1)
                                in_degree_list[type_][usr2] += 1

                        #store in intensity list
                        if usr2 not in intensity_list[type_]:
                            intensity_list[type_][usr2] = 1
                        else:
                            intensity_list[type_][usr2] += 1

                        if (usr1,usr2) not in output_list:
                            output_list[type_][(usr1,usr2)] = 1
                        else:
                            output_list[type_][(usr1,usr2)] += 1


                         

line2write = []
OUTPUT_DIR = 'student_edges.csv'

for edge in output_list[0].keys():
    if edge in output_list[0]:
        like_num = output_list[0][edge]
        if like_num > 1:
            print("hello")
    else:
        like_num = 0

    if edge in output_list[1]:
        comment_num = output_list[1][edge]
        if comment_num > 1:
            print("hello")
    else:
        comment_num = 0

    if edge in output_list[2]:
        tag_num = output_list[2][edge]
        if tag_num > 1:
            print("hello")
    else:
        tag_num = 0

    usr1 = edge[0]
    usr2 = edge[1]

    line2write.append((usr1[2:][:-2], gender_dict[usr1], usr2[2:][:-2], gender_dict[usr2], like_num, comment_num, tag_num))
   

with open(OUTPUT_DIR, 'w') as writefile:
            writer = csv.writer(writefile)
            for line in line2write:
                writer.writerow(line)

sorted_intensity_list = [[],[],[]]
sorted_in_degree_list =[[],[],[]]

for i in range(len(byType)):
    sorted_intensity_list[i] = sorted(intensity_list[i].items(), key = lambda d : int(d[1]), reverse = True)
    sorted_in_degree_list[i] = sorted(in_degree_list[i].items(), key = lambda d : int(d[1]), reverse = True)
#edge_list_sorted = [(usr , edge_list[usr]) for usr in sorted(edge_list.keys())]


usr_list = list(gender_dict.keys())

for i in range(len(byType)):

    line2write = []
    not_zero_intensity = []
    for pair in sorted_intensity_list[i]:
        not_zero_intensity.append(pair[0])
        usr = pair[0]
        line2write.append((usr[2:][:-2], gender_dict[usr], pair[1]))

    zero_intensity = list(set(usr_list) - set(not_zero_intensity))

    for z in  zero_intensity:
        line2write.append((z[2:][:-2], gender_dict[z], 0))

    OUTPUT_DIR_ = 'sorted_student_intensity_{}.csv'.format(byType[i][1:][:-1])
    with open(OUTPUT_DIR_, 'w') as writefile:
            writer = csv.writer(writefile)
            for line in line2write:
                writer.writerow(line)



    line2write = []
    not_zero_indegree = []
    for pair in sorted_in_degree_list[i]:
        not_zero_indegree.append(pair[0])
        usr = pair[0]
        line2write.append((usr[2:][:-2], gender_dict[usr], pair[1]))

    not_zero_indegree = list(set(usr_list) - set(not_zero_indegree))

    for z in  not_zero_indegree:
        line2write.append((z[2:][:-2], gender_dict[z], 0))


    OUTPUT_DIR_ = 'sorted_student_indegree_{}.csv'.format(byType[i][1:][:-1])
    with open(OUTPUT_DIR_, 'w') as writefile:
            writer = csv.writer(writefile)
            for line in line2write:
                writer.writerow(line)



    







