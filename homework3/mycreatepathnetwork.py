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

    poly_lines = []

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
    return nodes, edges, polys


def checkTriangle(world, point1, point2, point3):
    return_list = []
    temp_list = [point1, point2, point3]
    for obstacle in world.getObstacles():
        for point in obstacle.getPoints():
            if pointInsidePolygonPoints(point, temp_list):
                return_list.append(temp_list)
    return return_list