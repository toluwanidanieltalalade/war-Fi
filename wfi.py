import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import json
import os
from datetime import datetime

# ==========================================
# 1. HISTORICAL DATA (US Public Data 2010-2023)
# ==========================================
np.random.seed(42)

historical_data = pd.DataFrame({
    "Year": pd.date_range("2010", periods=14, freq="YE"),
    "GDP_Per_Capita": [48400, 49800, 51600, 53100, 55000, 56800,
                       58000, 60000, 63000, 65100, 63500, 70200,
                       76300, 81600],
    "Military_Percent_Of_GDP": [4.9, 4.8, 4.4, 4.0, 3.7, 3.4, 3.3, 3.3, 3.3,
                                3.4, 3.7, 3.5, 3.5, 3.4],
    "Inflation_Rate": [1.6, 3.2, 2.1, 1.5, 1.6, 0.1, 1.3, 2.1, 2.4,
                       1.8, 1.2, 4.7, 8.0, 4.1],
    "Foreign_Aid_Billions": [13.2, 14.1, 15.0, 14.8, 14.5, 14.2, 16.5,
                             17.1, 18.0, 18.2, 18.5, 20.1, 44.5, 52.3],
    "Total_Military_Spending_Billions": [738, 752, 725, 680, 654, 633, 632, 646,
                                         682, 734, 778, 806, 877, 916],
    "Total_Troops": [2_270_000, 2_250_000, 2_200_000, 2_150_000, 2_100_000,
                     2_080_000, 2_090_000, 2_100_000, 2_120_000, 2_140_000,
                     2_130_000, 2_110_000, 2_050_000, 1_976_000],
    "Active_Fighters": [3100, 3050, 3000, 2950, 2900, 2850, 2800, 2820,
                        2830, 2840, 2850, 2860, 2870, 2880],
    "Nuclear_Submarines": [71, 71, 72, 73, 72, 71, 70, 70, 69, 68, 68, 68, 67, 67],
    "Aircraft_Carriers": [11, 11, 11, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11]
})

# ==========================================
# 2. TRAIN PREDICTION MODEL
# ==========================================
# These factors are used to predict the total military spending
input_factors = ["GDP_Per_Capita", "Military_Percent_Of_GDP", "Inflation_Rate", "Foreign_Aid_Billions"]
target_budget = "Total_Military_Spending_Billions"

model = LinearRegression()
model.fit(historical_data[input_factors], historical_data[target_budget])

predicted_training_budget = model.predict(historical_data[input_factors])
print(f"Model Accuracy (R² Score): {r2_score(historical_data[target_budget], predicted_training_budget):.4f}")

# Save Error / Residuals Graph
plt.figure(figsize=(10, 5))
plt.scatter(historical_data["Year"], historical_data[target_budget] - predicted_training_budget, color="red")
plt.axhline(y=0, color="blue", linestyle="--")
plt.title("Residuals Plot (US Public Data)")
plt.xlabel("Year")
plt.ylabel("Prediction Error (Billions USD)")
plt.grid(True)
plt.savefig("residuals_plot.png")

# ==========================================
# 3. FUTURE PROJECTIONS (Default Trends)
# ==========================================
total_years = len(historical_data) - 1
latest_year = historical_data.iloc[-1]

def calculate_future_trend(column_name, target_year=2025):
    """Calculates the historical average growth and projects it out to the target year."""
    years_ahead = target_year - 2023 # dataset ends at 2023
    start_value = historical_data[column_name].iloc[0]
    end_value = latest_year[column_name]
    
    average_growth_rate = (end_value / start_value) ** (1 / total_years) - 1
    return end_value * (1 + average_growth_rate) ** years_ahead

# Calculate what the numbers *should* naturally be in 2025
projected_defaults = {col: calculate_future_trend(col, 2025) for col in [
    "GDP_Per_Capita", "Military_Percent_Of_GDP", "Inflation_Rate",
    "Foreign_Aid_Billions", "Total_Troops", "Active_Fighters",
    "Nuclear_Submarines", "Aircraft_Carriers"
]}

# ==========================================
# 4. INTERACTIVE USER PROMPT ("What-If" Analysis)
# ==========================================
print("\n" + "="*50)
print("INTERACTIVE MILITARY BUDGET SIMULATOR (2025)")
print("="*50)
print("Enter your own estimates for 2025 to see how the budget reacts.")
print("Press [ENTER] to skip and just use the natural historical trend.\n")

def get_user_input(prompt_text, default_value):
    user_input = input(f"{prompt_text} (Default: {default_value:.2f}): ").strip()
    if not user_input:
        return default_value
    try:
        return float(user_input)
    except ValueError:
        print(f"  [!] Invalid number. Using default: {default_value:.2f}")
        return default_value

user_gdp = get_user_input("Estimated GDP Per Capita in USD", projected_defaults["GDP_Per_Capita"])
user_mil_pct = get_user_input("Military Spending as % of GDP", projected_defaults["Military_Percent_Of_GDP"])
user_inflation = get_user_input("Estimated Inflation Rate (%)", projected_defaults["Inflation_Rate"])
user_aid = get_user_input("Foreign Military Aid (Billions USD)", projected_defaults["Foreign_Aid_Billions"])

# Package user choices to predict budget
future_scenario = pd.DataFrame([{
    "GDP_Per_Capita": user_gdp,
    "Military_Percent_Of_GDP": user_mil_pct,
    "Inflation_Rate": user_inflation,
    "Foreign_Aid_Billions": user_aid
}])

predicted_spending_billions = model.predict(future_scenario)[0]
predicted_spending_usd = predicted_spending_billions * 1_000_000_000

# ==========================================
# 5. ATTRITION MODEL (Personnel Reduction)
# ==========================================
gross_troops = int(projected_defaults["Total_Troops"])

RETIREMENT_RATE = 0.05       # ~5% standard retirement/separation
NATURAL_DEATH_RATE = 0.001   # ~0.1% expected natural mortality
TRAINING_DEATH_RATE = 0.0002 # ~0.02% expected training exercise fatalities

retirements = int(gross_troops * RETIREMENT_RATE)
natural_deaths = int(gross_troops * NATURAL_DEATH_RATE)
training_deaths = int(gross_troops * TRAINING_DEATH_RATE)

net_troops = gross_troops - (retirements + natural_deaths + training_deaths)

# ==========================================
# 6. FORMATTING UTILITIES
# ==========================================
def format_large_number(num):
    """Converts a large number into a readable English string (Trillions/Billions/Millions)."""
    if num >= 1_000_000_000_000:
        return f"${num / 1_000_000_000_000:.2f} Trillion"
    elif num >= 1_000_000_000:
        return f"${num / 1_000_000_000:.2f} Billion"
    elif num >= 1_000_000:
        return f"${num / 1_000_000:.2f} Million"
    else:
        return f"${num:,.2f}"

# ==========================================
# 7. SIMULATION OUTPUT
# ==========================================
print("\n" + "="*50)
print("=== 2025 SIMULATION RESULTS ===")
print("="*50)
print(f"Predicted Total Military Spending = {format_large_number(predicted_spending_usd)} (${predicted_spending_usd:,.0f})")
print(f"Projected Gross Army Strength (Before Attrition) = {gross_troops:,}")
print(f"  - Less Retirements/Separations: {retirements:,}")
print(f"  - Less Natural Deaths: {natural_deaths:,}")
print(f"  - Less Training Casualties: {training_deaths:,}")
print(f"Net Active Servicemembers = {net_troops:,}")
print(f"Nuclear Submarines = {int(projected_defaults['Nuclear_Submarines']):,}")
print(f"Active Fighters = {int(projected_defaults['Active_Fighters']):,}")
print(f"Aircraft Carriers = {int(projected_defaults['Aircraft_Carriers']):,}")

military_efficiency = predicted_spending_usd / net_troops
print(f"\nDerived Metric (Efficiency):")
print(f"Budget per Active Soldier = {format_large_number(military_efficiency)}")

# ==========================================
# 8. SAVE HISTORY (Last 20 Runs)
# ==========================================
def save_simulation_history():
    HISTORY_FILE = "simulation_history.json"
    MAX_HISTORY = 20
    
    current_run = {
        "timestamp": datetime.now().isoformat(),
        "inputs": {
            "gdp_per_capita": user_gdp,
            "military_pct_gdp": user_mil_pct,
            "inflation_rate": user_inflation,
            "foreign_aid_bn": user_aid
        },
        "outputs": {
            "predicted_spending_usd": predicted_spending_usd,
            "net_active_troops": net_troops,
            "military_efficiency_usd": military_efficiency
        }
    }
    
    try:
        # Load existing history if possible
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        else:
            history = []
            
        # Append new run to list and slice to keep only the last 20
        history.append(current_run)
        history = history[-MAX_HISTORY:]
        
        # Save back to file
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=4)
            
        print(f"\n[System] Successfully saved simulation log to {HISTORY_FILE} (Tracking last {len(history)} runs).")
        
    except Exception as e:
        print(f"\n[Warning] Could not save simulation history due to an error: {e}")

# Trigger the save module
save_simulation_history()