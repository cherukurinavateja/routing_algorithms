import numpy as np
import random
from utils import Util
import copy
import pandas as pd
from datetime import datetime


class SimulatedAnnealing:

    def sAnnealing(self,depo,customerList):
        startTime=datetime.now()

        routeList=[]
        initialTemp=100  #initial temperature
        finalTemp=1      #final temeprature
        noOfIterations=6000  #number of iterations
        coolingFactor=0.98

        routeList.insert(0,depo)#adding firstcustomer as depo

        routeList.insert(1,depo)#adding second customer as depo 

        for i in customerList:
            routeList.insert(len(routeList)-1,i)

        
        
        #assigning initial route as best,current,neighbour routes
        bestRouteList=routeList.copy() 
        currRouteList=routeList.copy()
        neighbourRouteList=routeList.copy()
        
        #calculating the cost the best,current routes
        costOfBestRouteList=Util().calculateDistanceForRoute(bestRouteList)
        costOfCurrRouteList=Util().calculateDistanceForRoute(currRouteList)

        currentTemp=initialTemp #setting current temperature as initial temperature


        while currentTemp > finalTemp:

            iteration = 1
            while  iteration < noOfIterations:

                swappedList = Util().swapRoute(currRouteList)
                neighbourRouteList= swappedList.copy() #swapping the 2 random routes 
                costOfNeighbourRouteList=Util().calculateDistanceForRoute(neighbourRouteList)

                costDiff = costOfNeighbourRouteList - costOfCurrRouteList

                sigmoidFunction= 1/(1+np.exp(costDiff/currentTemp))

                if (costOfNeighbourRouteList > costOfBestRouteList) & (sigmoidFunction > random.random()) :
                    currRouteList.clear()
                    currRouteList = neighbourRouteList.copy()
                    costOfCurrRouteList=costOfNeighbourRouteList

                elif costOfNeighbourRouteList < costOfBestRouteList:
                    bestRouteList.clear()
                    bestRouteList=neighbourRouteList.copy()
                    costOfBestRouteList=costOfNeighbourRouteList
                    currRouteList=neighbourRouteList.copy()
                    costOfCurrRouteList=costOfNeighbourRouteList

                neighbourRouteList.clear()
                iteration=iteration+1

            currentTemp = currentTemp * coolingFactor

        #checking performance of the algorithm    
        endTime=datetime.now()
        computationTime=(endTime-startTime).total_seconds()

        #Returns Best Route
        finalRoute={
                "path":bestRouteList,
                "totalDistance":costOfBestRouteList,
                "timeTaken":computationTime
        }
        
        # print(costOfBestRouteList)
        # print("\n")
        return finalRoute




        
