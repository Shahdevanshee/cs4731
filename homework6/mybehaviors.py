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
from moba2 import *
from btnode import *

###########################
### SET UP BEHAVIOR TREE


def treeSpec(agent):
    myid = str(agent.getTeam())
    spec = None
    ### YOUR CODE GOES BELOW HERE ###

    ### YOUR CODE GOES ABOVE HERE ###
    return spec

def myBuildTree(agent):
    myid = str(agent.getTeam())
    root = None
    ### YOUR CODE GOES BELOW HERE ###
    root = makeNode(SuperRoot, agent, "root")
    sel_1 = makeNode(Selector, agent, "sel_1")
    retreat = makeNode(Retreat, agent, 0.5, "retreat")
    hp_daemon = makeNode(HitpointDaemon, agent, 0.5, "hp_daemon")
    sel_2 = makeNode(Selector, agent, "hero_minion_sel")
    bf_daemon = makeNode(BuffDaemon, agent, 1, "bf_daemon")
    seq_hero = makeNode(Sequence, agent, "hero_seq")
    chase_hero = makeNode(ChaseHero, agent, "chase_hero")
    kill_hero = makeNode(KillHero, agent, "kill_hero")
    seq_minion = makeNode(Sequence, agent, "minion_seq")
    chase_minion = makeNode(ChaseMinion, agent, "chase_minion")
    kill_minion = makeNode(KillMinion, agent, "kill_minion")
    root.addChild(sel_1)
    sel_1.addChild(retreat)
    sel_1.addChild(hp_daemon)
    hp_daemon.addChild(sel_2)
    sel_2.addChild(bf_daemon)
    sel_2.addChild(seq_minion)
    bf_daemon.addChild(seq_hero)
    seq_hero.addChild(chase_hero)
    seq_hero.addChild(kill_hero)
    seq_minion.addChild(chase_minion)
    seq_minion.addChild(kill_minion)
    ### YOUR CODE GOES ABOVE HERE ###
    return root

### Helper function for making BTNodes (and sub-classes of BTNodes).
### type: class type (BTNode or a sub-class)
### agent: reference to the agent to be controlled
### This function takes any number of additional arguments that will be passed to the BTNode and parsed using BTNode.parseArgs()
def makeNode(type, agent, *args):
    node = type(agent, args)
    return node

###############################
### BEHAVIOR CLASSES:


##################
### Taunt
###
### Print disparaging comment, addressed to a given NPC
### Parameters:
###   0: reference to an NPC
###   1: node ID string (optional)

class Taunt(BTNode):

    ### target: the enemy agent to taunt

    def parseArgs(self, args):
        BTNode.parseArgs(self, args)
        self.target = None
        # First argument is the target
        if len(args) > 0:
            self.target = args[0]
        # Second argument is the node ID
        if len(args) > 1:
            self.id = args[1]

    def execute(self, delta = 0):
        ret = BTNode.execute(self, delta)
        if self.target is not None:
            print "Hey", self.target, "I don't like you!"
        return ret

##################
### MoveToTarget
###
### Move the agent to a given (x, y)
### Parameters:
###   0: a point (x, y)
###   1: node ID string (optional)

class MoveToTarget(BTNode):

    ### target: a point (x, y)

    def parseArgs(self, args):
        BTNode.parseArgs(self, args)
        self.target = None
        # First argument is the target
        if len(args) > 0:
            self.target = args[0]
        # Second argument is the node ID
        if len(args) > 1:
            self.id = args[1]

    def enter(self):
        BTNode.enter(self)
        self.agent.navigateTo(self.target)

    def execute(self, delta = 0):
        ret = BTNode.execute(self, delta)
        if self.target == None:
            # failed executability conditions
            print "exec", self.id, "false"
            return False
        elif distance(self.agent.getLocation(), self.target) < self.agent.getRadius():
            # Execution succeeds
            print "exec", self.id, "true"
            return True
        else:
            # executing
            return None
        return ret

##################
### Retreat
###
### Move the agent back to the base to be healed
### Parameters:
###   0: percentage of hitpoints that must have been lost to retreat
###   1: node ID string (optional)


class Retreat(BTNode):

    ### percentage: Percentage of hitpoints that must have been lost

    def parseArgs(self, args):
        BTNode.parseArgs(self, args)
        self.percentage = 0.5
        # First argument is the factor
        if len(args) > 0:
            self.percentage = args[0]
        # Second argument is the node ID
        if len(args) > 1:
            self.id = args[1]

    def enter(self):
        BTNode.enter(self)
        self.agent.navigateTo(self.agent.world.getBaseForTeam(self.agent.getTeam()).getLocation())

    def execute(self, delta = 0):
        ret = BTNode.execute(self, delta)
        if self.agent.getHitpoints() > self.agent.getMaxHitpoints() * self.percentage:
            # fail executability conditions
            print "exec", self.id, "false"
            return False
        elif self.agent.getHitpoints() == self.agent.getMaxHitpoints():
            # Exection succeeds
            print "exec", self.id, "true"
            return True
        else:
            # executing
            return None
        return ret

##################
### ChaseMinion
###
### Find the closest minion and move to intercept it.
### Parameters:
###   0: node ID string (optional)


class ChaseMinion(BTNode):

    ### target: the minion to chase
    ### timer: how often to replan

    def parseArgs(self, args):
        BTNode.parseArgs(self, args)
        self.target = None
        self.timer = 50
        # First argument is the node ID
        if len(args) > 0:
            self.id = args[0]

    def enter(self):
        BTNode.enter(self)
        self.timer = 50
        enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
        if len(enemies) > 0:
            best = None
            dist = 0
            for e in enemies:
                if isinstance(e, Minion):
                    d = distance(self.agent.getLocation(), e.getLocation())
                    if best == None or d < dist:
                        best = e
                        dist = d
            self.target = best
        if self.target is not None:
            navTarget = self.chooseNavigationTarget()
            if navTarget is not None:
                self.agent.navigateTo(navTarget)


    def execute(self, delta = 0):
        ret = BTNode.execute(self, delta)
        if self.target == None or self.target.isAlive() == False:
            # failed execution conditions
            print "exec", self.id, "false"
            return False
        elif distance(self.agent.getLocation(), self.target.getLocation()) < BIGBULLETRANGE:
            # succeeded
            print "exec", self.id, "true"
            return True
        else:
            # executing
            self.timer = self.timer - 1
            if self.timer <= 0:
                self.timer = 50
                navTarget = self.chooseNavigationTarget()
                if navTarget is not None:
                    self.agent.navigateTo(navTarget)
            return None
        return ret

    def chooseNavigationTarget(self):
        if self.target is not None:
            return self.target.getLocation()
        else:
            return None

##################
### KillMinion
###
### Kill the closest minion. Assumes it is already in range.
### Parameters:
###   0: node ID string (optional)


class KillMinion(BTNode):

    ### target: the minion to shoot

    def parseArgs(self, args):
        BTNode.parseArgs(self, args)
        self.target = None
        # First argument is the node ID
        if len(args) > 0:
            self.id = args[0]

    def enter(self):
        BTNode.enter(self)
        self.agent.stopMoving()
        enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
        if len(enemies) > 0:
            best = None
            dist = 0
            for e in enemies:
                if isinstance(e, Minion):
                    d = distance(self.agent.getLocation(), e.getLocation())
                    if best == None or d < dist:
                        best = e
                        dist = d
            self.target = best


    def execute(self, delta = 0):
        ret = BTNode.execute(self, delta)
        if self.target == None or distance(self.agent.getLocation(), self.target.getLocation()) > BIGBULLETRANGE:
            # failed executability conditions
            print "exec", self.id, "false"
            return False
        elif self.target.isAlive() == False:
            # succeeded
            print "exec", self.id, "true"
            return True
        else:
            # executing
            self.shootAtTarget()
            return None
        return ret

    def shootAtTarget(self):
        if self.agent is not None and self.target is not None:
            self.agent.turnToFace(self.target.getLocation())
            self.agent.shoot()


##################
### ChaseHero
###
### Move to intercept the enemy Hero.
### Parameters:
###   0: node ID string (optional)

class ChaseHero(BTNode):

    ### target: the hero to chase
    ### timer: how often to replan

    def ParseArgs(self, args):
        BTNode.parseArgs(self, args)
        self.target = None
        self.timer = 50
        # First argument is the node ID
        if len(args) > 0:
            self.id = args[0]

    def enter(self):
        BTNode.enter(self)
        self.timer = 50
        enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
        for e in enemies:
            if isinstance(e, Hero):
                self.target = e
                navTarget = self.chooseNavigationTarget()
                if navTarget is not None:
                    self.agent.navigateTo(navTarget)
                return None


    def execute(self, delta = 0):
        ret = BTNode.execute(self, delta)
        if self.target == None or self.target.isAlive() == False:
            # fails executability conditions
            print "exec", self.id, "false"
            return False
        elif distance(self.agent.getLocation(), self.target.getLocation()) < BIGBULLETRANGE:
            # succeeded
            print "exec", self.id, "true"
            return True
        else:
            # executing
            self.timer = self.timer - 1
            if self.timer <= 0:
                navTarget = self.chooseNavigationTarget()
                if navTarget is not None:
                    self.agent.navigateTo(navTarget)
            return None
        return ret

    def chooseNavigationTarget(self):
        if self.target is not None:
            return self.target.getLocation()
        else:
            return None

##################
### KillHero
###
### Kill the enemy hero. Assumes it is already in range.
### Parameters:
###   0: node ID string (optional)


class KillHero(BTNode):

    ### target: the minion to shoot

    def ParseArgs(self, args):
        BTNode.parseArgs(self, args)
        self.target = None
        # First argument is the node ID
        if len(args) > 0:
            self.id = args[0]

    def enter(self):
        BTNode.enter(self)
        self.agent.stopMoving()
        enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
        for e in enemies:
            if isinstance(e, Hero):
                self.target = e
                return None

    def execute(self, delta = 0):
        ret = BTNode.execute(self, delta)
        if self.target == None or distance(self.agent.getLocation(), self.target.getLocation()) > BIGBULLETRANGE:
            # failed executability conditions
            if self.target == None:
                print "foo none"
            else:
                print "foo dist", distance(self.agent.getLocation(), self.target.getLocation())
            print "exec", self.id, "false"
            return False
        elif self.target.isAlive() == False:
            # succeeded
            print "exec", self.id, "true"
            return True
        else:
            #executing
            self.shootAtTarget()
            return None
        return ret

    def shootAtTarget(self):
        if self.agent is not None and self.target is not None:
            self.agent.turnToFace(self.target.getLocation())
            self.agent.shoot()


##################
### HitpointDaemon
###
### Only execute children if hitpoints are above a certain threshold.
### Parameters:
###   0: percentage of hitpoints that must have been lost to fail the daemon check
###   1: node ID string (optional)


class HitpointDaemon(BTNode):

    ### percentage: percentage of hitpoints that must have been lost to fail the daemon check

    def parseArgs(self, args):
        BTNode.parseArgs(self, args)
        self.percentage = 0.5
        # First argument is the factor
        if len(args) > 0:
            self.percentage = args[0]
        # Second argument is the node ID
        if len(args) > 1:
            self.id = args[1]

    def execute(self, delta = 0):
        ret = BTNode.execute(self, delta)
        if self.agent.getHitpoints() < self.agent.getMaxHitpoints() * self.percentage:
            # Check failed
            print "exec", self.id, "fail"
            return False
        else:
            # Check didn't fail, return child's status
            return self.getChild(0).execute(delta)
        return ret

##################
### BuffDaemon
###
### Only execute children if agent's level is significantly above enemy hero's level.
### Parameters:
###   0: Number of levels above enemy level necessary to not fail the check
###   1: node ID string (optional)

class BuffDaemon(BTNode):

    ### advantage: Number of levels above enemy level necessary to not fail the check

    def parseArgs(self, args):
        BTNode.parseArgs(self, args)
        self.advantage = 0
        # First argument is the advantage
        if len(args) > 0:
            self.advantage = args[0]
        # Second argument is the node ID
        if len(args) > 1:
            self.id = args[1]

    def execute(self, delta = 0):
        ret = BTNode.execute(self, delta)
        hero = None
        # Get a reference to the enemy hero
        enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
        for e in enemies:
            if isinstance(e, Hero):
                hero = e
                break
        if hero == None or self.agent.level <= hero.level + self.advantage:
            # fail check
            print "exec", self.id, "fail"
            return False
        else:
            # Check didn't fail, return child's status
            return self.getChild(0).execute(delta)
        return ret





#################################
### MY CUSTOM BEHAVIOR CLASSES
class SuperRoot(BTNode):
    def parseArgs(self, args):
        BTNode.parseArgs(self, args)
        # First argument is the node ID
        if len(args) > 0:
            self.id = args[0]


    def execute(self, delta):
        BTNode.execute(self, delta)

        ret = self.children[0].execute()

        attack_closest(self.agent)
        area_effect(self.agent)
        dodge_bullet(self.agent)

        return ret


def attack_closest(agent):
    if not agent.canfire:
        return False

    enemies = agent.world.getEnemyNPCs(agent.getTeam())

    if enemies is None or len(enemies) == 0:
        return False

    sorted_enemies = sort_enemies(agent, enemies)
    closest = sorted_enemies[0]

    if distance(agent.getLocation(), closest.getLocation()) <= BIGBULLETRANGE:
        agent.turnToFace(closest.getLocation())
        agent.shoot()
        return True

    return False


def area_effect(agent):
    if not agent.canAreaEffect():
        return False

    enemies = agent.world.getEnemyNPCs(agent.getTeam())

    if enemies is None or len(enemies) == 0:
        return False

    for enemy in enemies:
        return agent.areaEffect()

    return False


def dodge_bullet(agent):
    # if not agent.candodge:
    #     return False

    all_bullets = (agent.getVisibleType(Bullet))
    enemy_bullets = []
    sorted_enemy_bullets = []

    for b in all_bullets:
        if b.getOwner().getTeam() != agent.getTeam():
            enemy_bullets.append(b)

    sorted_enemy_bullets = sort_enemies(agent, enemy_bullets)

    for b in sorted_enemy_bullets:
        angle = math.radians(b.orientation)
        add_to_loc = (1000 * math.cos(angle), -1000 * math.sin(angle))
        trajectory_end = (b.getLocation()[0] + add_to_loc[0], b.getLocation()[1] + add_to_loc[1])
        if minimumDistance([b.getLocation(), trajectory_end], agent.getLocation()) < agent.getMaxRadius():
            return agent.dodge((angle + math.pi / 2))
        else:
            continue

    return False


def sort_enemies(agent, enemies):
    dist_dict = {}
    ret_list = []
    dist_list = []

    for e in enemies:
        dist = distance(agent.getLocation(), e.getLocation())
        dist_dict[e] = dist

    for k, v in sorted(dist_dict.iteritems(), key=lambda (k, v): (v, k)):
        ret_list.append(k)
        dist_list.append(v)

    return ret_list
