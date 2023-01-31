# Homework 2: Working with JSON

## Objective
The objective of this homework is to gain a better understanding of how to use the JSON library to read, write, and analyze data. This homework also includes applications of random and math modules. 
The contents of this folder include scripts solving Task 1 and 2.

## Mars Meteorite Landing Sites
The task of this homework is to explore meteorite landing sites in Sytris Major in order to operate a robotic vehicle on Mars.

### Task 1
The first task, completed within the "generate_sites.py" file, is to randomly generate five meteorite landings in Sytris Major. This means the landing site latitudes must range between 16.0 and 18.0 degrees North and the longitudes must range between 82.0 and 84.0 degrees East. Each landing site must also include the meteorite composition of either stony, iron, or stony-iron. Finally, this information must be saved into a dictionary with key "sites" and stored in a new JSON file. 

## Task 2
Using the new JSON file created in Task 1, Task 2 calculates the time required to visit and take samples from each of the five meteorite landing sites in order of index, which is completed within the "calculate_trip.py" file. Constraints include a maximum robot speed of 10 km per hour and sampling time of 1 hour for stony meteorites, 2 hours for iron meteorites, and 3 hours for stony-iron meteorites. It is assumed the robot starts at {16.0,82.0}. The great-circle distance algorithm is used to calculat the distance between points, assuming the radius of Mars is 3389.5 km. For each leg of the trip descriptive information should be printed (time to travel, time to sample, etc.). And finally, a summary of the trip after sampling the last meteorite should be printed. 

## Instructions 
Installation of python3 was used and is recommended to run these programs.
The generate_sites file must be run first so that the new JSON file of meteorite sites is created. Within the same path, run the calculate_trip file, which uses the newly create JSON file. The result of this file is a summary of how long it would take to visit and sample all the meteorite landings in order of index given the listed constraints in Task 2. 
