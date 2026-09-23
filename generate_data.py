import pandas as pd
import numpy as np

# Make results reproducible
np.random.seed(42)

# Number of records
n = 500

# Generate dates
dates = pd.date_range(start="2025-01-01", periods=n, freq="D")

# Products
products = np.random.choice(
    ["Laptop", "Mobile", "Headphones", "Tablet", "Smartwatch"],
    size=n
)

# Quantity sold
quantity = np.random.randint(1, 20, size=n)

# Product prices
prices = {
    "Laptop": 55000,
    "Mobile": 25000,
    "Headphones": 3000,
    "Tablet": 18000,
    "Smartwatch": 5000
}

price = [prices[product] for product in products]

# Promotion: 1 = Yes, 0 = No
promotion = np.random.choice([0, 1], size=n, p=[0.7, 0.3])

# Weekend: 1 = Weekend, 0 = Weekday
weekend = [1 if date.weekday() >= 5 else 0 for date in dates]

# Calculate sales
sales = (
    np.array(quantity) * np.array(price)
    * (1 + 0.20 * np.array(promotion))
)

# Add some random variation
sales = sales + np.random.normal(0, 5000, n)

# Make sure sales are positive
sales = np.maximum(sales, 0)

# Create dataset
data = pd.DataFrame({
    "date": dates,
    "product": products,
    "quantity": quantity,
    "price": price,
    "promotion": promotion,
    "weekend": weekend,
    "sales": sales.round(2)
})

# Save dataset
data.to_csv("sales_data.csv", index=False)

print("Dataset generated successfully!")
print(data.head())
print("\nDataset shape:", data.shape)