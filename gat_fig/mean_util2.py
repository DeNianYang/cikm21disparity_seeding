import networkx as nx
import pandas as pd
import csv
import os
import math
import time

import matplotlib.pyplot as plt
import numpy as np

def mean(gender_list):
    return int(sum(gender_list))/int(len(gender_list))


sort_number = [0,1,2]
types = ['comment', 'like', 'tag']
cate = ['indegree', 'outdegree', 'intesnity', 'intensity_sent']



for s in sort_number:

    FILE_DIR = 'students_indegree_{}.csv'

    FILE_WRITE = 'students_indegree_{}_mean_result.txt'

    male_measurement_list = []
    female_measurement_list = []

    with open(FILE_DIR.format(types[s]), 'r') as read_file:
        for line in read_file:
            token = line.strip().split(",")

            #if(float(token[1]) == 0 or float(token[2]) == 0):
                #pass
            #else:
            user_gender = token[1]
            if(int(user_gender) == 1):
                measurement = token[2]
                male_measurement_list.append(int(measurement))
            elif(int(user_gender) == 2):
                measurement = token[2]
                female_measurement_list.append(int(measurement))

    male_mean = mean(male_measurement_list)
    female_mean = mean(female_measurement_list)

    male_mean = round(male_mean, 2)
    female_mean = round(female_mean, 2)

    with open(FILE_WRITE.format(s), 'w') as write_file:

        write_file.write(str(male_mean))
        write_file.write(",")
        write_file.write(str(female_mean))
        #write_file.write(",")
