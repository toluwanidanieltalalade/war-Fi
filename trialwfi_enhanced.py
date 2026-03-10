import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# --------------------
# 1. LOAD DATA (Simulated)
# --------------------
np.random.seed(42)  # For reproducibility
training_data = pd.DataFrame({
    "year": pd.date_range(2010, periods=14, freq='YE'),
    "gdp_per_capita_usb": [11500, 11800, 121000, 123000, 125000, 128000, 130000, 132000, 135000, 137000, 140000, 142000, 145000, 148000],
    "military_pct_gdp": [4.2, 3.9, 3.7, 3.5, 3.4, 4.8, 4.9, 5.1, 5.2, 5.3, 5.5, 5.6, 5.8, 5.9],
    "military_spending_usb": [950, 1020, 1080, 1120, 1150, 1450, 1500, 1580, 1620, 1650, 1700, 1750, 1800, 1850],
    "military_troops": [500_000, 520_000, 540_000, 560_000, 580_000, 620_000, 650_000, 680_000, 700_000, 720_000, 750_000, 780_000, 800_000, 820_000],
    "fighter_active": [150, 160, 170, 180, 190, 210, 230, 250, 270, 290, 310, 330, 350, 360],
    "nuclear_submarines": [12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38],
    "aircraft_carriers": [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
})

# Add dummy columns (for robustness)
training_data["military_titans"] = np.random.randint(100, 200, size=len(training_data))
training_data["fighter_aircraft"] = np.random.randint(100, 200, size=len(training_data))

# --------------------
# 2. MODEL SETUP & EVALUATION
# --------------------
features = ["gdp_per_capita_usb", "military_pct_gdp"]
target = "military_spending_usb"

model = LinearRegression()
model.fit(training_data[features], training_data[target])

# Evaluate model performance
y_pred = model.predict(training_data[features])
r2 = r2_score(training_data[target], y_pred)
print(f"Model R² Score: {r2:.4f}")

# Plot residuals (to check for patterns)
residuals = training_data[target] - y_pred
plt.figure(figsize=(10, 5))
plt.scatter(training_data["year"], residuals, color='red')
plt.axhline(y=0, color='blue', linestyle='--')
plt.title("Residuals Plot (Model Fit Check)")
plt.xlabel("Year")
plt.ylabel("Residuals")
plt.grid(True)
plt.show()

# --------------------
# 3. SIMULATION PARAMETERS (2024)
# --------------------
future_gdp = 149_000
future_pct = 5.2

future_data = pd.DataFrame({
    "gdp_per_capita_usb": [future_gdp],
    "military_pct_gdp": [future_pct]
})

predicted_spending = model.predict(future_data)[0]

# Predict other metrics (e.g., troops, submarines) using linear trends
def predict_linear_trend(series,