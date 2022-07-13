import os

files = [f for f in os.listdir('.') if os.path.isfile(f)]

ff = open('result.txt', 'w')

for f in files:
    if f.endswith('.out'):
        each = open(f, 'r')
        token_f = f.strip().split('_')
        ff.write(token_f[0]+'\t'+token_f[1][:-1]+'\t'+token_f[2][:-4]+'\t')
        print(each)
        for line in each:
            ff.write(line)
            break
        each.close()
ff.close()
        
# import os
# import sys

# files = [f for f in os.listdir('.') if os.path.isfile(f)]

# for intrv in [int(int(sys.argv[1])*0.2), int(int(sys.argv[1])*0.4), int(int(sys.argv[1])*0.5), int(int(sys.argv[1])*0.6), int(int(sys.argv[1])*0.8)]:
#     ff = open('result_{}.txt'.format(intrv), 'w')
#     for f in files:
#         if ("-{}-".format(intrv) in f) and (f.endswith('.out')):
#             each = open(f, 'r')
#             token_f = f.strip().split('_')
#             ff.write(token_f[0]+'\t'+token_f[1][:-1]+'\t'+token_f[2][:-4]+'\t')
#             for line in each:
#                 ff.write(line)
#                 break
#             each.close()
#     ff.close()

