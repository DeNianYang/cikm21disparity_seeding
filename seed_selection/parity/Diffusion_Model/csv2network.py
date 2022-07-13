import os

name = 'remove1interaction'

##f = open(name+'.csv', 'r')
##ffl = open(name+'-l', 'w')
##ffc = open(name+'-c', 'w')
##ffi = open(name+'-i', 'w')
##
##count = 0
##for line in f:
##    count += 1
##    if count % 100000 == 0:
##        print(count)
##    token = line.strip().split(',')
##    ffl.write(' '.join(token[0:4])+' '+token[4]+'\n')
##    ffc.write(' '.join(token[0:4])+' '+token[5]+'\n')
##    ffi.write(' '.join(token[0:4])+' '+token[6]+'\n')
##f.close()
##ffl.close()
##ffc.close()
##ffi.close()

task = ['l', 'c', 'i']
for i in range(3):
    f = open(name+'-'+task[i], 'r')
    total = {}
    for line in f:
        token = line.strip().split(' ')
        if token[0] in total:
            total[token[0]] += int(token[4])
            #total[token[0]] += 1
        else:
            total[token[0]] = int(token[4])
            #total[token[0]] = 1
    f.close()

    f = open(name+'-'+task[i], 'r')
    ff = open(name+task[i], 'wb')
    for line in f:
        token = line.strip().split(' ')
        if total[token[0]] > 0:
            w = str(round(float(token[4])/float(total[token[0]]),2))
            #w = str(round(float(1)/float(total[token[0]]),2))
            if w != '0.0':
                ff.write(token[2]+' '+token[3]+' '+token[0]+' '+token[1]+' '+w+'\n')
    f.close()
    ff.close()
