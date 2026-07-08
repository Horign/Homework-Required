import numpy as np
arr = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
print("original array:")
print(arr)
row2=arr[1,0:3]#直接读取第二行的第1-3列（左闭右开）
print("line 2 col 1-3", row2)
col3=arr[:,2]#所有行读取第三列数据
print("all lines col 3 ",col3)
odd=arr[::2, :]#先取一行，然后隔一行取一行（取奇数行），取其所有列
print("odd lines:")
print(odd)
