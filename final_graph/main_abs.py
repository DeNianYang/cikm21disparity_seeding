import sys
import math 
import random
import statistics
import more_itertools as mit
from math import log
import numpy as np
from bokeh.io import curdoc, export_svgs
from bokeh.layouts import row, column
from bokeh.models import Legend, ColumnDataSource
from bokeh.plotting import figure, show, output_file
from bokeh.models.markers import Circle

all_seed = ['5','10','20','50','100']

FILE_READ = 'newfile2.csv'
# like and comment
male_spread_list = [[[] for j in range(6)] for i in range(6)]
female_spread_list = [[[] for j in range(6)] for i in range(6)]

for algo in range(6):

    #if algo == 0: algo_str = 'none'
    if algo == 0: algo_str = 'target_hindex'
    elif algo == 1: algo_str = 'pagerank'
    elif algo == 2: algo_str = 'influence_net'
    elif algo == 3: algo_str = 'new_parity'
    elif algo == 4: algo_str = 'im'
    elif algo == 5: algo_str = 'agnostic'

    
    male = [[0.0 for j in range(11)] for i in range(3)]
    female = [[0.0 for j in range(11)] for i in range(3)]

    with open(FILE_READ) as file_read:
        for line in file_read:
            token = line.strip().split('\t')
            if len(token) == 1:
                token = line.strip().split()
            #print(token)
            if int(token[2]) == 1000:
                if algo_str in token[1]:

                    if algo == 6:
                        if token[0] == 'comment':
                            if algo_str in token[1]:
                                male[0] = [float(token[3]) for _ in range(11)]
                                female[0] = [float(token[4]) for _ in range(11)]
                        elif token[0] == 'like':
                            if algo_str in token[1]: 
                                male[1] = [float(token[3]) for _ in range(11)]
                                female[1] = [float(token[4]) for _ in range(11)]
                        elif token[0] == 'tag':
                            if algo_str in token[1]: 
                                male[2] = [float(token[3]) for _ in range(11)]
                                female[2] = [float(token[4]) for _ in range(11)]

                        
                    else:
                        
                        ratio_sub = token[1].split('-')[2].split('.')
                        ratio = float(ratio_sub[0]+"."+ratio_sub[1])
                        if token[0] == 'comment':
                            if algo_str in token[1]:
                                male[0][int(ratio*10)] = float(token[3])
                                female[0][int(ratio*10)] = float(token[4])
                        elif token[0] == 'like':
                            if algo_str in token[1]: 
                                male[1][int(ratio*10)] = float(token[3])
                                female[1][int(ratio*10)] = float(token[4])

                        elif token[0] == 'tag':
                            if algo_str in token[1]: 
                                male[2][int(ratio*10)] = float(token[3])
                                female[2][int(ratio*10)] = float(token[4])
        
    male_spread_list[0][algo] = male[0]
    female_spread_list[0][algo] = female[0]
    male_spread_list[1][algo] = male[1]
    female_spread_list[1][algo] = female[1]
    male_spread_list[2][algo] = male[2]
    female_spread_list[2][algo] = female[2]
'''  
for lst in male_spread_list:
    for l in lst:
        print(l)
'''
# like and comment
# ratio and spread
data_retrival = [[[[] for j in range(6)] for i in range(2)] for k in range(3)]
for byType in range(3):
    for algo in range(6):
        for idx in range(11):
            male_spread = male_spread_list[byType][algo][idx]
            female_spread = female_spread_list[byType][algo][idx]
            
            data_retrival[byType][0][algo].append(female_spread/(male_spread+female_spread))
            data_retrival[byType][1][algo].append(male_spread+female_spread)
        
def spread_compare(lst, com, idx):
    max = 0
    for algo in range(6):
        if lst[algo][idx] > max: max = lst[algo][idx]
    if max == com: return True
    else: return False
        


def plotting(action_retrival, action_str):
    p1 = figure(
        plot_width=600, plot_height=500,
        y_range=(0, 0.55),
        x_range=(0, 1),
        y_axis_label='Absolute error',
        x_axis_label='Target Ratio(Female)'
        )
    
    x1 = []
    y1 = []
    idx1 = []    
    x2 = []
    y2 = []
    idx2 = []    
    x3 = []
    y3 = []
    idx3 = []
    x4 = []
    y4 = []
    idx4 = []
    x5 = []
    y5 = []
    idx5 = []
    x6 = []
    y6 = []
    idx6 = []
   
    paras2save = [[] for _ in range(6)]
    
    PF = 1.0
    #print(action_retrival[1])
    for i in range(11):
        # radius

        #action_retrival[1][0][i] = 0
        #modifedddddd
        if (i/10-PF)<action_retrival[0][0][i]<(i/10+PF): pass
        else: action_retrival[1][0][i] = 0

        if (i/10-PF)<action_retrival[0][1][i]<(i/10+PF): pass
        else: action_retrival[1][1][i] = 0

        if (i/10-PF)<action_retrival[0][2][i]<(i/10+PF): pass
        else: action_retrival[1][2][i] = 0

        if (i/10-PF)<action_retrival[0][3][i]<(i/10+PF): pass
        else: action_retrival[1][3][i] = 0

        if (i/10-PF)<action_retrival[0][4][i]<(i/10+PF): pass
        else: action_retrival[1][4][i] = 0

        if (i/10-PF)<action_retrival[0][5][i]<(i/10+PF): pass
        else: action_retrival[1][5][i] = 0
        
        # x
        #if action_retrival[0][0][i] == 0 or action_retrival[0][1][i] == 0 or action_retrival[0][2][i] == 0 or action_retrival[0][3][i] == 0 or action_retrival[0][4][i] == 0 :pass
        #or action_retrival[0][5][i] == 0
        #: pass
        #else: 
        idx1.append(i/10)
        y1.append(abs(float(action_retrival[0][0][i])-i/10))
        #paras2save[0].append([action_retrival[0][0][i], (action_retrival[0][0][i])*(i/(10*action_retrival[0][0][i]))])
        
        idx2.append(i/10)
        y2.append(abs(float(action_retrival[0][1][i])-i/10))
        #paras2save[1].append([action_retrival[0][1][i], (action_retrival[0][1][i])*(i/(10*action_retrival[0][1][i]))])
            

        idx3.append(i/10)
        y3.append(abs(float(action_retrival[0][2][i])-i/10))
        #paras2save[2].append([action_retrival[0][2][i], (action_retrival[0][2][i])*(i/(10*action_retrival[0][2][i]))])
        
        idx4.append(i/10)
        y4.append(abs(float(action_retrival[0][3][i])-i/10))
        #paras2save[3].append([action_retrival[0][3][i], (action_retrival[0][3][i])*(i/(10*action_retrival[0][3][i]))])

        idx5.append(i/10)
        y5.append(abs(float(action_retrival[0][4][i])-i/10))
        #paras2save[4].append([action_retrival[0][4][i], (action_retrival[0][4][i])*(i/(10*action_retrival[0][4][i]))])

        idx6.append(i/10)
        y6.append(abs(float(action_retrival[0][5][i])-i/10))
        #paras2save[5].append([action_retrival[0][5][i], (action_retrival[0][5][i])*(i/(10*action_retrival[0][5][i]))])

    print(action_str)
    print(idx1)
    print(y1)
    print(idx2)
    print(y2)
    print(idx3)
    print(y3)
    print(idx4)
    print(y4)
    print(idx5)
    print(y5)
    print(idx6)
    print(y6)
    
    for i in range(11):
        if spread_compare(action_retrival[1], action_retrival[1][0][i], i):
            x1.append(action_retrival[1][0][i])
        else: x1.append(0)
        if spread_compare(action_retrival[1], action_retrival[1][1][i], i):
            x2.append(action_retrival[1][1][i])
        else: x2.append(0)
        if spread_compare(action_retrival[1], action_retrival[1][2][i], i):
            x3.append(action_retrival[1][2][i])
        else: x3.append(0)
        if spread_compare(action_retrival[1], action_retrival[1][3][i], i):
            x4.append(action_retrival[1][3][i])
        else: x4.append(0)
        if spread_compare(action_retrival[1], action_retrival[1][4][i], i):
            x5.append(action_retrival[1][4][i])
        else: x5.append(0)
        if spread_compare(action_retrival[1], action_retrival[1][5][i], i):
            x6.append(action_retrival[1][5][i])
        else: x6.append(0)
        

    #print("{}, {}, {}, {}, {}".format(statistics.mean(x1), statistics.mean(x2), statistics.mean(x3), statistics.mean(x4), statistics.mean(x5)))
    '''
    idx1 = [idx for idx in idx1]
    y1 = [y for y in y1]
    idx2 = [idx for idx in idx2]
    y2 = [y for y in y2]
    idx3 = [idx for idx in idx3]
    y3 = [y for y in y3]
    idx4 = [idx for idx in idx4]
    y4 = [y for y in y4]
    idx5 = [idx for idx in idx5]
    y5 = [y for y in y5]
    '''
    #idx6 = [1-idx for idx in idx6]
    #y6 = [1-y for y in y6]

    
    data = {'x': idx1, 'y': y1, 'radius': [y/5000 for y in x1]}
    data1 = {'x': idx2, 'y': y2, 'radius': [y/5000 for y in x2]}
    data2 = {'x': idx3, 'y': y3, 'radius': [y/5000 for y in x3]}
    data3 = {'x': idx4, 'y': y4, 'radius': [y/5000 for y in x4]}
    data4 = {'x': idx5, 'y': y5, 'radius': [y/5000 for y in x5]}
    data5 = {'x': idx6, 'y': y6, 'radius': [y/5000 for y in x6]}

    source = ColumnDataSource(data)
    source1 = ColumnDataSource(data1)
    source2 = ColumnDataSource(data2)
    source3 = ColumnDataSource(data3)
    source4 = ColumnDataSource(data4)
    source5 = ColumnDataSource(data5)
    
    #p1.circle(x='x', y='y', radius='radius', color='red', alpha=0.5, source=source)
    p1.line(idx1, y1, line_width=5, color='red', line_dash="4 4")
    
    #p1.circle(x='x', y='y', radius='radius', color='black', alpha=0.5, source=source1)
    #p1.line(idx2, y2, line_width=5, color='black', line_dash="4 4")

    #p1.circle(x='x', y='y', radius='radius', color='green', alpha=0.5, source=source2)
    p1.line(idx3, y3, line_width=5, color='green', line_dash="4 4")

    #p1.circle(x='x', y='y', radius='radius', color='yellow', alpha=0.5, source=source3)
    p1.line(idx4, y4, line_width=5, color='orange', line_dash="4 4")

    #p1.circle(x='x', y='y', radius='radius', color='purple', alpha=0.5, source=source4)
    p1.line(idx5, y5, line_width=5, color='purple', line_dash="4 4")
    
    #p1.circle(x='x', y='y', radius='radius', color='purple', alpha=0.5, source=source5)
    p1.line(idx6, y6, line_width=5, color='black', line_dash="4 4")

    # p1.line([0,1], [0,1], line_width=5, color='purple')
    # p1.line([PF,1], [0,1-PF], line_width=5, color='purple')
    # p1.line([0,1-PF], [PF,1], line_width=5, color='purple')

    #p1.varea(x=[0, 1], y1=[PF, 1+PF], y2=[-PF, 1-PF], alpha=0.25, color='gray', legend_label='Error Margins ±{}%'.format(round(PF*100)))
    
    # p1.ray(('x', 1),('y', 1),length=10e7, angle=np.pi/4, line_color="black", line_dash="4 4")

    #p1.legend.location = "bottom_right"
    #p1.legend.label_text_font_size = '26pt'
    # p1.legend.visible = False
    p1.xaxis.axis_label_text_font_size = "26pt"
    p1.yaxis.axis_label_text_font_size = "26pt"
    p1.xaxis.major_label_text_font_size = "26px"
    p1.yaxis.major_label_text_font_size = "26px"
    p1.output_backend = "svg"
    export_svgs(p1, filename="fig_abs/fb_new_parento_frontier_{}_{}_100.svg".format(action_str, PF))
    return p1, paras2save

plots = {'like': {}, 'comment': {}, 'tag':{}}
paras = [{},{},{}]
for byType in range(3):
    if byType == 0: action_str = "Comment"
    elif byType == 1: action_str = "Like"
    elif byType == 2: action_str = "Tag"
    plots[byType], paras[byType] = plotting(data_retrival[byType], action_str)

'''
for byType in range(3):
    for algo in range(5):


        if algo == 1: algo_str = 'target_hindex'
        elif algo == 2: algo_str = 'pagerank'
        elif algo == 3: algo_str = 'influence_net'
        elif algo == 4: algo_str = 'parity'
        elif algo == 5: algo_str = 'agnostic'
        
        with open("./dataset/discount_factor_train/weight/weight_{}_{}.txt".format(algo_str, byType), 'w') as write_file:
            for i in range(len(paras[byType][algo])):
                write_file.write("{},{}\n".format(paras[byType][algo][i][0], paras[byType][algo][i][1]))
    
'''

p = row(plots[0], plots[1])
curdoc().add_root(p)
curdoc().title = "Discount Factor"
