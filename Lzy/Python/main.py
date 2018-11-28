"""
A solver that solves the Vehicle Routing Problem with Time Windows and Capacity Constraint.
This is the main file. Model is defined in model.py, where cplex 12.8 Acedemic Edition.

Model Unit:
Time : Hour
Distance : Kilometer
Weight : Ton
Volume : Cubic Meter
"""

# import
import pandas as pd
from model import model

# Main
def main():
    """main"""

    # reading data
    customer_data = pd.read_csv("customer_sample.csv")
    dist_time_data = pd.read_csv("dist_time_sample.csv")
    # delete unecessary data
    del customer_data['lng']
    del customer_data['lat']

    # parameter inpput
    K = 50          # number of vehicles
    c_f = 300       # fixed vehicle cost
    c_d = 14        # travel cost
    c_w = 24        # waiting time cost
    t_un = 0.5      # unloading time
    D_max = 120     # maximal distance allowed
    W_max = 2.5     # maximal weight
    V_max = 16      # maximal volume
    T_thr = 8       # wait time threshold

    # modeling and solving
    model(customer_data, dist_time_data, c_f, c_d, c_w, t_un, D_max, W_max, V_max, T_thr, K)
    

# calling main
if __name__ == "__main__":
    main()
