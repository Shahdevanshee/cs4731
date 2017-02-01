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
    ############################################################################
    # drawCross(world.debug, (300, 515))
    pip_flag = True
    rt_flag = True
    for obstacle in obstacles:
        print obstacle.getPoints()
        # print points[2], points[len(points) - 3]
        if rayTraceWorld(points[0], points[len(points) - 3], obstacle.getLines()) is not None:
            rt_flag = False
    print rt_flag
    ############################################################################
    ###pip_flag#################################################################
        # for point in obstacle.getPoints():
            # print not pointInsidePolygonPoints(point, [points[4], points[1], points[2]])
    #         if not pointInsidePolygonPoints(point, [points[4], points[1], points[2]]):
    #             pip_flag = False
    # if pip_flag:
    #     print pip_flag
    #     print not pointInsidePolygonPoints(point, [points[4], points[1], points[2]])
    #     print 'appended'
    #     polys.append([points[4], points[1], points[2]])
    ###pip_flag#################################################################
    ############################################################################
    for point1 in points:
        for point2 in points:
            for point3 in points:
                if point1 == point2 or point1 == point3 or point2 == point3:
                    continue
                # Making it a triangle
                triangle = [point1, point2, point3]
                rt_flag = True
                pip_flag = True
                for obstacle in obstacles:
                    if rayTraceWorldNoEndPoints(point1, point2, obstacle.getLines()) is not None or rayTraceWorldNoEndPoints(point1, point3, obstacle.getLines()) is not None or rayTraceWorldNoEndPoints(point2, point3, obstacle.getLines()) is not None:
                        rt_flag = False
                    # if point1 in obstacle.getPoints() and point2 in obstacle.getPoints() and point3 in obstacle.getPoints():
                    #     rt_flag = False

                #     for obst_point in obstacle.getPoints():
                #         print (triangle, obst_point, pointInsidePolygonPoints(obst_point, triangle))
                #         if pointInsidePolygonPoints(obst_point, triangle):
                #             pip_flag = False
                # print (rt_flag, pip_flag)

                if rt_flag and pip_flag:
                    polys.append(triangle)
    print '\npolys:'
    for poly in polys:
        if (1224, 0) in poly:
            continue
        if (0, 0) in poly:
            continue
        if (1224, 900) in poly:
            continue
        if (0, 900) in poly:
            continue
        # if (628, 698) not in poly:
        #     continue
        # if (582, 717) not in poly:
            # continue
        # print poly
    # drawCross(world.debug, (628, 698))
    # drawCross(world.debug, (582, 717))
    # drawCross(world.debug, (549, 688))
    # drawCross(world.debug, (554, 566))
    # drawCross(world.debug, (676, 548))
    print len(polys)

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