# -*- coding: utf-8 -*-
"""Thesis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UGrf6uIGiQlXXxtBAGb1flbYkvrbdtK3
"""

import itertools
frame_rate=2
def distance(point1, point2):
    return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2) ** 0.5



def classify_beams(b1, b2):
    combo=list(itertools.permutations(range(len(b1)), 3))
    combo2=list(itertools.permutations(range(len(b2)), 3))
    boats = []
    check=[]
    for i, j, k in combo:
      for l,m,n in combo2:
        if all([i not in check for i in [b2[l],b2[m], b2[n],b1[i],b1[j], b1[k]]]):
          x=distance(b1[i].point, b2[l].point)
          y=distance(b1[j].point, b2[m].point)
          z=distance(b1[k].point, b2[n].point)
          if x==y==z:
            boats+=[[(b2[l],b2[m],b2[n]), x * frame_rate]]
            check+=[b2[l],b2[m],b2[n],b1[i],b1[j], b1[k]]
            print(b2[l].point,b2[m].point, b2[n].point,b1[i].point,b1[j].point, b1[k].point)
    for i in b2:
      if i not in check:
        print(i.point)
        boats+=[[i, None]]
    return boats
class beam:
  def __init__(self, a):
    self.point=a

b1= [beam((x,y)) for x,y in [(2,3),(4,6),(3,9),(2,3),(2,4),(6,8)]]
b2= [beam((x,y)) for x,y in [(0,1),(4,6),(0,2),(5,9),(3,5),(1,2),(2,8),(3,9),(8,8)]]
boats= classify_beams(b1, b2)

import math as m
import time as t
import itertools

#-----------------------------------------------------------------------------------------------------------------------
#Global variables

global k

Horizontal_resolution=1
Actual_beam_diameter=1
HFOV= m.radians(30) ## angular fieald of view
k = Horizontal_resolution*Actual_beam_diameter/(2*m.tan(HFOV))
frame_rate=2

#-----------------------------------------------------------------------------------------------------------------------

class Ship:

    def __init__(self, beam):
        self.area = 0
        self.lasers = beam
        self.type = None
        self.abs_speed=None
        self.app_speed=None
        self.findFacerVesselSize(beam)


    def findFacerVesselSize (self, oneFacerLasers):
        #assuming it is a list of objects, given in the parameter
        width = 0
        length = 0
        height = 0
        for eachLaser in oneFacerLasers:
            for alternativeLaser in oneFacerLasers:
                if eachLaser != alternativeLaser:
                    temp_angle = abs(eachLaser.angle - alternativeLaser.angle)
                    l1Distance = eachLaser.distance
                    l2Distance = alternativeLaser.distance

                    temp = ((l1Distance**2) + (l2Distance**2) - (2*l1Distance*l2Distance*m.cos(m.radians(temp_angle))))**(1/2)

                    if width == 0:
                        width = temp
                    else:
                        if temp > width:
                            length = temp
                        else:
                            length = width
                            width = temp
            break
        height = ((length**2) - ((width/2)**2))**(1/2)
        self.area = round(height * width)
        for key in shipDictionary.keys():
            if shipDictionary[key] == self.area:
                self.type = key
                break
        return round(self.area,2)

#------------------------------------------------------------------------------------------------------------------

class LaserBeam:

    def __init__(self,angle,apparent_width):
        self.angle = angle
        self.distance= apparent_width
        self.point=(round(self.distance*m.sin(m.radians(angle)),2), round(self.distance*m.cos(m.radians(angle)),2))

#--------------------------------------------------------------------------------------------------------------------------

def distance(point1, point2):
  return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2) ** 0.5

def distance_single_point(point1, point2):
    return ((point1)**2 + (point2)**2) ** 0.5


def classify_beams(b1, b2):
    combo=list(itertools.permutations(range(len(b1)), 3))
    combo2=list(itertools.permutations(range(len(b2)), 3))
    boats = []
    check=[]
    for i, j, k in combo:
      for l,m,n in combo2:
        if all([i not in check for i in [b2[l],b2[m], b2[n],b1[i],b1[j], b1[k]]]):
          x=distance(b1[i].point, b2[l].point)
          y=distance(b1[j].point, b2[m].point)
          z=distance(b1[k].point, b2[n].point)
          if abs(x-y)<=1 and abs(z-y)<=1 and abs(x-z)<=1:
            boats+=[[(b2[l],b2[m],b2[n]), (b1[i].point[0]- b2[l].point[0], b1[i].point[1]- b2[l].point[1])]]
            check+=[b2[l],b2[m],b2[n],b1[i],b1[j], b1[k]]
    for i in b2:
      if i not in check:
        boats+=[[[i], None]]
    return boats


def findVelocityOfFacerVessel(beam, v):
    hor= v[0]- host_h_speed
    ver = v[1] - host_v_speed
    return round(distance_single_point(hor, ver)*frame_rate, 2)


def laserSuccessorChecker(givenLasers, predecessorLasers):
    pass
    '''
    #since frame rate is medium and hence time interval between each frame is small and hence the angle change would not be significant
    for beam in givenLasers:
        beamDifferenceWithAll = []
        for i in range(len(predecessorLasers)):
            beamDifferenceWithAll.append(abs(beam.angle - predecessorLasers[i].angle))
        minDifference = min(beamDifferenceWithAll)
        minDifferenceIndex = beamDifferenceWithAll.index(minDifference)
        beam.predecessor = predecessorLasers[minDifferenceIndex]
        beam.ship = predecessorLasers[minDifferenceIndex].ship
        predecessorLasers[minDifferenceIndex].ship.lasers.append(beam)
    '''


#k yet to be initialised

currentLasers = []
mainCounter = 0
newLasers = []

shipDictionary = {"Waterbus" : 246} #there will be more
safeDistance = {"Waterbus" : 1}

xtra_beams = []
ships = []
captureImage = True

vesselCount = len(ships)
laserCounter = len(newLasers)
shipCounter = 0

host_h_speed=8
host_v_speed=6
x=1
for i in dummy:

    datafromImageProcessing = i #input() from image processing algorithm
    apparentWidthList = [i[1] for i in datafromImageProcessing]
    angleList = [i[0] for i in datafromImageProcessing]
    for j in range(len(i)):
        name = "laser{}".format(laserCounter)
        laserCounter += 1
        newLasers += [LaserBeam(angleList[j], apparentWidthList[j])]
    if mainCounter == 0:
        mainCounter = 1
        #findFacerVesselNumbers() for classification where a list of tuples is returned
        #from here each tuple will be used to make a ship object
        #for group in returnedList:
        '''
        name = "ship{}".format(shipCounter)
        shipCounter += 1
        ships[name] = Ship()
        ships[name].append

        '''
        currentLasers=newLasers.copy()
        t.sleep(1)
    else:
        boats= classify_beams(currentLasers, newLasers)
        w=1
        boat = f"Boat {w}"
        print("Image",x)
        for i in boats:
          boat = f"Boat {w}"
          if len(i[0])<3:
            xtra_beams.append(i[0][0])
          else:
            ship= Ship(i[0])
            ship.app_speed = round(distance_single_point(i[1][0], i[1][1])*frame_rate,2)
            ship.abs_speed = findVelocityOfFacerVessel(i[0][0], i[1])
            ships.append(ship)

            print(boat)
            print("Expected Absolute speed: 28.28 ","Calculated Absolute Speed:", ship.abs_speed, "\nExpected Apparent Speed: 8.94", "Calculated Apparent Speed:", ship.app_speed)
            w+=1

        ## use ship objects from ships list for simulation
        ##SIMULATION  CODE call
    t.sleep(1)
    ships=[]
    x+=1
    currentLasers=newLasers.copy()
    newLasers=[]
    xtra_beams=[]

    captureImage = False

##Generate Dummy data

import math as m

def distance(point1, point2):
    return ((point1)**2 + (point2)**2) ** 0.5

def dummy(args):

  for j in range(3):
    l=[]
    for k in args:
      points=k[0]
      dx= k[1]
      dy=k[2]
      wx=k[3]
      wy=k[4]
      for i in range(3):
          b=points[i]
          x=b[0]+j*(dx-wx)
          y=b[1]+j*(dy-wy)
          d= distance(x,y)
          angle= m.atan(abs(y/x))*180/m.pi
          if x >= 0:
            if y>=0:
              angle=90-angle
            else:
              angle=90+angle
          else:
            if y>=0:
              angle=270+angle
            else:
              angle=270-angle


          l+=[(round(angle, 1), round(d, 1))]
    print(l)
print("Dummy data")
dummy([([(20,30),(10, 50),(30, 50)], -4 , 8, 12, 9),([(-5, 50),(-15, 55),(-15, 45)], -4 , 8, 12, 9), ([(60, -100),(80, -150),(90, -125)], -4 , 8, 12, 9)])

## Classification Test



dummy= [[(33.7, 36.1), (11.3, 51.0), (31.0, 58.3)],
[(31.2, 38.6), (10.7, 53.9), (29.5, 60.9)],
[(29.1, 41.2), (10.1, 56.9), (28.2, 63.5),(354.3, 50.2)],
[(27.1, 43.8), (9.6, 59.8), (27.0, 66.2), (354.3, 50.2), (344.7, 57.0), (341.6, 47.4)],
[(25.5, 46.5), (9.2, 62.8), (25.8, 68.9), (354.6, 53.2), (345.5, 59.9), (342.6, 50.3)],
[(354.9, 56.2), (346.2, 62.8), (343.6, 53.2)],
[(355.2, 59.2), (346.8, 65.7), (344.5, 56.0), (149.0, 116.6), (151.9, 170.0), (144.2, 154.0)],
[(355.4, 62.2), (347.4, 68.7), (345.3, 58.9), (148.3, 114.1), (151.4, 167.4), (143.6, 151.6)],
[(147.4, 111.5), (150.9, 164.7), (142.9, 149.2)],
[(146.6, 109.0), (150.4, 162.1), (142.2, 146.8)],
[(145.7, 106.5), (149.9, 159.5), (141.5, 144.5)]]
import math as m
import time as t
import itertools

#-----------------------------------------------------------------------------------------------------------------------
#Global variables

global k

Horizontal_resolution=1
Actual_beam_diameter=1
HFOV= m.radians(30) ## angular fieald of view
k = Horizontal_resolution*Actual_beam_diameter/(2*m.tan(HFOV))
frame_rate=2

#-----------------------------------------------------------------------------------------------------------------------

class Ship:

    def __init__(self, beam):
        self.area = 0
        self.lasers = beam
        self.type = None
        self.abs_speed=None
        self.app_speed=None
        self.findFacerVesselSize(beam)


    def findFacerVesselSize (self, oneFacerLasers):
        #assuming it is a list of objects, given in the parameter
        width = 0
        length = 0
        height = 0
        for eachLaser in oneFacerLasers:
            for alternativeLaser in oneFacerLasers:
                if eachLaser != alternativeLaser:
                    temp_angle = abs(eachLaser.angle - alternativeLaser.angle)
                    l1Distance = eachLaser.distance
                    l2Distance = alternativeLaser.distance

                    temp = ((l1Distance**2) + (l2Distance**2) - (2*l1Distance*l2Distance*m.cos(m.radians(temp_angle))))**(1/2)
                    if width == 0:
                        width = temp
                    else:
                        if temp > width:
                            length = temp
                        else:
                            length = width
                            width = temp
            break
        height = ((length**2) - ((width/2)**2))**(1/2)
        self.area = round(height * width)
        for key in shipDictionary.keys():
            if shipDictionary[key] == self.area:
                self.type = key
                break
        return round(self.area,2)

#------------------------------------------------------------------------------------------------------------------

class LaserBeam:

    def __init__(self,angle,apparent_width):
        self.angle = angle
        self.distance= apparent_width
        self.point=(round(self.distance*m.sin(m.radians(angle)),2), round(self.distance*m.cos(m.radians(angle)),2))

#--------------------------------------------------------------------------------------------------------------------------

def distance(point1, point2):
  return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2) ** 0.5

def distance_single_point(point1, point2):
    return ((point1)**2 + (point2)**2) ** 0.5


def classify_beams(b1, b2):
    combo=list(itertools.permutations(range(len(b1)), 3))
    combo2=list(itertools.permutations(range(len(b2)), 3))
    boats = []
    check=[]
    for i, j, k in combo:
      for l,m,n in combo2:
        if all([i not in check for i in [b2[l],b2[m], b2[n],b1[i],b1[j], b1[k]]]):
          x=distance(b1[i].point, b2[l].point)
          y=distance(b1[j].point, b2[m].point)
          z=distance(b1[k].point, b2[n].point)
          if abs(x-y)<=1 and abs(z-y)<=1 and abs(x-z)<=1:
            boats+=[[(b2[l],b2[m],b2[n]), (b1[i].point[0]- b2[l].point[0], b1[i].point[1]- b2[l].point[1])]]
            check+=[b2[l],b2[m],b2[n],b1[i],b1[j], b1[k]]
            print("Added",(b2[l].angle, b2[l].distance),(b2[m].angle, b2[m].distance),(b2[n].angle, b2[n].distance))
    for i in b2:
      if i not in check:
        print("Not Added", (i.angle, i.distance))
        boats+=[[[i], None]]
    return boats


def findVelocityOfFacerVessel(beam, v):
    hor= v[0]- host_h_speed
    ver = v[1] - host_v_speed
    return round(distance_single_point(hor, ver)*frame_rate, 2)


def laserSuccessorChecker(givenLasers, predecessorLasers):
    pass
    '''
    #since frame rate is medium and hence time interval between each frame is small and hence the angle change would not be significant
    for beam in givenLasers:
        beamDifferenceWithAll = []
        for i in range(len(predecessorLasers)):
            beamDifferenceWithAll.append(abs(beam.angle - predecessorLasers[i].angle))
        minDifference = min(beamDifferenceWithAll)
        minDifferenceIndex = beamDifferenceWithAll.index(minDifference)
        beam.predecessor = predecessorLasers[minDifferenceIndex]
        beam.ship = predecessorLasers[minDifferenceIndex].ship
        predecessorLasers[minDifferenceIndex].ship.lasers.append(beam)
    '''


#k yet to be initialised

currentLasers = []
mainCounter = 0
newLasers = []

shipDictionary = {"Waterbus" : 246} #there will be more
safeDistance = {"Waterbus" : 1}

xtra_beams = []
ships = []
captureImage = True

vesselCount = len(ships)
laserCounter = len(newLasers)
shipCounter = 0

host_h_speed=8
host_v_speed=6
x=1
for i in dummy:
    print("Image",x)
    datafromImageProcessing = i #input() from image processing algorithm
    apparentWidthList = [i[1] for i in datafromImageProcessing]
    angleList = [i[0] for i in datafromImageProcessing]
    for j in range(len(i)):
        name = "laser{}".format(laserCounter)
        laserCounter += 1
        newLasers += [LaserBeam(angleList[j], apparentWidthList[j])]
    if mainCounter == 0:
        mainCounter = 1
        #findFacerVesselNumbers() for classification where a list of tuples is returned
        #from here each tuple will be used to make a ship object
        #for group in returnedList:
        '''
        name = "ship{}".format(shipCounter)
        shipCounter += 1
        ships[name] = Ship()
        ships[name].append

        '''
        currentLasers=newLasers.copy()
        t.sleep(1)
    else:
        print("Previous beams:",[(beam.angle, beam.distance) for beam in currentLasers])
        print("New beams:",[(beam.angle, beam.distance) for beam in newLasers])
        boats= classify_beams(currentLasers, newLasers)

        for i in boats:

          if len(i[0])<3:
            xtra_beams.append(i[0][0])
            print("Unidentified beam: ", (i[0][0].angle,i[0][0].distance), end=" ")
            print()
          else:
            ship= Ship(i[0])
            ship.app_speed = round(distance_single_point(i[1][0], i[1][1])*frame_rate,2)
            ship.abs_speed = findVelocityOfFacerVessel(i[0][0], i[1])
            ships.append(ship)

            print("Area: ",ship.area,"Beam", [(beam.angle, beam.distance) for beam in ship.lasers])

        ## use ship objects from ships list for simulation
        ##SIMULATION  CODE call
    t.sleep(1)
    ships=[]
    currentLasers=newLasers.copy()
    newLasers=[]
    xtra_beams=[]
    x+=1
    captureImage = False

## Speed Test 1



dummy= [[(33.7, 36.1), (11.3, 51.0), (31.0, 58.3),(354.3, 50.2), (344.7, 57.0), (341.6, 47.4),(149.0, 116.6), (151.9, 170.0), (144.2, 154.0)],
[(32.9, 40.5), (12.5, 55.3), (30.7, 62.8), (356.8, 54.1), (347.6, 60.4), (345.1, 50.7), (147.1, 114.3), (150.7, 167.5), (142.8, 152.0)],
[(32.3, 44.9), (13.6, 59.7), (30.4, 67.2),(359.0, 58.0), (350.1, 64.0), (348.3, 54.1), (145.2, 112.1), (149.4, 165.0), (141.2, 150.1)],
[(31.8, 49.4), (14.5, 64.0), (30.1, 71.7), (0.9, 62.0), (352.3, 67.6), (351.0, 57.7), (143.1, 110.0), (148.1, 162.6), (139.7, 148.3)],
[(31.3, 53.9), (15.3, 68.4), (29.9, 76.2), (2.6, 66.1), (354.4, 71.3), (353.5, 61.4), (141.0, 108.1), (146.7, 160.3), (138.0, 146.6)]]

import math as m
import time as t
import itertools

#-----------------------------------------------------------------------------------------------------------------------
#Global variables

global k

Horizontal_resolution=1
Actual_beam_diameter=1
HFOV= m.radians(30) ## angular fieald of view
k = Horizontal_resolution*Actual_beam_diameter/(2*m.tan(HFOV))
frame_rate=2

#-----------------------------------------------------------------------------------------------------------------------

class Ship:

    def __init__(self, beam):
        self.area = 0
        self.lasers = beam
        self.type = None
        self.abs_speed=None
        self.app_speed=None
        self.findFacerVesselSize(beam)


    def findFacerVesselSize (self, oneFacerLasers):
        #assuming it is a list of objects, given in the parameter
        width = 0
        length = 0
        height = 0
        for eachLaser in oneFacerLasers:
            for alternativeLaser in oneFacerLasers:
                if eachLaser != alternativeLaser:
                    temp_angle = abs(eachLaser.angle - alternativeLaser.angle)
                    l1Distance = eachLaser.distance
                    l2Distance = alternativeLaser.distance

                    temp = ((l1Distance**2) + (l2Distance**2) - (2*l1Distance*l2Distance*m.cos(m.radians(temp_angle))))**(1/2)

                    if width == 0:
                        width = temp
                    else:
                        if temp > width:
                            length = temp
                        else:
                            length = width
                            width = temp
            break
        height = ((length**2) - ((width/2)**2))**(1/2)
        self.area = round(height * width)
        for key in shipDictionary.keys():
            if shipDictionary[key] == self.area:
                self.type = key
                break
        return round(self.area,2)

#------------------------------------------------------------------------------------------------------------------

class LaserBeam:

    def __init__(self,angle,apparent_width):
        self.angle = angle
        self.distance= apparent_width
        self.point=(round(self.distance*m.sin(m.radians(angle)),2), round(self.distance*m.cos(m.radians(angle)),2))

#--------------------------------------------------------------------------------------------------------------------------

def distance(point1, point2):
  return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2) ** 0.5

def distance_single_point(point1, point2):
    return ((point1)**2 + (point2)**2) ** 0.5


def classify_beams(b1, b2):
    combo=list(itertools.permutations(range(len(b1)), 3))
    combo2=list(itertools.permutations(range(len(b2)), 3))
    boats = []
    check=[]
    for i, j, k in combo:
      for l,m,n in combo2:
        if all([i not in check for i in [b2[l],b2[m], b2[n],b1[i],b1[j], b1[k]]]):
          x=distance(b1[i].point, b2[l].point)
          y=distance(b1[j].point, b2[m].point)
          z=distance(b1[k].point, b2[n].point)
          if abs(x-y)<=1 and abs(z-y)<=1 and abs(x-z)<=1:
            boats+=[[(b2[l],b2[m],b2[n]), (b1[i].point[0]- b2[l].point[0], b1[i].point[1]- b2[l].point[1])]]
            check+=[b2[l],b2[m],b2[n],b1[i],b1[j], b1[k]]
    for i in b2:
      if i not in check:
        boats+=[[[i], None]]
    return boats


def findVelocityOfFacerVessel(beam, v):
    hor= v[0]- host_h_speed
    ver = v[1] - host_v_speed
    return round(distance_single_point(hor, ver)*frame_rate, 2)


def laserSuccessorChecker(givenLasers, predecessorLasers):
    pass
    '''
    #since frame rate is medium and hence time interval between each frame is small and hence the angle change would not be significant
    for beam in givenLasers:
        beamDifferenceWithAll = []
        for i in range(len(predecessorLasers)):
            beamDifferenceWithAll.append(abs(beam.angle - predecessorLasers[i].angle))
        minDifference = min(beamDifferenceWithAll)
        minDifferenceIndex = beamDifferenceWithAll.index(minDifference)
        beam.predecessor = predecessorLasers[minDifferenceIndex]
        beam.ship = predecessorLasers[minDifferenceIndex].ship
        predecessorLasers[minDifferenceIndex].ship.lasers.append(beam)
    '''


#k yet to be initialised

currentLasers = []
mainCounter = 0
newLasers = []

shipDictionary = {"Waterbus" : 246} #there will be more
safeDistance = {"Waterbus" : 1}

xtra_beams = []
ships = []
captureImage = True

vesselCount = len(ships)
laserCounter = len(newLasers)
shipCounter = 0

host_h_speed=8
host_v_speed=6
x=1
for i in dummy:

    datafromImageProcessing = i #input() from image processing algorithm
    apparentWidthList = [i[1] for i in datafromImageProcessing]
    angleList = [i[0] for i in datafromImageProcessing]
    for j in range(len(i)):
        name = "laser{}".format(laserCounter)
        laserCounter += 1
        newLasers += [LaserBeam(angleList[j], apparentWidthList[j])]
    if mainCounter == 0:
        mainCounter = 1
        #findFacerVesselNumbers() for classification where a list of tuples is returned
        #from here each tuple will be used to make a ship object
        #for group in returnedList:
        '''
        name = "ship{}".format(shipCounter)
        shipCounter += 1
        ships[name] = Ship()
        ships[name].append

        '''
        currentLasers=newLasers.copy()
        t.sleep(1)
    else:
        boats= classify_beams(currentLasers, newLasers)
        w=1
        boat = f"Boat {w}"
        print("Image",x)
        for i in boats:
          boat = f"Boat {w}"
          if len(i[0])<3:
            xtra_beams.append(i[0][0])
          else:
            ship= Ship(i[0])
            ship.app_speed = round(distance_single_point(i[1][0], i[1][1])*frame_rate,2)
            ship.abs_speed = findVelocityOfFacerVessel(i[0][0], i[1])
            ships.append(ship)

            print(boat)
            print("Expected Absolute speed: 28.28 ","Calculated Absolute Speed:", ship.abs_speed, "\nExpected Apparent Speed: 8.94", "Calculated Apparent Speed:", ship.app_speed)
            w+=1

        ## use ship objects from ships list for simulation
        ##SIMULATION  CODE call
    t.sleep(1)
    ships=[]
    x+=1
    currentLasers=newLasers.copy()
    newLasers=[]
    xtra_beams=[]

    captureImage = False

## Speed Test 2



dummy= [[(33.7, 36.1), (11.3, 51.0), (31.0, 58.3), (354.3, 50.2), (344.7, 57.0), (341.6, 47.4), (149.0, 116.6), (151.9, 170.0), (144.2, 154.0)],
[(7.9, 29.3), (353.0, 49.4), (15.9, 51.0), (336.8, 53.3), (330.1, 62.3), (324.8, 53.8), (156.5, 110.2), (157.0, 164.0), (149.6, 146.1)],
[(336.8, 30.5), (335.4, 52.8), (357.6, 48.0), (322.4, 60.6), (318.4, 70.8), (312.5, 63.7), (164.6, 105.8), (162.5, 159.4), (155.5, 139.6)]]

import math as m
import time as t
import itertools

#-----------------------------------------------------------------------------------------------------------------------
#Global variables

global k

Horizontal_resolution=1
Actual_beam_diameter=1
HFOV= m.radians(30) ## angular fieald of view
k = Horizontal_resolution*Actual_beam_diameter/(2*m.tan(HFOV))
frame_rate=2

#-----------------------------------------------------------------------------------------------------------------------

class Ship:

    def __init__(self, beam):
        self.area = 0
        self.lasers = beam
        self.type = None
        self.abs_speed=None
        self.app_speed=None
        self.findFacerVesselSize(beam)


    def findFacerVesselSize (self, oneFacerLasers):
        #assuming it is a list of objects, given in the parameter
        width = 0
        length = 0
        height = 0
        for eachLaser in oneFacerLasers:
            for alternativeLaser in oneFacerLasers:
                if eachLaser != alternativeLaser:
                    temp_angle = abs(eachLaser.angle - alternativeLaser.angle)
                    l1Distance = eachLaser.distance
                    l2Distance = alternativeLaser.distance

                    temp = ((l1Distance**2) + (l2Distance**2) - (2*l1Distance*l2Distance*m.cos(m.radians(temp_angle))))**(1/2)

                    if width == 0:
                        width = temp
                    else:
                        if temp > width:
                            length = temp
                        else:
                            length = width
                            width = temp
            break
        height = ((length**2) - ((width/2)**2))**(1/2)
        self.area = round(height * width)
        for key in shipDictionary.keys():
            if shipDictionary[key] == self.area:
                self.type = key
                break
        return round(self.area,2)

#------------------------------------------------------------------------------------------------------------------

class LaserBeam:

    def __init__(self,angle,apparent_width):
        self.angle = angle
        self.distance= apparent_width
        self.point=(round(self.distance*m.sin(m.radians(angle)),2), round(self.distance*m.cos(m.radians(angle)),2))

#--------------------------------------------------------------------------------------------------------------------------

def distance(point1, point2):
  return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2) ** 0.5

def distance_single_point(point1, point2):
    return ((point1)**2 + (point2)**2) ** 0.5


def classify_beams(b1, b2):
    combo=list(itertools.permutations(range(len(b1)), 3))
    combo2=list(itertools.permutations(range(len(b2)), 3))
    boats = []
    check=[]
    for i, j, k in combo:
      for l,m,n in combo2:
        if all([i not in check for i in [b2[l],b2[m], b2[n],b1[i],b1[j], b1[k]]]):
          x=distance(b1[i].point, b2[l].point)
          y=distance(b1[j].point, b2[m].point)
          z=distance(b1[k].point, b2[n].point)
          if abs(x-y)<=1 and abs(z-y)<=1 and abs(x-z)<=1:
            boats+=[[(b2[l],b2[m],b2[n]), (b1[i].point[0]- b2[l].point[0], b1[i].point[1]- b2[l].point[1])]]
            check+=[b2[l],b2[m],b2[n],b1[i],b1[j], b1[k]]
    for i in b2:
      if i not in check:
        boats+=[[[i], None]]
    return boats


def findVelocityOfFacerVessel(beam, v):
    hor= v[0]- host_h_speed
    ver = v[1] - host_v_speed
    return round(distance_single_point(hor, ver)*frame_rate, 2)


def laserSuccessorChecker(givenLasers, predecessorLasers):
    pass
    '''
    #since frame rate is medium and hence time interval between each frame is small and hence the angle change would not be significant
    for beam in givenLasers:
        beamDifferenceWithAll = []
        for i in range(len(predecessorLasers)):
            beamDifferenceWithAll.append(abs(beam.angle - predecessorLasers[i].angle))
        minDifference = min(beamDifferenceWithAll)
        minDifferenceIndex = beamDifferenceWithAll.index(minDifference)
        beam.predecessor = predecessorLasers[minDifferenceIndex]
        beam.ship = predecessorLasers[minDifferenceIndex].ship
        predecessorLasers[minDifferenceIndex].ship.lasers.append(beam)
    '''


#k yet to be initialised

currentLasers = []
mainCounter = 0
newLasers = []

shipDictionary = {"Waterbus" : 246} #there will be more
safeDistance = {"Waterbus" : 1}

xtra_beams = []
ships = []
captureImage = True

vesselCount = len(ships)
laserCounter = len(newLasers)
shipCounter = 0

host_h_speed=8
host_v_speed=6
x=1
for i in dummy:

    datafromImageProcessing = i #input() from image processing algorithm
    apparentWidthList = [i[1] for i in datafromImageProcessing]
    angleList = [i[0] for i in datafromImageProcessing]
    for j in range(len(i)):
        name = "laser{}".format(laserCounter)
        laserCounter += 1
        newLasers += [LaserBeam(angleList[j], apparentWidthList[j])]
    if mainCounter == 0:
        mainCounter = 1
        #findFacerVesselNumbers() for classification where a list of tuples is returned
        #from here each tuple will be used to make a ship object
        #for group in returnedList:
        '''
        name = "ship{}".format(shipCounter)
        shipCounter += 1
        ships[name] = Ship()
        ships[name].append

        '''
        currentLasers=newLasers.copy()
        t.sleep(1)
    else:
        boats= classify_beams(currentLasers, newLasers)
        w=1
        boat = f"Boat {w}"
        print("Image",x)
        for i in boats:
          boat = f"Boat {w}"
          if len(i[0])<3:
            xtra_beams.append(i[0][0])
          else:
            ship= Ship(i[0])
            ship.app_speed = round(distance_single_point(i[1][0], i[1][1])*frame_rate,2)
            ship.abs_speed = findVelocityOfFacerVessel(i[0][0], i[1])
            ships.append(ship)

            print(boat)
            print("Expected Absolute speed: 17.89 ","Calculated Absolute Speed:", ship.abs_speed, "\nExpected Apparent Speed: 32.06", "Calculated Apparent Speed:", ship.app_speed)
            w+=1

        ## use ship objects from ships list for simulation
        ##SIMULATION  CODE call
    t.sleep(1)
    ships=[]
    x+=1
    currentLasers=newLasers.copy()
    newLasers=[]
    xtra_beams=[]

    captureImage = False

import matplotlib.pyplot as plt

# Data for the first set
data1 = [
    [(33.7, 36.1), (11.3, 51.0), (31.0, 58.3), (354.3, 50.2), (344.7, 57.0), (341.6, 47.4), (149.0, 116.6), (151.9, 170.0), (144.2, 154.0)],
    [(7.9, 29.3), (353.0, 49.4), (15.9, 51.0), (336.8, 53.3), (330.1, 62.3), (324.8, 53.8), (156.5, 110.2), (157.0, 164.0), (149.6, 146.1)],
    [(336.8, 30.5), (335.4, 52.8), (357.6, 48.0), (322.4, 60.6), (318.4, 70.8), (312.5, 63.7), (164.6, 105.8), (162.5, 159.4), (155.5, 139.6)]
]

# Data for the second set
data2 = [
    [(33.7, 36.1), (11.3, 51.0), (31.0, 58.3), (354.3, 50.2), (344.7, 57.0), (341.6, 47.4), (149.0, 116.6), (151.9, 170.0), (144.2, 154.0)],
    [(32.9, 40.5), (12.5, 55.3), (30.7, 62.8), (356.8, 54.1), (347.6, 60.4), (345.1, 50.7), (147.1, 114.3), (150.7, 167.5), (142.8, 152.0)],
    [(32.3, 44.9), (13.6, 59.7), (30.4, 67.2), (359.0, 58.0), (350.1, 64.0), (348.3, 54.1), (145.2, 112.1), (149.4, 165.0), (141.2, 150.1)],
    [(31.8, 49.4), (14.5, 64.0), (30.1, 71.7), (0.9, 62.0), (352.3, 67.6), (351.0, 57.7), (143.1, 110.0), (148.1, 162.6), (139.7, 148.3)],
    [(31.3, 53.9), (15.3, 68.4), (29.9, 76.2), (2.6, 66.1), (354.4, 71.3), (353.5, 61.4), (141.0, 108.1), (146.7, 160.3), (138.0, 146.6)]
]

# Extract x and y values for both sets
x1 = [point[0] for sublist in data1 for point in sublist]
y1 = [point[1] for sublist in data1 for point in sublist]

x2 = [point[0] for sublist in data2 for point in sublist]
y2 = [point[1] for sublist in data2 for point in sublist]

# Create the scatter plots
plt.figure(figsize=(10, 5))
plt.scatter(x1, y1, label='Set 1', marker='x', color='darkslateblue', alpha=0.7)
plt.scatter(x2, y2, label='Set 2', marker='o', color='red', alpha=0.7)

# Add labels and legend
plt.xlabel('Angle')
plt.ylabel('Distance')
plt.title('Scatter Plot of 2 Dummy Data sets')
plt.legend()

# Show the plot
plt.grid(True)
plt.show()

import matplotlib.pyplot as plt


categories = ['I2B1', 'I2B2', 'I2B3', 'I3B1','I3B2', 'I3B3', 'I4B1', 'I4B2','I4B3', 'I5B1', 'I5B2', 'I5B3']
values = [28.2, 28.34, 28.3, 28.2, 28.26, 28.03, 28.38, 28.26, 28.5, 28.36, 28.38, 28.2]
values_d2 = [18.86,18.93, 18.94, 18.96, 18.84, 18.66]

# Create a bar chart
plt.figure(figsize=(8, 6))

plt.bar(categories, values, color='darkorange')
#plt.line(categories, values_d2, color='blue')

plt.axhline(y=28.28, color='black', linestyle='--', label='Y = 28.28')
plt.text(1.75, 28.3, 'Expected Absolute Speed = 28.28', color='black', fontsize=12)
# plt.axhline(y=17.89, color='pink', linestyle='--', label='Y = 17.89')
# plt.text(1.75, 17.90, 'Expected Absolute Speed = 17.89', color='red', fontsize=10)

plt.ylim(28, 28.6)
# Add labels and title
plt.xlabel('Image & Boat No.')
plt.ylabel('Absolute Speed')
plt.title('Speed test 1 (Absolute Speed)')

# Show the plot
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()  # Ensures labels fit within the figure area
plt.show()

import matplotlib.pyplot as plt


categories = ['I2B1', 'I2B2', 'I2B3', 'I3B1','I3B2', 'I3B3']
#values = [28.2, 28.34, 28.3, 28.2, 28.26, 28.03, 28.38, 28.26, 28.5, 28.36, 28.38, 28.2]
values_d2 = [18.86,18.93, 18.94, 18.96, 18.84, 18.66]

# Create a bar chart
plt.figure(figsize=(7, 6))

#plt.bar(categories, values, color='lightblue')
plt.bar(categories, values_d2, color='darkorange', width = 0.4)

#plt.axhline(y=28.28, color='red', linestyle='--', label='Y = 28.28')
#plt.text(1.75, 28.3, 'Expected Absolute Speed = 28.28', color='red', fontsize=12)
plt.axhline(y=17.89, color='black', linestyle='--', label='Y = 17.89')
plt.text(1.75, 17.90, 'Expected Absolute Speed = 17.89', color='black', fontsize=10)

plt.ylim(17.8, 19)
# Add labels and title
plt.xlabel('Image & Boat No.')
plt.ylabel('Absolute Speed')
plt.title('Speed test 2(Absolute Speed)')

# Show the plot
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()  # Ensures labels fit within the figure area
plt.show()

import matplotlib.pyplot as plt


categories = ['I2B1', 'I2B2', 'I2B3', 'I3B1','I3B2', 'I3B3', 'I4B1', 'I4B2','I4B3', 'I5B1', 'I5B2', 'I5B3']
values = [8.86, 9.04, 8.94, 8.85, 8.90, 8.71, 9.03, 8.93, 9.15, 9.06, 9.04, 8.85]

# Create a bar chart
plt.figure(figsize=(8, 6))
plt.bar(categories, values, color='darkslateblue', width = 0.4)
plt.axhline(y=8.94, color='red', linestyle='--', label='Y = 8.94')
plt.text(2.25, 8.95, 'Expected Apparent Speed = 8.94', color='red', fontsize=12)
plt.ylim(8.70, 9.16)
# Add labels and title
plt.xlabel('Image & Boat No.')
plt.ylabel('Apparent Speed')
plt.title('Speed test 1 (Apparent Speed)')

# Show the plot
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()  # Ensures labels fit within the figure area
plt.show()

import matplotlib.pyplot as plt


categories = ['I2B1', 'I2B2', 'I2B3', 'I3B1','I3B2', 'I3B3']
values_ap2 = [32.06,32.08,32.3,32.16,32.0,32.74]

# Create a bar chart
plt.figure(figsize=(8, 6))
plt.bar(categories, values_ap2, color='darkslateblue', width = 0.4)
plt.axhline(y=32.06, color='red', linestyle='--', label='Y = 32.06')
plt.text(-0.4, 32.1, 'Expected Apparent Speed = 32.06', color='red', fontsize=12)
plt.ylim(31.9, 32.8)
# Add labels and title
plt.xlabel('Image & Boat No.')
plt.ylabel('Apparent Speed')
plt.title('Speed test 2 (Apparent Speed)')

# Show the plot
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()  # Ensures labels fit within the figure area
plt.show()

original_value = 28.28
values = [28.2, 28.34, 28.3, 28.2, 28.26, 28.03, 28.38, 28.26, 28.5, 28.36, 28.38, 28.2]

percentage_accuracy = [(100-abs((value - original_value) / original_value * 100)) for value in values]

original_value2 = 17.89
values_d2 = [18.86,18.93, 18.94, 18.96, 18.84, 18.66]

percentage_accuracy2 = [(100-abs((value2 - original_value2) / original_value2 * 100)) for value2 in values_d2]

#print(percentage_accuracy)

plt.figure(figsize=(8, 6))
plt.plot(range(len(values)), percentage_accuracy, marker='o', linestyle='', markersize=10, color='darkslateblue')
plt.plot(range(len(values_d2)), percentage_accuracy2, marker='x', linestyle='', markersize=10, color='red')

plt.text(-0.4, 98.5, 'Accuracy % for speed test 1', color='darkslateblue', fontsize=12)
plt.text(-0.4, 95.2, 'Accuracy % for speed test 2', color='red', fontsize=12)
# Add labels and title
plt.xlabel('Data Points')
plt.ylabel('Percentage Accuracy (%)')
plt.title('Percentage Accuracy of Absolute Speed')

# Show the plot
plt.xticks(range(len(values)), range(1, len(values) + 1))  # Label x-axis with data point numbers
plt.grid(axis='y', linestyle='--', alpha=0.5)  # Add grid lines for better readability
plt.tight_layout()
plt.show()

original_value = 8.94
values = [8.86, 9.04, 8.94, 8.85, 8.90, 8.71, 9.03, 8.93, 9.15, 9.06, 9.04, 8.85]

percentage_accuracy = [(100-abs((value - original_value) / original_value * 100)) for value in values]

original_value2 = 32.06
values_d2 = [32.06,32.08,32.3,32.16,32.0,32.74]

percentage_accuracy2 = [(100-abs((value2 - original_value2) / original_value2 * 100)) for value2 in values_d2]

#print(percentage_accuracy)

plt.figure(figsize=(8, 6))
plt.plot(range(len(values)), percentage_accuracy, marker='o', linestyle='', markersize=10, color='darkslateblue')
plt.plot(range(len(values_d2)), percentage_accuracy2, marker='x', linestyle='', markersize=10, color='red')

plt.text(5.4, 98.5, 'Accuracy % for speed test 1', color='darkslateblue', fontsize=12)
plt.text(-0.4, 99.5, 'Accuracy % for speed test 2', color='red', fontsize=12)
# Add labels and title
plt.xlabel('Data Points')
plt.ylabel('Percentage Accuracy (%)')
plt.title('Percentage Accuracy of Apparent Speed')

# Show the plot
plt.xticks(range(len(values)), range(1, len(values) + 1))  # Label x-axis with data point numbers
plt.grid(axis='y', linestyle='--', alpha=0.5)  # Add grid lines for better readability
plt.tight_layout()
plt.show()