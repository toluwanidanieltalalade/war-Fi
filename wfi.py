import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# --------------------
# 1. LOAD DATA (Real US Public Data 2010-2023)
# --------------------
np.random.seed(42)  # For reproducibility
training_data = pd.DataFrame({
    "year": pd.date_range("2010", periods=14, freq="YE"),
    "gdp_per_capita_usd": [48400, 49800, 51600, 53100, 55000, 56800,
                           58000, 60000, 63000, 65100, 63500, 70200,
                           76300, 81600],
    "military_pct_gdp": [4.9, 4.8, 4.4, 4.0, 3.7, 3.4, 3.3, 3.3, 3.3,
                         3.4, 3.7, 3.5, 3.5, 3.4],
    "military_spending_bn_usd": [738, 752, 725, 680, 654, 633, 632, 646,
                                 682, 734, 778, 806, 877, 916],
    "military_troops": [2_270_000, 2_250_000, 2_200_000, 2_150_000, 2_100_000,
                        2_080_000, 2_090_000, 2_100_000, 2_120_000, 2_140_000,
                        2_130_000, 2_110_000, 2_050_000, 1_976_000],
    "fighter_active": [3100, 3050, 3000, 2950, 2900, 2850, 2800, 2820,
                       2830, 2840, 2850, 2860, 2870, 2880],
    "nuclear_submarines": [71, 71, 72, 73, 72, 71, 70, 70, 69, 68, 68, 68, 67, 67],
    "aircraft_carriers": [11, 11, 11, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11]
})

# --------------------
# 2. MODEL SETUP & EVALUATION
# --------------------
features = ["gdp_per_capita_usd", "military_pct_gdp"]
target = "military_spending_bn_usd"

model = LinearRegression()
model.fit(training_data[features], training_data[target])

y_pred = model.predict(training_data[features])
print(f"Model R² Score: {r2_score(training_data[target], y_pred):.4f}")

# Plot residuals
plt.figure(figsize=(10, 5))
plt.scatter(training_data["year"], training_data[target] - y_pred, color="red")
plt.axhline(y=0, color="blue", linestyle="--")
plt.title("Residuals Plot (US Public Data)")
plt.xlabel("Year")
plt.ylabel("Residuals (Billions USD)")
plt.grid(True)
plt.savefig("residuals_plot.png")

# --------------------
# 3. PROJECTIONS (2024 - 1 year ahead)
# --------------------
years = len(training_data) - 1
latest_data = training_data.iloc[-1]

def project_future_value(col_name, years_ahead=1):
    """Calculates CAGR and projects the value forward."""
    start, end = training_data[col_name].iloc[0], latest_data[col_name]
    cagr = (end / start) ** (1 / years) - 1
    return end * (1 + cagr) ** years_ahead

# Project values dynamically
projected = {col: project_future_value(col) for col in [
    "gdp_per_capita_usd", "military_pct_gdp", "military_troops", 
    "fighter_active", "nuclear_submarines", "aircraft_carriers"
]}

# Predict spending for 2024 (in billions)
future_data = pd.DataFrame([{
    "gdp_per_capita_usd": projected["gdp_per_capita_usd"], 
    "military_pct_gdp": projected["military_pct_gdp"]
}])
predicted_spending_bn = model.predict(future_data)[0]
predicted_spending_usd = predicted_spending_bn * 1_000_000_000

army_strength = int(projected["military_troops"])

# --------------------
# 4. ARMY ATTRITION MODEL (Projected Reductions)
# --------------------
RETIREMENT_RATE = 0.05       # ~5% standard retirement/separation
NATURAL_DEATH_RATE = 0.001   # ~0.1% expected natural mortality
TRAINING_DEATH_RATE = 0.0002 # ~0.02% expected training exercise fatalities

retirements = int(army_strength * RETIREMENT_RATE)
natural_deaths = int(army_strength * NATURAL_DEATH_RATE)
training_deaths = int(army_strength * TRAINING_DEATH_RATE)

net_army_strength = army_strength - (retirements + natural_deaths + training_deaths)

# --------------------
# 5. SIMULATION OUTPUT (2024)
# --------------------
print("\n=== 2024 MILITARY SIMULATION RESULTS (US DATA PROJECTIONS) ===")
print(f"Predicted military spending = ${predicted_spending_usd:,.0f} (${predicted_spending_bn:,.1f} Billion)")
print(f"Projected Gross Army Strength (before attrition) = {army_strength:,}")
print(f"  - Less Retirements: {retirements:,}")
print(f"  - Less Natural Deaths: {natural_deaths:,}")
print(f"  - Less Training Casualties: {training_deaths:,}")
print(f"Net Army Strength (Active Personnel) = {net_army_strength:,}")
print(f"Nuclear submarines = {int(projected['nuclear_submarines']):,}")
print(f"Fighter sorties (annual) = {int(projected['fighter_active']):,}")
print(f"Aircraft carriers = {int(projected['aircraft_carriers']):,}")
print(f"\nDerived Metrics:")
military_efficiency = predicted_spending_usd / net_army_strength
print(f"Military efficiency (USD per active soldier): ${military_efficiency:,.2f}")