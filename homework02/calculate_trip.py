#calculate the meterorite_sites.json file and calculates the time required to visit and take samples from the five sites in order
import json
import math

def mars_dist(latitude1, longitude1, latitude2, longitude2):

    lat1 = math.radians(latitude1)
    lat2 = math.radians(latitude2)
    long1 = math.radians(longitude1)
    long2 = math.radians(longitude2)
    d = math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(abs(long1-long2))) #apart of the calculation of the great-circle distance formula 
    #d = r*cos^-1[cosa cosb  cos(x-y) + sina sinb] with d being distance, lat(a,b) and long(x,y), and r as mars’s radius
    return (3389.5 * d) #3389.5 is mars's radius

with open("meteorite_sites.json", "r") as f:
    data = json.load(f) #data of meteroite landings

# starting location
lat_start = 16.0
long_start = 82.0

#initialize variables
speed = 10  # in km/hr
sample_times = {"stony": 1, "iron": 2, "stony-iron": 3} #in hours
total_time = 0
leg_count=0

#find time to travel from one site to another
for site in data["sites"]:
    leg_count = leg_count+1
    distance = mars_dist(lat_start, long_start, site["latitude"], site["longitude"])
    travel_time = distance / speed #in hours
    sample_time = sample_times[site["composition"]]
    total_time = total_time + sample_time + travel_time
    print("leg",leg_count,": time to travel =",travel_time,"hrs, time to sample =",sample_time,"hrs") #print leg info
   # update starting variable
    lat_start = site["latitude"]

#print trip summary
print("====================================")
print("number of legs =", leg_count,", total time elapsed =", total_time, "hrs")
