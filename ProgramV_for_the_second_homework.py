import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"]=["SimHei"]
plt.rcParams["axes.unicode_minus"]=False
np.random.seed(42)
tradingdays=252
stocknum=3
s0=np.array([100,120,95])
mu=np.array([0.08,0.05,0.12])
sigma=np.array([0.18,0.25,0.22])
dt=1/tradingdays
dailyreturn=(mu-0.5*sigma**2)*dt+sigma*np.random.normal(0,np.sqrt(dt),(tradingdays,stocknum))
price=np.zeros((tradingdays+1,stocknum))
price[0]=s0
for t in range(1,tradingdays+1):
    price[t]=price[t-1]*np.exp(dailyreturn[t-1])
logreturn=np.log(price[1:]/price[:-1])
annualvol=np.std(logreturn,axis=0)*np.sqrt(tradingdays)
print("Single note annual changing rate:")
for i,vol in enumerate(annualvol):
    print(f"note{i+1}:{vol:.2%}")
def calcma(priceseries,window):
    weight=np.ones(window)/window
    ma=np.convolve(priceseries,weight,mode="valid")
    return ma
p1=price[:,0]
ma5=calcma(p1,5)
ma20=calcma(p1,20)
covmatrix=np.cov(logreturn.T)
print("convariance matrix of income:")
print(np.round(covmatrix,6))
weight=np.array([1/stocknum]*stocknum)
portvariance=weight@covmatrix@weight.T
portvol=np.sqrt(portvariance)*np.sqrt(tradingdays)
print(f"\nsame weight collaboration annual changing rate:{portvol:.2%}")
fig,(ax1,ax2)=plt.subplots(2,1,figsize=(12,9))
ax1.plot(p1,label="note 1 original price",color="#2E86AB")
ax1.plot(np.arange(4,len(ma5)+4),ma5,label="MA5",color="#A23B72",linewidth=1.5)
ax1.plot(np.arange(19,len(ma20)+19),ma20,label="MA20",color="#F18F01",linewidth=1.5)
ax1.set_title("note 1 prices and 5/20 days changing average line")
ax1.legend()
ax1.grid(alpha=0.3)
ax2.hist(logreturn[:,0],bins=40,alpha=0.7,color="#C73E1D")
ax2.set_title("note 1 income ratio histogram in log")
ax2.set_xlabel("daily income rate in log")
ax2.set_ylabel("frequency")
ax2.grid(alpha=0.3)
plt.tight_layout()
plt.show()
