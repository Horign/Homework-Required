import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
np.random.seed(42)
dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
n = len(dates)
pm25_base = 60 + 30 * np.sin(np.linspace(0, 2*np.pi, n) + np.pi) + np.random.normal(0, 15, n)
pm10 = pm25_base * 1.5 + np.random.normal(0, 20, n)
so2 = 15 + 8 * np.sin(np.linspace(0, 2*np.pi, n) + np.pi) + np.random.normal(0, 5, n)
no2 = 35 + 15 * np.sin(np.linspace(0, 2*np.pi, n) + np.pi) + np.random.normal(0, 8, n)
co = 0.8 + 0.4 * np.sin(np.linspace(0, 2*np.pi, n) + np.pi) + np.random.normal(0, 0.2, n)
o3 = 50 + 30 * np.sin(np.linspace(0, 2*np.pi, n)) + np.random.normal(0, 10, n)

df = pd.DataFrame({
    'datetime': dates,
    'PM2.5': np.clip(pm25_base, 10, 300),
    'PM10': np.clip(pm10, 20, 400),
    'SO2': np.clip(so2, 5, 100),
    'NO2': np.clip(no2, 10, 150),
    'CO': np.clip(co, 0.2, 3),
    'O3': np.clip(o3, 20, 200)
})
df = df.set_index('datetime')
pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
print("=== Statistical Indicators of Pollutants ===")
print(df[pollutants].describe())
corr_matrix = df[pollutants].corr()
print("\n=== Correlation Matrix ===")
print(corr_matrix.round(2))
def get_season(month):
    if month in [3,4,5]:
        return 'Spring'
    elif month in [6,7,8]:
        return 'Summer'
    elif month in [9,10,11]:
        return 'Autumn'
    else:
        return 'Winter'
df['season'] = df.index.month.map(get_season)
seasonal_stats = df.groupby('season')[pollutants].mean().reindex(['Spring','Summer','Autumn','Winter'])
print("\n=== Seasonal Average Concentration ===")
print(seasonal_stats.round(2))
fig = plt.figure(figsize=(16, 12))
ax1 = plt.subplot(2,2,1)
df['PM2.5'].plot(ax=ax1, linewidth=0.8, color='#1f77b4')
ax1.set_title('PM2.5浓度全年变化趋势')
ax1.set_xlabel('日期')
ax1.set_ylabel('PM2.5浓度 (μg/m³)')
ax2 = plt.subplot(2,2,2)
seasonal_stats['PM2.5'].plot(kind='bar', ax=ax2, color=['#2ca02c','#ff7f0e','#9467bd','#d62728'])
ax2.set_title('各季节平均PM2.5浓度对比')
ax2.set_xlabel('季节')
ax2.set_ylabel('平均浓度 (μg/m³)')
ax2.set_xticklabels(['春季','夏季','秋季','冬季'], rotation=0)
ax3 = plt.subplot(2,2,3)
sns.scatterplot(x='PM2.5', y='PM10', data=df, ax=ax3, alpha=0.6, color='#ff7f0e')
ax3.set_title('PM2.5与PM10浓度相关性散点图')
ax3.set_xlabel('PM2.5浓度 (μg/m³)')
ax3.set_ylabel('PM10浓度 (μg/m³)')
ax4 = plt.subplot(2,2,4)
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax4, fmt='.2f', vmin=-1, vmax=1)
ax4.set_title('各污染物相关性热力图')
plt.tight_layout()
plt.show()
