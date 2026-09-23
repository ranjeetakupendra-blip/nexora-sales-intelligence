import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Load processed dataset
df = pd.read_csv("processed_sales_data.csv")

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Aggregate sales by date
daily_sales = df.groupby("date")["sales"].sum().reset_index()

# Rename columns for Prophet
prophet_data = daily_sales.rename(
    columns={
        "date": "ds",
        "sales": "y"
    }
)

# Create Prophet model
model = Prophet()

# Train model
model.fit(prophet_data)

# Create future dates
future = model.make_future_dataframe(periods=30)

# Generate forecast
forecast = model.predict(future)

# Display forecast
print("\nNext 30 Days Sales Forecast:")
print(
    forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
    .tail(30)
)

# Save forecast
forecast[
    ["ds", "yhat", "yhat_lower", "yhat_upper"]
].to_csv(
    "sales_forecast.csv",
    index=False
)

print("\nForecast saved successfully as sales_forecast.csv")