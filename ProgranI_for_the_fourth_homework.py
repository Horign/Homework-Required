import pandas as pd
import numpy as np
import seaborn as sns

df = sns.load_dataset('titanic')

print("=== Missing Values Overview ===")
print(df.isnull().sum())
print("\n=== Original Dataset Shape ===")
print(df.shape)

df_drop = df.dropna(subset=['embarked'])
print("\n=== Shape After Dropping Missing Embarked ===")
print(df_drop.shape)

df_fill = df.copy()
df_fill['age'] = df_fill['age'].fillna(df_fill['age'].median())
df_fill['embarked'] = df_fill['embarked'].fillna(df_fill['embarked'].mode()[0])
df_fill['deck'] = df_fill['deck'].cat.add_categories('Unknown')
df_fill['deck'] = df_fill['deck'].fillna('Unknown')
print("\n=== Missing Values After Filling ===")
print(df_fill.isnull().sum())

df_interp = df.copy()
df_interp['age'] = df_interp['age'].interpolate(method='linear')
print("\n=== Missing Age Values After Interpolation ===")
print(df_interp['age'].isnull().sum())

print("\n=== Number of Duplicate Rows ===")
print(df.duplicated().sum())
df_dedup = df.drop_duplicates()
print("\n=== Shape After Removing Duplicates ===")
print(df_dedup.shape)

df_clean = df_fill.copy()
df_clean['survived'] = df_clean['survived'].astype('category')
df_clean['pclass'] = df_clean['pclass'].astype('category')
df_clean['sex'] = df_clean['sex'].str.capitalize()
print("\n=== Data Types After Conversion ===")
print(df_clean.dtypes)
print("\n=== Sample of Cleaned Data ===")
print(df_clean.head())
