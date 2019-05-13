import numpy as np
from math import sin, cos, sqrt, atan2, radians
import random

class Util:

    def cTocDistance(self,data):#calculating distancematrix
        l=[]
        for i in data:
            for j in data:
                l.append(np.sqrt((j['lat']-i['lat'])**2+(j['lng']-i['lng'])**2))
        distance=[]
        for i in range(len(data)):
            a=l[:len(data)]
            distance.append(a) 
            del l[:len(data)]

        return distance

    def calculateDistanceForRoute(self,route):#calculating totalDistance of route
        totalDistance=0
        radiusOfEarth=6373.0
        for i in range(len(route)-1):
            c1=route[i]
            c2=route[i+1]
            lat1=radians(c1["lat"])
            lon1=radians(c1["lng"])
            lat2=radians(c2["lat"])
            lon2=radians(c2["lng"])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = radiusOfEarth * c
            totalDistance = totalDistance + distance

        return totalDistance

    def swapRoute(self,route):
        i=random.randint(1,(len(route)-2))
        j=random.randint(1,(len(route)-2))
        a=[]
        if i == j:
            return Util().swapRoute(route)
        if [i,j] not in a:
            a.clear()
            route[i],route[j]=route[j],route[i]
            a.append([i,j])
        else:
            return Util().swapRoute(route)
        return route

    def distance2d(self,route):
        totalDistance=0
        for i in range(len(route)-1):
            c1=route[i]
            c2=route[i+1]
            distance=np.sqrt((c2["lat"]-c1["lat"]) + (c2["lng"]-c1["lng"]))
            totalDistance=totalDistance+distance
            return totalDistance

    def second_smallest(self,numbers):
        m1, m2 = float('inf'), float('inf')
        for x in numbers:
            if x <= m1:
                m1, m2 = x, m1
            elif x < m2:
                m2 = x
        return m2



    
    
    
