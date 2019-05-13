import numpy as np
from utils import Util
import copy
import pandas as pd
from datetime import datetime

class Tabu:

    def tabuSearch(self,depo,customerList):
        startTime=datetime.now()

        currentRoute=[]#initial route
        currentRoute.insert(0,depo)#adding firstcustomer as depo

        currentRoute.insert(1,depo)#adding second customer as depo 

        for i in customerList:
            currentRoute.insert(len(currentRoute)-1,i)

        bestRoute=currentRoute.copy()

        #calculating the cost the best,current routes
        costOfBestRouteList=Util().calculateDistanceForRoute(bestRoute)
        costOfCurrRouteList=Util().calculateDistanceForRoute(currentRoute)

        #storing distance,indexes of every possible swaps for single iteration and clearing list after iteration
        swaproutesdistances=[]
        swaproutesindex=[]

        #storing tabulist and tabumoves
        tabulist=[]
        tabumoves=[]
        
        #storing best distance after every iteration
        iterationwiseBestDistance=[]
        
        #setting number of iterations 
        maxIterations=2*len(currentRoute)
        noofiterations=0
        #iterating
        while noofiterations < maxIterations:
            for i in range(len(currentRoute)-2):

                for j in range(len(currentRoute)-2):
                    if i!=j:
                        currentRoute[i+1],currentRoute[j+1]= currentRoute[j+1],currentRoute[i+1]#swapping the routes
                        distance=Util().calculateDistanceForRoute(currentRoute)
                        swaproutesdistances.append(distance)
                        swaproutesindex.append([i+1,j+1])
                        currentRoute[i+1],currentRoute[j+1]= currentRoute[j+1],currentRoute[i+1]

                    
            #getting minimum distance,indexposition,tabumove of minimum distance of each iteration
            minimum=min(swaproutesdistances)
            indexposition=swaproutesdistances.index(minimum)
            tabumove=swaproutesindex[indexposition]
           
           #removing tabu moves after every iteration
            for i in tabumoves:
                if i in tabulist:
                    tabulist.remove(i)
                                
  
            if (minimum < costOfBestRouteList) & (tabumove in tabulist):

                if  len(iterationwiseBestDistance)!=0: 
                    #checking aspiration criteria
                    if minimum < min(iterationwiseBestDistance):
                        #if aspiration criteria satisfies remove the tabu move from the tabu list
                        tabulist=list(filter(lambda x:x!=tabumove,tabulist))
                        #making the tabu move as best move ,swapping the moves
                        bestRoute[tabumove[0]],bestRoute[tabumove[1]]=bestRoute[tabumove[1]],bestRoute[tabumove[0]]
                        currentRoute[tabumove[0]],currentRoute[tabumove[1]]=currentRoute[tabumove[1]],currentRoute[tabumove[0]]
                        #adding the tabu move to the tabu list
                        for i in range(3):
                            tabulist.append(tabumove)

                        iterationwiseBestDistance.append(minimum)
                        costOfBestRouteList=minimum
                        costOfCurrRouteList=minimum
                        tabumoves.append(tabumove)      

            elif minimum < costOfBestRouteList :

                bestRoute[tabumove[0]],bestRoute[tabumove[1]]=bestRoute[tabumove[1]],bestRoute[tabumove[0]]
                currentRoute[tabumove[0]],currentRoute[tabumove[1]]=currentRoute[tabumove[1]],currentRoute[tabumove[0]]
                for i in range(3):
                    tabulist.append(tabumove)
                iterationwiseBestDistance.append(minimum)
                costOfBestRouteList=minimum
                costOfCurrRouteList=minimum
                tabumoves.append(tabumove)

            
            elif minimum > costOfBestRouteList:
                #checking if minimum value is in tabu list
                if tabumove in tabulist:
                    #if minimum in tabu list then selecting next top 10 moves if any move is not in tabu list making that as a current route
                    uniquedistances=list(set(swaproutesdistances))
                    uniquedistances.sort()
                    uniquedistances=uniquedistances[1:11]
                    distances=[]
                    indexes=[]
                    sortedmoves=[]
                
                    for i in uniquedistances:
                        index=swaproutesdistances.index(i)
                        move=swaproutesindex[index]
                        if move not in tabulist:
                            distances.append(i)
                            indexes.append(index)
                            sortedmoves.append(move)

                    minimumdistanceaftersorting=min(distances)
                    indexofsorteddistance=distances.index(minimumdistanceaftersorting)
                    sortedmove=sortedmoves[indexofsorteddistance]

                    currentRoute[sortedmove[0]],currentRoute[sortedmove[1]]=currentRoute[sortedmove[1]],currentRoute[sortedmove[0]]
                    
                    iterationwiseBestDistance.append(minimumdistanceaftersorting)
                    costOfCurrRouteList=minimumdistanceaftersorting
                    tabumoves.append(sortedmove)        
                
                elif tabumove not in tabulist:
                    currentRoute[tabumove[0]],currentRoute[tabumove[1]]=currentRoute[tabumove[1]],currentRoute[tabumove[0]]

                    for i in range(3):
                        tabulist.append(tabumove)

                    iterationwiseBestDistance.append(minimum)
                    costOfCurrRouteList=minimum
                    tabumoves.append(tabumove)

            elif (minimum == costOfBestRouteList) :
                uniquedistances=list(set(swaproutesdistances))
                uniquedistances.sort()
                uniquedistances=uniquedistances[1:11]
                distances=[]
                indexes=[]
                sortedmoves=[]
                for i in uniquedistances:
                    index=swaproutesdistances.index(i)
                    move=swaproutesindex[index]
                    if move not in tabulist:
                        distances.append(i)
                        indexes.append(index)
                        sortedmoves.append(move)

                
                
                minimumdistanceaftersorting=min(distances)
                indexofsorteddistance=distances.index(minimumdistanceaftersorting)
                sortedmove=sortedmoves[indexofsorteddistance]

                currentRoute[sortedmove[0]],currentRoute[sortedmove[1]]=currentRoute[sortedmove[1]],currentRoute[sortedmove[0]]
                
                for i in range(3):
                    tabulist.append(sortedmove)

                
                        
                iterationwiseBestDistance.append(minimumdistanceaftersorting)
                costOfCurrRouteList=minimumdistanceaftersorting
                tabumoves.append(sortedmove)

            
            swaproutesdistances.clear()
            swaproutesindex.clear()
            noofiterations = noofiterations +1
        
        #checking performance of the algorithm    
        endTime=datetime.now()
        computationTime=(endTime-startTime).total_seconds()

        #returns Best Route  
        finalRoute={   
            "path":bestRoute,
            "totalDistance":costOfBestRouteList,
            "timeTaken":computationTime
        }

        return finalRoute