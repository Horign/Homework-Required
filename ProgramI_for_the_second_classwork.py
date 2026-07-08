import numpy as np
arr=np.random.randint(0,10,size=(3,4))
print("origin arr:")
print(arr)
reshaped=arr.reshape(4,3).T
print("arr after reshape:")
print(reshaped)
filtered=arr[arr>5]
print("units that larger than 5:")
print(filtered)
