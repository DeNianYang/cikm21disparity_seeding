# # female_ratio
# fr = 59.7/(59.7+40.3)
# # male_ratio
# mr = 1 - fr
# seeds = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
import sys
seeds = [25]
types = ['comment', 'like', 'tag']
#gender_dict = {}
#FILE_DIR = '../../../dataset_2015/dataset_remove1interaction/1_stat_user1.csv'
line2write=[]
FILE_DIR = 'sorted_file/pagerank_{}_{}.csv'
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

tt = ['c', 'l', 't']



#for ratio in range(11):
    #for s in seeds:
        #FILE_WEIGHT = 'weight_{}_target_hindex{}.csv'

    	#with open(FILE_WEIGHT.format(s, tt[]))
    # male_ratio
    #fr = ratio/10
    # female_ratio
    #mr = 1-fr



for s in seeds:
    
    FILE_DIR = 'sorted_file/target_hindex_{}_{}.csv'
    FILE_WRITE = 'new_dataset/target_hindex3-{}-{}-{}.csv'

    #FILE_WEIGHT = 'weight_{}_target_hindex{}.csv'
    
    for byType in range(3):
        FILE_WEIGHT = 'brand_weight/weight3_{}_target_hindex{}.csv'
        with open(FILE_WEIGHT.format(s, tt[byType]), 'r') as read_file:
            fr_list = []
            mr_list = []
            for line in read_file:
                token = line.strip().split(',')
              
                fr = float(token[1])
                #print(fr)
                if fr <0:
                    fr = 0.0
                elif fr >1.0:
                    fr=1.0
                mr = 1.0-fr

                fr_list.append(fr)
                mr_list.append(mr)



        #FILE_DIR = 'sorted_file/target_hindex_{}_{}.csv'
        for ratio in range(11):
            user_list=[]
            fs = round(s * fr_list[ratio], 0)
            ms = round(s * mr_list[ratio], 0)
            print(fs)
            print(ms)
            with open(FILE_DIR.format(types[byType], ratio/10), 'r') as read_file:
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
            if byType == 0: seedfile = 'target_hindexc'
            elif byType == 1: seedfile = 'target_hindexl'
            elif byType ==2: seedfile = 'target_hindext'
            with open(FILE_WRITE.format(seedfile, s, ratio/10), 'w+b') as write_file:
                for user in user_list:
                    toWrite = user+'\n'
                    write_file.write(toWrite.encode('utf-8'))
            
