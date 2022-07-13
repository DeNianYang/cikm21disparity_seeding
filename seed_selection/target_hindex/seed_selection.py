import numpy as np
import csv
import os
import pandas as pd
import math
import time
# seeds = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
seeds = [25]
types = ['comment', 'like', 'tag']
#for s in seeds:
line2write=[]
    
FILE_DIR = 'sorted_file/target_hindex_{}_{}.csv'

for s in seeds:
    FILE_WRITE = 'dataset/target_hindex-{}-{}-{}.csv'


    for byType in range(3):
        for ratio in range(11):
            user_list = []
            with open(FILE_DIR.format(types[byType], ratio/10), 'r') as read_file:
                for idx, line in enumerate(read_file):
                    token = line.strip().split(',')
                    userId = token[0]
                    user_list.append(userId)
                    if idx == s-1: break

            if byType == 0: seedfile = 'target_hindexc'
            elif byType == 1: seedfile = 'target_hindexl'
            elif byType == 2: seedfile = 'target_hindext'
            with open(FILE_WRITE.format(seedfile, s, ratio/10), 'w+b') as write_file:
                for user in user_list:
                    toWrite = user+'\n'
                    write_file.write(toWrite.encode('utf-8'))
 
           
