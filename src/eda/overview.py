import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('/path_to_csv')

# Basic Information
print("Basic Information:")
print(df.info())
print('****************************************\n')

# Missing Values
print("\nMissing Values:")
print(df.isnull().sum())
print('****************************************\n')

# Data Cleaning: Remove unnamed columns and drop columns with missing values
df_clean = df.loc[:, ~df.columns.str.startswith('Unnamed')]
df_clean_columns = df_clean.dropna(axis=1)

# Basic Information On Clean Data
print("Basic Information On Clean Data:")
print(df_clean.info())
print('****************************************\n')

df = df_clean

# Display the first few rows of the dataset
print("\nFirst 5 Rows:")
print(df.head())
print('****************************************\n')

# Summary statistics of the dataset
print("\nSummary Statistics:")
print(df.describe())
print('****************************************\n')

# Distribution of the 'price' column
plt.figure(figsize=(10, 6))
sns.histplot(df['price'], bins=10, kde=True)
plt.title('Distribution of Cryptocurrency Prices')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()

# Correlation matrix for numeric features
numeric_df = df.select_dtypes(include=['float64', 'int64'])
correlation_matrix = numeric_df.corr()
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Top 10 cryptocurrencies by market cap
df['marketcap'] = pd.to_numeric(df['marketcap'], errors='coerce')
df = df.dropna(subset=['marketcap'])  # Drop rows where 'marketcap' is NaN
top_10_marketcap = df.nlargest(10, 'marketcap')

# Plot the top 10 cryptocurrencies by market cap
plt.figure(figsize=(12, 8))
sns.barplot(x='marketcap', y='name', data=top_10_marketcap)
plt.title('Top 10 Cryptocurrencies by Market Cap')
plt.xlabel('Market Cap')
plt.ylabel('Cryptocurrency')
plt.show()

# Scatter plot of price vs market cap
plt.figure(figsize=(10, 6))
sns.scatterplot(x='price', y='marketcap', data=df, color='red')
plt.title('Price vs Market Cap')
plt.xlabel('Price')
plt.ylabel('Market Cap')
plt.show()

# Time series analysis of the top cryptocurrency by market cap
top_crypto = df.loc[df['marketcap'].idxmax()]
print("\nTop Cryptocurrency by Market Cap:")
print(top_crypto)
