#generate five meteorite landing sites
import json
import random

def random_coords():
   return (random.uniform(16.0, 18.0), random.uniform(82.0, 84.0))

sites = [] #new dict for sites
compositions = ["stony", "iron", "stony-iron"] #the composition options

for i in range(5): #generate five sites
   lati, longi = random_coords()
   composition = random.choice(compositions)
   site = {"site_id": i, "latitude": lati, "longitude": longi, "composition": composition}
   sites.append(site)

info = {"sites": sites} #creates dict with site info

with open("meteorite_sites.json", "w") as f: #write data and save as a json file
   json.dump(info, f)


