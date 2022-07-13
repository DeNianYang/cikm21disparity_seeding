# # female_ratio
# fr = 59.7/(59.7+40.3)
# # male_ratio
# mr = 1 - fr
# seeds = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
import sys
import numpy as np
seeds = [25]
types = ['tag']
#gender_dict = {}
#FILE_DIR = '../../../dataset_2015/dataset_remove1interaction/1_stat_user1.csv'
line2write=[]
FILE_DIR = 'sorted_file/target_hindex_{}_{}.csv'
'''
with open(FILE_DIR, 'r') as read_file:
    for line in read_file:
        token = line.strip().split(',')
        senderId = token[0]
        senderGen = int(token[1])
        receiverId = token[2]
        receiverGen = int(token[3])
        if senderId not in gender_dict: gender_dict[senderId] = senderGen
        if receiverId not in gender_dict: gender_dict[receiverId] = receiverGen
'''
for ratio in range(26):
    # male_ratio
    fr = ratio/25
    # female_ratio
    mr = 1-fr
    for s in seeds:
        FILE_DIR = 'sorted_file/target_hindex_{}_{}.csv'
        FILE_WRITE = 'dataset/target_hindex-{}-{}.csv'
        for byType in range(1):
            #FILE_DIR = 'sorted_file/target_hindex_{}_{}.csv'
            user_list=[]
            fs = int(np.round(s * fr, 0))
            #ms = int(np.round(s * mr, 0))
            ms = s - fs
            with open(FILE_DIR.format(types[byType], ratio/25), 'r') as read_file:
                for line in read_file:
                    token = line.strip().split(',')
                    userId = token[0]
                    userGen = int(token[1])
                    if fs or ms:
                        if userGen == 1 and ms: 
                            user_list.append(userId)
                            ms-=1
                        elif userGen == 2 and fs: 
                            user_list.append(userId)
                            fs-=1
                        else: pass
                    else: break
            with open(FILE_WRITE.format(s, ratio/25), 'w+b') as write_file:
                for user in user_list:
                    toWrite = user+'\n'
                    write_file.write(toWrite.encode('utf-8'))
            
