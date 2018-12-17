
# coding: utf-8

# In[37]:


import pandas as pd
from datetime import datetime
data = pd.read_excel('../Materials/input_node.xlsx')
dist_and_time = pd.read_csv('../Materials/input_distance-time.txt')


# In[38]:


# The capacity of truck
max_weit = 2.5
max_volu = 16
max_driv = 200000
max_time = 720
cost_distance = 14
cost_vehicle = 300
cost_wait = 24


# In[47]:


# get the distance from i to j
def distance (fromNode,toNode):
    if fromNode == toNode:
        print("Illegal (distance): i = j.")
    else:
        dist = dist_and_time[(dist_and_time.from_node == fromNode) & (dist_and_time.to_node == toNode)]
        return int(dist.distance)

# get the traval time from i to j
def time (fromNode,toNode):
    if fromNode == toNode:
        print("Illegal (time): i = j.")
    else:
        dist = dist_and_time[(dist_and_time.from_node == fromNode) & (dist_and_time.to_node == toNode)]
        return int(dist.spend_tm)

# get weight of node i
def weight (i):
    if i in range(1,1001):             # check if i is allowed
        row = data[data.ID == i]
        return float(row.pack_total_weight)
    else:                            # if i is not allowed     
        print("Illegal (weight): Customer ID should be between 1 to 1000.")
        
# get volume of node i
def volume (i):
    if i in range(1,1001):
        row = data[data.ID == i]
        return float(row.pack_total_volume)
    else: 
        print("Illegal (volume): Customer ID should be between 1 to 1000.")
        
def cost (routes):
    Tcost = 0
    routesCopy = routes[:]
    for route in routesCopy:
        Tweight = 0
        Tvolume = 0
        Tdistance = 0
        Ttime = 0
        fromNode = 0
        flag = 0
        
        if 0 in route:
            route.remove(0) 
        if 0 in route:
            route.remove(0) 
            
        for node in route:
            Tweight = Tweight + weight(node)
            Tvolume = Tvolume + volume(node)
            Tdistance = Tdistance + distance(fromNode,node)
            Ttime = Ttime + time(fromNode,node)
            fromNode = node
        Tdistance = Tdistance + distance(fromNode,0)
        Ttime = Ttime + time(fromNode,0)

        if Tweight > max_weit or Tvolume > max_volu or Ttime > max_time or Tdistance > max_driv:
            print("Route",route,"is not feasible!")
            print("Weight,volume,time,distance:\n",Tweight,Tvolume,Ttime,Tdistance)
            flag = flag + 1
        else:
            Tcost = Tcost + (Tdistance * 14 / 1000) + 300
    if flag == 0:
        return Tcost


def isFeasible (route):
    routeCopy = route[:]
    if 0 in routeCopy:
        routeCopy.remove(0) 
    if 0 in routeCopy:
        routeCopy.remove(0)
    Tweight = 0
    Tvolume = 0
    Tdistance = 0
    Ttime = 0
    fromNode = 0

    for node in routeCopy:
        Tweight = Tweight + weight(node)
        Tvolume = Tvolume + volume(node)
        Tdistance = Tdistance + distance(fromNode,node)
        Ttime = Ttime + time(fromNode,node)
        fromNode = node
    Tdistance = Tdistance + distance(fromNode,0)
    Ttime = Ttime + time(fromNode,0)

    if Tweight > max_weit or Tvolume > max_volu or Ttime > max_time or Tdistance > max_driv:
        #print("Route",routeCopy,"is not feasible!")
        #print("Weight,volume,time,distance:\n",Tweight,Tvolume,Ttime,Tdistance)
        return False
    else:
        return True

