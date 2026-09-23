import pandas as pd
import matplotlib.pyplot as plt

# Load processed dataset
df = pd.read_csv("processed_sales_data.csv")

# Convert date column
df["date"] = pd.to_datetime(df["date"])


# 1. Sales over time
plt.figure(figsize=(10, 5))
plt.plot(df["date"], df["sales"])
plt.title("Sales Over Time")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 2. Sales by product
product_sales = df.groupby("product")["sales"].sum()

plt.figure(figsize=(8, 5))
product_sales.plot(kind="bar")
plt.title("Total Sales by Product")
plt.xlabel("Product")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 3. Quantity sold by product
product_quantity = df.groupby("product")["quantity"].sum()

plt.figure(figsize=(8, 5))
product_quantity.plot(kind="bar")
plt.title("Quantity Sold by Product")
plt.xlabel("Product")
plt.ylabel("Quantity Sold")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# 4. Promotion vs sales
promotion_sales = df.groupby("promotion")["sales"].mean()

plt.figure(figsize=(7, 5))
promotion_sales.plot(kind="bar")
plt.title("Average Sales: Promotion vs No Promotion")
plt.xlabel("Promotion (0 = No, 1 = Yes)")
plt.ylabel("Average Sales")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


# 5. Weekday vs weekend sales
weekend_sales = df.groupby("weekend")["sales"].mean()

plt.figure(figsize=(7, 5))
weekend_sales.plot(kind="bar")
plt.title("Average Sales: Weekday vs Weekend")
plt.xlabel("Weekend (0 = Weekday, 1 = Weekend)")
plt.ylabel("Average Sales")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()


print("EDA completed successfully!")