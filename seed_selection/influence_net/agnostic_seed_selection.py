# seeds = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
seeds = [5,10,20,50,100]
avg = [0,1,2,3,4]
network = ['comment']
for case in avg:
	for s in seeds:
		FILE_DIR = '../../gat/influence_net_{}_{}.csv'
		FILE_WRITE = 'dataset_test/influenct_net-{}-{}-{}-{}.csv'
		for byType in range(1):
		#for ratio in range(11):
			user_list = []
			with open(FILE_DIR.format(network[byType], case), 'r') as read_file:
				for idx, line in enumerate(read_file):
					token = line.strip().split(',')
					userId = token[0]
					user_list.append(userId)
					if idx == s-1: break

			if byType == 0: seedfile = 'influence_netcc'
			elif byType == 1: seedfile = 'influence_netl'
			elif byType == 2: seedfile = 'influence-nett'
			with open(FILE_WRITE.format(case,seedfile, s, 0.0), 'w+b') as write_file:
				for user in user_list:
					toWrite = user+'\n'
					write_file.write(toWrite.encode('utf-8'))
		    
