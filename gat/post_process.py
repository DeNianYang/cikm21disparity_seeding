import networkx as nx
import pandas as pd
import csv
import os
import math
import time
from collections import OrderedDict



file = '../only_post/students_labels.csv'

#edge type
byType = ["\"post_comment\"" , "\"post_like\"" , "\"post_tag\"" , "\"uploaded_photos_comment\"" , "\"uploaded_photos_likes\"" , "\"uploaded_photos_tags\"" , "\"tagged_photos_comments\"" , "\"tagged_photos_likes\"" , "\"tagged_photos_tags\""]

post_type = ["\"post_comment\"" , "\"post_like\"" , "\"post_tag\""]


# read in profile
gender_dict={}
with open(file, 'r') as read_file:
    for line in read_file:
        token = line.strip().split(",")
        usr = token[0]
        usr_g = token[-1]

        if usr not in gender_dict:
            gender_dict[usr] = usr_g

file_name=['old_gat_comment.csv', 'old_gat_like.csv', 'old_gat_tag.csv', 'influence_net_comment.csv', 'influence_net_like.csv', 'influence_net_tag.csv']

for files in file_name:
    line2write = []
    with open(files, 'r') as read_file:
        for line in read_file:
            token = line.strip().split(",")
            usr = token[0]
            val = token[1]
            line2write.append((usr, gender_dict[usr], val))



    OUTPUT_DIR = 'sorted_file/{}'.format(files)
    with open(OUTPUT_DIR, 'w') as writefile:
        writer = csv.writer(writefile,delimiter=",")
        for line in line2write:
            writer.writerow(line)



