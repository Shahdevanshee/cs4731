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
from moba import *

class MyMinion(Minion):

    def __init__(self, position, orientation, world, image = NPC, speed = SPEED, viewangle = 360, hitpoints = HITPOINTS, firerate = FIRERATE, bulletclass = SmallBullet):
        Minion.__init__(self, position, orientation, world, image, speed, viewangle, hitpoints, firerate, bulletclass)
        self.states = [Idle]
        ### Add your states to self.states (but don't remove Idle)
        ### YOUR CODE GOES BELOW HERE ###
        self.states += [Move, AttackTower, AttackBase]
        ### YOUR CODE GOES ABOVE HERE ###

    def start(self):
        Minion.start(self)
        self.changeState(Idle)





############################
### Idle
###
### This is the default state of MyMinion. The main purpose of the Idle state is to figure out what state to change to and do that immediately.

class Idle(State):

    def enter(self, oldstate):
        State.enter(self, oldstate)
        # stop moving
        self.agent.stopMoving()

    def execute(self, delta = 0):
        State.execute(self, delta)
        ### YOUR CODE GOES BELOW HERE ###
        closest = float("inf")
        target = None
        my_team = self.agent.getTeam()
        enemy_towers = self.agent.world.getEnemyTowers(my_team)
        enemy_bases = self.agent.world.getEnemyBases(my_team)
        if enemy_towers != None and len(enemy_towers) > 0:
            for key, tower in enumerate(enemy_towers):
                if distance(self.agent.getLocation(), tower.getLocation()) < closest:
                    target = tower
                    closest = distance(self.agent.getLocation(), target.getLocation())
        if target is not None:
            self.agent.changeState(Move, target, my_team, enemy_towers, enemy_bases)
        if enemy_towers is None or len(enemy_towers) == 0:
            if enemy_bases != None and len(enemy_bases) > 0:
                for key, base in enumerate(enemy_bases):
                    if distance(self.agent.getLocation(), base.getLocation()) < closest:
                        target = base
                        closest = distance(self.agent.getLocation(), target.getLocation())
            if target is not None:
                self.agent.changeState(Move, target, my_team, enemy_towers, enemy_bases)
        ### YOUR CODE GOES ABOVE HERE ###
        return None

##############################
### Taunt
###
### This is a state given as an example of how to pass arbitrary parameters into a State.
### To taunt someome, Agent.changeState(Taunt, enemyagent)

class Taunt(State):

    def parseArgs(self, args):
        self.victim = args[0]

    def execute(self, delta = 0):
        if self.victim is not None:
            print "Hey " + str(self.victim) + ", I don't like you!"
        self.agent.changeState(Idle)

##############################
### YOUR STATES GO HERE:


############################
### Move
###
###

class Move(State):
    def parseArgs(self, args):
        self.target = args[0]
        self.team = args[1]
        self.enemy_towers = args[2]
        self.enemy_bases = args[3]

    def enter(self, oldstate):
        self.agent.navigateTo(self.target.getLocation())

    def execute(self, delta = 0):
        # print 'getVisible()', self.agent.getVisible(), '\n'
        if self.agent.moveTarget is None and self.target is not None:
            self.agent.navigateTo(self.target.getLocation())
        for tower in self.enemy_towers:
            if tower in self.agent.getVisible() and distance(self.agent.getLocation(), tower.getLocation()) <= BULLETRANGE:
                self.agent.changeState(AttackTower, tower)
        for base in self.enemy_bases:
            if base in self.agent.getVisible() and distance(self.agent.getLocation(), base.getLocation()) <= BULLETRANGE:
                self.agent.changeState(AttackBase, base)
        # for enemy in self.agent.world.getEnemyNPCs(self.team):
        #     print 'enemy info', enemy, enemy in self.agent.getVisible(), '\n'
        #     if enemy in self.agent.getVisible(): #and distance(self.agent.getLocation(), base.getLocation()) <= BULLETRANGE:
        #         print '-------------- entering attack enemy --------------'
        #         self.agent.changeState(AttackEnemy, enemy, self.target, self.team, self.enemy_towers, self.enemy_bases)

############################
### AttackTower
###
###

class AttackTower(State):

    def parseArgs(self,args):
        self.tower = args[0]

    def enter(self, oldstate):
        # State.enter(self, oldstate)
        # stop moving
        self.agent.stopMoving()
        # return None

    def execute(self, delta = 0):
        ### YOUR CODE GOES BELOW HERE ###
        if not (self.tower in self.agent.getVisible() and distance(self.agent.getLocation(), self.tower.getLocation()) <= BULLETRANGE):
            self.agent.changeState(Idle)
        else:
            self.agent.turnToFace(self.tower.getLocation())
            self.agent.shoot()
        ### YOUR CODE GOES ABOVE HERE ###
        # return None


############################
### AttackBase
###
###

class AttackBase(State):

    def parseArgs(self,args):
        self.base = args[0]

    def enter(self, oldstate):
        # State.enter(self, oldstate)
        # stop moving
        self.agent.stopMoving()
        # return None

    def execute(self, delta = 0):
        ### YOUR CODE GOES BELOW HERE ###
        if not (self.base in self.agent.getVisible() and distance(self.agent.getLocation(), self.base.getLocation()) <= BULLETRANGE):
            self.agent.changeState(Idle)
        else:
            self.agent.turnToFace(self.base.getLocation())
            self.agent.shoot()
        if not self.base.isAlive():
            print '--------------- num spawned enemy base ----------------', self.base.numSpawned
        if self.agent.world.getBaseForTeam(self.agent.getTeam()) is not None:
            print '--------------- num spawned my base----------------', self.agent.world.getBaseForTeam(self.agent.getTeam()).numSpawned
        ### YOUR CODE GOES ABOVE HERE ###
        # return None


############################
### AttackEnemy
###
###

# class AttackEnemy(State):

#     def parseArgs(self,args):
#         self.enemy = args[0]
#         self.target = args[1]
#         self.team = args[2]
#         self.enemy_towers = args[3]
#         self.enemy_bases = args[4]

#     def enter(self, oldstate):
#         # State.enter(self, oldstate)
#         # stop moving
#         self.agent.stopMoving()
#         self.oldstate = oldstate
#         # return None

#     def execute(self, delta = 0):
#         ### YOUR CODE GOES BELOW HERE ###
#         if not (self.enemy in self.agent.getVisible() and distance(self.agent.getLocation(), self.enemy.getLocation()) <= BULLETRANGE):
#             # self.agent.changeState(Move, self.target, self.team, self.enemy_towers, self.enemy_bases)
#             # print 'nope'
#             State.enter(self, self.oldstate)
#         else:
#             self.agent.turnToFace(self.enemy.getLocation())
#             self.agent.shoot()
#         ### YOUR CODE GOES ABOVE HERE ###
#         # return None


