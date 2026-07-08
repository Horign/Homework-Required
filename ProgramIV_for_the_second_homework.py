import numpy as np
arr1d=np.array([1,2,3,4,5])
print("array 1d:",arr1d,";shape:",arr1d.shape)
arr2d=np.arange(12).reshape(3,4)
print("\narray 2d:\n",arr2d,"\nshape:\n",arr2d.shape)
arr3d=np.random.randint(0,10,size=(2,3,4))
print("\narray 3d:\n",arr3d,"\nshape:\n",arr3d.shape)
print("the 3rd dot of 1d:",arr1d[2])
print("begin 3 dots of 1d:",arr1d[:3])
print("\nrow 2 col 3 dot of 2d:",arr2d[1,2])
print("begin 2 rows,last 2 cols dots of 2d:\n",arr2d[:2,:-2])
print("\nfloor 1,row 2,all cols dots of 3d:\n",arr3d[0,1,:])
testarr=np.arange(16)
print("origin 1d:",testarr)
testarr2d=testarr.reshape(4,4)
print("reshape(4,4):\n",testarr2d)
arrflat=testarr2d.flatten()
print("flatten:",arrflat)
arrT=testarr2d.T
print("transpose:\n",arrT)
def matadd(a,b):
    if a.shape!=b.shape:
        raise ValueError("matrix must be plused in the same dimension")
    return a+b
def matmul(a,b):
    if a.shape[1]!=b.shape[0]:
        raise ValueError("calculation cannot be done unless the number of cols of A equals that of rows of B")
    return a@b
def mattrans(a):
    return a.T
m1=np.array([[1,2],[3,4]])
m2=np.array([[5,6],[7,8]])
print("plus:\n",matadd(m1,m2))
print("multiply:\n",matmul(m1,m2))
print("transpose:\n",mattrans(m1),mattrans(m2))
randdata=np.random.normal(loc=50,scale=10,size=1000)
print("average:",np.mean(randdata))
print("middle:",np.median(randdata))
print("var:",np.var(randdata))
print("std:",np.std(randdata))
print("maximum/minimum:",np.max(randdata),np.min(randdata))
print("25%,75%:",np.percentile(randdata,[25,75]))
