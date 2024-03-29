
"""
Copyright 2014, 2015 Andrew Russell

This file is part of PotionWars.
PotionWars is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PotionWars is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PotionWars.  If not, see <http://www.gnu.org/licenses/>.
"""
import items
import random
import universal
import positions

LEATHER_STRAP_SEVERITY = 4
CANE_SEVERITY = 6

allSpankingPositions = {}

OTK = 0 
STANDING = 1
ON_THE_GROUND = 2

implements = {}

def spanking_string(top, bottom, position):
    """
    For all spanking string functions:
    1. top is the character administering the spanking
    2. bottom is the character receiving the spanking.
    """
    #Only enemies contain spanking text
    try:
        return top.spanks(bottom, position)
    except NotImplementedError, AttributeError:
        return bottom.spanked_by(top, position)

def reversed_spanking(top, bottom, position):
    """
    For all spanking string functions:
    1. top is the character administering the spanking
    2. bottom is the character receiving the spanking.

    Note that in the case of a reversal, this means that the intended bottom is passed to this function as top, while the intended top is passed to this function as bottom.
    """
    try:
        return top.reverses(bottom, position)
    except (NotImplementedError, AttributeError):
        if bottom == universal.state.player:
            raise
        return bottom.reversed_by(top, position)

def continue_spanking(top, bottom, position):
    try:
        return top.continue_spanking(bottom, position)
    except (NotImplementedError, AttributeError):
        if bottom == universal.state.player:
            raise
        return bottom.continue_being_spanked(top, position)

def failed_spanking(top, bottom, position):
    try:
        return top.failed(bottom, position)
    except (NotImplementedError, AttributeError):
        if bottom == universal.state.player:
            raise
        return bottom.blocks(top, position)

class Implement(items.Item):
    """
    Spanking implements. Once (if) I've implemented the ability to use an implement in combat, severity will give a bonus to the duration of the Humiliation status.
    """
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, severity=0):
        super(Implement, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense)
        self.severity = severity
        implements[self.name] = self


    def display(self):
        displayString = super(Implement, self).display()    
        return '\n'.join([displayString, 'severity: ' + str(self.severity)])

    def is_combat_implement(self):
        return False


class CombatImplement(Implement):
    """
    Implements that can be used in combat (e.g. the wooden spoon). Some implements (such as the cane) just wouldn't work in the close quarters grappling that a combat
    spanking consists of.
    """
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, severity=0):
        super(CombatImplement, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, severity)
            
    def is_combat_implement(self):
        return True


hand = CombatImplement('hand', 'Your hand. It stings like the dickens.', severity=0)
