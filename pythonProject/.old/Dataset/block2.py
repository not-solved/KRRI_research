import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(4)
labels = ['lc1', 'lc2', 'lc3', 'lc4']

b2_1 = pd.read_csv('Dataset/sb_board_1/block_2_1.csv')
'''
b2_1 = [round(b2_1['lc1'].sum() / b2_1['lc1'].count()),
        round(b2_1['lc2'].sum() / b2_1['lc2'].count()),
        round(b2_1['lc3'].sum() / b2_1['lc3'].count()),
        round(b2_1['lc4'].sum() / b2_1['lc4'].count())]
plt.bar(x, b2_1)
plt.xticks(x, labels)
plt.title('Block 2-1')
plt.show()
'''
idx = b2_1[b2_1['minor'] != 2].index
b2_1 = b2_1.drop(idx)
length = np.arange(0, len(b2_1['lc1']))

plt.plot(length, b2_1['lc1'])
plt.plot(length, b2_1['lc2'])
plt.plot(length, b2_1['lc3'])
plt.plot(length, b2_1['lc4'])
plt.legend(['lc1', 'lc2', 'lc3', 'lc4'])
plt.title('Block 2-1')
plt.show()


b2_2 = pd.read_csv('Dataset/sb_board_1/block_2_2.csv')
'''
b2_2 = [round(b2_2['lc1'].sum() / b2_2['lc1'].count()),
        round(b2_2['lc2'].sum() / b2_2['lc2'].count()),
        round(b2_2['lc3'].sum() / b2_2['lc3'].count()),
        round(b2_2['lc4'].sum() / b2_2['lc4'].count())]
plt.bar(x, b2_2)
plt.xticks(x, labels)
plt.title('Block 2-2')
plt.show()
'''

idx = b2_2[b2_2['minor'] != 2].index
b2_2 = b2_2.drop(idx)
length = np.arange(0, len(b2_2['lc1']))

plt.plot(length, b2_2['lc1'])
plt.plot(length, b2_2['lc2'])
plt.plot(length, b2_2['lc3'])
plt.plot(length, b2_2['lc4'])
plt.legend(['lc1', 'lc2', 'lc3', 'lc4'])
plt.title('Block 2-2')
plt.show()


b2_3 = pd.read_csv('Dataset/sb_board_1/block_2_3.csv')
'''
b2_3 = [round(b2_3['lc1'].sum() / b2_3['lc1'].count()),
        round(b2_3['lc2'].sum() / b2_3['lc2'].count()),
        round(b2_3['lc3'].sum() / b2_3['lc3'].count()),
        round(b2_3['lc4'].sum() / b2_3['lc4'].count())]
plt.bar(x, b2_3)
plt.xticks(x, labels)
plt.title('Block 2-3')
plt.show()
'''
idx = b2_3[b2_3['minor'] != 2].index
b2_3 = b2_3.drop(idx)
length = np.arange(0, len(b2_3['lc1']))

plt.plot(length, b2_3['lc1'])
plt.plot(length, b2_3['lc2'])
plt.plot(length, b2_3['lc3'])
plt.plot(length, b2_3['lc4'])
plt.legend(['lc1', 'lc2', 'lc3', 'lc4'])
plt.title('Block 2-3')
plt.show()


b2_4 = pd.read_csv('Dataset/sb_board_1/block_2_4.csv')
'''
b2_4 = [round(b2_4['lc1'].sum() / b2_4['lc1'].count()),
        round(b2_4['lc2'].sum() / b2_4['lc2'].count()),
        round(b2_4['lc3'].sum() / b2_4['lc3'].count()),
        round(b2_4['lc4'].sum() / b2_4['lc4'].count())]
plt.bar(x, b2_4)
plt.xticks(x, labels)
plt.title('Block 2-4')
plt.show()
'''
idx = b2_4[b2_4['minor'] != 2].index
b2_4 = b2_4.drop(idx)
length = np.arange(0, len(b2_4['lc1']))

plt.plot(length, b2_4['lc1'])
plt.plot(length, b2_4['lc2'])
plt.plot(length, b2_4['lc3'])
plt.plot(length, b2_4['lc4'])
plt.legend(['lc1', 'lc2', 'lc3', 'lc4'])
plt.title('Block 2-4')
plt.show()

