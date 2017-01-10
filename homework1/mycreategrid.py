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
    # grid[0][0] = True
    # dimensions = (1, 1)
    # print ('points', world.getPoints())
    points_list = world.getPoints()
    maxX = points_list[0][0]
    maxY = points_list[0][1]
    for item in points_list:
        if (item[0] > maxX and item[1] > maxY):
            maxX = item[0]
            maxY = item[1]
    dimensions = (maxX, maxY)
    print ('lines', world.getLines())
    # print ('lines w/o borders', world.getLinesWithoutBorders())
    # print ('obstacles', world.getObstacles())
    drawCross(world.debug, (0, 0))
    drawCross(world.debug, (1024, 0))
    drawCross(world.debug, (1024, 768))
    drawCross(world.debug, (0, 768))
    drawCross(world.debug, (628, 698))
    drawCross(world.debug, (582, 717))
    drawCross(world.debug, (549, 688))
    drawCross(world.debug, (554, 546))
    drawCross(world.debug, (676, 548))
    drawCross(world.debug, (942, 484))
    drawCross(world.debug, (811, 396))
    drawCross(world.debug, (843, 299))
    drawCross(world.debug, (921, 300))
    drawCross(world.debug, (457, 422))
    drawCross(world.debug, (371, 506))
    drawCross(world.debug, (300, 515))
    drawCross(world.debug, (300, 400))
    drawCross(world.debug, (454, 350))
    drawCross(world.debug, (425, 325))

    ### YOUR CODE GOES ABOVE HERE ###
    return grid, dimensions

