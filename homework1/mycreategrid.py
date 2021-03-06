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

import sys, pygame, math, numpy, random, time, copy
from pygame.locals import *

from constants import *
from utils import *
from core import *

# Creates a grid as a 2D array of True/False values (True =  traversable). Also returns the dimensions of the grid as a (columns, rows) list.
def myCreateGrid(world, cellsize):
    grid = None
    dimensions = (0, 0)
    ### YOUR CODE GOES BELOW HERE ###
    int_cellsize = int(cellsize)
    maxX = int(math.ceil(world.getDimensions()[0] / int_cellsize))
    maxY = int(math.ceil(world.getDimensions()[1] / int_cellsize))
    # print maxX, maxY
    # print world.getLines()
    dimensions = (maxX, maxY)

    # drawCross(world.debug, (620, 690))
    # drawCross(world.debug, (628, 698))
    # drawCross(world.debug, (635, 705))
    # drawCross(world.debug, (608, 684))
    # drawCross(world.debug, (980, 484))

    grid = numpy.ones((maxX, maxY), dtype=bool)
    # print world.getObstacles()[5].getLines()
    # drawCross(world.debug, (81, 38))
    # drawCross(world.debug, (119, 38))
    # for line in world.getObstacles()[5].getLines():
        # print line
        # x = getIntersectPoint((0, 38), (152, 38), line[0], line[1])
        # y = calculateIntersectPoint((0, 38), (152, 38), line[0], line[1])
        # z = rayTrace((76, 38), (114, 38), line)
        # print (line, ' intersects at ', z)
    # print rayTraceWorld((38, 76), (114, 76), world.getObstacles()[5].getLines()[2])
    # for obstacle in world.getObstacles():
        # print obstacle.getPoints()
        # for point in obstacle.getPoints():
            # print point
            # if point[0] == 114 or point[0] == 113:
                # print point

    for i in range(maxX):
        for j in range(maxY):
            xLoc = i * int_cellsize
            yLoc = j * int_cellsize
            # drawCross(world.debug, (xLoc, yLoc))
            # drawCross(world.debug, (xLoc + int_cellsize, yLoc))
            # drawCross(world.debug, (xLoc, yLoc + int_cellsize))
            # drawCross(world.debug, (xLoc + int_cellsize, yLoc + int_cellsize))
            for obstacle in world.getObstacles():
                # if withinRangeOfPoints((i, j), cellsize, obstacle.getPoints()):
                # if (isGood((i, j), world, cellsize)):
                if checkPoint(obstacle, xLoc, yLoc, int_cellsize):
                    grid[i][j] = False

                for line in obstacle.getLines():
                    # query = rayTrace((xLoc, yLoc), (xLoc + int_cellsize, yLoc), line) or rayTrace((xLoc, yLoc), (xLoc, yLoc + int_cellsize), line) or rayTrace((xLoc + int_cellsize, yLoc), (xLoc + int_cellsize, yLoc + int_cellsize), line) or rayTrace((xLoc, yLoc + int_cellsize), (xLoc + int_cellsize, yLoc + int_cellsize), line)
                # print line, query
                    if checkIntersection(line, xLoc, yLoc, int_cellsize) is not None:
                        # print ('before', grid[i][j])
                        # print ('this is the line you are looking for1', line)
                        grid[i][j] = False
                        # print ('after', grid[i][j])

                # if rayTraceWorld(xLoc, yLoc, world.getLines()) is not None:
                    # grid[i][j] = False
                # for point in obstacle.getPoints():

                    # grid[point[0]][point[1]] = False
    # print (grid)
    # print (grid[11][8])

    # print (grid[0][0])
    # print ('grid[620][690]', grid[620][690])
    # print ('grid[628][698]', grid[628][698])
    # print ('grid[635][705]', grid[635][705])
    ### YOUR CODE GOES ABOVE HERE ###
    return grid, dimensions


def checkPoint(obstacle, xLoc, yLoc, cellsize):
    # print (obstacle.getPoints())
    return \
    obstacle.pointInside((xLoc, yLoc)) or \
    obstacle.pointInside((xLoc + cellsize, yLoc)) or \
    obstacle.pointInside((xLoc, yLoc + cellsize)) or \
    obstacle.pointInside((xLoc + cellsize, yLoc + cellsize)) or \
    pointOnPolygon((xLoc, yLoc), obstacle.getPoints()) or \
    pointOnPolygon((xLoc + cellsize, yLoc), obstacle.getPoints()) or \
    pointOnPolygon((xLoc, yLoc + cellsize), obstacle.getPoints()) or \
    pointOnPolygon((xLoc + cellsize, yLoc + cellsize), obstacle.getPoints())


def checkIntersection(line, xLoc, yLoc, cellsize):
    return \
    rayTrace((xLoc, yLoc), (xLoc + cellsize, yLoc), line) or \
    rayTrace((xLoc, yLoc), (xLoc, yLoc + cellsize), line) or \
    rayTrace((xLoc + cellsize, yLoc), (xLoc + cellsize, yLoc + cellsize), line) or \
    rayTrace((xLoc, yLoc + cellsize), (xLoc + cellsize, yLoc + cellsize), line)


