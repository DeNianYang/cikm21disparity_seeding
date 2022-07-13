# female_ratio
fr = 59.1/(59.1+40.9)
# male_ratio
mr = 1 - fr
seeds = [5,10,20,50,100]
seeds_100 = [100]
target_ratio = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
ago_ratio = [0.61,0.5,0.68]
gender_dict = {}
FILE_DIR = '../../students_labels.csv'

with open(FILE_DIR, 'r') as read_file:
    for line in read_file:
        token = line.strip().split(',')
        senderId = token[0]
        senderGen = int(token[1])
        #receiverId = token[2]
        #receiverGen = int(token[3])
        if senderId not in gender_dict: gender_dict[senderId] = senderGen
        #if receiverId not in gender_dict: gender_dict[receiverId] = receiverGen

for s in seeds_100:
    FILE_DIR = '../../indegree/students_indegree_{}.csv'
    FILE_WRITE = 'parity-{}-{}-{}.csv'
    for i in range(11):
        for byType in range(3):
            user_list = []
            fr = target_ratio[i]
            mr = 1.0-fr
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
            if byType == 0: seedfile = 'new_parityc'
            elif byType == 1: seedfile = 'new_parityl'
            else: seedfile = 'new_parityt'

            with open(FILE_WRITE.format(seedfile, s, target_ratio[i] ), 'w+b') as write_file:
                for user in user_list:
                    toWrite = user+'\n'
                    write_file.write(toWrite.encode('utf-8'))
     
