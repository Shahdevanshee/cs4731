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
    # https://github.gatech.edu/rmendes3/4731_1/blob/master/randomgridnavigator.py
    # https://github.gatech.edu/ywang438/gameAI/blob/master/mycreatepathnetwork.py
    print pathnodes
    for i, item in enumerate(pathnodes):
        print '-------- pathnode[' + str(i) + '] --------'
        for j, obstacle in enumerate(world.getObstacles()):
            print '-- obstacle ' + str(j) + ' --'
            append_flag = True
            if i == len(pathnodes) - 1:
                if rayTraceWorld(pathnodes[i], pathnodes[0], obstacle.getLines()) is not None:
                    append_flag = False
            else:
                if rayTraceWorld(pathnodes[i], pathnodes[i + 1], obstacle.getLines()) is not None:
                    append_flag = False
                    print pathnodes[i]
                    print pathnodes[i + 1]
                    print rayTraceWorld(pathnodes[i], pathnodes[i + 1], obstacle.getLines())
            if append_flag and i == len(pathnodes) - 1 and j == len(world.getObstacles()) - 1:
                lines.append((pathnodes[i], pathnodes[0]))
            elif append_flag and j == len(world.getObstacles()) - 1:
                lines.append((pathnodes[i], pathnodes[i + 1]))
        # print i
        # print item
        # print agent.getRadius()
        # print agent.getMaxRadius()
        # if i == len(pathnodes) - 1:
        #     lines.append((pathnodes[i], pathnodes[0]))
        # else:
        #     lines.append((pathnodes[i], pathnodes[i + 1]))
    ### YOUR CODE GOES ABOVE HERE ###
    return lines
