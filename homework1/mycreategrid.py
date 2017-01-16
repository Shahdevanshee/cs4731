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
    maxX = int(math.ceil(world.dimensions[0] / int_cellsize))
    maxY = int(math.ceil(world.dimensions[1] / int_cellsize))
    print maxX, maxY
    dimensions = (maxX, maxY)

    drawCross(world.debug, (620, 690))
    drawCross(world.debug, (628, 698))
    drawCross(world.debug, (635, 705))
    drawCross(world.debug, (608, 684))
    drawCross(world.debug, (980, 484))

    grid = numpy.ones((maxX, maxY), dtype=bool)

    for i in range(maxX):
        for j in range(maxY):
            xLoc = i * int_cellsize
            yLoc = j * int_cellsize
            drawCross(world.debug, (xLoc, yLoc))
            # if i % int_cellsize == 0 and j % int_cellsize == 0:
            for obstacle in world.getObstacles():
                if obstacle.pointInside((xLoc, yLoc)):
                # if withinRangeOfPoints((i, j), cellsize, obstacle.getPoints()):
                # if (isGood((i, j), world, cellsize)):
                    grid[i][j] = False
    print (grid)

    # print (grid[0][0])
    # print ('grid[620][690]', grid[620][690])
    # print ('grid[628][698]', grid[628][698])
    # print ('grid[635][705]', grid[635][705])
    ### YOUR CODE GOES ABOVE HERE ###
    return grid, dimensions

