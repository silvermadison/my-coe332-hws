import requests
import json
import math
from typing import List

def calc_turbidity(data:List[dict]) ->float:
    """
    This function iternates through a given list of dictionaries of turbidity data to find the average water turbidity of the first five data points.

    Args:
        data (list): A list of dictionaries, each dict should have the same keys

    Returns:
        current_turbidity (float): The average water turbidity of first five data points
    """

    current_turbidity = 0
    for i in range(5):
        current_turbidity = current_turbidity + data[i]['detector_current']*data[i]['calibration_constant']
    return current_turbidity/5

def calc_min_time(turbidity:float, safe:float, decay_factor:float) ->float:
    """
    This function finds the minimum time required for the turbidity to return below the safe threshold.

    Args:
        turbidity (float): the current average water turbidity
        safe (float): Is a given safe threshold the water turbidity should be below.
        decay_factor (float): Is the decaying factor per hour, expressed as a decimal

    Returns:
        hours (float): the number of hours it takes to return below the safe threshold
    """

    if turbidity <= safe:
        hours = 0
    else:
        hours = math.log(safe/turbidity,1 - decay_factor)
    return hours

def main():
    c_data = requests.get("https://raw.githubusercontent.com/wjallen/turbidity/main/turbidity_data.json")
    d_data = c_data.json()
    data = d_data["turbidity_data"]

    #constants
    safe_threshold = 1.0
    decay_factor = 0.02

    #variables
    current_turbidity = calc_turbidity(data)
    min_time = calc_min_time(current_turbidity, safe_threshold, decay_factor)

    #print messages
    print("Average turbidity based on five most recent measurements = ", current_turbidity, "NTU")
    if current_turbidity > safe_threshold:
        print("Warning: Turbidity is above threshold for safe use")
    else:
        print("Info: Turbidity is below threshold for safe use")
    print("Minimum time required to return below a safe threshold = ", min_time,"hours")

if __name__ == "__main__":
   main()


