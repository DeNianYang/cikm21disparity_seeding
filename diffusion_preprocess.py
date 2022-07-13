import networkx as nx
import pandas as pd
import csv
import os
import math
import time
from collections import OrderedDict



gender_dict = {}
file_node = 'DT_node.csv'
file_edge = 'DT_edge.csv'

#edge type
byType = ["\"post_comment\"" , "\"post_like\"" , "\"post_tag\"" , "\"uploaded_photos_comment\"" , "\"uploaded_photos_likes\"" , "\"uploaded_photos_tags\"" , "\"tagged_photos_comments\"" , "\"tagged_photos_likes\"" , "\"tagged_photos_tags\""]

post_type = ["\"post_comment\"" , "\"post_like\"" , "\"post_tag\""]


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


line2write = []

usr_id = 0
id_dict = {}
id_gender_dict = {}
sorted_usr_list = []
for usr in gender_dict:
    sorted_usr_list.append(usr)
sorted_usr_list = sorted(sorted_usr_list)

for i in range(len(sorted_usr_list)):
    usr = sorted_usr_list[i]

    if usr not in id_dict:
        id_dict[usr] = i
        id_gender_dict[i] = gender_dict[usr]

    out = []
    out.append(i)
    for j in range(len(sorted_usr_list)):
        if j != i:
            out.append(0)
        else:
            out.append(1)
    out.append(gender_dict[usr])
    out_tu = tuple(out)
    line2write.append(out)

#usr:[in-neighbor1, in-neighbor2,...]

#type: comment / like / tag
#edge_list = [{},{},{}]
intensity_list = [{},{},{}]
output_list=[{},{},{}]


com = set()
lik = set()
ta = set()


#intensity matrix
node_num = len(gender_dict)
matrix_c = [[0] * node_num for _ in range(node_num)]
matrix_l = [[0] * node_num for _ in range(node_num)]
matrix_t = [[0] * node_num for _ in range(node_num)]


with open(file_edge, 'r') as read_file:
    next(read_file)
    for line in read_file:
        token = line.strip().split(",")
        edge_type = token[1]
        #edge: user1 -> user2 
        #user1 likes or comments user2
        #buile edge: user2 -> user1
        usr1 = token[2]
        usr2 = token[4]
        #remove self-loop
        if usr1 != usr2:
            if edge_type in post_type:
            
                if "comment" in edge_type:
                    #print(edge_type)
                    com.add(edge_type)
                    if usr1 in gender_dict:
                        if usr2 in gender_dict:
                            
                            if usr2 not in intensity_list[0]:
                                intensity_list[0][usr2] = 1
                            else:
                                intensity_list[0][usr2] += 1

                            if (usr2 , usr1) not in output_list[0]:
                                output_list[0][(usr2, usr1)] = 1
                            else:
                                output_list[0][(usr2, usr1)] += 1

                            matrix_c[id_dict[usr1]][id_dict[usr2]] += 1


                elif "like" in edge_type:
                    #print(edge_type)
                    lik.add(edge_type)
                    if usr1 in gender_dict:
                        if usr2 in gender_dict:
                            
                            if usr2 not in intensity_list[1]:
                                intensity_list[1][usr2] = 1
                            else:
                                intensity_list[1][usr2] += 1

                            if (usr2 , usr1) not in output_list[1]:
                                output_list[1][(usr2, usr1)] = 1
                            else:
                                output_list[1][(usr2, usr1)] += 1

                            matrix_l[id_dict[usr1]][id_dict[usr2]] += 1

                elif "tag" in edge_type:
                    #print(edge_type)
                    ta.add(edge_type)
                    if usr1 in gender_dict:
                        if usr2 in gender_dict:
                            
                            if usr2 not in intensity_list[2]:
                                intensity_list[2][usr2] = 1
                            else:
                                intensity_list[2][usr2] += 1

                            if (usr2 , usr1) not in output_list[2]:
                                output_list[2][(usr2, usr1)] = 1
                            else:
                                output_list[2][(usr2, usr1)] += 1

                            matrix_t[id_dict[usr1]][id_dict[usr2]] += 1



id_intensity_list = [{},{},{}]

for usr in gender_dict.keys():
    if usr in intensity_list[0]:
        id_intensity_list[0][id_dict[usr]] = intensity_list[0][usr]
    else:
        id_intensity_list[0][id_dict[usr]] = 0


    if usr in intensity_list[1]:
        id_intensity_list[1][id_dict[usr]] = intensity_list[1][usr]
    else:
        id_intensity_list[1][id_dict[usr]] = 0

    if usr in intensity_list[2]:
        id_intensity_list[2][id_dict[usr]] = intensity_list[2][usr]
    else:
        id_intensity_list[2][id_dict[usr]] = 0

          

line2write = []

types = ["comment" , "like" , "tag"]
comment_set = set(output_list[0].keys())
like_set = set(output_list[1].keys())
tag_set = set(output_list[2].keys())
keys = comment_set.union(like_set , tag_set)


for j in range(node_num):
    for i in range(node_num):
        #print(j)
        #comment network
        if matrix_c[i][j] != 0:
            prob = matrix_c[i][j] * 1.0 / id_intensity_list[0][j]
            line2write.append((j , id_gender_dict[j], i, id_gender_dict[i], prob))

OUTPUT_DIR = 'diffusion/{}.csv'.format(types[0])
with open(OUTPUT_DIR, 'w') as writefile:
    writer = csv.writer(writefile,delimiter=" ")
    for line in line2write:
        writer.writerow(line)

line2write =[]
for j in range(node_num):
    for i in range(node_num):
        #print(j)
        #like network
        if matrix_l[i][j] != 0:
            prob = matrix_l[i][j] * 1.0 / id_intensity_list[1][j]
            line2write.append((j , id_gender_dict[j], i, id_gender_dict[i], prob))

OUTPUT_DIR = 'diffusion/{}.csv'.format(types[1])
with open(OUTPUT_DIR, 'w') as writefile:
    writer = csv.writer(writefile,delimiter=" ")
    for line in line2write:
        writer.writerow(line)


line2write=[]
for j in range(node_num):
    for i in range(node_num):
        #print(j)
        #tag network
        if matrix_t[i][j] != 0:
            prob = matrix_t[i][j] * 1.0 / id_intensity_list[2][j]
            line2write.append((j , id_gender_dict[j], i, id_gender_dict[i], prob))

OUTPUT_DIR = 'diffusion/{}.csv'.format(types[2])
with open(OUTPUT_DIR, 'w') as writefile:
    writer = csv.writer(writefile,delimiter=" ")
    for line in line2write:
        writer.writerow(line)

line2write=[]

        





'''
for edge in keys:
    if edge in output_list[0]:
        comment_num = output_list[0][edge]
    else:
        comment_num = 0

    if edge in output_list[1]:
        like_num = output_list[1][edge]
    else:
        like_num = 0

    if edge in output_list[2]:
        tag_num = output_list[2][edge]
    else:
        tag_num = 0

    usr1 = edge[0]
    usr2 = edge[1]

    line2write.append((id_dict[usr1], gender_dict[usr1], id_dict[usr2], gender_dict[usr2], comment_num, like_num, tag_num))

with open(OUTPUT_DIR, 'w') as writefile:
    writer = csv.writer(writefile)
    for line in line2write:
        writer.writerow(line)
'''

'''

sorted_intensity_list =[[],[],[]]

for i in range(len(post_type)):
    sorted_intensity_list[i] = sorted(intensity_list[i].items(), key = lambda d : d[1], reverse = True)



for i in range(3):
    for pair in sorted_intensity_list[i]:
        usr = pair[0]
        intensity_num = pair[1]
        line2write.append((id_dict[usr], gender_dict[usr], intensity_num))

    #insert 0
    for j in id_dict:
        if j not in intensity_list[i]:
            line2write.append((id_dict[j], gender_dict[j], 0))

    OUTPUT_DIR = 'intensity/students_intensity_{}.csv'.format(types[i])
    with open(OUTPUT_DIR, 'w') as writefile:
                writer = csv.writer(writefile)
                for line in line2write:
                    writer.writerow(line)
    line2write = []
'''

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













