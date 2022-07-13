# # female_ratio
# fr = 59.7/(59.7+40.3)
# # male_ratio
# mr = 1 - fr
# seeds = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
import sys
seeds = [5,10,20,50,100]
types = ['comment', 'like', 'tag']
#gender_dict = {}
#FILE_DIR = '../../../dataset_2015/dataset_remove1interaction/1_stat_user1.csv'
line2write=[]
#FILE_DIR = 'sorted_file/influence_net_{}_{}.csv'
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
    
    FILE_DIR = '../../gat/sorted_file/influence_net_{}.csv'
    FILE_WRITE = 'final_trial_2_dataset/influence_net-{}-{}-{}.csv'

    #FILE_WEIGHT = 'weight_{}_target_hindex{}.csv'
    
    for byType in range(3):
        FILE_WEIGHT = 'weight_{}_influence_net{}.csv'
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
            with open(FILE_DIR.format(types[byType]), 'r') as read_file:
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
            if byType == 0: seedfile = 'influence_netc'
            elif byType == 1: seedfile = 'influence_netl'
            elif byType ==2: seedfile = 'influence_nett'
            with open(FILE_WRITE.format(seedfile, s, ratio/10), 'w+b') as write_file:
                for user in user_list:
                    toWrite = user+'\n'
                    write_file.write(toWrite.encode('utf-8'))
            
