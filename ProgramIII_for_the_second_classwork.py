import numpy as np
import math
A=np.random.randint(1,5,size=(2,3))
B=np.random.randint(1,5,size=(2,3))
print("array A:")
print(A)
print("array B:")
print(B)
elem=A*B#逐元素乘
mat=A@B.T#线性代数矩阵乘
print("element multiplication A*B:")
print(elem)
print("matrix multiplication A*B:")
print(mat)
mat2=np.array([[1,2],[3,4]])
colsum=np.sum(mat,axis=0)
rowsum=np.sum(mat,axis=1)#axis参数：0表示列向，1表示横向
print("origin matrix:",mat2)
print("sum of col:",colsum)
print("sum of row:",rowsum)
nums=np.array([1.2,3.5,2.8])
mean=np.mean(nums)#均值
std=np.std(nums)#标准差=方差开根号
roundsums=np.round(nums)#分别四舍五入
print("origin array:",nums)
print("mean of array:",mean)
print("std of array:",std)
print("round of array:",roundsums)
