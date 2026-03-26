# WarFi - Technical Workflow & Core Concepts

This document serves as a detailed technical breakdown of the `wfi.py` architecture, mapping the mathematical models and system engineering principles used to predict military spending and personnel limits.

## 1. Multiple Linear Regression (Machine Learning)
**Concept Reference:** [Scikit-Learn: Ordinary Least Squares](https://scikit-learn.org/stable/modules/linear_model.html#ordinary-least-squares)

The script uses `sklearn.linear_model.LinearRegression` to form a multidimensional plane mapping macroeconomic inputs (Features: $X$) to the target budget (Response: $Y$).
- **Features ($X$):** GDP Per Capita, Military Spending as % of GDP, Inflation Rate, Foreign Military Aid.
- **Complexity:** Training complexity scales at $O(N \cdot P^2)$ where $N$ is the dataset row count and $P$ is the feature count. Given the dataset is currently confined to $14$ historical rows, the training latency is nominal ($\approx O(1)$).

## 2. Compound Annual Growth Rate (CAGR) Projection
**Locality:** `calculate_future_trend()` function.

Instead of predicting all tertiary variables via Machine Learning, non-core features (e.g., Number of Aircraft Carriers, Nuclear Submarines) are projected via their historical Compound Annual Growth Rate over the standard tracking timeline.
- **Formula Used:** $\left(\frac{V_{final}}{V_{initial}}\right)^{\frac{1}{t}} - 1$
- Where $t$ is the `total_years` interval in the dataset. This derives the natural year-over-year percentage trajectory to establish a mathematical baseline without overfitting a secondary ML model on low-variance data.

## 3. Deterministic Attrition Modeling
**Locality:** Attrition block (Lines ~142-154).

The simulator applies fixed probabilistic decay rates to calculate logical personnel overhead and survivability rates over a single simulation phase instead of raw approximations.
- **Retirement Rate:** $5.0\%$
- **Natural Mortality:** $0.1\%$
- **Training Casualties:** $0.02\%$
- **Logic Pipeline:** `Net Troops = Gross Troops - (Retirements + Natural Deaths + Training Deaths)`

## 4. Input Validation and Boundary Enforcement
**Concept Reference:** Data Type Sanitization & Float Overflow Constraints

- String stripping removes syntactical barriers (e.g., `$`, `%`, `,`). 
- Standard mathematical conversions are tightly constrained to strict floats `0.0 <= val <= 1e15` while aggressively discarding `numpy.inf` (Infinity) and `numpy.nan` (Not a Number) representations using `np.isinf` and `np.isnan`. 
- **Impact:** This prevents exponential memory cascades or downstream metric corruption (like `ZeroDivisionError` when calculating military efficiency via division by troops).

## 5. Atomic File Replacement (Concurrency Safety)
**Concept Reference:** POSIX Time-of-Check to Time-of-Use (TOCTOU) Mitigation

- **Mechanism:** Writing to a live JSON history log sequentially is vulnerable to corruption if the main thread halts or another instance calls the script concurrently.
- **Execution:** WarFi writes a temporary file (`simulation_history.json.tmp`) using full JSON dumps and formally commits it via `os.replace`. 
- **Impact:** On POSIX systems, `os.replace` resolves to an atomic `rename` system call. This guarantees that processes either parse the old file perfectly or the new file perfectly; halting midway or parallel writes will not destroy the previously indexed JSON array structure.
