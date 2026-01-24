# Data Analysis 

## Dataset
- Name: sample_equipment_data
- Source:datasets\sample_equipment_data.csv
- Description attributes:('Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature')


## Data Preparation
a. Null Values
Null Values in numeric types - Flowrate, Pressure, Temperature replaced by mean
drop record if >= 3 null values found
b. Duplicate Values
drop fully duplicated records


## Analysis Performed
STEP1: UNIVARIATE ANALYSIS
Min, Max, Avg Numeric attributes can be uused to caution about equipment
a. Histograms and density plots for numeric attributes
b. Bar chart to understand the distribution of Types

STEP2: BIVARIATE ANALYSIS
Pair	Correlation
Flowrate – Temperature	0.79
Flowrate – Pressure	0.54
Pressure – Type_Compressor	0.61
Temperature – Type_Reactor	0.61
Pressure – Type_Valve	-0.75
Flowrate – Type_Valve	-0.84
Temperature – Type_Compressor	-0.59
Temperature – Type_Valve	-0.46


Variable 1	Variable 2	Correlation	Plot Type
Flowrate	Temperature	0.79	Scatter + Regression
Flowrate	Pressure	0.54	Scatter + Regression
Pressure	Type_Compressor	0.61	Box Plot
Temperature	Type_Reactor	0.61	Box / Violin Plot
Pressure	Type_Valve	-0.75	Box Plot
Flowrate	Type_Valve	-0.84	Box / Violin Plot
Temperature	Type_Compressor	-0.59	Box Plot
Temperature	Type_Valve	-0.46	Box Plot

STEP3: MULTIVARIATE ANALYSIS
Uses groupBy, query and aggregate methods based on common queries of user like:


## Issues
Unknown metric types - What metric of temperature/pressure/flow rate is used? (Rename Numeric Attributes with metric names)
using mean for missing numeric attributes smoothens the data

## Future Scope
Ask questions and obtain a plot(can use groupBy, query and aggregate methods)
Use advanced missing value finding techniques like regression


