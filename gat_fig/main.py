from math import log
import math
import numpy as np
from math import log
from bokeh.io import curdoc, export_svgs
from bokeh.layouts import row, column
from bokeh.models import Legend
from bokeh.plotting import figure, show
from bokeh.models import BasicTickFormatter
from bokeh.models import DataRange1d

def plotting(action_retrival, action_str, testcase):
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"

    '''
    p1 = figure(
        # title="Testcase: {}".format(display, action_str), 
        tools=TOOLS, # y_range= (0.4, 1), 
        y_axis_label='CCDF', y_axis_type='log',
        x_axis_type='log', x_axis_label='Number of {}'.format(action_str))
    '''
    
    # p1.yaxis.formatter = BasicTickFormatter(use_scientific=True, power_limit_low=1)

    if action_str == "Comment - GAT":
        
        p1 = figure(
        # title="Testcase: {}".format(display, action_str), 
        tools=TOOLS,  #x_range=DataRange1d(end=2.5e-3)
        y_axis_label='CCDF', y_axis_type='log',
        x_axis_type='log')
     
    elif action_str == "Like - GAT":
        
        p1 = figure(
        # title="Testcase: {}".format(display, action_str), 
        tools=TOOLS,  #x_range=DataRange1d(end=3e-3)
        y_axis_label='CCDF', y_axis_type='log',
        x_axis_type='log')

    elif action_str == "Tag - GAT":
        p1 = figure(
        # title="Testcase: {}".format(display, action_str), 
        tools=TOOLS, #x_range=DataRange1d(end=2.5e-3)
        y_axis_label='CCDF', y_axis_type='log',
        x_axis_type='log')
    
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    for line in action_retrival[0]:
        if line[0] == 0: line[0] = 1
        x1.append(float(line[0]))
        y1.append(line[1])
    for line in action_retrival[1]:
        if line[0] == 0: line[0] = 1
        x2.append(float(line[0]))
        y2.append(line[1])
    p1.line(np.asarray(x1), np.asarray(y1), legend_label="male", line_color="blue")
    p1.line(np.asarray(x2), np.asarray(y2), legend_label="female", line_color="red")
    

    '''
    if action_str == 'Comment - Indegree': 
        p1.ray(('x', 175),('y', 0.064),length=10e7, angle=-np.pi/2, line_color="black", line_dash="4 4")
        p1.ray(('x', 175),('y', 0.064),length=10e7, angle=-np.pi, line_color="black", line_dash="4 4")
        p1.circle(x=[175], y=[0.064], size=6,line_color="black")
        x,y=245,120
        # cross_axis = '({}, {})'.format(740, '0.0155')

    elif action_str == 'Like - Indegree': 
        p1.ray(('x', 87.5),('y', 0.11),length=10e7, angle=-np.pi/2, line_color="black", line_dash="4 4")
        p1.ray(('x', 87.5),('y', 0.11),length=10e7, angle=-np.pi, line_color="black", line_dash="4 4")
        p1.circle(x=[87.5], y=[0.11], size=6,line_color="black")
        x,y=240,110
        # cross_axis = '({}, {})'.format(570, '0.004')

    elif action_str == 'Tag - Indegree': 
        p1.ray(('x', 87.5),('y', 0.11),length=10e7, angle=-np.pi/2, line_color="black", line_dash="4 4")
        p1.ray(('x', 87.5),('y', 0.11),length=10e7, angle=-np.pi, line_color="black", line_dash="4 4")
        p1.circle(x=[87.5], y=[0.11], size=6,line_color="black")
        x,y=240,110
    '''

    p1.legend.location = "bottom_left"
    p1.legend.label_text_font_size = '22pt'
    p1.xaxis.axis_label_text_font_size = "26pt"
    p1.yaxis.axis_label_text_font_size = "26pt"
    p1.xaxis.major_label_text_font_size = "26px"
    p1.yaxis.major_label_text_font_size = "26px"

    #p1.xaxis.major_label_orientation = math.pi/3

    '''
    if action_str == "Comment - GAT":
        p1.xaxis.ticker = [0.46, 0.48, 0.50, 0.52, 0.54]
        #x_range(0, 2.5e-3)
    elif action_str == "Like - GAT":
        p1.xaxis.ticker = [0.48, 0.50, 0.52, 0.54]
        #x_range(0, 3e-3)
    #elif action_str == "Tag - GAT":
        #p1.xaxis.ticker = [5e-4, 1e-3, 1.5e-3, 2e-3, 2.5e-3]
    '''


    p1.output_backend = "svg"
    export_svgs(p1, filename="fig/{}.svg".format(action_str))
    return p1



# testcases = ['nofilter', 'receivernosend', 'remove1interaction', 'bothcriteria']
testcases = ['remove1interaction']
testcase_plot = []
for testcase_idx in range(1):
    OPEN_DIR = 'dataset/sorted_file_with_{}_{}.csv'
    if testcases[testcase_idx] == 'nofilter': display = "Original Data Set"
    elif testcases[testcase_idx] == 'receivernosend': display = "Remove the receiver but not sender"
    elif testcases[testcase_idx] == 'remove1interaction': display = "Remove pairs with only one interaction"
    elif testcases[testcase_idx] == 'bothcriteria': display = "With both criteria"

    # data_retrival = [like, action, interact] {0, 1, 2}
    # like = [male, female] {0, 1}
    # male = [[#actions, cumulative of ppl]*n]
    data_retrival = [[[],[]],[[],[]],[[],[]]]
    for byType in range(3):
        for gender in range(2):
            with open(OPEN_DIR.format(gender, byType), 'r') as open_file:
                for line in open_file:
                    token = line.strip().split(',')
                    data_retrival[byType][gender].append([float(token[0]), float(token[1])])

    plots = {'comment': {}, 'like': {}, 'tag': {}}
    for byType in range(3):
        if byType == 0: action_str = "Comment - GAT"
        elif byType == 1: action_str = "Like - GAT"
        elif byType == 2: action_str = "Tag - GAT"

        plots[byType] = plotting(data_retrival[byType], action_str, testcases[testcase_idx])
    p = row(plots[0], plots[1], plots[2])
    testcase_plot.append(p)
# p = column(testcase_plot[0], testcase_plot[1], testcase_plot[2], testcase_plot[3])
p = column(testcase_plot[0])
curdoc().add_root(p)
curdoc().title = "glassceiling - GAT"
