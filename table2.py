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

post_type = ["\"post_comment\"" , "\"post_like\"" , "\"post_tag\""]



sender_dict = {}
receiver_dict={}
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

male_num = 0
female_num = 0
for usr in gender_dict:
    if gender_dict[usr] == '1':
        male_num += 1
    else:
        female_num += 1
print("male ratio: ", male_num/len(gender_dict))
print("female ratio: ", female_num/len(gender_dict))
print("male num: ", male_num)
print("female num: ", female_num)




#usr:[in-neighbor1, in-neighbor2,...]

#type: comment / like / tag
edge_list = [{},{},{}]
intensity_list = [{},{},{}]
#in_degree_list = [{},{},{}]
output_list=[{},{},{}]


com = set()
lik = set()
ta = set()

se_dict={}
re_dict={}


receiver_count = [{},{},{}]
sender_count = [{},{},{}]
with open(file_edge, 'r') as read_file:
    next(read_file)
    for line in read_file:
        token = line.strip().split(",")
        edge_type = token[1]
        usr1 = token[2]
        usr2 = token[4]
        
        
        if edge_type in post_type:

            if usr1 in gender_dict:
                if usr2 in gender_dict:

                    if usr1 not in se_dict:
                        se_dict[usr1] = gender_dict[usr1]
                    if usr2 not in re_dict:
                        re_dict[usr2] = gender_dict[usr2]


        
            if "comment" in edge_type:
                #print(edge_type)
                com.add(edge_type)
                if usr1 in gender_dict:
                    if usr2 in gender_dict:
                        if usr1 not in sender_count[0]:
                            sender_count[0][usr1] = 1
                        else:
                            sender_count[0][usr1] += 1

                        if usr2 not in receiver_count[0]:
                            receiver_count[0][usr2] = 1
                        else:
                            receiver_count[0][usr2] += 1





            elif "like" in edge_type:
                #print(edge_type)
                lik.add(edge_type)
                if usr1 in gender_dict:
                    if usr2 in gender_dict:
                        if usr1 not in sender_count[1]:
                            sender_count[1][usr1] = 1
                        else:
                            sender_count[1][usr1] += 1

                        if usr2 not in receiver_count[1]:
                            receiver_count[1][usr2] = 1
                        else:
                            receiver_count[1][usr2] += 1

            elif "tag" in edge_type:
                #print(edge_type)
                ta.add(edge_type)
                if usr1 in gender_dict:
                    if usr2 in gender_dict:
                        if usr1 not in sender_count[2]:
                            sender_count[2][usr1] = 1
                        else:
                            sender_count[2][usr1] += 1

                        if usr2 not in receiver_count[2]:
                            receiver_count[2][usr2] = 1
                        else:
                            receiver_count[2][usr2] += 1


print("total sender : ", len(se_dict))
se_fe = 0
for usr in se_dict:
    if se_dict[usr] == '2':
        se_fe += 1
print("female sender: ", se_fe)

print("total recieder : ", len(re_dict))
re_fe = 0
for usr in re_dict:
    if re_dict[usr] == '2':
        re_fe += 1
print("female receiver: ", re_fe)







print("comment sender count: ", len(sender_count[0]))
print("like sender count: ", len(sender_count[1]))
print("tag sender count: ", len(sender_count[2]))

print("comment receiver_dict count: ", len(receiver_count[0]))
print("like receier_count count: ", len(receiver_count[1]))
print("tag receivernosend count: ", len(receiver_count[2]))


re_female_count = [0,0,0]
re_male_count = [0,0,0]

se_female_count = [0,0,0]
se_male_count = [0,0,0]


for i in range(3):
    for usr in sender_count[i]:
        if gender_dict[usr] == '2':
            se_female_count[i] += 1
        else:
            se_male_count[i] += 1

    for usr in receiver_count[i]:
        if gender_dict[usr] == '2':
            re_female_count[i] += 1
        else:
            re_male_count[i] += 1

print("receiver")
print("comment female ratio: ", re_female_count[0]*1.0/len(receiver_count[0]))
print("like female ratio: ", re_female_count[1]*1.0/len(receiver_count[1]))
print("tag female ratio: ", re_female_count[2]*1.0/len(receiver_count[2]))

print("comment female : ", re_female_count[0])
print("like female : ", re_female_count[1])
print("tag female r: ", re_female_count[2])



print("sender")
print("comment female ratio: ", se_female_count[0]*1.0/len(sender_count[0]))
print("like female ratio: ", se_female_count[1]*1.0/len(sender_count[1]))
print("tag female ratio: ", se_female_count[2]*1.0/len(sender_count[2]))


print("comment female : ", se_female_count[0])
print("like female : ", se_female_count[1])
print("tag female r: ", se_female_count[2])





'''
for usr in gender_dict:
    usr_g = gender_dict[usr]
    #insert one-hot label
    out = ()
    out.append(usr)
    for i in range(len(gender_dict)):
        if 
        out.append(0)
    line2write.append((usr , usr_g))

with open(OUTPUT_DIR, 'w') as writefile:
    writer = csv.writer(writefile)
    for line in line2write:
        writer.writerow(line)

'''


'''
      

line2write = []
OUTPUT_DIR = 'students_edges_all.csv'

types = ["comment" , "like" , "tag"]
comment_set = set(output_list[0].keys())
like_set = set(output_list[1].keys())
tag_set = set(output_list[2].keys())
keys = comment_set.union(like_set , tag_set)



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

    interact_num = comment_num + like_num + tag_num

    usr2 = edge[0]
    usr1 = edge[1]

    line2write.append((id_dict[usr2], gender_dict[usr2], id_dict[usr1], gender_dict[usr1], comment_num, like_num, tag_num, interact_num))

OUTPUT_DIR = 'students_edges_all.csv'
with open(OUTPUT_DIR, 'w') as writefile:
    writer = csv.writer(writefile)
    for line in line2write:
        writer.writerow(line)
'''


'''
line2write = []
types = ["comment" , "like" , "tag"]

indegree_list=[]

for i in range(3):
    for edge in output_list[i].keys():
        interaction_num = output_list[i][edge]
        usr1 = edge[0]
        usr2 = edge[1]
        indegree_list.append(usr2)
        line2write.append((id_dict[usr1], id_dict[usr2], interaction_num))

    for usr in gender_dict:
        if usr not in indegree_list:
            line2write.append((id_dict[usr], id_dict[usr], 0.001))

    indegree_list=[]

    OUTPUT_DIR = 'only_post/students_edges_{}.csv'.format(types[i])
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













