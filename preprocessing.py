import pandas as pd

# Load the new sales dataset
df = pd.read_csv("sales_data.csv")

# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# Remove duplicate rows
df = df.drop_duplicates()

# Check for missing values
print("Missing values:")
print(df.isnull().sum())

# Create additional date features
df["day"] = df["date"].dt.day
df["month"] = df["date"].dt.month
df["year"] = df["date"].dt.year
df["day_of_week"] = df["date"].dt.dayofweek

# Display the processed dataset
print("\nProcessed Dataset:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)

# Save processed dataset
df.to_csv("processed_sales_data.csv", index=False)

print("\nPreprocessing completed successfully!")