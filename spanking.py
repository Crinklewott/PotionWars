
"""
Copyright 2014 Andrew Russell

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

LEATHER_STRAP_SEVERITY = 4
CANE_SEVERITY = 6

allSpankingPositions = {}
class SpankingPosition(object):
    def __init__(self, name, description, difficulty=1, maintainability=1, reversalRate=1):
        self.name = name
        self.description = description
        self.difficulty = difficulty
        self.maintainability = maintainability
        self.reversalRate = reversalRate
        global allSpankingPositions
        allSpankingPositions[name] = self

    def _save(self):
        return NotImplementedError()

    def _load(dataList):
        return NotImplementedError()


class Implement(items.Item):
    """
    Spanking implements. Once (if) I've implemented the ability to use an implement in combat, severity will give a bonus to the duration of the Humiliation status.
    """
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, severity=0):
        super(Implement, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense)
        self.severity = severity


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



