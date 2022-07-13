# seeds = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
seeds = [5,10,20,50,100]
seeds_100 = [100]
#compute_ratio = [[0,0],[0,0],[0,0]]
#compute_ratio_l = [0,0]
#compute_ratio_t = [0,0]
for s in seeds_100:
    FILE_DIR = '../../indegree/students_indegree_{}.csv'
    FILE_WRITE = 'dataset/agnostic-{}-{}-{}.csv'
    for byType in range(3):
        compute_ratio = [[0,0],[0,0],[0,0]]
        for ratio in range(11):
            user_list = []
            with open(FILE_DIR.format(byType), 'r') as read_file:
                for idx, line in enumerate(read_file):
                    token = line.strip().split(',')
                    userId = token[0]
                    user_list.append(userId)
                    
                    compute_ratio[byType][int(token[1])-1] += 1
                        
                    if idx == s-1: break

            if byType == 0: seedfile = 'agnosticc'
            elif byType == 1: seedfile = 'agnosticl'
            elif byType == 2: seedfile = 'agnostict'
            with open(FILE_WRITE.format(seedfile, s, ratio/10), 'w+b') as write_file:
                for user in user_list:
                    toWrite = user+'\n'
                    write_file.write(toWrite.encode('utf-8'))

            print(byType, compute_ratio)
            
