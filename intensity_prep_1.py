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
file_node = '../dataset_2015/dataset_remove1interaction/1_stat_user1.csv'


# read in profile

#receive  and    send
comment_intensity_list=[{},{}]
like_intensity_list=[{},{}]

with open(file_node, 'r') as read_file:
    #next(read_file)
    for line in read_file:
        token = line.strip().split(",")
        if 1:
            usr1 = token[0]
            #1 for female and 0 for male
            usr2 = token[2]

            usr1_g = token[1]

            usr2_g = token[3]
            
            if usr1 not in gender_dict: 
                gender_dict[usr1] = usr1_g
            if usr2 not in gender_dict:
                gender_dict[usr2] = usr2_g


            like = int(token[4])
            comment = int(token[5])

            if usr2 not in like_intensity_list[0]:
                like_intensity_list[0][usr2] = like
            else:
                like_intensity_list[0][usr2] += like
            if usr2 not in comment_intensity_list[0]:
                comment_intensity_list[0][usr2] = comment
            else:
                
                comment_intensity_list[0][usr2] += comment

            if usr1 not in like_intensity_list[1]:
                like_intensity_list[1][usr1] = like
            else:
                like_intensity_list[1][usr1] += like

            if usr1 not in comment_intensity_list[1]:
                comment_intensity_list[1][usr1] = comment
            else:
                
                comment_intensity_list[1][usr1] += comment



            
'''
for key, value in gender_dict.items():
    print(key,'->', value)
print(len(gender_dict))
'''

print("#graph node : ", len(gender_dict))



#usr:[in-neighbor1, in-neighbor2,...]

#type: comment / like / tag
#edge_list = [{},{},{}]
intensity_list = [{},{}]
#indegree_list = [{},{},{}]
output_list=[{},{}]


com = set()
lik = set()
ta = set()





comment_sorted_intensity_list =[[],[]]


for i in range(2):
    comment_sorted_intensity_list[i] = sorted(comment_intensity_list[i].items(), key = lambda d : d[1], reverse = True)


like_sorted_intensity_list =[[],[]]


for i in range(2):
    like_sorted_intensity_list[i] = sorted(like_intensity_list[i].items(), key = lambda d : d[1], reverse = True)


for i in range(2):
    line2write = []

    if i == 0:

        for pair in comment_sorted_intensity_list[i]:
            usr = pair[0]
            intensity_num = pair[1]
            line2write.append((usr, gender_dict[usr], intensity_num))

       
        OUTPUT_DIR = 'intensity/ig_commment_{}.csv'.format(i)
        with open(OUTPUT_DIR, 'w') as writefile:
                    writer = csv.writer(writefile)
                    for line in line2write:
                        writer.writerow(line)

    elif i == 1:

        for pair in like_sorted_intensity_list[i]:
            usr = pair[0]
            intensity_num = pair[1]
            line2write.append((usr, gender_dict[usr], intensity_num))


        OUTPUT_DIR = 'intensity/ig_like_{}.csv'.format(i)
        with open(OUTPUT_DIR, 'w') as writefile:
                    writer = csv.writer(writefile)
                    for line in line2write:
                        writer.writerow(line)
    


'''

line2write = []
OUTPUT_DIR = 'test_all.csv'


for edge in output_list[0].keys():
    
    like_num = output_list[0][edge]
    
    if edge in output_list[1]:
        comment_num = output_list[1][edge]
    else:
        comment_num = 0
    if edge in output_list[2]:
        tag_num = output_list[2][edge]
    else:
        tag_num = 0

    usr1 = edge[0]
    usr2 = edge[1]

    line2write.append((usr1[2:][:-2], gender_dict[usr1], usr2[2:][:-2], gender_dict[usr2], like_num, comment_num, tag_num))



for edge in output_list[1].keys():
    if edge not in output_list[0]:
    
        like_num = 0
        
        comment_num = output_list[1][edge]
        
        if edge in output_list[2]:
            tag_num = output_list[2][edge]
        else:
            tag_num = 0

        usr1 = edge[0]
        usr2 = edge[1]

        line2write.append((usr1[2:][:-2], gender_dict[usr1], usr2[2:][:-2], gender_dict[usr2], like_num, comment_num, tag_num))

for edge in output_list[2].keys():
    if edge not in output_list[0]:
        if edge not in output_list[1]:
    
            like_num = 0
            comment_num = 0
            
            tag_num = output_list[2][edge]

            usr1 = edge[0]
            usr2 = edge[1]

            line2write.append((usr1[2:][:-2], gender_dict[usr1], usr2[2:][:-2], gender_dict[usr2], like_num, comment_num, tag_num))
   
with open(OUTPUT_DIR, 'w') as writefile:
            writer = csv.writer(writefile)
            for line in line2write:
                writer.writerow(line)

'''













