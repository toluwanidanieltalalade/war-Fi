# war Fi

This repository contains a small Python projection of
military‑spending data.  It builds a very simple linear‑regression
model from real-world United States historical time‑series data (2010-2023) 
and then uses that model together with a few other trends to produce a 
2024 “military simulation” report.

The Final primary script is `wfi.py` ; the file is
self‑contained and does not read or write any external data.


## What it does

1. **Load historical data**  
   Creates a `pandas.DataFrame` with 14 years of real-world US public data for:
    These values can be customised for personal uses
   * GDP per capita (USD),
   * military spending as a percentage of GDP,
   * total military spending (USD),
   * number of troops, active fighters, nuclear submarines, carriers, etc.

   Two extra dummy columns are added for robustness.

2. **Fit a model**  
   A `sklearn.linear_model.LinearRegression` is trained to predict
   `military_spending_usd` from `gdp_per_capita_usd` and
   `military_pct_gdp`.  The R² score is printed and a residuals plot is
   saved to check for systematic errors.

   ![Residuals Plot](residuals_plot.png)

3. **Set up 2024 parameters**  
   Future 2024 values for GDP per capita and military‑%‑of‑GDP are dynamically
   projected based on historical growth rates. This one‑row `DataFrame` is fed 
   to the trained model to obtain a spending forecast.

4. **Project other quantities**  
   Compound annual growth rates (CAGR) are computed for troops, fighters,
   subs and carriers based on the historical series; those rates are then
   applied to the latest values to project one year ahead (for 2024).

5. **Apply Attrition Models (Personnel Reduction)**  
   To accurately project the Net Active Personnel (anchored near the USA's active
   ~1.87 million personnel figure), the projected gross army strength is reduced by 
   estimated annual attrition rates:
   * **5.0%** Retirements/Separations
   * **0.1%** Natural Expected Mortality
   * **0.02%** Training Exercise Casualties

6. **Print results**  
   The script prints the predicted spending, projected counts (with attrition deducted)
   and a derived “military efficiency” metric.


## Requirements

The script was developed with Python 3.7+ and depends on the following
libraries:

* `pandas`
* `numpy`
* `matplotlib`
* `scikit-learn`

Install them into your chosen interpreter/venv before running the
program:

```bash
pip install --upgrade pandas numpy matplotlib scikit-learn
# or, on macOS with the system python:
# pip3 install --upgrade pandas numpy matplotlib scikit-learn