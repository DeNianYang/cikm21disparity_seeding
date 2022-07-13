# # female_ratio
# fr = 59.7/(59.7+40.3)
# # male_ratio
# mr = 1 - fr
# seeds = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
import sys
seeds = list(map(int, sys.argv[1:]))
gender_dict = {}
FILE_DIR = '../../../dataset_2015/dataset_remove1interaction/1_stat_user1.csv'

with open(FILE_DIR, 'r') as read_file:
    for line in read_file:
        token = line.strip().split(',')
        senderId = token[0]
        senderGen = int(token[1])
        receiverId = token[2]
        receiverGen = int(token[3])
        if senderId not in gender_dict: gender_dict[senderId] = senderGen
        if receiverId not in gender_dict: gender_dict[receiverId] = receiverGen

for ratio in range(11):
    # male_ratio
    mr = ratio/10
    # female_ratio
    fr = 1-mr
    for s in seeds:
        FILE_DIR = '../../dataset/seed_selection/remove1interaction/pagerank/Pagerank_sort_{}.csv'
        FILE_WRITE = '../../dataset/seed_selection/remove1interaction/diversity/diversity-{}-{}-{}.csv'
        for byType in range(2):
            user_list = []
            fs = round(s * fr, 0)
            ms = round(s * mr, 0)
            with open(FILE_DIR.format(byType), 'r') as read_file:
                for line in read_file:
                    token = line.strip().split(',')
                    userId = token[0]
                    userGen = int(gender_dict[userId])
                    if fs or ms:
                        if userGen == 1 and ms: 
                            user_list.append(userId)
                            ms-=1
                        elif userGen == 2 and fs: 
                            user_list.append(userId)
                            fs-=1
                        else: pass
                    else: break
            if byType == 0: seedfile = 'pagerankl'
            elif byType == 1: seedfile = 'pagerankc'
            with open(FILE_WRITE.format(seedfile, s, ratio/10), 'w+b') as write_file:
                for user in user_list:
                    toWrite = user+'\n'
                    write_file.write(toWrite.encode('utf-8'))
            