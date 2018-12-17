
# coding: utf-8

# In[7]:


import myFunction as mf
import datetime


# In[17]:


def Algo_C_W(customerID):
    timeBegin = datetime.datetime.now()
    
    custID = customerID[:]
    custID.sort()
    routes = []
    
    for i in custID:
        routes.append([i])

    sij = []
    for i in custID:
        for j in custID:
            if i != j:
                x = [(mf.distance(i,0) + mf.distance(0,j) - mf.distance(i,j)),i,j]
                sij.append(x)
    sij.sort(reverse = True)

    for item in sij:  
        if item != []:
            flag = item[1]
            flag2 = item[2]

            for subroute in routes:
                if subroute[len(subroute)-1] == flag :
                    subroute.append(flag2)

                    if mf.isFeasible(subroute) == 0:
                        subroute.remove(flag2)
                    else:
                        routes.remove([flag2])
                        # clear sij because some node can not be used any more
                        for element in sij:   
                            if (element != []) and ((element[1] == flag) or (element[2] == flag) or (element[2] == flag2)):
                                element.clear()
                        break
                        
    timeFinish = datetime.datetime.now()
    time = timeFinish - timeBegin
    print("Run time:",time) 
    return routes

