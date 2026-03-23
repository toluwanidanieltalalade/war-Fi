# WarFi: The Military Budget Forecaster.
War Finance Influenced by the book economics of war by Horst Mendershausen.
## What is this project?
WarFi is a simple Python program that tries to predict how much money the United States will spend on its military in the year **2025**. It also predicts how many soldiers, submarines, planes, and aircraft carriers the military will likely have.

Think of it like a weather forecast, but instead of predicting rain tomorrow based on the clouds today, it predicts the military budget based on how much the US government has spent in the past.

## How does it work? 

I built this program to work in four easy steps:

1. **Studying the Past (The Data)**  
   I give my program a list of actual US history from the years 2010 to 2023. I tell it:
   * How big the US Economy was (GDP)
   * The percentage of the economy spent on the military
   * The inflation rate (how fast prices went up)
   * The amount of foreign military aid the US sent to other countries
   * And the exact budget and troop sizes for those years.
   The image for this will be in the folder you forked, showing a linear graph of real-world data during this time period.

2. **Finding the Pattern (The Math)**  
   My program uses **Linear Regression**, which is just a fancy math term for "connecting the dots." It draws a line through all that historical data to figure out the exact mathematical relationship between the economy falling/rising and the military budget getting smaller/bigger. 

3. **Playing "What-If" (The Simulator)**  
   When you run the script, it pauses and asks you a question: *What do you think the economy and inflation will look like in 2025?* 
   You get to be the boss and type in your own guesses! (Or, you can just press `Enter` to skip, and it will use the historical average trend). It takes your answers and uses that "connect the dots" math pattern from earlier to spit out an exact dollar amount for the 2025 budget!

4. **Accounting for Real Life (Attrition)**  
   Instead of just blindly guessing the number of soldiers, my program uses common sense. It predicts the *total* number of soldiers, and then subtracts an estimated 5% for soldiers who retire, and tiny fractions for natural accidents or deaths, so that the final answer is realistic.

5. **Saving Your Score (History Log)**
   My program will save your recent simulated guesses into a file called `simulation_history.json` so you can look back and see what you tested!
   Please note that this save file automatically has a max length of twenty data entries. After that, it will start deleting the oldest data entry to make room for the newest data entry to avoid massive file sizes and "buffering" or lag when reading it.

---

## How to use it yourself!

You need to have Python installed on your computer.

1. **Install the required side-packages** by running this in your terminal:
   ```bash
   pip install pandas numpy matplotlib scikit-learn
   ```

2. **Run the simulator**:
   ```bash
   python3 wfi.py
   ```

3. **When my program asks you questions in the terminal**, type your number guesses and press enter!

4. **Clear Your History Log (Optional)**  
   If you ever want to reset the saved `simulation_history.json` tracking file, you can wipe it clean safely at any time by running:
   ```bash
   python3 wfi.py --clear-history
   ```

### Example of what it looks like:

```text
==================================================
INTERACTIVE MILITARY BUDGET Forecaster (2025)
==================================================
Enter your own estimates for 2025 to see how the budget reacts.
Press [ENTER] to skip and just use the natural historical trend.

Estimated GDP Per Capita in USD (Default: 88427.91): 95000
Military Spending as % of GDP (Default: 3.21): 4.5
Estimated Inflation Rate (%) (Default: 4.74): 3.0
Foreign Military Aid (Billions USD) (Default: 64.64): 18.0

==================================================
=== 2025 SIMULATION RESULTS ===
==================================================
Predicted Total Military Spending = $1.20 Trillion ($1,198,498,217,114)
Projected Gross Army Strength (Before Attrition) = 1,934,280
  - Less Retirements/Separations: 96,714
  - Less Natural Deaths: 1,934
Net Active Servicemembers = 1,835,246
...
```

Have fun forecasting the future!


##Sneak peak :bowtie:
-Version 2 will focus on forecasting United kingdom military spending and nhs data
-Version 3 we go across europe and try to forecast Asain spending 

