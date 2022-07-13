# # female_ratio
# fr = 59.7/(59.7+40.3)
# # male_ratio
# mr = 1 - fr
# seeds = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
import sys
import numpy as np
seeds = 25
#gender_dict = {}
#FILE_DIR = '../../../dataset_2015/dataset_remove1interaction/1_stat_user1.csv'
line2write=[]
#FILE_DIR = 'sorted_file/target_hindex_{}_{}.csv'


FILE_DIR = '../../intensity/students_intensity_tag.csv'
FILE_WRITE = 'data/intensity-agnostic.csv'
#FILE_DIR = 'sorted_file/target_hindex_{}_{}.csv'
user_list=[]
m = 0
f = 0
with open(FILE_DIR, 'r') as read_file:
    for line in read_file:
        token = line.strip().split(',')
        userId = token[0]
        userGen = int(token[1])
        if seeds:
            if userGen == 1:
                m+=1
            else:
                f+=1
            user_list.append(userId)
            seeds -= 1
        else: break
with open(FILE_WRITE, 'w+b') as write_file:
    for user in user_list:
        toWrite = user+'\n'
        write_file.write(toWrite.encode('utf-8'))
print(m) # 5
print(f) # 20
            
