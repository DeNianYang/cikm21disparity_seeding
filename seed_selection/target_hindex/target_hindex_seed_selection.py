import numpy as np
import csv
import os
import pandas as pd
import math
import time
# seeds = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
seeds = [25]
types = ['tag']
#for s in seeds:
FILE_DIR_1 = '../../hindex/{}_hi_index.csv'
FILE_DIR_2 = '../../target_hindex/fb_ratio_{}.csv'

original_score=[{},{},{}]
female_ratio=[{},{},{}]
final_score_0=[{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}]
final_score_1=[{},{},{},{},{},{},{},{},{},{},{}]
final_score_2=[{},{},{},{},{},{},{},{},{},{},{}]

gender_dict={}
with open(FILE_DIR_1.format(types[0], 'r')) as read_file:
    for line in read_file:
        token = line.strip().split(',')
        usr = token[0]
        usr_g = token[1]
        gender_dict[usr] = usr_g
 


for i in range(1):

    with open(FILE_DIR_1.format(types[i]), 'r') as read_file:
        for line in read_file:
            token = line.strip().split(',')
            usr = token[0]
            original_score[i][usr] = int(token[1])
    
    with open(FILE_DIR_2.format(types[i], 'r')) as read_file:
        for line in read_file:
            token = line.strip().split(',')
            usr = token[0]
            female_ratio[i][usr] = float(token[1])
    
    for user in female_ratio[i]:
        for ratio in range(26):
            if i == 0:
                final_score_0[ratio][user] = float(original_score[i][user]) * (1.0 - np.absolute(float(female_ratio[i][user] - ratio * 1.0/25)))
            elif i == 1:
                final_score_1[ratio][user] = float(original_score[i][user]) * (1.0 - np.absolute(float(female_ratio[i][user] - ratio * 1.0/10)))
            elif i == 2:
                final_score_2[ratio][user] = float(original_score[i][user]) * (1.0 - np.absolute(float(female_ratio[i][user] - ratio * 1.0/10)))
 
 


print(final_score_0[3])


OUT_DIR = 'sorted_file/target_hindex_{}_{}.csv'
line2write=[]
for ratio in range(26):
    for ty in range(1):
       if ty == 0:
           sorted_list = sorted(final_score_0[ratio].items(), key=lambda x: x[1],reverse=True) 
       elif ty == 1:
           sorted_list = sorted(final_score_1[ratio].items(), key=lambda x: x[1],reverse=True) 
 
       elif ty == 2:
           sorted_list = sorted(final_score_2[ratio].items(), key=lambda x: x[1],reverse=True) 
 
       for pair in sorted_list:
           line2write.append((pair[0], gender_dict[pair[0]],pair[1]))
       with open(OUT_DIR.format(types[ty],ratio/25),'w' ) as writefile:
           writer = csv.writer(writefile)
           for line in line2write:
               writer.writerow(line)

       line2write=[]
    
'''

for s in seeds:
    FILE_WRITE = 'dataset/target_hindex-{}-{}-{}.csv'


    for byType in range(3):
        for ratio in range(11):
            user_list = []
            with open(FILE_DIR.format(byType), 'r') as read_file:
                for idx, line in enumerate(read_file):
                    token = line.strip().split(',')
                    userId = token[0]
                    user_list.append(userId)
                    if idx == s-1: break

            if byType == 0: seedfile = 'agnosticc'
            elif byType == 1: seedfile = 'agnosticl'
            elif byType == 2: seedfile = 'agnostict'
            with open(FILE_WRITE.format(seedfile, s, ratio/10), 'w+b') as write_file:
                for user in user_list:
                    toWrite = user+'\n'
                    write_file.write(toWrite.encode('utf-8'))
 

'''           
