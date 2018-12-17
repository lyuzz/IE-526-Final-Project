
# coding: utf-8

# In[203]:


import myFunction as mf
import datetime


# In[204]:


def getRoute_LD(customerID):
    # Initialization
    custID = customerID[:] # make a copy of customerID
    nbCustomer = len (customerID)
    route = []
    starNode = 0
    toNode = 1

    # get a route by the least distance
    for attemp in range(1,nbCustomer + 1):
        Dist = mf.distance(starNode,custID[0])

        for node in custID:
            if (node != starNode):
                if mf.distance(starNode,node) <= Dist:
                    toNode = node 
                    Dist = mf.distance(starNode,node)

        custID.remove(toNode)
        route.append(toNode)
        starNode = toNode
        print("Attemp:",attemp,"/",nbCustomer)
        
    # print('The final routes are:\n',route,"\n")
    return route


# In[211]:


def cut(route):
    routes = []
    fromNode = 0
    weight = 0
    volume = 0
    distance = 0
    time = 0
    routePlan = [0]
    truck = 1
    travelCost = 0
    timeExceed = 0

    for nextNode in route:
        # If next customer could fit.
        if ((weight+mf.weight(nextNode)<=mf.max_weit)&(volume+mf.volume(nextNode)<=mf.max_volu)&(distance+mf.distance(fromNode,nextNode)+mf.distance(nextNode,0)<=mf.max_driv)&(time<=mf.max_time+mf.time(fromNode,nextNode)+mf.time(nextNode,0))):
            routePlan.append(nextNode)
            distance = distance + mf.distance(fromNode,nextNode)
            time = time + mf.time(fromNode,nextNode)
            weight = weight + mf.weight(nextNode)
            volume = volume + mf.volume(nextNode)
            fromNode = nextNode  

        # If next customer doesn't fit, let truck go back.
        else:
            routePlan.append(0)
            time = time + mf.time(fromNode,0)
            distance = distance + mf.distance(fromNode,0)
            travelCost = travelCost + distance * 14 /1000
            routes.append(routePlan)
            
            # Print the route of this truck.
            print("The route of truck",truck,"is",routePlan)
            # print(weight,volume,time,distance)

            # Reset all of the capacity and make assignment for next truck.
            truck = truck + 1
            weight = 0
            volume = 0
            distance = 0
            time = 0
            routePlan = [0]
            fromNode = 0

            # If this node could fit in a new truck?
            if ((weight<=mf.max_weit)&(volume<=mf.max_volu)&(distance+mf.distance(fromNode,nextNode)+mf.distance(nextNode,0)<=mf.max_driv)&(time<=mf.max_time+mf.time(fromNode,nextNode)+mf.time(nextNode,0))): 
                distance = distance + mf.distance(fromNode,nextNode)
                time = time + mf.time(fromNode,nextNode)
                weight = weight + mf.weight(nextNode)
                volume = volume + mf.volume(nextNode)
                routePlan.append(nextNode)
                fromNode = nextNode

            else:
                print("Error! This is no feasible solution because node",nextnode,"can't fit in a new truck")
                break

    # The last loop is completed and let this truck go home.
    routePlan.append(0)
    time = time + mf.time(fromNode,0)
    distance = distance + mf.distance(fromNode,0)

    # caculate the cost
    travelCost = travelCost + distance * 14 /1000
    fixCost = truck * 300

    # print the result
    print("The route of truck",truck,"is",routePlan)
    routes.append(routePlan)
    # print(weight,volume,time,distance)
    print("Completed!")
    return routes


# In[212]:


def Algo_LD(customerID):
    timeBegin = datetime.datetime.now()
    route = getRoute_LD(customerID)
    routes = cut(route)
    timeFinish = datetime.datetime.now()
    time = timeFinish - timeBegin
    print("Run time:",time)   
    return routes


# # Test

# In[213]:


#customerID= [185,888,423,360,660,662,137,322,631,689,559,550,582,606,943,901,121,763,972,303
#,247,17,140,101,255,851,645,977,601,810,406,400,182,484,276,359,947,215,616,221,299,833,184,604,
#443,283,51,109,331,842]
#Algo_LD(customerID)

