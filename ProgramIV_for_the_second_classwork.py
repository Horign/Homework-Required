import numpy as np
rand=np.random.rand(10)
vmin=rand.min()
vmax=rand.max()
norm=(rand-vmin)/(vmax-vmin)
print("random array:",rand)
print("normalization of array:",norm)
cumsum=np.cumsum(norm)
cummax=np.maximum.accumulate(norm)
print("sum in total:",cumsum)
print("maximum in total:",cummax)

