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

    # triangle = [points[0], points[1], points[2]]
    # drawPolygon(triangle, world.debug, color=(0, 0, 0), width=1, center=False)
    # mid = lambda (x1, y1), (x2, y2): ((x1 + x2) / 2.0, (y1 + y2) / 2.0)
    # drawCross(world.debug, mid(points[0], points[1]))
    # drawCross(world.debug, mid(points[0], points[2]))
    # drawCross(world.debug, mid(points[2], points[1]))
    # for obstacle in obstacles:
    #     print pointInsidePolygonPoints(mid(points[0], points[1]), obstacle.getPoints())
    #     print pointInsidePolygonPoints(mid(points[0], points[2]), obstacle.getPoints())
    #     print pointInsidePolygonPoints(mid(points[2], points[1]), obstacle.getPoints())
    # poly_lines = []
    '''
    for p1 in points:
        for p2 in points:
            if p1 == p2:
                continue

            pip_flag = False
            mid = lambda (x1, y1), (x2, y2): ((x1 + x2) / 2.0, (y1 + y2) / 2.0)
            for obstacle in obstacles:
                if pointInsidePolygonPoints(mid(p1, p2), obstacle.getPoints()):
                    pip_flag = True
            if pip_flag:
                continue

            rt_flag = False
            for line in lines:
                if p1 in line or p2 in line:
                    continue
                inter = rayTrace(p1, p2, line)
                if inter is None:
                    continue
                else:
                    rt_flag = True
            if rt_flag:
                continue

            for p3 in points:
                if p1 == p3 or p2 == p3:
                    continue

                pip_flag_2 = False
                for obstacle in obstacles:
                    if pointInsidePolygonPoints(mid(p1, p3), obstacle.getPoints()):
                        pip_flag_2 = True
                if pip_flag_2:
                    continue

                pip_flag_3 = False
                for obstacle in obstacles:
                    if pointInsidePolygonPoints(mid(p2, p3), obstacle.getPoints()):
                        pip_flag_3 = True
                if pip_flag_3:
                    continue

                rt_flag_2 = False
                for line in lines:
                    if p1 in line or p3 in line:
                        continue
                    inter = rayTrace(p1, p3, line)
                    if inter is None:
                        continue
                    else:
                        rt_flag_2 = True
                if rt_flag_2:
                    continue

                rt_flag_3 = False
                for line in lines:
                    if p2 in line or p3 in line:
                        continue
                    inter = rayTrace(p2, p3, line)
                    if inter is None:
                        continue
                    else:
                        rt_flag_3 = True
                if rt_flag_3:
                    continue

                rt_flag_4 = False
                for line in poly_lines:
                    if p1 in line or p2 in line:
                        continue
                    inter = rayTrace(p1, p2, line)
                    if inter is None:
                        continue
                    else:
                        rt_flag_4 = True
                if rt_flag_4:
                    continue

                rt_flag_5 = False
                for line in poly_lines:
                    if p1 in line or p3 in line:
                        continue
                    inter = rayTrace(p1, p3, line)
                    if inter is None:
                        continue
                    else:
                        rt_flag_5 = True
                if rt_flag_5:
                    continue


                rt_flag_6 = False
                for line in poly_lines:
                    if p2 in line or p3 in line:
                        continue
                    inter = rayTrace(p2, p3, line)
                    if inter is None:
                        continue
                    else:
                        rt_flag_6 = True
                if rt_flag_6:
                    continue

                polys.append((p1, p2, p3))
    '''
    # return nodes, edges, polys
    ############################################################################
    # https://github.gatech.edu/whamrick3/homework2---navigation-mesh--path-network/blob/master/mycreatepathnetwork.py
    # https://github.gatech.edu/ywang438/gameAI/blob/master/mycreatepathnetwork.py
    # drawCross(world.debug, (300, 515))
'''
    pip_flag = True
    rt_flag = True
    for obstacle in obstacles:
        print '\n'
        print obstacle.getPoints()
        print '\n'
        # print points[2], points[len(points) - 3]
    #     if rayTraceWorld(points[0], points[len(points) - 3], obstacle.getLines()) is not None:
    #         rt_flag = False
    # print rt_flag
    ############################################################################
    ###pip_flag#################################################################
        for point in obstacle.getPoints():
            print 'point:', point
            print pointInsidePolygonPoints(point, [(0, 0), (1224, 900), (811, 396)])
            if pointInsidePolygonPoints(point, [(0, 0), (1224, 900), (811, 396)]) and point != (0, 0) and point != (811, 396) and point != (1224, 900):
                pip_flag = False
    print 'finally: ', pip_flag
    # if pip_flag:
    #     print pip_flag
    #     print not pointInsidePolygonPoints(point, [points[4], points[1], points[2]])
    #     print 'appended'
    #     polys.append([points[4], points[1], points[2]])
    ###pip_flag#################################################################
    ############################################################################
    for i in range(len(points)):
        for j in range(len(points)):
            for k in range(len(points)):
                # if i == j or i == k or j == k:
                #     continue
                if j > i and k > j:
                    # Making it a triangle
                    triangle = [points[i], points[j], points[k]]

                    rt_flag = True
                    for obstacle in obstacles:
                        if rayTraceWorldNoEndPoints(points[i], points[j], lines) is not None or rayTraceWorldNoEndPoints(points[i], points[k], lines) is not None or rayTraceWorldNoEndPoints(points[j], points[k], lines) is not None:
                            rt_flag = False

                    if rt_flag:
                        polys.append(triangle)

                    # pip_flag = True
                    # for obstacle in obstacles:
                    #     for point in obstacle.getPoints():
                    #         if triangle in polys:
                    #             if pointInsidePolygonPoints(point, triangle) and point != triangle[0] and point != triangle[1] and point != triangle[2]:
                    #                 pip_flag = False
                    # print pip_flag

                    # for triangle in polys:

                        # if pointInsidePolygonLines(triangle[0], obstacle.getLines()) and or pointInsidePolygonLines(triangle[1], obstacle.getLines()) or pointInsidePolygonLines(triangle[2], obstacle.getLines()):
                    #         pip_flag = False
                        # for obst_point in obstacle.getPoints():
                        #     print (triangle, obst_point, pointInsidePolygonPoints(obst_point, triangle))
                        #     if triangle[0] == obst_point or triangle[1] == obst_point or triangle[2] == obst_point:
                        #         continue
                        #     if pointInsidePolygonPoints(obst_point, triangle):
                        #         pip_flag = False
                    # if pip_flag:
                    #     print triangle
                    #     drawPolygon(triangle, world.debug, color=(0, 0, 0), width=10, center=False)
    temp = []

    for poly in polys:
        print poly
        pip_flag = True
        for obstacle in obstacles:
            for obst_point in obstacle.getPoints():
                print obst_point, pointInsidePolygonPoints(obst_point, poly) and obst_point != poly[0] and obst_point != poly[1] and obst_point != poly[2]
                if pointInsidePolygonPoints(obst_point, poly) and obst_point != poly[0] and obst_point != poly[1] and obst_point != poly[2]:
                    pip_flag = False
        print 'pip_flag', pip_flag, '\n'
        if pip_flag:
            temp.append(poly)
    print '\ntemp\n'
    polys = temp
    # poly = []
    # for item in temp:
    #     poly.append(item)
    # for item in poly:
    #     print item




    print '\npolys:'
    # for poly in polys:
        # if (1224, 0) in poly:
        #     continue
        # if (0, 0) not in poly:
        #     continue
        # if (1224, 900) not in poly:
        #     continue
        # if (0, 900) in poly:
        #     continue
        # if (628, 698) not in poly:
        #     continue
        # if (554, 566) not in poly:
        #     continue
        # if (942, 484) not in poly:
        #     continue
        # if (811, 396) not in poly:
        #     continue
        # print poly
    drawPolygon([(0, 0), (1224, 900), (811, 396)], world.debug, color=(0, 0, 0), width=10, center=False)
    # drawCross(world.debug, (628, 698))
    # drawCross(world.debug, (582, 717))
    # drawCross(world.debug, (549, 688))
    # drawCross(world.debug, (554, 566))
    # drawCross(world.debug, (676, 548))
    # drawPolygon(poly, screen, color = (0, 0, 0), width = 1, center = False):
    # p = [(0, 900), (381, 490), (811, 396)]


    # drawPolygon(p, world.debug, color=(255, 0, 0), width=4, center=False)
    print len(polys)
    '''

    ############################################################################
    ############################################################################
    #             pip_flag = True
    #             for obstacle in obstacles:
    #                 for point in obstacle.getPoints():
    #                     if pointInsidePolygonPoints(point, triangle):
    #                         pip_flag = False
    #             if pip_flag:
    #                 polys.remove(triangle)
    ############################################################################

    #             for obstacle in world.getObstacles():
    #                 if point1 in obstacle.getPoints() or point2 in obstacle.getPoints() or point3 in obstacle.getPoints():
    #                     print (point1, point2, point3)
    #                 if rayTraceWorld(point1, point2, obstacle.getLines()) is not None:
    #                     continue
    #                 elif rayTraceWorld(point1, point3, obstacle.getLines()) is not None:
    #                     continue
    #                 elif rayTraceWorld(point2, point3, obstacle.getLines()) is not None:
    #                     continue
    #             # if rayTraceWorldNoEndPoints(point1, point2, lines) is not None:
    #             #     continue

                # temp_list = [point1, point2, point3]
                # for obstacle in world.getObstacles():
                #     for point in obstacle.getPoints():
                #         if not pointInsidePolygonPoints(point, temp_list):
                #             polys.append(temp_list)
    # print (points[0])
    # print (points[1])
    # print (points[2])
    # list_mine = [points[0], points[1], points[2]]
    # print (isConvex(list_mine))
    # for obstacle in world.getObstacles():
    #     for point in obstacle.getPoints():
    #         if pointInsidePolygonPoints(point, list_mine):
    #             print obstacle
    # polys.append(list_mine)
    ### YOUR CODE GOES ABOVE HERE ###
    # return nodes, edges, polys
# Creates a pathnode network that connects the midpoints of each navmesh together
'''
def myCreatePathNetwork(world, agent = None):
    nodes = []
    edges = []
    polys = []
    # ## YOUR CODE GOES BELOW HERE ###
    polys = findTriangles(world)
    polys = mergePolys(polys)
    for poly in polys:
        drawPolygon(poly, world.debug, (255, 0, 0), 1, True)


    ### YOUR CODE GOES ABOVE HERE ###
    return nodes, edges, polys

def findTriangles(world):
    obstacles = world.getObstacles()
    lines = world.getLines()
    points = world.getPoints()
    print points

    polylines = []
    polys = []
    ## find convex hulls ##
    # find triangles #
    for p1 in world.getPoints():
        for p2 in world.getPoints():
            if p1 == p2: continue
            if checkWithinObstacle(p1, p2, obstacles):
                print 0
                continue
            if crossExceptCorner(p1, p2, lines):
                print 1
                continue
            for p3 in world.getPoints():
                if p1 == p3 or p2 == p3: continue
                #make sure that the three formed lines are not within an obstacle
                if checkWithinObstacle(p3, p2, obstacles) or checkWithinObstacle(p3, p1, obstacles):
                    print 0
                    continue
                #not cross any existing lines
                if crossExceptCorner(p1, p3, lines) or crossExceptCorner(p2, p3, lines):
                    #drawPolygon([p1,p2,p3], world.debug, (255,0,0), 1, False)
                    print 1
                    continue
                #not cross any formed polygon/triangles
                if crossExceptCorner(p1, p2, polylines) or crossExceptCorner(p1, p3, polylines) or crossExceptCorner(p2, p3, polylines):
                    print 2
                    continue
                # #no obstacles within the triangle
                # flag3 = True
                # for point in points:
                #   if pointInsidePolygonPoints(point,(p1,p2,p3)):
                #       flag3 = False
                #       break
                # if flag3==False:
                #   print 3
                #   continue
                #add triangle
                polys.append((p1, p2, p3))
                polylines += [(p1, p2), (p2, p3), (p1, p3)]
            #drawPolygon([p1,p2,p3], world.debug, (0,255,0), 1, True)
    return polys

def mergePolys(polys):
    print len(polys)
    while True:
        size = len(polys)
        for poly1 in polys:
            flag = False
            for poly2 in polys:
                if poly2 == poly1: continue
                points = polygonsAdjacent(poly1, poly2)
                if points != False:
                    merged = list(set(list(poly1) + list(poly2)))
                    if isConvex(merged):
                        print (poly1, poly2)
                        polys.remove(poly1)
                        polys.remove(poly2)
                        polys.append(tuple(merged))
                        flag = True
                        break
            if flag == True:
                break

        if size == len(polys):
            break
    print len(polys)
    return polys

# Returns True if any of the formed lines are within an obstacle
def checkWithinObstacle(p1, p2, obstacles):
    mid = lambda (x1, y1), (x2, y2): ((x1 + x2) / 2.0, (y1 + y2) / 2.0);
    for obstacle in obstacles:
        if pointInsidePolygonPoints(mid(p1, p2), obstacle.getPoints()):
            return True

    return False

#Returns True if the line(p1,p2) crosses one of the lines at intermediate point
def crossExceptCorner(p1, p2, lines):
    for (p3, p4) in lines:
        if p1 in (p3, p4) or p2 in (p3, p4):
            continue
        inter = calculateIntersectPoint(p1, p2, p3, p4)
        if inter == None:
            continue
        else:
            # print (p1,p2,p3,p4)
            # print (inter)
            return True
    return False

def checkTriangle(world, point1, point2, point3):
    return_list = []
    temp_list = [point1, point2, point3]
    for obstacle in world.getObstacles():
        for point in obstacle.getPoints():
            if pointInsidePolygonPoints(point, temp_list):
                return_list.append(temp_list)
    return return_list
'''