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

# Creates the pathnetwork as a list of lines between all pathnodes that are traversable by the agent.
def myBuildPathNetwork(pathnodes, world, agent = None):
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
    for line in lines:
        for corner in corners:
            # print minimumDistance(line, corner), line, corner
            if minimumDistance(line, corner) < agent.getMaxRadius():
                if line in lines:
                    lines.remove(line)

    ### YOUR CODE GOES ABOVE HERE ###
    return lines
