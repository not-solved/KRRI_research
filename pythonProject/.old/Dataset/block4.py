import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(4)
labels = ['lc1', 'lc2', 'lc3', 'lc4']

b4_1 = pd.read_csv('Dataset/sb_board_1/block_4_1.csv')
'''
b4_1 = [round(b4_1['lc1'].sum() / b4_1['lc1'].count()),
        round(b4_1['lc2'].sum() / b4_1['lc2'].count()),
        round(b4_1['lc3'].sum() / b4_1['lc3'].count()),
        round(b4_1['lc4'].sum() / b4_1['lc4'].count())]
plt.bar(x, b4_1)
plt.xticks(x, labels)
plt.title('Block 4-1')
plt.show()
'''
idx = b4_1[b4_1['minor'] != 4].index
b4_1 = b4_1.drop(idx)
length = np.arange(0, len(b4_1['lc1']))

plt.plot(length, b4_1['lc1'])
plt.plot(length, b4_1['lc2'])
plt.plot(length, b4_1['lc3'])
plt.plot(length, b4_1['lc4'])
plt.legend(['lc1', 'lc2', 'lc3', 'lc4'])
plt.title('Block 4-1')
plt.show()


b4_2 = pd.read_csv('Dataset/sb_board_1/block_4_2.csv')
'''
b4_2 = [round(b4_2['lc1'].sum() / b4_2['lc1'].count()),
        round(b4_2['lc2'].sum() / b4_2['lc2'].count()),
        round(b4_2['lc3'].sum() / b4_2['lc3'].count()),
        round(b4_2['lc4'].sum() / b4_2['lc4'].count())]
plt.bar(x, b4_2)
plt.xticks(x, labels)
plt.title('Block 4-2')
plt.show()
'''

idx = b4_2[b4_2['minor'] != 4].index
b4_2 = b4_2.drop(idx)
length = np.arange(0, len(b4_2['lc1']))

plt.plot(length, b4_2['lc1'])
plt.plot(length, b4_2['lc2'])
plt.plot(length, b4_2['lc3'])
plt.plot(length, b4_2['lc4'])
plt.legend(['lc1', 'lc2', 'lc3', 'lc4'])
plt.title('Block 4-2')
plt.show()


b4_3 = pd.read_csv('Dataset/sb_board_1/block_4_3.csv')
'''
b4_3 = [round(b4_3['lc1'].sum() / b4_3['lc1'].count()),
        round(b4_3['lc2'].sum() / b4_3['lc2'].count()),
        round(b4_3['lc3'].sum() / b4_3['lc3'].count()),
        round(b4_3['lc4'].sum() / b4_3['lc4'].count())]
plt.bar(x, b4_3)
plt.xticks(x, labels)
plt.title('Block 4-3')
plt.show()
'''
idx = b4_3[b4_3['minor'] != 4].index
b4_3 = b4_3.drop(idx)
length = np.arange(0, len(b4_3['lc1']))

plt.plot(length, b4_3['lc1'])
plt.plot(length, b4_3['lc2'])
plt.plot(length, b4_3['lc3'])
plt.plot(length, b4_3['lc4'])
plt.legend(['lc1', 'lc2', 'lc3', 'lc4'])
plt.title('Block 4-3')
plt.show()


b4_4 = pd.read_csv('Dataset/sb_board_1/block_4_4.csv')
'''
b4_4 = [round(b4_4['lc1'].sum() / b4_4['lc1'].count()),
        round(b4_4['lc2'].sum() / b4_4['lc2'].count()),
        round(b4_4['lc3'].sum() / b4_4['lc3'].count()),
        round(b4_4['lc4'].sum() / b4_4['lc4'].count())]
plt.bar(x, b4_4)
plt.xticks(x, labels)
plt.title('Block 4-4')
plt.show()
'''
idx = b4_4[b4_4['minor'] != 4].index
b4_4 = b4_4.drop(idx)
length = np.arange(0, len(b4_4['lc1']))

plt.plot(length, b4_4['lc1'])
plt.plot(length, b4_4['lc2'])
plt.plot(length, b4_4['lc3'])
plt.plot(length, b4_4['lc4'])
plt.legend(['lc1', 'lc2', 'lc3', 'lc4'])
plt.title('Block 4-4')
plt.show()

