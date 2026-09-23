import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# Load processed dataset
df = pd.read_csv("processed_sales_data.csv")


# Features used by the model
features = [
    "quantity",
    "price",
    "promotion",
    "weekend",
    "day",
    "month",
    "year",
    "day_of_week"
]

X = df[features]
y = df["sales"]


# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Create Random Forest model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)


# Train the model
model.fit(X_train, y_train)


# Make predictions
predictions = model.predict(X_test)


# Evaluate the model
mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions) ** 0.5
r2 = r2_score(y_test, predictions)


print("\nModel Performance")
print("------------------------")
print("MAE :", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R2  :", round(r2, 2))


# Save the trained model
joblib.dump(model, "sales_model.pkl")

print("\nModel saved successfully as sales_model.pkl")