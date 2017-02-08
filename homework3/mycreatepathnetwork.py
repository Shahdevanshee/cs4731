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
    obstacles = world.getObstacles()
    temp = []
    for p1 in points:
        for p2 in points:
            for p3 in points:
                if p1 == p2 or p1 == p3 or p2 == p3:
                    continue
                if not checkCollision1(world, temp, p1, p2, p3) and not checkCollision2(world, obstacles, temp, p1, p2, p3):
                    temp.append(list((p1, p2, p3)))

    # Get rid of duplicates
    for t in temp:
        t.sort()
        if t not in polys:
            polys.append(t)

    for n in range(len(polys)):
        for p1 in polys:
            for p2 in polys:
                if p1 == p2:
                    continue
                if polygonsAdjacent(p1, p2):
                    # print p1, p2
                    merged = merge(p1, p2)
                    # print 'merged: ', merged
                    if isConvex(merged):
                        # drawPolygon(merged, world.debug, (0,0,0), 10, False)
                        polys.remove(p1)
                        polys.remove(p2)
                        polys.append(merged)
                        break

    for p1 in polys:
        temp = []
        for p2 in polys:
            if p1 == p2:
                continue
            common = polygonsAdjacent(p1, p2)
            if common:
                # common = commonPoints(p1, p2)
                # print 'common points: ', commonPoints(p1, p2)
                mid = midpt(common[0], common[1])
                temp.append(mid)
                if mid not in nodes:
                    nodes.append(mid)
                # drawCross(world.debug, mid)
        for i in range(len(temp)):
            if i == len(temp) - 1:
                if checkCollision3(obstacles, temp[i], temp[0], agent):
                    edges.append((temp[i], temp[0]))
            else:
                if checkCollision3(obstacles, temp[i], temp[i + 1], agent):
                    edges.append((temp[i], temp[i + 1]))
        # for obstacle in obstacles:
        #     for point in obstacle.getPoints():
        #         if minimumDistance()
        # print temp
    # for n1 in nodes:
    #     print n1
        # for n2 in nodes:
            # if n1 == n2:
                # continue


    # edges = myBuildPathNetwork(nodes, world, agent)
    # for edge in edges:
    #     print edge

    return nodes, edges, polys


def checkCollision1(world, polys, p1, p2, p3):
    lines = world.getLines()
    for p in polys:
        lines.append((p[0], p[1]))
        lines.append((p[0], p[2]))
        lines.append((p[1], p[2]))

    if (rayTraceWorldNoEndPoints(p2, p3, lines) is not None and (p2, p3) not in lines and (p3, p2) not in lines) or \
    (rayTraceWorldNoEndPoints(p1, p2, lines) is not None and (p1, p2) not in lines and (p2, p1) not in lines) or \
    (rayTraceWorldNoEndPoints(p1, p3, lines) is not None and (p1, p3) not in lines and (p3, p1) not in lines):
        return True

    return False


def checkCollision2(world, obstacles, polys, p1, p2, p3):
    lines = world.getLines()
    for p in polys:
        lines.append((p[0], p[1]))
        lines.append((p[0], p[2]))
        lines.append((p[1], p[2]))

    for obstacle in obstacles:
        mid1 = midpt(p2, p3)
        mid2 = midpt(p1, p2)
        mid3 = midpt(p1, p3)

        # Check our triangle inside any of the pre-made obstacles
        if (pointInsidePolygonLines(mid1, obstacle.getLines()) and (p2, p3) not in lines and (p3, p2) not in lines) or \
        (pointInsidePolygonLines(mid2, obstacle.getLines()) and (p1, p2) not in lines and (p2, p1) not in lines) or \
        (pointInsidePolygonLines(mid3, obstacle.getLines()) and (p1, p3) not in lines and (p3, p1) not in lines):
            return True

        # Check pre-made obstacles inside our triangle
        pts = obstacle.getPoints()

        center_x = 0
        center_y = 0

        for (x, y) in pts:
            center_x += x
            center_y += y

        center_x /= len(pts)
        center_y /= len(pts)

        if pointInsidePolygonPoints((center_x, center_y), (p1, p2, p3)):
            return True

    return False


def checkCollision3(obstacles, temp1, temp2, agent=None):
    for obstacle in obstacles:
        for point in obstacle.getPoints():
            if minimumDistance((temp1, temp2), point) <= agent.getMaxRadius():
                return False
    return True


def midpt(p1, p2):
    midX = ((p1[0] + p2[0]) / 2)
    midY = ((p1[1] + p2[1]) / 2)
    return (midX, midY)


def merge(poly1, poly2):
    pts = []
    for pt in poly1:
        pts.append(pt)
    for pt in poly2:
        if pt not in pts:
            pts.append(pt)

    # http://math.stackexchange.com/questions/1329128/
    # how-to-sort-vertices-of-a-polygon-in-counter-clockwise-order-computing-angle?noredirect=1&lq=1
    center_x = 0
    center_y = 0

    for (x, y) in pts:
        center_x += x
        center_y += y

    center_x /= len(pts)
    center_y /= len(pts)

    temp_dict = {}
    temp_list = []

    for (x, y) in pts:
        angle = math.atan2(center_y - y, center_x - x)
        temp_list.append(angle)
        temp_dict[angle] = (x, y)

    temp_list.sort()
    pts = []
    for item in temp_list:
        pts.append(temp_dict[item])

    return pts


def myBuildPathNetwork(pathnodes, world, agent=None):
    lines = []
    ### YOUR CODE GOES BELOW HERE ###

    # Append all possible lines to lines array
    for i in range(len(pathnodes)):
        for j in range(len(pathnodes)):
            # Limit number of responses so we have new instead of repeats
            if j > i:
                append_flag = True
                for obstacle in world.getObstacles():
                    if rayTraceWorld(pathnodes[i], pathnodes[j], obstacle.getLines()) is not None:
                        append_flag = False
                # Append only if no intersection
                if append_flag:
                    lines.append((pathnodes[i], pathnodes[j]))

    # Get list of points that make up obstacles
    corners = []
    for obstacle in world.getObstacles():
        for point in obstacle.getPoints():
            corners.append(point)

    # Checking min_dist
    bad_lines = []
    for line in lines:
        for corner in corners:
            if minimumDistance(line, corner) < agent.getMaxRadius():
                bad_lines.append(line)

    # Remove bad lines
    for line in bad_lines:
        if line in lines:
            lines.remove(line)

    ### YOUR CODE GOES ABOVE HERE ###
    return lines
