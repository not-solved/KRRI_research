import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(4)
labels = ['lc1', 'lc2', 'lc3', 'lc4']

b3_1 = pd.read_csv('Dataset/sb_board_1/block_3_1.csv')
'''
b3_1 = [round(b3_1['lc1'].sum() / b3_1['lc1'].count()),
        round(b3_1['lc2'].sum() / b3_1['lc2'].count()),
        round(b3_1['lc3'].sum() / b3_1['lc3'].count()),
        round(b3_1['lc4'].sum() / b3_1['lc4'].count())]
plt.bar(x, b3_1)
plt.xticks(x, labels)
plt.title('Block 3-1')
plt.show()
'''
idx = b3_1[b3_1['minor'] != 3].index
b3_1 = b3_1.drop(idx)
length = np.arange(0, len(b3_1['lc1']))

plt.plot(length, b3_1['lc1'])
plt.plot(length, b3_1['lc2'])
plt.plot(length, b3_1['lc3'])
plt.plot(length, b3_1['lc4'])
plt.legend(['lc1', 'lc2', 'lc3', 'lc4'])
plt.title('Block 3-1')
plt.show()


b3_2 = pd.read_csv('Dataset/sb_board_1/block_3_2.csv')
'''
b3_2 = [round(b3_2['lc1'].sum() / b3_2['lc1'].count()),
        round(b3_2['lc2'].sum() / b3_2['lc2'].count()),
        round(b3_2['lc3'].sum() / b3_2['lc3'].count()),
        round(b3_2['lc4'].sum() / b3_2['lc4'].count())]
plt.bar(x, b3_2)
plt.xticks(x, labels)
plt.title('Block 3-2')
plt.show()
'''

idx = b3_2[b3_2['minor'] != 3].index
b3_2 = b3_2.drop(idx)
length = np.arange(0, len(b3_2['lc1']))

plt.plot(length, b3_2['lc1'])
plt.plot(length, b3_2['lc2'])
plt.plot(length, b3_2['lc3'])
plt.plot(length, b3_2['lc4'])
plt.legend(['lc1', 'lc2', 'lc3', 'lc4'])
plt.title('Block 3-2')
plt.show()


b3_3 = pd.read_csv('Dataset/sb_board_1/block_3_3.csv')
'''
b3_3 = [round(b3_3['lc1'].sum() / b3_3['lc1'].count()),
        round(b3_3['lc2'].sum() / b3_3['lc2'].count()),
        round(b3_3['lc3'].sum() / b3_3['lc3'].count()),
        round(b3_3['lc4'].sum() / b3_3['lc4'].count())]
plt.bar(x, b3_3)
plt.xticks(x, labels)
plt.title('Block 3-3')
plt.show()
'''
idx = b3_3[b3_3['minor'] != 3].index
b3_3 = b3_3.drop(idx)
length = np.arange(0, len(b3_3['lc1']))

plt.plot(length, b3_3['lc1'])
plt.plot(length, b3_3['lc2'])
plt.plot(length, b3_3['lc3'])
plt.plot(length, b3_3['lc4'])
plt.legend(['lc1', 'lc2', 'lc3', 'lc4'])
plt.title('Block 3-3')
plt.show()


b3_4 = pd.read_csv('Dataset/sb_board_1/block_3_4.csv')
'''
b3_4 = [round(b3_4['lc1'].sum() / b3_4['lc1'].count()),
        round(b3_4['lc2'].sum() / b3_4['lc2'].count()),
        round(b3_4['lc3'].sum() / b3_4['lc3'].count()),
        round(b3_4['lc4'].sum() / b3_4['lc4'].count())]
plt.bar(x, b3_4)
plt.xticks(x, labels)
plt.title('Block 3-4')
plt.show()
'''
idx = b3_4[b3_4['minor'] != 3].index
b3_4 = b3_4.drop(idx)
length = np.arange(0, len(b3_4['lc1']))

plt.plot(length, b3_4['lc1'])
plt.plot(length, b3_4['lc2'])
plt.plot(length, b3_4['lc3'])
plt.plot(length, b3_4['lc4'])
plt.legend(['lc1', 'lc2', 'lc3', 'lc4'])
plt.title('Block 3-4')
plt.show()

