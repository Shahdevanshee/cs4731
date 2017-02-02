'''
 * Copyright (c) 2014, 2015 Entertainment Intelligence Lab, Georgia Institute of Technology.
 * Originally developed by Mark Riedl.
 * Last edited by Mark Riedl 05/2015
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

import sys, pygame, math, numpy, random, time, copy, operator
from pygame.locals import *

from constants import *
from utils import *
from core import *

# Creates a pathnode network that connects the midpoints of each navmesh together
def myCreatePathNetwork(world, agent = None):
    nodes = []
    edges = []
    polys = []
    ### YOUR CODE GOES BELOW HERE ###
    points = world.getPoints()
    lines = world.getLines()
    obstacles = world.getObstacles()
    print points
    print lines
    temp = []
    for p1 in points:
        for p2 in points:
            if p1 == p2:
                continue
            if isValid(lines, p1, p2):
                for p3 in points:
                    if p1 == p3 or p2 == p3:
                        continue
                    # print isValid(lines, p1, p3) and isValid(lines, p2, p3)
                    if isValid(lines, p1, p3) and isValid(lines, p2, p3):
                        temp.append(list((p1, p2, p3)))

    # Get rid of duplicates
    for t in temp:
        t.sort()
        if t not in polys:
            polys.append(t)

    # Get rid of polys with obstacles connected pt. 1
    # Problematic for runrandomnavigator2.py
    temp = []
    for p in polys:
        if not validPoly(obstacles, p[0], p[1]):
            continue
        if not validPoly(obstacles, p[0], p[2]):
            continue
        if not validPoly(obstacles, p[1], p[2]):
            continue
        temp.append(p)

    # Reassign polys correct values
    polys = temp

    print len(polys)
    rem_list = []
    for p in polys:
        print '\npoly: ---> ', p
        for obstacle in obstacles:
            print '\n', obstacle.getPoints()
            count = 0
            for pt in obstacle.getPoints():
                print pointInsidePolygonPoints(pt, p)
                if not pointInsidePolygonPoints(pt, p):
                    continue
                else:
                    count += 1
            if count == len(obstacle.getPoints()):
                rem_list.append(p)

        # if (0, 0) not in p:
        #     continue
        # if (921, 300) not in p:
        #     continue
        # if (1224, 900) not in p:
        #     continue
        # drawPolygon(p, world.debug, color=(0,0,0), width=5, center=False)

    print len(rem_list)
    for rem in rem_list:
        print rem
        if (0, 0) not in rem:
            continue
        if (300, 515) not in rem:
            continue
        drawPolygon(rem, world.debug, color=(0,0,0), width=5, center=False)
        # polys.remove(rem)

    return nodes, edges, polys

def isValid(lines, p1, p2):
    # print rayTraceWorld(p1, p2, obstacle.getLines())
    if rayTraceWorldNoEndPoints(p1, p2, lines) is not None:
        return False
    return True

def validPoly(obstacles, p1, p2):
    midpoint_x = (p1[0] + p2[0]) / 2
    midpoint_y = (p1[1] + p2[1]) / 2
    for obstacle in obstacles:
        if pointInsidePolygonLines((midpoint_x, midpoint_y), obstacle.getLines()):
            return False
    return True
