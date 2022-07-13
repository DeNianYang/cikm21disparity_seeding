# retrieving the csv file from task1
# user1_ID, user1_gender, user2_ID, user2_gender, #likes, #comments, #interactions,
# interv_like, interv_comment, interv_interaction\n

import csv
import math
from collections import OrderedDict

FILE = '../intensity_sent/students_intensity_sent_{}.csv'
# testcases = ['nofilter', 'receivernosend', 'remove1interaction', 'bothcriteria']
#testcases = ['remove1interaction']

from os import listdir
from os.path import isfile, join

types = ['comment', 'like', 'tag']

#FILEDIR = '../only_post/students_edges_all.csv'
#file_length = len([f for f in listdir(FILEDIR) if isfile(join(FILEDIR, f))])
for byType in range(3):
    percentile_list = [{}, {}]
    sorted_percentile_list = [{}, {}]
    #for idx in range(file_length):
        #print("loading file{}...".format(idx))
    stats = csv.reader(open(FILE.format(types[byType])), delimiter=",")
    for line in stats:
        if line[1] == '1':
            if int(line[2]) not in percentile_list[0]:
                percentile_list[0][int(line[2])] = 1
            else:
                percentile_list[0][int(line[2])] += 1
            

        elif line[1] == '2':
            if int(line[2]) not in percentile_list[1]:
                percentile_list[1][int(line[2])] = 1
            else:
                percentile_list[1][int(line[2])] += 1
            

    sorted_percentile_list[0] = OrderedDict(sorted(percentile_list[0].items()))
    sorted_percentile_list[1] = OrderedDict(sorted(percentile_list[1].items()))
    male_last = next(reversed(sorted_percentile_list[0]))
    female_last = next(reversed(sorted_percentile_list[1]))
    if male_last < female_last:
        percentile_list[0][female_last] = 0
    else:            
        percentile_list[1][male_last] = 0
    
    sorted_percentile_list[0] = OrderedDict(sorted(percentile_list[0].items()))
    sorted_percentile_list[1] = OrderedDict(sorted(percentile_list[1].items()))

    # calculate the sum of gender
    s = [0,0]
    for gender in range(2):
        sum = 0
        tmp_line2write = []
        for k, v in sorted_percentile_list[gender].items():
            sum = sum + v
            tmp_line2write.append([k, sum])
        s[gender] = s[gender] + sum
    # print(s)

    # CCDF Calculation
    for gender in range(2):
        sum = 0
        line2write = []
        for k, v in sorted_percentile_list[gender].items():
            line2write.append([k, 1 - float(sum+v)/float(s[gender])])
            sum = sum + v
        OUTPUT_DIR = 'dataset/sorted_file_with_{}_{}.csv'.format(gender, byType)
        with open(OUTPUT_DIR, 'w') as writefile:
            writer = csv.writer(writefile)
            #print(line2write)
            for line in line2write:
                writer.writerow(line)




