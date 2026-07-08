import numpy as np
import timeit
np.random.seed(42)
A=np.random.rand(1000,2000)
B=np.random.rand(2000,3000)
def fdot():
    return np.dot(A,B)
def fat():
    return A@B
def fmatmul():
    return np.matmul(A,B)
t1=timeit.timeit(fdot,number=1)
t2=timeit.timeit(fat,number=1)
t3=timeit.timeit(fmatmul,number=1)
print(f"1. np.dot(A,B): {t1:.2f} s")
print(f"2. A@B : {t2:.2f} s")
print(f"1. np.matmul(A,B): {t3:.2f} s")
arrc=np.random.rand(1000,1000)
arrf=np.asfortranarray(arrc.copy())
print("Comparison")
def crowsum():
    return arrc.sum(axis=1)
def fcolsum():
    return arrf.sum(axis=0)
def ccolsum():
    return arrc.sum(axis=0)
def frowsum():
    return arrf.sum(axis=1)
tcrow=timeit.timeit(crowsum,number=200)
tfcol=timeit.timeit(fcolsum,number=200)
tccol=timeit.timeit(ccolsum,number=200)
tfrow=timeit.timeit(frowsum,number=200)
print(f"array in c-order sum in row costs {tcrow:.2f} s time.")
print(f"array in f-order sum in col costs {tfcol:.2f} s time.")
print(f"array in c-order sum in col costs {tccol:.2f} s time.")
print(f"array in f-order sum in row costs {tfrow:.2f} s time.")
Asmall=np.random.rand(1000,1000)
resnorm=Asmall**2+2*Asmall+1
resopt=np.empty_like(Asmall)
temp=np.empty_like(Asmall)
def calcnorm():
    return Asmall**2+2*Asmall+1
def calcopt():
    np.multiply(Asmall,Asmall,out=resopt)
    np.multiply(2,Asmall,out=temp)
    np.add(resopt,temp,out=resopt)
    np.add(resopt,1,out=resopt)
    return resopt
print("two methods of calculation are the same:",np.allclose(resnorm,calcopt()))
tnorm=timeit.timeit(calcnorm,number=100)
topt=timeit.timeit(calcopt,number=100)
print(f"time cost on normal calculation:{tnorm:.4f}s")
print(f"time cost on optional(out) calculation:{topt:.4f}s")
