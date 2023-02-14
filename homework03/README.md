# Homework 3: Turbidity Data

## Objective
The key takeaway from this project is to practice code organization, documentation including type hints and docstrings, and unit testing. The contents of this folder include 2 scripts solving Tasks 1 and 2.

## Requirements
Installation of python3 and pytest were used and are required to run these programs.

The requests, JSON, math, and typing modules are used within this code to support data handling, complex math functions, and type hints. Errors will arise if these modules are not installed correctly.

Finally, the "analyze_water.py" file contains a reference to a JSON file which can also be accessed [here]( https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json). The data has information on turbidity which is used to determine water quality. Using the requests module, as shown in the "analyze_water.py" file, you can access and use this data. 

## Clean Water Analysis
Homework 3 follows after Homework 2 where a robotic vehicle on Mars explored meteorite landing sites in Syrtis Major and collected meteorite samples. In Homework 3, the samples are analyzed. In order to analyze the samples, clean water is needed. Therefore, the purpose of this project is to assess the current water quality, given as turbidity data, to determine if the water is clean or the lab needs a boil water notice. 

### Task 1
Task 1, completed within the “analyze_water.py” file, is to print (1) the current water turbidity (being the average of the first five data points), (2) whether the turbidity is below a safe threshold or not, and (3) the minimum time required for turbidity to fall below the safe threshold. If turbidity is already above the safe threshold then its output would be 0 hours. 
Output may look similar to the following depending on if turbidity is above or below the safe threshold.
```
Average turbidity based on most recent five measurements = 1.1992 NTU
Warning: Turbidity is above threshold for safe use
Minimum time required to return below a safe threshold = 8.99 hours
```

```
Average turbidity based on most recent five measurements = 0.9852 NTU
Info: Turbidity is below threshold for safe use
Minimum time required to return below a safe threshold = 0 hours
```
If turbidity is above the threshold, that means it is not clean water and the lab will need a boil water notice. If turbidity is below the threshold then the water is clean enough to test the meteorite samples. 


#### Part 1 
In order to print the first value, the equation below is used to calculate current water turbidity. In a separate function named “calc_turbidity”, the turbidity value for the first five data points is calculated. The values within the equation are located in the turbidity data list with keys “calibration_constant” and “detector_current”.
```
T = a0 * I90
T = Turbidity in NTU Units (0 - 40)
a0 = Calibration constant
I90 = Ninety degree detector current
```

#### Part 2 
In order to print the second statement, simply compare the calculated turbidity with the given safe threshold of 1.0 NTU.

#### Part 3
To print the last statement, another function named “calc_min_time” was created to find the minimum time for the turbidity to fall below the threshold. An if-else clause was used so that if the water was safe, hours could be set to 0. To calculate the number of hours till turbidity was below the safe threshold the equation below was used and manipulated to solve for hours elapsed (b).
```
Ts > T0(1-d)**b
Ts = Turbidity threshold for safe water
T0 = Current turbidity
d = decay factor per hour, expressed as a decimal
b = hours elapsed
```
Constraints of the equation above include the given values:
* The turbidity threshold for safe water is a constant, 1.0 NTU
* The decay factor per hour is a constant, 2% or 0.02 expressed as a decimal

### Task 2
Task 2, completed within the "test_analyze_water.py" file, is to write unit tests confirming the functions from Task 1 correctly compute turbidity and minimum time for the turbidity to fall below the threshold. The tests within this file ensure that the math of the functions are correct.

