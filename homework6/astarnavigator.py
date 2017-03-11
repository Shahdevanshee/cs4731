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
from mycreatepathnetwork import *
from mynavigatorhelpers import *


###############################
### AStarNavigator
###
### Creates a path node network and implements the FloydWarshall all-pairs shortest-path algorithm to create a path to the given destination.

class AStarNavigator(NavMeshNavigator):

    def __init__(self):
        NavMeshNavigator.__init__(self)


    ### Create the pathnode network and pre-compute all shortest paths along the network.
    ### self: the navigator object
    ### world: the world object
    def createPathNetwork(self, world):
        self.pathnodes, self.pathnetwork, self.navmesh = myCreatePathNetwork(world, self.agent)
        return None

    ### Finds the shortest path from the source to the destination using A*.
    ### self: the navigator object
    ### source: the place the agent is starting from (i.e., it's current location)
    ### dest: the place the agent is told to go to
    def computePath(self, source, dest):
        ### Make sure the next and dist matricies exist
        if self.agent != None and self.world != None:
            self.source = source
            self.destination = dest
            ### Step 1: If the agent has a clear path from the source to dest, then go straight there.
            ###   Determine if there are no obstacles between source and destination (hint: cast rays against world.getLines(), check for clearance).
            ###   Tell the agent to move to dest
            ### Step 2: If there is an obstacle, create the path that will move around the obstacles.
            ###   Find the pathnodes closest to source and destination.
            ###   Create the path by traversing the self.next matrix until the pathnode closes to the destination is reached
            ###   Store the path by calling self.setPath()
            ###   Tell the agent to move to the first node in the path (and pop the first node off the path)
            if clearShot(source, dest, self.world.getLines(), self.world.getPoints(), self.agent):
                self.agent.moveToTarget(dest)
            else:
                start = findClosestUnobstructed(source, self.pathnodes, self.world.getLinesWithoutBorders())
                end = findClosestUnobstructed(dest, self.pathnodes, self.world.getLinesWithoutBorders())
                if start != None and end != None:
                    print len(self.pathnetwork)
                    newnetwork = unobstructedNetwork(self.pathnetwork, self.world.getGates())
                    print len(newnetwork)
                    closedlist = []
                    path, closedlist = astar(start, end, newnetwork)
                    if path is not None and len(path) > 0:
                        path = shortcutPath(source, dest, path, self.world, self.agent)
                        self.setPath(path)
                        if self.path is not None and len(self.path) > 0:
                            first = self.path.pop(0)
                            self.agent.moveToTarget(first)
        return None

    ### Called when the agent gets to a node in the path.
    ### self: the navigator object
    def checkpoint(self):
        myCheckpoint(self)
        return None

    ### This function gets called by the agent to figure out if some shortcutes can be taken when traversing the path.
    ### This function should update the path and return True if the path was updated.
    def smooth(self):
        return mySmooth(self)

    def update(self, delta):
        myUpdate(self, delta)


def unobstructedNetwork(network, worldLines):
    newnetwork = []
    for l in network:
        hit = rayTraceWorld(l[0], l[1], worldLines)
        if hit == None:
            newnetwork.append(l)
    return newnetwork




def astar(init, goal, network):
    path = []
    open = []
    closed = []
    ### YOUR CODE GOES BELOW HERE ###
    parent_dict = {}
    dist_dict = {init: 0}
    heuristic_dict = {init: dist_dict[init] + distance(init, goal)}
    open.append(init)

    while open:
        open = sort_open(open, heuristic_dict)
        current = open[0]

        if current != goal:
            open.remove(current)
            closed.append(current)

            neighbors = getNeighbors(current, network)
            for n in neighbors:
                if n not in closed:
                    dist = dist_dict[current] + distance(current, n)
                    if n not in open or dist < dist_dict[n]:
                        parent_dict[n] = current
                        dist_dict[n] = dist
                        heuristic_dict[n] = dist_dict[n] + distance(n, goal)
                        if n not in open:
                            open.append(n)

        else:
            path.append(current)
            while current in parent_dict:
                current = parent_dict[current]
                if current == init:
                    continue
                else:
                    path = [current] + path

            path = [init] + path
            break

    ### YOUR CODE GOES ABOVE HERE ###
    return path, closed


def sort_open(open, heuristic_dict):
    resorted = []
    temp = []
    for item in open:
        temp.append((item, heuristic_dict[item]))

    temp.sort(key=lambda x: x[1])
    for item in temp:
        resorted.append(item[0])
    return resorted


def getNeighbors(point, network):
    neighbors = []
    for item in network:
        if point in item and point == item[0] and item[1] not in neighbors:
            neighbors.append(item[1])
        elif point in item and point == item[1] and item[0] not in neighbors:
            neighbors.append(item[0])
    return neighbors


def myUpdate(nav, delta):
    ### YOUR CODE GOES BELOW HERE ###
    gates = nav.world.getGates()
    for gate in gates:
        if nav.getDestination() is None or rayTrace(nav.agent.getLocation(), nav.agent.moveTarget, gate) is not None or minimumDistance(gate, nav.agent.getLocation()) <= nav.agent.getMaxRadius():
            break
    nav.world.getAgent().stopMoving()
    nav.setPath(None)
    ### YOUR CODE GOES ABOVE HERE ###
    return None


def myCheckpoint(nav):
    ### YOUR CODE GOES BELOW HERE ###
    gates = nav.world.getGates()
    for gate in gates:
        if nav.getDestination() is None or rayTrace(nav.agent.getLocation(), nav.agent.moveTarget, gate) is not None or minimumDistance(gate, nav.agent.getLocation()) <= nav.agent.getMaxRadius():
            break
    nav.world.getAgent().stopMoving()
    nav.setPath(None)
    ### YOUR CODE GOES ABOVE HERE ###
    return None


### Returns true if the agent can get from p1 to p2 directly without running into an obstacle.
### p1: the current location of the agent
### p2: the destination of the agent
### worldLines: all the lines in the world
### agent: the Agent object
def clearShot(p1, p2, worldLines, worldPoints, agent):
    ### YOUR CODE GOES BELOW HERE ###
    if rayTraceWorldNoEndPoints(p1, p2, worldLines) is not None:
        return False
    else:
        for point in worldPoints:
            if minimumDistance((p1, p2), point) <= agent.getMaxRadius():
                return False
        return True
    ### YOUR CODE GOES ABOVE HERE ###
    return False
