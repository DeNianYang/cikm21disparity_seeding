import sys
import math 
import random
import statistics
import more_itertools as mit
import networkx as nx
import pandas as pd
import csv
import os
import math
import time
from collections import OrderedDict
from math import log
import numpy as np




seeds = [5,10,20,50,100]
seeds100=[100]
measurement = ['pagerank','target_hindex', 'influence_net','agnostic','new_parity']
measurement_r = ['parity']
network = ['comment', 'like', 'tag']
st = ['c','l','t']

ratio = [0.0 ,0.1 ,0.2 ,0.3 ,0.4 ,0.5 ,0.6 ,0.7 ,0.8 ,0.9 ,1.0]


FILE_DIR_R = '../seed_selection/{}/output/{}.csv_{}-{}{}-{}.csv.out'
#tag.csv_agnostic-agnostict-50-0.9.csv.out
FILE_DIR = '../seed_selection/{}/output/{}.csv_{}-{}{}-{}-{}.csv.out'

FILE_DIR_inf = '../seed_selection/{}/final_workspace/output/{}.csv_{}-{}{}-{}-{}.csv.out'
OUT_DIR = 'result_{}.csv'


line2write=[]
#5*5*3*10 = 750 in result
#150 in each result_{}
for s in seeds100:

    line2write=[]
    for measure in measurement:
        if measure == 'agnostic':
            for byType in range(3):
            
                with open(FILE_DIR.format(measure, network[byType], measure,
                    measure, st[byType], s, '0.4')) as file_read:


                    for line in file_read:

                        token = line.strip().split('\t')

                        spread_m = float(token[0])
                        spread_f = float(token[1])
                        out_string = network[byType]+'\t'+measure+st[byType]+'-'+str(s)+'-'+str('0.4')+'.csv.out'+'\t'+'1000'+'\t' +str(spread_m) + '\t' + str(spread_f)
                        line2write.append(out_string)
                        break


        elif measure == 'influence_net':
            for byType in range(3):
                for rat in ratio:

                    with open(FILE_DIR_inf.format(measure, network[byType], measure,
                        measure, st[byType], s, rat)) as file_read:


                        for line in file_read:

                            token = line.strip().split('\t')

                            spread_m = float(token[0])
                            spread_f = float(token[1])
                            out_string = network[byType]+'\t'+measure+st[byType]+'-'+str(s)+'-'+str(rat)+'.csv.out'+'\t'+'1000'+'\t' +str(spread_m) + '\t' + str(spread_f)
                            line2write.append(out_string)


        else:

            for byType in range(3):
                for rat in ratio:

                    with open(FILE_DIR.format(measure, network[byType], measure,
                        measure, st[byType], s, rat)) as file_read:


                        for line in file_read:

                            token = line.strip().split('\t')

                            spread_m = float(token[0])
                            spread_f = float(token[1])
                            out_string = network[byType]+'\t'+measure+st[byType]+'-'+str(s)+'-'+str(rat)+'.csv.out'+'\t'+'1000'+'\t' +str(spread_m) + '\t' + str(spread_f)
                            line2write.append(out_string)

    for byType in range(3):
        for measure in measurement_r:

            with open(FILE_DIR_R.format(measure, network[byType], measure,
                    measure, st[byType], s)) as file_read:


                    for line in file_read:

                        token = line.strip().split('\t')

                        spread_m = float(token[0])
                        spread_f = float(token[1])
                        out_string = network[byType]+'\t'+measure+st[byType]+'-'+str(s)+'-'+str(0.5)+'.csv.out'+'\t'+'1000'+'\t' +str(spread_m) + '\t' + str(spread_f)
                        line2write.append(out_string)





    with open(OUT_DIR.format(s), 'w') as writefile:
            #writer = csv.writer(writefile)
            for line in line2write:
                writefile.write(line)
                writefile.write("\n")




