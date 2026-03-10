import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


training_data = pd.DataFrame({
  
})

# Add dummy columns (for robustness)
training_data["military_titans"] = np.random.randint(100, 200, size=len(training_data))
training_data["fighter_aircraft"] = np.random.randint(100, 200, size=len(training_data))


# 3. SIMULATION PARAMETERS (2024)

future_gdp = 149_000  # Predicted GDP per capita in USD
future_pct = 5.2      # Predicted military percentage of GDP

# Create future data DataFrame for prediction
future_data = pd.DataFrame({
    "gdp_per_capita_usb": [future_gdp],
    "military_pct_gdp": [future_pct]
})

# Predict military spending using the trained model
predicted_spending = model.predict(future_data)[0]

# Extract latest values from training data for other simulation elements
latest_year_data = training_data.iloc[-1]  # Get last row


# compute genuine annual growth rates (CAGR) for the historical series

years = len(training_data) - 1  # 14 points span 13 full year‑on‑year intervals

def compound_rate(start, end, periods):
    """compound annual growth rate between `start` and `end` over `periods` years"""
    return (end / start) ** (1 / periods) - 1

gdp_growth_rate = compound_rate(
    training_data["gdp_per_capita_usb"].iloc[0],
    latest_year_data["gdp_per_capita_usb"],
    years
)

military_troops_rate = compound_rate(
    training_data["military_troops"].iloc[0],
    latest_year_data["military_troops"],
    years
)

fighter_rate = compound_rate(
    training_data["fighter_active"].iloc[0],
    latest_year_data["fighter_active"],
    years
)

nuclear_sub_rate = compound_rate(
    training_data["nuclear_submarines"].iloc[0],
    latest_year_data["nuclear_submarines"],
    years
)

carriers_rate = compound_rate(
    training_data["aircraft_carriers"].iloc[0],
    latest_year_data["aircraft_carriers"],
    years
)

# Project future values based on those rates
def project_future_value(current_value, growth_rate, years_ahead=4):
    return current_value * (1 + growth_rate) ** years_ahead

army_strength = int(project_future_value(
    latest_year_data["military_troops"],
    military_troops_rate
))

fighter_sorties = int(project_future_value(
    latest_year_data["fighter_active"],
    fighter_rate
))

nuclear_subs = int(project_future_value(
    latest_year_data["nuclear_submarines"],
    nuclear_sub_rate
))

carriers = int(project_future_value(
    latest_year_data["aircraft_carriers"],
    carriers_rate
))


print("\n=== 2024 MILITARY SIMULATION RESULTS ===")
print(f"Predicted military spending (USD) = ${predicted_spending:,.0f}")
print(f"Army strength (personnel) = {army_strength:,}")
print(f"Nuclear submarines = {nuclear_subs:,}")
print(f"Fighter sorties (annual) = {fighter_sorties:,}")
print(f"Aircraft carriers = {carriers:,}")
# Calculate some derived metrics
military_efficiency = predicted_spending / army_strength * 1000
print(f"\nDerived Metrics:")
print(f"Military efficiency (USD per soldier): ${military_efficiency:,.2f}")

