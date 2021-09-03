import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


'''
filename = ['block1.py', 'block2.py', 'block3.py', 'block4.py']
for i in filename :
        exec(open(i).read())
'''

x = np.arange(4)
labels = ['lc1', 'lc2', 'lc3', 'lc4']

b1_1 = pd.read_csv('Dataset/sb_board_1/block_1_1.csv')
'''
b1_1 = [round(b1_1['lc1'].sum() / b1_1['lc1'].count()),
        round(b1_1['lc2'].sum() / b1_1['lc2'].count()),
        round(b1_1['lc3'].sum() / b1_1['lc3'].count()),
        round(b1_1['lc4'].sum() / b1_1['lc4'].count())]
plt.bar(x, b1_1)
plt.xticks(x, labels)
plt.title('Block 1-1')
plt.show()
'''
idx = b1_1[b1_1['minor'] != 1].index
b1_1 = b1_1.drop(idx)
length = np.arange(0, len(b1_1['lc1']))

plt.plot(length, b1_1['lc1'])
plt.plot(length, b1_1['lc2'])
plt.plot(length, b1_1['lc3'])
plt.plot(length, b1_1['lc4'])
plt.legend(['lc1', 'lc2', 'lc3', 'lc4'])
plt.title('Block 1-1')
plt.show()


b1_2 = pd.read_csv('Dataset/sb_board_1/block_1_2.csv')
'''
b1_2 = [round(b1_2['lc1'].sum() / b1_2['lc1'].count()),
        round(b1_2['lc2'].sum() / b1_2['lc2'].count()),
        round(b1_2['lc3'].sum() / b1_2['lc3'].count()),
        round(b1_2['lc4'].sum() / b1_2['lc4'].count())]
plt.bar(x, b1_2)
plt.xticks(x, labels)
plt.title('Block 1-2')
plt.show()
'''

idx = b1_2[b1_2['minor'] != 1].index
b1_2 = b1_2.drop(idx)
length = np.arange(0, len(b1_2['lc1']))

plt.plot(length, b1_2['lc1'])
plt.plot(length, b1_2['lc2'])
plt.plot(length, b1_2['lc3'])
plt.plot(length, b1_2['lc4'])
plt.legend(['lc1', 'lc2', 'lc3', 'lc4'])
plt.title('Block 1-2')
plt.show()


b1_3 = pd.read_csv('Dataset/sb_board_1/block_1_3.csv')
'''
b1_3 = [round(b1_3['lc1'].sum() / b1_3['lc1'].count()),
        round(b1_3['lc2'].sum() / b1_3['lc2'].count()),
        round(b1_3['lc3'].sum() / b1_3['lc3'].count()),
        round(b1_3['lc4'].sum() / b1_3['lc4'].count())]
plt.bar(x, b1_3)
plt.xticks(x, labels)
plt.title('Block 1-3')
plt.show()
'''
idx = b1_3[b1_3['minor'] != 1].index
b1_3 = b1_3.drop(idx)
length = np.arange(0, len(b1_3['lc1']))

plt.plot(length, b1_3['lc1'])
plt.plot(length, b1_3['lc2'])
plt.plot(length, b1_3['lc3'])
plt.plot(length, b1_3['lc4'])
plt.legend(['lc1', 'lc2', 'lc3', 'lc4'])
plt.title('Block 1-3')
plt.show()


b1_4 = pd.read_csv('Dataset/sb_board_1/block_1_4.csv')
'''
b1_4 = [round(b1_4['lc1'].sum() / b1_4['lc1'].count()),
        round(b1_4['lc2'].sum() / b1_4['lc2'].count()),
        round(b1_4['lc3'].sum() / b1_4['lc3'].count()),
        round(b1_4['lc4'].sum() / b1_4['lc4'].count())]
plt.bar(x, b1_4)
plt.xticks(x, labels)
plt.title('Block 1-4')
plt.show()
'''
idx = b1_4[b1_4['minor'] != 1].index
b1_4 = b1_4.drop(idx)
length = np.arange(0, len(b1_4['lc1']))

plt.plot(length, b1_4['lc1'])
plt.plot(length, b1_4['lc2'])
plt.plot(length, b1_4['lc3'])
plt.plot(length, b1_4['lc4'])
plt.legend(['lc1', 'lc2', 'lc3', 'lc4'])
plt.title('Block 1-4')
plt.show()

